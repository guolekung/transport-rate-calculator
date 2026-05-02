---

## 2026-04-29 (Session Summary #68 - Transport Rate: ดึงราคาย้อนหลัง + คลุมหาเฉลี่ยแบบ Excel)

### บริบทจากผู้ใช้
- ผู้ใช้ต้องการเพิ่มในหน้า `transport_rate_calculator.html` ให้ดึงราคาน้ำมันรายวันจากเว็บได้
- ต้องการ workflow หา "ค่าเฉลี่ย" แบบใช้งานง่ายเหมือน Excel โดยคลุมช่วงข้อมูลแล้วเห็นค่าเฉลี่ยทันที

### การตัดสินใจรอบนี้
- เพิ่ม panel ใหม่ใน Step 1 สำหรับดึงข้อมูลราคาย้อนหลังจากหน้า Bangchak ผ่าน proxy-read (`r.jina.ai`) เพื่อลดปัญหา cross-origin
- รองรับการเลือกชนิดน้ำมัน (ค่าเริ่มต้น `ไฮดีเซล S`) และปี พ.ศ. ที่ต้องการดึง
- เพิ่ม interaction แบบ drag-select บนตารางย้อนหลัง (คลุมหลายวัน) แล้วคำนวณ `ค่าเฉลี่ย / ต่ำสุด / สูงสุด / จำนวนวัน`
- เพิ่มปุ่ม "ใช้ค่าเฉลี่ยที่คลุม" เพื่อเติมกลับช่อง `ราคาน้ำมัน` อัตโนมัติใน Step 1

### สิ่งที่ทำแล้ว
- แก้ `TransportRateCalculator/transport_rate_calculator.html`
  - เพิ่ม UI: historical panel, ตารางรายวัน, กล่องสรุปค่าเฉลี่ย
  - เพิ่ม JS parser ตารางย้อนหลังจาก markdown table
  - เพิ่ม selection logic (click + drag) และการคำนวณสถิติ
  - เพิ่ม fallback status message เมื่อดึงข้อมูลไม่สำเร็จ

### Action ถัดไป
- ให้ผู้ใช้เปิดหน้าแล้วทดสอบ `ดึงข้อมูลย้อนหลัง` → คลุมช่วงวัน → กดใช้ค่าเฉลี่ย
- ถ้าเครือข่ายบางจุดบล็อก proxy ให้เตรียม endpoint ฝั่ง backend สำหรับ fetch/parse แล้วให้หน้าเว็บเรียก endpoint ภายในแทน (ลด CORS risk)

---

## 2026-04-29 (Session Summary #69 - เพิ่ม fallback วางข้อมูลเองเมื่อดึงย้อนหลังไม่ผ่าน)

### บริบทจากผู้ใช้
- ผู้ใช้ทดสอบแล้วหน้าจอขึ้นสถานะว่าไม่มีข้อมูลที่เลือก (ยังคลุมไม่ได้) หลังลองดึงข้อมูลย้อนหลัง

### การตัดสินใจรอบนี้
- เพิ่ม fallback แบบไม่พึ่ง network call: ให้ผู้ใช้คัดลอกตารางจากหน้าเว็บแล้ววางข้อความเข้า textarea ใน Step 1
- parser รองรับทั้งรูปแบบ markdown table (`| วันที่ | ... |`) และบรรทัดสั้น (`dd/mm/yyyy 40.20`)

### สิ่งที่ทำแล้ว
- แก้ `transport_rate_calculator.html`:
  - เพิ่ม UI `historyPasteInput` + ปุ่ม `แปลงข้อมูลที่วาง`
  - เพิ่มฟังก์ชัน `extractRowsFromPastedText()` และ `parseHistoricalFromPaste()`
  - ปรับข้อความสถานะตอน fetch ไม่ผ่านให้ชี้ไปใช้ fallback ทันที

### Action ถัดไป
- ให้ผู้ใช้ลองคัดลอกจากหน้าราคาย้อนหลังมาวาง แล้วกดแปลงข้อมูล จากนั้นคลุมช่วงและกดใช้ค่าเฉลี่ย

---

## 2026-04-29 (Session Summary #70 - รองรับ paste แบบ tab-separated จากเว็บตรงๆ)

### บริบทจากผู้ใช้
- ผู้ใช้ส่งตัวอย่างข้อมูลที่ copy มาจากเว็บโดยตรงเป็นบรรทัด tab-separated (วันที่ + ราคาหลายคอลัมน์)
- ต้องการให้วางแบบนี้แล้วระบบ parse ได้ทันที

### การตัดสินใจรอบนี้
- ปรับ parser ให้ดึงเลขทุกคอลัมน์หลังวันที่ แล้ว map ตามชนิดน้ำมันที่เลือก (`ไฮดีเซล S` / `ไฮพรีเมียมดีเซล S`)
- เพิ่ม dedup ตามวันที่ เพื่อกันแถวซ้ำเมื่อวางข้อมูลจำนวนมากหรือวางทั้งหน้า

### สิ่งที่ทำแล้ว
- แก้ `extractRowsFromPastedText()` ใน `transport_rate_calculator.html`
  - parse แบบ markdown table เดิม
  - parse แบบ tab/space multi-column (รูปแบบที่ผู้ใช้ copy จากเว็บ)
  - fallback กรณีมีเลขท้ายแถวเพียงตัวเดียว

### Action ถัดไป
- ให้ผู้ใช้วางชุดข้อมูล tab-separated ที่ส่งมา แล้วกด `แปลงข้อมูลที่วาง` และคลุมช่วงทดสอบค่าเฉลี่ย

---

## 2026-04-29 (Session Summary #71 - เติมวันที่หายด้วยราคาวันก่อน + เลือกช่วงวันที่ตั้งแต่-ถึง)

### บริบทจากผู้ใช้
- หน้าเว็บต้นทางไม่ได้มีทุกรายวัน จึงอยากให้ระบบเติมวันที่เองและใช้ราคาวันก่อนหน้าเมื่อยังไม่เปลี่ยนราคา
- ต้องการเพิ่มการเลือกช่วงวันที่แบบ `ตั้งแต่-ถึง` แล้วให้ระบบคำนวณค่าเฉลี่ยให้อัตโนมัติ

### การตัดสินใจรอบนี้
- หลัง parse ข้อมูลย้อนหลัง ให้ normalize เป็นรายวันต่อเนื่องในช่วงข้อมูลที่มี (`min..max date`) โดยเติมวันขาดด้วยค่า `carry-forward` จากวันก่อนหน้า
- เพิ่ม date range selector (`ตั้งแต่`, `ถึง`) และปุ่มเลือกช่วง เพื่อไฮไลต์รายการในช่วงวันที่ที่กำหนดแล้วใช้ระบบเฉลี่ยชุดเดียวกับการคลุมด้วยเมาส์
- แสดง badge `เติมวันหาย` ในตารางเพื่อให้ trace ได้ว่าแถวไหนเป็นข้อมูลเติมอัตโนมัติ

### สิ่งที่ทำแล้ว
- แก้ `transport_rate_calculator.html`
  - เพิ่ม helper แปลงวันไทย/สากลและฟังก์ชัน `fillMissingHistoricalDates()`
  - เพิ่ม date range inputs + `selectHistoryByDateRange()`
  - ปรับ status message ให้รายงานจำนวนวันที่ดึงจริงและจำนวนวันที่เติมเพิ่ม

### Action ถัดไป
- ให้ผู้ใช้ทดสอบด้วยข้อมูล Alt+A ทั้งหน้า: แปลงข้อมูล → เลือกช่วงตั้งแต่-ถึง → กดใช้ค่าเฉลี่ยที่คลุม

---

## 2026-04-29 (Session Summary #72 - เปลี่ยนหน้าราคาย้อนหลังเป็นค.ศ.ทั้งหมด)

### บริบทจากผู้ใช้
- ผู้ใช้ยืนยันให้ใช้ปีค.ศ.ทั้งหมดใน workflow นี้

### การตัดสินใจรอบนี้
- เปลี่ยน UI input ปีใน Step 1 เป็น `ปี (ค.ศ.)` ค่าเริ่มต้น `2026`
- ปรับ parser ให้รับข้อมูลวันที่จากเว็บได้ทั้ง พ.ศ./ค.ศ. แต่ filter ตามปีค.ศ.ที่ผู้ใช้กรอก
- แสดงวันที่ในตารางย้อนหลังและวันที่เติมอัตโนมัติเป็นรูปแบบ `dd/mm/yyyy` (ค.ศ.) ทั้งหมด

### สิ่งที่ทำแล้ว
- แก้ `transport_rate_calculator.html`:
  - label + default year เป็นค.ศ.
  - normalize year raw จากเว็บ (`>2400` ถือเป็นพ.ศ.แล้วลบ 543)
  - ปรับ display date formatter ให้แสดงค.ศ.

### Action ถัดไป
- ให้ผู้ใช้ทดสอบกรอกปีค.ศ. เช่น 2026 แล้ววางข้อมูลเดิมจากเว็บ (พ.ศ.) ระบบควร parse และแสดงตารางเป็นค.ศ.ได้ถูกต้อง

## 2026-04-28 (Session Summary #50 - Step 1 เปลี่ยนเป็นราคาน้ำมันย้อนหลังและโฟกัสไฮดีเซล S)

### บริบทจากผู้ใช้
- ผู้ใช้ขอให้หน้าแรกเปลี่ยนเป็นมุมมองราคาย้อนหลังตามตัวอย่างที่แนบ
- ต้องการดูเฉพาะ `ไฮดีเซล S` (ไม่ต้องสนใจชนิดน้ำมันอื่น)

### การตัดสินใจรอบนี้
- ปรับ Step 1 จาก "ราคาปัจจุบัน" เป็น "ราคาย้อนหลัง"
- ใช้ iframe ชี้ไปหน้า `Bangchak historical`
- ปรับ copywriting ให้ชัดว่าให้ดูและกรอกเฉพาะคอลัมน์ `ไฮดีเซล S`

### สิ่งที่ทำแล้ว
- แก้ `TransportRateCalculator/transport_rate_calculator.html`:
  - เปลี่ยน title/description ของ Step 1
  - เปลี่ยน iframe source เป็น `https://www.bangchak.co.th/th/oilprice/historical`
  - เปลี่ยนข้อความ hint ใต้ iframe ให้โฟกัสเฉพาะไฮดีเซล S
  - เปลี่ยน label ช่องกรอกจาก `ราคาน้ำมัน` เป็น `ราคาไฮดีเซล S`
- ตรวจ lints แล้วไม่พบ error

### Action ถัดไป
- deploy ขึ้น GitHub Pages
- ให้ผู้ใช้ลองรีเฟรชหน้าเว็บแล้วยืนยันว่า flow ใช้ดูย้อนหลังสะดวกขึ้น

---

## 2026-04-28 (Session Summary #51 - Rollback Step 1 เพราะ historical iframe ถูกบล็อก)

### บริบทจากผู้ใช้
- หลัง deploy ผู้ใช้ทดสอบแล้วพบข้อความ `www.bangchak.co.th refused to connect` ใน iframe
- ผู้ใช้อนุญาตให้ rollback กลับแบบเดิมหากใช้งานไม่ได้

### การตัดสินใจรอบนี้
- rollback Step 1 กลับไปใช้ iframe หน้า "ราคาปัจจุบัน" ที่ embed ได้จริง
- คงลิงก์ไปหน้า `historical` ไว้สำหรับเปิดแท็บใหม่แทนการฝัง

### สิ่งที่ทำแล้ว
- แก้ `TransportRateCalculator/transport_rate_calculator.html` กลับเป็น:
  - title/desc แบบเดิม (ราคาปัจจุบัน)
  - iframe source `oil-price.bangchak.co.th/BcpOilPrice1/th`
  - label ช่องกรอกกลับเป็น `ราคาน้ำมัน`
  - ลิงก์ `ราคาน้ำมันย้อนหลัง` คงไว้ให้กดเปิดใหม่
- ตรวจ lints แล้วไม่พบ error

### Action ถัดไป
- deploy ขึ้น GitHub Pages ให้ผู้ใช้รีเฟรชแล้วใช้งานต่อได้ทันที
# CONTEXT LOG

ไฟล์นี้ใช้เก็บสรุปบริบทสำคัญจากการคุยแต่ละรอบ เพื่อป้องกันข้อมูลหล่นเมื่อแชทยาว

---

## 2026-04-08 (Session Summary #24 — Phase 3 COMPLETE: CFO Dashboard)

### คำสั่งผู้ใช้
> "ข้อมูลหนี้ เดี๋ยวฉันคิดว่าทำเป็น อีกหน้านึงไว้กรอก เพิ่มที่หลังละกัน ส่วนตอนนี้ลุยต่อได้เลยยาวๆ วันใหม่แล้ว"

→ เลื่อนการกรอกข้อมูลหนี้ออกไป (ทำเป็นหน้า form สำหรับ admin กรอกเอง) แล้วลุย Phase 3 ให้จบในคืนเดียว

### สิ่งที่เสร็จ
- **Schema v13** (2 ตารางใหม่ใน `models.py`):
  - `Loan`: code auto (L0001), lender, loan_kind (6 ประเภท), purpose, principal, annual_rate_pct, term_months, start_date, first_payment_date, pay_day_of_month, monthly_payment (override), current_balance, collateral, linked_vehicle_id, status
  - `LoanPayment`: pay_date, amount, principal_portion, interest_portion, notes — หักจาก `Loan.current_balance` อัตโนมัติ
  - `LOAN_KINDS`: term (ลดต้นลดดอก) / hire_purchase (งวดคงที่) / revolving (OD — ดอกต่อเดือน) / informal (ยืมส่วนตัว) / factoring / other

- **`services/finance.py`** (ฟังก์ชันบริสุทธิ์ทั้งหมด รับ Session → คืน dict):
  - `amortization_schedule`: สูตร `P * r*(1+r)^n / ((1+r)^n - 1)` สำหรับ term / งวดคงที่ / ดอกอย่างเดียวสำหรับ revolving
  - `loan_summary`: รวม active loans → total_balance + monthly_burden + next_year_interest
  - `monthly_pnl`: revenue (DailyJob + DailyJobFee) − cost (FuelTxn + PayRunItem.gross_total + PettyCashTxn ที่กรองหมวด + MaintRecord + dok) → net_profit + net_margin_pct
    - **สำคัญ**: petty cash กรองเฉพาะ `toll/parking/loading/fine/accident` เพราะ `fuel/repair/tire` ซ้ำกับ FuelTxn/MaintRecord, `driver_advance/salary_partial` recover ผ่าน payroll — มี toggle `include_other_petty`
    - แสดง breakdown `petty_by_cat` ให้ admin เห็นว่าอะไรถูกรวม/ไม่รวม
  - `cost_per_vehicle`: revenue/fuel/maint ต่อคัน + gross margin + %
  - `cash_flow_projection`: N วันข้างหน้า (hardcoded: AR เข้าปลายเดือน M+1, เงินเดือนต้นเดือน, หนี้ตามตารางผ่อน, fuel/petty = avg 30 วัน)
  - `break_even_and_runway`: avg_rev_per_trip − avg_fuel_per_trip = contribution → break_even = fixed_monthly / contribution

- **6 หน้าเว็บใหม่ `/finance/*`** (+ templates):
  - `/finance` → dashboard หลัก (KPI 4 ใบ + P&L ซ้าย + health ขวา + trend 6 เดือน + top 15 รถ)
  - `/finance/loans` → ตารางรายการหนี้ + สรุป
  - `/finance/loans/new` + `/finance/loans/{id}` → ฟอร์มกรอก + ตารางผ่อน auto + บันทึกจ่าย (+ `/payment` `/delete`)
  - `/finance/pnl?year=YYYY` → P&L 12 เดือนทั้งปี + สรุปแถวสุดท้าย
  - `/finance/vehicles?month=YYYY-MM` → ต้นทุนต่อคันทั้งหมด
  - `/finance/cashflow?days=N` → ตารางเงินเข้า-ออก + running balance

- **Bug fix ระหว่างทาง**: FastAPI route decorator stacking (`@app.post("/new")` + `@app.post("/{id}")`) ทำให้ "new" match เป็น `loan_id` → แยก handler ใช้ `{loan_id:int}`

- **Petty cash realization**: ข้อมูลเก่า 50,753 rows → หลายแถวยัง `category="other"` (ค่า default ตอน import) → ยอดพุ่งเป็น 1.8M/เดือน ถ้ารวมหมด จึง default exclude และมี toggle

### ตัวเลขจริงที่ทดสอบ (Feb 2026)
- Revenue total: 2,181,067 ฿ (705 เที่ยว)
- Fuel: 1,249,693 ฿
- Payroll gross: 474,442 ฿
- Petty (strict): 296,002 ฿
- Maint: 0 (ยังไม่มี import)
- Interest: 0 (ยังไม่มี loan)
- **Net profit: +160,930 ฿ (7.4% margin)** — ดูสมเหตุสมผล

### Break-even (90-day avg)
- Avg rev/trip: 3,798 ฿
- Avg fuel/trip: 2,117 ฿
- Contribution: 1,681 ฿/เที่ยว (44%)
- Fixed monthly (ไม่มีดอก): 134,020
- Break-even: 80 trips/เดือน · ปัจจุบัน 326/เดือน → มี headroom 246 trips
- **Status: healthy** (+413k/เดือนเฉลี่ย)

### `.gitignore` ใหม่
- กัน *.db, Salary/, Fuel/, *.xlsx, *.pdf, credentials*.json, .env, nested .git
- Sensitive business data จะไม่โดน commit โดย accident อีก

### TODO ต่อ
- ผู้ใช้ทยอยกรอกหนี้ผ่าน UI เมื่อได้ข้อมูลจากพ่อ
- Phase 4 (Driver PWA): login, job view, photo + OCR, vehicle check + alcohol test, safety audit pack
- Promote raw→master ที่เหลือ (Petty ~80%, Daily ~7%)

---

## 2026-04-08 (Session Summary #1)

### สิ่งที่ตกลงร่วมกัน
- เป้าหมายคือระบบเดียวครบวงจร: Dispatch -> Daily -> Billing -> Petty Cash -> Payroll -> Accounting -> Owner Dashboard
- ใช้ไฟล์เดิมของแต่ละไซต์ (`AYU`, `BigC`, `LCB`) เป็นฐานก่อน แล้วค่อย migrate ไปคีย์งานในระบบ
- โครง deploy เลือกแบบฟรีบน Windows server เครื่องหลัก
- แนวทางเชื่อมสองไซต์เลือก `Tailscale` เป็นหลัก (แทน public IP + DDNS)
- เพิ่มขอบเขต Maintenance & Stock แล้ว:
  - PM/RM
  - สต็อกอะไหล่
  - ประวัติยาง
  - เรทน้ำมัน/ค่าซ่อม/เลขไมล์

### เอกสารที่สร้างแล้ว
- `docs/MASTER_SPEC.md`
- `docs/ROLE_MATRIX.md`
- `docs/DEPLOYMENT_FREE_WINDOWS.md`
- `docs/DAILY_MODULE_DESIGN.md`

### หมายเหตุการทำงานต่อ
- ทุกครั้งที่คุยเพิ่ม ต้องอัปเดตไฟล์นี้พร้อมแผนถัดไปใน `NEXT_ACTION_PLAN.md`

---

## 2026-04-08 (Session Summary #2 - Phase 0 Started)

### สิ่งที่สั่งและทำแล้ว
- ผู้ใช้สั่งเริ่ม `Phase 0`
- สร้างเอกสารสำคัญเพิ่ม 3 ไฟล์:
  - `docs/DATA_DICTIONARY.md`
  - `docs/JOB_STATUS_FLOW.md`
  - `docs/CUSTOMER_BILLING_PROFILE_TEMPLATE.md`

### ผลลัพธ์
- โครงข้อมูลกลางเริ่มนิ่งขึ้น พร้อมชื่อ table/field ระดับปฏิบัติการ
- สถานะงานมาตรฐานและ lock policy ถูกนิยามแล้ว
- มี template เก็บกติกาวางบิลรายลูกค้าแบบ versioned

### Action ถัดไป
- เก็บ requirement จริงลูกค้า 3-5 เจ้าแรกลง profile template
- ตัดสินใจชนิด primary key กลาง (uuid หรือ bigint)
- ล็อก enum กลาง (status, category, pay_type) ก่อนเริ่มพัฒนา API

---

## 2026-04-08 (Session Summary #3 - Phase 0 Continued)

### สิ่งที่ทำเพิ่ม
- สร้าง `docs/ENUMS_AND_RULES.md` (ล็อก enum กลาง)
- สร้าง `docs/DATA_LOCK_POLICY.md` (policy lock/adjust หลังปิดรอบ)
- สร้าง `docs/CUSTOMER_BILLING_PROFILES.md` (seed profile ลูกค้า 5 โปรไฟล์)
- อัปเดต `docs/README.md` ให้ index เอกสารชุดใหม่

### สถานะปัจจุบัน
- Phase 0 ส่วนหลักครบแล้วในระดับเอกสาร blueprint
- พร้อมก้าวไป phase implementation (schema SQL + API contract)

### ความเสี่ยงที่ยังต้องเคลียร์
- รายละเอียด customer profile ยังต้องยืนยันกับทีมปฏิบัติงานจริง
- ต้องเลือกระหว่าง PK แบบ `uuid` หรือ `bigint` ให้ชัดก่อน generate schema

---

## 2026-04-08 (Session Summary #4 - Phase 0.5 Started)

### สิ่งที่ทำแล้ว
- สร้าง `docs/API_CONTRACT_V1.md`
- สร้าง `docs/SQL_SCHEMA_V1.md` (PostgreSQL DDL v1)
- อัปเดต index ใน `docs/README.md`

### การตัดสินใจรอบนี้
- ใช้ REST API รูปแบบ `/api/v1` สำหรับ MVP
- SQL schema รุ่นแรกใช้ `bigserial` เพื่อลดความซับซ้อนช่วงเริ่ม
- lock rule และ enum ยังคงอิงเอกสารก่อนหน้า (`ENUMS_AND_RULES.md`, `DATA_LOCK_POLICY.md`)

### Action ถัดไป
- สร้าง `IMPORT_MAPPING_SPEC.md` สำหรับ AYU/BigC/LCB
- สร้าง `VALIDATION_RULEBOOK.md` ให้ครบทุก blocker/warn
- แปลง `SQL_SCHEMA_V1.md` เป็นไฟล์ migration SQL จริง

---

## 2026-04-22 (Session Summary #5 - Petty Cash Online MVP Bootstrap)

### สิ่งที่ทำแล้ว
- สร้างสคริปต์ `tools/build_petty_cash_online.py` สำหรับย้ายข้อมูลย้อนหลังจาก `Salary/AYU|BigC|LCB/สดย่อยวังน้อย.xlsx` ไปเป็นข้อมูลออนไลน์
- สร้างหน้าเว็บ `reports/petty-cash-online/index.html` สำหรับใช้งานแบบค้นหา/กรอง/ดูยอดรวมได้ทันที
- สร้างไฟล์ผลลัพธ์อัตโนมัติ:
  - `reports/petty-cash-online/petty_cash_records.csv`
  - `reports/petty-cash-online/petty_cash_records.json`
  - `reports/petty-cash-online/summary.json`

### การตัดสินใจรอบนี้
- เริ่มออนไลน์ด้วยแนวทาง "Data First, UI Improve Later" เพื่อให้ทีมใช้งานได้เร็ว
- เพิ่มหมวด `finance` สำหรับคำสำคัญเงินกู้/ไฟแนนซ์/ค่างวดตั้งแต่รอบนำเข้าข้อมูล
- เก็บฟิลด์ parse memo เบื้องต้น (`parsed_person`, `memo_amount_in_text`, `memo_has_deduction`) เพื่อเตรียมต่อยอดหักเงินเดือนอัตโนมัติ

### Action ถัดไป
- เพิ่ม rule parser ภาษาไทยแบบแม่นยำขึ้นสำหรับรูปแบบ `ชื่อ + รายละเอียด + จำนวน + หัก`
- เพิ่มหน้ากรอกข้อมูลออนไลน์ (create/edit) พร้อมสิทธิ์ผู้ใช้และ audit log
- เชื่อมรายการ `รับตู้/คืนตู้/สำรอง` เข้ากับ trip key (วันที่, คนขับ, ทะเบียน, เลขจ็อบ/เบอร์ตู้)


---

## 2026-04-22 (Session Summary #6 - Day-1 Skeleton Built)

### บริบทจากผู้ใช้
- ผู้ใช้มืด 8 ด้าน เพราะมีหลายแชทคุยกันคนละเรื่อง + ของเดิมหลายตัว (TransportRateCalculator, AccidentCases, payroll_system.py, Excel ทุกไซต์)
- เป้าหมาย: ระบบเดียวจบ อัตโนมัติทุกส่วน ลดงานที่คนไม่จำเป็นต้องทำเอง
- Flow ต้นน้ำ→ปลายน้ำ: Daily → Dispatch → Billing/Accounting → Petty Cash → Payroll → Maintenance
- ผู้ใช้ไม่เขียนโค้ดเอง ทำหน้าที่ vibe-test (รัน/หาบัค/สั่งแก้)
- ทีม 7 คน (บัญชี 2 / OP 3 / ผู้จัดการ 1 / เจ้าของ 1)
- ความเร่ง: สูงสุด (เคยเสียเวลาเกือบ 1 ปีกับโปรแกรมเมอร์ภายนอก)
- Server: ยังไม่แตะ ทดสอบบนโน้ตบุ๊กก่อน ตอนขึ้นจริงขอเป็น one-click installer
- ผู้ใช้เซฟ context เดิมไว้ที่: Daily module design backup/cursor_daily_module_design_for_automate 1 22.4.26 18.35.md

### การตัดสินใจรอบนี้
- **Stack**: FastAPI + SQLite + HTMX + Tailwind (CDN) + start.bat
  - เหตุผล: รันบนโน้ตบุ๊กได้ทันที ไม่ต้องติดตั้ง Node/Postgres/Docker
  - Migration path: ย้าย SQLite → PostgreSQL ตอนขึ้น PC Server + Tailscale
- **จุดเริ่มต้นโค้ดจริง**: โมดูล Daily (ต้นน้ำ)
- **ตำแหน่งโค้ด**: ProjectYK_System/app/

### สิ่งที่ทำแล้ว
- สร้างโครง ProjectYK_System/app/ ประกอบด้วย:
  - main.py (FastAPI + SQLModel + routes)
  - templates/base.html, daily_list.html, daily_new.html
  - requirements.txt, start.bat, README.md, .gitignore
- โมเดลแรก: DailyJob (อ้างอิงจาก Salary/daily_module/contracts.py)
- ฟังก์ชันพร้อมใช้: รายการ/ฟิลเตอร์ site+วันที่/เพิ่ม/ลบ/health
- ติดตั้ง venv และทดสอบ: server ขึ้นได้, /health ตอบ {"ok":true}
- อัปเดต MODULE_REGISTRY ลงทะเบียน OnePlatformApp
- อัปเดต CHANGELOG_MASTER

### Action ถัดไป
- ผู้ใช้ดับเบิลคลิก ProjectYK_System/app/start.bat เพื่อทดสอบ (ดูวิธีที่ README)
- เมื่อ vibe-test ผ่าน → ต่อ Master Data (employees, vehicles, customers) ด้วย dropdown
- เขียนสคริปต์ import Excel → SQLite สำหรับ AYU เป็นไซต์แรก
- เพิ่มหน้า Dispatch (plan งาน + จับคู่รถ/คนขับ)

---

## 2026-04-22 (Session Summary #7 - Context Rule + 3-Site Field Mapping)

### บริบทจากผู้ใช้
- ยืนยัน Day-1 skeleton รันผ่าน ไม่มี error
- กังวลเรื่อง context หายเมื่อเปลี่ยนแชท
- แนบไฟล์ `ProjectYK_System/Daily.xlsx` (ตัวอย่างจริง 3 sheet: AYU 28 cols, BIGC 19 cols, LCB 40 cols)

### การตัดสินใจรอบนี้
- สร้าง Cursor rule `.cursor/rules/project-yk-context.mdc` ให้ทุก agent `alwaysApply=true`
  - บังคับอ่าน AGENT_BOOTSTRAP / MODULE_REGISTRY / CHANGELOG / CONTEXT_LOG / NEXT_ACTION_PLAN ทุกรอบ
  - บังคับอัปเดต CONTEXT_LOG + NEXT_ACTION_PLAN + CHANGELOG ก่อนจบ turn
  - ล็อก tech stack (FastAPI/SQLite/HTMX/Tailwind) และภาษาตอบ (ไทย)
- สร้าง `docs/IMPORT_MAPPING_SPEC.md` บันทึก mapping ของ 3 sheet จากตัวอย่างจริง

### สิ่งที่เรียนรู้จาก Daily.xlsx
- AYU: โมเดลเรียบ (งาน 1 เที่ยว = 1 แถว, มี placeholder สำหรับรถว่าง), ประเภทรถ 6W/10W/10WL
- BIGC: รถหัวลาก + หางแยก, มีเงินเดือนผสมในแถวรายวัน, มีระบบ "น้ำมันทำได้" (target vs actual)
- LCB: ซับซ้อนสุด 40 คอลัมน์, Status column เป็น enum ลูกค้า/สถานะรถ, มีค่าแยก lift/yard/clean/shore/port/weighing, Type=Export/Import/Domestic

### ปัญหาโครงสร้างที่ต้องแก้ในเฟสถัดไป
- `DailyJob` ปัจจุบันเล็กไป ต้องเพิ่ม: doc_no, fuel_liter/amount/mile, container_no, trip_type, invoice_no/date, wht_53, mflow
- ควรแยกตาราง: `daily_job_fees` (ค่า lift/yard/clean/shore/port/weighing/special/ot), `fuel_txns` (link 1:N)
- ต้องมีตาราง `trucks` (head/tail) และ `trailers` แยกสำหรับ BIGC

