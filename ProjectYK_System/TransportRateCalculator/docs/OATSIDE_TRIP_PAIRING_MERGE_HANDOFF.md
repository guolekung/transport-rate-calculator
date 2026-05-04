# Oatside → P&G GPS รายงานเที่ยว: สเปกการจับคู่ + Merge ต้นทางหลายช่วง (Handoff สำหรับ Claude Code)

**อัปเดต:** 2026-05-01 (เพิ่มคำอธิบาย UM 71-6802 + ไฟล์ export 02.05.2026 07:15)  
**ไฟล์หลัก:** `Oatside/build_oatside_reports.py`  
**ผู้ใช้งานจริง:** โอ (ผู้จัดการ) — ใช้รายงาน Excel + HTML จาก GPS export

### เก็บเงินลูกค้า (อัปเดต 2026-05-02)

- **`oatside_config.json`**
  - **`customer_idle_windows`**: ช่วงเวลาที่ **จอดฝากลูกค้า / ไม่เกี่ยวกับลูกค้า** — ตัดชม.รอปลายทาง (`Dest_Wait`) ออกจาก **`Daily_Time_24h_Check`** และคอลัมน์ **`Dest_Wait_customer_h`** / **`Total_Cycle_customer_h`** ใน `Trip_Detail` (เที่ยวส่งก่อนจอดยังนับปกติ; ตัดเฉพาะช่วงทับ `start`–`end` กับ `(Dest_In, Dest_Out)`); **Unmatched ฝั่ง Destination** ในช่วงเดียวกันจะ **ถูกตัดชม.ออกจาก `Unmatched_Dest_h`** ใน `Daily_Time_24h_Check` ด้วย
  - **`use_origin_24h_fifty`**: `false` = กฎเดิม (50% ตาม **วันปฏิทิน `Dest_In`** เที่ยว = 1); `true` = กฎใหม่ **หน้าต่าง 24 ชม. rolling** จาก `Origin_In` — ถ้าในหน้าต่างมี matched **พอดี 1 เที่ยว** → +50% (ชีต `Surcharge_50pct_1Trip` เพิ่มคอลัมน์ `Window_Origin_In` / `Window_End`); **2 เที่ยวในหน้าต่างเดียวกัน → ไม่เก็บ 50%**
- **ค่าเริ่มต้นในโค้ด**: ช่วง **`71-8967`** `2026-04-20 14:00`–`2026-04-29 17:00` (ไทย) — ตาม `CONTEXT_LOG` Session #90–91

### เก็บเงินลูกค้า (อัปเดต 2026-05-01 — กรณี `use_origin_24h_fifty`: false)

- **ไม่ใช้ “ค่าเสียเวลา” ตาม wait threshold แล้ว** — เหลือกฎหลัก: ถ้า `(ทะเบียน, วันที่ Dest_In)` มี **matched trip = 1** → เก็บเพิ่ม **50% ของเรทวันนั้น** (`trip_rate_baht`: **12–15 เม.ย. 2026 = 8,000** / **นอกนั้น 7,500**)
- **Manual override (จำค่า):** แก้ไฟล์ `Oatside/oatside_billing_overrides.json` (หรือตั้ง `OATSIDE_OVERRIDES_JSON`) — ดูตัวอย่าง `ProjectYK_System/TransportRateCalculator/docs/oatside_billing_overrides.example.json`
  - `exclude_50` = ไม่เก็บ 50% วันนั้นทะเบียนนั้น
  - `include_50` = บังคับเก็บ 50% แม้มีมากกว่า 1 เที่ยว
- **Excel:** ชีต `Customer_Summary` (A/B/C + TOTAL), **`Customer_Trips_Per_Day`** (จำนวนเที่ยว matched รวมต่อวันตาม `Dest_In` + จำนวนรถ), `Plate_DestDay` (รายวันต่อทะเบียน), `Surcharge_50pct_1Trip` (รายละเอียด 50%)
- **HTML:** การ์ด Base / 50% / Total extra / **Customer grand** + ตาราง per plate per day; หน้า `plates/<ทะเบียน>.html` มีตาราง “By Dest_In day”

### Guard ลำดับเวลา (หลังจับคู่ทั้งหมด)

