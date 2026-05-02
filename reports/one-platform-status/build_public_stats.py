"""
Generate public-stats.json from local SQLite app.db (no PII).
Run from repo root: python ProjectYK_System/docs-public/one-platform-status/build_public_stats.py
Or from this dir: python build_public_stats.py (auto-find app.db)
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def find_db() -> Path:
    here = Path(__file__).resolve().parent
    candidates = [
        here.parents[2] / "app" / "app.db",
        here.parents[1] / "app" / "app.db",
        Path("ProjectYK_System/app/app.db"),
        Path("../app/app.db"),
    ]
    for p in candidates:
        if p.exists():
            return p.resolve()
    raise FileNotFoundError("app.db not found; run from Project YK repo root")


def main() -> None:
    db_path = find_db()
    out_path = Path(__file__).resolve().parent / "public-stats.json"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    tables = [r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
    ).fetchall()]

    def count(table: str) -> int | None:
        if table not in tables:
            return None
        try:
            return int(cur.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0])
        except sqlite3.Error:
            return None

    # Core tables (SQLModel default names are lowercased class names)
    row_counts = {
        "employee": count("employee"),
        "vehicle": count("vehicle"),
        "customer": count("customer"),
        "dailyjob": count("dailyjob"),
        "pettycashtxn": count("pettycashtxn"),
        "payrun": count("payrun"),
        "payrunitem": count("payrunitem"),
        "driversession": count("driversession"),
        "driversubmission": count("driversubmission"),
        "loan": count("loan"),
        "loanpayment": count("loanpayment"),
        "maintenanceworkorder": count("maintenanceworkorder"),
        "maintrecord": count("maintrecord"),
    }

    daily_range = None
    if "dailyjob" in tables:
        row = cur.execute(
            "SELECT MIN(work_date), MAX(work_date) FROM dailyjob WHERE work_date IS NOT NULL"
        ).fetchone()
        if row and row[0]:
            daily_range = {"min": row[0], "max": row[1]}

    emp_by_site: dict[str, int] = {}
    if "employee" in tables:
        for site, n in cur.execute(
            "SELECT home_site_code, COUNT(*) FROM employee GROUP BY home_site_code ORDER BY home_site_code"
        ).fetchall():
            emp_by_site[str(site or "")] = int(n)

    vehicles_by_site: dict[str, int] = {}
    if "vehicle" in tables:
        for site, n in cur.execute(
            "SELECT home_site_code, COUNT(*) FROM vehicle GROUP BY home_site_code ORDER BY home_site_code"
        ).fetchall():
            vehicles_by_site[str(site or "")] = int(n)

    petty_range = None
    if "pettycashtxn" in tables:
        # try common txn_date / work_date column names
        for col in ("txn_date", "work_date", "book_date", "created_at"):
            try:
                row = cur.execute(
                    f'SELECT MIN("{col}"), MAX("{col}") FROM pettycashtxn WHERE "{col}" IS NOT NULL'
                ).fetchone()
                if row and row[0]:
                    petty_range = {"column": col, "min": str(row[0])[:10], "max": str(row[1])[:10]}
                    break
            except sqlite3.Error:
                continue

    payroll_cycles = None
    payrun_by_status: dict[str, int] = {}
    if "payrun" in tables:
        try:
            payroll_cycles = int(
                cur.execute("SELECT COUNT(DISTINCT pay_cycle_tag) FROM payrun").fetchone()[0]
            )
        except sqlite3.Error:
            payroll_cycles = None
        try:
            for st, n in cur.execute(
                "SELECT status, COUNT(*) FROM payrun GROUP BY status ORDER BY status"
            ).fetchall():
                payrun_by_status[str(st or "")] = int(n)
        except sqlite3.Error:
            pass

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "db_path_hint": "ProjectYK_System/app/app.db (local dev)",
        "db_file_bytes": db_path.stat().st_size,
        "table_row_counts": {k: v for k, v in row_counts.items() if v is not None},
        "daily_job_work_date_range": daily_range,
        "employee_count_by_home_site": emp_by_site,
        "vehicle_count_by_home_site": vehicles_by_site,
        "petty_date_range": petty_range,
        "payroll_distinct_cycle_tags": payroll_cycles,
        "payrun_by_status": payrun_by_status or None,
        "disclaimer_th": "สถิติรวมจากฐานข้อมูลพัฒนา (app.db) — ไม่มีชื่อบุคคล/ทะเบียน/ยอดเงินรายบรรทัด — โพสต์บน URL สาธารณะได้",
    }

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out_path} from {db_path}")


if __name__ == "__main__":
    main()