### คำถามเปิดต่อผู้ใช้ (รอคำตอบรอบหน้า)
- ค่า enum ของ LCB.Status
- ความหมายของ BIGC.รับตู้ และ BIGC.เงินเดือน ต่อแถว
- ใครคีย์/คีย์เมื่อไหร่ของแต่ละไซต์
- ทีมอยากเริ่มทดลองจากไซต์ไหนก่อน (ผมแนะนำ AYU เพราะโมเดลง่ายสุด)

### Action ถัดไป
- ตอบคำถามข้างบนจากผู้ใช้
- ขยาย `DailyJob` schema ให้ครอบคลุมทั้ง 3 ไซต์ (หรือทำ AYU ก่อน)
- สร้างสคริปต์ `tools/import_daily_ayu.py` นำเข้า Excel → SQLite
- เพิ่ม Master Data (employees, vehicles, customers) + dropdown

---

## 2026-04-22 (Session Summary #8 - Full Domain Knowledge Captured)

### บริบทจากผู้ใช้ (ข้อมูลสำคัญมาก - อย่าลืม!)

**ตอบคำถาม 10 ข้อจาก Session #7:**

1. LCB.Status ปนกันจริง (ลูกค้า + สถานะรถ) เพราะไม่มีช่องอื่นให้ใส่
2. BIGC.รับตู้ ค่าที่เป็นไปได้: รับรถ (event เปลี่ยนคนขับ), 1DH (direct backhaul), 1Big c (สายสั้นหลัก), 1+ (สายสั้นพ่วง), 2BigC (สายยาวหลัก), 2++ (สายยาวพ่วง)
3. BIGC.เงินเดือน = แอดมินใส่เฉยๆ (9000 บาท) ตอนทำเงินเดือนจริงใช้การันตีเต็ม แล้วหักรายวันตาม "ลาหยุด" ที่แอดมินใส่ใน col G
4. ประเภทรถ: แอดมินบางทีไม่ดู แต่กำหนด Master ได้
5. คนคีย์: OP 1 = AYU+BIGC, OP 2 = LCB (ใช้ไลน์+Notepad), บัญชี 1 เอาเอกสารมาลงเดลี่. Vision: OP ลงทันทีตอน dispatch, บัญชีมา "หยอดตัวเลข" ไม่พิมพ์ซ้ำ
6. คีย์ตอนได้รับใบงาน (realtime)
7. PC 100% + Google Sheet สำหรับดูนอกออฟฟิศ, อนาคตมือถือ/แท็บเล็ต
8. ใส่ทะเบียนรถล่วงหน้า คนขับสลับรถได้
9. Base เป็นทุกไซต์ แต่รถบิ๊กซีไปวิ่งแหลมได้ (ต้องรวม Daily ข้ามไซต์ได้)
10. ใช้ Feb 2026 ทดสอบ

### Payroll Rules (เก็บละเอียดใน SITE_PAYROLL_RULES.md)

**Common ทุกไซต์:**
- เงินประกันตน 10,000 หักเดือนละ 1,000 จนครบ
- ประกันสังคม 5% ฐาน 9000 (สมมุติทุกคน)
- เงินเบิก/หักจากสดย่อย
- ค่าอุบัติเหตุ 2000/ครั้ง ผ่อน 500x4 งวด แอดมินลง Excel เดือนล่วงหน้า

**BIGC:** เงินเดือน 9000 + ค่าเที่ยว (250/100/ตามระยะทาง/200) + ค่าเรทน้ำมันเหลือคืน (target - actual) x 16 บาท. ตัดรอบ 1-สิ้นเดือน จ่าย 1 ของเดือนถัดไป

**LCB 2 modes:**
- A: รายเที่ยว เงินเดือน 9240 + ค่าดูแลรถ 3000 + ค่าเที่ยว (หักรายวันเมื่อลา)
- B: เหมาน้ำมัน 60% ของค่าขนส่ง, บางค่าไม่แบ่ง (ค่าเสียเวลา ค่าค้างคืน), คนขับจ่ายน้ำมันเอง
- ตัดรอบ 16-15 จ่าย 1

**AYU 2 modes:**
- A: รายเที่ยวอย่างเดียว 6 ล้อ 300-500, 10 ล้อ +100, อาจมีการันตี 12000/15000
  - ไม่นับวันคนขับไม่มา, นับวันบริษัทไม่มีงาน, คนใหม่ไม่ตกลง=ไม่จ่าย
- B: เหมาน้ำมัน 55-60% (แล้วแต่ตกลง), คนขับจ่ายน้ำมัน+M-Flow
- ตัดรอบ 26-25 จ่ายสิ้นเดือน

### BIGC Branch Rate (ต้องขอไฟล์จากผู้ใช้ภายหลัง)

**สูตรเบื้องต้น:**
- 1Big c: ค่าขนส่ง = rate ของสาขาไกลสุดในเที่ยว, ค่าเที่ยว = 250
- 1+: ค่าขนส่ง = 400/สาขา, ค่าเที่ยว = 100/สาขา
- 2BigC: ค่าขนส่ง = rate สาขาไกลสุด, ค่าเที่ยว = ตามระยะทาง (ต้องใช้ตาราง)
- 2++: ค่าขนส่ง = 600/สาขา, ค่าเที่ยว = 200/สาขา

### สิ่งที่ทำแล้วรอบนี้
- สร้าง `docs/SITE_PAYROLL_RULES.md` (เก็บกฎ payroll 3 ไซต์ + edge cases)
- สร้าง `docs/BIGC_BRANCH_RATE_SPEC.md` (โครงสร้างค่าขนส่ง BIGC + ตารางสาขา)
- สร้าง `docs/WORKFLOW_BY_TEAM.md` (ทีม 7 คน + vision workflow + cross-site scenario)

### Open Questions ที่ยังรอคำตอบ (ถามใน session หน้า)

1. LCB Mode A: หักรายวันแบบ (9240+3000)/30 หรือ 9240/30 + 3000/30 แยก?
2. LCB Mode B: รายการ `ไม่แบ่ง` ครบทั้งหมดคืออะไรบ้าง?
3. AYU Mode B: 2 กลุ่มคนขับ 55% vs 60% แบ่งตามเกณฑ์อะไร?
4. BIGC: 1+ ค่าขนส่ง 400 บวกกับ rate สาขาหลัก หรือแทน?
5. AYU การันตี: pro-rate ได้ไหมถ้าประกาศแค่บางช่วง?
6. ประกันสังคม: ฐาน 9000 ถาวร หรือเปลี่ยนตามเงินเดือนจริง?
7. BIGC `รับรถ`: ถือเป็น event ไม่ใช่ billable ใช่ไหม?
8. BIGC `1DH`: คิดเงินอย่างไร?
9. คนขับข้ามไซต์: คิดค่าเที่ยวตามไซต์ของงาน หรือของคนขับ?
10. Line OA: มีอยู่แล้วหรือเริ่มใหม่?

### Action ถัดไป (priority)

1. ขยาย DailyJob schema ให้รองรับทั้ง 3 ไซต์ (เพิ่ม doc_no, fuel fields, container, fees, trip_type, leave_status)
2. เพิ่ม Master Data: employees (พร้อม employee_contract สำหรับ pay_mode), vehicles, customers
3. สร้าง import script อ่านจาก `Daily.xlsx` → SQLite (เริ่มจาก AYU แล้วค่อย BIGC, LCB)
4. ทำหน้า Dispatch เริ่มต้น (ถ้าต่อเนื่องได้ในรอบนี้)
5. รอผู้ใช้ส่งตาราง BIGC branch rates → สร้าง import script

---

## 2026-04-22 (Session Summary #9 - Answers + Schema Direction)

### ผู้ใช้เลือก: ทาง A (ขยายโครงให้เต็ม + Master Data ก่อน import)

### คำตอบคำถามรอบที่แล้ว

**กลุ่ม A (Payroll):**
1. LCB Mode A: หักรายวัน **แยก** = `9240/30` + `3000/30` (ไม่รวมเป็นก้อนเดียว)
2. LCB Mode B รายการ "ไม่แบ่ง": แค่ที่นึกออก (ค่าเสียเวลา, ค่าค้างคืน) — **ทำ flexible option** ให้ configurable ไม่ fix ใน schema
3. AYU Mode B: 55%/60% **ตามตกลงราย ๆ ต่อคน** — flexible ต่อ contract
4. AYU การันตี: **เต็มเดือน** — ถ้าคนขับทำงานไม่ครบ/ลา หักเฉลี่ยเป็นวันๆไปจากยอดการันตี

**กลุ่ม B (Billing BIGC):**
5. BIGC 1+: ค่าขนส่งลูกค้า = `rate สาขาไกลสุด + (400 × N)` ✓ (บวก ไม่ใช่แทน)
6. BIGC 1DH: **คิดเหมือนสาขาเดี่ยว** (ใช้ rate สาขาของปลายทาง)
7. BIGC รับรถ: **ไม่เกี่ยวข้อมูล billing/payroll** — เป็น event บันทึกว่าเริ่มขับรถคันนั้นเมื่อไหร่ ไว้ดูย้อนหลังได้

**กลุ่ม C (Architecture):**
8. Cross-site driver: **ตามไซต์คนขับ** — แต่ช่วงแรกค่าเที่ยวอาจต้อง**กรอกเอง** (เพราะข้อมูล cross-site เยอะ ไม่ fix ได้ทันที)
9. Permission: **ทุกคนเห็นทุกไซต์** — ต่างจาก Google Sheet (คน 2 คน filter ไม่ทับกัน) เพราะ DB ไม่มีปัญหานั้น
10. Line OA: **ยังไม่มี** — ปัจจุบันใช้ Line กลุ่มที่ชวนคนขับทั้งหมด (งาน + รูป + ปัญหา + โอนเงิน + แจ้งซ่อมปนกัน) ลูกค้าแต่ละเจ้าแยกกลุ่ม Line ตอนนี้เยอะมากๆแล้ว → **ยังไม่เร่งทำ Line integration** ใช้ copy-paste ไปก่อน

### Design Principles ที่ได้จากคำตอบ

1. **Flexible over fixed**: AYU share rate, LCB "ไม่แบ่ง" items → เก็บเป็น JSON/config ต่อ contract ไม่ hard-code
2. **Guarantee = monthly ceiling, prorate by absence**: การันตีเต็มเดือน หักตามวันลา/ไม่มาทำงาน
3. **Cross-site = driver's home site wins**: ตอนคำนวณ payroll ใช้ไซต์คนขับ ไม่ใช่ไซต์งาน
4. **Driver fee in cross-site = manual entry first**: ให้ช่องกรอกได้เสมอ อย่าบังคับ formula
5. **All users see all sites**: ไม่แยก permission ตามไซต์ — filter UI เท่านั้น
6. **No Line OA now**: ปุ่ม "แจ้งคนขับ" = copy message → paste ไป Line group

### สิ่งที่ต้องทำในรอบถัดไป (Phase 1.1 กำลังเริ่ม)

1. ขยาย DailyJob + สร้างตารางเสริมทั้งหมด (employees, employee_contracts, vehicles, customers, leave_records, accident_cases, accident_installments, driver_deposits, pay_cycles, daily_job_fees, bigc_branches)
2. Seed `pay_cycles` ด้วยกฎ 3 ไซต์ (AYU 26-25 จ่ายสิ้นเดือน, BIGC 1-end จ่าย 1 ถัดไป, LCB 16-15 จ่าย 1 ถัดไป)
3. สร้างหน้า Master Data CRUD (employees, vehicles, customers)
4. ปรับ DailyJob form ให้ใช้ dropdown (driver/vehicle/customer) แทนพิมพ์
5. ยังคงให้ start.bat ใช้งานได้

---

## 2026-04-22 (Session Summary #10 - Q&A + 2-Track Plan)

### คำถาม-ตอบเพิ่มเติมจากผู้ใช้

1. **รหัส Employee/Customer** → auto-gen ถ้าเว้นว่าง (E0001, C0001) พิมพ์เองก็ได้ — **ทำแล้ว**
2. **ค้นหาชื่ออย่างเดียว** → ใช้ได้ substring match ข้าม full_name + nickname + code — **ยืนยัน**
3. **วันเริ่ม-สิ้นสุดรถ** → ตอนนี้เป็นแค่ข้อมูลอ้างอิง ไม่ผูกกับ DP/ค่าเสื่อม/บัญชี Asset Register เก็บไว้ **Phase 2 Maintenance & Accounting** ต้องเพิ่ม: purchase_price, down_payment, monthly_installment, installment_months, finance_company, interest_rate, depreciation_method, book_value, salvage_value, disposal_date, sale_price
4. **Billing Profile อ้างอิง** = text pointer ไปที่ `docs/CUSTOMER_BILLING_PROFILES.md` (เช่น `bigc_standard`, `lcb_export_standard`) ภายหลังเปลี่ยนเป็น FK dropdown
5. **Raw name → auto-create master?** ไม่ทำ auto (อันตราย พิมพ์ผิด = คนซ้ำ) — ทำเป็น workflow: daily list โชว์ ⚠️ เมื่อ driver_id=null + ปุ่ม "ลิงก์/สร้าง master" → Phase 1.1.5
6. **ภงด 53** แก้ไขทีหลังได้ เป็น 1% ของค่าขนส่ง — ใส่ helper text แล้ว อนาคต auto-calc ตอน export
7. **น้ำมัน** ย้ายเป็น **FuelTxn (table แยก)** → import จาก Excel fuel เดิมได้เลย: vehicle_id, driver_id (nullable), txn_date, liter, amount, station, mile_snapshot (nullable), fill_type, daily_job_id (link ทีหลัง). Field น้ำมันใน daily_form จะถูกย้ายออกเมื่อ /fuel UI เสร็จ
8. **ช่วงเปลี่ยนถ่าย Excel + ระบบ คู่กัน** = 3 phases: Import-only → Dual-entry → System-only
9. **🌟 Petty Cash ก่อน** (ผู้ใช้เสนอ) — ตกลงทำ 2-Track parallel (ดูแผนด้านล่าง)
10. **Context update** — ยืนยันยังทำต่อเนื่องทุก turn ผ่าน Cursor rule

### การตัดสินใจแผนใหม่: 2-Track Parallel

**Track A (USE-NOW) — Petty Cash Quick Win** → ให้แอดมินหยุดใช้ Excel เร็วสุด
- A1 UI กรอกโอนเงิน (ใคร / จำนวน / เรื่อง / หักคนขับไหม)
- A2 Parser memo ไทย (ชื่อ + รายละเอียด + จำนวน + flag หัก)
- A3 รายการรอหักแยกตามคนขับ (ป้อนเข้า payroll ทีหลัง)
- A4 Import Excel สดย่อยเก่าย้อนหลัง → ตารางเดียวกัน
- เป้า: แอดมินใช้งานจริงภายใน 1 สัปดาห์

**Track B (FOUNDATION) — Daily Import + Master** → เดินต่อช้ากว่า แต่สำคัญ
- B1 Import AYU sheet (ง่ายสุด)
- B2 Import BIGC (ระดับกลาง)
- B3 Import LCB (ซับซ้อนที่สุด — ตู้ container)
- B4 เชื่อม petty_cash deductions → payroll module
- เป้า: payroll รอบแรกออกจากระบบ (1-2 เดือนถัดไป)

ทั้งสอง track ข้อมูลลง `app.db` เดียวกัน → ไม่เสียงาน เวลา Track B ตามมา

### โค้ดที่อัพเดทรอบนี้

- `main.py`: เพิ่ม `_gen_next_code()` helper, ทำให้ code ของ Employee/Customer optional
- `employee_form.html`, `customer_form.html`: รหัสเป็น optional + hint
- `daily_form.html`: helper 1% สำหรับ ภงด 53 + หมายเหตุน้ำมัน "จะมีหน้า /fuel แยก"

### สิ่งที่ผู้ใช้ฝากไว้ก่อนนอน

- โหวต **Track B = ทำ Import Daily** เป็นทางหลัก แต่เสนอให้แทรก **Track A Petty Cash** ก่อน (เพราะแอดมินกดดัน)
- เลือก: พรุ่งนี้ทำ Track A ก่อน Track B

---

## 2026-04-23 (Session Summary #11 — Track A Started)

### เริ่ม Track A: Petty Cash (สดย่อย) — A1/A2/A5 เสร็จ

**Excel audit:** ตรวจไฟล์ `Salary/AYU/สดย่อยวังน้อย.xlsx` — 25 คอลัมน์, รายเดือน 1 sheet,
คอลัมน์ key = **"พขร.เบิก หัก เงินเดือน"** เชื่อม payroll ตรง ๆ

**A1 ทำแล้ว — ตาราง `PettyCashTxn`** (ใน `app/models.py`):
- core: txn_date, site_code, direction(in/out), amount, category, memo
- people: requester_raw + driver_id FK (nullable)
- payroll hook: deduct_from_driver + deduct_amount + deduction_status + pay_cycle_tag
- links: linked_vehicle_id, linked_vehicle_plate_raw, linked_daily_job_id
- lifecycle: status (draft/posted/locked), source (manual/import)
- parser: parsed_confidence + parsed_payload_json (รอ A3)
- เพิ่ม enums: PETTY_DIRECTIONS, PETTY_CATEGORIES (14 หมวด), DEDUCTION_STATUS, PETTY_TXN_STATUS
- **bump schema v2 → v3** + เปลี่ยน `init_db` ให้ drop/recreate เมื่อ version mismatch (dev mode)

**A2 ทำแล้ว — UI CRUD** (`/petty-cash`):
- list หน้าหลัก พร้อมฟิลเตอร์ 6 มิติ (site, วันที่ from/to, คนขับ, หมวด, เฉพาะหัก)
- card สรุป 3 ก้อน: จ่ายออก / เข้ามา / รอหัก
- form: new + edit (ใช้ template เดียวกัน) + lock guard (locked = แก้ไม่ได้)
- delete with confirm

**A5 ทำแล้ว — หน้า `/petty-cash/pending`**:
- สรุปรอหักต่อคนขับ (card ต่อคน)
- warning box สำหรับรายการที่ไม่มี driver_id
- filter ตาม cycle + site

**Helper `_cycle_tag_for_site()`**: คำนวณรอบ YYYY-MM อัตโนมัติตามไซต์ (AYU 26→25, BIGC 1→end, LCB 16→15)

**Navigation:** เพิ่ม tab "สดย่อย" + "รอหักคนขับ" ใน `base.html`

**Smoke test ผ่าน:** seed 1 คน + 3 txn (hard-coded BIGC) → list แสดง, pending แสดงยอดรวมต่อคนขับ, edit form ดึง cycle tag ถูก (2026-02 สำหรับ BIGC 2026-02-15)

**ทำเอกสาร:** `docs/PETTY_CASH_SPEC.md` สรุป Excel mapping + schema + category rules + cycle tag logic

### สิ่งที่ยังเหลือใน Track A (พรุ่งนี้ต่อ)

- A3 Parser memo ไทย (regex keyword → category, extract driver/plate)
- A4 Import Excel เก่า (สคริปต์ `tools/import_petty_cash.py` อ่าน 3 ไฟล์ `สดย่อยวังน้อย.xlsx`)
- A6 Payroll lock hook (เมื่อปิดรอบ → status=locked)

### คำถามค้างให้ผู้ใช้ตอบ (ดูใน PETTY_CASH_SPEC.md §9)

- ปุ่ม "ปิดรอบ" อยู่ payroll หรือ petty?
- ให้แอดมินเพิ่มหมวดเองได้ไหม?
- รายการ "รอ/ทอน" ที่ค้างใน Excel track แยกหรือใส่ note?

---

## 2026-04-24 (Session Summary #12 — Track A: Q&A round 2 + Historical Import)

ผู้ใช้ตอบคำถามค้างทั้งหมด + ขอ import ข้อมูล 5 ปีย้อนหลัง → ทำทั้งหมดในเซสชันนี้

### 1. คำตอบการออกแบบ (จากผู้ใช้)

| Q | คำตอบ | สถานะ |
|---|---|---|
| ปุ่ม "ปิดรอบ" | อยู่หน้า Payroll (ไม่ใช่ petty) | บันทึก spec, ยังไม่ build |
| เพิ่มหมวดเอง | ทำเป็น 2-tier (system / custom) | บันทึก spec, ยังไม่ build |
| "รอ/ทอน" column | ต้อง track แยก → เพิ่ม 3 field | **ทำแล้ว** |
| เบิกข้ามรอบ | default auto + ปุ่ม override (ไม่เพิ่มภาระ admin) | **ทำแล้ว** |
| 5 ปี historical import | ทำเลย | **ทำแล้ว** |

### 2. Schema v4 — เพิ่ม pending clearance fields

ใน `PettyCashTxn`:
- `pending_amount: float` — ยอดค้าง (รอใบเสร็จ/ทอน)
- `pending_note: str` — คำอธิบาย
- `pending_cleared_at: Optional[date]` — null = ยังค้าง

บัมพ์ `SCHEMA_VERSION=3 → 4`; init_db มี auto drop/recreate logic ครอบอยู่แล้ว

### 3. UX ใหม่ (Cycle Override)

**Form `/petty-cash/new|edit`**:
- ช่อง `pay_cycle_tag` + 3 ปุ่มช่วย: `[auto]` `[+1 เดือน]` + พิมพ์เอง
- JS fetch `/api/cycle-tag?site=X&d=YYYY-MM-DD` → แนะนำ auto
- แสดง hint สีเหลืองถ้า override ไม่ตรงกับ auto

**List `/petty-cash`**:
- Badge "ย้ายจาก 2026-03" ถ้า override
- Badge "รอเคลียร์ NNN" ถ้ามี pending_amount > 0 ยังไม่เคลียร์

**หน้าใหม่ `/petty-cash/clearance`**:
- list รายการค้างใบเสร็จ/ทอน
- highlight แถวที่ค้างเกิน 7 วัน (สีเหลือง) / 14 วัน (สีแดง)
- ปุ่ม "เคลียร์แล้ว" (ตั้ง `pending_cleared_at = today`)
- เพิ่ม tab ใน nav

### 4. Historical Import (`tools/import_petty_cash.py`)

**ค้นพบสำคัญ:** ไฟล์ทั้ง 3 folder (`Salary/{AYU,BigC,LCB}/สดย่อยวังน้อย.xlsx`) เป็น**ก๊อปปี้ของไฟล์เดียวกัน**
(47,054/47,484 ≈ 99.1% ของ unique records ซ้ำทั้ง 3 ไฟล์)

→ ระบบจึงเลือก file ที่ **mtime ล่าสุด** เป็น canonical แล้ว import ไฟล์เดียว, ตั้ง `site_code=""` (mixed/unassigned)

**ผลรัน:**
```
Sheets scanned:   80
Rows imported:    50,753
Date range:       2019-12-14 → 2026-06-14 (6.5 ปี)
With deduction:   17,458 (34.4%)
With pending:     312
Plate extracted:  15,705 (30.9%)
Total OUT:        313,021,880 THB
Pending deducts:  22,141,100 THB

หมวดอัตโนมัติ (top 5):
  driver_advance  28.1%
  other           21.7%
  toll            18.8%
  repair           9.2%
  salary_partial   7.8%
```

Parser ใหม่:
- memo keyword → category (อุบัติเหตุ/เคลม → `accident`, ทางด่วน → `toll`, น้ำมัน → `fuel`, ฯลฯ)
- fallback ถ้าหัก > 0 และ memo ไม่ชัด → `driver_advance`
- regex แยก plate number ออกจาก memo
- clamp year 2015-2030 (ทิ้ง typo เช่น "30/1/33" ที่กลายเป็น 1933)

### 5. Next — รอตัดสินใจจากผู้ใช้

- **A-Site-Assigner (ใหม่):** สคริปต์ match `requester_raw` → `Employee.full_name` → auto ตั้ง `driver_id` + `site_code`
  ต้องรอให้ผู้ใช้ seed ข้อมูลพนักงานก่อน (หน้า `/employees` หรือ import master)
- **A6 Payroll lock hook** — ทำตอนเริ่ม Payroll module
- **B (FuelTxn + Daily import)** — track 2 ต่อไป

### 6. ไฟล์ที่แตะในเซสชันนี้

- `app/models.py` — เพิ่ม 3 field ใน PettyCashTxn
- `app/main.py` — SCHEMA_VERSION=4, route `/petty-cash/clearance`, API `/api/cycle-tag`, save handler รับ pending fields
- `app/templates/base.html` — เพิ่ม tab "รอเคลียร์"
- `app/templates/petty_form.html` — section รอเคลียร์ + JS cycle helper
- `app/templates/petty_list.html` — badge ย้ายรอบ + badge pending
- `app/templates/petty_clearance.html` — **NEW**
- `TransportRateCalculator/docs/PETTY_CASH_SPEC.md` — §8-11 update
- `tools/import_petty_cash.py` — **NEW** (parser + canonical picker + wipe/reimport)
- `tools/petty_stats.py` — **NEW** (sanity check tool)
- `tools/petty_dup_check.py` — **NEW** (ค้นพบ duplicate issue)

---

## 2026-04-08 (Session Summary #13)

### Context
หลัง import 50,753 แถว ผู้ใช้รายงาน:
1. **UI กระตุก/ช้า** เวลาเปิด `/petty-cash` — คนขับหลายคนลาออกไปแล้ว ไม่จำเป็นต้องมีประวัติ 6.5 ปี
2. กลัว task ที่ยังไม่ทำจะหลุดจากความจำ — ขอ reassurance
3. ขอ UX: `linked_daily_job_id` ควรมี "suggestion" แสดง Job ที่น่าจะใช่

### สิ่งที่ทำในรอบนี้

**1. Trim historical data** (`tools/import_petty_cash.py`)
- เพิ่ม flag `--from-date YYYY-MM-DD` (default `2026-02-01`)
- รัน `--wipe-prior --from-date 2026-02-01` → เหลือ **1,366 rows** (จาก 50,753)
- รันใหม่ด้วย cutoff อื่นเมื่อไรก็ได้

**2. Daily Job Suggester** (`/api/daily-jobs/suggest`)
- Input: `d`, `driver_id`, `driver_name`, `plate`, `site`, `window=3`, `limit=15`
- Scoring: driver_id +3, ชื่อ +2, ทะเบียน +2, ไซต์ +1, ใกล้วัน +0.5
- ภายใน `petty_form.html` — ปุ่ม "🔍 แนะนำ Job" เปิด panel แสดงรายการ, คลิกเพื่อกรอก ID
- ได้ผลเต็มรูปแบบเมื่อ Track B (import Daily) เสร็จ — ตอนนี้ยังไม่มี DailyJob ใน db

**3. Pagination /petty-cash** (100 rows/page, ตั้งค่าได้ `per_page`)
- COUNT/SUM ทำฝั่ง SQL (ไม่โหลดทุกแถวมา aggregate ใน Python)
- รักษา filter state ข้ามหน้า
- Header แสดง "หน้า X/Y"

### การตอบคำถามผู้ใช้

**Q: "ที่ยังไม่ทำ จะจำได้ไหม?"**
→ ได้ — pending items อยู่ใน 3 ไฟล์ (`NEXT_ACTION_PLAN.md` + `CONTEXT_LOG.md` + `PETTY_CASH_SPEC.md`) และ Cursor rule `.cursor/rules/project-yk-context.mdc` บังคับให้ agent เช็คก่อนเริ่มเซสชันทุกครั้ง
→ เหลือหลัก: A6 (Payroll lock), A10 (Site Assigner), B1-B7 (Daily import), 1.1.5 (Leaves/Accidents/Deposits UI), 1.4 (Dispatch)

### Next options
- [B] Track B (Daily import) — เริ่ม B1 `FuelTxn` table + import AYU Daily sheet Feb 2026
- [A10] Site-Assigner — ต้อง seed Employee master ก่อน (ผู้ใช้ต้องใส่ชื่อคนขับ)
- [1.1.5] UI ที่ขาด: `/leaves`, `/accidents`, `/deposits`, `/pay-cycles`
- [ทดสอบ] ผู้ใช้รัน `start.bat` ลอง UI ที่ทำในรอบนี้ก่อนค่อยเลือก

### ไฟล์ที่แตะในเซสชันนี้
- `tools/import_petty_cash.py` — เพิ่ม `--from-date`
- `app/main.py` — `/api/daily-jobs/suggest` + pagination ใน `/petty-cash`
- `app/templates/petty_form.html` — UI suggester panel + JS fetcher
- `app/templates/petty_list.html` — pagination controls

---

## 2026-04-08 (Session Summary #14) — Track B: Daily Import

### Context
ผู้ใช้สั่งลุยต่อ Track B — ผู้ใช้ยืนยันให้ใช้ `ProjectYK_System/Daily.xlsx` ที่เคยให้ไว้

### ผล
- **Schema v5** เพิ่มตาราง `FuelTxn` + 3 fields (pickup_location, store_code, truck_type_raw) ใน DailyJob
- **`tools/import_daily.py`** — one script รองรับทั้ง 3 sheet (AYU/BIGC/LCB)
- Import สำเร็จ: **DailyJob 1,550 / DailyJobFee 1,215 / FuelTxn 533**
  - AYU: 592 rows (406 real job + 173 idle + 13 leave)
  - BIGC: 373 rows (219 real + 145 placeholder + 9 leave)
  - LCB: 585 rows (402 real + 154 idle + 37 leave + 1,215 fee breakdown: lift/yard/shore/port/special/clean)
- **Cross-check:** AYU ค่าขนส่งรวม 1,081,270 ตรงเป๊ะกับ Excel R1 = 1,081,269.85 ✅
- **UI `/fuel`** — list/new/edit/delete + 6 filters + pagination (100/page) + 3 summary cards
- **UI `/daily`** — อัพเกรดเป็น pagination + 6 filters + 3 summary cards
- Daily list แสดง badge สถานะ (idle/placeholder/leave) พร้อมสีพื้นหลังแยก