- ฟังก์ชัน **`demote_chronology_violations`** (หลัง loop ทะเบียน): ต่อทะเบียน เรียงเที่ยวตาม **`Origin_In`** แล้ววนจนนิ่ง — ถ้า **`Origin_In` เที่ยวถัดไป `< Dest_Out` เที่ยวก่อนหน้า** ถือว่าลำดับเที่ยวขัดแย้ง → **ย้ายเที่ยวก่อนหน้า** ออกจากรายการ matched ไป **Unmatched** (ต้นทางแยกตาม `row_no` ย่อย + ปลายทาง 1 ขา)
- จากนั้นค่อยคำนวณ `travel_flag` (IQR) ใหม่จาก `travel_h` ที่เหลือ

### หมายเหตุแหล่งข้อมูล (Geofence)

- ผู้ใช้ระบุว่าความผิดเพี้ยนของช่วงเข้า–ออกจุด **อาจมาจากการตั้งวง Geofence ในระบบ GPS** (วงเล็ก/ใหญ่เกิน หรือจุดหลุด) — ถ้าปรับวงแล้ว export ใหม่ **ชุดแถว `Leg` ใน Excel จะเปลี่ยน** โดยไม่จำเป็นต้องแก้ heuristic merge ใน repo
- เมื่อได้ไฟล์อัปเดต: นำเข้าโฟลเดอร์ `Oatside/` ตามชื่อเดิม (`discover_gps_files` เลือกไฟล์ล่าสุด) แล้วรัน build ใหม่ทั้งชุด

---

## 1) บริบทธุรกิจ

- มีไฟล์ Excel GPS สองฝั่ง: **จุดต้นทาง (Oatside)** และ **จุดปลายทาง (P&G / เวลล์โกล)**  
- ชีตที่อ่านคือชีตอุปกรณ์ (หัวคอลัมน์ภาษาไทย — ในโค้ดค้นหาชีตจากแถว 1 คอลัมน์ D)  
- ต้องการสรุป **เที่ยว** = ต้นทาง (เข้า/ออก) + ปลายทาง (เข้า/ออก) + เวลารอต้นทาง / เดินทาง / รอปลายทาง + สรุปรายวัน / billing heuristic (เช่น lost-time)  
- **ปัญหาเดิม:** greedy จับคู่ `Origin` กับ `Destination` ทีละคู่ ได้ลำดับที่ **อ่านแล้วขัดแย้ง** เช่นเที่ยวถัดไป `Origin_In` ก่อน `Dest_In` ของเที่ยวก่อน (รถยังไม่ถึงปลายทางแต่มี “เข้าต้นทาง” ใหม่)

---

## 2) ตัวอย่างที่ผู้ใช้ยก (ทะเบียน 71-6802)

**ความหมายทางธุรกิจที่ผู้ใช้อธิบาย**

- รถเข้าต้นทางแล้วออก **โดยยังไม่ขึ้นของ / ยังไม่ไปส่ง**  
- กลับเข้า **ต้นทางอีกรอบ** (ช่วงที่สอง)  
- จากนั้นค่อยไปปลายทางจริง **ครั้งเดียว**

**เวลาที่ต้องการให้เห็นเป็น “เที่ยวเดียว”**

| บทบาท | เวลา |
|--------|------|
| ต้นทางเข้า (ช่วง 1) | 2026-04-13 14:25:23 |
| ต้นทางออก (ช่วง 1) | 2026-04-13 16:54:36 |
| ต้นทางเข้า (ช่วง 2) | 2026-04-13 21:38:41 |
| ต้นทางออก (ช่วง 2) | 2026-04-14 07:11:56 |
| ปลายทางเข้า | 2026-04-14 09:56:11 |
| ปลายทางออก | 2026-04-14 10:36:06 |

**สิ่งที่ต้องไม่เกิด:** แถวถัดไปเป็น “เที่ยวใหม่” ที่ `Origin_In` วันที่ 13 ก่อน `Dest_In` ของเที่ยวก่อน (วันที่ 14) โดยไม่มีการอธิบาย — เพราะอ่านแล้ว “เป็นไปไม่ได้” ถ้าเป็นเที่ยวเดียวตามลำดับเวลาจริงของรถ

### กรณีจอ UM: ต้นทาง 14:22–16:58 กับปลายทาง 18:46–19:20 (สครีนช็อตเดิม)

