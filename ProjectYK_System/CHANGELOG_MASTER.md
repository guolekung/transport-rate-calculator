# Project YK Master Changelog

สรุปการตัดสินใจสำคัญระดับภาพรวมข้ามทุกโมดูล

## 2026-05-04 (Oatside HTML — hero หน้าเที่ยว + Excel ขวาหัวแต่ละตาราง)

- **`Oatside/build_oatside_reports.py`**: ลบบล็อก **คำอธิบายสี / ไฮไลต์ชั่วโมงรอ**; แถบ **hero** ชวนเปิด `trips.html` + ลิงก์ Excel รวม; ลิงก์ **ดาวน์โหลด Excel** อยู่ **ขวาใน `<summary>`** ของแต่ละหัวข้อ; **`trips.html`** เน้น “หน้าหลักลูกค้า” + ปุ่ม Excel Trip Detail ขวาหัวตาราง — **`ProjectYK_System/tools/patch_oatside_hero_xlsx_inline.py`**
- **`Oatside/build_oatside_reports.py`**: CSS `summary.section-sum-row` ให้เต็มความกว้าง + ดันลิงก์ Excel ชิดขวา; ข้อความ **(คลิกเพื่อขยาย)** ของ Audit ย้ายไปหน้าหัวข้อ — **`ProjectYK_System/tools/patch_oatside_summary_flex_audit.py`**

## 2026-05-04 (Oatside Excel — export แยกต่อตาราง + จัดรูปแบบ)