### Decision points
- **Placeholder rows เก็บไว้** (ไม่ skip) เพื่อเป็น attendance trail — ใช้ `status_code` = `idle` / `placeholder` / `leave` แยก
- **LCB Status column** (MOL, KLND, DHL, KAO, WHALE, EAL, SDS, Nippon, NHL, KN, KTL) ถูกเก็บเป็น `status_code` ตรงๆ — ถือเป็น customer_code ชั่วคราว จนกว่าจะทำ Customer master
- **Schema drop & recreate** ระหว่าง v4→v5 ส่งผลให้ petty cash หาย → re-import เรียบร้อย (1,366 rows กลับคืน)
- **Fuel duplicated** — ตอนนี้ fuel เก็บทั้งใน DailyJob (liter/amount/mile) และ FuelTxn เพื่อให้ backward-compatible; อนาคตย้าย fuel ใน DailyJob ออกเมื่อ UI ใหม่พร้อม

### Next options (เหลือสำหรับรอบถัดไป)
- [A10/B7] **Promote raw → master**: seed Employee + Vehicle จากข้อมูลที่ import แล้ว auto-match
  - มี driver top 10: สมัย, ติ๋ว, เรวัตร, สมประสงค์, ธนวัฒน์, วัชร์นล, ทองสุข, เกศศักดิ์, ณัชพน, สันติพงษ์
  - มี plate top 10: 71-0567, 71-0557, 71-5042, 71-0560, 71-8002, 71-3899, 71-8001, 71-8003, 71-0556, 71-0564
- [Dispatch 1.4] หน้าสร้างงาน + จับคู่รถ/คนขับ
- [Payroll 1.5] รันรอบจ่ายเงินเดือนครั้งแรก
- [UI เสริม] `/leaves`, `/accidents`, `/deposits`, `/pay-cycles`

### ไฟล์ที่แตะในเซสชันนี้
- `app/models.py` — เพิ่ม `FuelTxn` + 3 fields ใน DailyJob
- `app/main.py` — SCHEMA_VERSION=5, routes `/fuel*`, pagination + filters ใน `/daily`
- `app/templates/base.html` — เพิ่ม nav "น้ำมัน"
- `app/templates/daily_list.html` — pagination + 6 filters + badges
- `app/templates/fuel_list.html` — NEW
- `app/templates/fuel_form.html` — NEW
- `tools/import_daily.py` — NEW (3-in-1 importer)
- `tools/daily_stats.py` — NEW (sanity check)
- `tools/_daily_inspect.py` — NEW (ad-hoc sheet inspector)

---

## 2026-04-08 (Session Summary #15) — Caltex Fuel Import (LCB authoritative source)

### Context
ผู้ใช้แจ้ง: "ให้ฉันส่งไฟล์น้ำมันที่แอดมินบันทึกให้ด้วยไหม" แล้วชี้ไปโฟลเดอร์ `Fuel/` ซึ่งมี:
- `น้ำมันคาลเท็ก.xlsx` — statement เครดิตจาก Caltex (4 sheets: Dec 2025, Jan/Feb/Mar 2026)
- `fill_fuel_daily.py` — สคริปต์เดิมที่ใช้ match Caltex → Daily (AE/AF/AG = mile/liter/price)
- CSV audit files (shifted/unmatched/value_mismatch)

**ความเข้าใจใหม่:** Caltex คือ **ข้อมูลจริงจากปั๊ม** (ไมล์จริง, ลิตรจริง, ราคาปั๊มจริง, เครดิตคงเหลือ) ขณะที่ฟิลด์ fuel ใน `Daily.xlsx` เป็นผล merge จากสคริปต์เดิมเท่านั้น → Caltex เป็น source of truth สำหรับ LCB

### ผล
- **`tools/import_caltex_fuel.py`** — ใหม่
  - รับ 4 sheets, skip "ยกยอด"/"ส่วนต่าง"/placeholder rows
  - Normalize plate/driver + match DailyJob (±1 day shift, driver substring)
  - Import เป็น `FuelTxn(source='caltex', site_code='LCB')` พร้อม station + pump_price + rate
  - Audit: `Fuel/caltex_import_unmatched.csv` + `Fuel/caltex_import_shifted.csv`
- รันจริง (`--wipe-prior --also-wipe-import-daily --from-date 2026-02-01`):
  - Wiped 298 LCB FuelTxn ที่มาจาก Daily (ลบซ้ำซ้อน)
  - Imported **553 Caltex rows** (36,261.71 L / ฿1,089,516.40)
  - **Matched DailyJob: 309 (55.9%)** — 268 exact + 41 shifted
  - **Unmatched 244:** ส่วนใหญ่คือ (ก) วันที่อยู่นอกช่วง DailyJob Feb16–Mar15 (Caltex มี Feb1–Mar23) (ข) ทะเบียน บษ2681 = "พ่อบ้าน" ไม่ใช่คนขับ
- **UI `/fuel`** — เพิ่ม 2 filter (source: caltex/import_daily/manual, linked: yes/no) + source badge ในตาราง + badge "ยังไม่เชื่อม" สำหรับ daily_job_id=null

### Decision points
- **Caltex เฉพาะ LCB:** confirmed จากรายชื่อคนขับทุกคนเป็น LCB drivers (เนื้อ, ณัฐวัฒน์, อภิชาติ, พชร, สันติพงษ์ ฯลฯ)
- **Daily-sourced LCB fuel ถูก wipe:** เพราะ Caltex authoritative กว่า — ยังไม่ลบใน DailyJob.liter/amount/mile (เก็บไว้ backward-compatible)
- **Matcher ดีกว่าสคริปต์เดิม:** ลองทั้ง `d-1`, `d`, `d+1` (เดิมแค่ `d`, `d+1`) — match เพิ่มได้ ~15 rows
- **Housekeeper vehicle บษ2681:** ไม่ถือว่า daily job, เก็บไว้ใน FuelTxn (site=LCB) เพื่อบัญชี แต่ daily_job_id=null ถาวร

### Next options
- [C5] ลิงก์ manual: UI ให้ admin review caltex_import_unmatched แล้วลาก-drop link → DailyJob / หรือ mark "non-driver"
- [A10/B7] Promote driver_raw_name + plate_no_raw → Employee/Vehicle master (รวมถึง Caltex rows)
- [Dispatch 1.4] หน้าสร้างงาน
- [Payroll 1.5] LCB pay run ใช้ Caltex เป็น fuel cost authoritative

### ไฟล์ที่แตะในเซสชันนี้
- `tools/import_caltex_fuel.py` — NEW (Caltex statement → FuelTxn)
- `app/main.py` — เพิ่ม `source`/`linked` filter ใน `/fuel`
- `app/templates/fuel_list.html` — source badge + filter + linked-unlinked badge
- `Fuel/caltex_import_unmatched.csv` / `caltex_import_shifted.csv` — generated

---

## 2026-04-08 (Session Summary #16) — A10/B7: Promote Raw → Master

### Context
แอดมินยังไม่ได้อัพเดทน้ำมัน user สั่ง "ลุยต่อได้เลย" → เลือกลุย **A10/B7** เพราะปลดล็อก Payroll/Dispatch/Suggester ได้ทันที (มี raw driver/plate สะสมอยู่แล้ว 3,637 refs)

### ผล
- **`app/services/promote.py`** — โมดูลรวมตรรกะทั้งหมด
  - `normalize_name/normalize_plate` ตัด prefix นาย/นาง/น.ส./พี่/พ่อบ้าน, ช่องว่าง, วงเล็บ
  - `_cluster_drivers` ใช้ **union-find** รวม variants ที่เป็น substring กัน (เช่น "สมัย" + "นายสมัย ...(BIG C)" + "สมัย อยุธยา" → 1 cluster)
  - Site-majority guard: ไม่ merge ถ้า sites ชัดเจนคนละฝั่ง
  - Infer `home_site_code` จาก majority (ละทิ้ง "?")
  - Default `pay_mode`: AYU→ayu_trip / BIGC→bigc_monthly / LCB→lcb_monthly
  - `is_confident`: total≥3, มี home_site_code, และต้องไม่ใช่ PettyCash-only (ฟ้อง owner/admin ไม่ใช่คนขับ)
  - `promote_drivers/vehicles` สร้าง Employee/Vehicle + backfill driver_id/vehicle_id ใน DailyJob/PettyCashTxn/FuelTxn
- **`/admin/promote`** — UI 2 tabs (drivers/plates)
  - แสดง variants, site distribution, sources (DailyJob:52, PettyCash:21, Fuel:13)
  - Checkbox ติ๊กไว้เฉพาะ confident (amber row สำหรับ unconfident)
  - ฟอร์มแก้ full_name, nickname, home_site, pay_mode ก่อนกด create
  - ปุ่ม "เลือกทั้งหมด"/"ล้างเลือก"/"สร้าง + ลิงก์ข้อมูลเก่า"
- **รันครั้งแรก (auto-confident only):**
  - สร้าง **44 Employees + 69 Vehicles**
  - Backfilled: DailyJob 1,443 / FuelTxn 788 (ทั้งหมด) / PettyCashTxn 802
  - เหลือ unfilled: DailyJob 107 (เป็น empty/ว่าง placeholder หมด), PettyCash 564 (เป็น พ่อ/เมย์/ศราวุธ/ช่างน้อย ฯลฯ = owner/admin ไม่ใช่คนขับ)

### Decision points
- **Owner/admin (พ่อ, เมย์, ศราวุธ) ไม่ auto-promote** — รอ user ติ๊กเองใน UI ถ้าต้องการ (อาจจะสร้างเป็น non-driver employee type ในอนาคต)
- **Union-find over greedy loop** — กันปัญหา "สมัย" merge กับ "สมัยbigc" แล้ว break ทิ้ง "สมัยอยุธยา" ไว้เป็น orphan
- **Site-conflict guard** — ถ้า "สมัย" เจอที่ BIGC อย่างเดียว และมี variant อื่นเจอที่ AYU อย่างเดียว = ไม่ merge (น่าจะคนละคน)
- **Display name polish** — ตัด "(BIG C)", "อยุธยา", "แหลมฉบัง" ออกจาก display เพราะเป็น site tag ที่แอดมินใส่กันชื่อซ้ำ

### Next options
- [E] **Payroll run แรก** — ตอนนี้ Employee + Vehicle + DailyJob + FuelTxn มีครบแล้ว พอคำนวณ AYU/BIGC/LCB เงินเดือนรอบ Feb-Mar 2026 ได้
- [F] **Dispatch UI** (1.4) — สร้างหน้าคีย์งาน + จับคู่คนขับ/รถ
- [G] **Non-driver Employee type** — flag พ่อ/เมย์ เป็น role='admin' หรือ 'owner' แยกจากคนขับ
- [H] **Advanced merge** — ถ้า user เจอ "สมัย อยุธยา" แต่ระบบไม่ merge กับ "สมัย" (AYU/BIGC conflict), ให้ UI มีปุ่ม "merge manually"

### ไฟล์ที่แตะในเซสชันนี้
- `app/services/promote.py` — NEW (clustering + backfill)
- `app/services/__init__.py` — NEW (empty package marker)
- `app/main.py` — เพิ่ม routes `/admin/promote`, `/admin/promote/drivers`, `/admin/promote/vehicles`
- `app/templates/admin_promote.html` — NEW (2-tab UI)
- `app/templates/base.html` — เพิ่ม nav "สร้าง Master"
- `tools/_master_survey.py` — NEW (diagnostic script)

---

## 2026-04-08 (Session Summary #17 — Payroll MVP + Ops fixes)

### ประเด็นจากผู้ใช้ (3 เรื่อง)
1. **ชื่อคนขับซ้ำระหว่างไซต์** → แทนด้วยชื่อจริง + นามสกุล (เลือกจาก dropdown อยู่แล้ว ไม่ต้องพิมพ์เอง)
2. **สดย่อยมีคนที่ไม่ใช่คนขับ** (พ่อ, ออฟฟิส, ช่าง) — ต้องแยกออกจากคนขับเวลาทำ payroll
3. **start.bat ขึ้น Internal Server Error** `[Errno 10048] only one usage of each socket address` — port 8000 โดน PC Server (AnyDesk ของโปรแกรมเมอร์ที่จ้าง) ใช้อยู่

### สิ่งที่แก้/เพิ่มในเซสชันนี้

#### 1) Auto-detect free port
- `main.py::_find_free_port(start=8000, count=20)` ลอง bind 127.0.0.1 หา port ว่าง
- `main.py` รองรับ env `YK_PORT` (override ได้) + fallback พยายาม port ถัดไปถ้า bind fail
- `start.bat` query port จาก Python ก่อน uvicorn.run
- ทดสอบแล้ว: 8000/8001 โดนใช้ → app ขึ้นที่ **8002** อัตโนมัติ

#### 2) Additive schema migration (non-destructive)
- เลิกใช้ `drop_all + create_all` บน version mismatch (เสี่ยงล้างข้อมูล user)
- เพิ่ม `_ensure_column(table, col, type, default)` — ALTER TABLE ADD COLUMN IF NOT EXISTS แบบ SQLite
- `_apply_additive_migrations()` รันทุก startup safe re-run
- `SchemaInfo.version` แค่ stamp (ไม่ trigger drop)
- ทดสอบแล้ว: bump v5→v6 + ALTER TABLE ADD role → ข้อมูล Employee/Vehicle/DailyJob/ฯลฯ ทั้งหมดยังอยู่ครบ
- แก้ `tools/import_*.py` ให้เรียก `main.init_db()` แทน inline drop logic

#### 3) Employee.role field
- เพิ่ม `role: str = "driver"` ใน `Employee` model
- Choices: driver | office | owner | mechanic | guard | other
- UI `/admin/promote`:
  - Role dropdown ติดกับแต่ละ cluster (default suggest จาก `DriverCluster.suggested_role`)
  - PettyCash-only names → suggest `office` (หรือ `owner` ถ้าชื่อมี "พ่อ")
  - JS auto-switch pay_mode → `none` เมื่อ role != driver
- Placeholder ใน input ชื่อจริง: "เช่น สมัย สายศิลป์" (กระตุ้นให้พิมพ์เต็มชื่อ-นามสกุล)
- Payroll skip role != driver อัตโนมัติ

#### 4) Payroll MVP v1 (Phase 1.5 step 35)
- **Tables:** `PayRun`, `PayRunItem` (schema v6)
- **Service:** `app/services/payroll.py`
  - `compute_period(site, tag)`: BIGC 1→end of month, LCB 16→15, AYU 26→25
  - `compute_pay_cycle_tag(site, date)`: ใช้ร่วมกับ pay_cycle_tag ของ PettyCashTxn
  - `calc_one_employee(session, emp, start, end, tag) -> PayrollCalc` (dataclass)
  - `get_or_create_pay_run(site, tag)` + `compute_pay_run(pr, recompute=True)`
- **รองรับ pay_mode 5 แบบ:**
  - `bigc_monthly` — 9,000 base − (9000/30)×missed_days + Σ DailyJob.trip_fee_driver
  - `lcb_monthly` — 9,240 base + 3,000 care − (per/30)×missed + trip_fee
  - `lcb_mao` — revenue × 60% − Σ FuelTxn.amount
  - `ayu_trip` — trip_fee_total + guarantee_topup (ถ้า < การันตี × eligible_days/30)
  - `ayu_mao` — revenue × share_rate − fuel
  - `none` → skip (ออฟฟิส/พ่อ/ช่าง)
- **Deductions:**
  - `social_security` — 9000×5% = 450 ต่อเดือน, ลดตาม missed_days
  - `deposit_install` — 1,000/เดือน จนครบ 10,000
  - `accident_install` — sum AccidentInstallment.amount ใน tag นี้
  - `petty_cash_deduction` — sum PettyCashTxn (deduct_from_driver=True + pay_cycle_tag==tag + status=pending)
  - `fuel_cost_self` — สำหรับ *_mao เท่านั้น
- **Finalize lock** — PayRun.status=finalized + PettyCashTxn ที่ consume → deduction_status=deducted + status=locked

#### 5) UI `/payroll`
- `payroll_list.html` — สรุปรอบทั้งหมด (site, tag, period, count, gross, ded, net, status)
- `payroll_new.html` — เลือก site + tag (default = เดือนปัจจุบัน) + notes
- `payroll_detail.html` — ตาราง 21 คอลัมน์ per employee (days + 7 earnings + 6 deductions + net)
  - Recompute / Finalize / Delete buttons (ล็อกเมื่อ finalized)
- เพิ่มลิงก์ใน nav (emerald color)

### ผลลัพธ์ทดสอบ (Feb 2026)
- **BIGC 2026-02** (1/2 → 28/2): 9 drivers, gross 210k, ded 97k, net ~113k
- **LCB 2026-02** (16/1 → 15/2): 22 drivers, gross ~270k, ded ~29k, net ~242k (trip_fee=0 เพราะ DailyJob ยังว่างช่วง Jan ต้อง import เพิ่ม)
- **AYU 2026-02** (26/1 → 25/2): 13 drivers, gross ≈ 0, ded ~115k → net negative (แอดมินยังไม่กรอก trip_fee_driver จริง)

### ข้อจำกัดที่รู้ (สำหรับ v1.1)
- **BIGC fuel_rate_income (16฿/L residual)** ยังไม่คำนวณอัตโนมัติ — ต้อง map budgeted liters per DailyJob ก่อน
- **AYU_mao toll deduction** ยังไม่รวม PettyCashTxn category=toll แยก
- **LCB_mao fuel_cost** ใช้ FuelTxn.amount ตรง ๆ (ถูกแล้วถ้า driver_id linked ครบ)

### ไฟล์ที่แตะในเซสชันนี้
- `app/main.py` — `_find_free_port`, `_ensure_column`, `_apply_additive_migrations`, payroll routes
- `app/models.py` — `Employee.role`, `PayRun`, `PayRunItem`, `EMPLOYEE_ROLES`, `PAY_MODES` update
- `app/services/promote.py` — `DriverCluster.suggested_role`, role field in `promote_drivers()`
- `app/services/payroll.py` — NEW (calculation engine, ~380 lines)
- `app/start.bat` — auto-port detection via Python helper
- `app/templates/admin_promote.html` — role dropdown + placeholder + JS auto-switch
- `app/templates/base.html` — add /payroll nav link
- `app/templates/payroll_list.html` + `payroll_new.html` + `payroll_detail.html` — NEW
- `tools/import_caltex_fuel.py`, `tools/import_daily.py`, `tools/import_petty_cash.py` — use `main.init_db()`

### Next options
- [I] **Payroll v1.1** — BIGC fuel_rate_income + AYU toll deduction + cross-check Feb 2026 vs Excel
- [J] **Non-driver dashboard** — หน้าดูเฉพาะ role != driver (ใครเบิกเยอะ, refund, owner transfer)
- [K] **Payslip PDF / Diff report** — เปรียบเทียบ payroll กับ Excel `สดย่อยวังน้อย.xlsx` รอบเดียวกัน
- [L] **Dispatch UI (1.4)** — หน้าคีย์งานต้นน้ำ + Line notify


## Session #18 — Payroll v1.1 + port robustness (2026-04-08)

### Ops / startup
- Default port เปลี่ยน 8000 → **8010** (กันชน PC Server/AnyDesk ที่ถือ 8000 อยู่)
- `_find_free_port` ใช้ `SO_EXCLUSIVEADDRUSE` + `listen(1)` ให้ตรงกับที่ uvicorn ทำจริง
  (กัน false-positive: เดิม bind ผ่าน แต่ uvicorn ยัง 10048 เพราะตั้งค่า SO_EXCLUSIVEADDRUSE)
- main.py ใช้ threading.Timer เปิด browser อัตโนมัติ → ลบ for-loop ใน start.bat
  (ที่เดิมแตกเพราะ quoting: `from is not recognized`)
- `start.bat` สั้นลง ใช้แค่เรียก `main.py` อย่างเดียว

### Payroll v1.1
- **BIGC fuel_rate_income**: `(งบ DailyJob.fuel_liter − FuelTxn.liter ใช้จริง) × 16฿`
  note แสดงงบ/ใช้จริง/เหลือ เพื่อให้ผู้ใช้ตรวจทานได้
- **AYU toll deduction**: PettyCashTxn category=toll direction=out ถูกหักจาก ayu_mao
  + `_sum_petty_cash_deduction(exclude_toll=True)` กันหักซ้ำ
- **Drilldown view** `/payroll/{run_id}/employee/{emp_id}`:
  - สรุป 3 คอลัมน์ (รายได้/หัก/การทำงาน) พร้อม net ขนาดใหญ่
  - ตาราง DailyJob ของคนนั้นในรอบ (highlight แถวลา = amber)
  - ตาราง PettyCashTxn (highlight deduct = rose) + สถานะ pending/deducted/waived
  - ตาราง FuelTxn พร้อม badge แหล่งที่มา + link ไป DailyJob ถ้าเชื่อมแล้ว
  - print-friendly CSS → กด "พิมพ์สลิป" ได้เลย

### Data gap ที่พบจาก smoke test
- AYU: ยังไม่มี DailyJob Feb 2026 → gross 0, deduction -120k (ติดลบหมด)
- LCB: trip_fee ทั้งหมด 0 → ทุกคนได้แค่ base 9240+3000
- BIGC: fuel_liter งบ ไม่มีใน DailyJob → rebate = 0 (แต่สูตรทำงานแล้ว)

**Next:** import DailyJob ที่ขาด หรือใช้ drilldown เปิดดูคนขับ 1 คน → แก้ข้อมูลทีละคน

---

## 2026-04-08 (Session #19) ? BIGC Fuel Rate Option B + PayRunAdjust

### ??????????????????
- **Option B**: import per-trip ?????????????????????? BIGC ?????? summary-only
- **Budget pattern**: budget ??????? scale ??????? ? Nakhonphanom ??? 384L ????, Kham Ta Kla varies 343-359L. ? ???????? formula master, ?????????????????? admin ???????? ? ?? `DailyJob.fuel_liter`
- **Pay cycle BIGC**: ???????? = work month (???? "??????? 68" = ?.?.2568 ? tag 2025-12, ??? 1 ?.?.2569)
- **Driver matching**: ????????????????????+??????????, ????????? admin ???????

### ???????/??????
**Schema**
- `PayRunItem` ????? `fuel_budget_liter` / `fuel_consumed_liter` / `fuel_residual_liter` (audit)
- **`PayRunAdjust`** (new table) ? ???? `fuel_adjust_liter` + `fuel_rate_override_thb` ??? (run, emp) ? ?????? recompute

**Payroll calc (`services/payroll.py`)**
- ?? `max(0, ...)` ? rebate ????????
- ??? `PayRunAdjust.fuel_adjust_liter` ??????? residual ??????? 16
- ?????? `fuel_rate_override_thb` (manual hard-override)

**Importer: `tools/import_bigc_fuel_rate.py`** (new)
- parse `??????` + ???????? (14 columns)
- ?????? typo "????????"/"?????????" ?? footer + fuzzy match ???? 1-char edit distance
- upsert DailyJob + FuelTxn + record PayRunAdjust
- **???? conflict**: ?? FuelTxn source `import_daily`+`bigc_fuel_rate` ??? zero `DailyJob.fuel_liter` ??? BIGC ??????????????? import
- **Verification**: ABS DIFF 3 ???? = 0.66 ??? (pure float rounding)

**UI**
- `/payroll/{id}/employee/{id}`: ?????????? "? BIGC Fuel-Rate Audit" (budget / consumed / residual / rebate + admin adjust note)

### ??????? PayRun BIGC ??? import ????
- BIGC 2025-12: 9 drivers, gross 202,822 / net 189,772 (TOTAL DIFF 0.18)
- BIGC 2026-01: 9 drivers, gross 199,238 / net 186,188 (TOTAL DIFF 0.11)
- BIGC 2026-02: 9 drivers, gross 205,162 / net 129,842 (TOTAL DIFF 0.24)

### Known issues / gaps
- "???" (nickname driver) ?????????? Employee master ? unmatched ????????
- "???? ?????" (Dec 68) sheet footer residual_after = 0 ??? admin ????? 0 ??????????? ? ??????????????????????? (???????)
- Budget sum ????????? summary residual_before ? adjust ????????????????? audit ?????? ? ???????????????? parse ???????? main trip

### ?????????? (user ??????)
1. Maintenance/Tire module (????)
2. Promote "???" + other unmatched drivers


---

## 2026-04-08 (Session #20) — Maintenance Module Wave 1

### สิ่งที่ user สั่ง
- ขอเพิ่มระบบบันทึกซ่อมบำรุง / ยาง-ดอกยาง-ตำแหน่ง / แผน RM PM — scope **full** และ **ลุยต่อเลย**
- ยืนยันสมมติฐาน BIGC budget scale ตามจำนวนจุดส่ง (หลัก+พ่วง+พ่วง=100L vs หลักเดี่ยว=90L) → ถูกต้อง เก็บใน `DailyJob.fuel_liter`
- BIGC Option B: ยืนยัน — จะยังไม่ปล่อยให้แอดมินเทสจนกว่าจะสมบูรณ์ทั้งระบบ
- ยืนยันว่าไฟล์ Daily ใช้ชื่อจริง + นามสกุล; ไฟล์สดย่อยอาจไม่มีนามสกุล → ให้ admin แก้ได้
- ยืนยัน pay-cycle mapping: ชื่อเดือนในไฟล์ = เดือนทำงาน; โฟลเดอร์ = เดือนจ่าย (เช่น "ธันวาคม 68" อยู่ในโฟลเดอร์ `1.Jan` → tag `2026-01`)

### Schema v8 (เพิ่มใหม่ — additive migration เดิม)
- **Vendor** — ร้าน/อู่ (kinds: parts|tire|service|oil|insurance|other) auto-code `V0001`
- **Part** — อะไหล่ master + `is_tire` flag + `min_stock_qty` + `default_price` auto-update auto-code `P0001`
- **StockTxn** — in/out/adjust ผูก vendor/maint_record/petty_cash
- **MaintRecord** — ซ่อม/บริการ/ตรวจ/เปลี่ยนยาง/อุบัติเหตุ auto-code `M000001`
- **MaintPart** — line-items อะไหล่ที่ใช้ (ผูก tire_id ได้สำหรับ tire_change)
- **Tire** — lifecycle ยางแต่ละเส้น (brand/spec/serial/status/tread/retread_count)
- **TireEvent** — mount/unmount/rotate/inspect/retread/scrap
- **PmPlan** — PM|RM|inspection per-vehicle หรือ global interval_km/interval_days
- **ENUMs ล็อก:** MAINT_KINDS/MAINT_STATUS/MAINT_PAID_BY/PART_CATEGORIES/PART_UNITS/VENDOR_KINDS/TIRE_STATUS/TIRE_EVENT_TYPES/PM_KINDS
- **TIRE_POSITIONS_BY_KIND** — ตำแหน่งยางมาตรฐานต่อประเภทรถ (6W/10W/10WL/18W)

### UI Wave 1 (เสร็จแล้ว)
- `/maint` — Dashboard (cards: records/tires/PM/parts + cost by vehicle + recent 10)
- `/maint/records` — filter (วันที่/รถ/ประเภท/สถานะ) + summary cost
- `/maint/records/new` + `/maint/records/{id}` — CRUD + line-items แบบ inline
- `/maint/vendors` — เพิ่ม/ดู/นับจำนวนใช้
- `/maint/parts` — เพิ่ม/ดู + live stock + low-stock alert (bg-rose vs bg-emerald)
- `/maint/stock` — รับเข้า/เบิกออก/ปรับยอด + 100 รายการล่าสุด
- `/maint/tires` + `/maint/pm` — placeholder (Wave 2/3)

### Auto-logic สำคัญ
- MaintPart link Part master → สร้าง `StockTxn(direction='out')` อัตโนมัติ (maint_record_id FK)
- ลบ MaintPart → ลบ StockTxn ที่ match กันอัตโนมัติ
- StockTxn direction='in' + unit_price > 0 → อัปเดต `Part.default_price`
- เพิ่ม/ลบ line → recompute `MaintRecord.parts_cost` และ `total_cost` (= parts+labor+other)
- plate_raw free-text + resolve `vehicle_id` อัตโนมัติโดย match `Vehicle.plate_no`

### Smoke test ที่รัน
- 8 GET routes return 200
- POST vendor/part/maint_record ทั้ง create + edit ทำงานถูก (303 redirect)
- Add MaintPart 2 lines (master + ad-hoc) → parts_cost recompute 1,600 → 1,900 ✓
- Stock auto-deduct ตรวจผ่าน `/maint/parts` ✓
- test data ถูก clean หลังจากนั้นแล้ว (record M000001 ลบแล้ว)

### Files touched
- `ProjectYK_System/app/models.py` — +8 tables, +9 enum groups
- `ProjectYK_System/app/main.py` — `SCHEMA_VERSION=8`, +20 maint routes, +`_gen_code`/`_stock_map_for_parts` helpers
- `ProjectYK_System/app/templates/base.html` — nav link สี orange
- `ProjectYK_System/app/templates/maint_*.html` — 6 templates ใหม่

### Next
- **Wave 2 (Tire UI)** — mount/rotate/scrap + ตำแหน่งยาง (FL/FR/RLO/RLI/…)
- **Wave 3 (PM Plan UI)** — สร้างแผน + auto-due detection (km + days) + แจ้งเตือน
- หลังจาก wave 2-3 เสร็จ → กลับมาต่อ data gap + excel diff + dispatch UI
- User อาจจะต้องซื้อ Cursor Pro+ เนื่องจาก API ใช้เยอะ

---

## 2026-04-08 (Session #21) â€” Rate Book + Auto-learn Wave 1