**ไม่ใช่เพราะช่องว่าง ~1 ชม. 48 น.** — `feasible()` ใช้ `max_travel_h` (ค่าเริ่มต้น 48 ชม.) ช่วง 16:58 → 18:46 ผ่านเกณฑ์ได้

**สาเหตุเดิม (ก่อนแก้ `match_plate`):**

1. **`match_plate` แบบ origin-first** — ต้นทางที่ออกก่อนไปคว้า `Dest_In` เร็วสุดที่ยังว่าง → ช่วงสั้นแย่งปลายทางของช่วงยาว  
2. **`demote_chronology_violations`** — เก็บเที่ยวที่ลำดับเวลา “เป็นไปไม่ได้” (เข้าต้นทางเที่ยวถัดไปก่อนออกจากปลายทางเที่ยวก่อน) โดยยกเลิกเที่ยวก่อนหน้า

**การแก้ในโค้ด (2026-05-01):** เปลี่ยนเป็น **ปลายทางตามเวลา → จับกับต้นทางล่าสุดที่ `Origin_Out` ก่อน `Dest_In`** ลดการแย่งคู่ผิดและลดการโดน demote เป็นวง

**ผลจาก export ใหม่ (`...07-15-32 Oatside.xlsx`):** ตัวอย่างทะเบียน **71-6802** — คู่ `10.7` (ต้น 16:03–19:51) กับ `Dest 10.6` (21:35–22:23) กลายเป็น **matched** หลังเปลี่ยนอัลกอริทึม (ยังมี `uo` เฉพาะช่วงต้นทางสั้น ๆ ที่ไม่มีปลายทางในช่วง เช่น `10.6` 11:56–14:46)

---

## 3) โมเดลข้อมูลในโค้ด

### `Leg` (dataclass)

- `row_no: str` — เลขแถวจากไฟล์ (เช่น `10.3`) ใช้ทั้งอ้างอิงและ **จับคู่ต้น–ปลาย** เมื่อ export ตรงกัน  
- `plate: str` — ทะเบียน `71-xxxx`  
- `device: str` — ข้อความอุปกรณ์/ป้าย  
- `t_in`, `t_out: datetime`

### `Trip` (dataclass)

- เก็บ `o_in`, `o_out`, `d_in`, `d_out` สำหรับแสดงผล  
- `o_row` อาจเป็นแบบรวม: `10.2+10.3+10.4`  
- `origin_wait_h`, `travel_h`, `dest_wait_h`, `total_cycle_h`  
- `travel_flag` — หลังคำนวณทั้งหมด ใช้ IQR ของ `travel_h` ทั้งชุดเพื่อทำ `ABNORMAL`

### `parse_legs(path)`

- อ่าน openpyxl, หา worksheet ที่แถว 1 คอลัมน์ D ตรงกับหัวชีตอุปกรณ์  
- แถวรายละเอียดต้อง match `DETAIL_KEY = ^\d+\.\d+$`  
- เรียง `legs` ด้วย `(plate, t_out)` ก่อนนำไปจับคู่ต่อ

---

## 4) ขั้นที่ 1 — `match_plate` (อัปเดต 2026-05-01: ปลายทางก่อน + ต้นทางล่าสุด)

**ไฟล์:** `match_plate(origins, dests, max_travel_h)`

**พฤติกรรมปัจจุบัน (แก้ปัญหา UM เกินจริง / 71-6802):**

- เรียง **ปลายทาง** ด้วย `(t_in, t_out)` แล้วไล่ทีละ `d`  
- กับแต่ละ `d` เลือก **ต้นทางที่ยังไม่ถูกใช้** ที่ `feasible(o, d)` และมี **`Origin_Out` ช้าที่สุด** (ล่าสุดก่อน `Dest_In`) — เทียบเท่า “รอบออกฮับครั้งล่าสุดก่อนเข้าปลายทาง”  
- `feasible`: `d.t_in >= o.t_out` และ `hours(o.t_out, d.t_in) <= max_travel_h` (default 48)

**ผลลัพธ์:** `pairs`, `uo`, `ud`

