# Deploy หน้า One Platform status ไป repo `yk-logistics`

หน้า `index.html` + `public-stats.json` — **สถิติจริง** จาก `app.db` (เฉพาะจำนวนรวม / ช่วงวันที่ ไม่มีชื่อคนหรือยอดรายบรรทัด)

## ก่อน push (บนเครื่องที่มี app.db)

รันจากรากโปรเจกต์ Project YK:

```bat
python ProjectYK_System\docs-public\one-platform-status\build_public_stats.py
```

แล้วคัดลอกทั้งโฟลเดอร์ `one-platform-status` ไปยัง clone ของ `transport-rate-calculator` อีกครั้ง (ให้ `public-stats.json` เป็นข้อมูลล่าสุด)

## แนวทางที่ตรงกับ Pages เดิม

Repo ตัวอย่าง: `yk-logistics/transport-rate-calculator`  
Pages base: `https://yk-logistics.github.io/transport-rate-calculator/`

### วิธี A — วางใต้ `reports/` (แนะนำ สอดคล้อง Oatside)

1. คัดลอกโฟลเดอร์ `one-platform-status` ทั้งก้อนไปที่ repo Pages เช่น  
   `transport-rate-calculator/reports/one-platform-status/`
2. Commit + push
3. ลิงก์ที่ได้:  
   `https://yk-logistics.github.io/transport-rate-calculator/reports/one-platform-status/index.html`

### วิธี B — วางที่ root ของ Pages

คัดลอกแค่ `index.html` ไปเป็น `one-platform.html` ที่ root ของ branch ที่ Pages ชี้ — แล้วแก้ลิงก์ภายในหน้า (ส่วน “เปิดออนไลน์แล้ว”) ให้เป็น path สัมพัทธ์ที่ถูกต้องกับ repo จริง

## หลัง deploy

- เครื่องคิดเรทบน Pages มักอยู่ที่ **root** (`index.html` จากสคริปต์ deploy) — ลิงก์ในหน้า pitch ชี้ `https://yk-logistics.github.io/transport-rate-calculator/` แล้ว
- รายงาน Oatside อาจเปลี่ยนโฟลเดอร์รอบ (เช่น `oatside-may2026`) — อัปเดตลิงก์ใน hero section ให้ชี้รายงานล่าสุด

## แหล่งที่มาเนื้อหา

สอดคล้อง `AGENTS.md` และ `CHANGELOG_MASTER.md` ในโปรเจกต์ Project YK (เครื่องพัฒนา)