### à¸ªà¸´à¹ˆà¸‡à¸—à¸µà¹ˆ user à¹€à¸ªà¸™à¸­ (à¹à¸™à¸§à¸„à¸´à¸”à¸«à¸¥à¸±à¸)
- à¸„à¸£à¸±à¹‰à¸‡à¹à¸£à¸ admin à¸à¸£à¸­à¸ â†’ à¸£à¸°à¸šà¸šà¸ˆà¸³ â†’ à¸„à¸£à¸±à¹‰à¸‡à¸•à¹ˆà¸­à¹„à¸›à¸—à¸µà¹ˆ pattern à¹€à¸”à¸´à¸¡ auto-fill
- à¸›à¸£à¸°à¸¢à¸¸à¸à¸•à¹Œà¸à¸±à¸šà¸—à¸¸à¸ rate: à¸„à¹ˆà¸²à¸‚à¸™à¸ªà¹ˆà¸‡ à¸„à¹ˆà¸²à¹€à¸—à¸µà¹ˆà¸¢à¸§ à¸‡à¸šà¸™à¹‰à¸³à¸¡à¸±à¸™ à¸„à¹ˆà¸²à¸—à¸²à¸‡à¸”à¹ˆà¸§à¸™
- à¸•à¹‰à¸­à¸‡à¸£à¸­à¸‡à¸£à¸±à¸š wildcard **"any"** â€” à¹€à¸Šà¹ˆà¸™ LCB loading=CNC origin=* destination=* à¹ƒà¸«à¹‰à¹€à¸£à¸—à¹€à¸”à¸µà¸¢à¸§
- à¸•à¹‰à¸­à¸‡à¸£à¸­à¸‡à¸£à¸±à¸š "except" (à¸ˆà¸”à¹€à¸›à¹‡à¸™ annotation; à¸¢à¸±à¸‡à¹„à¸¡à¹ˆ enforce à¹€à¸•à¹‡à¸¡)
- à¸„à¹ˆà¸²à¹€à¸—à¸µà¹ˆà¸¢à¸§à¸œà¸¹à¸à¸•à¸²à¸¡à¸›à¸£à¸°à¹€à¸ à¸—à¸£à¸–à¸”à¹‰à¸§à¸¢ (6W/10W/trailer)

### Design à¸—à¸µà¹ˆà¹€à¸¥à¸·à¸­à¸
- **Scoring pattern match**: +10 exact / +1 wildcard Â· tiebreak priority+updated_at
- **auto_record on save**: hook à¹ƒà¸™ POST `/daily/new` + `/daily/{id}/edit`
- **manual pin**: admin à¸•à¸´à¹Šà¸à¸šà¹‡à¸­à¸à¸‹à¹Œ promote_to_manual â†’ priority=1 â†’ à¸Šà¸™à¸° auto
- **4 rate kinds à¹à¸£à¸**: `fuel_budget_liter`, `revenue_customer`, `trip_fee_driver`, `toll_fee`, `other` (extensible)

### Schema v9 â€” RateCard
- dims: site_code / customer_id / vehicle_kind / trip_type_code / origin / destination / pickup_location
- value: rate_value + rate_unit (THB/L)
- meta: priority / source(manual|auto|import) / use_count / last_used_at / last_seen_job_id
- period: effective_from / effective_to
- free-text: except_pattern (annotation only) / notes

### Files touched
- `models.py` â€” `RateCard` + `RATE_KINDS` + `RATE_UNIT_BY_KIND`
- `main.py` â€” `SCHEMA_VERSION=9`, helpers (`rate_find` / `rate_record` / `rate_record_from_daily`), 7 routes, auto-record hook à¹ƒà¸™ DailyJob POST
- `templates/rate_list.html` + `templates/rate_form.html`
- `templates/base.html` â€” nav link "à¹€à¸£à¸—à¸£à¸²à¸„à¸²" à¸ªà¸µ cyan

### Routes
- `GET  /rates` + filter (kind/site/source/q)
- `GET  /rates/new`, `/rates/{id}` â€” form
- `POST /rates/new`, `/rates/{id}` â€” create/update
- `POST /rates/{id}/delete` â€” delete
- `POST /rates/backfill` â€” one-shot scan DailyJob â†’ auto-create rules
- `GET  /api/rates/suggest?kind=X&site_code=Y&...` â€” JSON for HTMX (Wave 2)

### Results from backfill (scan 1,550 DailyJob rows)
- **1,167 unique patterns learned** in one click
  - 492 trip_fee_driver
  - 393 revenue_customer
  - 283 fuel_budget_liter (BIGC à¸‡à¸šà¸¥à¸´à¸•à¸£à¸•à¹ˆà¸­à¸ªà¸²à¸‚à¸²)

### Examples learned
| Site | origin â†’ dest | Loading | veh | kind | value | used |
|---|---|---|---|---|---|---|
| AYU | à¸šà¸²à¸‡à¸žà¸¥à¸µ à¸™à¸µà¹€à¸§à¸µà¸¢ â†’ Big-C à¸šà¸²à¸‡à¸›à¸°à¸­à¸´à¸™ | â€” | 6W | revenue | 3,046à¸¿ | 18x |
| AYU | à¸šà¸²à¸‡à¸žà¸¥à¸µ à¸™à¸µà¹€à¸§à¸µà¸¢ â†’ Big-C à¸šà¸²à¸‡à¸›à¸°à¸­à¸´à¸™ | â€” | 6W | trip_fee | 1,827.6à¸¿ | 18x |
| AYU | à¸šà¸²à¸‡à¸žà¸¥à¸µ à¸™à¸µà¹€à¸§à¸µà¸¢ â†’ CPà¸šà¸²à¸‡à¸šà¸±à¸§à¸—à¸­à¸‡ | â€” | 6W | revenue | 2,997à¸¿ | 12x |
| LCB | CDS â†’ C1C2 | DAIKIN FAC à¸­à¸¡à¸•à¸° | 6W | revenue | 4,200à¸¿ | 2x |
| LCB | CDS â†’ C1C2 | DAIKIN FAC à¸­à¸¡à¸•à¸° | 6W | trip_fee | 2,520à¸¿ | 2x |
| LCB | HK1 â†’ C1C2 | KITZ à¸­à¸¡à¸•à¸° | 6W | fuel_liter | 50L | 1x |
| BIGC | * â†’ Samutprakarn | 1Big c | * | trip_fee | 250à¸¿ | 8x |
| BIGC | * â†’ Nong Khai | â€” | * | fuel_liter | 320L | 3x |

### Suggest API verified
- Query: BIGC / destination=Samutprakarn / pickup=1Big c â†’ **matched card #354 = 250à¸¿** (matched_dims: site_code, destination, pickup_location)
- Query: LCB non-matching pickup â†’ `{"rate_value": null}` âœ“ (reject correctly)

### Known gaps / follow-up
- **Rate Book Wave 2**: wire HTMX into DailyJob form â€” on field change, call `/api/rates/suggest` â†’ auto-fill empty rate fields
- Manual rate editing UI works, but no "explain why this rate matched" hint yet (matched_dims exists in API but not shown to user)
- BIGC importer (`tools/import_bigc_fuel_rate.py`) mutates DailyJob directly without triggering hook â€” à¸•à¹‰à¸­à¸‡à¸à¸” backfill à¸«à¸¥à¸±à¸‡ import

### Route-order gotcha (fixed)
- POST `/rates/backfill` à¸•à¹‰à¸­à¸‡à¸­à¸¢à¸¹à¹ˆà¸à¹ˆà¸­à¸™ POST `/rates/{card_id}` à¹„à¸¡à¹ˆà¸‡à¸±à¹‰à¸™ FastAPI à¸ˆà¸° match `backfill` à¹€à¸›à¹‡à¸™ path param

### Next
- **Wave 2 (HTMX integration)**: hook `/api/rates/suggest` à¹€à¸‚à¹‰à¸²à¸Ÿà¸­à¸£à¹Œà¸¡ DailyJob â€” à¸žà¸´à¸¡à¸žà¹Œ origin/dest â†’ auto-fill
- Maintenance Wave 2/3 (Tire/PM)
- Promote "à¸­à¸²à¸—" + re-import BIGC fuel

---

## 2026-04-08 (Session Summary #22 — Phase 2 import + Driver safety roadmap)

### บริบทจากผู้ใช้
- ต้องการคนขับ **เช็ครถ / เป่าแอลกอฮอล์ + ถ่ายรูปมือถือ** ในอนาคต และขยายเป็นเอกสาร **Safety / Audit ลูกค้า** (อ้างถึงแนว **OSCP ของ DHL** — ในทางปฏิบัติคือชุดข้อกำหนด compliance/audit ของลูกค้า logistics ไม่ใช่ OSCP ด้าน cybersecurity โดยตรง)
- ให้ **ลุย Phase 2** — import Daily + Petty

### การตัดสินใจรอบนี้
- `DailyJob.source` (schema v12) เพื่อ **wipe import ซ้ำได้โดยไม่ลบงาน manual**
- default `--from-date 2018-01-01` สำหรับ Daily + Petty import
- `tools/phase2_import.bat` รันทั้งสองสคริปต์ต่อกัน
- บันทึก roadmap Driver PWA + safety ใน `AGENTS.md` + `.cursor/rules` (profile)

### สิ่งที่ทำแล้ว
- `models.py` + migration + `daily_save` สร้างงานใหม่ `source=manual`
- `import_daily.py`: ใส่ `source=import_daily`, `--wipe-prior` selective, `--mark-legacy-import`
- `import_petty_cash.py`: default from-date 2018
- `import_bigc_fuel_rate.py`: DailyJob ใหม่ `source=bigc_fuel_rate`
- `AGENTS.md`, `CHANGELOG_MASTER.md`, `phase2_import.bat`

### Action ถัดไป
- รัน `python tools/import_daily.py` (และ petty) บนเครื่องที่ติดตั้ง openpyxl แล้ว — ถ้า DB เก่ามี import ก่อน v12 ใช้ `--mark-legacy-import --wipe-prior` ครั้งเดียว (อ่านคำเตือนใน changelog)
- `/admin/promote` คนขับ + ทะเบียน
- Billing export (งานถัดไป Phase 2)

---

## 2026-04-08 (Session Summary #23 — Phase 2 COMPLETE: import + billing + pin)

### สิ่งที่ทำจริงในรอบนี้
1. **ติดตั้ง dependencies**: `openpyxl`, `sqlmodel`, `fastapi`, `uvicorn`, `jinja2`, `python-multipart`, `httpx` (Python 3.13 + 3.14)
2. **Backup DB**: `app.db.bak_phase2_<timestamp>`
3. **Migrate schema v11 → v12**: เรียก `main.init_db()` ก่อน เพื่อเพิ่มคอลัมน์ `dailyjob.source`
4. **Import Daily** (ใหม่หมด): `python tools/import_daily.py --wipe-prior`
   - AYU 592 jobs · BIGC 375 jobs · LCB 585 jobs (+1,215 fees) · รวม **1,552 DailyJob · 533 FuelTxn · 1,215 DailyJobFee**
5. **Import Petty** (ย้อน 2018): `python tools/import_petty_cash.py --wipe-prior`
   - **50,753 PettyCashTxn** (เดิม 1,366) · ย้อนถึง **2019-12-14** · sheets 80 ใน `Salary/LCB/สดย่อยวังน้อย.xlsx` (mtime ล่าสุด)
6. **Backfill FK** (`tools/backfill_links.py` ใหม่): เติม `driver_id`, `head_vehicle_id`, `linked_vehicle_id` จาก Employee/Vehicle master
   - Daily: driver_id 1,445/1,552 (93%) · vehicle 1,552/1,552 (100%)
   - Petty: driver_id 10,390/50,753 (20% — ที่เหลือส่วนใหญ่คือ `พ่อ`, `ศราวุธ`, `โอ`, `เมย์`, `หมิว`, ช่างน้อย, คนขับเก่าที่ออกไปแล้ว)
   - FuelTxn: 100% linked
7. **Billing export** (P0-3):
   - `/billing` — กรอง site/month/customer + สรุปต่อลูกค้า (count, revenue, extra fees, wht, net) + แสดงแถวแรก 40 ต่อกลุ่ม
   - `/billing/export.csv` — UTF-8 BOM + ช่อง `ค่าขนส่ง/ค่าใช้จ่ายอื่น/ภงด/สุทธิ`
   - Nav เพิ่ม link `Billing`
8. **Dependency pin ใหม่ (สำคัญ!)** ใน `ProjectYK_System/app/requirements.txt`
   - `starlette<0.40` + `fastapi<0.115` · starlette 1.0.0 แตก Jinja2 template globals → TypeError "unhashable type: 'dict'" ทุก template
   - ทำให้ /daily, /billing, /admin/promote, /rates, /maint, /payroll 500 error บน environment ใหม่
9. **Smoke test ผ่าน 11 routes** (200 OK) — `/health /daily /petty-cash /billing /billing/export.csv /admin/promote /rates /maint /payroll /vehicles /employees`

### Unmatched ที่เหลือ (ทำทีหลังผ่าน /admin/promote UI)
- Daily: 107 แถว (60 AYU เว้นว่าง + 38 LCB "(ว่าง)" idle/empty + **2 คนขับใหม่**: `บัณดิษฐ์`, `ณัชพล`)
- Petty (top unmatched): `พ่อ` 7,034 · `ศราวุธ` 1,507 · `โอ` 1,317 · `เมย์` 1,113 · `หมิว` 889 · `ช่างน้อย` 805 · ...

### Next
- Promote คนขับเก่า/office staff ที่เหลือใน Petty → /admin/promote
- Collect debt schedule จากพ่อ → Phase 3 CFO Dashboard
- Phase 4 Driver PWA (ตรวจรถ + เป่าแอลกอฮอล์ + OCR)

---

## 2026-04-25 (Session Summary #26 - KYT Weekly Workflow Baseline)

### บริบทจากผู้ใช้
- ผู้ใช้ต้องการให้ช่วยกรอกไฟล์ `KYT TC Weekly` จากรูปในไฟล์ โดยต้องคง template ลูกค้าเดิมให้มากที่สุด
- ผู้ใช้กังวลเรื่องภาษาไทยกลายเป็น `???` และกังวล layout เพี้ยนเมื่อ agent แก้ไขไฟล์
- ผู้ใช้ถามเรื่องนำงานนี้ไปต่อเป็น HTML + AI Vision ในระบบ Project YK

### การตัดสินใจรอบนี้
- เริ่มจากแนวทาง `.md playbook` ก่อน เพื่อใช้งานซ้ำข้ามแชทได้ทันที
- ล็อกกติกา KYT: ห้ามปรับ row/column size และห้ามเปลี่ยนโครง template เดิม
- ใช้ตำแหน่งเซลล์มาตรฐาน Round 1-4 และให้ Round 4 คำขวัญอยู่ที่โซนขาว `L61:AJ64`
- เฟสถัดไปค่อยพัฒนา HTML `KYT Assistant` (upload + AI draft + edit + export)

### สิ่งที่ทำแล้ว
- สร้างคู่มือ `ProjectYK_System/docs/KYT_AUTOFILL_GUIDE.md`
- ใส่ Prompt Template สำหรับเปิดแชทใหม่โดยอ้างไฟล์ guide ผ่าน `@ProjectYK_System/docs/KYT_AUTOFILL_GUIDE.md`
- บันทึกวิธีคุมข้อความล้นช่องแบบไม่แตะขนาดช่อง (`wrap_text` + `shrink_to_fit` + ปรับฟอนต์)

### Action ถัดไป
- ทำหน้า HTML MVP `KYT Assistant` ใน `ProjectYK_System/app` (drag-drop image/file, AI draft Round 1-4, แก้ไขก่อนบันทึก, export กลับ template เดิม)
- แยก prompt ชุด production สำหรับภาพมุมถนน/จุดเสี่ยงโลจิสติกส์ให้ตอบคงที่มากขึ้น

---

## 2026-04-25 (Session Summary #27 - KYT Assistant HTML MVP)

### บริบทจากผู้ใช้
- ผู้ใช้สั่ง "ต่อเลย ยาวจนเสร็จได้เลย" เพื่อทำต่อจาก `.md workflow` ไปเป็นหน้า HTML ใช้งานจริง
- ต้องการ flow: ลากรูป/อัปโหลด → AI วิเคราะห์ → ได้ข้อความ Round 1-4 แบบเดียวกับที่ทำในแชท → export ลง Excel template
- ย้ำเงื่อนไขเดิม: ห้ามทำ layout ลูกค้าเพี้ยน

### การตัดสินใจรอบนี้
- ใช้แนวทาง Human-in-the-loop: AI draft ก่อน แล้วผู้ใช้แก้ข้อความในฟอร์มได้ก่อนกด export
- AI layer ใช้แบบ configurable:
  - ถ้ามี `OPENAI_API_KEY` → เรียก Vision API
  - ถ้าไม่มี key → ใช้ fallback ข้อความมาตรฐาน (ระบบยังใช้งานได้)
- Export layer แยก service โดยคงกฎ "ไม่แตะขนาดช่อง/แถว/คอลัมน์"

### สิ่งที่ทำแล้ว
- เพิ่มหน้าใหม่ `GET /kyt` + template `app/templates/kyt_assistant.html`
  - drag & drop รูป, ปุ่ม Analyze, ฟอร์มแก้ Round 1-4, อัปโหลด template, ปุ่ม Export
- เพิ่ม API `POST /kyt/analyze`
  - รับรูปแล้วคืน JSON:
    - `round1`, `round2`, `round3` (อย่างละ 3 ข้อ)
    - `round4_slogan`
    - `confidence_note`
- เพิ่ม API `POST /kyt/export`
  - รับฟอร์มข้อความ + ไฟล์ `.xlsx` template
  - เติมเซลล์มาตรฐาน KYT แล้วส่งไฟล์ดาวน์โหลดกลับ (`*_filled.xlsx`)
- เพิ่ม service:
  - `app/services/kyt_ai.py` — AI Vision + JSON normalize + fallback
  - `app/services/kyt_excel.py` — เติม Excel แบบคง layout
- เพิ่มเมนูใน navbar: `KYT AI` (ลิงก์ `/kyt`)
- Smoke test ผ่าน:
  - `GET /kyt` = 200
  - `POST /kyt/analyze` = 200
  - `POST /kyt/export` = 200 (ได้ไฟล์ Excel คืน)

### Action ถัดไป
- เพิ่มตารางเก็บประวัติ KYT ใน DB (ภาพ, คนแก้, เวลายืนยัน, สถานะอนุมัติ)
- เพิ่ม batch mode วิเคราะห์หลายภาพพร้อมกัน และ export หลายไฟล์ในครั้งเดียว
- เพิ่ม provider switch/prompt preset ตามประเภทภาพเพื่อให้ output คงที่ขึ้น

---

## 2026-04-25 (Session Summary #28 - KYT Vision fallback policy)

### บริบทจากผู้ใช้
- ผู้ใช้กังวลค่า token และถามว่า local model ใช้ได้ไหม
- ผู้ใช้ขอชัดเจนว่า ถ้าไม่ได้วิเคราะห์รูปจริง ให้คืนค่าว่างหรือแจ้งทำไม่ได้ แทนการเดา

### การตัดสินใจรอบนี้
- เปลี่ยน policy ของ KYT analyze:
  - ถ้าไม่มี provider วิเคราะห์ภาพจริง ให้คืนค่า empty payload + ข้อความ error note
  - ไม่ใช้ fallback ข้อความสำเร็จรูปแบบเดา
- เพิ่มรองรับ local vision ผ่าน Ollama เป็นทางเลือกลดค่าใช้จ่าย cloud token

### สิ่งที่ทำแล้ว
- อัปเดต `app/services/kyt_ai.py`
  - ลำดับการเรียก: OpenAI Vision -> Ollama Vision -> empty result
  - เพิ่ม env รองรับ local: `OLLAMA_VISION_MODEL`, `OLLAMA_BASE_URL`
  - ถ้าวิเคราะห์ไม่ได้ คืน:
    - `round1/2/3` เป็นค่าว่าง
    - `round4_slogan` ว่าง
    - `confidence_note` ระบุสาเหตุชัดเจน
- อัปเดตคู่มือ `ProjectYK_System/docs/KYT_AUTOFILL_GUIDE.md` ให้ตรง policy ใหม่
- ทดสอบ `POST /kyt/analyze` กรณีไม่มี key/model แล้ว ได้ empty result ตามต้องการ

### Action ถัดไป
- ทำหน้า Settings สำหรับเลือก provider และตรวจสถานะการเชื่อมต่อ OpenAI/Ollama
- เพิ่ม health endpoint เพื่อเช็ค local model พร้อมใช้งานก่อน analyze

---

## 2026-04-25 (Session Summary #29 - Ollama setup + strict validation)

### บริบทจากผู้ใช้
- ผู้ใช้ถามว่าสามารถจัดการติดตั้ง local model ให้ครบได้ไหม และต้องโหลดอะไรเพิ่มหรือไม่
- ผู้ใช้ต้องการให้ผลลัพธ์เชื่อถือได้ ถ้า local model วิเคราะห์ไม่ดีให้ระบบแจ้ง/เว้นว่างแทน

### การตัดสินใจรอบนี้
- ติดตั้ง Ollama บนเครื่องและดึง model vision ให้พร้อมใช้งาน
- เพิ่ม quality gate ฝั่ง backend: ถ้า output local ไม่ผ่านรูปแบบ KYT ที่กำหนด ให้คืนค่าว่างพร้อม note

### สิ่งที่ทำแล้ว
- ติดตั้ง `ollama` สำเร็จ (CLI ใช้งานได้)
- pull model `llava:7b` สำเร็จ
- ตั้งค่า env ระดับผู้ใช้:
  - `OLLAMA_VISION_MODEL=llava:7b`
  - `OLLAMA_BASE_URL=http://127.0.0.1:11434`
- อัปเดต `app/services/kyt_ai.py`:
  - เพิ่ม validator เช็คจำนวนข้อ/prefix/ภาษาไทย
  - sanitize error message ให้สั้น อ่านง่าย
  - ถ้าผลลัพธ์ local ไม่ผ่าน validation -> คืน empty payload + reason
- ทดสอบ `POST /kyt/analyze` ผ่าน และคืนค่าว่างตาม policy เมื่อผล local เพี้ยน

### Action ถัดไป
- ทดลองโมเดล local ที่คุณภาพดีกว่า (เช่น `llama3.2-vision:11b`) แล้วเปรียบเทียบความเสถียรภาษาไทย
- เพิ่มหน้า provider health check ใน UI เพื่อดูสถานะ OpenAI/Ollama แบบเรียลไทม์

---

## 2026-04-25 (Session Summary #30 - Ollama 500 retry hardening)

### บริบทจากผู้ใช้
- ผู้ใช้ปิดเปิดใหม่แล้วพบข้อความ error ว่า Ollama Vision ตอบ 500 ที่ `/api/generate`
- ต้องการให้ระบบใช้งานได้จริง ไม่เด้ง error ทาง UX

### การตัดสินใจรอบนี้
- ปรับชั้นเรียก Ollama ให้ retry อัตโนมัติเมื่อพบ 500
- หาก call ที่ใส่ `format=json` พัง ให้ fallback เรียกแบบไม่ใส่ `format` แล้ว parse JSON ต่อเอง

### สิ่งที่ทำแล้ว
- อัปเดต `app/services/kyt_ai.py` ใน `_try_ollama_vision`:
  - เพิ่ม timeout เป็น 90s
  - ถ้า response status >=500 จาก call แรก ให้ retry call ที่สองแบบตัด `format`
- ทดสอบ endpoint `/kyt/analyze` ผ่าน (200) หลังแพตช์

### Action ถัดไป
- เพิ่ม endpoint health check `/kyt/providers/health` เพื่อบอกสถานะ Ollama/OpenAI ก่อนกด Analyze
- ทดลองเปลี่ยนโมเดลเป็น `llama3.2-vision:11b` เพื่อลด output เพี้ยนและผ่าน validation ได้บ่อยขึ้น

---

## 2026-04-25 (Session Summary #31 - Remove KYT module from app)

### บริบทจากผู้ใช้
- ผู้ใช้ตัดสินใจว่าโมดูล KYT ในแอปยังไม่เวิร์กตามต้องการ และขอ "เอาออกจากโปรเจค" ก่อน
- ผู้ใช้ต้องการกลับไปใช้ workflow ผ่าน Cursor chat แทนชั่วคราว

### การตัดสินใจรอบนี้
- rollback ฟีเจอร์ KYT ทั้งชุดออกจาก `ProjectYK_System/app`
- คงระบบหลักอื่นๆ ของ One Platform ไว้ตามเดิม โดยไม่แตะโมดูลที่ไม่เกี่ยวข้อง

### สิ่งที่ทำแล้ว
- ลบ route และ logic ที่เกี่ยวข้องกับ `/kyt`, `/kyt/analyze`, `/kyt/export` ใน `app/main.py`
- ลบเมนู `KYT AI` จาก `app/templates/base.html`
- ลบไฟล์ที่เพิ่มเพื่อ KYT:
  - `app/templates/kyt_assistant.html`
  - `app/services/kyt_ai.py`
  - `app/services/kyt_excel.py`
  - `ProjectYK_System/docs/KYT_AUTOFILL_GUIDE.md`
  - `tools/fill_kyt_weekly.py`
- ตรวจซ้ำว่าไม่มี reference `/kyt` หรือ `kyt_*` ค้างในโค้ด
- compile `main.py` ผ่าน และ lints ไม่มี error

### Action ถัดไป
- หากผู้ใช้ต้องการกลับมาทำ KYT ในระบบอีกครั้ง ให้เริ่มจาก mini-scope/UAT ก่อน แล้วค่อย merge เข้า One Platform

---

## 2026-04-27 (Session Summary #32 - BIGC เม.ย. โครงไฟล์ + 4 แหล่งข้อมูล)

### บริบทจากผู้ใช้
- เริ่มทำเงินเดือน BIGC เดือนเมษายน (รอบวิ่งมีนาคม) ลำดับไซต์: BigC → LCB → AYU
- ตกลงโฟลเดอร์ข้อมูลอยู่ที่ราก repo: `Salary/BigC/2026-04/` (ไม่ใส่ใน `ProjectYK_System/` หรือ `Docs/`)
- อ้างอิงไฟล์เป็นเลขได้: (1) daily, (2) fuel_rate_daily จากแอดมิน, (3) fuel_rate กลาง (พี่ต้น/มาร์ค), (4) ไฟล์วางบิลลูกค้าใน `Billing/BigC/` สำหรับตรวจทานอนาคต

### รายละเอียดแต่ละไฟล์ (บันทึกจากโอ — อ้างอิงเลข 1–4)

**1) `Salary/BigC/2026-04/daily_bigc_2026-04.xlsx`**
- ชีทหลัก: **Sheet1** — ใช้เป็นหลักสำหรับดูเที่ยววิ่ง, ค่าเที่ยว, วันลา/หยุดของทุกคน (มี Sheet2 เพิ่มเติม)
- บทบาทในระบบ: แหล่ง **DailyJob** / attendance สำหรับ payroll BIGC

**2) `Salary/BigC/2026-04/fuel_rate_daily_bigc_2026-04.xlsx`** (แอดมินพี่หวานทำให้)
- ชีท **รวมเรท**: สรุปผลรวมต่อคนขับ — เรททำได้, จำนวนลิตร, ราคา (คูณคืนให้ พขร.; ปัจจุบันตั้ง 16 บาทเพราะราคาน้ำมัน ~32 และแบ่ง 50/50 กับบริษัท; **ถ้าคนไหนติดลบ หักเต็ม 32** — อนาคตอาจปรับเมื่อราคาน้ำมันเปลี่ยน)
- ชีทอื่น: แยกตามคนขับ เสมือนเดลี่ — มีค่าเที่ยว, น้ำมันที่ (กำหนด), เลขไมล์, จำนวน (เติมจริงลิตร); **คอลัมน์ M** = สรุปลิตรเหลือจากที่กำหนด (งบ − เติมจริง)
- บทบาทในระบบ: แหล่ง **งบลิตรต่อเที่ยว/ต่อวัน + เติมจริง + residual** เพื่อคิด fuel rebate และ audit กับ (1)

**3) `Salary/BigC/fuel_rate/fuel_rate.xlsx`** (แอดมินทำ — ไฟล์กลาง)
- ชีท **เรทน้ำมัน พี่ต้น** / **เรทน้ำมัน มาร์ค**: กำหนดจำนวนลิตร (งบ) ตามกติกาที่ OP ใช้
- ชีท **ค่าเที่ยว**: ค่าเที่ยวที่ให้คนขับ (ต้องอ่านร่วมกับ (1) ว่าตรงกันหรือเป็น master แยก)
- บทบาทในระบบ: **master / policy** ที่ (2) อ้างอิงหรือ sync มา

**4) `Billing/BigC/.../1-31 Mar'2026-YKLL.xlsx`** (ลูกค้าส่ง — ตรวจทาน vs เดลี่; หน้าที่พี่หวาน อนาคตให้ระบบช่วย reconcile)
- หลักการค่าขนส่งอธิบายใน **ชีท Rate WNDC** และ **ชีท KM.& Rete_BPD**
- **Rate WNDC**: Base rate ต่อระยะทางต่อประเภทรถ (โดยทั่วไป Head Only; มี 18W–22P เมื่อลูกค้าขอรถพร้อมหาง/ตู้)
- คอลัมน์ **L–U**: ราคาปรับตามน้ำมัน — ลูกค้าใส่ราคาน้ำมันเฉลี่ยเดือนใน **B2** (ปัจจุบันลูกค้าอาจคิดเฉลี่ยเป็น **รายสัปดาห์** แทนเดือน); ปรับตามประเภทรถ: 4 ล้อ **1.2%**, 6 ล้อ **1.6%**, 10 ล้อขึ้นไป **2%** ต่อการเปลี่ยนราคาน้ำมัน **1 บาท**
- **KM.& Rete_BPD**: แต่ละสาขา + กม.; ถ้ามีพ่วงสาขาให้คิดสาขาไกลสุด และพ่วงนับเป็นจุดพ่วงในการวางบิล; จุดราคาอ้างอิงใน Rate WNDC แถว **W–AE**; **BKK** (กรุงเทพและปริมณฑล) หัวลากจุดละ **400**; **UPC** (ตจว.) หัวลากจุดละ **600**

