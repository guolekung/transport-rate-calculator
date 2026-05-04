# Oatside / P&G — รายงานลูกค้า (เงื่อนไข UI + Excel ที่ตกลง)

เอกสารนี้สรุป **สิ่งที่ต้องมี** ใน `Oatside/build_oatside_reports.py` และผลลัพธ์หลังรัน build — ใช้เก็บบริบทข้ามแชท / กันหลงเมื่อ deploy หรือ reset ไฟล์

## 1) Pipeline หลังรัน `python Oatside/build_oatside_reports.py`

1. สร้างไฟล์รวมทุกชีต: `Oatside/Oatside_PG_Trip_Summary_By_Site.xlsx` (ตำแหน่งเดิมต่อโฟลเดอร์ Oatside)
2. จัดรูปทั้ง workbook ด้วย `beautify_oatside_workbook` ก่อน save
3. สร้างรายงาน HTML ใต้  
   `ProjectYK_System/TransportRateCalculator/reports/oatside-apr2026/`  
   (บน GitHub Pages อาจ deploy เป็น slug อื่น เช่น `oatside-pg-2026` — ดูสคริปต์ deploy)
4. แยก Excel รายตารางลง `…/exports/` ด้วย `write_split_excel_exports` — ไฟล์ตาม mapping ชีต → ชื่อไฟล์ (ดู `OATSIDE_EXPORT_TABLES` ใน builder)

## 2) หน้า `index.html` (สรุป)

- **ไม่** แสดงแผง “ดาวน์โหลด Excel แยกตาราง” ยาวทั้งหน้า (ไม่ใช้ `{html_export_downloads_block()}` ในเนื้อหา index)
- **มี Hero (`hero-trips`)**: เน้นชวนไป **เที่ยวทั้งหมด** (`trips.html`) + ปุ่มหลัก **เปิดเที่ยวทั้งหมด**
- **แถบรอง (`nav-secondary`)**: ลิงก์ไป `trips.html` + ลิงก์ดาวน์โหลด **ไฟล์ Excel รวมทุกชีต** (`../../../Oatside/Oatside_PG_Trip_Summary_By_Site.xlsx`)
- **ไม่** แสดงบล็อก “คำอธิบายสี / ไฮไลต์ชั่วโมงรอ” (ลบออกจากสรุป — รายละเอียดอยู่ในเที่ยว/แผ่นงานถ้าต้องการภายหลัง)
- **แต่ละหัวข้อหลัก (1)(2)(3), Audit, รายทะเบียน)** ใช้ `<details class='section-fold'>` และหัวแบบ **`section-sum-row`**:
  - ซ้าย: ข้อความหัวข้อ (`sum-main`)
  - ขวา: ลิงก์ **ดาวน์โหลด Excel** ไปที่ `exports/<ชื่อไฟล์>.xlsx` (`sum-dl`) — helper `_xlsx_dl(fname, short)` อยู่ใน scope ของ `write_html` ตอนสร้าง `idx`

### แมปหัวข้อ → ไฟล์ `exports/` (ลูกค้า)

| หัวข้อ | ไฟล์ |
|--------|------|
| (1) จำนวนเที่ยวต่อวัน | `01_CPD_MatchedTripsPerDay.xlsx` |
| (2) เดลี่รถทุกคัน | `02_Plate_DestDay_Daily.xlsx` |
| (3) Unmatched | `03_Unmatched_Legs.xlsx` |
| Audit Log | `04_Audit_Log.xlsx` |
| รายทะเบียน | `02_Plate_DestDay_Daily.xlsx` (ซ้ำตารางเดลี่ — ตามที่ตกลง) |

- **Audit**: ข้อความหัวต้องเรียงเป็น **`(คลิกเพื่อขยาย) Audit Log — …`** และ CSS หัวแถวต้องให้ลิงก์ Excel **ชิดขวา** (`summary.section-sum-row` แบบ `width:100%`, `sum-dl{margin-left:auto}`)

### Unmatched — เวลา (ชม.)

- **อยู่จุด (ชม.)** = `t_out − t_in` ของแถว Unmatched นั้น (ระยะอยู่ที่จุดก่อนออก)
- **ถึงเข้าครั้งถัดไป (ชม.)** = จาก `t_out` ของแถวนี้ ถึง `t_in` ของเหตุการณ์ถัดไปบนทะเบียนเดียวกัน (เรียงจากรวมแถว Origin+Dest ตามเวลาเข้า) — ถ้าไม่มีแถวถัดไปแสดง `—`
- ชีต Excel **`Unmatched_Log`** มีคอลัมน์ **`Dwell_h`**, **`Gap_to_next_In_h`** สอดคล้องกัน
- หน้า **`trips.html`** / **`plates/*.html`**: แถว matched ใช้ `—` ในสองคอลัมน์นี้; แถว UM แสดงค่าจริง

## 3) หน้า `trips.html` (เที่ยวทั้งหมด — hero ของลูกค้า)

- หัว `h1` มี **แท็ก** `trips-tag` (เช่น “หน้าหลักลูกค้า”) + บรรทัดนำ (`trips-lead`)
- **แถบนำทาง**: กลับ `index.html` + ลิงก์ **Excel รวมทุกชีต** (path เดียวกับหน้าแรก)
- ตารางหลัก:
  - แถวกรองทะเบียน + search (`filter-bar`, `tripsPlateFilter`, `tripsPlateQuery`)
  - `<table id='tripsAllTable'>` + แถวข้อมูลมี `data-plate` สำหรับกรอง
  - หัวแผงเป็น **`panel-title-row`**: ซ้ายหัวข้อ · ขวาลิงก์ **`exports/05_Trip_Detail.xlsx`** (Trip Detail)
- มีสคริปต์ `_TRIPS_FILTER_JS` ต่อท้ายเนื้อหา HTML

## 4) CSS ที่เกี่ยวข้อง (สรุป)

- `hero-trips`, `btn-primary`, `nav-secondary`
- `section-sum-row`, `sum-main`, `sum-dl`, `xlsx-dl`
- `panel-title-row`, `trips-tag`, `trips-lead`
- `filter-bar` + `section-fold` / `section-sum` (จากพับหัวข้อ)

## 5) เมื่อโค้ด “หาย” หรือ deploy สับสน

- **Calculator `deploy.ps1`** แตะแค่ `transport_rate_calculator.html` → `index.html` ที่ราก repo — **ไม่แก้** `Oatside/build_oatside_reports.py`
- ถ้า UI รายงาน Oatside ไม่ตรงเอกสารนี้: ใช้สคริปต์ใน `ProjectYK_System/tools/` ตามลำดับที่บันทึกใน `CONTEXT_LOG` (หรือ restore จาก git/`reflog` ถ้ามี)

## 6) Checklist หลัง build (โอ vibe-test)

- [ ] โฟลเดอร์รายงานมี `exports/` และไฟล์ `01_…` ถึง `05_…` อย่างน้อยตามชีตที่มีข้อมูล
- [ ] `index.html`: มี hero + **ไม่มี**แผงดาวน์โหลดยาวกลางหน้า + แต่ละ section มีปุ่มขวา
- [ ] `trips.html`: กรองทะเบียนได้ + ปุ่ม Trip Detail ขวาหัวตาราง
- [ ] Hard refresh (Ctrl+F5) เมื่อเปิดไฟล์ในเบราว์เซอร์