**ทำไมเปลี่ยนจากเดิม:** แบบเดิม (ต้นทางเรียงก่อน แล้วคว้า `Dest_In` เร็วสุด) ทำให้ช่วงต้นทางสั้น ๆ ไปแย่งปลายทางของช่วงยาว → เหลือ UM แปลก ๆ แล้วไปชน **`demote_chronology_violations`** เป็นวง

**ข้อจำกัดที่ยังมี:** ช่วงต้นทางสั้น ๆ ที่ **ไม่มี** `Dest_In` ภายใน `max_travel_h` หลัง `Origin_Out` จะยังเป็น `uo` ได้ตามปกติ

---

## 5) ขั้นที่ 2 — `merge_chained_origin_pairs` (แก้ปัญหา double origin)

### 5.1 การเรียงลำดับคู่ก่อน merge

- **เรียง `pairs` ด้วย `(origin.t_out, origin.t_in)`** — ลำดับ “ปิดช่วงต้นทาง” ตามเวลา  
- **ไม่**ใช้การเรียงตาม `Dest_In` เป็นหลักในรอบ merge (เคยทำแล้วทำให้เลือกปลายทางผิดและปลายทางที่ถูกต้องกลายเป็น unmatched)

### 5.2 เงื่อนไขการ “ต่อขา” เข้าเที่ยวเดียว

จากคู่เริ่ม `(o_acc, d_acc)` ที่ดัชนี `i` ให้ `j = i+1` วนซ้ำ:

- ถ้าไม่มีคู่ถัดไป → จบ inner loop  
- ดึง `(o2, d2) = pairs[j]`  
- ถ้า **`o2.t_in >= d_acc.t_in`** → **หยุด** (ไม่ถือว่าเป็นการซ้อนต้นทางก่อนปลายทางเดิม)  
- มิฉะนั้น: **รวมต้นทาง**  
  - `o_acc = Leg(row_no=o_acc.row_no + "+" + o2.row_no, t_in=o_acc.t_in, t_out=o2.t_out, ...)`  
- หลังรวมแล้ว `last_out = o_acc.t_out`  
- พิจารณา `pool = [d_acc, d2]`  
- `feas = [d for d in pool if d.t_in >= last_out]`  
- `use_pool = feas if feas else pool` (fallback ถ้าไม่มีใคร feasible ตามเวลา)

### 5.3 การเลือกปลายทางหลังรวมต้นทาง (สำคัญมาก)

ใช้ตัวแปร `first_extend` (bool) ต่อหนึ่ง “ก้อน” ที่เริ่มจากดัชนี `i`:

**รอบแรกของการต่อช่วง (`first_extend == True`)**

- ลอง **`row_pref = [d for d in use_pool if d.row_no == o2.row_no]`**  
  - ถ้าไม่ว่าง → เลือก `pick = min(row_pref, key=(hours(last_out, d.t_in), d.t_in))`  
  - ถ้าว่าง → `pick = min(use_pool, key=...)` เหมือนกัน  
- ตั้ง `first_extend = False`

**รอบถัดไป (`first_extend == False`)**

- ถ้า **`d_acc` ยังอยู่ใน `use_pool`** → **`pick = d_acc`** (เกาะปลายทางเดิมของเที่ยว — “ยังเป็นเที่ยวส่งเดิม”)  
- มิฉะนั้น → `pick = min(use_pool, key=...)`

**ปลายทางใน `pool` ที่ไม่ถูกเลือก** → append เข้า **`orphan_dests`** (จะนำไป rematch ทีหลัง)

### 5.4 การเลื่อนดัชนีนอก

- หลัง inner loop จบ: `out.append((o_acc, d_acc))`  
- **`i = j`** (ข้ามคู่ที่ถูกดูดเข้า merge แล้ว — ไม่ประมวลซ้ำเป็นคู่แยก)

---

## 6) ขั้นที่ 3 — ทำเครื่องหมายต้นทางที่ใช้แล้ว + Rematch orphan

**ฟังก์ชันช่วย**

- `collect_origin_row_refs(ol)` — split `o_row` ด้วย `"+"`  
- `constituent_origin_legs(ol, by_row)` — map `row_no` → `Leg` จริงจาก `by_row` (dict ต่อทะเบียน)  
- `mark_used_origin_legs(ol, by_row, used_o)` — `used_o.add(id(leg))` ทุกช่วงที่รวมอยู่