### ความสอดคล้องระหว่างไฟล์ (สรุปให้โอ)
- **เชิงบทบาท**: (1)(2)(3) สอดคล้องกัน — เป็น pipeline เดียวกัน (เดลี่ + งบ/เติมจริง + master เรท) สำหรับ **payroll คนขับ**
- **(4)** ไม่ใช่ไฟล์ payroll โดยตรง แต่เป็น **แหล่งอ้างอิงรายได้ลูกค้า** — ต้อง reconcile กับ (1) ทีหลัง; วันที่ในไฟล์ตัวอย่างเป็น มี.ค. 2026 จึงไม่บังคับให้ตรงรอบเม.ย. ของ (1) ในทุกเซลล์ — ใช้เป็น pattern + ตรวจขาดเกินได้
- **เชิงตัวเลข**: ยังไม่ยืนยันว่า “ทุกช่องตรงกันทุกแถว” จนกว่าจะ import แล้วเทียบ (ชื่อคน, วันที่, เที่ยว, ลิตร, ค่าเที่ยว) — ที่ต้องระวังคือ (1) vs (3) ค่าเที่ยว, (1)(2) vs (3) งบลิตร, และกฎ 16/32 กับ residual คอลัมน์ M

### การตัดสินใจรอบนี้
- ยืนยัน workflow: import ต้นทาง → สร้าง PayRun รอบ `2026-04` → เทียบ manual → แก้ต้นทางแล้วกด "คำนวณใหม่"
- BIGC fuel rebate: กฎที่ผู้ใช้อธิบาย — คูณ 16 ฿/ลิตรเมื่อเหลือจากงบ (50/50 กับบริษัทที่ราคาน้ำมัน ~32); ถ้าติดลบหักเต็ม 32 — ต้องออกแบบในระบบให้ชัด (config ราคาเต็ม + ส่วนแบ่งคนขับ)
- ชีท `รวมเรท` ใน fuel_rate_daily: คอลัมน์ M = ลิตรเหลือจากที่กำหนด — ต้อง map เข้า `DailyJob` / audit field

### สิ่งที่ทำแล้ว
- ตรวจไฟล์ใน workspace จริง: `daily_bigc_2026-04.xlsx` (Sheet1, Sheet2), `fuel_rate_daily_bigc_2026-04.xlsx` (รวมเรท + ชีทตามคนขับ), `fuel_rate.xlsx` (ค่าเที่ยว, เรทน้ำมัน พี่ต้น, เรทน้ำมัน มาร์ค), `1-31 Mar'2026-YKLL.xlsx` (มี Rate WNDC, KM.& Rete_BPD ฯลฯ)
- Agent ยังอ่านแบบ **โครงชีท + ความหมายจากโอ** — ยังไม่ได้ไล่ทุกเซลล์ทุกชีทด้วยตา/สคริปต์ละเอียดในรอบนี้

### Action ถัดไป
- Import BIGC เม.ย. จาก (1)(2) เข้า `DailyJob` / `FuelTxn` / override ตามสเปก
- ออกแบบ import หรือ sync จาก (3) เป็น master งบลิตรต่อคันต่อวัน
- เฟสหลัง: สคริปต์ตรวจทาน (4) เทียบเที่ยว/รายได้กับ daily

---

## 2026-04-27 (Session Summary #33 - BIGC มี.ค. 69 import + payroll เรทลบ)

### บริบทจากผู้ใช้
- คำสั่ง "เริ่มต้นเลย" — import ไฟล์ (1) daily + (2) fuel_rate_daily สำหรับรอบจ่ายเมษายน (งานเดือนมีนาคม)

### การตัดสินใจรอบนี้
- **แท็กรอบในระบบ = `2026-03`** (เดือนของ `work_date`) แม้โฟลเดอร์ชื่อ `2026-04` — BIGC `compute_pay_cycle_tag` = เดือนปฏิทินของงาน
- `import_bigc_fuel_rate.py`: เพิ่ม `--tag YYYY-MM` override + regex ดึง `YYYY-MM` จากชื่อไฟล์ + map ชีท `อาท` → `เกรียงไกร สายแก้ว`
- `import_daily.py`: เพิ่ม `--xlsx` / `--sheet`; `--wipe-prior` + `--site` + `--from-date` ลบเฉพาะไซต์+ช่วงวันที่
- **Payroll BIGC**: เมื่อ residual น้ำมันติดลบ ใช้ `BIGC_FUEL_OVERSPEND_THB_PER_L = 32.15` คูณแทน 16 — ให้ตรงไฟล์ `รวมเรท`
- เพิ่ม `Employee` ขาด: `บุญชอบ พูลสวัสดิ์` (code `BIGC-8009`)
- Backfill `driver_id` บน `DailyJob` มี.ค. BIGC ด้วยการเทียบ **ชื่อแรก** กับ `Employee` ไซต์ BIGC (289/325 แถว)

### สิ่งที่ทำแล้ว
- Import `daily_bigc_2026-04.xlsx` Sheet1 → 325 jobs, 122 fuel (source import_daily)
- Import `fuel_rate_daily_bigc_2026-04.xlsx` + `--tag 2026-03` → อัปเดตงบลิตร + FuelTxn; PayRunAdjust 9 คน; verification vs `รวมเรท` **TOTAL ABS DIFF ≈ 0.44 บาท**
- PayRun id=10 recompute: 9 drivers | gross≈300k | net≈247k

### Action ถัดไป
- แก้ 36 แถว `DailyJob` ที่ยังไม่มี `driver_id` ผ่าน `/admin/promote` หรือเพิ่มกฎ match ชื่อ
- สดย่อย BIGC มี.ค. + finalize รอบเมื่อตรวจครบ
- ไฟล์ (3) `fuel_rate.xlsx` master — ยังไม่ import (เฟสถัดไป)

---

## 2026-04-27 (Session Summary #34 - Import สดย่อย MAR 26 + กันชื่อซ้ำข้ามไซต์)

### บริบทจากผู้ใช้
- ผู้ใช้แจ้งข้อมูล HR: `บุญชอบ พูลสวัสดิ์` เป็นพนักงานใหม่และลาออกวันที่ `2026-04-06`
- ให้ import สดย่อยจาก `Salary/PettyCash/2026-04/petty_cash_all_sites_2026-04.xlsx` โดยใช้ชีท `MAR 26` (รอบวิ่งมีนาคม)
- เน้นชัดเจน: ชื่อซ้ำต้องไม่ปนไซต์ (`สมัย BIG C` vs `สมัย อยุธยา`) และมี `สมพร BIG-C`

### การตัดสินใจรอบนี้
- ปรับ `import_petty_cash.py` ให้รับ `--file`, `--sheet`, `--source-tag`, `--link-drivers`
- เพิ่ม safe linker: ลิงก์ `requester_raw -> Employee` เฉพาะกรณี match ชัดเจน; ถ้าไม่ชัด/ข้ามไซต์ให้ข้าม (ไม่เดาสุ่ม)
- เพิ่ม site-hint parser ใน requester (`BIG C/BIG-C/BIGC`, `อยุธยา/AYU`, `LCB/แหลม`) เพื่อลดโอกาสปนชื่อซ้ำ
- ปรับ payroll engine: ไม่กรองเฉพาะ `Employee.status=="active"` อย่างเดียว แต่ใช้ช่วงการทำงาน (`start_date/end_date`) ซ้อนทับกับรอบเงินเดือน เพื่อให้พนักงานลาออกยังถูกคำนวณในรอบย้อนหลังที่ยังทำงานอยู่

### สิ่งที่ทำแล้ว
- ตั้งค่า `บุญชอบ พูลสวัสดิ์` เป็น `inactive` + `end_date=2026-04-06`
- import ชีท `MAR 26` สำเร็จด้วย `source=import_petty_mar26`: imported 740 rows, deduction 292, pending 8
- safe link รอบแรก: linked 374 rows; รอบสองหลังเพิ่ม site-hint linked เพิ่มอีก 8 rows
- ตรวจชื่อซ้ำ:
  - `สมพร BIG-C` ถูกลิงก์ BIGC ถูกต้อง (`driver_id=30`, `site_code=BIGC`)
  - `สมัย BIG C` ลิงก์ไป BIGC ได้
  - `สมัย อยุธยา` ยังไม่ลิงก์ (ไม่มี Employee AYU ชื่อนี้ใน master ณ ตอนนี้) — **ไม่ปน BIGC**
- recompute BIGC `2026-03` หลังปรับ employment overlap: run id=10 มี 9 คนอีกครั้ง

### Action ถัดไป
- ตัดสินใจว่าจะเพิ่ม Employee สำหรับ `สมัย อยุธยา` หรือคงเป็น unlinked แล้วหัก manual
- ตรวจเทียบยอด `petty_cash_deduction` รายคนใน BIGC run id=10 กับไฟล์ manual
- ไปลำดับถัดไป LCB ตามแผน (daily + fuel + petty)

---

## 2026-04-27 (Session Summary #35 - แก้ payroll BIGC ให้หักลา/ขาดจากคำไทย)

### บริบทจากผู้ใช้
- ผู้ใช้ตรวจหน้า payroll แล้วพบว่า “ยังไม่มีหัก” แม้ควรมีการหักวันลา

### การตัดสินใจรอบนี้
- แก้ `_count_work_days()` ใน `services/payroll.py` ให้รองรับ status ภาษาไทยจากเดลี่จริง:
  - `ลา/ป่วย/ลากิจ/หยุด` -> leave
  - `ขาด` -> absent
  - `ไม่มีงาน/รถจอด/รองาน` -> company_no_work
- ใช้ทั้ง `status_code`, `leave_status`, และ `remark` ประกอบ (ไม่ยึดเฉพาะ code อังกฤษเดิม)

### สิ่งที่ทำแล้ว
- recompute BIGC `2026-03` (run id=10) แล้ว:
  - เกศศักดิ์: leave 1 -> base 8700
  - ธนวัฒน์: leave 1 -> base 8700
  - ณัชพน: leave 1 -> base 8700
  - บุญชอบ: leave 1 -> base 8700
- ยืนยันว่าการหักลาเริ่มมีผลใน payroll detail แล้ว

### Action ถัดไป
- ให้ผู้ใช้ refresh หน้า `/payroll/10` และตรวจรายคนเทียบ manual รอบ BIGC 2026-03 อีกครั้ง
- หากกติกาจริงต้อง “หัก company_no_work ด้วย” ให้ปรับสูตรต่อ (ตอนนี้ยังหักเฉพาะ leave+absent)

---

## 2026-04-27 (Session Summary #36 - ปรับความหมายวันทำงานตาม manual)

### บริบทจากผู้ใช้
- ผู้ใช้ยืนยันกติกาใหม่: **วันทำงาน = 31 - ลา - ขาด** (ไม่นับหัก NO_WORK)
- แต่ถ้าไม่มีแถวเดลี่ของคนนั้นจริงในช่วงนั้น (เช่น ยังไม่ทำงาน/ลาออกแล้ว) ต้องไม่บังคับเป็น 31

### การตัดสินใจรอบนี้
- ปรับ `_count_work_days()`:
  - `worked = จำนวนวัน distinct ที่มี DailyJob แถวจริง - leave - absent`
  - `company_no_work` เก็บไว้แสดงผล แต่ไม่หัก worked
  - ถ้าไม่มี DailyJob ในช่วงเลย -> worked=0

### สิ่งที่ทำแล้ว
- recompute BIGC run id=10 แล้ว
- ตัวอย่างผลหลังปรับ:
  - `สมัย`: worked 31, leave 0, absent 0
  - `พรศักดิ์`: worked 25 (มีแถวเดลี่ 25 วันจริง), leave 0
  - `สมพร BIG-C`: worked 3 (มีแถวเดลี่ 3 วัน)
  - `บุญชอบ`: worked 2, leave 1 (มีแถวเดลี่ 3 วัน)

### Action ถัดไป
- ให้ผู้ใช้ refresh `/payroll/10` แล้วตรวจว่าอ่านค่า worked/leave ตรง manual หรือไม่

---

## 2026-04-27 (Session Summary #37 - อ่านคอลัมน์ G BIGC เพื่ออัปเดตวันเริ่ม/ออก/กลับมา)

### บริบทจากผู้ใช้
- ผู้ใช้ถามให้ดึงข้อมูลจากคอลัมน์ G (เช่น G5, G9) ที่มีข้อความ `เริ่มทำงาน`, `ออก`, `กลับมา`
- ถามว่าแอดมินไม่ต้องใส่วันที่คอลัมน์ A ได้ไหม ถ้าเป็นแถวแจ้งสถานะพนักงาน

### การตัดสินใจรอบนี้
- `import_daily.py` (BIGC) รองรับ parse event จากข้อความในคอลัมน์ G:
  - `เริ่มทำงาน dd/mm[/yy]`
  - `ออก|ลาออก dd/mm[/yy]`
  - `กลับมา dd/mm[/yy]`
- ถ้าแถวแจ้งสถานะไม่มีวันที่ในคอลัมน์ A แต่พบวันที่ในข้อความ G ให้ใช้ fallback date จากข้อความนั้นได้
- อัปเดต `Employee.start_date/end_date/status` อัตโนมัติ (เฉพาะ match ได้ชัดเจนในไซต์เดียว)
- เพิ่ม fallback name match ด้วย “ชื่อแรก” สำหรับกรณี master เก็บชื่อสั้น (เช่น `ณัชพน`)

### สิ่งที่ทำแล้ว
- re-import BIGC Sheet1 แล้วพบว่า start_date ถูกเติมเข้า Employee หลายคน:
  - เกรียงไกร 2021-07-16
  - ณัชพน 2025-02-07
  - ธนวัฒน์ 2022-11-30
  - เกศศักดิ์ 2024-08-27
  - สมประสงค์ 2023-01-23
  - พรศักดิ์ 2026-02-04
  - สมัย 2024-08-01
- บุญชอบคง end_date=2026-04-06 ตามข้อมูลผู้ใช้
- sync fuel-rate และ recompute run id=10 ใหม่เรียบร้อย (verification รวมเรทยัง diff ~0.44)

### Action ถัดไป
- ให้ผู้ใช้ refresh หน้า payroll และตรวจผลที่มีผลจาก start/end date ในรอบถัดไป
- ถ้าต้องการ จะเพิ่มหน้า preview event ที่ parse จากคอลัมน์ G ก่อน commit เข้า Employee

---

## 2026-04-27 (Session Summary #38 - Guardrail รายการหัก unlinked ไม่ให้ตกหล่น)

### บริบทจากผู้ใช้
- ผู้ใช้กังวลเรื่องชื่อแปรผัน (`BigC/BIGC/Big C/BIG C` และชื่อย่อ/ยาว) ทำให้รายการหักอาจไม่ถูกลิงก์และตกหล่นเงียบๆ
- ขอให้มีวิธี “เห็นได้ชัด” ว่ามีรายการที่ยังไม่ลิงก์ และแก้ได้

### การตัดสินใจรอบนี้
- เพิ่ม guardrail ในหน้า payroll:
  - ถ้ามี `PettyCashTxn` ที่ `deduct_from_driver=true`, `deduction_status=pending`, `driver_id is null` ในรอบ/ไซต์เดียวกัน -> แสดง banner เตือน
  - แสดงจำนวนรายการ + ยอดเงินรวมที่ยังไม่ถูกคิด payroll + ตัวอย่างรายการ
  - มีปุ่มลัดไปหน้า `petty-cash` ที่ pre-filter รายการ unlinked
- เพิ่ม filter `unlinked=1` ใน `/petty-cash` เพื่อคัดเฉพาะรายการยังไม่ลิงก์คนขับ

### สิ่งที่ทำแล้ว
- `main.py`
  - `petty_list()` รับ query `unlinked`
  - `payroll_detail()` คำนวณ `unlinked_count/unlinked_amount/unlinked_top` แล้วส่งเข้า template
- `templates/payroll_detail.html`
  - เพิ่ม banner สีแดงเตือน “รายการหักคนขับยังไม่ลิงก์”
- `templates/petty_list.html`
  - เพิ่ม checkbox filter “เฉพาะยังไม่ลิงก์คนขับ”
  - เพิ่ม badge `unlinked` ที่ชื่อผู้เบิก
  - pagination เก็บค่า filter `unlinked`

### Action ถัดไป
- ให้ผู้ใช้ตรวจ banner ใน `/payroll/10`; ถ้าเจอรายการค้างให้กดลัดไปแก้ link ทันที
- เฟสถัดไป (optional): เพิ่ม alias mapping table กลาง เพื่อ auto-link ชื่อแปรผันได้แม่นยำยิ่งขึ้น

---

## 2026-04-27 (Session Summary #39 - ตั้งค่า AI รอบคอบเป็น default ทั้งโปรเจกต์)

### บริบทจากผู้ใช้
- ผู้ใช้ต้องการให้แนวทำงานแบบ “รอบคอบ/ถามซ้ำ/คิดเผื่อ” เป็น default ทุกแชท

### การตัดสินใจรอบนี้
- สร้าง Cursor rule แบบ always apply สำหรับโปรเจกต์นี้
- บังคับ checklist ก่อนสรุป: completeness/leak check + แจ้งความเสี่ยง + next actions

### สิ่งที่ทำแล้ว
- เพิ่มไฟล์ `.cursor/rules/oa-careful-default.mdc` (`alwaysApply: true`)
- ใส่รูปแบบตอบมาตรฐาน: สิ่งที่ทำแล้ว / ค้าง-เสี่ยง / คำถามยืนยัน / ขั้นถัดไป

### Action ถัดไป
- ใช้ rule นี้กับทุกแชทถัดไปในโปรเจกต์นี้โดยอัตโนมัติ

---

## 2026-04-27 (Session Summary #40 - Alias Map กลาง + Preflight/Finalize guard)

### บริบทจากผู้ใช้
- ผู้ใช้อนุมัติให้เดินหน้าตามข้อเสนอที่ค้าง: Alias Map กลาง + ระบบกันตกหล่นก่อน finalize

### การตัดสินใจรอบนี้
- เพิ่ม alias map กลางที่ระดับ app service (`services/alias_map.py`) เพื่อใช้ร่วมกันหลาย importer
- เพิ่ม finalization gate: ถ้ายังมีหักคนขับ `pending` ที่ยังไม่ลิงก์ (`driver_id is null`) ในไซต์เดียวกัน -> บล็อกการปิดรอบ
- เพิ่ม UX เตือนในหน้า payroll + ปุ่มลัดไปหน้า petty ที่กรอง `unlinked`

### สิ่งที่ทำแล้ว
- สร้างไฟล์ `ProjectYK_System/app/services/alias_map.py`
  - normalize site (`BigC/BIG C/Big C` -> `BIGC`)
  - normalize/canonical person aliases (global + per-site)
- ผูก alias map เข้ากับ:
  - `tools/import_daily.py` (employee date parsing match)
  - `tools/import_petty_cash.py` (safe link)
  - `tools/import_bigc_fuel_rate.py` (sheet/driver canonicalization)
- `main.py`
  - `/petty-cash` รองรับ filter `unlinked=1`
  - `/payroll/{run_id}` แสดงจำนวน/ยอด unlinked deductions
  - `/payroll/{run_id}/finalize` บล็อกเมื่อยังมี unlinked pending deductions ในไซต์นั้น
- `templates/payroll_detail.html` เพิ่ม error/banner กรณี finalize ไม่ผ่าน
- `templates/petty_list.html` เพิ่ม checkbox filter `เฉพาะยังไม่ลิงก์คนขับ` + badge `unlinked`
- ตรวจ compile/lints ผ่าน

### Action ถัดไป
- เปิด `/payroll/10` ตรวจว่า banner unlinked เป็น 0 และ flow finalize ผ่าน
- ถ้าต้องการเพิ่ม alias ใหม่ ให้แก้ที่ `services/alias_map.py` กลางไฟล์เดียว

---

## 2026-04-27 (Session Summary #41 - แก้ปัญหาสมัยถูกปนข้ามไซต์ใน payroll)

### บริบทจากผู้ใช้
- ผู้ใช้พบว่า `สมัย` เหมือนมีเที่ยวซ้อน และมีข้อมูลจากไซต์อื่นปนใน BIGC payroll
- ขอให้เช็คและอัปเดต context เพราะ token ใกล้เต็ม

### การตัดสินใจรอบนี้
- ยืนยันสาเหตุหลัก: query คำนวณ payroll เดิม filter แค่ `driver_id + date` (ไม่ได้กรอง `site_code`) ทำให้ employee ที่มีประวัติข้ามไซต์เดิม (`book2_2026`) ถูกนับปน
- แก้โดยบังคับ site filter ใน helper คำนวณทั้งหมด + หน้า drill-down

### สิ่งที่ทำแล้ว
- พบหลักฐาน:
  - `Employee สมัย (BIGC id=1)` มี DailyJob ช่วงมี.ค. ทั้ง `BIGC:58` และ `AYU:28`
  - ตรวจ key ซ้ำ (วันที่+trip_type+destination) ในกลุ่มเดียวกัน **ไม่พบ duplicate key**
  - จึงไม่ใช่ import สองไฟล์ซ้อนแบบแถวซ้ำตรงกัน แต่เป็นการ “ปนข้ามไซต์” ตอน aggregate
- ปรับ `services/payroll.py` ให้ทุก helper รับ/ใช้ `site_code`:
  - trip fee, trip count, gross revenue, fuel cost, bigc fuel rebate, work day, petty deduction, ayu toll
  - `calc_one_employee()` ส่ง `site_code` ทุกจุด
- ปรับ `main.py` หน้า `payroll_employee_detail` ให้ดึง `daily/petty/fuel` เฉพาะ `pr.site_code`
- recompute BIGC `2026-03` ใหม่หลัง fix

### Action ถัดไป
- ให้ผู้ใช้ refresh `/payroll/10` และเปิด drill-down ของ `สมัย` เพื่อยืนยันว่าไม่เห็นแถว AYU ปนแล้ว
- ถ้ายอดที่ถูกต้องตาม manual คือก่อนหน้า ให้ตรวจว่ามีรายการที่เคยนับข้ามไซต์อยู่เท่าไรแล้วตัดสิน policy ต่อ

---

## 2026-04-27 (Session Summary #42 - ตรวจเที่ยวเบิ้ลทั้งเดือนและแก้ duplicate pipeline)

### บริบทจากผู้ใช้
- ผู้ใช้ยกตัวอย่างเที่ยวซ้ำของ `สมัย` (อุบล 1 มี.ค., โซ่พิสัย 4 มี.ค.) และขอให้เช็คทั้งเดือน

### การตัดสินใจรอบนี้
- นิยาม duplicate ที่ใช้ตรวจ: `(work_date + driver + plate + destination)` ภายในไซต์ BIGC
- ยืนยันว่าต้นเหตุเป็น pipeline import:
  - `import_daily` เก็บเที่ยวหลัก
  - `import_bigc_fuel_rate` เคยสร้าง `DailyJob source=bigc_fuel_rate` ทิ้งค้างจากรอบก่อน แล้วไม่ได้ purge ทั้งหมดก่อน re-run
  - ทำให้เห็นเที่ยวคู่ (daily + fuel_rate) รายการเดิม
- แก้ importer ให้ idempotent:
  - ลบ `DailyJob source=bigc_fuel_rate` ของเดือนนั้นก่อนทุกครั้ง
  - post-import dedup pass: ถ้ามีคู่ `import_daily + bigc_fuel_rate` key เดียวกัน ให้ merge field สำคัญกลับเข้า import_daily และลบแถว bigc_fuel_rate

### สิ่งที่ทำแล้ว
- Audit พบ duplicate groups 130 กลุ่ม (260 แถวเกี่ยวข้อง) ก่อนแก้
- แพตช์ `tools/import_bigc_fuel_rate.py` ตามด้านบน
- re-import ใหม่ + recompute run id=10
- re-audit หลังแก้: duplicate groups ตามนิยาม = **0**

### Action ถัดไป
- ให้ผู้ใช้ refresh หน้า detail ของ `สมัย` และ spot-check destination ตัวอย่างที่แจ้งอีกครั้ง
- ถ้าตัวเลข manual ยังต่าง ให้เทียบเฉพาะค่าเที่ยว (`trip_fee_total`) รายวันก่อน จากนั้นค่อยไล่ deduction

---

## 2026-04-27 (Session Summary #43 - แก้สดย่อยสมัยซ้ำจาก 2 source)

### บริบทจากผู้ใช้
- ผู้ใช้แจ้งว่าในสดย่อย `สมัย` ยังซ้ำ

### การตัดสินใจรอบนี้
- ตรวจพบ root cause: BIGC รอบ `2026-03` มี deduction ซ้ำระหว่าง `source=book2_2026` และ `source=import_petty_mar26`
- นโยบาย dedup รอบนี้: ให้ `import_petty_mar26` เป็น source หลัก และ mark แถวซ้ำจาก `book2_2026` เป็น `settled_offline`

### สิ่งที่ทำแล้ว
- พบ duplicate pending deduction groups = 30 (เช่น memo `เงินเบิก` วันเดียว/คนเดียว/ยอดเดียวกัน)
- อัปเดตแถว `book2_2026` ที่ทับกับ `import_petty_mar26` เป็น `deduction_status=settled_offline` พร้อม note marker
- recompute BIGC run id=10 หลัง dedup
- ตรวจซ้ำ: pending duplicate groups = 0
- เคส `สมัย`:
  - pending deduct = 11,050
  - settled_offline deduct = 4,000 (กลุ่มซ้ำที่ถูกตัดออก)

### Action ถัดไป
- ให้ผู้ใช้ refresh หน้า payroll/employee ของ `สมัย` และยืนยันว่ายอดหักไม่ซ้ำแล้ว
- ถ้าต้องการ ให้ยก logic dedup source-priority นี้ไปทำเป็น function/endpoint ถาวรสำหรับทุกเดือน

---

## 2026-04-27 (Session Summary #44 - ตรวจค่าทางด่วนของสมัย BIGC)

### บริบทจากผู้ใช้
- ผู้ใช้แจ้งว่า `สมัย` เหมือนค่าทางด่วน “ไม่มี” ในยอดหัก

### การตัดสินใจรอบนี้
- ตรวจสอบเชิงข้อมูลก่อนเปลี่ยนกติกา: แยกดู `toll` ทั้งหมดของสมัยใน BIGC รอบ `2026-03` และดูว่ารายการไหนถูกตั้งให้หักคนขับจริง

### สิ่งที่ทำแล้ว
- พบ `toll` ของสมัยใน BIGC `2026-03` ทั้งหมด 23 แถว (`amount` รวม 3,115)
- แต่ในข้อมูลมีเพียง 1 แถวที่ `deduct_from_driver=true` (`deduct_amount=50`)
- ที่เหลือส่วนใหญ่เป็น `deduct_from_driver=false` จึงไม่ถูกนำไปหักใน payroll (ตามกติกาปัจจุบันที่นับเฉพาะรายการตั้งหักคนขับ)

### Action ถัดไป
- รอยืนยัน policy จากผู้ใช้: BIGC ค่าทางด่วนควรหักคนขับทั้งหมด หรือเฉพาะแถวที่แอดมินติ๊กหักเท่านั้น

---

## 2026-04-27 (Session Summary #45 - แก้ toll 50 ของสมัยให้เป็น AYU)

### บริบทจากผู้ใช้
- ผู้ใช้ยืนยันว่า `ค่าทางด่วน สมัย 50` เป็นของอยุธยา ไม่ใช่ BIGC

### การตัดสินใจรอบนี้
- ย้ายรายการ `toll` ของสมัยที่อยู่ `site_code=BIGC` (source `book2_2026`, cycle `2026-03`) ไป `AYU` เพื่อไม่ให้ไปหักใน BIGC payroll

### สิ่งที่ทำแล้ว
- อัปเดตแถว toll ของสมัย BIGC->AYU จำนวน 23 แถว
- recompute BIGC run id=10 หลังแก้
- ผล BIGC:
  - net รวมเพิ่มจาก 123,213.99 -> 123,263.99 (+50)
  - สมัย: petty_ded 11,000 / ded_total 11,450 / net 16,122.18

### Action ถัดไป
- ให้ผู้ใช้ refresh หน้า payroll ของ BIGC แล้วตรวจว่า 50 บาทไม่ถูกหักฝั่ง BIGC แล้ว

---

## 2026-04-27 (Session Summary #46 - Surgical reset BIGC 2026-03 แบบเฉพาะจุด)

### บริบทจากผู้ใช้
- ผู้ใช้อนุมัติให้เดินหน้า reset เฉพาะ BIGC รอบ `2026-03` ทันที เพื่อกันข้อมูลปนจาก import รอบก่อน
- เป้าหมายคือไม่ลบทั้งฐาน แต่ล้างเฉพาะ source/รอบที่เกี่ยวข้อง แล้ว import ใหม่ครบชุด

### การตัดสินใจรอบนี้
- ใช้แนวทาง **surgical reset** แทนการลบข้อมูลทั้งหมด:
  - backup DB ก่อนทุกครั้ง
  - ลบเฉพาะ BIGC มี.ค. 2026 และเฉพาะ source ที่ต้อง reimport (`import_daily`, `bigc_fuel_rate`, `import_petty_mar26`)
  - คงข้อมูล historical/source อื่นไว้
- หลัง import ใหม่ต้อง recompute payroll และรัน preflight (duplicate + unlinked) เป็น gate ก่อนให้ผู้ใช้ตรวจ

### สิ่งที่ทำแล้ว
- สร้าง backup: `ProjectYK_System/app/app.db.bak_bigc_202603_reset_20260427_202208`
- ล้างข้อมูลเฉพาะจุด:
  - `DailyJob` BIGC มี.ค. จาก source `import_daily`/`bigc_fuel_rate` = 328 แถว
  - `FuelTxn` ที่ลิงก์กับ DailyJob ข้างต้น = 100 แถว + fuel เฉพาะ source เพิ่มเติม 1 แถว
  - `PettyCashTxn` BIGC cycle `2026-03` source `import_petty_mar26` = 54 แถว
  - ล้าง `PayRunItem/PayRunAdjust` ของ BIGC `2026-03` เดิมเพื่อคำนวณใหม่สะอาด
