# อัปเดตไฟล์ GPS Oatside โดยไม่ส่งไฟล์ผ่านแชท

โฟลเดอร์ที่ใช้วางไฟล์บนเครื่องโอ:

`C:\Users\Home\Desktop\Project YK\Oatside`

## ขั้นตอน

1. **คัดลอก** ไฟล์ Excel export จากระบบ GPS มาวางในโฟลเดอร์ด้านบน (แทนของเก่าหรือวางคู่ใหม่ — สคริปต์เลือกไฟล์ที่ **แก้ล่าสุด** ตามเวลาไฟล์)
2. **ชื่อไฟล์** (ให้ตรงกับที่สคริปต์ค้นหา):
   - ต้นทาง: ชื่อมี **`Oatside`** และไม่ใช่ไฟล์สรุป `Oatside_PG_Trip_Summary...`
   - ปลายทาง: ชื่อมี **`P&G`** หรือคำว่า **เวลล์โกล** (ตามที่เคยใช้)
3. เปิด **PowerShell** แล้วรัน:

```bat
cd "C:\Users\Home\Desktop\Project YK"
python Oatside\build_oatside_reports.py
```

4. ดูผลท้ายคอนโซล — จะบอก path ของ **Excel** และ **HTML** (ใน Excel มีชีต **`Customer_Trips_Per_Day`** = จำนวนเที่ยว matched รวมต่อวันตาม `Dest_In` + จำนวนรถ)
5. (ถ้าต้องการ deploy เว็บ) จากรากโปรเจกต์รัน `deploy_oatside_report_one_click.bat`

## ลิงก์รายงานบนเว็บ (GitHub Pages — org `yk-logistics`)

หลัง deploy สำเร็จ รอ GitHub Actions/Pages ~1–2 นาที แล้วเปิด:

`https://yk-logistics.github.io/transport-rate-calculator/reports/oatside-pg-2026/index.html`

ถ้าเคยบันทึกลิงก์แบบ `…github.io/…` ใต้ user เดิม ให้เปลี่ยนมาใช้ URL ด้านบนเมื่อส่งลูกค้า

### เปลี่ยนเฉพาะ path บนเว็บ (ลิงก์เก่า 404 — Pages ยังเปิด)

รายงานถูก deploy ไปที่ **`reports/oatside-pg-2026/`** แทน `reports/oatside-apr2026/`  
จากราก Project YK รัน **`deploy_oatside_report_one_click.bat`** — สคริปต์จะ **ลบโฟลเดอร์เก่า** `reports/oatside-apr2026` บน clone แล้ว push (ลิงก์ `…/oatside-apr2026/…` ในไลน์จะเข้าไม่ได้)

ปรับชื่อ path เองได้:

```powershell
.\deploy_oatside_report.ps1 -PagesReportSlug "ชื่อโฟลเดอร์ใหม่"
```

(ไม่ใส่ `-RemoveLegacyApr2026` = ไม่ลบโฟลเดอร์เก่า `reports/oatside-apr2026` — เก็บสอง path พร้อมกันได้ชั่วคราว)

### ถอดรายงานทั้งโฟลเดอร์ (ไม่ย้าย path ใหม่)

บน clone ของ **`yk-logistics/transport-rate-calculator`** (branch เดียวกับที่ Pages ใช้):

```powershell
cd "C:\path\to\transport-rate-calculator-repo"
git checkout main
git pull
git rm -r reports/oatside-pg-2026    # หรือชื่อโฟลเดอร์ที่ใช้อยู่จริง
git commit -m "Remove public Oatside report"
git push
```

**ทางเลือกแทนการลบทิ้ง:** แทนที่ `index.html` / `trips.html` เป็นหน้าสั้น ๆ ว่า “หยุดเผยแพร่แล้ว”

**ข้อจำกัดที่ต้องรู้ (ไม่ใช่ 100% ลบจากโลก):**

- **แคชไลน์ / แคชเบราว์เซอร์** — บางเครื่องอาจเห็นหน้าเก่าชั่วคราว  
- ถ้าใคร **บันทึกไฟล์ / สกรีนช็อต / Web Archive** ไว้แล้ว — การลบบน GitHub **กู้คืนจากมือคนนั้นไม่ได้**  
- แชร์จำกัด: ใช้ path ที่เดาไม่ง่าย + แชร์เฉพาะคนที่ต้องการ หรือโฮสต์ที่มี **รหัสผ่าน** (แนว `HOSTING_FREE_DEMO_TH.md`)

## ในแชทกับ AI

ไม่ต้องแนบไฟล์ — พิมพ์ว่า **วางไฟล์ใน `Oatside` แล้ว** + ชื่อไฟล์หรือวันที่ export ก็พอ ให้ AI รัน `python Oatside\build_oatside_reports.py` บนเครื่องคุณแล้วเช็กทะเบียนที่สนใจได้

## ปรับเก็บเงิน (50% / override) แบบจำค่า

1. แก้ไฟล์ **`Oatside/oatside_billing_overrides.json`** (สร้างแล้วว่าง `entries: []` ได้)
2. ดูตัวอย่างโครง JSON: **`ProjectYK_System/TransportRateCalculator/docs/oatside_billing_overrides.example.json`**
3. **`exclude_50`** = วันนั้นทะเบียนนั้น **ไม่เก็บ 50%** แม้ระบบจะเห็นว่าวิ่ง 1 เที่ยว  
4. **`include_50`** = **บังคับเก็บ 50%** แม้วันนั้นจะมีมากกว่า 1 เที่ยว (กรณีพิเศษ)
5. แก้แล้วรัน `python Oatside\build_oatside_reports.py` ใหม่ — Excel/HTML จะสะท้อนค่าใหม่

ค่าแวดล้อม **`OATSIDE_OVERRIDES_JSON`** ชี้ path อื่นได้ถ้าไม่อยากวางไว้ใน `Oatside/`

## ถ้าต้องการบังคับ path ไฟล์

ตั้งค่า env ก่อนรัน (ตัวอย่าง):

```bat
set OATSIDE_ORIGIN=C:\Users\Home\Desktop\Project YK\Oatside\ชื่อไฟล์ต้นทาง.xlsx
set OATSIDE_DEST=C:\Users\Home\Desktop\Project YK\Oatside\ชื่อไฟล์ปลายทาง.xlsx
python Oatside\build_oatside_reports.py
```