**ลำดับใน `build_trips` ต่อทะเบียน `p`**

1. `all_o = by_plate_o[p]` สร้าง `by_row` (ถ้า `row_no` ซ้ำ ใช้ตัวแรกที่เจอ)  
2. `pairs, uo, ud = match_plate(all_o, by_plate_d[p], mx)`  
3. `merged_pairs, orphan_d = merge_chained_origin_pairs(pairs)`  
4. `used_o = set()` แล้ว mark จากทุก `ol` ใน `merged_pairs`  
5. `candidates = [o for o in all_o if id(o) not in used_o]`  
6. `rematch_pairs, still_orphan = rematch_orphan_dests_to_origins(orphan_d, candidates, mx)`  
7. mark `used_o` จาก `rematch_pairs`  
8. `pairs_final = merged_pairs + rematch_pairs`  
9. สร้าง `Trip` จากทุกคู่ใน `pairs_final`  
10. Unmatched ต้นทาง: `all_o` ที่ `id` ไม่อยู่ใน `used_o`  
11. Unmatched ปลายทาง: `ud + still_orphan`

**`rematch_orphan_dests_to_origins`**

- เรียง orphan dest ตาม `(t_in, t_out)`  
- แต่ละ dest เลือก origin ใน `candidates` ที่ยังไม่ถูกใช้ ที่ feasible และ **เดินทางสั้นสุด** (tie ใช้ `o.t_out` น้อยกว่า)

---

## 7) การคำนวณ `origin_wait_h` หลัง merge

**ห้าม**ใช้ `hours(merged_o.t_in, merged_o.t_out)` เป็นค่ารอเดียว เพราะช่วงระหว่าง “ออกช่วงแรก” ถึง “เข้าช่วงสอง” คือเวลารถอยู่นอกต้นทาง / บนถนน — **ไม่ใช่รอที่ต้นทาง**

**ที่ทำแล้ว**

- `segs = constituent_origin_legs(ol, by_row)`  
- ถ้า `len(segs) > 1` → `origin_wait_h = sum(hours(s.t_in, s.t_out) for s in segs)`  
- มิฉันนั้น → `hours(ol.t_in, ol.t_out)`

**ฟิลด์อื่นที่เกี่ยวกับเวลา**

- `travel_h = hours(ol.t_out, dl.t_in)` — `ol.t_out` คือ **ออกช่วงสุดท้าย** หลัง merge  
- `total_cycle_h = hours(segs[0].t_in, dl.t_out)`  
- `device` ใช้จาก `segs[0].device`  
- `o_in` / `o_out` ใน `Trip` ใช้ `segs[0].t_in` และ `ol.t_out`

---

## 8) ตัวแปรสภาพแวดล้อมที่เกี่ยวข้อง

| ตัวแปร | ความหมาย |
|--------|-----------|
| `OATSIDE_ORIGIN` | path ไฟล์ต้นทาง (ไม่ตั้ง = เลือกไฟล์ล่าสุดใน `Oatside/`) |
| `OATSIDE_DEST` | path ไฟล์ปลายทาง |
| `OATSIDE_MAX_TRAVEL_H` | เพดานชั่วโมง `Origin_Out → Dest_In` (default 48) |
| `OATSIDE_LOST_TIME_WAIT_MIN_H` | threshold ชั่วโมงรอรวมสำหรับกฎ lost-time (ดูในโมดูล/ชีตรายงาน) |

---

## 9) วิธีรันและผลลัพธ์ล่าสุด (เครื่อง dev รอบนี้)

จากราก repo:

```bash
python -m py_compile Oatside/build_oatside_reports.py
python Oatside/build_oatside_reports.py
```

**ตัวอย่างผลลัพธ์ล่าสุด (หลัง merge ใหม่)**

- `Trips: 88 | Unmatched legs: 31`  
- Excel: `Oatside/Oatside_PG_Trip_Summary_By_Site.xlsx`  
- HTML: ใต้ `Oatside/TransportRateCalculator/reports/oatside-apr2026` หรือ `ProjectYK_System/TransportRateCalculator/reports/...` ขึ้นกับ `_root()` ในไฟล์ (ถ้ามีโฟลเดอร์ `TransportRateCalculator` ที่ราก repo จะชี้ไปที่นั้น)