- import ใหม่ครบ:
  - `tools/import_daily.py` BIGC มี.ค. -> jobs 325, fuel 122
  - backfill `driver_id` หลัง import -> linked เพิ่ม 289 แถว (คง unlinked 36 แถวที่เป็น placeholder/ข้อมูลไม่พอ)
  - `tools/import_bigc_fuel_rate.py --tag 2026-03` -> verification รวมเรท diff รวม 0.44 บาท
  - `tools/import_petty_cash.py` sheet `MAR 26` source `import_petty_mar26` (ทั้งไฟล์) + safe link
- recompute BIGC payrun `2026-03` ใหม่สำเร็จ
- Preflight หลัง reset:
  - duplicate daily groups = 0
  - pending duplicate deduction groups = 0
  - pending unlinked deductions (BIGC 2026-03) = 0

### Action ถัดไป
- ให้ผู้ใช้เปิด `/payroll/10` ตรวจรายคนเทียบ manual รอบ BIGC `2026-03` อีกครั้ง
- หากยอดตรงแล้ว ค่อย finalize รอบ BIGC และเดินต่อ LCB ตามลำดับ

---

## 2026-04-27 (Session Summary #47 - แก้สดย่อย 9/3 ของสมัยแยกไซต์ผิด)

### บริบทจากผู้ใช้
- ผู้ใช้พบความผิดปกติรายการสดย่อยวันที่ `9/3` ของ `สมัย` ว่ามีทั้ง 1000 และ 2000 และสงสัยว่า 1000 เป็นของอยุธยา

### การตัดสินใจรอบนี้
- ยืนยันตาม domain fact ผู้ใช้: เคส `สมัย อยุธยา` ต้องอยู่ฝั่ง AYU
- เคส legacy ชื่อสั้น `สมัย` ยอด 1000 (9/3) ที่ติด BIGC จาก source เก่า ให้ย้ายไป AYU
- คงรายการ `สมัย BIG C` 2000 ไว้ที่ BIGC

### สิ่งที่ทำแล้ว
- แก้ `PettyCashTxn` วันที่ 2026-03-09 ที่เกี่ยวข้องรวม 5 แถว:
  - ย้าย `สมัย` 1000 (`book2_2026`) จาก BIGC -> AYU
  - บังคับ `สมัย อยุธยา` 1000 (ทั้ง `book2_2026` และ `import_petty_mar26`) -> AYU
  - คง `สมัย BIG C` 2000 ทั้งสอง source ไว้ BIGC
- recompute payroll ใหม่ทั้ง BIGC และ AYU รอบ `2026-03`

### Action ถัดไป
- ควรเพิ่ม employee/master alias สำหรับ `สมัย อยุธยา` โดยตรง เพื่อลดการต้องแก้ manual ซ้ำในเดือนถัดไป

---

## 2026-04-27 (Session Summary #48 - เพิ่มหักภาษีรายได้แบบขั้นบันไดใน payroll engine)

### บริบทจากผู้ใช้
- ผู้ใช้ต้องการให้ระบบ payroll คำนวณภาษีรายได้คนขับแบบถูกต้องที่สุดในระบบ แม้ไฟล์ manual จะยังใช้สูตรเดิมไปก่อน

### การตัดสินใจรอบนี้
- เพิ่มการคำนวณภาษีแบบ progressive (รายปี) แล้วเฉลี่ยเป็นยอดหักรายเดือน
- ใช้เป็น payroll deduction อัตโนมัติผ่าน `other_deduction`
- อนุญาต override รายคนผ่าน `Employee.custom_terms` (เช่นยกเว้นภาษี/เพิ่มลดหย่อน)

### สิ่งที่ทำแล้ว
- แก้ `ProjectYK_System/app/services/payroll.py`:
  - เพิ่ม `_annual_progressive_tax()` ตามขั้นภาษีบุคคลธรรมดา
  - เพิ่ม `_compute_income_tax_withholding()`:
    - annualized income = `gross_total * 12`
    - หักค่าใช้จ่าย 50% capped 100,000
    - หัก personal allowance 60,000
    - คำนวณภาษีขั้นบันไดแล้วหาร 12
  - เพิ่ม parser `custom_terms` JSON สำหรับ config ต่อพนักงาน:
    - `tax_exempt`
    - `tax_deduct_expense_pct`
    - `tax_deduct_expense_cap`
    - `tax_personal_allowance`
    - `tax_extra_allowance_annual`
  - ผูกยอดภาษีเข้า `calc.other_deduction` พร้อมโน้ตในสลิป payroll
- ทดสอบ syntax ผ่าน (`py_compile`)
- recompute BIGC `2026-03` เพื่อยืนยัน flow ใช้งานจริงแล้ว

### Action ถัดไป
- ให้ผู้ใช้ตรวจหน้ารายละเอียด payroll ว่าบรรทัดหักเพิ่มสอดคล้องกับ manual ที่ต้องการ
- ถ้าต้องการความโปร่งเพิ่ม ให้แยก field `income_tax_withholding` ใน `PayRunItem` และแสดงเป็นบรรทัดเฉพาะใน UI

---

## 2026-04-28 (Session Summary #49 - Default tax mode = catch-up + แยกช่องภาษีชัดเจน)

### บริบทจากผู้ใช้
- ผู้ใช้ยืนยันต้องการ default `catch-up`
- เงื่อนไขสำคัญ: ถ้าเฉลี่ยทั้งปีไม่ถึงเกณฑ์ภาษี (หรือทำงานไม่ครบปีแล้วไม่ถึง) ต้องไม่หัก เพื่อลดปัญหาหักแล้วไม่ได้คืน

### การตัดสินใจรอบนี้
- ตั้งค่า default ภาษีเป็น `catch-up` ใน engine
- แยกภาษีออกจาก `other_deduction` เป็นฟิลด์เฉพาะ `income_tax_withholding` เพื่อโปร่งใส
- โหมด `safe` ยังรองรับผ่าน config รายคนใน `custom_terms`

### สิ่งที่ทำแล้ว
- `models.py`
  - เพิ่ม `PayRunItem.income_tax_withholding`
- `main.py`
  - เพิ่ม additive migration: `ALTER TABLE payrunitem ADD COLUMN income_tax_withholding REAL DEFAULT 0`
- `services/payroll.py`
  - `PayrollCalc` เพิ่มฟิลด์ `income_tax_withholding`
  - `deduction_total` รวมภาษีจากฟิลด์นี้โดยตรง
  - ปรับ `_compute_income_tax_withholding(...)` ให้รับ `session` และคำนวณตามโหมด:
    - `catch_up` (default): เอาภาษีทั้งปีที่คาดการณ์ หักยอดที่เคยหักแล้วในปีนี้ แล้วเฉลี่ยเดือนที่เหลือ
    - `safe`: หักแบบ flat รายเดือนเมื่อ projected annual เข้าเกณฑ์ (ไม่ไล่เก็บย้อนหลัง)
  - projected annual ใช้ YTD gross + projection เดือนที่เหลือจาก gross เดือนปัจจุบัน
  - ถ้า annual tax <= 0 -> หัก 0
  - รองรับ `tax_mode` ใน `custom_terms` (`catch_up`/`safe`)
  - map ลง `PayRunItem.income_tax_withholding` ตอน save
- Templates:
  - `payroll_detail.html` เพิ่มคอลัมน์ “ภาษี”
  - `payroll_employee_detail.html` เพิ่มบรรทัด “ภาษีหัก ณ ที่จ่าย”
- ทดสอบ:
  - py_compile ผ่าน
  - run migration + recompute BIGC `2026-03` สำเร็จ

### Action ถัดไป
- ให้ผู้ใช้เปิดหน้า payroll ตรวจบรรทัดภาษีแยกรายคน
- ถ้าต้องการ จะเพิ่ม config เพดานหักภาษีต่อเดือน (% ของ net) เพื่อกันยอดหักกระชากในเคสรายได้ผันผวน

---

## 2026-04-28 (Session Summary #54 - หารฐานเงินเดือนตามจำนวนวันจริงของรอบจ่าย ทุกไซต์)

### บริบทจากผู้ใช้
- ผู้ใช้แจ้งว่ามีนาคมมี 31 วัน ต้องหารฐานเงินเดือนตามจำนวนวันจริงของเดือนนั้น
- เดิม BIGC/AYU ตั้ง divisor = 30 ตายตัว ไม่ตรงตามนโยบาย

### การตัดสินใจรอบนี้
- ใช้ `period_days` (จำนวนวันจริงของ cycle) เป็น divisor สำหรับทุกไซต์
- สอดคล้องกับ LCB ที่ใช้ period_days อยู่แล้ว

### สิ่งที่ทำแล้ว
- แก้ `services/payroll.py`: เปลี่ยน `days_in_month` เป็น `period_days` ทุกไซต์
- recompute ทั้ง 3 ไซต์รอบ `2026-03`:
  - BIGC period=31 net=125,045.25 (เกรียงไกร base=8,129.03 หลังหัก 3 วันลาด้วย 9000/31)
  - AYU period=28 net=374,131.43
  - LCB period=28 net=456,069.53

### Action ถัดไป
- เทียบสลิป manual BIGC `2026-03` ดูว่ายอดยังคลาดจุดไหน
- ขยาย Batch 4 (multi-select filter) เมื่อผู้ใช้ยืนยัน

---

## 2026-04-28 (Session Summary #53 - เพิ่ม keyword "เข้าบ้าน" เป็นวันลา)

### บริบทจากผู้ใช้
- ผู้ใช้พบคำใหม่ในเดลี่ของเกรียงไกร: "เข้าบ้าน"
- ขอให้นับ "เข้าบ้าน" เป็นวันลา เพราะคนขับขอลาเพื่อกลับบ้าน

### การตัดสินใจรอบนี้
- เพิ่ม keyword `เข้าบ้าน` เข้า rule ของ `is_leave` ใน `_count_work_days`
- ขยาย scope การ scan ให้รวม `destination` ของ DailyJob ด้วย (เพราะ keyword ถูกบันทึกในช่องนี้จริง)

### สิ่งที่ทำแล้ว
- แก้ `services/payroll.py`:
  - blob ที่ใช้ตรวจคำเพิ่ม `destination` เข้าไป
  - rule `is_leave` รวม `เข้าบ้าน`
- recompute BIGC `2026-03`
- ตรวจเกรียงไกร: leave=3 (ตรงตามคนแจ้ง 22/26/27 มี.ค.), worked=28, base=8,100 (หัก 3 วันออก)

### Action ถัดไป
- ในอนาคตคนขับจะเขียน "ลา" ตรงๆ logic ทั้งคู่จะ catch ได้
- ถ้ามี keyword อื่นเพิ่ม (เช่น "ออกธุระ", "หยุดงาน") แจ้งได้ ผมขยาย rule ให้

---

## 2026-04-28 (Session Summary #52 - UI polish รอบ 1: tax form + dmy filter + jump-to-page)

### บริบทจากผู้ใช้
- ขอช่องตั้งค่าภาษีในฟอร์มพนักงาน (ไม่อยากพิมพ์ JSON)
- ขอ format วันที่เป็น `27/04/2026` ทุกหน้า
- ขอ pagination แบบพิมพ์/เลือกเลขหน้าได้

### การตัดสินใจรอบนี้
- เพิ่ม UI section "ภาษีเงินได้ (หัก ณ ที่จ่าย)" ในฟอร์มพนักงาน รวมเข้า `custom_terms` JSON
- เพิ่ม Jinja filter กลาง `dmy` / `dmy_hm` แล้ว apply ใน list/detail หลัก
- ใส่ jump-to-page (input box ใน petty + dropdown ทั้ง 3 list)
- multi-select filter ทั้ง 3 หน้า (Batch 4) ขอแยกออกไปรอบถัดไป

### สิ่งที่ทำแล้ว
- `templates/employee_form.html`: section ภาษี (โหมด catch_up/safe, cap %, extra allowance, exempt)
- `main.py`:
  - `_parse_custom_terms_safe()` parse JSON ปลอดภัย
  - `employees_new/edit` ส่ง `custom_terms_obj` ให้ template
  - `employees_save` merge ฟิลด์ภาษีลง `custom_terms` JSON
  - register Jinja filters `dmy` / `dmy_hm`
- Apply `| dmy` ใน:
  - `daily_list.html`, `fuel_list.html`, `petty_list.html`
  - `payroll_list.html`, `payroll_detail.html`, `payroll_employee_detail.html`
  - `petty_pending.html`, `petty_clearance.html`, `vehicles_list.html`
- เพิ่ม jump-to-page:
  - `petty_list.html` (input + dropdown)
  - `daily_list.html`, `fuel_list.html` (dropdown)
- ตรวจ parse template ผ่านทุกไฟล์

### Action ถัดไป
- Batch 4 (multi-select filter) สำหรับ /petty-cash /daily /fuel
- ขยาย `dmy` ไปฟอร์ม/หน้าอื่น (loan_form, billing_page, finance_*)
- ปรับ `tools/import_petty_cash.py` pre-assign site จาก suffix
- เริ่มไล่เปรียบเทียบยอด BIGC `2026-03` กับ manual หลัง dedup รอบล่าสุด

---

## 2026-04-28 (Session Summary #51 - dedup สดย่อยสมัย 9/3 ที่ค้าง + reassign site จากชื่อ)

### บริบทจากผู้ใช้
- ผู้ใช้ยังเห็น `เงินเบิก สมัย 9/3` 2000 ซ้ำสองครั้ง และ 1000 unlinked
- ตั้งคำถามว่าควรลบข้อมูลเก่าทั้งหมดเริ่มใหม่หรือไม่

### การตัดสินใจรอบนี้
- ไม่ลบทั้งหมด (เสี่ยงข้อมูลปีก่อนหายโดยไม่จำเป็น)
- ใช้ dedup แบบ fuzzy key ที่ไม่ขึ้นกับ `site_code/driver_id` แล้วถ่วงน้ำหนัก source ใหม่ (`import_petty_mar26 > book2_2026`)
- เพิ่ม alias `สมัย -> สมัย อยุธยา` ใน AYU เพื่อให้ canonical name ตรงกันข้าม source

### สิ่งที่ทำแล้ว
- เพิ่ม alias ใน `app/services/alias_map.py`: `AYU: สมัย -> สมัย อยุธยา`
- รัน dedup pass:
  - ครั้งที่ 1 (fuzzy by requester+amount+memo+date): mark legacy เป็น `settled_offline` 461 แถว
  - ครั้งที่ 2 (canonical name พร้อม site_hint จากคำว่า "อยุธยา"): เพิ่มอีก 24 แถว
- assign `site_code=AYU` ให้ PettyCashTxn ที่ requester มีคำว่า "อยุธยา" และ site ว่าง: 565 แถว
- recompute payroll BIGC `2026-03` + AYU `2026-03` หลัง dedup
- ตรวจ Samai 9/3:
  - เงินเบิก 2000 BIGC = 1 รายการ (ไม่ซ้ำ)
  - เงินเบิก 1000 AYU = 1 รายการ (ไม่ซ้ำ)
  - รายการ deduct=0 อื่นๆ ไม่กระทบ payroll

### Action ถัดไป
- ปรับ `tools/import_petty_cash.py` ให้ pre-assign site จาก suffix ของ requester ตอน insert (กันรอบ import ใหม่ๆ)
- เริ่มงานใหญ่ฝั่ง UI: date format ไทย / multi-select filter / pagination jump-to-page

---

## 2026-04-28 (Session Summary #50 - ตั้งเพดานหักภาษีรายเดือน 15%)

### บริบทจากผู้ใช้
- ผู้ใช้ตัดสินใจเลือกเพดานหักภาษีรายเดือนที่ 15%

### การตัดสินใจรอบนี้
- ตั้งค่า default เพดานภาษีรายเดือนเป็น 15% ของเงินสุทธิก่อนหักภาษี
- ใช้ได้ทั้งโหมด `catch_up` และ `safe` เพื่อลดการหักกระชาก

### สิ่งที่ทำแล้ว
- แก้ `services/payroll.py`:
  - เพิ่ม `tax_monthly_cap_rate` ใน `custom_terms` (default `0.15`)
  - คำนวณ `monthly_cap = net_before_tax * cap_rate`
  - จำกัดยอดภาษีเดือนนี้ด้วย `min(raw_monthly, monthly_cap)` ทั้งในโหมด `safe` และ `catch_up`
- ทดสอบ `py_compile` ผ่าน
- recompute BIGC `2026-03` หลังเปิด cap แล้วสำเร็จ

### Action ถัดไป
- ถ้าต้องการปรับรายคน: ใส่ `{"tax_monthly_cap_rate": 0.12}` หรือค่าที่ต้องการใน `Employee.custom_terms`

---

## 2026-04-28 (Session Summary #49 - เพิ่มโหมดปรับราคาแบบบาทต่อช่วงในหน้า Fuel Rate)

### บริบทจากผู้ใช้
- ผู้ใช้ขอเพิ่มวิธีปรับราคาแบบ "จำนวนบาทต่อช่วง" เพราะเดิมหน้าเครื่องคิดรองรับเฉพาะแบบเปอร์เซ็นต์
- ขอให้ทำเสร็จแล้วอัปเดตขึ้น Git page

### การตัดสินใจรอบนี้
- เพิ่มโหมดใหม่ `baht_per_step` ในหน้า `TransportRateCalculator/transport_rate_calculator.html`
- โหมดใหม่นับ "ขั้นห่างจากช่วงฐาน" แล้วบวก/ลบราคาเป็นบาทคงที่ต่อขั้น
- ยังคงโหมดเดิมเปอร์เซ็นต์ครบ (`compound`, `base`, `% ต่อ 1 บาท`, `% ต่อ 1 ช่วง`) เพื่อไม่กระทบงานที่ใช้อยู่

### สิ่งที่ทำแล้ว
- เพิ่ม UI เลือกชนิดการปรับราคา:
  - `ปรับแบบเปอร์เซ็นต์ (%)`
  - `ปรับแบบจำนวนเงิน (บาท/ช่วง)`
- ปรับ label ช่องกรอกค่าให้เปลี่ยนตามโหมดอัตโนมัติ (`%` หรือ `บาท`)
- ซ่อน/แสดงตัวเลือก `% ต่อ 1 บาท` และ `% ต่อ 1 ช่วง` เฉพาะตอนอยู่โหมดเปอร์เซ็นต์
- อัปเดตสูตรคำนวณใน:
  - ตารางตัวอย่าง (Step 4)
  - ตารางผลลัพธ์หลัก
  - สรุปผลบนการ์ด
  - Export Excel
- ตรวจ lints แล้วไม่พบ error

### Action ถัดไป
- push งานขึ้น remote เพื่อให้ GitHub Pages แสดงโหมดใหม่
- ผู้ใช้ทดสอบหน้าเว็บจริงบน Git page โดยลองเทียบ 2 กรณี:
  - `% ต่อ 1 บาท` (เดิม)
  - `บาท/ช่วง` (ใหม่)

---

## 2026-04-28 (Session Summary #50 - วางทางเลือกใช้พื้นที่เช่าในลาน วาย.เค)

### บริบทจากผู้ใช้
- ผู้เช่าปัจจุบันทำงานประกอบ/ตัดต่อโครงรถบรรทุก (เพิ่มเพลา 6 ล้อเป็น 10 ล้อ) ในพื้นที่ วาย.เค และมีความเสี่ยงย้ายออกถ้าค่าเช่าปรับขึ้นทุกปี
- พื้นที่ที่เกี่ยวข้องมีช่องจอดรถบรรทุก 3 ช่อง, ตู้ออฟฟิศผู้เช่า, ตู้ทึบ 7.2 เมตรใช้เก็บของ, และลานจอดที่แชร์กับรถ วาย.เค/รถลูกค้าเป็นล็อต 10-20 คัน
- หากผู้เช่าย้ายออก คาดว่ารายได้หายประมาณ 34,000 บาท/เดือน (รวมเช่า+น้ำไฟ)

### การตัดสินใจรอบนี้
- ให้ประเมินทางเลือกเช่าพื้นที่แบบ "สะอาดและคุมความเสี่ยง" ก่อนอู่ซ่อมหนัก เพื่อหลีกเลี่ยงคราบน้ำมัน/งานสกปรกที่กระทบภาพลักษณ์และต้นทุนดูแล
- กรอบตัดสินใจหลัก: รายได้ขั้นต่ำต้องไม่ต่ำกว่า 34,000 บาท/เดือน และต้องไม่แย่ง capacity ลานจอดที่รองรับงานลูกค้าหลักของ วาย.เค

### สิ่งที่ทำแล้ว
- สรุปแนวทางธุรกิจที่เหมาะกับพื้นที่จริง: ลานพักรถ+คิวงาน, จุด cross-dock เบา, และบริการเสริมที่เกี่ยวเนื่องกับรถบรรทุกแบบไม่สกปรก
- วางแนว guardrail ที่ต้องใช้ถ้าเปิดเช่ารายใหม่: สัญญาแบ่งโซน, SLA ความสะอาด, และเพดานจำนวนรถต่อช่วงเวลา

### Action ถัดไป
- เก็บข้อมูลหน้างานเพิ่มเพื่อทำ decision sheet 1 หน้า: อัตราเช่าตลาดรอบพื้นที่, จำนวนรถ peak ต่อวันของ วาย.เค, และต้นทุนดูแลพื้นที่/น้ำไฟจริงต่อเดือน

---

## 2026-04-28 (Session Summary #51 - ข้อจำกัดทางเข้าออกลานและคดีถนน)

### บริบทจากผู้ใช้
- ผู้ใช้ยืนยันว่าปัจจุบันรถบรรทุกเข้า-ออกพื้นที่ค่อนข้างยาก
- มีข้อพิพาท/คดีเรื่องถนนทางเข้าออกอยู่ระหว่างฟ้องร้อง

### การตัดสินใจรอบนี้
- ปรับเกณฑ์คัดผู้เช่าใหม่เป็น "access-first": ธุรกิจที่พึ่งพารถใหญ่ถี่สูงให้ถือเป็นความเสี่ยงสูงชั่วคราว
- ระหว่างคดียังไม่จบ ให้ prioritise ผู้เช่าที่ใช้รถขนาดเล็กกว่า/เข้าออกเป็นช่วงเวลา/ไม่พึ่ง turnaround หนาแน่น

### สิ่งที่ทำแล้ว
- อัปเดตคำแนะนำเชิงกลยุทธ์จากเดิม (ลานรถบรรทุก) ไปเป็นแนว conservative มากขึ้นเพื่อกันรายได้สะดุดและกันปัญหาหน้างานซ้ำ
- เพิ่มแนวคิดสัญญาแบบมีเงื่อนไข access clause และทดลองสั้น 3-6 เดือนก่อนล็อกยาว

### Action ถัดไป
- ทำ traffic log จริง 14 วัน (จำนวนรถเข้าออก แยกช่วงเวลาและประเภทรถ) เพื่อใช้ตั้งเพดานรถในสัญญา
- ให้ที่ปรึกษากฎหมายช่วยร่าง clause กรณี access disruption เพื่อปิดความเสี่ยงค่าเสียหายจากผู้เช่า

---

## 2026-04-28 (Session Summary #52 - สูตรเสนอราคา Direct-to-store แบบทำในแชท)

### บริบทจากผู้ใช้
- ผู้ใช้ต้องการทำราคาใบเสนอแบบ ad-hoc ในแชท Cursor โดยไม่ต้องเข้าระบบ
- ยืนยันค่ามาตรฐานรอบนี้: รถ 6 ล้อค่าเที่ยว 500, รถ 10 ล้อค่าเที่ยว 600, maintenance 1.5 บาท/กม., back office 12%
- ยืนยันว่า `700,000` คือมูลค่ารถ (ไม่ใช่ต้นทุนต่อเดือน) และให้คิดค่าเสื่อมแบบ 8 ปี
- ยืนยันเบี้ยประกันจริงใช้ `13,500/ปี` เหมือนกันทั้ง 6/10 ล้อ และยึด conservative assumption `1 เที่ยว = 1 วัน (5 วัน/สัปดาห์)`

### การตัดสินใจรอบนี้
- ใช้สูตรต้นทุนคงที่ต่อเที่ยวเป็น `((700000/8)+13500)/365`
- ตั้งแนวทางคุมตลาดค่าดรอปที่ `400-600 บาท/drop` และปัดราคาเป็นหลักสิบ
- ถ้าวิ่งมากกว่า 1 เที่ยว/วัน ให้ถือเป็น upside (ไม่ลด baseline ตอนเสนอราคา)

### สิ่งที่ทำแล้ว
- เติมสูตรคอลัมน์ `K/L/M` ในไฟล์เสนอราคาลูกค้า Direct-to-store:
  - `K` = 6 wheels
  - `L` = 10 wheels
  - `M` = drop charge (ใช้ `MEDIAN` คุม floor/cap)
- ใส่ assumptions ชุดเดียวกันลงชีทเพื่อให้ตรวจย้อนหลังได้ (มูลค่ารถ, อายุปี, เบี้ยประกัน, น้ำมัน, maintenance, back office, drop floor/cap)

### Action ถัดไป
- สร้าง prompt template มาตรฐานสำหรับลูกค้า ad-hoc รายใหม่ (แม้รูปแบบไฟล์ต่างกัน)
- เพิ่มตาราง stress test น้ำมัน (`±1 บาท`, `±2 บาท`) เพื่อดูจุด break-even และเตือนเมื่อเสี่ยงขาดทุน

---

## 2026-04-28 (Session Summary #53 - ปรับตาม consumption แยกรถ 6W/10W + เพิ่ม Fuel%)

### บริบทจากผู้ใช้
- ผู้ใช้ยืนยันว่า consumption เดิม 3 กม./ลิตรเป็นหัวลากเฉลี่ย ไม่ใช่สำหรับงานนี้
- ระบุค่าใหม่สำหรับงานเสนอราคา:
  - 6 ล้อ = `5.5 กม./ลิตร`
  - 10 ล้อ = `4.5 กม./ลิตร`
- ขอเพิ่มคอลัมน์ `%น้ำมันต่อค่าขนส่ง` ในไฟล์เสนอราคา

### การตัดสินใจรอบนี้
- คำนวณต้นทุนน้ำมันแยกตามประเภทรถแทนการใช้ค่าเดียวทั้งตาราง
- คง baseline เดิมของดีลนี้:
  - ช่วงน้ำมันอ้างอิง 31.00-31.99 (ใช้ 31.5)
  - maintenance 1.5 บาท/กม.
  - back office 12%
  - ราคา floor 6W/10W = 2200/2300
  - ปัดราคาเป็นหลักร้อย

### สิ่งที่ทำแล้ว
- อัปเดตไฟล์ลูกค้า `Direct to store (Thainumtip_Lotus).xlsx`
- เติม assumption ใหม่ในชีท (consumption 6W/10W)
- เพิ่มคอลัมน์ `%น้ำมันต่อค่าขนส่ง` (6W/10W) เพื่อให้เห็นสัดส่วน fuel burden ต่อรูท

### Action ถัดไป
- ถ้าจะใช้เชิงพาณิชย์ต่อเนื่อง ให้เพิ่มธงเตือนอัตโนมัติเมื่อ `%น้ำมันต่อค่าขนส่ง` เกิน threshold (เช่น 30%)
- ทำ stress test น้ำมันขึ้นลงเพื่อหา base rate ขั้นต่ำที่ยังไม่ขาดทุนรายรูท

---

## 2026-04-28 (Session Summary #54 - เพิ่ม fuel escalation model ต่อ 1 บาท)

### บริบทจากผู้ใช้
- ผู้ใช้ต้องการทดสอบว่าเมื่อราคาน้ำมันขึ้นมาก (ถึง 50 บาท/ลิตร) ยังไม่ขาดทุนได้หรือไม่
- ถามเชิงนโยบายว่าควรขอปรับราคา `2% ต่อ 1 บาท` จากลูกค้าหรือไม่
- กำหนดเกณฑ์ตีความ fuel burden: สวย `<=50%`, รับได้ถึง `<=60%`

### การตัดสินใจรอบนี้
- เพิ่มโหมดในไฟล์ให้กรอก `% ปรับต่อ 1 บาท` ได้เอง (`P21`) และกรอกน้ำมันเป้าหมายได้ (`P22`)
- เพิ่มคอลัมน์คำนวณราคา/มาร์จิ้นที่น้ำมันเป้าหมาย และ `% ต่อบาทที่ต้องการขั้นต่ำ` รายรูท
- จากการคำนวณ baseline พบว่า `2% ต่อ 1 บาท` ยังไม่ครอบคลุมทุกรูทถึงน้ำมัน 50; เพดานที่ปลอดภัยทั้งชุดอยู่ราว `2.3% ต่อ 1 บาท`

### สิ่งที่ทำแล้ว
- เพิ่มคอลัมน์ `AE:AJ` ในไฟล์ลูกค้า:
  - ราคาปรับ 6W/10W ที่น้ำมันเป้าหมาย
  - มาร์จิ้นที่น้ำมันเป้าหมาย
  - `% ต่อ 1 บาท` ขั้นต่ำเพื่อ break-even แยก 6W/10W
- เพิ่ม assumption `P21` และ `P22` สำหรับ user input แบบ editable

### Action ถัดไป
- ให้ผู้ใช้กด recalc ใน Excel แล้วดูค่า `AI/AJ` เพื่อสรุปเรทเจรจาจริง
- ถ้าต้องการ policy เดียวทั้งดีล แนะนำตั้ง `2.5% ต่อ 1 บาท` เพื่อกัน rounding/floor effects

---

## 2026-04-28 (Session Summary #55 - เปลี่ยนเงื่อนไขลูกค้าเป็น 1.5% ต่อ 1 บาท)

