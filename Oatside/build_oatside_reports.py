"""
Build Oatside -> P&G trip summary from raw GPS workbooks (sheet อุปกรณ์),
write Oatside_PG_Trip_Summary_By_Site.xlsx + HTML under TransportRateCalculator/reports/oatside-apr2026.

Run from repo root:
  python Oatside/build_oatside_reports.py

Billing rules are read from Oatside/oatside_config.json (auto-created with defaults if missing).
Override JSON: Oatside/oatside_billing_overrides.json (or env OATSIDE_OVERRIDES_JSON).

Optional env:
  OATSIDE_ORIGIN        = path to Oatside point xlsx (else newest Y.K.*Oatside*.xlsx in Oatside/)
  OATSIDE_DEST          = path to P&G point xlsx (else newest Y.K.*P&G* or *เวลล์โกล*.xlsx)
  OATSIDE_MAX_TRAVEL_H  = overrides config max_travel_h (max hours Origin_Out->Dest_In for pairing)
  OATSIDE_OVERRIDES_JSON = optional path to billing overrides JSON
"""

from __future__ import annotations

import html as html_module
import math
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
import json
from typing import Any, Callable, Iterable

import openpyxl

BIGC_EXACT = frozenset({"71-5041", "71-5042"})
PLATE_HEAD = re.compile(r"^(\d{2}-\d{4})\b")
DETAIL_KEY = re.compile(r"^\d+\.\d+$")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

@dataclass
class OatsideConfig:
    trip_rates: list[dict]
    one_trip_surcharge_pct: float
    min_trips_per_truck: int
    max_travel_h: float
    max_origin_chain_gap_h: float
    enable_origin_chain_merge: bool
    charge_min_trip_shortfall: bool


_DEFAULT_CONFIG = OatsideConfig(
    trip_rates=[
        {"from": "2026-04-12", "to": "2026-04-15", "rate_baht": 8000},
        {"rate_baht": 7500},
    ],
    one_trip_surcharge_pct=50.0,
    min_trips_per_truck=2,
    max_travel_h=48.0,
    max_origin_chain_gap_h=3.0,
    enable_origin_chain_merge=False,
    charge_min_trip_shortfall=False,
)

_DEFAULT_CONFIG_JSON = {
    "version": 1,
    "_help": "แก้ไฟล์นี้เพื่อเปลี่ยนกฎการคิดเงิน แล้วรัน build_oatside_reports.py ใหม่",
    "trip_rates": [
        {"_note": "ช่วงวันที่พิเศษ (สงกรานต์ 2026)", "from": "2026-04-12", "to": "2026-04-15", "rate_baht": 8000},
        {"_note": "เรทปกติ (ใช้เมื่อไม่ตรงช่วงไหนข้างบน)", "rate_baht": 7500},
    ],
    "one_trip_surcharge_pct": 50,
    "min_trips_per_truck_per_day": 2,
    "max_travel_h": 48,
    "max_origin_chain_gap_h": 3,
    "_note_max_origin_chain_gap_h": "hours: max gap Origin_Out(prev)->Origin_In(next) for chain-merge; larger gap = new hub visit (only if enable_origin_chain_merge is true)",
    "enable_origin_chain_merge": False,
    "_note_enable_origin_chain_merge": "false = never merge multiple Origin rows before one Dest (disables merge_chained_origin_pairs entirely)",
    "charge_min_trip_shortfall": False,
    "_note_charge_min_trip_shortfall": "ถ้า false = ไม่เก็บเงินค่าชดเชยเที่ยวขาด (min trips) ในรายงานลูกค้า — ใช้ชาร์จ % วันละ 1 เที่ยวแทน | true = เก็บทั้งค่าชดเชย + % ตามเดิม",
}


def _config_path() -> Path:
    return _oatside_dir() / "oatside_config.json"


