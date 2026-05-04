# Deploy & Git — ป้องกันของหาย (สำหรับโอ)

## สรุปสั้น

- **`deploy.ps1` / `deploy_oatside_report.ps1` ตอนนี้ (ค่าเริ่มต้น)** = **commit บนเครื่อง/ใน clone เท่านั้น** — **ยังไม่ push** จนกว่าจะใส่ **`-Push`**
- สคริปต์ **one-click ที่เคยใช้** (`.bat`) ถูกตั้งให้ส่ง **`-Push`** อยู่ — ยัง **publish ได้เหมือนเดิม** แค่กด bat
- ถ้าอยาก **ลองก่อนไม่ขึ้นเน็ต** — ใช้ **`deploy_one_click_local.bat`** (calculator) หรือรัน PowerShell โดย**ไม่ใส่** `-Push` (Oatside)

## ทำไมก่อนหน้าเคย “ไฟล์หาย”

- มักมาจาก **คำสั่ง Git แรง** เช่น `git reset --hard` ไปหา `origin` ขณะที่ **remote เป็น repo บาง ๆ (แค่ Pages)** แต่โฟลเดอร์เดียวกันคือ **โปรเจกต์เต็ม** → Git พยายามให้ตรงกับ remote เลยเหมือนโฟลเดอร์ใหญ่หาย
- **`deploy.ps1` เองไม่ได้ลบโปรเจกต์** — แค่ copy HTML + `git add` + `commit` (+ `push` ถ้าใส่ `-Push`)

## นิสัยที่แนะนำ

1. ก่อน deploy: รัน **`preflight_deploy.ps1`** หรือ `git status` ดูก่อน
2. งานยังไม่ commit: **`git stash push -u -m "before deploy"`** ก่อนลองอะไรเสี่ยง
3. สำรอง: zip โฟลเดอร์ `Project YK` ไปอีกที่ (ท้ายวัน)
4. ลองกู้/สำรวจ: ใช้ **worktree แยก** (เช่น `Project YK_recover_6ea72f6`) แทน `reset --hard` กับโฟลเดอร์หลัก

## ไฟล์ที่เกี่ยวกับ deploy

| ไฟล์ | หมายเหตุ |
|------|-----------|
| `deploy.ps1` | Calculator → root `index.html`; **`-Push`** = ขึ้น GitHub |
| `deploy_one_click.bat` | copy + commit + **push** |
| `deploy_one_click_local.bat` | copy + commit เท่านั้น (ไม่ push) |
| `deploy_oatside_report.ps1` | Oatside → clone Pages; **`-Push`** = pull --rebase + push |
| `deploy_oatside_report_one_click.bat` | build Python + deploy script พร้อม **`-Push`** |

---

อัปเดตลำดับความปลอดภัย (ค่าเริ่มต้นไม่ push): Session deploy safety — `ProjectYK_System/TransportRateCalculator/`