### บริบทจากผู้ใช้
- ผู้ใช้ยืนยันให้เปลี่ยนเงื่อนไขเจรจาเป็นปรับราคาน้ำมัน `1.5% ต่อ 1 บาท` (จากเดิม 2%)
- ต้อง recalibrate ราคา Base ใหม่ให้ยังถือเป้า margin ที่น้ำมัน 50 ได้
- ต้องการบันทึกบริบทแชทนี้ไว้ใช้ซ้ำกับไฟล์ลูกค้ารูปแบบอื่นในอนาคต

### การตัดสินใจรอบนี้
- ตั้งค่าในไฟล์ทำงานหลัก (`_v3_adjusted_only`) เป็น:
  - `P21 = 0.015` (1.5%)
  - `P22 = 50`
  - `P23 = 0.10` (target margin ที่ fuel target)
- คงกติกาเดิม: ปัดหลักร้อย, floor 6W/10W = 2200/2300, stress view แสดงเฉพาะกรณี after-adjust

### สิ่งที่ทำแล้ว
- Reprice ตารางใหม่ภายใต้ 1.5%/บาท บนไฟล์ `_v3_adjusted_only`
- เคลียร์ค่า context ที่ทำให้สับสน (`P24`) และย้ำว่าใช้ `P21` ช่องเดียวสำหรับ % ปรับน้ำมัน
- ตรวจซ้ำ margin ที่น้ำมัน 50 ได้ต่ำสุดประมาณ:
  - 6W ≈ 10.06%
  - 10W ≈ 10.01%

### Action ถัดไป
- หากต้องใช้ไฟล์ชื่อหลัก ให้ sync จาก `_v3_adjusted_only` กลับไฟล์ production หลังปิดไฟล์ต้นทาง
- ทำ checklist input สั้นสำหรับงานลูกค้าใหม่ (distance, drop basis, consumption, escalation %, target fuel, target margin)

---

## 2026-04-28 (Session Summary #56 - ปรับ consumption/ค่าเที่ยวขั้นบันได + โซนเน้นงาน 5%)

### บริบทจากผู้ใช้
- ปรับ consumption 6W จาก 5.5 -> `5.0 กม./ลิตร`
- กำหนดค่าเที่ยวแบบขั้นบันไดตามระยะทาง (อิง `J`):
  - `0-200 กม.` = `500/600` (6W/10W)
  - เกิน 200 กม. ทุก +100 กม. เพิ่มค่าเที่ยวอีก +100 ทั้ง 6W/10W
- โซนเป้าหมายที่ยอมมาร์จิ้นต่ำลงเพื่อชิงงาน: `สมุทรปราการ / ฉะเชิงเทรา / ชลบุรี`
  - target margin ที่ fuel target ใช้ `5%` (โซนอื่นยัง `10%`)

### การตัดสินใจรอบนี้
- ยังคงเงื่อนไขคีย์เดิม: fuel base 31.00-31.99 (31.5), fuel target 50, escalation 1.5%/บาท, ปัดหลักร้อย, floor 2200/2300
- เพิ่มความโปร่งใสโดยเขียนคอลัมน์ helper:
  - `AK` = target margin ที่ถูกใช้จริงต่อแถว
  - `AL/AM` = trip fee 6W/10W ที่คำนวณตามขั้นบันได

### สิ่งที่ทำแล้ว
- Reprice ทั้งตารางในไฟล์ `Direct to store (Thainumtip_Lotus)_v3_adjusted_only.xlsx`
- อัปเดต assumptions (`P14=5.0`, `P15=4.5`, `P21=0.015`) และคอลัมน์ stress/target ให้สอดคล้องเงื่อนไขใหม่
- ตรวจพบแถวที่เข้าโซน margin 5% = 7 แถว

### Action ถัดไป
- หากผู้ใช้ยืนยันเวอร์ชันนี้ ให้ sync กลับไฟล์ชื่อหลักเพื่อใช้ส่งลูกค้า
- เพิ่มสีเตือนอัตโนมัติบน `AG/AH` เมื่อ margin ต่ำกว่า target ของแถวนั้น (เทียบกับ `AK`)

---

## 2026-04-29 (Session Summary #57 - Payroll PDF bundle + bank sheet)

### บริบทจากผู้ใช้
- ต้องการปุ่มส่งออกสลิปทุกคนในไซท์รอบนั้นเป็น PDF (เรียงชื่อ) บันทึกอัตโนมัติที่โฟลเดอร์ Salary เพื่อส่งไลน์คนขับ
- ต้องการหน้าสรุปรวมให้พ่อดู และหน้าโอนเงินสำหรับบัญชี (อ้างอิง PDF เดิม แบ็งค์ / รวม YK BigC)

### การตัดสินใจรอบนี้
- ใช้ **fpdf2** + ฟอนต์ Windows (Tahoma / TH Sarabun)
- เก็บไฟล์ที่ `Salary/{SITE}/{YYYY-MM}/Driver/` — ไฟล์สรุป / โอนเงิน / ชุดครบ / โฟลเดอร์ `รายคน/` สลิปแยกคน
- เลขบัญชีโอน: `Employee.custom_terms` (`bank_name`, `bank_account`, `payment_note`)

### สิ่งที่ทำแล้ว
- `services/payroll_slip.py`, `services/payroll_export_pdf.py`, `POST /payroll/{id}/export-pdfs`, ปุ่มใน `payroll_detail.html`, `fpdf2` ใน requirements

### Action ถัดไป
- รัน `pip install -r requirements.txt` แล้วทดสอบปุ่มส่งออก — ฟอนต์หายให้ติดตั้งไทยบน Windows

---

## 2026-04-29 (Session Summary #58 - Payroll PDF: BIGC เดือนจ่าย / เลขบัญชี seed / สลิป 1 หน้า)

### บริบทจากผู้ใช้
- BIGC งวดวิ่งมีนาคมแต่จ่ายเมษายน — เก็บไฟล์ผิดโฟลเดอร์เดือน (ควรเป็นโฟลเดอร์เดือนจ่าย)
- ต้องการหน้าตา PDF ใกล้แบบเดิม + เลขบัญชีตาม PDF ที่ส่งมา + สลิปรายคนพอดีหนึ่งหน้า

### การตัดสินใจรอบนี้
- **`salary_folder_month_tag(pr)`**: เฉพาะไซต์ **BIGC** ให้โฟลเดอร์เก็บเป็นเดือนถัดจาก `pay_cycle_tag` (มีนาคม `2026-03` → `2026-04`); ไซต์อื่นยังใช้ `pay_cycle_tag` เดิม
- **`merged_bank_terms` + `services/bigc_bank_seed.py`**: ถ้ายังไม่มีเลขบัญชีใน `custom_terms` → เติมจากชุดตัวอย่าง BIGC (ผู้ใช้ให้ในแชทก่อนหน้า)
- **PDF**: สรุป/โอน — หัวตารางโทนสลับแถว · สลิปรายคน — **แนวนอน A4** ซ้ายตารางเที่ยว / ขวาสรุปเงิน / แถบเขียวสุทธิล่าง · ชื่อไฟล์มีทั้งเดือนจ่ายและแท็กงวดวิ่ง

### สิ่งที่ทำแล้ว
- แก้ `payroll_slip.py`, `payroll_export_pdf.py`, `main.py` (แจ้ง path ใน payroll_detail), เทมเพลต export done/detail

### Action ถัดไป
- ให้ทดสอบปุ่มส่งออกรอบ BIGC `2026-03` แล้วเปิดโฟลเดอร์ `Salary/BIGC/2026-04/Driver/` ว่าตรงใจ + เทียบเลขบัญชีกับไฟล์จริง

---

## 2026-04-29 (Session Summary #61 - BIGC ชื่อไม่มีนามสกุล → alias + PDF โอนชื่อเต็ม)

### สิ่งที่ทำแล้ว
- `alias_map.py`: BIGC alias `บุญชอบ` → `บุญชอบ พูลสวัสดิ์`
- `bigc_bank_seed.py`: `lookup_bigc_bank` เพิ่มจับคู่ prefix แบบ dedupe เมื่อมีชุดเลขบัญชีเดียว
- `payroll_slip.py`: `employee_bank_display_name()` — canonical ตามไซต์
- `payroll_export_pdf.py`: สรุป/โอน/สลิป/ชื่อไฟล์ใช้ชื่อแสดงผลแบบเต็ม · ขยายคอลัมน์ชื่อหน้าโอน

### Action ถัดไป
- ถ้ามีคนอื่นชื่อสั้นในระบบอีก ให้เพิ่มบรรทัดใน `PERSON_ALIASES_BY_SITE["BIGC"]` แบบเดียวกับบุญชอบ

---

## 2026-04-29 (Session Summary #59 - PDF สลิปซ้อนตัวอักษร fpdf ln reset)

### สิ่งที่ทำแล้ว
- แก้ `render_driver_slip_page`: fpdf `cell(..., ln=True)` จะดัน **abscissa กลับขอบซ้ายของหน้า** — ทำให้บล็อกสรุปเงินทับคอลัมน์ซ้าย · เพิ่ม `_rcell()` ที่ `set_x(rx)` ก่อนทุกบรรทัดในคอลัมน์ขวา

### Action ถัดไป
- ส่งออก PDF ซ้ำแล้วตรวจสลิปรายคนว่าตารางซ้ายไม่ถูกทับอีก

---

## 2026-04-29 (Session Summary #60 - BIGC seed เลขบัญชีตามตารางผู้ใช้)

### สิ่งที่ทำแล้ว
- อัปเดต `services/bigc_bank_seed.py` ให้ตรงตาราง 9 คน: กสิกร / SCB / กรุงไทย / กรุงศรี · เพิ่ม **บุญชอบ พูลสวัสดิ์** `payment_note` = `#N/A` (ไม่ให้ไปเป็นกดเงินสด)

### Action ถัดไป
- ส่งออก PDF โอนเงินซ้ำแล้วตรวจชื่อในระบบว่าตรง canonical (ถ้าไม่แม็ชให้กรอกใน `custom_terms`)

---

## 2026-04-29 (Session Summary #62 - Petty ลิงก์แก้ไขจาก payroll drill-down)

### สิ่งที่ทำแล้ว
- `payroll_employee_detail.html`: คอลัมน์ «แก้ไข» → `/petty-cash/{id}/edit?next=/payroll/{run}/employee/{emp}`
- `main.py`: `_safe_internal_path`, `petty_edit` รับ query `next`, `petty_save` รับ `next_url` แล้ว redirect กลับเมื่อปลอดภัย
- `petty_form.html`: hidden `next_url` + ลิงก์ «กลับหน้าเดิม (ไม่บันทึก)»

### Action ถัดไป
- คลิกแก้ไขจากหน้า drill-down แล้วบันทึก — ควรกลับมาที่หน้า payroll employee เดิม

---

## 2026-04-29 (Session Summary #63 - หลังแก้สดย่อย → คำนวณใหม่ + อยู่หน้า drill-down)

### สิ่งที่ทำแล้ว
- `petty_save` redirect กลับ payroll employee พร้อม `?petty_saved=1`
- `payroll_employee_detail` แบนเนอร์ฟ้าอธิบาย + ปุ่มคำนวณใหม่
- `POST /payroll/{id}/recompute` รับ `return_to` — หลังคำนวณ redirect กลับหน้า drill-down ได้

### Action ถัดไป
- ทดสอบแก้สดย่อย → กดคำนวณใหม่ → ตัวเลขหักสดย่อยตรงกับ «สด ณ ตอนนี้»

---

## 2026-04-29 (Session Summary #64 - Re-import สดย่อยเม.ย. 2569 จาก `petty_cash_all_sites_2026-04 rev.1.xlsx`)

### บริบทจากผู้ใช้
- มีไฟล์สดย่อยรวมไซต์อัปเดต `Salary/PettyCash/2026-04/petty_cash_all_sites_2026-04 rev.1.xlsx` ให้ยึดเป็นต้นทาง และระวังข้อมูลซ้ำ

### การตัดสินใจรอบนี้
- **ไม่ใช้** `--wipe-prior` แบบทั้ง `source` — เพราะ `book2_2026` มีหลายเดือน (มี.ค./เม.ย./ฯลฯ)
- ลบเฉพาะ `PettyCashTxn` ที่ `source='book2_2026'` **และ** `pay_cycle_tag='2026-04'` (48 แถวเก่า) แล้ว import ใหม่จากชีท **`APR 26`** เท่านั้น (`pay_cycle_tag` จากชื่อชีท)
- Backup DB: `ProjectYK_System/app/app.db.bak_petty_202604_rev1_20260429`
- ตรวจแล้วรอบ `2026-04` ใน DB เหลือแหล่งเดียว `book2_2026` (ไม่ซ้อนกับ source อื่น)

### สิ่งที่ทำแล้ว
- Import: `1425` แถว (สแกน 1653, skip empty/nodate)
- Driver-link `--link-drivers` รันได้ตามโค้ดเดิม (ประมวลผลทุกแถว `book2_2026` ที่ยังไม่มี driver)

### Action ถัดไป [Leak risk]
- รายการหักที่ยัง **ไม่ผูกคนขับ** ในรอบเม.ย. (`deduct_from_driver` + `driver_id` null + pending): **353 แถว ~205,356 บาท** — หาก finalize payroll โดยไม่จัดการ alias/link จะไม่เข้ายอดหักอัตโนมัติตามคนจริง
- หลังจัดการแล้วให้ **คำนวณ payroll ใหม่** รอบที่เกี่ยวข้อง

---

## 2026-04-29 (Session Summary #65 - ชีท MAR 26 เป็นหลักรอบมี.ค. 2569)

### บริบทจากผู้ใช้
- ให้ยึดชีท **MAR 26** เป็นต้นทางหลักสำหรับงวดมีนาคม (ไม่ให้ซ้ำกับ import เดิม)

### การตัดสินใจรอบนี้
- ลบของเก่ารอบ `pay_cycle_tag=2026-03` สองชุดที่เป็นซ้ำซ้อนกัน: **`book2_2026`** (682 แถว) + **`import_petty_mar26`** (740 แถว)
- Import ใหม่จาก `petty_cash_all_sites_2026-04 rev.1.xlsx` ชีท **`MAR 26`** → `source=book2_2026`
- Backup: `app.db.bak_petty_mar26_rev1_20260429`

### สิ่งที่ทำแล้ว
- นำเข้า **740** แถว (ตรงกับจำนวนเดิมของ `import_petty_mar26` — cross-check sanity)
- รอบ `2026-03` เหลือ bulk หลักที่ `book2_2026` เท่านั้น; ยังมี `ayu_office_mar_2026` (5) + `lcb_advance_summary` (20) — ถ้า payroll รวมทุก source อาจต้องพิจารณา merge ภายหลัง

### Action ถัดไป
- **คำนวณ payroll ใหม่** รอบที่ใช้แท็ก `2026-03` (BIGC/LCB/AYU ตามลำดับที่ใช้อยู่)

---

## 2026-04-29 (Session Summary #66 - สมพร BIG-C / โม่งปราณีต + bug link_drivers_safe เมื่อมี BIG-C ในชื่อ)

### บริบทจากผู้ใช้
- **สมพร BIG-C** กับ **สมพร โม่งปราณีต** เป็นคนเดียวกัน — มีหักสดย่อย **2,000 บาท**

### การตัดสินใจรอบนี้
- **`GLOBAL_PERSON_ALIASES`**: เพิ่มแม็ปชื่อเต็ม + typo (`โม่งปรำณีต`) → `สมพร BIG-C` เพื่อให้ canonical ใช้ได้แม้แถวสดย่อยไม่มี `site_code`
- **`link_drivers_safe`** (`ProjectYK_System/tools/import_petty_cash.py`): เมื่อมีคำว่า BIG-C ใน `requester_raw` ระบบเดิม strip เหลือแค่ `สมพร` แล้วไปคีย์ที่ไม่ชน `Employee` (`สมพร BIG-C`) → **เก็บผลจับคู่จาก canonical key เดิม** ถ้าคัดจากชื่อที่ strip แล้วว่าง
- **`canonical_person_name(raw_req, row_site)`**: ส่ง `site_code` จากแถวเข้า alias เมื่อมี

### สิ่งที่ทำแล้ว
- รัน `link_drivers_safe(book2_2026)` ใหม่ → linked เพิ่ม (รวมแถวมี.ค. เช่น id **55933** `สมพร BIG-C` 2,000฿ → `driver_id=30`, `site_code=BIGC`)

### Action ถัดไป
- **คำนวณ payroll ใหม่** รอบ BIGC `2026-03` เพื่อให้หักสดย่อยเข้ายอดพนักงานคนนี้

---

## 2026-04-29 (Session Summary #67 - LAN เข้าเว็บเดียวกัน: bind 0.0.0.0)

### บริบทจากผู้ใช้
- `start.bat` แล้วเข้า `127.0.0.1:8010/daily` ได้ แต่เครื่องอื่นเข้าไม่ได้

### การตัดสินใจรอบนี้
- **`uvicorn` host เดิม `127.0.0.1`** รับสายเข้าได้แค่เครื่องตัวเอง → default **`YK_BIND_HOST=0.0.0.0`** (override เป็น `127.0.0.1` ได้)
- พิมพ์ URL ให้เครื่องอื่นด้วย **LAN IPv4 + พอร์ต** (ไม่ใช้ 127.0.0.1)
- เตือนเปิด **Windows Firewall** ถ้ายังบล็อกพอร์ต

### สิ่งที่ทำแล้ว
- แก้ `main.py` (`_find_free_port` probe ใช้ host เดียวกับ uvicorn, `_primary_lan_ipv4`, พิมพ์ลิงก์ LAN)
- ปรับข้อความ `start.bat`

---

## 2026-04-30 (Session Summary #68 - รวมโฟลเดอร์ ProjectYK_System + ประหยัด token Cursor)

### บริบทจากผู้ใช้
- อยากให้ของที่เกี่ยวกับระบบหลักอยู่รวมกัน และถามวิธีลดการกิน token เวลา AI อ่านโปรเจกต์

### การตัดสินใจรอบนี้
- ย้าย **`tools/`** เข้า **`ProjectYK_System/tools/`** พร้อม `_repo_paths.py` ให้ทุกสคริปต์ resolve `REPO_ROOT` / `APP_DIR` / `SYSTEM_DIR` ถูกต้อง
- ย้ายสคริปต์ราก **`_*.py`** ไป **`ProjectYK_System/dev_scripts/`** + `_paths.py`
- อัปเดต `phase2_import.bat`, `AGENT_BOOTSTRAP.md`, `MODULE_REGISTRY.md`, `CHANGELOG_MASTER.md`, `NEXT_ACTION_PLAN.md` (path ใหม่)
- เพิ่ม **`.cursorignore`** ที่ราก repo — ไม่ให้ Cursor index โฟลเดอร์ใหญ่/อ่อนไหวที่ไม่จำเป็นต่อการแก้โค้ดแอป

### สิ่งที่ทำแล้ว
- โครงสร้างรวมศูนย์ใต้ `ProjectYK_System/` สำหรับแอป + import CLI + dev scratch
- คำสั่งมาตรฐาน: จากราก repo ใช้ `python ProjectYK_System/tools/import_daily.py` (และคู่กัน)

### Action ถัดไป
- ถ้าเปิด Workspace แค่โฟลเดอร์ `ProjectYK_System` ใน Cursor จะประหยัด context ได้อีก (ไม่บังคับ)
- เอกสารเก่าใน `CONTEXT_LOG.md` บางแถวยังอ้าง `tools/...` แบบเดิม — อ่านร่วมกับ path ใหม่ได้ (`ProjectYK_System/tools/...`)

---

## 2026-04-30 (Session Summary #69 - รวม Salary/Fuel/Billing ใต้ data/)

### บริบทจากผู้ใช้
- อยากย้ายโฟลเดอร์ข้อมูลแบบ `Salary`, `Fuel`, `Billing` ไปหมวดหมู่ที่ถูกต้อง (เสนอ `docs` — ใช้ `data/` แทนเพราะไม่ใช่ markdown สเปก)

### การตัดสินใจรอบนี้
- สร้าง **`data/`** ที่ราก repo: `data/Salary`, `data/Fuel`, `data/Billing`
- **`.gitignore`**: รวมเป็น **`data/`** บรรทัดเดียว · **`.cursorignore`**: ignore ทั้ง `data/`

### สิ่งที่ทำแล้ว
- ย้ายโฟลเดอร์จริง + อัปเดตโค้ด (`_repo_paths`, import scripts, `payroll_slip`, `build_petty_cash_online`, `dev_scripts`)

