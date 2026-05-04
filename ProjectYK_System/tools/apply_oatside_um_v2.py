# -*- coding: utf-8 -*-
"""Single-file patch: UM timing columns + leg_timeline (read/write Oatside/build_oatside_reports.py)."""
from __future__ import annotations

from pathlib import Path

P = Path(r"c:\Users\Home\Desktop\Project YK\Oatside\build_oatside_reports.py")


def main() -> None:
    s = P.read_text(encoding="utf-8")
    o = s

    # 1) Helpers after hours()
    anchor = (
        "def hours(a: datetime, b: datetime) -> float:\n"
        "    return (b - a).total_seconds() / 3600.0\n\n\n"
        "def customer_idle_clip_dest_wait_h"
    )
    insert = (
        "def hours(a: datetime, b: datetime) -> float:\n"
        "    return (b - a).total_seconds() / 3600.0\n\n\n"
        "def build_leg_timeline_by_plate(o_legs: list[Leg], d_legs: list[Leg]) -> dict[str, list[Leg]]:\n"
        '    """Merge Origin+Dest legs per plate, sorted by In time (gap to next In)."""\n'
        "    by: dict[str, list[Leg]] = defaultdict(list)\n"
        "    for L in o_legs + d_legs:\n"
        "        by[L.plate].append(L)\n"
        "    for p in by:\n"
        "        by[p].sort(key=lambda z: z.t_in)\n"
        "    return by\n\n\n"
        "def um_leg_dwell_gap_h(leg: Leg, timeline: list[Leg] | None) -> tuple[float, float | None]:\n"
        '    """Dwell at stop (Out−In); gap hours from this Out to next leg In on same plate."""\n'
        "    dwell = max(0.0, hours(leg.t_in, leg.t_out))\n"
        "    if not timeline:\n"
        "        return dwell, None\n"
        "    idx = next((i for i, L in enumerate(timeline) if L is leg), None)\n"
        "    if idx is None or idx + 1 >= len(timeline):\n"
        "        return dwell, None\n"
        "    gap = hours(leg.t_out, timeline[idx + 1].t_in)\n"
        "    return dwell, gap\n\n\n"
        "def customer_idle_clip_dest_wait_h"
    )
    if "def build_leg_timeline_by_plate" not in s:
        if anchor not in s:
            raise SystemExit("hours anchor missing")
        s = s.replace(anchor, insert, 1)

    # 2) unmatched_merged signature + body tail
    s = s.replace(
        """def unmatched_merged_trip_one_row_html(
    src: str,
    leg: Leg,
    *,
    include_plate_link: bool = True,
    include_plate_column: bool = True,
) -> str:""",
        """def unmatched_merged_trip_one_row_html(
    src: str,
    leg: Leg,
    *,
    dwell_h: float,
    gap_h: float | None,
    include_plate_link: bool = True,
    include_plate_column: bool = True,
) -> str:""",
        1,
    )

    s = s.replace(
        """        f"<td>{dash}</td><td>{dash}</td><td>{dash}</td>"
        f"<td>{dash}</td><td>{dash}</td><td>{dash}</td><td>{dash}</td><td>{dash}</td></tr>"
    )""",
        """        f"<td>{dash}</td><td>{dash}</td><td>{dash}</td>"
        f"<td>{fmt_hm(dwell_h)}</td><td>{fmt_hm(gap_h) if gap_h is not None else dash}</td>"
        f"<td>{dash}</td><td>{dash}</td><td>{dash}</td><td>{dash}</td><td>{dash}</td></tr>"
    )""",
        1,
    )

    # 3) interleaved signature + um call
    s = s.replace(
        """def interleaved_matched_unmatched_rows_html(
    trips: list[Trip],
    unmatched: list[tuple[str, Leg, str]],
    trip_row_cb: Callable[[Trip], str],
    *,
    plate: str | None = None,
    include_plate_link: bool = True,
    include_plate_column: bool = True,
) -> str:""",
        """def interleaved_matched_unmatched_rows_html(
    trips: list[Trip],
    unmatched: list[tuple[str, Leg, str]],
    trip_row_cb: Callable[[Trip], str],
    *,
    plate: str | None = None,
    include_plate_link: bool = True,
    include_plate_column: bool = True,
    leg_timeline_by_plate: dict[str, list[Leg]] | None = None,
) -> str:""",
        1,
    )

    s = s.replace(
        """        um_html = unmatched_merged_trip_one_row_html(
            src,
            leg,
            include_plate_link=include_plate_link,
            include_plate_column=include_plate_column,
        )""",
        """        _dw, _gp = um_leg_dwell_gap_h(
            leg, leg_timeline_by_plate.get(leg.plate) if leg_timeline_by_plate else None
        )
        um_html = unmatched_merged_trip_one_row_html(
            src,
            leg,
            dwell_h=_dw,
            gap_h=_gp,
            include_plate_link=include_plate_link,
            include_plate_column=include_plate_column,
        )""",
        1,
    )

    # 4) trip_row — insert — — before money (matched rows)
    s = s.replace(
        """            f"{_td_wait_h(t.origin_wait_h, _hi_o, False)}<td>{fmt_hm(t.travel_h)}</td>{_td_wait_h(t.dest_wait_h, _hi_d, True)}"
            f"{money}</tr>"
        )

    merged_all_rows = interleaved_matched_unmatched_rows_html(""",
        """            f"{_td_wait_h(t.origin_wait_h, _hi_o, False)}<td>{fmt_hm(t.travel_h)}</td>{_td_wait_h(t.dest_wait_h, _hi_d, True)}"
            f"<td>—</td><td>—</td>"
            f"{money}</tr>"
        )

    merged_all_rows = interleaved_matched_unmatched_rows_html(""",
        1,
    )

    # 5) trip_row_plate
    s = s.replace(
        """            f"{_td_wait_h(t.origin_wait_h, _hi_o, False)}<td>{fmt_hm(t.travel_h)}</td>{_td_wait_h(t.dest_wait_h, _hi_d, True)}"
            f"{money}</tr>"
        )

    daily_act_rows_html = "".join(""",
        """            f"{_td_wait_h(t.origin_wait_h, _hi_o, False)}<td>{fmt_hm(t.travel_h)}</td>{_td_wait_h(t.dest_wait_h, _hi_d, True)}"
            f"<td>—</td><td>—</td>"
            f"{money}</tr>"
        )

    daily_act_rows_html = "".join(""",
        1,
    )

    # 6) write_html signature
    s = s.replace(
        """    unmatched: list[tuple[str, Leg, str]],
    nw_total_baht: int,
    cfg: OatsideConfig,
    cpd_rows: list[dict],
) -> None:""",
        """    unmatched: list[tuple[str, Leg, str]],
    nw_total_baht: int,
    cfg: OatsideConfig,
    cpd_rows: list[dict],
    leg_timeline_by_plate: dict[str, list[Leg]],
) -> None:""",
        1,
    )

    # 7) um_section_html block — replace join with loop-style (clear)
    old_um = """    um_section_html = "".join(
        f"<tr><td><span class='badge abn'>{'UM-O' if src == 'Origin' else 'UM-D'}</span></td>"
        f"<td><a href='plates/{esc(leg.plate)}.html'>{esc(leg.plate)}</a></td>"
        f"<td>{leg.t_in}</td><td>{leg.t_out}</td>"
        f"<td class='note'>{'Origin ไม่มีคู่' if src == 'Origin' else 'Dest ไม่มีคู่'}</td></tr>"
        for src, leg, _ in sorted(unmatched, key=lambda x: x[1].t_in)
    ) or "<tr><td colspan=5 class='note'>ไม่มี Unmatched</td></tr>\""""
    new_um = """    _um_rows: list[str] = []
    for src, leg, _ in sorted(unmatched, key=lambda x: x[1].t_in):
        _dwell, _gap = um_leg_dwell_gap_h(leg, leg_timeline_by_plate.get(leg.plate))
        _gap_cell = fmt_hm(_gap) if _gap is not None else "—"
        _um_rows.append(
            f"<tr><td><span class='badge abn'>{'UM-O' if src == 'Origin' else 'UM-D'}</span></td>"
            f"<td><a href='plates/{esc(leg.plate)}.html'>{esc(leg.plate)}</a></td>"
            f"<td>{leg.t_in}</td><td>{leg.t_out}</td>"
            f"<td class='note'>{fmt_hm(_dwell)}</td><td class='note'>{_gap_cell}</td>"
            f"<td class='note'>{'Origin ไม่มีคู่' if src == 'Origin' else 'Dest ไม่มีคู่'}</td></tr>"
        )
    um_section_html = "".join(_um_rows) or "<tr><td colspan=7 class='note'>ไม่มี Unmatched</td></tr>\""""
    if old_um not in s:
        if "_um_rows" in s and "colspan=7" in s:
            pass
        else:
            raise SystemExit("um_section block pattern not found")
    else:
        s = s.replace(old_um, new_um, 1)

    # 8) index thead
    s = s.replace(
        "<table><thead><tr><th>ประเภท</th><th>ทะเบียน</th><th>เวลาเข้า</th><th>เวลาออก</th><th>เหตุผล</th></tr></thead><tbody>",
        "<table><thead><tr><th>ประเภท</th><th>ทะเบียน</th><th>เวลาเข้า</th><th>เวลาออก</th>"
        "<th>อยู่จุด (ชม.)</th><th>ถึงเข้าครั้งถัดไป (ชม.)</th><th>เหตุผล</th></tr></thead><tbody>",
        1,
    )

    # 9) trips + plate thead (Dest Wait before money)
    s = s.replace(
        "<th>Dest Wait</th><th>ค่าขนส่ง(฿)</th>",
        "<th>Dest Wait</th><th>อยู่จุด UM (ชม.)</th><th>ถึงเข้าครั้งถัดไป (ชม.)</th><th>ค่าขนส่ง(฿)</th>",
        2,
    )

    # 10) merged_all_rows / merged_plate_rows kwargs
    s = s.replace(
        """    merged_all_rows = interleaved_matched_unmatched_rows_html(
        trips,
        unmatched,
        trip_row,
        plate=None,
        include_plate_link=True,
        include_plate_column=True,
    )""",
        """    merged_all_rows = interleaved_matched_unmatched_rows_html(
        trips,
        unmatched,
        trip_row,
        plate=None,
        include_plate_link=True,
        include_plate_column=True,
        leg_timeline_by_plate=leg_timeline_by_plate,
    )""",
        1,
    )

    s = s.replace(
        """        merged_plate_rows = interleaved_matched_unmatched_rows_html(
            lst,
            unmatched,
            trip_row_plate,
            plate=p,
            include_plate_link=False,
            include_plate_column=False,
        )""",
        """        merged_plate_rows = interleaved_matched_unmatched_rows_html(
            lst,
            unmatched,
            trip_row_plate,
            plate=p,
            include_plate_link=False,
            include_plate_column=False,
            leg_timeline_by_plate=leg_timeline_by_plate,
        )""",
        1,
    )

    # 11) write_excel signature + Unmatched excel
    s = s.replace(
        """    pday_rows: list[dict],
    cpd_rows: list[dict],
) -> None:
    base_baht = base_trips_revenue_baht(trips, cfg) + sum_manual_extra_baht(cfg)""",
        """    pday_rows: list[dict],
    cpd_rows: list[dict],
    leg_timeline_by_plate: dict[str, list[Leg]],
) -> None:
    base_baht = base_trips_revenue_baht(trips, cfg) + sum_manual_extra_baht(cfg)""",
        1,
    )

    s = s.replace(
        """    um.append(["Source", "Plate", "Device", "Row_No", "In", "Out"])
    for src, leg, _ in sorted(unmatched, key=lambda x: (x[2], x[1].t_in)):
        um.append([src, leg.plate, leg.device, leg.row_no, leg.t_in, leg.t_out])""",
        """    um.append(
        ["Source", "Plate", "Device", "Row_No", "In", "Out", "Dwell_h", "Gap_to_next_In_h"]
    )
    for src, leg, _ in sorted(unmatched, key=lambda x: (x[2], x[1].t_in)):
        d_dw, g_gap = um_leg_dwell_gap_h(leg, leg_timeline_by_plate.get(leg.plate))
        um.append(
            [
                src,
                leg.plate,
                leg.device,
                leg.row_no,
                leg.t_in,
                leg.t_out,
                round(d_dw, 4),
                round(g_gap, 4) if g_gap is not None else "",
            ]
        )""",
        1,
    )

    # 12) main
    s = s.replace(
        """    o_legs_all = parse_legs(origin_path)
    nw_rows, nw_total = no_work_outbound_rows(trips, cfg)""",
        """    o_legs_all = parse_legs(origin_path)
    leg_timeline_by_plate = build_leg_timeline_by_plate(o_legs_all, parse_legs(dest_path))
    nw_rows, nw_total = no_work_outbound_rows(trips, cfg)""",
        1,
    )

    s = s.replace(
        """        cpd_rows,
    )
    report_dir = _root() / "TransportRateCalculator" / "reports" / "oatside-apr2026"
    write_split_excel_exports(""",
        """        cpd_rows,
        leg_timeline_by_plate,
    )
    report_dir = _root() / "TransportRateCalculator" / "reports" / "oatside-apr2026"
    write_split_excel_exports(""",
        1,
    )

    s = s.replace(
        """        cpd_rows,
    )

    print(f"Config:  {_config_path()}")""",
        """        cpd_rows,
        leg_timeline_by_plate,
    )

    print(f"Config:  {_config_path()}")""",
        1,
    )

    if s == o:
        print("no changes (already patched?)")
    else:
        P.write_text(s, encoding="utf-8")
        print("patched", P)


if __name__ == "__main__":
    main()