- **`Oatside/build_oatside_reports.py`**: `beautify_oatside_workbook` (หัวตารางสีแบรนด์, zebra, filter, freeze, คอลัมน์เงิน `#,##0`) + **`write_split_excel_exports`** → โฟลเดอร์ **`reports/oatside-apr2026/exports/*.xlsx`** 14 ไฟล์ — **`ProjectYK_System/tools/patch_oatside_excel_exports.py`** (ลิงก์จาก UI ย้ายไปขวาหัวแต่ละตารางใน Session #107)

## 2026-05-01 (Oatside HTML — กรองทะเบียน trips + พับหัวข้อสรุป)

- **`Oatside/build_oatside_reports.py`**: `trips.html` — `<select>` + ช่องค้นหา + `data-plate` ต่อแถว + JS กรอง; **`index.html`** — หัวข้อสรุป/รายทะเบียน ใช้ `<details class='section-fold'>` แบบ Audit — **`ProjectYK_System/tools/apply_oatside_ui_trips_filter_index_fold.py`**

## 2026-05-01 (Oatside — manual_return_trips: ค่าขนส่งขากลับ flat)

- **`Oatside/build_oatside_reports.py`** + **`Oatside/oatside_config.json`**: `manual_return_trips` (ไม่เพิ่ม matched) — คอลัมน์ **ขากลับ(฿)** บน HTML + Excel `Return_trip_baht` / ชีต **`Manual_Return_Trips`** + บรรทัด **R** ใน Customer_Summary — `ProjectYK_System/tools/apply_oatside_manual_return_trips.py`

## 2026-05-01 (Oatside — manual_extra_trips: เที่ยวลูกค้าตกลงแต่ไม่มีใน GPS)

- **`Oatside/build_oatside_reports.py`** + **`Oatside/oatside_config.json`**: `manual_extra_trips` บวกเข้าฐาน/audit/CPD + ชีต **`Manual_Extra_Trips`**; **`ProjectYK_System/tools/patch_oatside_manual_extra_trips.py`** (แก้ anchor + comma ใน default JSON)

## 2026-05-01 (Oatside — คอลัมน์เงิน trips + dedupe origin24h + sticky หัวตาราง)

- **`Oatside/build_oatside_reports.py`**: คำอธิบายใต้ `trips.html` ว่าคอลัมน์เงินไม่ได้มาจากชั่วโมง Dest Wait โดยตรง; **อย่างมากหนึ่ง** surcharge `origin24h` ต่อ `(ทะเบียน, วัน Dest_In)` เพื่อกันซ้ำ 3,750+3,750=7,500; ตารางเที่ยวใช้ **`.table-scroll` + `thead th` sticky** (`trips.html`, `plates/*.html`)
- **`Oatside/build_oatside_reports.py`**: แถวตารางเที่ยวแบ่งโทนสีตามวัน (`day-band-0`/`day-band-1`; matched ยึด **Origin_In**, UM-D ใช้เวลา leg แทน) + รักษาไฮไลต์รอนาน; **เรียง matched ตาม `Origin_In`** ใน `interleaved_matched_unmatched_rows_html`

## 2026-05-01 (Oatside HTML — ป้าย surcharge: +100% ข้ามคืน + แยก ตีเปล่า / ค่าเสียเวลา)

- **`Oatside/build_oatside_reports.py`**: `fifty_kind` + `html_fifty_surcharge_badge` + คอลัมน์ **`Fifty_kind`** ใน Excel; การ์ด/ตาราง HTML ใช้คำว่า **ส่วนเพิ่ม** แทน +50% ตายตัว — `ProjectYK_System/tools/apply_oatside_fifty_patch.py`, `patch_oatside_audit_sub.py`
- **แก้ #98**: default วันงาน Origin 1 เที่ยว = **`downtime_origin_day`** (ป้าย **ค่าเสียเวลา +50%**); **ตีเปล่า** เฉพาะ `action: blank_run` หรือ note มี «ตีเปล่า»; ข้ามคืนเต็มเรท = **ค่าเสียเวลา +100%** — `ProjectYK_System/tools/patch_oatside_fifty_kind_v2.py`
- **#99**: คอลัมน์ส่วนเพิ่ม HTML — **หลายป้ายต่อวัน**; **No-work recovery** แสดงเป็น **ตีเปล่า +50%** ในคอลัมน์เดียวกับ fifty — `patch_oatside_multi_badge_nw.py`

## 2026-05-03 (Oatside — พิมพ์เขียว schema สำหรับ Claude บนเว็บ / Artifacts)

- **`TransportRateCalculator/docs/OATSIDE_BACKEND_SCHEMA.md`**: สรุปข้อมูล/ pipeline / billing / ชีต Excel / HTML สำหรับโยนให้ฝั่งเว็บออกแบบ UI โดยไม่ต้องอ่านทั้ง repo

## 2026-05-02 (Oatside — ปลายทางรอข้ามคืน → fifty เติมตาม `dest_date` + deploy.ps1)

- **`Oatside/build_oatside_reports.py`**: `long_dest_wait_midnight_fifty` + `supplement_long_dest_wait_midnight_fifty` (เช่น 71-6802 รอปลายทางข้ามคืน แต่ไม่มี Origin วันนั้น) — `ProjectYK_System/tools/patch_oatside_midnight_dwell_fifty.py`
- **`long_dest_wait_midnight_full_trip`** (default true): ค่าเติมข้ามคืน = **เรทเต็ม 1 เที่ยว** (ไม่ใช่แค่ +50%); **ไฮไลต์** รอต้นทาง/ปลายทางเกินเกณฑ์ชม. บน HTML — `patch_oatside_full_trip_midnight_highlight.py`
- **`deploy_oatside_report.ps1`**: แก้ `throw`/here-string ที่ทำให้ PowerShell parse พัง

## 2026-05-01 (Oatside — wave3: default `use_origin_24h_fifty` + no-work recovery + phantom/hints)

- **`Oatside/build_oatside_reports.py`**: default **`use_origin_24h_fifty=True`**; **`customer_no_work`** + **`outbound_half_dest_dates`** (auto วันหลังจบช่วง); บรรทัด **D** / รวม grand; **`Trip_Detail.Nw_outbound50_baht`**; ชีต **`NoWork_Outbound_50pct`**, **`Phantom_Trip_Candidates`**, **`Hints_DoubleOrigin`**; HTML **`grand_extra`** รวม no-work — สคริปต์ `ProjectYK_System/tools/apply_oatside_wave3_*.py`
- **นโยบาย recovery + fifty**: โอเลือก **เก็บคู่** (เที่ยวแรกวัน recovery อาจได้ทั้ง fifty ดาวน์ไทม์และ No-work 50% — บวกทั้งคู่); ชีต **Info** แถว **`Policy_recovery_plus_fifty`** — `ProjectYK_System/tools/apply_oatside_recovery_policy_info.py`

## 2026-05-02 (Oatside build — `customer_idle_windows` + optional `use_origin_24h_fifty`)

- **`Oatside/build_oatside_reports.py`**: ตัด `Dest_Wait` ช่วงฝากลูกค้า (`customer_idle_windows`, default **71-8967** 20–29 เม.ย.); `Trip_Detail` คอลัมน์ customer wait/cycle; **`use_origin_24h_fifty`** สลับกฎ +50% เป็น rolling 24h จาก `Origin_In` — `OATSIDE_TRIP_PAIRING_MERGE_HANDOFF.md`; patch scripts ใต้ `ProjectYK_System/tools/patch_oatside_*.py`

## 2026-05-02 (Agent workflow — ถามก่อนลงมือ + Oatside เคส 71-8967)

- **นโยบายทุกแชท**: ถ้าคำสั่งยังกำกวม → **ถามให้เคลียร์ก่อนลงมือ** — `.cursor/rules/oa-careful-default.mdc`, `.cursor/rules/project-yk-context.mdc` §1b, `AGENTS.md`
- **Oatside / ฝากรถ P&G**: **`71-8967`** ช่วง **`2026-04-20 ~14:00`–`2026-04-29 ~17:00` (ไทย)** — เที่ยวส่งก่อนจอด **นับลูกค้าปกติ**; ช่วงจอดในโรงงานหลังนั้น **ไม่เกี่ยวลูกค้า** (ยกเว้น dwell/เตือน); หลัง `Dest_Out` ถ้ามีวิ่งต่อนับตีเปล่าปกติ — `CONTEXT_LOG.md` Session #91

## 2026-05-02 (Oatside — ชีต/หน้าเว็บ «จำนวนเที่ยวต่อวัน» สำหรับลูกค้า)

- `Oatside/build_oatside_reports.py`: **`customer_trips_per_day_rows()`** + ชีต Excel **`Customer_Trips_Per_Day`** + ตารางบน **`index.html`** (นับ matched ตามวันที่ `Dest_In` · รวมทุกทะเบียน) — เอกสาร **`OATSIDE_TRIP_PAIRING_MERGE_HANDOFF.md`**, **`OATSIDE_LOCAL_UPDATE_WITHOUT_UPLOAD.md`**

## 2026-05-02 (Oatside GitHub Pages — path รายงานใหม่ `oatside-pg-2026`)

- **`deploy_oatside_report.ps1`**: **`PagesReportSlug`** (default `oatside-pg-2026`) + **`RemoveLegacyApr2026`** ลบ `reports/oatside-apr2026` เมื่อ deploy — **`deploy_oatside_report_one_click.bat`** ส่ง `-RemoveLegacyApr2026 $true` ให้ลิงก์เก่า 404 หลัง push; อัปเดตลิงก์ใน **`OATSIDE_LOCAL_UPDATE_WITHOUT_UPLOAD.md`**, **`NEXT_ACTION_PLAN.md`**, **`docs-public/one-platform-status/index.html`**

## 2026-05-02 (Payroll + Petty — unlinked ที่ `site_code` ว่างไม่ถูกนับใน guardrail)

- **ปัญหา**: แถวหักสดย่อย pending + ยังไม่ผูกคนขับแต่ `site_code` ว่าง → แบนเนอร์ payroll / finalize gate เดิมมองไม่เห็น (กรองแค่ไซต์รอบ)
- **แก้**: `main.py` — `_petty_unlinked_predicates_for_payrun` + stale petty scan; `payroll_detail.html` — ลิงก์สดย่อยใช้ `cycle=`; `payroll.py` + `payroll_slip.py` — รวม `site_code` ว่างเมื่อคิดยอด/สลิป

## 2026-05-02 (Cloud demo — Postgres + Basic auth + คู่มือฟรี)

- **`DATABASE_URL`** → แอปใช้ **PostgreSQL**; ไม่ตั้ง = SQLite เดิม (`db_config.py`, แก้ `main.py` + `_ensure_column` เฉพาะ SQLite)
- **`preview_auth.py`** + env **`YK_PREVIEW_AUTH` / `YK_PREVIEW_USER` / `YK_PREVIEW_PASSWORD`** — HTTP Basic กันคนนอก (ยกเว้น `/health`, `/static/`, `/uploads/`)
- **`ProjectYK_System/tools/sqlite_to_postgres.py`** + **`psycopg2-binary`** — ย้าย `app.db` → Postgres (`--wipe` บังคับ)
- **`ProjectYK_System/docs/HOSTING_FREE_DEMO_TH.md`** + **`render.yaml`** (ราก repo) — Neon + Render แบบฟรี
- **`ProjectYK_System/tools/cloud_demo_setup.ps1`** — รันบนเครื่องหลังได้ `DATABASE_URL` จาก Neon: pip + migrate + พิมพ์ env สำหรับ Render
- **`AGENT_BOOTSTRAP.md`** — ลิงก์คู่มือโฮสต์

## 2026-05-02 (Static pitch — One Platform สำหรับ GitHub Pages)

- เพิ่ม **`ProjectYK_System/docs-public/one-platform-status/index.html`** — หน้า HTML สรุป roadmap/สถานะระบบ (ไทย) + ลิงก์ไป Calculator root และรายงาน Oatside บน `yk-logistics.github.io`
- **`README_DEPLOY.md`** ในโฟลเดอร์เดียวกัน — วิธีคัดลอกไป `transport-rate-calculator/reports/one-platform-status/` แล้ว push
- **`build_public_stats.py`** + **`public-stats.json`** — ดึงสถิติจริงจาก `app.db` (จำนวนแถว / ช่วงวันที่ / จำนวนตามไซท์) ไม่มีชื่อคนหรือยอดเงินรายบรรทัด; หน้า `index.html` โหลด JSON แบบ `fetch`
- Push ขึ้น **`yk-logistics/transport-rate-calculator`** แล้ว (โฟลเดอร์ `reports/one-platform-status/` บนเครื่อง `transport-rate-calculator-repo`)
- หน้า pitch: เพิ่ม **`assets/screenshot-daily-desktop.png`** (หน้า Daily จริง) + คำอธิบายว่า GitHub Pages ไม่รัน FastAPI; ลบหัวข้องบ AI/IDE และ bullet Open-book / Profit share

## 2026-05-01 (Oatside — `match_plate` ปลายทางก่อน + ต้นทางล่าสุดก่อน Dest_In)

- `Oatside/build_oatside_reports.py`: แทนที่ origin-first greedy ด้วยการไล่ **`Dest` ตามเวลา** แล้วเลือก **`Origin_Out` ล่าสุด** ที่ feasible — ลด UM ผิดพลาด + ลดการชน `demote_chronology_violations` เป็นวง (ตัวอย่าง 71-6802 คู่ 19:51→21:35); เอกสาร **`OATSIDE_TRIP_PAIRING_MERGE_HANDOFF.md`** §4 — build ล่าสุด **Trips 105 | Unmatched 15**

## 2026-05-01 (Oatside — อธิบาย UM 71-6802: greedy + chronology demote + build Origin 07-15-32)

- เอกสาร **`TransportRateCalculator/docs/OATSIDE_TRIP_PAIRING_MERGE_HANDOFF.md`** (กรณีจอ UM 14:22/18:46) + **`OATSIDE_ORIGIN_CHAIN_MERGE_FIX.md`**; สคริปต์ **`ProjectYK_System/tools/run_oatside_may02_build.py`** ชี้ `...07-15-32 Oatside.xlsx` — build ล่าสุด **Trips 90 | Unmatched 45** (คู่กับ P&G `06-58-42`)

## 2026-05-01 (Oatside — ปิด chain-merge Origin ได้ทั้งก้อน + build ชุด GPS 02.05.2026)

- `Oatside/build_oatside_reports.py` + `oatside_config.json` template: **`enable_origin_chain_merge`** default **false** → ไม่รวมหลายแถวต้นทางก่อนปลายทาง; ตั้ง **true** ถ้าต้องการ merge พร้อม **`max_origin_chain_gap_h`** — อัปเดต **`TransportRateCalculator/docs/OATSIDE_ORIGIN_CHAIN_MERGE_FIX.md`** + สคริปต์ตัวอย่าง **`ProjectYK_System/tools/run_oatside_may02_build.py`**

## 2026-05-01 (Oatside — แก้ chain-merge Origin ผิดเมื่อปลายทางมาช้า)

- `merge_chained_origin_pairs(pairs, cfg.max_origin_chain_gap_h)`: หยุดรวมเมื่อช่องว่าง `Origin_Out` → `Origin_In` ช่วงถัดไปเกินเกณฑ์ — `OatsideConfig` + `oatside_config.json` **`max_origin_chain_gap_h`** (ค่าเริ่มต้น 3 ชม.) + เอกสาร **`TransportRateCalculator/docs/OATSIDE_ORIGIN_CHAIN_MERGE_FIX.md`**

## 2026-05-01 (Oatside HTML — Unmatched แทรกตามเวลา Dest In / leg.t_in)

- `Oatside/build_oatside_reports.py`: `interleaved_matched_unmatched_rows_html()` — เรียง matched (`d_in`) กับ unmatched (`leg.t_in`) ในตารางเดียว; `trips.html` / `plates/*.html`

## 2026-05-01 (Oatside HTML — Unmatched รวมแถวในตารางเดียวกับ matched)

- `Oatside/build_oatside_reports.py`: `unmatched_merged_trip_rows_html()` — แถว UM-O/UM-D ใช้คอลัมน์เดียวกับเที่ยว matched; เว้นวัน/เวลาฝั่งที่ยังไม่มีคู่เป็น em dash; `trips.html` / `plates/*.html` ตารางเดียว

## 2026-05-01 (Oatside — ปิดเก็บเงินค่าชดเชย min trips เมื่อใช้ชาร์จ 50%)

- `Oatside/build_oatside_reports.py` + `oatside_config.json` default: **`charge_min_trip_shortfall`** default **false** → ยอดลูกค้า = base + 50% เท่านั้น (การ์ด/Excel ยังโชว์เที่ยวขาดเป็น KPI แต่เงินชดเชย = 0); ตั้ง **true** ถ้าต้องการโหมดเก็บทั้งค่าชดเชย + 50% แบบเดิม

## 2026-05-01 (GitHub — Oatside/Pages repo อยู่ org `yk-logistics`)

- Repo **`yk-logistics/transport-rate-calculator`** + Pages รายงาน Oatside (อัปเดต path): `https://yk-logistics.github.io/transport-rate-calculator/reports/oatside-pg-2026/index.html` — เอกสาร deploy / `OATSIDE_LOCAL_UPDATE_WITHOUT_UPLOAD.md` / `deploy_oatside_report*.ps1|bat`

## 2026-05-01 (AI workflow — Cursor vs Claude Code + rtk/Graphify/mem)

- เพิ่ม **`ProjectYK_System/AI_CURSOR_CLAUDE_WORKFLOW.md`** (แบ่งงาน, Windows/rtk, Graphify, claude-mem, บล็อก HANDOFF คัดลอกวาง)
- อ้างอิงใน **`AGENTS.md`** (Key files #6) และ **`AGENT_BOOTSTRAP.md`** (อ่านเมื่องานเกี่ยวกับเครื่องมือ AI)
- อัปเดต workflow: ชัดว่า Cursor **ไม่แจ้งออโต้** — บังคับ Agent ให้ใส่หัวข้อ **ท่าประหยัดโทเค็นที่ใช้ในรอบนี้** เมื่อผู้ใช้ขอเขียน prompt สำหรับ Claude Code

## 2026-05-01 (Oatside — เรทเที่ยว 12-15 เม.ย. 2026 = 8000 นอกนั้น 7500)

- `Oatside/build_oatside_reports.py`: `trip_rate_baht` ใช้วันที่ **Dest_In** ช่วง **2026-04-12..15** → **8000** บาท · นอกช่วง → **7500** บาท (เดิม 9–11=7500 / อื่น=8000)

## 2026-05-01 (Oatside — billing 50% วันละ 1 เที่ยว + สรุปลูกค้า + overrides JSON)

- `Oatside/build_oatside_reports.py`: ตัด lost-time ตาม wait threshold; เก็บ **50%** เมื่อ matched **1 เที่ยว/วัน/ทะเบียน** (`Dest_In`); โหลด `Oatside/oatside_billing_overrides.json` (`exclude_50` / `include_50`) หรือ `OATSIDE_OVERRIDES_JSON`
- Excel: `Customer_Summary`, `Plate_DestDay`, `Surcharge_50pct_1Trip`; HTML: การ์ดยอดรวมลูกค้า + ตารางรายวัน + หน้า plate แสดงวันไหนโดน +50%

## 2026-05-01 (Oatside — guard ลำดับเวลา + deploy เลือกรายงานล่าสุด)

- `Oatside/build_oatside_reports.py`: `demote_chronology_violations` — ถ้า `Origin_In` เที่ยวถัดไป `< Dest_Out` เที่ยวก่อนหน้า (ทะเบียนเดียวกัน) ให้เที่ยวก่อนหน้าไป Unmatched แล้ววนจนนิ่ง
- `deploy_oatside_report.ps1`: เลือกโฟลเดอร์ `oatside-apr2026` ที่ `index.html` **แก้ล่าสุด** ระหว่าง `Oatside/` / `ProjectYK_System/` / ราก `TransportRateCalculator/` ก่อน copy + commit/push

## 2026-05-01 (Oatside — rebuild ด้วย export GPS 01.05.2026 21:33)

- รัน `Oatside/build_oatside_reports.py` ด้วย `OATSIDE_ORIGIN` / `OATSIDE_DEST` ชี้ไฟล์ `...21-33-31 Oatside.xlsx` + `...21-33-53 P&G.xlsx` → อัปเดต `Oatside/Oatside_PG_Trip_Summary_By_Site.xlsx` และ HTML ใต้ `Oatside/TransportRateCalculator/reports/oatside-apr2026` (Trips 88 / Unmatched 32)

## 2026-05-01 (Oatside GPS รายงาน — merge ต้นทางซ้อนก่อนปลายทาง)

- `Oatside/build_oatside_reports.py`: หลัง greedy จับคู่ เรียงตาม `Origin_Out` แล้วรวมหลายช่วงต้นทางเมื่อ `Origin_In` ถัดไป `< Dest_In` ปัจจุบัน; เลือกปลายทางรอบแรกด้วย `row_no` ตรงช่วงต้นทางล่าสุด รอบถัดไปเกาะ `d_acc` ถ้ายัง feasible; คำนวณ `origin_wait_h` เป็นผลรวมรายช่วง; orphan dest rematch กับต้นทางค้าง

## 2026-04-30 (TransportRateCalculator — ย้ายเข้า `ProjectYK_System/`)

- ย้าย **`TransportRateCalculator/`** → **`ProjectYK_System/TransportRateCalculator/`** (เครื่องคิดเรท + `docs/` สเปก + `reports/`)
- แก้ **`deploy_one_click.bat`** (`REPO_PATH=..\..`), **`deploy.ps1`** default repo path, **`tools/build_petty_cash_online.py`** (`ROOT_DIR` = parents[3], `OUTPUT_DIR` ใต้ TRC)
- แก้ **`deploy_oatside_report*.ps1|bat`** ให้ชี้ `ProjectYK_System\TransportRateCalculator\reports\oatside-apr2026`
- อัปเดต **`.cursor/rules/project-yk-context.mdc`**, **`AGENTS.md`**, **`MODULE_REGISTRY.md`**, **`.cursorignore`**

## 2026-04-30 (ข้อมูลธุรกิจ — รวมที่ `data/`)

- ย้าย **`Salary/`**, **`Fuel/`**, **`Billing/`** จากราก repo → **`data/Salary`**, **`data/Fuel`**, **`data/Billing`**
- **`.gitignore`**: ใช้บรรทัดเดียว **`data/`** แทนการ ignore แยก `Salary/` + `Fuel/`
- อัปเดต `_repo_paths.py` (`SALARY_DIR` / `FUEL_DIR` / `BILLING_DIR`), import scripts, `payroll_slip.salary_export_root()`, `ProjectYK_System/TransportRateCalculator/tools/build_petty_cash_online.py`, `dev_scripts/_paths.py`
- เพิ่มคำอธิบายโครงสร้าง: `data/README.md`

## 2026-04-30 (โครงสร้าง — รวมสคริปต์ระบบไว้ใต้ `ProjectYK_System/`)

- ย้าย `tools/` → `ProjectYK_System/tools/` + `_repo_paths.py` (ชี้ `REPO_ROOT` / `APP_DIR` / `SYSTEM_DIR`)
- สคริปต์ทดสอบราก `_*.py` → `ProjectYK_System/dev_scripts/` + `_paths.py`
- คำสั่ง import: รันจากราก repo เป็น `python ProjectYK_System/tools/import_daily.py` (ดู `AGENT_BOOTSTRAP.md`, `ProjectYK_System/tools/phase2_import.bat`)
- เพิ่ม `.cursorignore` ที่ราก repo เพื่อลดไฟล์ที่ Cursor index (ประหยัด token / โฟกัส)

## 2026-04-29 (Petty cash เม.ย. 2569 — `rev.1` ชีท APR 26)

- **DB**: backup → ลบเฉพาะ `book2_2026` + `pay_cycle_tag=2026-04` → import `ProjectYK_System/tools/import_petty_cash.py` จาก `petty_cash_all_sites_2026-04 rev.1.xlsx` (`--sheet APR 26`) เพื่อไม่ซ้ำเดือนอื่นและไม่ wipe หลายเดือน

## 2026-04-29 (Transport Rate Calculator — ดึงราคาย้อนหลัง + คลุมช่วงหาเฉลี่ย)

- **`TransportRateCalculator/transport_rate_calculator.html`**: Step 1 เพิ่ม historical panel ดึงข้อมูลรายวันจากเว็บ (Bangchak via proxy read), เลือกชนิดน้ำมัน/ปี และคลุมช่วงด้วยเมาส์เพื่อคำนวณค่าเฉลี่ย/ต่ำสุด/สูงสุด/จำนวนวัน
- เพิ่มปุ่มใช้ค่าเฉลี่ยที่คลุมเพื่อเติม `fuelPrice` อัตโนมัติ (workflow แบบ Excel selection)
- เพิ่ม fallback textarea ให้ paste ข้อมูลจากเว็บแล้ว parse เป็นตารางย้อนหลังได้ กรณี fetch อัตโนมัติไม่ผ่าน (CORS/network policy)
- parser รองรับข้อความแบบ tab-separated ที่ copy ตรงจากเว็บ (หลายคอลัมน์ราคา) และเลือกคอลัมน์ตามชนิดน้ำมันที่ user เลือก
- เพิ่ม normalization รายวัน: เติมวันที่ที่หายด้วยราคาวันก่อนหน้า (carry-forward) และติดป้าย `เติมวันหาย` ในตาราง
- เพิ่มตัวเลือกช่วงวันที่ `ตั้งแต่-ถึง` เพื่อ select แถวและเฉลี่ยอัตโนมัติ โดยใช้ workflow เดียวกับการคลุมเมาส์
- ปรับปี/วันที่ใน historical panel เป็นค.ศ.ทั้งหมด (input/filter/display) พร้อมรองรับ parse ข้อมูลต้นทางที่ยังเป็นพ.ศ.

## 2026-04-29 (Petty cash มี.ค. 2569 — MAR 26 เป็นหลัก)

- **DB**: ลบซ้ำรอบ `2026-03` ทั้ง `book2_2026` และ `import_petty_mar26` → import `rev.1.xlsx` ชีท **`MAR 26`** เท่านั้นเป็น bulk หลัก (`book2_2026`)

## 2026-05-02 (Payroll + Petty — unlinked ที่ `site_code` ว่างไม่ถูกนับใน guardrail)

- **ปัญหา**: แถวหักสดย่อย pending + ยังไม่ผูกคนขับแต่ `site_code` ว่าง → แบนเนอร์ payroll / finalize gate เดิมมองไม่เห็น (กรองแค่ไซต์รอบ)
- **แก้**: `main.py` — `_petty_unlinked_predicates_for_payrun` + stale petty scan; `payroll_detail.html` — ลิงก์สดย่อยใช้ `cycle=`; `payroll.py` + `payroll_slip.py` — รวม `site_code` ว่างเมื่อคิดยอด/สลิป (กันหลุมเมื่อผูก driver แล้วแต่ไซต์ว่าง)

## 2026-04-29 (Dev server LAN — bind `0.0.0.0` + `YK_BIND_HOST`)

- **`main.py`**: uvicorn default `host=0.0.0.0` เพื่อให้เครื่องอื่นใน LAN เข้าได้ · env `YK_BIND_HOST=127.0.0.1` ถ้าต้องการ localhost เท่านั้น · พิมพ์ลิงก์ `http://<LAN-IP>:port/daily`

## 2026-04-29 (Petty driver-link: BIG-C strip bug + GLOBAL alias สมพร)

- **`alias_map`**: GLOBAL alias `สมพร โม่งปราณีต` / typo `โม่งปรำณีต` → `สมพร BIG-C`
- **`tools/import_petty_cash.link_drivers_safe`**: ถ้าคัดจากชื่อหลัง strip site hint แล้วว่าง → ไม่ทับผลจับคู่จาก canonical key · `canonical_person_name(..., row_site)`

## 2026-04-29 (Payroll PDF — BIGC เดือนจ่าย vs งวดวิ่ง + seed เลขบัญชี + สลิปแนวนอนหนึ่งหน้า)

- **`salary_folder_month_tag` / `cycle_tag_th_label`**: BIGC เก็บไฟล์ที่ `Salary/BIGC/{YYYY-MM เดือนจ่าย}/Driver/` (งวดวิ่งมีนาคม → เดือนจ่ายเมษายน)
- **`merged_bank_terms` + `services/bigc_bank_seed.py`**: เติมธนาคาร/เลขบัญชีเมื่อยังไม่กรอกใน `custom_terms` — sync ตารางผู้ใช้ (กสิกร/SCB/กรุงไทย/กรุงศรี + `#N/A` บุญชอบ พูลสวัสดิ์)
- **`payroll_export_pdf.py`**: ตารางสรุป/โอนปรับโทนหัวตาราง + แถวสลับสี · สลิปรายคน landscape ซ้ายรายเที่ยวขวาสรุปเงิน · manifest เพิ่ม `folder_month_tag`

## 2026-04-29 (PDF bundle: สลิปทุกคน + สรุปรวม + โอนเงินบัญชี → Salary/…/Driver/)

- **deps**: `requirements.txt` เพิ่ม `fpdf2>=2.7,<3`
- **`services/payroll_slip.py`**: `build_payroll_slip_context()` — context เดียวกันสำหรับ HTML slip + PDF · `salary_export_root` / `export_driver_folder` → `Salary/{SITE}/{YYYY-MM}/Driver`
- **`services/payroll_export_pdf.py`**: `export_payroll_pdf_bundle()` สร้างด้วยฟอนต์ Windows Tahoma/Sarabun:
  - `{SITE}_{tag}_สรุปรวม.pdf` — landscape ตารางสรุป (เรียงชื่อ): ค่าเที่ยว / เงินเดือน / ค่าเรทน้ำมัน / รวมรายได้ / SS / ภาษี / หักสดย่อย / สุทธิ + แถวรวม
  - `{SITE}_{tag}_โอนเงินบัญชี.pdf` — ลำดับ / ชื่อ / ธนาคาร / เลขบัญชี / จำนวนโอน (`Employee.custom_terms`: `bank_name`, `bank_account`, `payment_note` — ว่างแสดง "กดเงินสด")
  - `{SITE}_{tag}_ชุดครบ_สรุปโอนสลิป.pdf` — รวมสรุป + โอน + สลิปแต่ละคนตามชื่อ (หนึ่งคนตามหลายหน้าถ้ายาว)
  - `รายคน/{ชื่อ}_{tag}.pdf` — แจกไลน์รายคน
- **`POST /payroll/{id}/export-pdfs`** → หน้า `payroll_export_done.html` แสดง path เต็ม
- **`payroll_detail.html`**: ปุ่ม **📄 ส่งออก PDF** (ใช้ได้แม้ปิดรอบแล้ว)
- **`employee_form.html`**: helper JSON `bank_name` / `bank_account` / `payment_note`

## 2026-04-29 (สลิปคนขับแบบมินิมอล — print-only view)

- **เคส**: หน้า `/payroll/{run}/employee/{id}` มีข้อมูล admin (UI controls, เตือน, override, etc.) เยอะ ไม่เหมาะปริ้นให้คนขับ
- **Reference**: ใช้ format จาก PDF เดิม `Salary/2026/3.Mar/BigC/คนขับ/เกรียงไกร.pdf` เป็นต้นแบบ
- **ใหม่** `templates/payroll_slip.html`: หน้าแยก minimal — ไม่ extend `base.html` (ไม่มี navbar)
  - Header: บริษัท + ช่วงงวด + รอบ
  - คนขับ + รหัส + ทะเบียนรถ (ดึงจาก `DailyJob.plate_no_raw` distinct)
  - ตาราง DailyJob: วันที่ / ทะเบียน / ส่งสินค้า+หมายเหตุ / ใบงาน / น้ำมัน(L) / ค่าเที่ยว / เรท — รวม placeholder rows ("ส่งงานต่อเนื่อง", "รองาน", note ของ admin)
  - Panel ซ้าย "การใช้รถ/น้ำมัน": ไมล์เริ่มต้น (min `mile_snapshot`) → ไมล์สิ้นสุด (max) → กม.วิ่ง → น้ำมันใช้ (FuelTxn liter หรือ DailyJob.fuel_liter) → เรทเฉลี่ย km/L → วันทำงาน/ลา/ขาด
  - Panel ขวา 2 ก้อน: **รายได้** (เฉพาะที่ ≠ 0: เงินเดือน, ค่าดูแลรถ, ค่าเที่ยว, ค่าเรทน้ำมัน, ส่วนแบ่งน้ำมัน, ชดเชยการันตี, รายได้อื่น) + **เงินหัก** (ประกันสังคม, ภาษี, เงินประกันผ่อน, ผ่อนอุบัติเหตุ, สดย่อย-แต่ละรายการพร้อมวันที่+memo, ค่าน้ำมันออกเอง, หักอื่น)
  - กล่องยอดสุทธิด้านล่าง สี emerald ถ้าบวก / rose ถ้าลบ
- `@media print { @page A4 portrait; toolbar hidden }` → ปริ้นได้สวยทันที
- **Route ใหม่** `GET /payroll/{run}/employee/{id}/slip` → ดึง DailyJob/PettyCash/FuelTxn + คำนวณไมล์/น้ำมัน → render template
- ปุ่ม "🖨 พิมพ์สลิป" ในหน้า detail เปลี่ยนจาก `window.print()` → ลิงก์เปิด tab ใหม่

## 2026-04-29 (Implicit absent: ไม่มี DailyJob ในวันนั้น = ขาดงาน)

- **เคส**: พรศักดิ์ทำงาน 1-25 มี.ค. แล้วเกิดอุบัติเหตุ 25/3 ไม่ได้ทำงาน 26-31 → admin ไม่ได้ใส่ end_date หรือ status='absent' → ระบบเดิมจ่ายเต็มเดือน 9,000 ฿
- **User policy**: "ชื่อใครถ้าไม่มีณ วันที่นั้นๆ หักออกเลย" — ทุกวันที่ไม่มี DailyJob = absent (ขาดงานเงียบ)
- **Refactor** `services/payroll.py`:
  - แยก `_resolve_effective_window(session, emp_id, start, end)` เป็น helper เดียว — ใช้ใน `_count_work_days` และ `calc_one_employee` (DRY)
  - เพิ่ม implicit absent calc: `implicit_absent_days = emp_window_days - len(by_date)` → รวมเข้า `days_absent`
  - **Guard สำคัญ**: ทำเฉพาะเมื่อ `by_date` ไม่ว่าง (มี DailyJob อย่างน้อย 1 วัน) → ป้องกันลงโทษ office_monthly staff ที่ไม่ใช้ DailyJob เลย (admin คน, ช่าง, ยาม, รปภ.)
- **ผล** BIGC `2026-03`:
  - พรศักดิ์ base 9,000 → **7,258.06** ฿ (= 9,000 × 25/31), ss 450 → 363
  - คนอื่นทำงานครบเดือน — ไม่กระทบ
  - Net total: 102,415.34 → 100,760.40 ฿
- **AYU office staff** ยังคงได้ base/ss เต็ม เพราะไม่มี DailyJob ทั้ง period → guard skip implicit absent ตามเจตนา

## 2026-04-29 (SS รายงานเป็นจำนวนเต็มบาทและปัดขึ้นเสมอ)

- ตามมาตรฐาน Thai SSO: ค่า contribution รายงานเป็นเลขเต็มบาทและปัดขึ้น (ceiling) เสมอ
- **Fix** `services/payroll.py`: เปลี่ยน `round(amount, 2)` → `math.ceil(amount)` สำหรับ `social_security`
- **ผล**: 82.50 → 83 (ขั้นต่ำ), 406.45 → 407, 435.48 → 436, 450.00 → 450 (เท่าเดิม)
- กระทบเล็กน้อย (รวมไม่กี่บาท): BIGC ss 3,213.38 → 3,216.00 / LCB ss 8,246.80 → 8,249.00 / AYU ไม่เปลี่ยน (ทุกคน 450 เท่ากัน)

## 2026-04-29 (Resignation trim: ใช้วันทำงานสุดท้ายแทน end_date paperwork)

- **บั๊ก**: สมพร BIG-C ลาออก 4/3 (`end_date=2026-03-04`) แต่ DailyJob มีแค่ 1, 2, 3 มี.ค. (วันที่ 4 ไม่ได้ทำงาน — น่าจะเป็นวันมาเซ็นเอกสาร) → ระบบนับ employed=4 → base = 9000 × 4/31 = 1,161.29 ฿
- **User เจตนา**: prorate ตามวันที่ทำงานจริง → 9000 × 3/31 = 870.97 ฿
- **Fix** `services/payroll.py` `calc_one_employee`: เพิ่ม "resignation trim" — ถ้า `employee.end_date` ถูกตั้ง ระบบจะ trim `eff_emp_end` ลงเป็น `last DailyJob.work_date` ภายใน period (เฉพาะกรณีที่ last_work < eff_emp_end). คนที่ไม่มี `end_date` (กำลังทำงาน) ไม่กระทบ
- **ผล** BIGC `2026-03`:
  - สมพร base 1,161.29 → **870.97** ✓
  - บุญชอบ ไม่กระทบ (ทำงานครบถึง 31/3 ใน period นี้)
  - Net total: 102,708.28 → 102,417.96 ฿

## 2026-04-29 (SS calc: prorate-then-clamp + start_date fallback)

- **บั๊กที่ user เจอ**: สมพร BIG-C ทำงาน 3/4 วัน (ลาออก 4/3) — ระบบโชว์ SS = 58.06 ฿ (ไม่ใช่ขั้นต่ำ 83 ฿ ตามกฎหมาย)
- **Root cause**: ลำดับคำนวณเดิมคือ `clamp(base, min, max) → ss_full → ss_full × work_factor` ทำให้ work_factor < 1 ดึง SS ลงต่ำกว่าขั้นต่ำได้
- **Fix** `services/payroll.py`: เปลี่ยนเป็น `prorated_base = base × work_factor → max(min_base, min(prorated_base, max_base)) → ss = capped × rate` → คนที่ทำงานอย่างน้อย 1 วันในรอบจะได้ SS ขั้นต่ำ 5% × 1,650 ≈ 82.50 ฿ เสมอ. คนที่ไม่ได้ทำงานเลย (factor=0) ยังคงได้ SS = 0
- **Fix start_date fallback**: บุญชอบเพิ่งเข้ามา 29/3/26 admin ยังไม่ใส่ "เริ่มทำงาน" ใน column G → start_date=None → ระบบนับ employment เต็มเดือน → SS เต็ม 450. เพิ่ม fallback ใน `calc_one_employee`: ถ้า `employee.start_date is None` → infer จาก `min(DailyJob.work_date)` ภายใน period (เฉพาะกรณีที่ first_work > period_start)
- **ผล** BIGC `2026-03`: สมพร 82.50 ✓, บุญชอบ 82.50 ✓, SS total ลดจาก 3,580.88 → 3,213.38 ฿
- **Note**: คนที่ลาออกกลางเดือน + ไม่ได้ทำงานเลย จะไม่มี SS — ตรงตามเจตนา (ต้องมีงานอย่างน้อย 1 วันในรอบจึงโดน clamp ขั้นต่ำ)

## 2026-04-28 (Manual day overrides + SS settings + imputed SS base for mao drivers)

- **PayRunAdjust** (ขยาย): เพิ่ม `days_worked_override`, `days_leave_override`, `days_absent_override`, `ss_rate_override`, `ss_base_min_override`, `ss_base_max_override`, `note` (per-employee overrides)
- **PayRun** (ขยาย): เพิ่ม `ss_rate`, `ss_base_min`, `ss_base_max` — ตั้งระดับ "ทั้งรอบ" สำหรับเดือนที่รัฐประกาศลด SS rate ชั่วคราว
- **payroll.py SS calc**: 4-tier resolution priority — PayRunAdjust → PayRun → Employee → defaults (5% / 1,650 / 15,000). Apply Thai legal min/max bounds. Imputed `social_security_base = 9,000` สำหรับ mao/trip drivers ที่ไม่มี base salary จริง (ตามข้อตกลง user "ฐานเงินเดือนแฝง"). หักลด SS proportional ตาม leave/absent/not-employed
- **payroll.py days override**: ค่าใน PayRunAdjust ทับค่า auto จาก _count_work_days สำหรับ days_worked/leave/absent → admin แก้ manual ได้เมื่อ data ผิด
- **UI** `payroll_employee_detail.html`: เพิ่มปุ่ม "แก้ Manual" เปิด panel กรอก override (วันทำงาน/ลา/ขาด + SS rate/min/max + note) มีปุ่ม "ล้าง (กลับ auto)" ด้วย ✎ icon ระบุค่าที่ overrideไว้
- **UI** `payroll_detail.html`: บรรทัดบนสุดแสดง SS rate/min/max ของรอบ + ปุ่ม [ตั้งค่า] เปิด panel ที่ใช้ POST `/payroll/{id}/ss-settings`
- **Endpoints ใหม่**:
  - `POST /payroll/{run_id}/employee/{emp_id}/override` — บันทึก/ล้าง PayRunAdjust + auto recompute
  - `POST /payroll/{run_id}/ss-settings` — บันทึก/ล้าง PayRun-level SS overrides + auto recompute
- ทดสอบ: AYU `2026-03` mao/trip/self_fuel drivers SS = 450.00 (5% × 9000 imputed) ✓ — เคยเป็น 0 เพราะไม่มี base salary

## 2026-04-28 (Rehire/Resign: employment-window aware payroll + UI quick action)

- เคสที่ user เจอ: ณัชพน บรรทัดแรกของวันที่ `1/3` มี note ว่า `เริ่มทำงาน07/02/25 ออก24/2/26 กลับมา 3/3` → ระบบไม่ได้ตีความ "กลับมา" เป็น rehire → start_date ยังเป็น 2025-02-07 → คำนวณ payroll ผิด
- **Schema (no breaking)**: ใช้ `Employee.start_date` เป็น "วันเริ่มของ employment ปัจจุบัน". เก็บ history ใน `Employee.custom_terms` JSON: `{"original_hire_date": "...", "rehire_log": [{"left": "...", "back": "..."}]}`
- **payroll** `services/payroll.py`:
  - `_count_work_days`: filter `DailyJob.work_date` ภายใน employment window (`max(period_start, emp.start_date)` ถึง `min(period_end, emp.end_date)`) → row ก่อน rehire/หลัง resign จะไม่ถูกนับ
  - `calc_one_employee`: เพิ่ม `not_employed_days = period_days - employed_days_in_period` รวมเข้าใน `missed` ของ base/care/SS → คนที่กลับมาวันที่ 3/3 ของเดือน 31 วัน → ได้ `base × (29-leave-absent)/31`
- **import_daily** `_apply_employee_dates`: ปรับให้ rehire (มี "กลับมา DD/MM") override → `start_date = return_date`, clear `end_date`, `status='active'`, append rehire log + เก็บ `original_hire_date`
- **UI** `employee_form.html`: เพิ่มกล่อง "⟲ บันทึกการลาออก/กลับมา" — แสดง original_hire_date + rehire_log, มีฟอร์ม quick action "ออก / กลับมา" → POST `/employees/{id}/rehire` (auto update + log)
- **Quick fix ณัชพน**: `tools/fix_natchapon_rehire.py` → start_date=2026-03-03, original_hire_date=2025-02-07
- ผลลัพธ์ BIGC `2026-03`: ณัชพน work=28 leave=1 base=8,129.03 (ก่อนหน้า 9,000) net=21,501.58. สมพร end=2026-03-04 work=3 base=1,161.29 (4/31 ของ 9,000) ✓
- Net total BIGC `2026-03`: 113,494.25 (ก่อนหน้า 121,463.61 — ลดลงเพราะ prorate ตาม employment window จริง)

## 2026-04-28 (Fix leave false-positives: substring "ลา" inside place names)

- **Root cause**: `_classify_status` ใน `tools/import_daily.py` และ `_count_work_days` ใน `services/payroll.py` ใช้ substring match (`"ลา" in joined`) → match ภายใน "ลาดพร้าว", "ลาดกระบัง", "ตลาดบุญเจริญ", "โนนศิลา" → ตั้ง `status_code='leave'` ผิด **118 แถว** (BIGC 2, AYU 25, LCB 91)
- เคสที่ user เจอ: เกศศักดิ์ 13/3 ไป Phangkhon (remark="โนนศิลา") เป็นเที่ยวจริง (rev 15,311.34, fee 1,400) → ระบบขึ้นเป็นลา
- **Fix 1** `services/payroll.py`:
  - **Money guard**: ถ้าวันใดมี trip ที่ `revenue_customer>0` หรือ `trip_fee_driver>0` → ห้าม classify เป็น leave/absent
  - **Token-based match**: split blob ด้วย `[\s/,;()\[\]\-_.]+` แล้ว exact-match keyword (ไม่ใช่ substring)
  - **ตัด `destination` ออกจาก scan ทั่วไป** (เป็นชื่อสถานที่ ไม่ใช่ status field) ยกเว้น `เข้าบ้าน` ที่เป็น status marker จริง
- **Fix 2** `tools/import_daily.py`: เปลี่ยน `_classify_status` เป็น token-based match เช่นเดียวกัน (ป้องกันการ import ครั้งหน้า)
- **Patch existing data**: `tools/fix_leave_falsepos.py` → clear `status_code`/`leave_status` 118 แถวที่ติด leave ผิดทั้งที่มี revenue/fee จริง
- Recompute: BIGC `2026-03` net=121,463.61, AYU `2026-03` net=368,750.13, LCB `2026-03` net=459,727.56
- เกศศักดิ์ work=31 leave=0 ✓, เกรียงไกร work=28 leave=3 (เข้าบ้าน) ✓

## 2026-04-28 (Petty cash redo: re-import MAR 26 + dedup 2 passes)

- **Pass 1 (MAR 26)**: ลบ `source='import_petty_mar26'` (740 rows) แล้ว re-import ชีท `MAR 26` ของ `petty_cash_all_sites_2026-04.xlsx` ด้วย logic ใหม่ → ทุก 740 rows tag `pay_cycle_tag=2026-03` ครบ (สมประสงค์ 26/2 + คนอื่นที่ตั้งใจหักรอบ มี.ค.)
- **Pass 1 dedup**: รัน fuzzy match (date + canonical name + amount + direction) → mark 102 rows จาก `book2_2026/import` เป็น `settled_offline` กันซ้ำ
- **Pass 2 (legacy)**: dedup `src='import'` ที่มาจาก master file ซ้ำ 3 ไซต์ → 391 affected groups, 778 rows mark `settled_offline` (memo prefix 25 chars เพื่อกัน false positive)
- หลัง dedup: BIGC dup_groups เหลือ 12 (ทั้งหมดเป็น false positive — ค่าปรับคนละสถานที่/คนละใบ ที่ amount เท่ากัน) — ปล่อยให้ user review เอง
- Recompute: BIGC `2026-03` net=120,853.28 (petty_ded 70,025.91), AYU `2026-03` net=368,266.43, BIGC `2026-02` net=119,341.78, AYU `2026-02` net=390,602.74
- Backup: `app.db.bak_petty_redo_20260428_231314`
- Tooling ใหม่: `tools/dedup_petty_mar26.py`, `tools/dedup_legacy_import.py` (idempotent, dry-run by default)

## 2026-04-28 (Petty cash cycle UX: filter + sheet auto-tag + bulk shift)

- เพิ่ม filter "รอบจ่าย" (`pay_cycle_tag`) ในหน้า `/petty-cash` (dropdown รวม count) — ใช้แทนการ filter ตามวันที่ เวลาที่ admin จะดูยอดของรอบ
- ปรับ `tools/import_petty_cash.py` ให้ default `pay_cycle_tag` ตามชื่อ sheet (`MAR 26 → 2026-03`, `มี.ค. 26 → 2026-03`, `MAR 2569 → 2026-03`) ทำให้รายการในชีท `MAR 26` ถึงจะเขียนวันที่ `26/2` ก็จะถูกหักรอบ มี.ค. ตามเจตนา admin (fallback per-site rule ถ้า sheet name parse ไม่ได้)
- เพิ่ม endpoint `/petty-cash/bulk-shift-cycle` + UI checkbox bulk-bar (ย้าย cycle ปลายทาง / ±1 เดือน) บน `petty_list.html` กรณีต้องโยกหลายแถวพร้อมกัน
- แก้เคส `เกรียงไกร 26/2 = 1,000` ที่อยู่ในชีท `MAR 26` ให้ tag `2026-03` พร้อม mark book2_2026 row เป็น `settled_offline` กันซ้ำ → BIGC `2026-03` หักสดย่อยเกรียงไกรรวม `11,000`

## 2026-04-27 (Reclassify Samai toll to AYU)

- ย้าย `PettyCashTxn` หมวด toll ของ `สมัย` ที่ติดไซต์ BIGC ผิด (source `book2_2026`, cycle `2026-03`) ไป `site_code=AYU`
- recompute BIGC `2026-03` ทำให้ยอดหักของ BIGC ลดลง 50 บาทตามข้อเท็จจริง

## 2026-04-28 (Transport Rate Calculator: add fixed-THB per range mode)

- หน้า `TransportRateCalculator/transport_rate_calculator.html` เพิ่มโหมดปรับราคาแบบ `บาท/ช่วง` ควบคู่โหมดเปอร์เซ็นต์เดิม
- อัปเดตสูตรคำนวณ, ตาราง preview/result และ Export Excel ให้รองรับทั้ง `%` และ `บาท/ช่วง` อย่างสอดคล้อง

## 2026-04-28 (Transport Rate Calculator: switch Step 1 to historical diesel-S workflow)

- เปลี่ยน Step 1 เป็นมุมมองราคาน้ำมันย้อนหลัง (Bangchak historical page)
- ปรับข้อความ UI ให้โฟกัสเฉพาะการดูและกรอก `ไฮดีเซล S` เพื่อลดความสับสนจากชนิดน้ำมันอื่น

## 2026-04-28 (Transport Rate Calculator: rollback historical iframe on Step 1)

- rollback Step 1 กลับ iframe ราคาน้ำมันปัจจุบัน เพราะหน้า historical ของ Bangchak บล็อกการฝัง (`refused to connect`)
- คงลิงก์ไปหน้า historical สำหรับเปิดแท็บใหม่แทนการ embed

## 2026-04-27 (BIGC petty deduction source-overlap dedup)

- ตรวจพบ deduction ซ้ำใน BIGC รอบ `2026-03` ระหว่าง `book2_2026` กับ `import_petty_mar26`
- ใช้ source priority: คง `import_petty_mar26` เป็น pending หลัก และ mark แถวซ้ำจาก `book2_2026` เป็น `settled_offline`
- หลัง dedup แล้ว pending duplicate groups = 0

## 2026-04-27 (BIGC duplicate-trip cleanup in fuel importer)

- `tools/import_bigc_fuel_rate.py` เพิ่ม idempotent cleanup:
  - purge `DailyJob source=bigc_fuel_rate` ของเดือนนั้นก่อน import
  - post-import dedup merge: ถ้าพบคู่ `import_daily + bigc_fuel_rate` key เดียวกัน ให้ merge ค่าใช้งานแล้วลบแถว `bigc_fuel_rate`
- ผลลัพธ์: duplicate trips ตาม key `(date,driver,plate,destination)` ใน BIGC มี.ค. ลดเหลือ 0

## 2026-04-27 (Payroll cross-site isolation fix)

- แก้ `services/payroll.py` ให้ aggregate ทุกส่วนกรอง `site_code` (ไม่ใช่แค่ driver_id+date)
- แก้ `/payroll/{run_id}/employee/{emp_id}` ให้ query `DailyJob/PettyCashTxn/FuelTxn` เฉพาะไซต์ของรอบ
- ปิดช่องโหว่คนขับชื่อเดียวกัน/driver_id เดียวกันที่มีประวัติข้ามไซต์แล้วถูกนับปนในรอบปัจจุบัน

## 2026-04-27 (Alias map centralization + finalize gate)

- เพิ่ม `app/services/alias_map.py` เป็น source เดียวสำหรับ normalize site/person aliases
- ผูก alias map เข้า `tools/import_daily.py`, `tools/import_petty_cash.py`, `tools/import_bigc_fuel_rate.py`
- เพิ่ม finalization guard ใน `/payroll/{run_id}/finalize`: ถ้ายังมี pending deductions ที่ unlinked ในไซต์เดียวกัน -> block finalize
- เพิ่ม filter `unlinked=1` ใน `/petty-cash` และแสดง badge `unlinked` ในตาราง

## 2026-04-27 (AI workflow default - OA careful mode)

- เพิ่ม rule ใหม่ `.cursor/rules/oa-careful-default.mdc` (`alwaysApply: true`)
- บังคับแนวตอบแบบรอบคอบทุกแชทในโปรเจกต์: completeness/leak check, ไม่เดาสุ่มเมื่อข้อมูลกำกวม, สรุปสิ่งที่ทำแล้ว/ค้าง/ความเสี่ยง/ขั้นถัดไป

## 2026-04-27 (Payroll guardrail - unlinked driver deductions)

- `/payroll/{run_id}` แสดง banner เตือนเมื่อมี `PettyCashTxn` หักคนขับที่ยัง `driver_id is null` ในรอบ/ไซต์เดียวกัน
- แสดงจำนวนรายการ + ยอดเงินรวมที่ยังไม่ถูกคิด payroll และลิงก์ลัดไป `/petty-cash?...&unlinked=1`
- `/petty-cash` เพิ่ม filter `unlinked=1` + badge `unlinked` ในตารางรายการ

## 2026-04-27 (BIGC column-G employment event parsing)

- `tools/import_daily.py` (BIGC): parse ข้อความคอลัมน์ G (`เริ่มทำงาน`, `ออก/ลาออก`, `กลับมา`) เพื่ออัปเดต `Employee.start_date/end_date/status`
- รองรับแถวแจ้งสถานะที่ไม่มีวันที่คอลัมน์ A โดย fallback วันที่จากข้อความใน G
- เพิ่ม fallback name match แบบชื่อแรก เพื่อรองรับ master ที่เก็บชื่อสั้น

## 2026-04-27 (BIGC worked-day semantics aligned to manual)

- `services/payroll.py::_count_work_days()` ปรับนิยาม `worked` เป็น `distinct DailyJob dates - leave - absent`
- `company_no_work` (รองาน/รถจอด) ไม่ถูกนำไปหัก worked อีกต่อไป
- กรณีไม่มี DailyJob ในช่วงเลย (เช่นยังไม่เริ่มงาน/ลาออกแล้ว) ให้ worked=0 ไม่เดาเป็น 31

## 2026-04-27 (BIGC leave deduction fix - Thai status aware)

- `services/payroll.py` ปรับ `_count_work_days()` ให้แปลสถานะวันจากคำไทยในเดลี่จริง (`ลา/ป่วย/ลากิจ/หยุด`, `ขาด`, `รถจอด/รองาน/ไม่มีงาน`) ร่วมกับ `status_code`
- แก้ปัญหา BIGC payroll ที่ก่อนหน้า leave ไม่ถูกนับเพราะโค้ดเดิมรองรับเฉพาะ token อังกฤษ

## 2026-04-27 (PettyCash import MAR 26 + duplicate-name safety)

- `tools/import_petty_cash.py` รองรับ `--file --sheet --source-tag --link-drivers` เพื่อ import เป็นรอบ/ชีทแบบควบคุมได้
- เพิ่ม safe driver-linker จาก `requester_raw` ไป `Employee`: link เฉพาะ match ชัดเจน, skip ชื่อกำกวมข้ามไซต์
- เพิ่ม site hint parser (`BIG C/BIG-C/BIGC`, `อยุธยา/AYU`, `LCB/แหลม`) ป้องกันปนชื่อซ้ำ เช่น `สมัย BIG C` vs `สมัย อยุธยา`
- `services/payroll.py` ปรับ employee selection ให้พิจารณา `start_date/end_date` ซ้อนทับรอบแทนกรอง `status=active` อย่างเดียว รองรับการคำนวณย้อนหลังของพนักงานลาออก

## 2026-04-27 (BIGC fuel residual ติดลบ × 32.15)

- `services/payroll.py`: ถ้า residual น้ำมัน BIGC ติดลบ ให้คูณ `BIGC_FUEL_OVERSPEND_THB_PER_L` (32.15) แทนเรทคืน 16 บาท/ลิตร — ตรงไฟล์เรทแอดมิน
- `tools/import_daily.py`: `--xlsx` / `--sheet`; `--wipe-prior` ร่วม `--site` (+ `--from-date`) ลบเฉพาะไซต์และช่วงวันที่
- `tools/import_bigc_fuel_rate.py`: `--tag YYYY-MM` override รอบ; ชื่อชีท `อาท` → เกรียงไกร สายแก้ว; fallback ชื่อไฟล์ `YYYY-MM`

## 2026-04-27 (BIGC payroll เม.ย. — โครงไฟล์ + 4 แหล่งข้อมูล)

- ข้อมูลรายเดือนอยู่ที่ **`data/Salary/BigC/YYYY-MM/`** (ไม่ใส่ใน `ProjectYK_System/`)
- ไฟล์วางบิลลูกค้าเก็บ **`data/Billing/BigC/YYYY-MM/`** สำหรับตรวจทานอนาคต (Rate WNDC, KM.& Rete_BPD)
- แหล่งที่ 1–3: daily, fuel_rate_daily (ชีทรวมเรท + รายคน), master `fuel_rate.xlsx` (ค่าเที่ยว + เรทน้ำมัน พี่ต้น/มาร์ค)

## 2026-04-25 (KYT Weekly workflow baseline)

- เพิ่มคู่มือมาตรฐาน `ProjectYK_System/docs/KYT_AUTOFILL_GUIDE.md` สำหรับการเติม KYT รายสัปดาห์จากรูปในไฟล์
- ล็อกกติกาใช้งาน: ห้ามเปลี่ยนขนาดแถว/คอลัมน์/เลย์เอาต์ template เดิม, ใส่เฉพาะข้อความลงตำแหน่งเซลล์มาตรฐาน Round 1-4
- ตกลงแนวทางต่อไป: เริ่มจาก `.md` workflow ก่อน แล้วค่อยต่อยอดเป็นหน้า HTML `KYT Assistant` (drag-drop + AI draft + export)
- ส่งมอบ MVP หน้า `/kyt` ใน One Platform: drag-drop รูป, วิเคราะห์ AI (fallback ได้), แก้ Round 1-4, และ export กลับเป็นไฟล์ `.xlsx` template เดิมโดยไม่แตะ row/column sizing
- ปรับ behavior KYT analyze: ถ้าไม่มี Vision จริง (ไม่มี key/ไม่มี local model) ให้คืนค่า **ว่าง** + ข้อความแจ้งไม่สามารถวิเคราะห์ได้ (ไม่ใช้ข้อความเดา)
- เพิ่มทางเลือก Local Vision ผ่าน Ollama (`OLLAMA_VISION_MODEL`, `OLLAMA_BASE_URL`) เพื่อลดค่าใช้จ่าย token cloud
- Hardened local output quality: เพิ่ม validation รูปแบบ KYT (prefix/จำนวนข้อ/ภาษาไทย) ถ้าไม่ผ่านให้คืนค่าว่างพร้อม note ชัดเจน
- เพิ่มความทนทานการเรียก Ollama Vision: ถ้า `/api/generate` 500 เมื่อใช้ `format=json` จะ retry อีกครั้งแบบไม่ใส่ `format` อัตโนมัติ

## 2026-04-25 (KYT rollback by user request)

- ถอดฟีเจอร์ KYT ออกจาก One Platform ตามคำขอผู้ใช้: ลบ route `/kyt*`, ลบเมนู `KYT AI`, และลบ service/template ที่เกี่ยวข้อง
- ลบเอกสาร `ProjectYK_System/docs/KYT_AUTOFILL_GUIDE.md` และสคริปต์ `tools/fill_kyt_weekly.py` ออกจากโปรเจกต์ เพื่อกลับไปใช้ workflow ผ่าน Cursor chat ตามเดิม

## 2026-04-08 (Phase 4 Wave 1 — Driver PWA: Auth + Vehicle Check + Alcohol Test)

- **Schema v14**:
  - `Employee.pin_hash` + `pin_set_at` — ตั้ง PIN 4-6 หลักต่อคนขับ (scrypt+salt)
  - `DriverSession` — cookie-based session token (30 วัน rolling), รองรับหลายอุปกรณ์ต่อคน
  - `DriverSubmission` — ตารางกลางเก็บทุกอย่างที่คนขับส่งจากมือถือ (`vehicle_check`, `alcohol_test`, `job_photo`, `fuel_receipt`, `signature`, `other`)
    - มี `vehicle_id`, `daily_job_id`, `gps_lat/lng/accuracy`, `photo_paths` (หลายรูป), `data_json` (flexible payload)
    - `review_status` + `review_note` สำหรับ admin
- **`services/driver_auth.py`** ใหม่:
  - `hash_pin` / `verify_pin` (stdlib scrypt, ไม่ต้องพึ่ง bcrypt/argon2)
  - In-memory rate limiting (5 ครั้งผิด → ล็อค 10 นาที)
  - `normalize_phone` — รับทุกรูปแบบ `081-234-5678`, `+66 81 234 5678`
  - `create_session` / `revoke_session` / `get_current_driver` (cookie `drv_session`)
  - `save_photo` — เก็บใน `uploads/driver/<emp_id>/<YYYY-MM-DD>/<kind>/<ts>.jpg`
- **Driver PWA pages (mobile-first)** — UI ใหญ่ เลือกได้ง่าย bottom-nav 4 ปุ่ม:
  - `/driver/login` — เบอร์โทร + PIN
  - `/driver` — home: tile ตรวจรถ/เป่าแอลกอฮอล์ (แสดงสถานะวันนี้), งานวันนี้, ส่งล่าสุด
  - `/driver/today` — รายการงานวันนี้ + 7 วันข้างหน้า
  - `/driver/check` — checklist 15 รายการ (ยาง/เบรค/ไฟ/น้ำมัน/เอกสาร…) + ถ่ายรูปหลายใบ + GPS
  - `/driver/alcohol` — ถ่ายรูปเครื่องเป่า + กรอกค่าอ่านได้ + GPS (ค่า > 0 = flagged อัตโนมัติ)
  - `/driver/history` — ประวัติการส่งของตัวเอง + สถานะตรวจ
- **Client-side image compression** — ย่อเป็น 1280px + JPEG 75% ก่อนอัพโหลด (ประหยัด data 4-10 เท่า)
- **Admin pages**:
  - `/admin/drivers/pins` — ตั้ง/เปลี่ยน/ล้าง PIN + เบอร์โทร (เปลี่ยน PIN = revoke sessions เก่าทั้งหมด)
  - `/admin/submissions` — ดูรายการจากคนขับทั้งหมด + filter (driver/kind/review/date) + review (approve/flag/archive) + preview รูป
- **Nav**: เพิ่มลิงก์ `📱 Driver` ในทุกหน้า admin
- **`/uploads` static mount** สำหรับ admin preview รูปภาพ

## 2026-04-08 (Phase 3 — CFO Dashboard + Debt/Loan tracking)

- **Schema v13**: `Loan` + `LoanPayment` tables (`models.py`)
  - รองรับ `term` (ลดต้นลดดอก), `hire_purchase` (งวดคงที่), `revolving` (OD/วงเงินหมุน), `informal` (ยืมส่วนตัว), `factoring`, `other`
  - ทุก Loan มี `code` auto (`L0001`), ผูก `linked_vehicle_id` ได้ (สำหรับไฟแนนซ์รถ)
- **`services/finance.py`** ใหม่: รวมสูตรการเงินทุกอย่างไว้ที่เดียว
  - `amortization_schedule` — คำนวณตารางผ่อนอัตโนมัติ (ลดต้นลดดอก / งวดคงที่ / ดอกเบี้ยอย่างเดียวสำหรับ revolving)
  - `loan_summary` — รวมยอดคงเหลือ + ภาระต่อเดือน + ประมาณดอกเบี้ยปีหน้า
  - `monthly_pnl` — รายรับ (ค่าขนส่ง + fees) − ต้นทุน (fuel + payroll + petty + maint + ดอกเบี้ย)
    - **Petty cash กรองหมวด**: รวมเฉพาะ `toll/parking/loading/fine/accident` เพราะ `fuel/repair/tire` ซ้ำกับ FuelTxn/MaintRecord, `driver_advance/salary_partial` หักผ่าน payroll เอง
    - มี toggle `include_other_petty` เผื่อข้อมูลเก่าที่ยัง `category="other"`
  - `cost_per_vehicle` — รายรับ/น้ำมัน/ซ่อม ต่อคัน + gross margin
  - `cash_flow_projection` — พยากรณ์ 30-180 วัน (AR M+1, หนี้ตามตารางผ่อน, payroll, fuel/petty รายวันเฉลี่ย)
  - `break_even_and_runway` — Contribution margin, break-even trips/เดือน, ค่าใช้จ่ายคงที่, สถานะ healthy/losing
- **หน้าเว็บใหม่ 5 หน้า**:
  - `/finance` — Dashboard หลัก (KPI + P&L + health + trend 6 เดือน + top 15 รถ)
  - `/finance/loans` — รายการหนี้ + สรุปยอดรวม + ภาระ/เดือน
  - `/finance/loans/new` & `/finance/loans/{id}` — ฟอร์มกรอก/แก้ไข + ตารางผ่อนอัตโนมัติ + บันทึกการชำระ
  - `/finance/pnl?year=YYYY` — กำไรขาดทุนรายเดือนทั้งปี (12 เดือน + สรุป)
  - `/finance/vehicles?month=YYYY-MM` — ต้นทุนต่อคันทั้งหมด
  - `/finance/cashflow?days=N` — ประมาณการกระแสเงินสด 30/60/90/120/180 วัน
- **Nav**: เพิ่มลิงก์ `💰 CFO` ในทุกหน้า
- **`.gitignore`** ใหม่: ป้องกันไฟล์ sensitive (Salary/, Fuel/, *.xlsx, *.pdf, app.db, secrets, nested .git, etc.)
- **ข้อมูลหนี้**: ผู้ใช้จะค่อยทยอยกรอกผ่านหน้า `/finance/loans/new` (ไม่บังคับ — ถ้าไม่มีข้อมูลหนี้ dashboard ก็ยังใช้ได้ แต่ break-even จะขาด fixed cost ส่วนดอก)

## 2026-04-08 (Phase 2 — import + provenance + billing export)

- **Schema v12**: `DailyJob.source` — `import_daily` | `manual` | `bigc_fuel_rate` | `""` (legacy)
  - ฟอร์มสร้างงานใหม่ใน UI → `source=manual`
  - `tools/import_daily.py` → `import_daily`; `--wipe-prior` ลบเฉพาะ `import_daily` (+ fees + fuel ผูก job นั้น) ไม่ลบงานคีย์มือ
  - `--mark-legacy-import` ใช้ครั้งเดียวเมื่ออัปเกรดจาก DB เก่า (ทุกแถว `source=""` เป็น import) — **ระวัง** ถ้ามีงาน manual เก่าที่ยัง `""`
- **Default import ย้อนหลัง**: `--from-date` เปลี่ยนเป็น **2018-01-01** ทั้ง `import_daily.py` และ `import_petty_cash.py`
- **`ProjectYK_System/tools/phase2_import.bat`**: รัน import Daily แล้วต่อด้วย Petty (ส่ง args ร่วมได้ เช่น `--wipe-prior`)
- **`import_bigc_fuel_rate.py`**: DailyJob ที่สร้างใหม่จากไฟล์เรท → `source=bigc_fuel_rate`
- **`tools/backfill_links.py`** ใหม่: เติม FK (driver_id/vehicle_id/etc.) ให้ DailyJob/PettyCash/FuelTxn จาก master เดิม — ใช้หลัง wipe+import
- **Billing export (P0-3)**:
  - หน้า `/billing` — กรอง site+เดือน+ลูกค้า, สรุปต่อลูกค้า (นับเที่ยว, ค่าขนส่ง, ค่าอื่น, ภงด.53, สุทธิ)
  - `/billing/export.csv` — ดาวน์โหลด CSV (UTF-8 BOM) ต่อ site/เดือน/ลูกค้า พร้อม extra fees รวมแล้ว
  - แบบฟอร์มใบวางบิลต่อลูกค้า (รูปเล่ม) เลื่อนไปทำเมื่อเก็บ requirements แต่ละเจ้าแล้ว
- **Dependency pin สำคัญ** (`ProjectYK_System/app/requirements.txt`):
  - `starlette>=0.36,<0.40` + `fastapi<0.115` — starlette 1.0 แตก Jinja2 template globals (unhashable type dict)
- **Import จริงใน DB**: DailyJob 1,552 (93% linked driver / 100% vehicle) · PettyCashTxn 50,753 ย้อนถึง 2019-12 (20% linked driver — ส่วนใหญ่เป็นพ่อ/office/คนขับเก่า) · FuelTxn 777
- **Roadmap Driver PWA**: ตรวจรถ + เป่าแอลกอฮอล์ (ถ่ายรูปมือถือ) + หลักฐาน Audit/Safety ลูกค้า (แนว compliance ลูกค้าใหญ่ / DHL-class) — บันทึกใน `AGENTS.md`

## 2026-04-21

- ตั้งศูนย์กลางบริบท AI ที่ `ProjectYK_System/`
- กำหนด bootstrap กลางให้ Agent อ่านจาก:
  - `AGENT_BOOTSTRAP.md`
  - `MODULE_REGISTRY.md`
  - `CHANGELOG_MASTER.md`
- ลงทะเบียนโมดูลหลัก:
  - `AccidentCases`
  - `TransportRateCalculator`
- วางกติกาอัปเดต context สองชั้น:
  - log ของโมดูล
  - changelog กลาง
- เพิ่ม template logo พร้อมใช้ที่:
  - `AccidentCases/_TEMPLATE_CASE/assets/images/yk_logo_mark.svg`
- เพิ่ม automation script สำหรับลงทะเบียนโมดูลใหม่:
  - `ProjectYK_System/bootstrap_module.py`

## 2026-04-22

- เริ่มใช้แนวทาง "Data First, UI Improve Later" สำหรับโมดูลสดย่อยออนไลน์
- เพิ่มเครื่องมือย้ายข้อมูลย้อนหลังจาก Excel ไปออนไลน์:
  - `TransportRateCalculator/tools/build_petty_cash_online.py`
- เพิ่มรายงานออนไลน์เบื้องต้นสำหรับใช้งานจริง:
  - `TransportRateCalculator/reports/petty-cash-online/index.html`
- เพิ่ม output กลางสำหรับต่อ API/DB ได้ทันที:
  - `petty_cash_records.csv`
  - `petty_cash_records.json`
  - `summary.json`
- ขยายการจัดหมวดต้นทุนให้รองรับรายการการเงิน (`finance`) เพื่อคำนวณต้นทุนจริง

- **เลือก Tech Stack สำหรับ One Platform**: FastAPI + SQLite + HTMX + Tailwind (CDN) + `start.bat`
  - เหตุผล: รันบนโน้ตบุ๊กได้ทันที ไม่ต้องติดตั้ง Node/Postgres/Docker เหมาะกับช่วง vibe-test
  - Migration path: ย้ายเป็น PostgreSQL ตอนขึ้น PC Server + Tailscale
- **สร้างโครง Day-1 ของโมดูล Daily** ที่ `ProjectYK_System/app/`
  - `main.py` (FastAPI) + `templates/` (base, daily_list, daily_new) + `start.bat`
  - โมเดล `DailyJob` เริ่มจาก contract ใน `Salary/daily_module/contracts.py`
  - CRUD ขั้นต้น: เพิ่ม/ดู/ลบ + ฟิลเตอร์ตาม site + วันที่
  - ทดสอบ: server ขึ้นได้, `/health` ตอบ `{"ok":true}`, `/daily` ใช้งานได้
- **บันทึกการตัดสินใจจากผู้ใช้**:
  - ผู้ใช้ไม่เขียนโค้ดเอง ทำหน้าที่ vibe-test (รัน, หาบัค, สั่งแก้)
  - ทีม 7 คน (บัญชี 2 / OP 3 / ผู้จัดการ 1 / เจ้าของ 1)
  - เร่งด่วนสุด เพราะเคยเสียเวลาเกือบ 1 ปีกับโปรแกรมเมอร์ภายนอกแล้วไม่ได้ใช้
  - เริ่มไหลจาก Daily → Dispatch → Billing/Accounting (สดย่อย) → Payroll

- **ตั้ง Cursor rule ให้ auto-update context**: `.cursor/rules/project-yk-context.mdc` (alwaysApply=true)
  - ทุก agent ที่เปิดแชทใหม่จะอ่านและอัปเดต CONTEXT_LOG / NEXT_ACTION_PLAN / CHANGELOG อัตโนมัติ
- **ทำ field mapping 3 ไซต์จากตัวอย่างจริง**: `ProjectYK_System/Daily.xlsx` → `docs/IMPORT_MAPPING_SPEC.md`
  - AYU 28 cols (งาน 1 เที่ยว/แถว), BIGC 19 cols (หัวลาก+หาง), LCB 40 cols (ตู้ container ซับซ้อน)
  - พบว่า `DailyJob` ต้องขยาย + แยกตาราง `daily_job_fees`, `fuel_txns`, `trucks`, `trailers`

- **เก็บ domain knowledge payroll/billing เต็มจากผู้ใช้**:
  - `docs/SITE_PAYROLL_RULES.md` — กฎเงินเดือน 3 ไซต์ (BIGC 9000 standard, LCB 2 modes, AYU 2 modes), common deductions (deposit/SSO/accident installments)
  - `docs/BIGC_BRANCH_RATE_SPEC.md` — สูตรค่าขนส่ง 1Big c / 1+ / 2BigC / 2++ / รับรถ / 1DH + ตารางสาขา (รอไฟล์จากผู้ใช้)
  - `docs/WORKFLOW_BY_TEAM.md` — บทบาท 7 คน, vision "Dispatch ต้นน้ำ บัญชีมาหยอดท้าย", cross-site scenario (BIGC → แหลม)
- **ยืนยันรอบจ่ายเงินเดือนต่อไซต์**: AYU 26→25 จ่ายสิ้นเดือน, BIGC 1→สิ้นเดือน จ่ายวันที่ 1, LCB 16→15 จ่ายวันที่ 1

- **Phase 1.1 เสร็จ: Master Data + Expanded Daily**:
  - `app/models.py` รวม 11 ตาราง: `SchemaInfo`, `Employee`, `Vehicle`, `Customer`, `PayCycle`, `DailyJob` (ขยาย 28 ฟิลด์), `DailyJobFee`, `LeaveRecord`, `AccidentCase`, `AccidentInstallment`, `DriverDeposit`, `BigcBranch`
  - Seed `pay_cycles` อัตโนมัติตอน startup (3 ไซต์)
  - UI CRUD: /employees /vehicles /customers + ฟอร์ม Daily ขยาย (dropdown + raw_name fallback + เลือกหาง)
  - Smoke test: สร้างคน 3 คน (BIGC standard / LCB trip / AYU mao+การันตี), รถ 3 คัน (head+tail+truck), ลูกค้า 2 ราย, daily 2 รายการ, แก้ได้ ลบได้ — ผ่านทุกจุด
  - Schema version track ในตาราง `schemainfo` (ปัจจุบัน v2)
- **ยืนยัน design principles รอบนี้จากผู้ใช้**:
  - AYU share rate 55-60% เก็บ**ต่อคน** (flexible) — ไม่ fix
  - LCB "ไม่แบ่ง" items (ค่าเสียเวลา, ค่าค้างคืน) → ใส่ใน `custom_terms` (JSON text) ไม่ hard-code
  - AYU การันตี = เต็มเดือน หักรายวันเมื่อลา
  - Cross-site: ใช้ pay rule ของไซต์**คนขับ** ไม่ใช่ไซต์งาน
  - ช่วงแรกคนกรอกค่าเที่ยวเอง cross-site ได้ (ไม่บังคับสูตร)
  - ทุก user เห็นทุกไซต์ (DB ไม่มีปัญหา Sheet filter ทับกัน)
  - ยังไม่ทำ Line OA — ใช้ copy-paste ไปก่อน

- **2026-04-22 Session 10 — Q&A + 2-Track Plan**:
  - เพิ่ม auto-gen code สำหรับ Employee (E0001) / Customer (C0001) — กรอกเองก็ได้
  - ยืนยัน search ด้วยชื่ออย่างเดียวใช้ได้ (substring, ไม่ต้องมีนามสกุล)
  - helper text: ภงด 53 = 1% ของค่าขนส่ง, ช่องน้ำมันใน daily_form จะย้ายเป็นหน้า /fuel แยก
  - วัน start/end รถตอนนี้เป็นแค่ info — Asset Register (DP/ค่าเสื่อม/มูลค่ารถ) เลื่อนไป Phase 2
  - Billing Profile อ้างอิง = text pointer ไป `CUSTOMER_BILLING_PROFILES.md` (จะเปลี่ยนเป็น FK dropdown ทีหลัง)
  - Raw name ไม่ auto-create master — ใช้ workflow "⚠️ + ปุ่ม promote" แทน
- **แผนใหม่: 2-Track Parallel** (ตามผู้ใช้เสนอ):
  - **Track A (Petty Cash Quick Win)** — `petty_cash_txns` + UI + parser memo ไทย + import Excel สดย่อยเก่า → แอดมินใช้แทน Excel ภายใน 1 สัปดาห์
  - **Track B (Daily Import + Foundation)** — FuelTxn + import scripts (AYU→BIGC→LCB) + promote-to-master UI
- **ลำดับถัดไป**: พรุ่งนี้เริ่ม Track A (Petty Cash) ก่อน

- **2026-04-23 Session 11 — Track A Petty Cash (A1+A2+A5 done)**:
  - schema v3: เพิ่มตาราง `PettyCashTxn` (20+ fields) + 4 enums ใหม่ใน `models.py`
  - `init_db` ใหม่: drop+recreate เมื่อ schema version mismatch (dev mode, สะดวก vibe-test)
  - UI /petty-cash: list + form + edit + delete + filter 6 มิติ + card 3 summary
  - UI /petty-cash/pending: สรุปรอหักเงินต่อคนขับ + แยกเคสไม่มี driver_id
  - auto compute pay_cycle_tag ตามไซต์ (AYU 26→25, BIGC 1→end, LCB 16→15)
  - lock guard: status=locked → แก้/ลบไม่ได้
  - เอกสาร `docs/PETTY_CASH_SPEC.md` mapping Excel เดิม → schema ใหม่
  - smoke test HTTP ผ่านทุก endpoint (health, list, new, edit, pending, filter)
- **ยังเหลือ A3 (parser memo), A4 (import Excel), A6 (payroll lock hook)**

## 2026-04-08 — Maintenance Module Full Scope (rm7 + rm8)

- **Schema v10 เสร็จสมบูรณ์** (Wave 2 + Wave 3 + full maintenance):
  - `Vehicle` + nickname/old_plate_no/brand/model/engine_no/chassis_no/current_mile
  - `PmPlan` + fluid_kind/alert_km_before + next_due_date/next_due_mile auto-compute
  - ตารางใหม่: `VendorPrice`, `VehicleSpec`, `MaintInspection`, `MaintInspectionItem`
  - ENUMs: `FLUID_KINDS`, `INSPECTION_STATUS`, `INSPECTION_ITEM_STATUS`
- **UI ครบชุด** (7 หน้าใหม่):
  - PM list/form + mark_done + auto next-due + dashboard overdue/due_soon
  - Tire list/form + per-vehicle visual layout + event system (mount/rotate/unmount/inspect/retread/scrap)
  - Part detail + VendorPrice CRUD + prefer + auto-learn from stock-in + comparison view
  - MaintInspection list/form + dynamic checklist + auto overall_status
- **Import tools เสร็จ**:
  - `tools/import_fluid_history.py` — `ProjectYK_System/ประวัติเปลี่ยนของเหลว.xlsx`
    - 8 VehicleSpec, 279 PmPlan (น้ำมันเครื่อง/เกียร์/เฟืองท้าย/จารบี/หล่อเย็น), 45 VendorPrice, 39 Part, 12 Vendor, 9 StockTxn opening-balance, 20 historical MaintRecord
    - idempotent (hash-based + unique-key upsert)
  - `tools/import_rm_history.py` — 3 RM History files:
    - `RM History(Wangnoi).xlsx`: 45 Vehicle + 105 MaintRecord (repair log) + 846 StockTxn (Stock อยุธยา)
    - `RM History(LCB).xlsx`: 43 Vehicle + 33 tire StockTxn + 1 part StockTxn
    - `RM History(BigC Thanya).xlsx`: 20 Vehicle (รองรับ layout BigC ที่มีคอลัมน์ จังหวัด คั่นระหว่าง plate/brand)
    - รวมทั้งระบบ: Vehicle 169 (brand-filled 78, old_plate 17), MaintRecord 146, StockTxn 900, Part 660 (tire 30), Vendor 138
    - กันข้อมูลเพี้ยน: strip Excel text-prefix `'` + strip province suffix `อย/ปท/นนท`
- **Dashboard upgrade**: PM widget (overdue/due_soon พร้อมทะเบียน + เหลือกี่วัน/km), recent stock activity (8 รายการล่าสุด), ลิงก์ไปทุก sub-module
- **Smoke test ผ่าน 8 routes**: `/maint`, `/maint/records`, `/maint/pm`, `/maint/tires`, `/maint/parts`, `/maint/vendor-prices`, `/maint/inspections`, `/maint/stock` — 200 OK ทั้งหมด

## 2026-04-08 — Fuel-Adjusted Transport Pricing (schema v11)

- **เพิ่มความสามารถ**: ค่าขนส่ง (revenue_customer) ผันแปรตามราคาน้ำมันรายเดือนได้
- **Design**: Hybrid pricing
  - Track A: ลูกค้าที่คุยรายเดือน ใช้ `RateCard.effective_from/to` (มีอยู่แล้ว) — admin กรอกเรทใหม่แต่ละเดือน
  - Track C: ลูกค้าที่ส่ง fuel surcharge step table ให้ (BigC/LCB) — ใช้ตาราง step table
- **Schema v11** (2 ตารางใหม่):
  - `FuelPriceIndex(month YYYY-MM, region, diesel_price, source, notes)` — อ้างอิงราคาดีเซลต่อเดือน
  - `FuelSurchargeBand(customer_id, trip_type_code, vehicle_kind, fuel_min, fuel_max, surcharge_pct, surcharge_flat, fuel_ref_mode [current/prev1/prev2], region, effective_from/to, priority, status, notes)` — ช่วงราคา → %/บาทบวก
- **Helper (`main.py`)**:
  - `get_fuel_price(month, region)` — lookup ราคาน้ำมัน + fallback region
  - `match_surcharge_band(customer, trip, vehicle, date, diesel_price)` — เลือก band ที่ match best (specific > wildcard, priority สูง > ต่ำ)
  - `compute_effective_rate(base, customer, trip, vehicle, date, region)` → `{base, diesel_price, band_id, pct, flat, effective, explain}`
- **Routes**:
  - `/fuel-index` GET/POST/delete — CRUD ราคาน้ำมันรายเดือน (upsert ถ้า month+region ซ้ำ)
  - `/fuel-surcharge` GET/POST/delete — CRUD Fuel Surcharge Bands ต่อลูกค้า
  - `GET /api/rates/effective?base_rate=X&customer_id=Y&work_date=Z` → preview JSON
- **UI**:
  - `fuel_index_list.html` / `fuel_surcharge_list.html` — table + inline form
  - Daily form (`daily_form.html`): เพิ่ม live preview ข้างช่อง "ค่าขนส่ง" — JS เรียก `/api/rates/effective` แล้วแสดง `⛽ base 1000 × (1 + 2%) = 1020 (น้ำมัน 2026-03=33.50 ฿/L, current)`
  - Nav เพิ่ม link `⛽ Fuel`
- **ตัวอย่าง test ผ่าน**:
  - Mar 2026, น้ำมัน 33.50 ฿/L → band 33.00-34.00 (+2%) → base 1000 → effective **1020**
  - Feb 2026, น้ำมัน 32.00 ฿/L → band 32.00-33.00 (+0%) → base 1000 → effective **1000**
- **URL design note**: ใช้ `/fuel-index` + `/fuel-surcharge` ที่ root (ไม่ใช่ nested `/rates/...`) เพื่อเลี่ยง route-collision กับ `/rates/{card_id:int}` (FastAPI match int จะ error 422 ก่อน)

- **2026-04-27 (BIGC 2026-03 data hygiene):** ทำ surgical reset เฉพาะ BIGC รอบ `2026-03` (backup DB, wipe เฉพาะ source `import_daily`/`bigc_fuel_rate`/`import_petty_mar26`, reimport ใหม่, recompute payroll, preflight duplicate/unlinked = 0)
- **2026-04-27 (Payroll tax withholding):** เพิ่มคำนวณภาษีรายได้แบบขั้นบันไดใน `services/payroll.py` (annualized progressive PIT แล้วหาร 12 ต่อเดือน) และผูกเป็น deduction อัตโนมัติผ่าน `other_deduction` พร้อมรองรับ override รายคนใน `Employee.custom_terms`
- **2026-04-28 (Tax catch-up default + explicit tax field):** ปรับ payroll ให้ default โหมดภาษีเป็น `catch_up` (คำนวณภาษีคาดการณ์ทั้งปีแล้วเฉลี่ยตามเดือนที่เหลือหลังหักยอดที่เคยหักแล้ว) และแยกเก็บ `PayRunItem.income_tax_withholding` พร้อมแสดงในหน้า payroll detail/employee detail
- **2026-04-28 (Monthly tax cap policy):** เพิ่มเพดานหักภาษีรายเดือนใน `services/payroll.py` (`tax_monthly_cap_rate`, default 15%) โดยจำกัดยอดหักทั้งโหมด `catch_up` และ `safe` ที่ระดับ `% ของเงินสุทธิก่อนหักภาษี`
- **2026-04-28 (UI polish #1):** ฟอร์มพนักงานเพิ่ม section ภาษี (โหมด/cap/ลดหย่อนเพิ่ม/ยกเว้น) merge เข้า `custom_terms` JSON, register Jinja filters `dmy`/`dmy_hm` (รูปแบบ `27/04/2026`) และใช้กับหน้า list/detail หลัก, เพิ่ม jump-to-page (input + dropdown) ที่ /petty-cash /daily /fuel
- **2026-04-28 (Petty dedup wave 2):** เพิ่ม alias `AYU: สมัย → สมัย อยุธยา`, ทำ dedup ข้าม source แบบ canonical-name + reassign site=AYU จาก suffix `อยุธยา` 565 แถว ลด unlinked/ซ้ำของรอบเก่า
- **2026-04-28 (Ops context):** บันทึกบริบทธุรกิจพื้นที่เช่าในลาน วาย.เค (เสี่ยงรายได้หาย ~34,000/เดือนหากผู้เช่าย้าย) และกรอบตัดสินใจเน้นผู้เช่าสายงานสะอาด/ไม่แย่ง capacity ลานจอดหลัก
- **2026-04-28 (Ops risk update):** เพิ่มข้อเท็จจริงหน้างานว่าทางเข้า-ออกรถบรรทุกติดข้อพิพาททางกฎหมาย (คดีถนนเข้าออก) ต้องปรับกลยุทธ์ผู้เช่าใหม่เป็น access-first และใช้สัญญาเงื่อนไขความเสี่ยง

## 2026-04-28 (Ad-hoc quote baseline for Direct-to-store)

- ล็อกสมมติฐานคำนวณเสนอราคาแบบแชท: ค่าเสื่อมรถ `700,000/8/365`, เบี้ยประกันจริง `13,500/365`, น้ำมันฐาน `31.5`, maintenance `1.5 บาท/กม.`, back office `12%`
- ตั้งหลักการ conservative สำหรับงาน ad-hoc: `1 เที่ยว = 1 วัน` (จันทร์-ศุกร์) และถ้าวิ่งมากกว่า 1 เที่ยว/วันให้นับเป็น upside
- ปรับคำนวณน้ำมันให้แยกตามประเภทรถในงานเสนอราคา Direct-to-store: 6W `5.5 กม./ลิตร`, 10W `4.5 กม./ลิตร` พร้อมเพิ่มตัวชี้วัด `%น้ำมันต่อค่าขนส่ง` ต่อรูท
- เปลี่ยนเงื่อนไขเจรจาน้ำมันเป็น `1.5% ต่อ 1 บาท` และ reprice ในไฟล์ทำงาน (`_v3_adjusted_only`) ให้ margin ที่ fuel target 50 ยังอยู่ราว 10%
- อัปเดตเงื่อนไขราคาดีล Direct-to-store เพิ่มเติม: 6W consumption = `5.0`, ค่าเที่ยวแบบ distance ladder (`0-200 = 500/600`, แล้ว +100 ต่อทุก 100 กม.), และโซนเชิงกลยุทธ์ `สมุทรปราการ/ฉะเชิงเทรา/ชลบุรี` ใช้ target margin `5%`
- **2026-05-01 (Oatside reports):** 	rips.html/รายเที่ยวต่อทะเบียน — คอลัมน์ ค่าขนส่ง / เสียเวลา+50% / เสียเวลา+100% / ตีเปล่า+50%; No-work recovery รองรับข้ามคืน (irst_no_work_trip_by_plate_recovery_day + synthetic plate_dest_day_rows)