### Action ถัดไป
- ถ้ามีสคริปต์/ลิงก์ **นอก repo** หรือ shortcut ชี้ไป `...\Project YK\Salary\` เดิม ต้องแก้เป็น `...\Project YK\data\Salary\`
- เอกสารเก่าใน repo ที่ยังเขียน `Salary/...` แบบเดิม = ประวัติ — path ปัจจุบันคือ **`data/Salary/...`**

---

## 2026-04-30 (Session Summary #70 - ย้าย TransportRateCalculator เข้า ProjectYK_System)

### บริบทจากผู้ใช้
- ต้องการให้ `TransportRateCalculator` อยู่รวมกับระบบหลัก เพราะมีการคำนวณสอดคล้องกัน และอนาคตอาจรวมเข้าแอป

### การตัดสินใจรอบนี้
- ย้ายโฟลเดอร์ **`TransportRateCalculator/`** → **`ProjectYK_System/TransportRateCalculator/`**
- ปรับ deploy (`deploy_one_click.bat`, `deploy.ps1`), `build_petty_cash_online.py`, `deploy_oatside_report*`, `.cursor/rules`, `AGENTS.md`, `MODULE_REGISTRY.md`, `.cursorignore`

### สิ่งที่ทำแล้ว
- โครงรวมศูนย์ใต้ `ProjectYK_System/` สำหรับแอป + import + TRC + สเปก

### Action ถัดไป
- ลิงก์เก่า/บุ๊กมาร์กที่เปิด `TransportRateCalculator/docs/...` จากราก repo ต้องเปลี่ยนเป็น **`ProjectYK_System/TransportRateCalculator/docs/...`**
- แชทเก่าที่ `@TransportRateCalculator` แบบ path เดิม — ใช้ path ใหม่เมื่ออ้างอิงไฟล์

---

## 2026-05-01 (Session Summary #71 - Oatside GPS: รวมต้นทางหลายช่วงก่อนปลายทางเดียว)

### บริบทจากผู้ใช้
- ตัวอย่าง **71-6802**: greedy จับคู่ได้เที่ยวที่เวลา “เข้าต้นทาง” แถวถัดไป **ก่อน** `Dest_In` ของเที่ยวก่อน ทำให้ลำดับเวลาอ่านแล้วขัดแย้ง — สมมติฐาน: เข้าต้นทางแล้วออกไม่ขึ้นของ กลับเข้าต้นทางอีกรอบ ก่อนไปปลายทางจริง
- **ต่อมา (โอ):** สงสัยว่าอาการผิดปกติบางส่วนอาจมาจาก **วง Geofence ฝั่งระบบ GPS** — จะลองปรับวงแล้วส่งไฟล์ export อัปเดตมาใหม่ (รอไฟล์แล้วค่อย rebuild รายงาน)

### การตัดสินใจรอบนี้
- หลัง `match_plate` เรียงคู่ตาม **`Origin_Out`** แล้วรวมช่วง: ถ้า `o_next.t_in < d_acc.t_in` ให้รวม `row_no` ต้นทาง + เลือกปลายทางแบบ **รอบแรก** ใช้ `dest.row_no == origin.row_no` ของช่วงที่เพิ่งต่อ (ถ้ามีหลายตัว feasible ใช้เวลาเดินทางสั้นสุด) · **รอบต่อ** ถ้า `d_acc` ยัง feasible หลัง `last_out` ให้ **เกาะ `d_acc`** (เที่ยวเดิม) แล้ว orphan ปลายทางอื่น
- **`origin_wait_h`** สำหรับต้นทางที่รวมหลายแถว = **ผลรวม** `(t_out - t_in)` รายช่วงจาก lookup `row_no` (ไม่ใช่ `last_out - first_in` เพราะรวมช่วงวิ่งว่างระหว่างออก-เข้า)
- ปลายทางที่ orphan → `rematch_orphan_dests_to_origins` กับต้นทางค้าง (เช่นเดิม)

### สิ่งที่ทำแล้ว
- แก้ `Oatside/build_oatside_reports.py` (`merge_chained_origin_pairs` + การคำนวณ wait ใน `build_trips`)
- รัน `python Oatside/build_oatside_reports.py` ผ่าน (ตัวอย่าง 71-6802 เที่ยว 14 เม.ย. สอดคล้อง narrative ผู้ใช้)

### Action ถัดไป
- หลัง deploy GitHub Pages ให้ hard refresh ดูรายงานใหม่
- ถ้ามีเคสที่ `row_no` ต้น/ปลายไม่ตรงกันในไฟล์จริง อาจต้องปรับ heuristic เลือกปลายทาง (หรือให้ผู้ใช้ยืนยันกฎธุรกิจ)
- เมื่อได้ไฟล์ GPS หลังปรับ Geofence: วางใน `Oatside/` → รัน `python Oatside/build_oatside_reports.py` (หรือ `deploy_oatside_report_one_click.bat`) แล้วเทียบทะเบียนเดิมที่เคยผิดปกติ

---

## 2026-05-01 (Session Summary #72 - Oatside: rebuild ด้วย export 01.05.2026 21:33)

### บริบทจากผู้ใช้
- วางไฟล์ใน `Oatside/` แล้ว ไม่ส่งไฟล์ผ่านแชท — ใช้ชื่อไฟล์ชัดเจนให้รัน build

### สิ่งที่ทำแล้ว
- รัน `python Oatside/build_oatside_reports.py` ด้วย `OATSIDE_ORIGIN` / `OATSIDE_DEST` ชี้ไฟล์ `...01.05.2026_21-33-31 Oatside.xlsx` และ `...21-33-53 P&G.xlsx` → **Trips 88 | Unmatched 32**; ออก `Oatside/Oatside_PG_Trip_Summary_By_Site.xlsx` + HTML ใต้ `Oatside/TransportRateCalculator/reports/oatside-apr2026`
- สุ่มตรวจ **71-6802**: เที่ยว 14 เม.ย. ยังเป็นโครง `10.2+10.3+10.4` → `Dest_In` 2026-04-14 09:56 (`travel` ~2.72 ชม. หลัง Geofence เลขเวลาเล็กน้อยจากรอบก่อน)

### Action ถัดไป
- ถ้าต้องการขึ้น GitHub Pages: รัน `deploy_oatside_report_one_click.bat` แล้ว hard refresh

---

## 2026-05-01 (Session Summary #73 - Oatside: guard ลำดับเวลา + deploy เลือกโฟลเดอร์ล่าสุด)

### บริบทจากผู้ใช้
- ถ้า `Origin_In` เที่ยวถัดไป **ก่อน** `Dest_Out` เที่ยวก่อนหน้า (ทะเบียนเดียวกัน) = ผิด → ให้ **เที่ยวก่อนหน้า** ไป Unmatched; ขอ deploy GitHub Pages อัตโนมัติ

### การตัดสินใจรอบนี้
- เพิ่ม `demote_chronology_violations`: เรียงเที่ยวตาม `Origin_In` ต่อทะเบียน วนจนนิ่ง — ถ้า `lst[i].o_in < lst[i-1].d_out` ให้ `pop` เที่ยว `i-1` แล้วแตกขาเป็น `Unmatched` (ต้นทางแยกตาม `row_no` + ปลายทางหนึ่งขา)
- แก้ `deploy_oatside_report.ps1`: เลือกโฟลเดอร์รายงานที่มี **`index.html` ใหม่สุด** ระหว่าง `Oatside/...`, `ProjectYK_System/...`, `TransportRateCalculator/...` (กัน copy ของเก่าเมื่อ build เขียนใต้ `Oatside/`)

### สิ่งที่ทำแล้ว
- แก้ `Oatside/build_oatside_reports.py` + รัน build (ชุด export 01.05.2026) → **Trips 87 | Unmatched 34**
- `deploy_oatside_report.ps1` → commit `Oatside report: chronology guard + rebuild` + **push** `transport-rate-calculator-repo`

### Action ถัดไป
- หน้า GitHub Pages: hard refresh หลัง Actions/เพจอัปเดต (~1–2 นาที)

---

## 2026-05-01 (Session Summary #74 - Oatside billing: 50% วันละ 1 เที่ยว + สรุปลูกค้า + override JSON)

### บริบทจากผู้ใช้
- ไม่คิด **ค่าเสียเวลา** (wait threshold) แล้ว — เก็บ **50%** เป็นหลักเมื่อวันนั้น **วิ่งได้ 1 เที่ยว** (matched ตาม `Dest_In`)
- ต้องการให้ user **แก้ manual ได้และระบบจำ** (เช่น วันที่ระบบจะเก็บ 50% แต่ความจริงไม่ได้กลับไปวิ่ง) และต้องการมุมมองให้ลูกค้าเห็นยอด **ทั้งแถวปกติ + 50%**

### การตัดสินใจรอบนี้
- ลบกฎ lost-time แบบรอรวม ≥ threshold — เหลือ **`one_trip_fifty_pct_details`**: วันละทะเบียนมี **1 matched trip** ต่อ `dest_date` → บวก **50% ของเรทวันนั้น** (ยกเว้น/บังคับด้วย JSON)
- ไฟล์ **`Oatside/oatside_billing_overrides.json`**: `exclude_50` / `include_50` + `note` ต่อคู่ `(plate, dest_date)`; env **`OATSIDE_OVERRIDES_JSON`** ชี้ path อื่นได้
- Excel เพิ่ม **`Customer_Summary`**, **`Plate_DestDay`**, เปลี่ยนชีตเป็น **`Surcharge_50pct_1Trip`**
- HTML summary: การ์ด Base / 50% / Total extra / **Customer grand** + ตาราง **Per plate / per Dest_In day**; หน้า `plates/*.html` มีตาราง “By Dest_In day” โชว์ `+50%` หรือ `1 trip (no +50%)`

### สิ่งที่ทำแล้ว
- แก้ `Oatside/build_oatside_reports.py` + สร้าง `Oatside/oatside_billing_overrides.json` ว่าง + ตัวอย่าง `docs/oatside_billing_overrides.example.json` + อัปเดต `OATSIDE_LOCAL_UPDATE_WITHOUT_UPLOAD.md`
- build + deploy GitHub Pages (`deploy_oatside_report.ps1`) สำเร็จ

### Action ถัดไป
- โอลองแก้ `oatside_billing_overrides.json` แล้วรัน build ทดสอบ 1 เคส

---

## 2026-05-01 (Session Summary #75 - Oatside: เรทเที่ยว 12-15 เม.ย. 8000 นอกนั้น 7500)

### บริบทจากผู้ใช้
- ปรับเรท: **12–15 เม.ย. = 8,000 บาท** · **วันอื่น = 7,500 บาท** (อ้างอิงวันที่ `Dest_In`)

### สิ่งที่ทำแล้ว
- แก้ `trip_rate_baht()` ใน `Oatside/build_oatside_reports.py` + ข้อความ subtitle ใน HTML
- อัปเดต `OATSIDE_TRIP_PAIRING_MERGE_HANDOFF.md`

### Action ถัดไป
- รัน `python Oatside/build_oatside_reports.py` + deploy ถ้าต้องการขึ้น GitHub Pages

---

## 2026-05-01 (Session Summary #76 - GitHub Org yk-logistics + ลิงก์ Pages ใหม่)

### บริบทจากผู้ใช้
- ย้าย repo `transport-rate-calculator` จาก user ส่วนตัวไป **Organization `yk-logistics`** เพื่อ URL ลูกค้าดูเป็นมืออาชีพ
- ถามว่าหลังย้ายแล้ว **ทำยังไงต่อ**

### การตัดสินใจรอบนี้
- ลิงก์สาธารณะที่ใช้ส่งลูกค้า/ทีม: **`https://yk-logistics.github.io/transport-rate-calculator/reports/oatside-apr2026/index.html`**
- เครื่องที่รัน `deploy_oatside_report_one_click.bat` ต้องให้โฟลเดอร์ clone มี **`origin`** ชี้ `github.com/yk-logistics/transport-rate-calculator` (ไม่ใช่ path user เดิม)

### สิ่งที่ทำแล้ว
- อัปเดต `README_DEPLOY.md` (ตัวอย่าง `git config` เป็น placeholder ไม่ผูกอีเมลส่วนตัวใน repo)
- เพิ่มคอมเมนต์ใน `deploy_oatside_report.ps1`, `deploy_oatside_report_one_click.bat`; เพิ่มหัวข้อลิงก์ใน `OATSIDE_LOCAL_UPDATE_WITHOUT_UPLOAD.md`
- บันทึก `CHANGELOG_MASTER.md`, `NEXT_ACTION_PLAN.md`, `CONTEXT_LOG.md` (session นี้)

### Action ถัดไป
- โอเปิดลิงก์ Pages ด้านบน hard refresh ยืนยันหน้าโหลดครบ
- ในโฟลเดอร์ `transport-rate-calculator-repo` (หรือชื่อที่ใช้): `git remote -v` → ถ้ายังเป็น URL เดิม ให้ `git remote set-url origin https://github.com/yk-logistics/transport-rate-calculator.git` แล้วลอง push อีกครั้ง

---

## 2026-05-01 (Session Summary #77 - Oatside: ไม่เก็บค่าชดเชยเที่ยวขาด min trips เมื่อใช้ชาร์จ 50%)

### บริบทจากผู้ใช้
- ต้องการ: **ถ้าเก็บ 50% (วันละ 1 เที่ยว) แล้ว ไม่ต้องมีค่าชดเชยเที่ยวขาด** (min 2 เที่ยว/คัน/วัน)

### การตัดสินใจรอบนี้
- เพิ่ม config **`charge_min_trip_shortfall`** (ค่าเริ่มต้น **`false`**) ใน `Oatside/oatside_config.json` + dataclass `OatsideConfig`
- เมื่อ **`false`**: ยอดลูกค้า = **ค่าเที่ยวปกติ (A) + ชาร์จ 50% (C)** เท่านั้น — **เงินค่าชดเชยเที่ยวขาด = 0** แต่ยังแสดงตัวเลข **เที่ยว commit / เที่ยวขาด** เป็นข้อมูลควบคุม
- เมื่อ **`true`**: พฤติกรรมเดิม (เก็บทั้งค่าชดเชย + 50%)

### สิ่งที่ทำแล้ว
- แก้ `Oatside/build_oatside_reports.py` (main / Excel Info+Customer_Summary / HTML subtitle+การ์ด+แยก Site)
- รัน `python Oatside/build_oatside_reports.py` ตรวจแล้ว — ตัวอย่าง: ยอดรวมลูกค้า **852,500** (= 665,500 + 187,000), การ์ดค่าชดเชย **0**

### Action ถัดไป
- ถ้าต้องการกลับไปเก็บค่าชดเชยแบบเดิม: ตั้ง `"charge_min_trip_shortfall": true` ใน `Oatside/oatside_config.json` แล้ว build ใหม่
- deploy GitHub Pages ตาม workflow เดิมเมื่อพร้อมส่งลูกค้า

---

## 2026-05-01 (Session Summary #78 - Oatside HTML: แสดง Unmatched ใน trips + หน้าทะเบียน)

### บริบทจากผู้ใช้
- ต้องการให้หน้า **เที่ยวทั้งหมด** (`trips.html`) และ **หน้าเฉพาะทะเบียน** (`plates/*.html`) แทรกรายการ **Unmatched** ให้เห็นด้วย

### การตัดสินใจรอบนี้
- เพิ่มฟังก์ชัน `unmatched_table_html()` — สร้างแถวตารางเหมือนชีต `Unmatched_Log` (Source, Plate, Device, Row, In, Out)
- `trips.html`: แบ่ง panel **Matched** + **Unmatched** ทั้งหมด
- `plates/*.html`: กรอง Unmatched เฉพาะทะเบียนนั้น — ถ้าไม่มีแสดงข้อความ **ไม่มี Unmatched**

### สิ่งที่ทำแล้ว
- แก้ `Oatside/build_oatside_reports.py` + รัน build ตรวจแล้ว

### Action ถัดไป
- deploy Pages เมื่อต้องการให้ลูกค้าเห็นบนเว็บ

---

## 2026-05-01 (Session Summary #79 - Oatside HTML: รวม Unmatched เข้าตารางเดียวกับ matched)

### บริบทจากผู้ใช้
- ต้องการให้ **Unmatched อยู่ในตารางเดียวกับ matched** — **เว้นช่อง** ถ้าฝั่งนั้นยังไม่มีเวลา/วันที่จับคู่ (ต้นทางหรือปลายทาง)

### การตัดสินใจรอบนี้
- แทนที่ `unmatched_table_html` ด้วย **`unmatched_merged_trip_rows_html()`** — คอลัมน์เดียวกับ `trip_row` (Origin/Dest date, Site, ทะเบียน, In/Out ทั้งสี่ฯลฯ)
- **UM-O** (Origin unmatched): มีวัน/เวลาต้นทาง — วันและเวลา **ปลายทางเป็น —**
- **UM-D** (Destination unmatched): วัน/เวลา **ต้นทางเป็น —** — มีวัน/เวลาปลายทาง
- คอลัมน์ Orig Wait / Travel / Dest Wait ของแถว unmatched ใช้ **—** (ไม่คำนวณรอบเดินทาง)
- `trips.html` และ `plates/*.html` ใช้ตารางเดียว; แถว unmatched มี class `um` + badge สี

### สิ่งที่ทำแล้ว
- แก้ `Oatside/build_oatside_reports.py` + รัน build ตรวจแล้ว (UM-O+UM-D = จำนวน unmatched)

### Action ถัดไป
- deploy GitHub Pages เมื่อต้องการ

---

## 2026-05-01 (Session Summary #80 - Oatside HTML: แทรก Unmatched ตาม timeline กับ matched)

### บริบทจากผู้ใช้
- ต้องการให้แถว **Unmatched แทรกระหว่างวัน/เวลาที่ต่อกัน** กับ matched — ทั้งหน้ารวมและหน้าแยกทะเบียน

### การตัดสินใจรอบนี้
- **`interleaved_matched_unmatched_rows_html()`** — รวม matched + unmatched แล้ว sort ด้วย **`(เวลาเรียง, tie-break)`**
  - Matched: ใช้ **`t.d_in`** (Dest In)
  - Unmatched: ใช้ **`leg.t_in`** ของขานั้น
  - tie-break: matched ก่อน unmatched เมื่อเวลาเท่ากัน แล้วตามทะเบียน/แถว
- แยก **`unmatched_merged_trip_one_row_html()`** + flag **`include_plate_column`** — หน้า `trips.html` มีคอลัมน์ทะเบียน, หน้า `plates/*.html` ไม่มี (ใส่ badge UM คู่ Site)
- เพิ่ม **`trip_row_plate`** (รองรับ ABNORMAL badge หลังชื่อ Site)

### สิ่งที่ทำแล้ว
- แก้ `Oatside/build_oatside_reports.py` + `from typing import Callable` + รัน build ตรวจแล้ว (ตาราง `trips.html` มีการสลับ M/U หลายจุด)

### Action ถัดไป
- deploy เมื่อพร้อม

---

## 2026-05-01 (Session Summary #81 - Oatside: แก้ merge ต้นทางยาวผิด + build ใหม่ + เอกสาร)

### บริบทจากผู้ใช้
- พบว่าแถว Excel ต้นทาง (เช่น 64) ไม่ถูกแยกเป็นรอบ Origin เอง แต่ถูก **รวบ Origin_Out ไปกับแถวถัดไป** (ออกตี 1) เมื่อปลายทางมาช้า
- ขอแก้แล้ว **import/build อีก 1 รอบ** และ **บันทึก .md**

### การตัดสินใจรอบนี้
- สาเหตุ: `merge_chained_origin_pairs` รวม Origin ถัดไปเมื่อ `o2.t_in < d_acc.t_in` โดยไม่ดูว่ามี **ช่องว่างกลับฮับ** ระหว่าง `o_acc.t_out` กับ `o2.t_in` หรือไม่
- แก้: ถ้า `hours(o_acc.t_out, o2.t_in) > max_origin_chain_gap_h` → **หยุดรวม** — ค่า default **3 ชม.** ปรับได้ใน `Oatside/oatside_config.json`
- เอกสาร: **`ProjectYK_System/TransportRateCalculator/docs/OATSIDE_ORIGIN_CHAIN_MERGE_FIX.md`**
- อัปเดต `oatside_config.json` บนเครื่องให้มี key ใหม่ (ถ้ายังไม่มี)

### สิ่งที่ทำแล้ว
- แก้ `Oatside/build_oatside_reports.py` (`merge_chained_origin_pairs(..., max_gap_h)`, `OatsideConfig.max_origin_chain_gap_h`, loader, Info sheet)
- รัน `python Oatside/build_oatside_reports.py` สำเร็จ (ชุดไฟล์ GPS ปัจจุบันบนเครื่อง: Trips 75 / Unmatched 76 — ตัวเลขอาจเปลี่ยนตาม export)

### Action ถัดไป
- โอเทียบทะเบียน `71-9629` (และคันอื่น) กับ Excel รอบเดียวกัน — ถ้า unmatched เยอะเกินจริง ลองปรับ `max_origin_chain_gap_h` ทีละขั้นแล้ว build ซ้ำ
- deploy GitHub Pages เมื่อพร้อม

---

## 2026-05-01 (Session Summary #82 - Oatside: ไม่รวบ Origin เลย + ไฟล์ GPS 02.05.2026 + เอกสาร)

### บริบทจากผู้ใช้
- ต้องการ **ไม่รวบ Origin แบบ chain-merge เลย** (คนละระดับกับแค่จำกัดช่องว่างชม.)
- ดึงไฟล์ export ใหม่ชื่อ **`...02.05.2026_06-56-46 Oatside.xlsx`** และ **`...02.05.2026_06-58-42 P&G.xlsx`**
- ให้ **บันทึก .md** อธิบายพฤติกรรมและวิธีรัน

### การตัดสินใจรอบนี้
- เพิ่ม **`enable_origin_chain_merge`** ใน `OatsideConfig` + `oatside_config.json` template (default **false**) — ถ้า false ไม่เรียก `merge_chained_origin_pairs`
- ถ้า true ยังใช้ **`max_origin_chain_gap_h`** ตามเอกสารเดิม
- ขยาย **`OATSIDE_ORIGIN_CHAIN_MERGE_FIX.md`**: โหมดปิด merge, ตัวอย่าง `OATSIDE_ORIGIN` / `OATSIDE_DEST`, ลิงก์สคริปต์ build ตัวอย่าง
- สคริปต์ **`ProjectYK_System/tools/run_oatside_may02_build.py`** ชี้ไฟล์วันที่ 02.05.2026 สองชื่อด้านบน

### สิ่งที่ทำแล้ว
- แก้ `Oatside/build_oatside_reports.py` (config + `build_trips` + Excel Info)
- รัน build สำเร็จด้วย env ชี้ไฟล์ใหม่: **Trips 89 | Unmatched 49**

### Action ถัดไป
- โอเปิด `Oatside/TransportRateCalculator/reports/oatside-apr2026/index.html` (หรือ path ที่ build พิมพ์) เทียบกับ Excel
- ถ้าต้องการกลับไปรวบ Origin แบบเดิม (มี gap guard): ตั้ง `enable_origin_chain_merge`: **true** ใน `oatside_config.json` แล้ว build ซ้ำ
- deploy GitHub Pages เมื่อพร้อม

---

## 2026-05-01 (Session Summary #83 - Oatside: อธิบาย UM 71-6802 + build ไฟล์ Origin 07-15-32)

### บริบทจากผู้ใช้
- ถามว่าทำไมปลายทาง 18:46–19:20 ไม่ match กับต้นทาง 14:22–16:58 (ทะเบียน 71-6802 จากสครีนช็อต)
- ขออัปเดตรายงานด้วยไฟล์ **`...02.05.2026_07-15-32 Oatside.xlsx`**

### การตัดสินใจรอบนี้
- อธิบายเป็นภาษาธุรกิจ/ลำดับ logic: **ไม่ใช่เพราะช่องว่าง ~1.8 ชม. เกิน `max_travel_h`** — สาเหตุหลักคือ **`match_plate` (greedy)** + **`demote_chronology_violations`** เมื่อไฟล์ต้นทางแยกหลายแถว; export ใหม่รวมช่วงต้นทางเป็นแถวเดียวแล้วจับคู่ 18:46 ได้
- อัปเดต **`OATSIDE_TRIP_PAIRING_MERGE_HANDOFF.md`** (หัวข้อย่อยกรณีจอ UM) + **`OATSIDE_ORIGIN_CHAIN_MERGE_FIX.md`** (ลิงก์ไป handoff)
- อัปเดต **`ProjectYK_System/tools/run_oatside_may02_build.py`** ชี้ Origin `07-15-32`

### สิ่งที่ทำแล้ว
- รัน `build_oatside_reports.py` ชุด Origin `07-15-32` + P&G `06-58-42` → **Trips 90 | Unmatched 45**
- เครื่องมือชั่วคราววิเคราะห์ทะเบียน: `ProjectYK_System/tools/debug_oatside_plate.py` (optional)

### Action ถัดไป
- โอเปิดหน้า `plates/71-6802.html` ในรายงาน HTML ชุดใหม่เทียบกับ Excel
- ถ้ามี export P&G คู่เวลาเดียวกับ Origin 07-15-32 ให้แทนที่ `OATSIDE_DEST` / ชื่อใน `run_oatside_may02_build.py` แล้ว build ซ้ำ

---

## 2026-05-01 (Session Summary #84 - Oatside: แก้ `match_plate` ลด UM 71-6802 — ไม่ถอด demote)

### บริบทจากผู้ใช้
- ตัวอย่าง **71-6802** ช่วง 15–16 เม.ย. ต้นทาง/ปลายทางเรียงเวลาแล้วน่าจะคู่กันได้ แต่ขึ้น UM หลายแถว
- ถามว่าเกี่ยวกับ **`demote_chronology_violations`** หรือไม่ และขอแก้ให้ถูกต้อง

### การตัดสินใจรอบนี้
- **เก็บ `demote_chronology_violations` ไว้** — ยังใช้กรองเที่ยวที่ลำดับเวลาเป็นไปไม่ได้จริง
- **รากปัญหา:** `match_plate` แบบ **origin-first + เลือก Dest เดินทางสั้นสุด** ทำให้ช่วงต้นทางสั้นแย่ง `Dest` ของช่วงยาว → เหลือ UM แล้วไปชน demote เป็นวง
- **แก้:** เปลี่ยนเป็น **ไล่ `Dest` ตามเวลา** แล้วจับกับ **ต้นทางที่ `Origin_Out` ล่าสุด** (ก่อน `Dest_In`) ที่ยังว่างและผ่าน `feasible`

### สิ่งที่ทำแล้ว
- แก้ `Oatside/build_oatside_reports.py` (`match_plate`)
- รัน build ชุด Origin `07-15-32` + P&G `06-58-42` → **Trips 105 | Unmatched 15** (เดิมหลัง merge ปิดแบบ origin-first ~90/45)
- อัปเดต **`OATSIDE_TRIP_PAIRING_MERGE_HANDOFF.md`** §4 + กรณี 71-6802, **`OATSIDE_ORIGIN_CHAIN_MERGE_FIX.md`** (ตัวเลข build)

### Action ถัดไป
- โอสุ่มเทียบทะเบียนอื่นใน HTML ว่าคู่เที่ยวยังสมเหตุสมผลกับงานจริง
- ถ้าพบเที่ยวที่ “เดินทางยาวผิดจริง” ให้ดู `travel_flag` / IQR และข้อมูล GPS ก่อนย้อนอัลกอริทึม

---

## 2026-05-02 (Session Summary #83 - หน้า HTML pitch One Platform สำหรับ repo yk-logistics)

### บริบทจากผู้ใช้
- มี repo บริษัท **`yk-logistics`** (Transport rate calculator + Oatside บน GitHub Pages แล้ว)
- ต้องการหน้า HTML สรุปว่าระบบ One Platform มีอะไร ทำถึงไหน — ส่งลิงก์ให้พ่อดู / ประกอบขออนุมัติงบเครื่องมือ ~200 USD

### การตัดสินใจรอบนี้
- สร้าง **static เดียว** ใต้ `ProjectYK_System/docs-public/one-platform-status/` — ไม่ผูก DB ไม่มีตัวเลขจริง
- ลิงก์ Calculator ชี้ **root Pages** `https://yk-logistics.github.io/transport-rate-calculator/` (สอดคล้อง `deploy.ps1` ที่ copy เป็น `index.html`)
- ลิงก์ Oatside ใช้ path ตัวอย่าง `reports/oatside-apr2026/index.html` — ถ้าโฟลเดอร์รายงานเปลี่ยนชื่อให้แก้ใน `index.html` หลัง deploy

### สิ่งที่ทำแล้ว
- `index.html` (Tailwind CDN + Sarabun) + `README_DEPLOY.md` คำสั่ง copy ไป `reports/one-platform-status/`
- อัปเดต `CHANGELOG_MASTER.md`, `NEXT_ACTION_PLAN.md`, `CONTEXT_LOG.md` (session นี้)

### Action ถัดไป
- โอคัดลอกโฟลเดอร์ไป clone `transport-rate-calculator` → push → ส่งลิงก์ `.../reports/one-platform-status/index.html` ให้พ่อ

---

## 2026-05-02 (Session Summary #84 - One Platform pitch: สถิติจริง + push GitHub)

### บริบทจากผู้ใช้
- ขอให้หน้า pitch **โชว์ข้อมูลจริง** และให้ **จัดการ push GitHub** ให้

### การตัดสินใจรอบนี้
- โชว์เฉพาะ **aggregate ปลอดภัยต่อ URL สาธารณะ**: จำนวนแถวตารางหลัก, ช่วงวันที่งานรายวัน/สดย่อย, จำนวนพนักงาน/รถแยกตาม `home_site_code`, PayRun จำนวนรอบ + สถานะ — **ไม่ใส่** ชื่อเต็ม, ทะเบียน, `net_pay`, รายการสดย่อยรายบรรทัด
- สคริปต์ **`build_public_stats.py`** เขียน **`public-stats.json`** จาก `ProjectYK_System/app/app.db`; หน้า **`index.html`** ใช้ `fetch('public-stats.json')`
- ใช้ clone ที่มีอยู่ **`transport-rate-calculator-repo`** (`origin` = `yk-logistics/transport-rate-calculator`) — copy ไป `reports/one-platform-status/` → commit → **push สำเร็จ**

### สิ่งที่ทำแล้ว
- อัปเดต `build_public_stats.py` (รวม `payrun` / `payrunitem` / `payrun_by_status`)
- อัปเดต `index.html` (ส่วน stats + JS), `README_DEPLOY.md`, `CHANGELOG_MASTER.md`, `NEXT_ACTION_PLAN.md`

### Action ถัดไป
- รอ GitHub Pages build ~1–2 นาที แล้วเปิดลิงก์: `https://yk-logistics.github.io/transport-rate-calculator/reports/one-platform-status/index.html`
- ถ้าไม่ต้องการให้คู่แข่งเห็นขนาดกิจการจากตัวเลขรวม: ลบ `public-stats.json` ออกจาก repo สาธารณะ หรือย้ายไปโฮสต์ส่วนตัว

---

## 2026-05-02 (Session Summary #85 - Pitch: รูปหน้า Daily จริง + ตัดงบ/Open-book + อธิบาย Pages vs แอป)

### บริบทจากผู้ใช้
- ไม่ต้องการข้อความงบเครื่องมือ AI/IDE (~200 USD) และไม่ต้องการพูดถึง Open-book / Profit share
- อยากให้มีหน้าระบบจริงแบบรูปแนบบน Git — ถามว่าทำหน้าจริงขึ้น git ได้ไหม

### การตัดสินใจรอบนี้
- **หน้าโต้ตอบแบบ `/daily` เต็มระบบ** ต้องมี FastAPI + DB — GitHub Pages ทำไม่ได้; ใส่ **สกรีนช็อตหน้า Daily จริง** ใน repo + อธิบายข้อจำกัดบนหน้าเว็บ
- คัดลอกรูปจาก assets ของ Cursor → `assets/screenshot-daily-desktop.png` — push `yk-logistics/transport-rate-calculator` อีก commit

### สิ่งที่ทำแล้ว
- แก้ `index.html` (ลบ section งบ, ลบ bullet Open-book, เพิ่ม section รูป + คำอธิบาย)
- `README_DEPLOY.md` อัปเดตเรื่องรวมโฟลเดอร์ `assets/`

### Action ถัดไป
- ถ้าต้องการ **ลองใช้จริงผ่านลิงก์** (filter/sort) → deploy แอปไป PaaS/VPS + ล็อกสิทธิ์ (ไม่ใช่แค่ Pages)

---

## 2026-05-02 (Session Summary #86 - โฮสต์ฟรี: Neon + Render + Basic auth + ย้าย SQLite)

### บริบทจากผู้ใช้
- เข้าได้แค่พ่อ/คนใน, อยากฟรี, ข้อมูลยกจากเครื่องได้แล้วค่อยลบทีหลัง

### การตัดสินใจรอบนี้
- **Neon** (Postgres ฟรี) + **Render** Web free + รัน **`sqlite_to_postgres.py --wipe`** บนเครื่องก่อน deploy
- ล็อกด้วย **HTTP Basic** เมื่อตั้ง `YK_PREVIEW_AUTH=1` + user/password
- `main.py`: `create_all` บน Postgres ไม่รัน `_ensure_column` (เฉพาะ SQLite)

### สิ่งที่ทำแล้ว
- `db_config.py`, `preview_auth.py`, แก้ `main.py` / `requirements.txt`, `tools/sqlite_to_postgres.py`, `docs/HOSTING_FREE_DEMO_TH.md`, `render.yaml`, `AGENT_BOOTSTRAP.md`, `CHANGELOG_MASTER.md`

### Action ถัดไป
- โอทำตาม `HOSTING_FREE_DEMO_TH.md` → ทดสอบ URL Render หลังตั้ง env
- รันบนเครื่อง: **`ProjectYK_System/tools/cloud_demo_setup.ps1`** หลังได้ `DATABASE_URL` จาก Neon

---

## 2026-05-02 (Session Summary #87 - Payroll + Petty ภาพรวม + แก้ guardrail unlinked `site_code` ว่าง)

### บริบทจากผู้ใช้
- ขอภาพรวม payroll + petty แล้วตรวจความผิดพลาด

### การตัดสินใจรอบนี้
- **DB จริง**: รายการหักสดย่อยที่ยังไม่ผูกคนขับ (`pending` + `driver_id` null) รอบ `2026-03` **33 แถว ~23,716 บาท** และ `2026-04` **353 แถว ~205,356 บาท** — **`site_code` ว่างทั้งหมด**
- **บั๊กระบบ**: แบนเนอร์ payroll / **finalize gate** / ตัวเลข stale petty กรองแค่ `PettyCashTxn.site_code == รอบ` → **ไม่เห็นและไม่บล็อก**รายการที่ไซต์ว่าง (หลุมเงียบ)
- **แก้**: `_petty_unlinked_predicates_for_payrun` ใน `main.py` — นับรวม `site` ตรงรอบ **หรือ** `site_code` ว่าง/null · ปรับ `_detect_payrun_stale` petty แบบเดียวกัน · ลิงก์ `/petty-cash` ใช้ `cycle=` แทน `site=` เท่านั้น
- **กันหลุมอนาคต**: `_sum_petty_cash_deduction`, `_sum_ayu_toll_deduction`, `payroll_employee_detail`, `payroll_slip` — รวมแถว `site_code` ว่างเมื่อมี `driver_id` แล้ว

### Action ถัดไป
- เปิด `/payroll/{BIGC|AYU|LCB 2026-03|04}` → กด **คำนวณใหม่** หลังแก้สดย่อย/ผูกคนขับ + ใส่ **ไซต์** ในแถวที่ว่าง
- `/petty-cash?cycle=2026-04&unlinked=1&deduct=1&dstatus=pending` แก้ทีละรายการหรือ batch ตามนโยบาย

---

## 2026-05-02 (Session Summary #88 - Oatside Pages: เปลี่ยน path URL + ลบลิงก์เก่า)

### บริบทจากผู้ใช้
- ต้องการ **เปลี่ยนแค่ URL** รายงาน Oatside บน GitHub Pages (ไม่ปิดทั้งเว็บ) หลังแชร์ลิงก์เก่าในไลน์กลุ่ม

### การตัดสินใจรอบนี้
- **`deploy_oatside_report.ps1`**: พารามิเตอร์ **`PagesReportSlug`** default `oatside-pg-2026` — copy รายงานไป `reports/<slug>/` บน clone `transport-rate-calculator`
- **`RemoveLegacyApr2026`** (switch): ถ้าเปิด → `git rm -r reports/oatside-apr2026` ให้ลิงก์ `…/oatside-apr2026/…` เป็น **404** หลัง push
- **`deploy_oatside_report_one_click.bat`**: ส่ง `-PagesReportSlug "oatside-pg-2026" -RemoveLegacyApr2026`
- อัปเดตลิงก์ใน **`OATSIDE_LOCAL_UPDATE_WITHOUT_UPLOAD.md`**, **`NEXT_ACTION_PLAN.md`**, **`docs-public/one-platform-status/index.html`**, **`CHANGELOG_MASTER.md`**

### สิ่งที่ทำแล้ว
- แก้สคริปต์ + เอกสาร (การ **push** ต้องรันบนเครื่องโอที่มี clone + สิทธิ์ GitHub)

### Action ถัดไป
- โอรัน **`deploy_oatside_report_one_click.bat`** แล้วเช็ก URL ใหม่: `https://yk-logistics.github.io/transport-rate-calculator/reports/oatside-pg-2026/index.html`
- ถ้าไม่ต้องการลบของเก่า: รัน `deploy_oatside_report.ps1` **โดยไม่ใส่** `-RemoveLegacyApr2026`

---

## 2026-05-02 (Session Summary #89 - Oatside: จำนวนเที่ยวต่อวันให้ลูกค้า + push git)

### บริบทจากผู้ใช้
- ลูกค้าต้องการ **จำนวนเที่ยวต่อวัน** — ถามว่าระบบทำแล้วหรือยัง ขอให้ทำและ **อัป git**

### การตัดสินใจรอบนี้
- เดิมมี **`Daily_Activity`** / ตารางกิจกรรมรายวันใน HTML ที่มีคอลัมน์เที่ยวจริง แต่ยังไม่มีชีต/บล็อกที่เน้นคำว่า “ให้ลูกค้า” แบบสั้น ๆ
- เพิ่ม **`customer_trips_per_day_rows()`** — รวม **matched** ตาม `dest_date` (วัน `Dest_In`) + นับจำนวนรถที่มีเที่ยววันนั้น
- Excel ชีต **`Customer_Trips_Per_Day`**; หน้า **`index.html`** ตาราง **สรุปให้ลูกค้า — จำนวนเที่ยวต่อวัน (matched)**

### สิ่งที่ทำแล้ว
- แก้ `Oatside/build_oatside_reports.py` + รัน `build_oatside_reports.py` ผ่าน (Trips 105 / Unmatched 15)
- อัปเดต **`OATSIDE_TRIP_PAIRING_MERGE_HANDOFF.md`**, **`OATSIDE_LOCAL_UPDATE_WITHOUT_UPLOAD.md`**, **`CHANGELOG_MASTER.md`**

### Action ถัดไป
- โอรัน **`deploy_oatside_report_one_click.bat`** เพื่ออัปเว็บ GitHub Pages
- ถ้าต้องการนับตาม **วันอื่น** (เช่น Origin) แจ้งมาได้ — ปัจจุบันตรงกับหลัก billing ที่ใช้ `Dest_In`