def load_oatside_config() -> OatsideConfig:
    """Load billing config from oatside_config.json; fall back to built-in defaults."""
    path = _config_path()
    if not path.is_file():
        # Write a default config so โอ can see/edit it
        try:
            path.write_text(json.dumps(_DEFAULT_CONFIG_JSON, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[INFO] สร้าง config เริ่มต้น: {path}")
        except OSError:
            pass
        return _DEFAULT_CONFIG

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print(f"[WARN] อ่าน {path} ไม่ได้ — ใช้ค่า default แทน")
        return _DEFAULT_CONFIG

    if not isinstance(raw, dict):
        return _DEFAULT_CONFIG

    trip_rates = raw.get("trip_rates", _DEFAULT_CONFIG.trip_rates)
    if not isinstance(trip_rates, list) or not trip_rates:
        trip_rates = _DEFAULT_CONFIG.trip_rates

    surcharge_pct = float(raw.get("one_trip_surcharge_pct", _DEFAULT_CONFIG.one_trip_surcharge_pct))
    min_trips = int(raw.get("min_trips_per_truck_per_day", _DEFAULT_CONFIG.min_trips_per_truck))

    env_travel = os.environ.get("OATSIDE_MAX_TRAVEL_H")
    if env_travel:
        try:
            max_travel = float(env_travel)
        except ValueError:
            max_travel = float(raw.get("max_travel_h", _DEFAULT_CONFIG.max_travel_h))
    else:
        max_travel = float(raw.get("max_travel_h", _DEFAULT_CONFIG.max_travel_h))

    charge_sf = bool(raw.get("charge_min_trip_shortfall", False))
    try:
        gap_h = float(raw.get("max_origin_chain_gap_h", _DEFAULT_CONFIG.max_origin_chain_gap_h))
    except (TypeError, ValueError):
        gap_h = float(_DEFAULT_CONFIG.max_origin_chain_gap_h)

    chain_merge = bool(raw.get("enable_origin_chain_merge", _DEFAULT_CONFIG.enable_origin_chain_merge))

    return OatsideConfig(
        trip_rates=trip_rates,
        one_trip_surcharge_pct=surcharge_pct,
        min_trips_per_truck=min_trips,
        max_travel_h=max_travel,
        max_origin_chain_gap_h=gap_h,
        enable_origin_chain_merge=chain_merge,
        charge_min_trip_shortfall=charge_sf,
    )


def trip_rate_baht(d: date, cfg: OatsideConfig) -> int:
    """Look up trip rate for a given Dest_In date using config rules (first match wins)."""
    for rule in cfg.trip_rates:
        frm = rule.get("from")
        to = rule.get("to")
        rate = rule.get("rate_baht")
        if rate is None:
            continue
        if frm and to:
            try:
                d_from = datetime.strptime(str(frm), "%Y-%m-%d").date()
                d_to = datetime.strptime(str(to), "%Y-%m-%d").date()
                if d_from <= d <= d_to:
                    return int(rate)
            except ValueError:
                continue
        else:
            return int(rate)
    return 7500


def config_rate_summary(cfg: OatsideConfig) -> str:
    """Human-readable summary of rate rules for subtitles/logs."""
    parts = []
    for rule in cfg.trip_rates:
        rate = rule.get("rate_baht")
        frm = rule.get("from")
        to = rule.get("to")
        if rate is None:
            continue
        if frm and to:
            parts.append(f"{frm}–{to}={rate:,}")
        else:
            parts.append(f"ปกติ={rate:,}")
    return " / ".join(parts) if parts else "7,500"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Leg:
    row_no: str
    plate: str
    device: str
    t_in: datetime
    t_out: datetime


@dataclass
class Trip:
    plate: str
    site: str
    device: str
    o_row: str
    d_row: str
    o_in: datetime
    o_out: datetime
    d_in: datetime
    d_out: datetime
    origin_wait_h: float
    travel_h: float
    dest_wait_h: float
    total_cycle_h: float
    origin_date: date
    dest_date: date
    trip_date: date
    travel_flag: str | None


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def _root() -> Path:
    here = Path(__file__).resolve().parent
    return here.parent if (here.parent / "TransportRateCalculator").is_dir() else here


def _oatside_dir() -> Path:
    return Path(__file__).resolve().parent


def _overrides_json_path() -> Path:
    v = os.environ.get("OATSIDE_OVERRIDES_JSON")
    if v:
        return Path(v)
    return _oatside_dir() / "oatside_billing_overrides.json"


# ---------------------------------------------------------------------------
# Overrides loader
# ---------------------------------------------------------------------------

def load_billing_overrides() -> dict[tuple[str, date], dict[str, Any]]:
    """Load manual billing actions keyed by (plate, dest_date).

    JSON shape (UTF-8):
      {"version": 1, "entries": [
        {"dest_date": "2026-04-14", "plate": "71-6802", "action": "exclude_50", "note": "..."},
        {"dest_date": "2026-04-20", "plate": "71-6001", "action": "include_50", "note": "..."}
      ]}

    - exclude_50: do not charge 50% even if auto rule would (exactly 1 matched trip that Dest_In day).
    - include_50: charge 50% of one trip rate that day even if auto rule would not (e.g. 2+ trips).
    """
    path = _overrides_json_path()
    out: dict[tuple[str, date], dict[str, Any]] = {}
    if not path.is_file():
        return out
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return out
    entries = raw.get("entries") if isinstance(raw, dict) else None
    if not isinstance(entries, list):
        return out
    for e in entries:
        if not isinstance(e, dict):
            continue
        ds = str(e.get("dest_date", "")).strip()[:10]
        plate = str(e.get("plate", "")).strip()
        action = str(e.get("action", "")).strip()
        note = str(e.get("note", "")).strip()
        if not ds or not plate or action not in ("exclude_50", "include_50"):
            continue
        try:
            d = datetime.strptime(ds, "%Y-%m-%d").date()
        except ValueError:
            continue
        out[(plate, d)] = {"action": action, "note": note}
    return out


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def discover_gps_files(folder: Path) -> tuple[Path, Path]:
    o_env, d_env = os.environ.get("OATSIDE_ORIGIN"), os.environ.get("OATSIDE_DEST")
    if o_env and d_env:
        return Path(o_env), Path(d_env)
    cands = sorted(
        [p for p in folder.glob("Y.K._*.xlsx") if "~$" not in p.name],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    origins = [p for p in cands if "Oatside" in p.name and "Oatside_PG" not in p.name]
    dests = [p for p in cands if ("P&G" in p.name or "เวลล์โกล" in p.name) and "Oatside_PG" not in p.name]
    if not origins or not dests:
        raise FileNotFoundError(
            "Need two GPS exports in Oatside/: one name containing 'Oatside', one 'P&G' or 'เวลล์โกล'."
        )
    return origins[0], dests[0]


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def plate_from_label(s: str | None) -> str | None:
    if not s or not isinstance(s, str):
        return None
    m = PLATE_HEAD.match(s.strip())
    return m.group(1) if m else None


def _parse_dt(val) -> datetime | None:
    if isinstance(val, datetime):
        return val
    if isinstance(val, date) and not isinstance(val, datetime):
        return datetime.combine(val, datetime.min.time())
    if isinstance(val, str):
        s = val.strip()
        if len(s) >= 19:
            try:
                return datetime.strptime(s[:19], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                pass
        try:
            return datetime.strptime(s[:10], "%Y-%m-%d")
        except ValueError:
            return None
    return None


def parse_legs(path: Path) -> list[Leg]:
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = None
    for name in wb.sheetnames:
        w = wb[name]
        if w.max_row >= 1 and w.cell(1, 4).value == "เวลาเข้า":
            ws = w
            break
    if ws is None:
        wb.close()
        raise ValueError(f"No equipment sheet in {path}")
    legs: list[Leg] = []
    current_plate: str | None = None
    for r in range(2, ws.max_row + 1):
        a, b, c, tin, tout = (
            ws.cell(r, 1).value, ws.cell(r, 2).value, ws.cell(r, 3).value,
            ws.cell(r, 4).value, ws.cell(r, 5).value,
        )
        c_s = str(c).strip() if c is not None else ""
        if c_s == "-----" or "-----" in c_s:
            current_plate = plate_from_label(str(b) if b else "")
            continue
        if not a or not DETAIL_KEY.match(str(a).strip()):
            continue
        tin = _parse_dt(tin)
        tout = _parse_dt(tout)
        if not tin or not tout:
            continue
        dev = str(c).strip() if c else ""
        p = plate_from_label(dev) or current_plate
        if not p:
            continue
        legs.append(Leg(row_no=str(a).strip(), plate=p, device=dev, t_in=tin, t_out=tout))
    wb.close()
    legs.sort(key=lambda x: (x.plate, x.t_out))
    return legs


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------

def hours(a: datetime, b: datetime) -> float:
    return (b - a).total_seconds() / 3600.0


def feasible(o: Leg, d: Leg, max_travel_h: float) -> bool:
    if d.t_in < o.t_out:
        return False
    return hours(o.t_out, d.t_in) <= max_travel_h


# Max hours between end of accumulated origin leg and start of next origin leg for
# "double origin" chain-merge. If the driver clearly left the hub (gap > this), the
# next origin row is a new visit — do not merge (avoids stretching Origin_Out to a
# later shift when Dest_In is still far in the future).


def match_plate(
    origins: list[Leg], dests: list[Leg], max_travel_h: float
) -> tuple[list[tuple[Leg, Leg]], list[Leg], list[Leg]]:
    """Pair each destination (time order) with the latest unused origin where
    Dest_In >= Origin_Out and travel <= max_travel_h.

    Origin-first greedy caused short hub exits to claim far Dest_In legs, leaving
    longer hub sessions unmatched and triggering demote_chronology_violations churn.
    Latest-origin-before-dest is closer to real dispatch (last exit before delivery)."""
    dests_sorted = sorted(dests, key=lambda x: (x.t_in, x.t_out))
    used_o: set[int] = set()
    pairs: list[tuple[Leg, Leg]] = []
    for d in dests_sorted:
        best_o: Leg | None = None
        for o in sorted(origins, key=lambda x: x.t_out, reverse=True):
            if id(o) in used_o:
                continue
            if not feasible(o, d, max_travel_h):
                continue
            best_o = o
            break
        if best_o is not None:
            pairs.append((best_o, d))
            used_o.add(id(best_o))
    uo = [x for x in origins if id(x) not in used_o]
    used_d = {id(dl) for _, dl in pairs}
    ud = [y for y in dests if id(y) not in used_d]
    return pairs, uo, ud


def merge_chained_origin_pairs(
    pairs: list[tuple[Leg, Leg]],
    max_gap_h: float,
) -> tuple[list[tuple[Leg, Leg]], list[Leg]]:
    """Resolve 'double origin' before one delivery: greedy pairs sorted by Origin_Out.
    If the next origin checks in before the current trip's Dest_In, merge origin legs and
    pick the destination with minimum feasible travel from merged Origin_Out (orphan others).
    Guard: if gap between accumulated Origin_Out and next Origin_In exceeds max_gap_h hours,
    do not chain-merge (separate hub visit)."""
    if not pairs:
        return [], []
    pairs = sorted(pairs, key=lambda pr: (pr[0].t_out, pr[0].t_in))
    out: list[tuple[Leg, Leg]] = []
    orphan_dests: list[Leg] = []
    i = 0
    while i < len(pairs):
        o_acc, d_acc = pairs[i]
        j = i + 1
        first_extend = True
        while j < len(pairs):
            o2, d2 = pairs[j]
            if o2.t_in >= d_acc.t_in:
                break
            gap_h = hours(o_acc.t_out, o2.t_in)
            if gap_h > max_gap_h:
                break
            o_acc = Leg(
                row_no=f"{o_acc.row_no}+{o2.row_no}",
                plate=o_acc.plate,
                device=o_acc.device,
                t_in=o_acc.t_in,
                t_out=o2.t_out,
            )
            last_out = o_acc.t_out
            pool = [d_acc, d2]
            feas = [d for d in pool if d.t_in >= last_out]
            use_pool = feas if feas else pool
            if first_extend:
                row_pref = [d for d in use_pool if d.row_no == o2.row_no]
                pick = min(
                    row_pref if row_pref else use_pool,
                    key=lambda d: (hours(last_out, d.t_in), d.t_in),
                )
                first_extend = False
            else:
                pick = d_acc if d_acc in use_pool else min(
                    use_pool, key=lambda d: (hours(last_out, d.t_in), d.t_in)
                )
            for d in pool:
                if id(d) != id(pick):
                    orphan_dests.append(d)
            d_acc = pick
            j += 1
        out.append((o_acc, d_acc))
        i = j
    return out, orphan_dests


def rematch_orphan_dests_to_origins(
    orphan_dests: list[Leg],
    candidates: list[Leg],
    max_travel_h: float,
) -> tuple[list[tuple[Leg, Leg]], list[Leg]]:
    """Pair orphan destinations with unused origin legs (same plate), min travel."""
    cands = sorted(candidates, key=lambda x: (x.t_out, x.t_in))
    used_o: set[int] = set()
    new_pairs: list[tuple[Leg, Leg]] = []
    still: list[Leg] = []
    for d in sorted(orphan_dests, key=lambda x: (x.t_in, x.t_out)):
        best_o: Leg | None = None
        best_tr = 1e9
        for o in cands:
            if id(o) in used_o:
                continue
            if not feasible(o, d, max_travel_h):
                continue
            tr = hours(o.t_out, d.t_in)
            if tr < best_tr or (tr == best_tr and (best_o is None or o.t_out < best_o.t_out)):
                best_o = o
                best_tr = tr
        if best_o is not None:
            new_pairs.append((best_o, d))
            used_o.add(id(best_o))
        else:
            still.append(d)
    return new_pairs, still


def collect_origin_row_refs(ol: Leg) -> list[str]:
    s = ol.row_no.strip()
    if not s:
        return []
    return [p.strip() for p in s.split("+") if p.strip()]


def constituent_origin_legs(ol: Leg, by_row: dict[str, Leg]) -> list[Leg]:
    refs = collect_origin_row_refs(ol)
    out: list[Leg] = []
    for r in refs:
        leg = by_row.get(r)
        if leg is not None:
            out.append(leg)
    if not out:
        return [ol]
    return out


def mark_used_origin_legs(ol: Leg, by_row: dict[str, Leg], used_o: set[int]) -> None:
    for lg in constituent_origin_legs(ol, by_row):
        used_o.add(id(lg))


# ---------------------------------------------------------------------------
# Site / IQR helpers
# ---------------------------------------------------------------------------

def site_for_plate(plate: str) -> str:
    if plate in BIGC_EXACT:
        return "BigC"
    m = re.match(r"^71-(\d+)$", plate)
    if m:
        n = int(m.group(1))
        if 8000 <= n <= 8009:
            return "BigC"
    return "LCB"


def iqr_threshold(travels: list[float]) -> float:
    if len(travels) < 4:
        return 8.0
    xs = sorted(travels)
    n = len(xs)

    def q(p: float) -> float:
        idx = p * (n - 1)
        lo = int(math.floor(idx))
        hi = int(math.ceil(idx))
        if lo == hi:
            return xs[lo]
        return xs[lo] + (xs[hi] - xs[lo]) * (idx - lo)

    q1, q3 = q(0.25), q(0.75)
    iqr = q3 - q1
    return max(8.0, q3 + 1.5 * iqr)


# ---------------------------------------------------------------------------
# Chronology guard
# ---------------------------------------------------------------------------

def _trip_legs_for_unmatched(t: Trip, origin_by_row: dict[str, Leg]) -> tuple[list[Leg], Leg]:
    fake_o = Leg(row_no=t.o_row, plate=t.plate, device=t.device, t_in=t.o_in, t_out=t.o_out)
    o_segs = constituent_origin_legs(fake_o, origin_by_row)
    if not o_segs:
        o_segs = [Leg(row_no=t.o_row, plate=t.plate, device=t.device, t_in=t.o_in, t_out=t.o_out)]
    dest_leg = Leg(
        row_no=t.d_row,
        plate=t.plate,
        device=t.device,
        t_in=t.d_in,
        t_out=t.d_out,
    )
    return o_segs, dest_leg


def demote_chronology_violations(
    trips: list[Trip],
    unmatched_rows: list[tuple[str, Leg, str]],
    origin_by_row_by_plate: dict[str, dict[str, Leg]],
) -> None:
    """Per plate: sort by Origin_In. If a trip Origin_In is strictly before the previous trip's
    Dest_Out, the previous match is impossible in real sequence — demote the *previous* trip to
    Unmatched (origin segment(s) + destination) and repeat until stable."""
    by_plate: dict[str, list[Trip]] = defaultdict(list)
    for t in trips:
        by_plate[t.plate].append(t)
    rebuilt: list[Trip] = []
    for plate in sorted(by_plate.keys()):
        lst = sorted(by_plate[plate], key=lambda t: (t.o_in, t.d_in))
        br = origin_by_row_by_plate.get(plate, {})
        changed = True
        while changed and len(lst) > 1:
            changed = False
            for i in range(1, len(lst)):
                if lst[i].o_in < lst[i - 1].d_out:
                    bad = lst.pop(i - 1)
                    o_segs, dleg = _trip_legs_for_unmatched(bad, br)
                    for ol in o_segs:
                        unmatched_rows.append(("Origin", ol, plate))
                    unmatched_rows.append(("Destination", dleg, plate))
                    changed = True
                    break
        rebuilt.extend(lst)
    trips[:] = sorted(rebuilt, key=lambda t: (t.plate, t.o_in))


# ---------------------------------------------------------------------------
# Build trips
# ---------------------------------------------------------------------------

def build_trips(
    origin_path: Path, dest_path: Path, cfg: OatsideConfig
) -> tuple[list[Trip], list[tuple[str, Leg, str]], list[float]]:
    o_legs = parse_legs(origin_path)
    d_legs = parse_legs(dest_path)
    by_plate_o: dict[str, list[Leg]] = defaultdict(list)
    by_plate_d: dict[str, list[Leg]] = defaultdict(list)
    for x in o_legs:
        by_plate_o[x.plate].append(x)
    for x in d_legs:
        by_plate_d[x.plate].append(x)
    plates = sorted(set(by_plate_o) | set(by_plate_d))
    trips: list[Trip] = []
    unmatched_rows: list[tuple[str, Leg, str]] = []
    origin_by_row_by_plate: dict[str, dict[str, Leg]] = {}
    mx = cfg.max_travel_h
    for p in plates:
        all_o = by_plate_o[p]
        by_row: dict[str, Leg] = {}
        for o in all_o:
            if o.row_no not in by_row:
                by_row[o.row_no] = o
        origin_by_row_by_plate[p] = by_row
        pairs, uo, ud = match_plate(all_o, by_plate_d[p], mx)
        if cfg.enable_origin_chain_merge:
            merged_pairs, orphan_d = merge_chained_origin_pairs(pairs, cfg.max_origin_chain_gap_h)
        else:
            merged_pairs, orphan_d = pairs, []
        used_o: set[int] = set()
        for ol, _ in merged_pairs:
            mark_used_origin_legs(ol, by_row, used_o)
        candidates = [o for o in all_o if id(o) not in used_o]
        rematch_pairs, still_orphan = rematch_orphan_dests_to_origins(orphan_d, candidates, mx)
        for ol, _ in rematch_pairs:
            mark_used_origin_legs(ol, by_row, used_o)
        pairs_final = merged_pairs + rematch_pairs
        for ol, dl in pairs_final:
            segs = constituent_origin_legs(ol, by_row)
            ow = sum(hours(x.t_in, x.t_out) for x in segs) if len(segs) > 1 else hours(ol.t_in, ol.t_out)
            tr = hours(ol.t_out, dl.t_in)
            dw = hours(dl.t_in, dl.t_out)
            tc = hours(segs[0].t_in, dl.t_out)
            trips.append(
                Trip(
                    plate=p,
                    site=site_for_plate(p),
                    device=segs[0].device,
                    o_row=ol.row_no,
                    d_row=dl.row_no,
                    o_in=segs[0].t_in,
                    o_out=ol.t_out,
                    d_in=dl.t_in,
                    d_out=dl.t_out,
                    origin_wait_h=ow,
                    travel_h=tr,
                    dest_wait_h=dw,
                    total_cycle_h=tc,
                    origin_date=segs[0].t_in.date(),
                    dest_date=dl.t_in.date(),
                    trip_date=segs[0].t_in.date(),
                    travel_flag=None,
                )
            )
        for ol in (o for o in all_o if id(o) not in used_o):
            unmatched_rows.append(("Origin", ol, p))
        for dl in ud + still_orphan:
            unmatched_rows.append(("Destination", dl, p))
    demote_chronology_violations(trips, unmatched_rows, origin_by_row_by_plate)
    travels = [t.travel_h for t in trips]
    thr = iqr_threshold(travels)
    for t in trips:
        t.travel_flag = "ABNORMAL" if t.travel_h >= thr else None
    return trips, unmatched_rows, travels


# ---------------------------------------------------------------------------
# Billing calculations
# ---------------------------------------------------------------------------

def base_trips_revenue_baht(trips: list[Trip], cfg: OatsideConfig) -> int:
    """Sum per-trip rate by Dest_In calendar day."""
    return sum(trip_rate_baht(t.dest_date, cfg) for t in trips)


def one_trip_fifty_pct_details(
    trips: list[Trip],
    overrides: dict[tuple[str, date], dict[str, Any]],
    cfg: OatsideConfig,
) -> tuple[list[dict], int]:
    """50% surcharge on a Dest_In calendar day when exactly 1 matched trip (unless overridden)."""
    by_pd: dict[tuple[str, date], list[Trip]] = defaultdict(list)
    for t in trips:
        by_pd[(t.plate, t.dest_date)].append(t)

    rows: list[dict] = []
    total = 0
    for (plate, d), lst in sorted(by_pd.items(), key=lambda x: (x[0][1], x[0][0])):
        key = (plate, d)
        ov = overrides.get(key, {})
        action = ov.get("action", "")
        note = ov.get("note", "")
        n = len(lst)
        auto_apply = n == 1
        if action == "exclude_50":
            apply_charge = False
        elif action == "include_50":
            apply_charge = True
        else:
            apply_charge = auto_apply
        if not apply_charge:
            continue
        rate = trip_rate_baht(d, cfg)
        sur = int(round(rate * cfg.one_trip_surcharge_pct / 100))
        rows.append(
            {
                "dest_date": d,
                "plate": plate,
                "site": site_for_plate(plate),
                "trips_that_day": n,
                "auto_1trip": auto_apply,
                "override_action": action or "",
                "override_note": note,
                "trip_rate_baht": rate,
                "surcharge_baht": sur,
            }
        )
        total += sur
    return rows, total


def plate_dest_day_rows(
    trips: list[Trip], fifty_rows: list[dict], cfg: OatsideConfig
) -> list[dict]:
    """Per (plate, Dest_In date): trip count, base line, whether 50% charged (after overrides)."""
    by_pd: dict[tuple[str, date], list[Trip]] = defaultdict(list)
    for t in trips:
        by_pd[(t.plate, t.dest_date)].append(t)
    fifty_key = {(r["plate"], r["dest_date"]): r for r in fifty_rows}
    out: list[dict] = []
    for (plate, d), lst in sorted(by_pd.items(), key=lambda x: (x[0][1], x[0][0])):
        rate = trip_rate_baht(d, cfg)
        n = len(lst)
        base_line = n * rate
        fr = fifty_key.get((plate, d))
        sur = int(fr["surcharge_baht"]) if fr else 0
        out.append(
            {
                "dest_date": d,
                "plate": plate,
                "site": site_for_plate(plate),
                "matched_trips": n,
                "trip_rate_baht": rate,
                "base_line_baht": base_line,
                "fifty_pct_baht": sur,
                "customer_day_baht": base_line + sur,
            }
        )
    return out


def customer_trips_per_day_rows(trips: list[Trip]) -> list[dict]:
    """Matched trips aggregated by Dest_In calendar day (fleet total) for customer one-pager."""
    by_t: dict[date, int] = defaultdict(int)
    by_plates: dict[date, set[str]] = defaultdict(set)
    for tr in trips:
        d = tr.dest_date
        by_t[d] += 1
        by_plates[d].add(tr.plate)
    return [
        {"dest_date": d, "matched_trips": by_t[d], "active_trucks": len(by_plates[d])}
        for d in sorted(by_t.keys())
    ]


def audit_log_rows(

    trips: list[Trip],
    fifty_rows: list[dict],
    overrides: dict[tuple[str, date], dict[str, Any]],
    cfg: OatsideConfig,
) -> list[dict]:
    """Per (plate, dest_date): one row explaining the billing decision in Thai."""
    by_pd: dict[tuple[str, date], list[Trip]] = defaultdict(list)
    for t in trips:
        by_pd[(t.plate, t.dest_date)].append(t)
    fifty_key = {(r["plate"], r["dest_date"]): r for r in fifty_rows}

    rows: list[dict] = []
    for (plate, d), lst in sorted(by_pd.items(), key=lambda x: (x[0][1], x[0][0])):
        n = len(lst)
        rate = trip_rate_baht(d, cfg)
        base = n * rate
        fr = fifty_key.get((plate, d))
        sur = int(fr["surcharge_baht"]) if fr else 0
        total = base + sur

        ov = overrides.get((plate, d), {})
        action = ov.get("action", "")
        note = ov.get("note", "")

        if action == "exclude_50":
            fifty_rule = f"ไม่เก็บ {cfg.one_trip_surcharge_pct:.0f}% [override: exclude_50]"
            if note:
                fifty_rule += f" — {note}"
        elif action == "include_50":
            fifty_rule = f"เก็บ {cfg.one_trip_surcharge_pct:.0f}% [override: include_50]"
            if note:
                fifty_rule += f" — {note}"
        elif n == 1:
            fifty_rule = f"เก็บ {cfg.one_trip_surcharge_pct:.0f}% อัตโนมัติ (วิ่ง 1 เที่ยว)"
        else:
            fifty_rule = f"ไม่เก็บ {cfg.one_trip_surcharge_pct:.0f}% (วิ่ง {n} เที่ยว)"

        rows.append({
            "dest_date": d,
            "plate": plate,
            "site": site_for_plate(plate),
            "matched_trips": n,
            "trip_rate_baht": rate,
            "base_line_baht": base,
            "fifty_pct_baht": sur,
            "customer_day_baht": total,
            "billing_note": fifty_rule,
        })
    return rows


def daily_activity_by_dest(trips: Iterable[Trip], cfg: OatsideConfig) -> list[tuple[date, dict]]:
    """Return sorted list of (dest_date, stats)."""
    by: dict[date, dict] = defaultdict(
        lambda: {
            "plates": set(),
            "trips": 0,
            "bigc_p": set(),
            "bigc_t": 0,
            "lcb_p": set(),
            "lcb_t": 0,
        }
    )
    for t in trips:
        d = t.dest_date
        by[d]["plates"].add(t.plate)
        by[d]["trips"] += 1
        if t.site == "BigC":
            by[d]["bigc_p"].add(t.plate)
            by[d]["bigc_t"] += 1
        else:
            by[d]["lcb_p"].add(t.plate)
            by[d]["lcb_t"] += 1
    out = []
    for d in sorted(by):
        s = by[d]
        trucks = len(s["plates"])
        commit = cfg.min_trips_per_truck * trucks
        short = max(0, commit - s["trips"])
        out.append((d, {**s, "trucks": trucks, "commit": commit, "short": short}))
    return out


def billing_totals(rows: list[tuple[date, dict]], cfg: OatsideConfig) -> tuple[int, int, int, int]:
    actual = sum(s["trips"] for _, s in rows)
    commit = sum(s["commit"] for _, s in rows)
    short = sum(s["short"] for _, s in rows)
    extra = 0
    for d, s in rows:
        r = trip_rate_baht(d, cfg)
        extra += s["short"] * r
    return actual, commit, short, extra


def site_billing(rows: list[tuple[date, dict]], cfg: OatsideConfig) -> tuple[int, int, int, int, int, int, int, int]:
    """Returns BigC (actual, commit, short, extra) then LCB (actual, commit, short, extra)."""
    bc_a = bc_c = bc_s = bc_e = 0
    lc_a = lc_c = lc_s = lc_e = 0
    for d, s in rows:
        r = trip_rate_baht(d, cfg)
        bt = s["bigc_t"]
        bc_min = cfg.min_trips_per_truck * len(s["bigc_p"])
        bs = max(0, bc_min - bt)
        lt = s["lcb_t"]
        lc_min = cfg.min_trips_per_truck * len(s["lcb_p"])
        ls = max(0, lc_min - lt)
        bc_a += bt
        bc_c += bc_min
        bc_s += bs
        bc_e += bs * r
        lc_a += lt
        lc_c += lc_min
        lc_s += ls
        lc_e += ls * r
    return bc_a, bc_c, bc_s, bc_e, lc_a, lc_c, lc_s, lc_e


def daily_time_rows(trips: list[Trip], unmatched: list[tuple[str, Leg, str]]) -> list[tuple]:
    matched_cycle_h: dict[tuple[date, str], float] = defaultdict(float)
    matched_origin_wait_h: dict[tuple[date, str], float] = defaultdict(float)
    matched_dest_wait_h: dict[tuple[date, str], float] = defaultdict(float)
    matched_travel_h: dict[tuple[date, str], float] = defaultdict(float)
    for t in trips:
        key = (t.trip_date, t.plate)
        matched_cycle_h[key] += t.total_cycle_h
        matched_origin_wait_h[key] += t.origin_wait_h
        matched_dest_wait_h[key] += t.dest_wait_h
        matched_travel_h[key] += t.travel_h
    uo: dict[tuple[date, str], float] = defaultdict(float)
    ud: dict[tuple[date, str], float] = defaultdict(float)
    for src, leg, _p in unmatched:
        key = (leg.t_in.date(), leg.plate)
        h = hours(leg.t_in, leg.t_out)
        if h < 0 or h > 72:
            continue
        if src == "Origin":
            uo[key] += h
        else:
            ud[key] += h
    keys = sorted(
        set(matched_cycle_h) | set(matched_origin_wait_h) | set(matched_dest_wait_h)
        | set(matched_travel_h) | set(uo) | set(ud),
        key=lambda x: (x[0], x[1]),
    )
    rows = []
    for d, plate in keys:
        key = (d, plate)
        cycle_h = matched_cycle_h.get(key, 0.0)
        matched_ow = matched_origin_wait_h.get(key, 0.0)
        matched_dw = matched_dest_wait_h.get(key, 0.0)
        matched_tr = matched_travel_h.get(key, 0.0)
        um_ow = uo.get(key, 0.0)
        um_dw = ud.get(key, 0.0)
        adjusted_ow = matched_ow + um_ow
        adjusted_dw = matched_dw + um_dw
        combined_h = adjusted_ow + matched_tr + adjusted_dw
        rows.append((
            d, plate, site_for_plate(plate),
            cycle_h, matched_ow, matched_dw, matched_tr,
            um_ow, um_dw, adjusted_ow, adjusted_dw, combined_h,
            24.0 - combined_h,
        ))
    return rows


# ---------------------------------------------------------------------------
# Excel export
# ---------------------------------------------------------------------------

def write_excel(
    path: Path,
    origin_name: str,
    dest_name: str,
    trips: list[Trip],
    unmatched: list[tuple[str, Leg, str]],
    daily_time: list[tuple],
    daily_rows: list[tuple[date, dict]],
    fifty_rows: list[dict],
    fifty_total_baht: int,
    min_trip_extra_baht: int,
    audit_rows: list[dict],
    cfg: OatsideConfig,
) -> None:
    base_baht = base_trips_revenue_baht(trips, cfg)
    customer_grand_baht = int(base_baht) + int(min_trip_extra_baht) + int(fifty_total_baht)
    pday = plate_dest_day_rows(trips, fifty_rows, cfg)
    wb = openpyxl.Workbook()
    default = wb.active
    wb.remove(default)

    # --- Info ---
    info = wb.create_sheet("Info", 0)
    info.append(["Built", datetime.now().strftime("%Y-%m-%d %H:%M")])
    info.append(["Origin file", origin_name])
    info.append(["Dest file", dest_name])
    info.append(["Config file", str(_config_path())])
    info.append(["Max_travel_h", cfg.max_travel_h])
    info.append(["Max_origin_chain_gap_h", cfg.max_origin_chain_gap_h])
    info.append(["Enable_origin_chain_merge", cfg.enable_origin_chain_merge])
    info.append(["Min_trips_per_truck_per_day", cfg.min_trips_per_truck])
    info.append(["One_trip_surcharge_pct", cfg.one_trip_surcharge_pct])
    info.append(["Trip_rates", config_rate_summary(cfg)])
    info.append(["Matcher",
        f"Greedy min-travel; feasible if Dest_In>=Origin_Out and travel<={cfg.max_travel_h}h"])
    info.append(["Surcharge_50pct_1Trip",
        f"If exactly 1 matched trip on Dest_In day -> add {cfg.one_trip_surcharge_pct:.0f}% of trip rate. "
        f"Overrides: {_overrides_json_path()} (exclude_50 / include_50)"])
    info.append(["Base_trips_revenue_baht", base_baht])
    info.append(["Charge_min_trip_shortfall", cfg.charge_min_trip_shortfall])
    info.append(["Min2trips_extra_baht", min_trip_extra_baht])
    info.append(["Fifty_pct_surcharge_total_baht", fifty_total_baht])
    cg_note = "base + min_trips + fifty" if cfg.charge_min_trip_shortfall else "base + fifty (min-trip shortfall not charged)"
    info.append([f"Customer_grand_baht ({cg_note})", customer_grand_baht])

    # --- Customer Summary ---
    cs = wb.create_sheet("Customer_Summary")
    cs.append(["Line", "รายการ", "บาท"])
    cs.append(["A", "ค่าเที่ยวปกติ (นับ 1 เที่ยว = 1 เรทตามวันที่ Dest_In)", base_baht])
    if cfg.charge_min_trip_shortfall:
        b_line = f"เที่ยวขาดจาก commit {cfg.min_trips_per_truck} เที่ยว/คัน/วัน (min trips)"
    else:
        b_line = (
            f"ค่าชดเชยเที่ยวขาด (min {cfg.min_trips_per_truck}/คัน/วัน) — ไม่เก็บเงิน "
            f"(ใช้ชาร์จ {cfg.one_trip_surcharge_pct:.0f}% วันละ 1 เที่ยวแทน)"
        )
    cs.append(["B", b_line, min_trip_extra_baht])
    cs.append(["C", f"ชาร์จ {cfg.one_trip_surcharge_pct:.0f}% วันที่วิ่งได้ 1 เที่ยว (หลัง override)", fifty_total_baht])
    tot_lbl = "รวมเสนอลูกค้า (A+B+C)" if cfg.charge_min_trip_shortfall else "รวมเสนอลูกค้า (A+C)"
    cs.append(["TOTAL", tot_lbl, customer_grand_baht])

    # --- Customer: trips per day (matched, by Dest_In date) ---
    cpd_rows = customer_trips_per_day_rows(trips)
    cpd = wb.create_sheet("Customer_Trips_Per_Day")
    cpd.append(["วันที่_Dest_In", "จำนวนเที่ยว_matched", "จำนวนรถ_มีเที่ยววันนั้น"])
    for r in cpd_rows:
        cpd.append([r["dest_date"], r["matched_trips"], r["active_trucks"]])

    # --- Audit Log (ชีตใหม่ — อธิบายเหตุผลการคิดเงินรายวัน/ทะเบียน) ---
    al = wb.create_sheet("Audit_Log")
    al.append([
        "Dest_In_date", "Plate", "Site",
        "เที่ยว", "เรท(฿)", "ค่าเที่ยว(฿)",
        f"+{cfg.one_trip_surcharge_pct:.0f}%(฿)", "รวมวันนี้(฿)",
        "เหตุผลการคิดเงิน",
    ])
    for r in audit_rows:
        al.append([
            r["dest_date"], r["plate"], r["site"],
            r["matched_trips"], r["trip_rate_baht"], r["base_line_baht"],
            r["fifty_pct_baht"], r["customer_day_baht"],
            r["billing_note"],
        ])

    # --- Trip Detail ---
    td = wb.create_sheet("Trip_Detail")
    td.append([
        "Trip_Date", "Origin_Date", "Dest_Date", "Site", "Plate", "Device",
        "Origin_Row", "Dest_Row",
        "Origin_In", "Origin_Out", "Origin_Wait_h",
        "Dest_In", "Dest_Out",
        "Travel_h(OriginOut->DestIn)", "Dest_Wait_h", "Total_Cycle_h",
        "Travel_Flag", "Billable_Trip",
    ])
    for t in sorted(trips, key=lambda x: (x.dest_date, x.plate, x.d_in)):
        td.append([
            t.trip_date, t.origin_date, t.dest_date,
            t.site, t.plate, t.device, t.o_row, t.d_row,
            t.o_in, t.o_out, round(t.origin_wait_h, 2),
            t.d_in, t.d_out,
            round(t.travel_h, 2), round(t.dest_wait_h, 2), round(t.total_cycle_h, 2),
            t.travel_flag, 1,
        ])

    # --- Unmatched Log ---
    um = wb.create_sheet("Unmatched_Log")
    um.append(["Source", "Plate", "Device", "Row_No", "In", "Out"])
    for src, leg, _ in sorted(unmatched, key=lambda x: (x[2], x[1].t_in)):
        um.append([src, leg.plate, leg.device, leg.row_no, leg.t_in, leg.t_out])

    # --- Daily Activity ---
    da = wb.create_sheet("Daily_Activity")
    da.append([
        "Dest_In date", "Active trucks (all)", "Actual trips (all)",
        f"Commit min ({cfg.min_trips_per_truck}x trucks)", "Shortfall trips (all)",
        "BigC trucks", "BigC trips", "LCB trucks", "LCB trips",
    ])
    for d, s in daily_rows:
        da.append([
            d, s["trucks"], s["trips"], s["commit"], s["short"],
            len(s["bigc_p"]), s["bigc_t"], len(s["lcb_p"]), s["lcb_t"],
        ])

    # --- Daily Time 24h Check ---
    dt = wb.create_sheet("Daily_Time_24h_Check")
    dt.append([
        "Activity_Date", "Plate", "Site",
        "Matched_Cycle_h", "Matched_Origin_Wait_h", "Matched_Dest_Wait_h", "Matched_Travel_h",
        "Unmatched_Origin_h", "Unmatched_Dest_h",
        "Adjusted_Origin_Wait_h", "Adjusted_Dest_Wait_h",
        "Combined_h(AdjustedWait+Travel)", "Gap_vs_24_h",
    ])
    for d, plate, site, cycle_h, m_ow, m_dw, m_tr, um_ow, um_dw, ad_ow, ad_dw, comb, gap in daily_time:
        dt.append([
            d.isoformat(), plate, site,
            round(cycle_h, 2), round(m_ow, 2), round(m_dw, 2), round(m_tr, 2),
            round(um_ow, 2), round(um_dw, 2), round(ad_ow, 2), round(ad_dw, 2),
            round(comb, 2), round(gap, 2),
        ])

    # --- Plate DestDay ---
    pd_sheet = wb.create_sheet("Plate_DestDay")
    pd_sheet.append([
        "Dest_In_date", "Plate", "Site", "Matched_trips",
        "Trip_rate_baht", "Base_line_baht", "Fifty_pct_baht", "Customer_day_baht",
    ])
    for r in pday:
        pd_sheet.append([
            r["dest_date"], r["plate"], r["site"], r["matched_trips"],
            r["trip_rate_baht"], r["base_line_baht"], r["fifty_pct_baht"], r["customer_day_baht"],
        ])

    # --- Surcharge 50% 1Trip ---
    lt = wb.create_sheet("Surcharge_50pct_1Trip")
    lt.append([
        "Dest_In_date", "Plate", "Site", "Trips_that_day",
        "Auto_1trip_rule_Y/N", "Override_action", "Override_note",
        "Trip_rate_baht", f"Surcharge_baht_{cfg.one_trip_surcharge_pct:.0f}pct",
    ])
    for r in fifty_rows:
        lt.append([
            r["dest_date"], r["plate"], r["site"], r["trips_that_day"],
            "Y" if r["auto_1trip"] else "N",
            r.get("override_action", ""), r.get("override_note", ""),
            r["trip_rate_baht"], r["surcharge_baht"],
        ])

    wb.save(path)


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------

def esc(x) -> str:
    return html_module.escape(str(x), quote=True)


def fmt_h(x: float) -> str:
    return f"{x:.2f}".rstrip("0").rstrip(".")


def fmt_hm(x: float) -> str:
    sign = "-" if x < 0 else ""
    total_minutes = int(round(abs(x) * 60))
    hh = total_minutes // 60
    mm = total_minutes % 60
    return f"{sign}{hh}.{mm:02d}"


def unmatched_merged_trip_one_row_html(
    src: str,
    leg: Leg,
    *,
    include_plate_link: bool = True,
    include_plate_column: bool = True,
) -> str:
    """One <tr> aligned with trip_row (full) or trip_row_plate (no plate column)."""
    dash = "—"
    tag = "UM-O" if src == "Origin" else "UM-D"
    badge = f"<span class='badge abn'>{tag}</span> "
    site = site_for_plate(leg.plate)
    site_html = f"<span class='badge {'bigc' if site == 'BigC' else 'lcb'}'>{site}</span>"
    if include_plate_column:
        if include_plate_link:
            plate_html = f"{badge}<a href='plates/{esc(leg.plate)}.html'>{esc(leg.plate)}</a>"
        else:
            plate_html = f"{badge}{esc(leg.plate)}"
        site_plate = f"<td>{site_html}</td><td>{plate_html}</td>"
    else:
        site_plate = f"<td>{site_html} {badge}</td>"
    if src == "Origin":
        od, dd = leg.t_in.date(), dash
        oi, oo = leg.t_in, leg.t_out
        di, do = dash, dash
    else:
        od, dd = dash, leg.t_in.date()
        oi, oo = dash, dash
        di, do = leg.t_in, leg.t_out
    return (
        f"<tr class='um'><td>{od}</td><td>{dd}</td>{site_plate}"
        f"<td>{oi}</td><td>{oo}</td><td>{di}</td><td>{do}</td>"
        f"<td>{dash}</td><td>{dash}</td><td>{dash}</td></tr>"
    )


def interleaved_matched_unmatched_rows_html(
    trips: list[Trip],
    unmatched: list[tuple[str, Leg, str]],
    trip_row_cb: Callable[[Trip], str],
    *,
    plate: str | None = None,
    include_plate_link: bool = True,
    include_plate_column: bool = True,
) -> str:
    """Sort matched (by Dest_In time) and unmatched (by leg time) into one timeline."""
    rows: list[tuple[datetime, tuple[Any, ...], str]] = []
    for t in trips:
        if plate is not None and t.plate != plate:
            continue
        rows.append((t.d_in, (0, t.plate, t.d_row or "", t.o_row or ""), trip_row_cb(t)))
    for src, leg, _mp in unmatched:
        if plate is not None and leg.plate != plate:
            continue
        um_html = unmatched_merged_trip_one_row_html(
            src,
            leg,
            include_plate_link=include_plate_link,
            include_plate_column=include_plate_column,
        )
        kind = 1 if src == "Origin" else 2
        rows.append((leg.t_in, (kind, leg.plate, src, leg.row_no), um_html))
    rows.sort(key=lambda x: (x[0], x[1]))
    return "".join(r[2] for r in rows)


# ---------------------------------------------------------------------------
# HTML export
# ---------------------------------------------------------------------------

def write_html(
    report_dir: Path,
    origin_label: str,
    trips: list[Trip],
    daily_rows: list[tuple[date, dict]],
    daily_time: list[tuple],
    actual: int,
    commit: int,
    short: int,
    extra: int,
    bc: tuple,
    fifty_rows: list[dict],
    fifty_total_baht: int,
    grand_extra_baht: int,
    base_baht: int,
    customer_grand_baht: int,
    pday_rows: list[dict],
    audit_rows: list[dict],
    unmatched: list[tuple[str, Leg, str]],
    cfg: OatsideConfig,
) -> None:
    bc_a, bc_c, bc_s, bc_e, lc_a, lc_c, lc_s, lc_e = bc
    thr = iqr_threshold([t.travel_h for t in trips])
    abn = [t for t in trips if t.travel_flag]
    plates = sorted({t.plate for t in trips})
    fifty_by_key = {(r["plate"], r["dest_date"]): r for r in fifty_rows}
    sub = (
        f"สร้าง {datetime.now():%Y-%m-%d %H:%M} | ต้นทาง: {esc(Path(origin_label).name)} | "
        f"เรท: {config_rate_summary(cfg)} ฿/เที่ยว | "
        f"min {cfg.min_trips_per_truck} เที่ยว/คัน/วัน | "
        f"+{cfg.one_trip_surcharge_pct:.0f}% วันที่วิ่ง 1 เที่ยว | "
        f"max travel {cfg.max_travel_h}h"
    )
    if not cfg.charge_min_trip_shortfall:
        sub += " | ไม่เก็บเงินค่าชดเชยเที่ยวขาด (min trips) — ใช้ชาร์จ % วันละ 1 เที่ยวแทน"


    def trip_row(t: Trip) -> str:
        ab = " <span class='badge abn'>ABNORMAL</span>" if t.travel_flag else ""
        return (
            f"<tr><td>{t.origin_date}</td><td>{t.dest_date}</td>"
            f"<td><span class='badge {'bigc' if t.site=='BigC' else 'lcb'}'>{t.site}</span></td>"
            f"<td><a href='plates/{esc(t.plate)}.html'>{esc(t.plate)}</a>{ab}</td>"
            f"<td>{t.o_in}</td><td>{t.o_out}</td><td>{t.d_in}</td><td>{t.d_out}</td>"
            f"<td>{fmt_hm(t.origin_wait_h)}</td><td>{fmt_hm(t.travel_h)}</td><td>{fmt_hm(t.dest_wait_h)}</td></tr>"
        )

    merged_all_rows = interleaved_matched_unmatched_rows_html(
        trips,
        unmatched,
        trip_row,
        plate=None,
        include_plate_link=True,
        include_plate_column=True,
    )

    def trip_row_plate(t: Trip) -> str:
        ab = " <span class='badge abn'>ABNORMAL</span>" if t.travel_flag else ""
        return (
            f"<tr><td>{t.origin_date}</td><td>{t.dest_date}</td><td>{t.site}{ab}</td>"
            f"<td>{t.o_in}</td><td>{t.o_out}</td><td>{t.d_in}</td><td>{t.d_out}</td>"
            f"<td>{fmt_hm(t.origin_wait_h)}</td><td>{fmt_hm(t.travel_h)}</td><td>{fmt_hm(t.dest_wait_h)}</td></tr>"
        )

    daily_act_rows_html = "".join(
        f"<tr><td>{d}</td><td>{s['trucks']}</td><td>{s['trips']}</td><td>{s['commit']}</td><td>{s['short']}</td>"
        f"<td>{len(s['bigc_p'])}</td><td>{s['bigc_t']}</td><td>{len(s['lcb_p'])}</td><td>{s['lcb_t']}</td></tr>"
        for d, s in daily_rows
    )

    tpd_rows_html = "".join(
        f"<tr><td>{r['dest_date']}</td><td>{r['matched_trips']}</td><td>{r['active_trucks']}</td></tr>"
        for r in customer_trips_per_day_rows(trips)
    ) or "<tr><td colspan=3>ไม่มีข้อมูล</td></tr>"

    dt_rows_html = "".join(
        f"<tr><td>{d}</td><td><a href='plates/{esc(p)}.html'>{esc(p)}</a></td>"
        f"<td><span class='badge {'bigc' if site=='BigC' else 'lcb'}'>{site}</span></td>"
        f"<td>{fmt_hm(cycle_h)}</td><td>{fmt_hm(m_ow)}</td><td>{fmt_hm(m_dw)}</td><td>{fmt_hm(m_tr)}</td>"
        f"<td>{fmt_hm(um_ow)}</td><td>{fmt_hm(um_dw)}</td><td>{fmt_hm(ad_ow)}</td><td>{fmt_hm(ad_dw)}</td><td>{fmt_hm(comb)}</td></tr>"
        for d, p, site, cycle_h, m_ow, m_dw, m_tr, um_ow, um_dw, ad_ow, ad_dw, comb, gap in daily_time
    )

    abn_rows_html = "".join(
        f"<tr><td>{t.origin_date}</td><td>{t.dest_date}</td><td><a href='plates/{esc(t.plate)}.html'>{esc(t.plate)}</a></td>"
        f"<td>{t.site}</td><td>{t.o_out}</td><td>{t.d_in}</td><td>{fmt_hm(t.travel_h)}</td></tr>"
        for t in abn
    )

    lt_rows_html = "".join(
        f"<tr><td>{r['dest_date']}</td><td><a href='plates/{esc(r['plate'])}.html'>{esc(r['plate'])}</a></td>"
        f"<td><span class='badge {'bigc' if r['site']=='BigC' else 'lcb'}'>{r['site']}</span></td>"
        f"<td>{r['trips_that_day']}</td><td>{'Y' if r['auto_1trip'] else 'N'}</td>"
        f"<td>{esc(r.get('override_action',''))}</td><td>{esc(r.get('override_note',''))}</td>"
        f"<td>{r['trip_rate_baht']:,}</td><td class='money'>{r['surcharge_baht']:,}</td></tr>"
        for r in fifty_rows
    )

    # Audit table — สรุปเหตุผลรายวัน/ทะเบียน (เพิ่มใหม่)
    audit_html = "".join(
        f"<tr><td>{r['dest_date']}</td>"
        f"<td><a href='plates/{esc(r['plate'])}.html'>{esc(r['plate'])}</a></td>"
        f"<td><span class='badge {'bigc' if r['site']=='BigC' else 'lcb'}'>{r['site']}</span></td>"
        f"<td>{r['matched_trips']}</td><td>{r['trip_rate_baht']:,}</td>"
        f"<td>{r['base_line_baht']:,}</td>"
        f"<td class='{'money' if r['fifty_pct_baht'] else ''}'>{r['fifty_pct_baht']:,}</td>"
        f"<td class='money'>{r['customer_day_baht']:,}</td>"
        f"<td class='note'>{esc(r['billing_note'])}</td></tr>"
        for r in audit_rows
    )

    css = (
        "body{font-family:Segoe UI,Tahoma,sans-serif;margin:24px;background:#f4f7fb;color:#152235}"
        "a{color:#0b57d0;text-decoration:none}a:hover{text-decoration:underline}"
        ".h1{font-size:30px;font-weight:700;margin-bottom:4px}.sub{color:#4b5b74;margin-bottom:16px;font-size:13px}"
        ".grid{display:grid;grid-template-columns:repeat(4,minmax(180px,1fr));gap:10px;margin-bottom:14px}"
        ".card{background:#fff;border-radius:10px;padding:12px;box-shadow:0 2px 8px rgba(16,24,40,.08)}"
        ".label{font-size:12px;color:#63758f}.value{font-size:28px;font-weight:700}"
        ".money{color:#0d6b3c}.warn{color:#b54708}"
        ".panel{background:#fff;border-radius:10px;padding:14px;box-shadow:0 2px 8px rgba(16,24,40,.08);margin-bottom:14px}"
        "table{width:100%;border-collapse:collapse;font-size:14px}"
        "th,td{padding:8px;border-bottom:1px solid #e6ebf2;text-align:left}th{background:#eef3fa}"
        ".badge{display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;font-weight:700}"
        ".bigc{background:#dfebff;color:#0a4da1}.lcb{background:#e3f5e9;color:#0f6a3b}"
        ".abn{background:#ffe9e9;color:#b42318}.nav{margin-bottom:12px}"
        ".note{color:#4b5b74;font-size:13px}"
        "tr.um td{color:#5a3b00}"
    )

    idx = f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Oatside report</title><style>{css}</style></head><body>
<div class='h1'>Oatside → P&G สรุปรายงาน</div>
<div class='sub'>{sub}</div>
<div class='nav'><a href='trips.html'>ดูเที่ยวทั้งหมด</a></div>
<div class='panel'><h3>สรุปให้ลูกค้า — จำนวนเที่ยวต่อวัน (matched)</h3>
<p class='sub'>นับตาม<strong>วันที่เข้า Dest_In</strong> · รวมทุกทะเบียน · เฉพาะเที่ยวที่จับคู่แล้ว (ไม่รวม Unmatched)</p>
<table><thead><tr><th>วันที่</th><th>จำนวนเที่ยว</th><th>จำนวนรถ (มีเที่ยววันนั้น)</th></tr></thead><tbody>
{tpd_rows_html}
</tbody></table></div>
<div class='grid'>
<div class='card'><div class='label'>เที่ยวจริง</div><div class='value'>{actual}</div></div>
<div class='card'><div class='label'>เที่ยว commit</div><div class='value'>{commit}</div></div>
<div class='card'><div class='label'>เที่ยวขาด</div><div class='value warn'>{short}</div></div>
<div class='card'><div class='label'>ค่าชดเชยเที่ยวขาด</div><div class='value money'>{extra:,}</div></div>
</div>
<div class='grid'>
<div class='card'><div class='label'>ค่าเที่ยวปกติ (A)</div><div class='value money'>{base_baht:,}</div></div>
<div class='card'><div class='label'>ชาร์จ {cfg.one_trip_surcharge_pct:.0f}% (วัน 1 เที่ยว)</div><div class='value money'>{fifty_total_baht:,}</div></div>
<div class='card'><div class='label'>รวมส่วนเพิ่ม</div><div class='value money'>{grand_extra_baht:,}</div></div>
<div class='card'><div class='label'>ยอดรวมลูกค้า</div><div class='value money'>{customer_grand_baht:,}</div></div>
</div>
<div class='panel'><h3>แยกตาม Site (min trips)</h3><table><thead><tr><th>Site</th><th>จริง</th><th>Commit</th><th>ขาด</th><th>ค่าชดเชย</th></tr></thead><tbody>
<tr><td><span class='badge bigc'>BigC</span></td><td>{bc_a}</td><td>{bc_c}</td><td>{bc_s}</td><td>{bc_e:,}</td></tr>
<tr><td><span class='badge lcb'>LCB</span></td><td>{lc_a}</td><td>{lc_c}</td><td>{lc_s}</td><td>{lc_e:,}</td></tr>
</tbody></table></div>
<div class='panel'><h3>Audit Log — เหตุผลการคิดเงิน (รายวัน × ทะเบียน)</h3>
<p class='sub'>ทุกแถวอธิบายว่าวันนั้นทะเบียนนั้นคิดเงินอย่างไร — ใช้อ้างอิงกับลูกค้าเมื่อมีข้อสงสัย</p>
<table><thead><tr><th>วันที่ Dest_In</th><th>ทะเบียน</th><th>Site</th><th>เที่ยว</th><th>เรท(฿)</th><th>ค่าเที่ยว(฿)</th><th>+{cfg.one_trip_surcharge_pct:.0f}%(฿)</th><th>รวม(฿)</th><th>เหตุผล</th></tr></thead><tbody>
{audit_html or "<tr><td colspan=9>ไม่มีข้อมูล</td></tr>"}
</tbody></table></div>
<div class='panel'><h3>กิจกรรมรายวัน (Dest_In date)</h3><table><thead><tr><th>วันที่</th><th>รถ</th><th>เที่ยวจริง</th><th>Commit min</th><th>ขาด</th><th>BigC รถ</th><th>BigC เที่ยว</th><th>LCB รถ</th><th>LCB เที่ยว</th></tr></thead><tbody>{daily_act_rows_html}</tbody></table></div>
<div class='panel'><h3>รายวัน × ทะเบียน (Plate_DestDay)</h3>
<p class='sub'>Base = เที่ยวในวันนั้น × เรท | คอลัมน์ +{cfg.one_trip_surcharge_pct:.0f}% แสดงเมื่อถูก charge (หลัง override)</p>
<table><thead><tr><th>วันที่</th><th>ทะเบียน</th><th>Site</th><th>เที่ยว</th><th>เรท</th><th>ค่าเที่ยว</th><th>+{cfg.one_trip_surcharge_pct:.0f}%</th><th>รวมวัน</th></tr></thead><tbody>
{"".join(f"<tr><td>{r['dest_date']}</td><td><a href='plates/{esc(r['plate'])}.html'>{esc(r['plate'])}</a></td><td><span class='badge {'bigc' if r['site']=='BigC' else 'lcb'}'>{r['site']}</span></td><td>{r['matched_trips']}</td><td>{r['trip_rate_baht']:,}</td><td>{r['base_line_baht']:,}</td><td class='{'money' if r['fifty_pct_baht'] else ''}'>{r['fifty_pct_baht']:,}</td><td class='money'>{r['customer_day_baht']:,}</td></tr>" for r in pday_rows) or "<tr><td colspan=8>ไม่มีข้อมูล</td></tr>"}
</tbody></table></div>
<div class='panel'><h3>รายละเอียด +{cfg.one_trip_surcharge_pct:.0f}% (วันที่วิ่ง 1 เที่ยว)</h3>
<p class='sub'>Auto=Y = ระบบเห็น 1 เที่ยวในวันนั้น | Override: exclude_50 / include_50 จาก oatside_billing_overrides.json</p>
<table><thead><tr><th>วันที่</th><th>ทะเบียน</th><th>Site</th><th>เที่ยว</th><th>Auto</th><th>Override</th><th>Note</th><th>เรท</th><th>+{cfg.one_trip_surcharge_pct:.0f}%</th></tr></thead><tbody>{lt_rows_html if lt_rows_html else f"<tr><td colspan=9>ไม่มี</td></tr>"}</tbody></table></div>
<div class='panel'><h3>Match cycle (Unmatched รวมเข้า wait)</h3>
<p class='sub'>หน่วย H.MM (เช่น 3.30 = 3 ชม. 30 นาที)</p>
<table><thead><tr><th>วันที่</th><th>ทะเบียน</th><th>Site</th><th>Cycle</th><th>Orig Wait</th><th>Dest Wait</th><th>Travel</th><th>UM Orig</th><th>UM Dest</th><th>Adj Orig</th><th>Adj Dest</th><th>Combined</th></tr></thead><tbody>{dt_rows_html}</tbody></table></div>
<div class='panel'><h3>เดินทางผิดปกติ (threshold {fmt_hm(thr)} h.mm)</h3><table><thead><tr><th>Origin Date</th><th>Dest Date</th><th>ทะเบียน</th><th>Site</th><th>Origin Out</th><th>Dest In</th><th>Travel</th></tr></thead><tbody>{abn_rows_html or '<tr><td colspan=7>ไม่มี</td></tr>'}</tbody></table></div>
<div class='panel'><h3>รายทะเบียน</h3><ul>{''.join(f"<li><a href='plates/{esc(p)}.html'>{esc(p)}</a></li>" for p in plates)}</ul></div>
</body></html>"""

    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "index.html").write_text(idx, encoding="utf-8")

    trips_html_content = f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Trips</title><style>{css}</style></head><body>
<div class='h1'>เที่ยวทั้งหมด</div>
<div class='nav'><a href='index.html'>&larr; กลับสรุป</a></div>
<div class='panel'><h3>เที่ยวทั้งหมด (matched + unmatched)</h3>
<p class='sub'>เรียงตามเวลา (matched ใช้ Dest In · unmatched ใช้เวลาขา Origin/Destination) — UM-O/UM-D เว้นฝั่งที่ยังไม่มีคู่เป็น —</p>
<table><thead><tr><th>Origin Date</th><th>Dest Date</th><th>Site</th><th>ทะเบียน</th><th>Origin In</th><th>Origin Out</th><th>Dest In</th><th>Dest Out</th><th>Orig Wait</th><th>Travel</th><th>Dest Wait</th></tr></thead><tbody>
{merged_all_rows}
</tbody></table></div>
</body></html>"""
    (report_dir / "trips.html").write_text(trips_html_content, encoding="utf-8")

    plates_dir = report_dir / "plates"
    plates_dir.mkdir(exist_ok=True)
    for old in plates_dir.glob("*.html"):
        old.unlink()
    by_plate: dict[str, list[Trip]] = defaultdict(list)
    for t in trips:
        by_plate[t.plate].append(t)
    for p, lst in by_plate.items():
        by_day: dict[date, list[Trip]] = defaultdict(list)
        for t in lst:
            by_day[t.dest_date].append(t)
        day_rows = []
        for d in sorted(by_day.keys()):
            cnt = len(by_day[d])
            fr = fifty_by_key.get((p, d))
            badge = ""
            if fr is not None:
                badge = f" <span class='badge abn'>+{cfg.one_trip_surcharge_pct:.0f}% {fr['surcharge_baht']:,}</span>"
            elif cnt == 1:
                badge = " <span class='badge lcb'>1 เที่ยว (ไม่เก็บ +%)</span>"
            day_rows.append(f"<tr><td>{d}</td><td>{cnt}</td><td>{badge}</td></tr>")
        day_tbl = "".join(day_rows)
        merged_plate_rows = interleaved_matched_unmatched_rows_html(
            lst,
            unmatched,
            trip_row_plate,
            plate=p,
            include_plate_link=False,
            include_plate_column=False,
        )
        pg = f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{esc(p)}</title><style>{css}</style></head><body>
<div class='h1'>ทะเบียน {esc(p)}</div>
<div class='nav'><a href='../index.html'>&larr; กลับสรุป</a> | <a href='../trips.html'>ดูเที่ยวทั้งหมด</a></div>
<div class='panel'><h3>รายวัน (Dest_In)</h3><table><thead><tr><th>วันที่</th><th>เที่ยว</th><th>หมายเหตุ billing</th></tr></thead><tbody>{day_tbl}</tbody></table></div>
<div class='panel'><h3>รายเที่ยว (matched + unmatched)</h3>
<p class='sub'>เรียงตามเวลา (matched ใช้ Dest In · unmatched ใช้เวลาขา Origin/Destination) — UM-O/UM-D เว้นฝั่งที่ยังไม่มีคู่เป็น —</p>
<table><thead><tr><th>Origin Date</th><th>Dest Date</th><th>Site</th><th>Origin In</th><th>Origin Out</th><th>Dest In</th><th>Dest Out</th><th>Orig Wait</th><th>Travel</th><th>Dest Wait</th></tr></thead><tbody>{merged_plate_rows}</tbody></table></div>
</body></html>"""
        (plates_dir / f"{p}.html").write_text(pg, encoding="utf-8")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    cfg = load_oatside_config()
    folder = _oatside_dir()
    origin_path, dest_path = discover_gps_files(folder)
    trips, unmatched, _travels = build_trips(origin_path, dest_path, cfg)
    daily_rows = daily_activity_by_dest(trips, cfg)
    daily_time = daily_time_rows(trips, unmatched)
    actual, commit, short, extra = billing_totals(daily_rows, cfg)
    bc_stats = site_billing(daily_rows, cfg)
    overrides = load_billing_overrides()
    fifty_rows, fifty_total = one_trip_fifty_pct_details(trips, overrides, cfg)
    base_baht = base_trips_revenue_baht(trips, cfg)
    pday_rows = plate_dest_day_rows(trips, fifty_rows, cfg)
    audit_rows = audit_log_rows(trips, fifty_rows, overrides, cfg)
    min_trip_money = int(extra) if cfg.charge_min_trip_shortfall else 0
    if not cfg.charge_min_trip_shortfall:
        bc_a, bc_c, bc_s, bc_e, lc_a, lc_c, lc_s, lc_e = bc_stats
        bc_stats = (bc_a, bc_c, bc_s, 0, lc_a, lc_c, lc_s, 0)
    grand_extra = min_trip_money + int(fifty_total)
    customer_grand_baht = int(base_baht) + int(grand_extra)

    xlsx_out = folder / "Oatside_PG_Trip_Summary_By_Site.xlsx"
    write_excel(
        xlsx_out,
        origin_path.name,
        dest_path.name,
        trips,
        unmatched,
        daily_time,
        daily_rows,
        fifty_rows,
        int(fifty_total),
        min_trip_money,
        audit_rows,
        cfg,
    )

    report_dir = _root() / "TransportRateCalculator" / "reports" / "oatside-apr2026"
    write_html(
        report_dir,
        origin_path.name,
        trips,
        daily_rows,
        daily_time,
        actual,
        commit,
        short,
        min_trip_money,
        bc_stats,
        fifty_rows,
        int(fifty_total),
        grand_extra,
        int(base_baht),
        int(customer_grand_baht),
        pday_rows,
        audit_rows,
        unmatched,
        cfg,
    )

    print(f"Config:  {_config_path()}")
    print(f"Trips: {len(trips)} | Unmatched legs: {len(unmatched)}")
    print(f"Excel:   {xlsx_out}")
    print(f"HTML:    {report_dir}")


if __name__ == "__main__":
    main()