**การตรวจทะเบียน 71-6802 (ชุดข้อมูลในโฟลเดอร์ Oatside ณ รอบ build)**

- มีเที่ยวที่ `Dest_In` วันที่ **2026-04-14 09:56** โดยต้นทางรวมหลายแถว (ในรอบที่ตรวจอาจเป็น `10.2+10.3+10.4`) และ **`origin_wait` / `travel` สมเหตุสมผล**  
- ปลายทางบางแถวที่เคยถูก greedy จับคู่ในแนวทางเดิม จะไป **orphan → unmatched หรือ rematch** — ต้องตรวจชีต Unmatched / logic rematch ว่าตรงความเป็นจริงหรือไม่

---

## 10) ความเสี่ยง / ขอบเขต heuristic (สำหรับงานต่อ)

1. **พึ่งพา `row_no` ตรงกันระหว่างต้นและปลาย** ในรอบแรกของการเลือก `dest` — ถ้าไฟล์ export รอบใดไม่ตรงกัน ต้องนิยามกฎใหม่ (เช่น min travel, หรือ manual mapping)  
2. **ช่วงต้นทางสั้นมาก** (เช่นแว๊บเข้า–ออก ~20 นาที) อาจถูกดูดรวมในก้อนเดียวกับเที่ยวยาว — ผู้ใช้อาจต้องการ **กั้น merge** ถ้าช่วงสั้นกว่า threshold  
3. **จำนวน Unmatched เพิ่มขึ้น** หลัง merge เป็นปกติในเชิง “แยกปลายทางที่ไม่ตรงกับเที่ยวเดิมออกมา” — ต้องมี QA ว่า rematch ไปคู่กับต้นทางที่ถูกต้องหรือยังค้างจริง  
4. การ merge หลายรอบในก้อนเดียวใช้ **sticky `d_acc`** หลังรอบแรก — ถ้ามีเคสธุรกิจที่ “เปลี่ยนปลายทาง” ระหว่างช่วงต้นทางที่สองไปสาม อาจต้องปรับ

---

## 11) ไฟล์เอกสารที่อัปเดตใน repo (บริบทระบบ)

- `ProjectYK_System/TransportRateCalculator/docs/CONTEXT_LOG.md` — Session Summary #71  
- `ProjectYK_System/CHANGELOG_MASTER.md` — bullet 2026-05-01 Oatside merge  

---

## 12) คำถามเปิดสำหรับงานถัดไป (ถ้าจะ refine)

1. ช่วงต้นทางสั้นกว่า **X นาที** ควร **ยกเว้น**จากการ merge หรือไม่ — `X` เท่าไร  
2. เมื่อ `row_no` ต้น/ปลายไม่ตรงกัน ต้องการ fallback เป็น **min travel** / **min Dest_In** / **manual table** แบบไหน  
3. หลัง merge ต้องการ **แสดงใน Excel เป็นแถวย่อยหลายบรรทัด** ภายใต้เที่ยวเดียวหรือไม่ (ปัจจุบันรวมเป็น `o_row` เดียว + คำนวณ wait เป็นผลรวม)

---

## 13) Checklist ให้ Claude Code ทำต่อ (ถ้ามอบหมาย)

- [ ] รัน build กับไฟล์ GPS ชุดล่าสุดของผู้ใช้ แล้วสุ่มตรวจ 3–5 ทะเบียนที่เคยมีปัญหา  
- [ ] เปรียบเทียบจำนวนเที่ยว/Unmatched ก่อน–หลัง merge (หรือเทียบกับรายงาน manual)  
- [ ] ถ้า heuristic ยังพลาด: เพิ่ม unit test จาก tuple เวลาจำลอง (ไม่ต้องพึ่งไฟล์จริง)  
- [ ] อัปเดต deploy script / GitHub Pages ถ้าโฟลเดอร์ output เปลี่ยนตามเครื่อง  
- [ ] (ถ้าต้องการ) แยก threshold ช่วงสั้น + logging เหตุผลการ merge ลงชีต debug

---

*จบเอกสาร handoff — path ใน repo: `ProjectYK_System/TransportRateCalculator/docs/OATSIDE_TRIP_PAIRING_MERGE_HANDOFF.md`*
