# Appendix A: Complete ITU-R M.1371-5 Message 1–27 Bit-Layout Reference Tables

> **Purpose:** This appendix provides the exhaustive, bit-verified reference catalog for all **27 message types** standardized in **Recommendation ITU-R M.1371-5 (Annex 8)**. Every table lists both **0-based inclusive bit ranges** (`libais`, `gpsd` `AIVDM.txt`, `pyais`, and C/C++/Rust/Python slice convention, where a 1-slot message spans bits `0..167`) and **1-based inclusive bit ranges** (official ITU-R M.1371-5 table numbering, `1..168`), alongside exact bit widths, signed/unsigned data types, physical scaling factors, and sentinel ("not available") values.

---

## A.1 Bit-Slicing and Data-Type Legend

* **Python / C++ / Rust Slice Rule:** A field listed with **0-Based Bits** `b_start..b_end` and **Width** $W = b_{\text{end}} - b_{\text{start}} + 1$ corresponds to the half-open slice `bits[b_start : b_start + W]`.
* **Data Types:**
  * `uintW`: $W$-bit unsigned MSB-first integer ($0 \le U \le 2^W - 1$).
  * `intW`: $W$-bit **two's complement signed** MSB-first integer ($-2^{W-1} \le S \le 2^{W-1} - 1$).
  * `bool`: 1-bit boolean flag (`0` = `False`, `1` = `True`).
  * `str6`: Sequence of 6-bit ASCII characters (`@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_ !"#$%&'()*+,-./0123456789:;<=>?`), padded on the right with `@` (`000000`).
  * `raw`: Variable-length binary bit array (application-specific or RTCM payload).

---

## A.2 Bit-Layout Tables for Messages 1 through 27

### Table A.1: Messages 1, 2, and 3 — Position Report (Class A Scheduled, Assigned, and Special)
* **Total Length:** `168 bits` (1 slot; 28 NMEA 6-bit armor characters, `0` fill bits).
* **Access Scheme:** Message 1 = `SOTDMA`; Message 2 = `SOTDMA` (Assigned Mode); Message 3 = `ITDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `1`, `2`, or `3` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` (`0` = default; `3` = do not repeat) |
| `8..37` | `9..38` | 30 | User ID (MMSI) | `mmsi` | `uint30` | ID | `000000000`–`999999999` |
| `38..41` | `39..42` | 4 | Navigation Status | `nav_status` | `uint4` | Enum (Table A.26) | `0–14`; **`15` = Not defined (default)** |
| `42..49` | `43..50` | 8 | Rate of Turn (ROT) | `rot` | `int8` | $4.733\sqrt{\|\omega_{\text{deg/min}}\|}$ | `-126`..`+126`; `±127` = $>5^\circ/30\text{s}$ no TI; **`-128` (`0x80`) = N/A** |
| `50..59` | `51..60` | 10 | Speed Over Ground (SOG) | `sog` | `uint10` | $0.1\text{ knot}$ | `0–1021` ($0.0\text{–}102.1\text{ kts}$), `1022` = $\ge 102.2$; **`1023` = N/A** |
| `60..60` | `61..61` | 1 | Position Accuracy | `position_accuracy` | `bool` | Flag | `1` = High ($\le 10\text{ m}$ DGNSS); `0` = Low ($>10\text{ m}$) |
| `61..88` | `62..89` | 28 | Longitude ($\lambda$) | `x` / `longitude` | `int28` | $\frac{1}{10{,}000}\text{ min}$ ($\frac{1}{600{,}000}^\circ$) | $[-180^\circ, +180^\circ]$; **`181.0°` (`108600000` / `0x6791AC0`) = N/A** |
| `89..115` | `90..116` | 27 | Latitude ($\phi$) | `y` / `latitude` | `int27` | $\frac{1}{10{,}000}\text{ min}$ ($\frac{1}{600{,}000}^\circ$) | $[-90^\circ, +90^\circ]$; **`91.0°` (`54600000` / `0x3412140`) = N/A** |
| `116..127` | `117..128` | 12 | Course Over Ground (COG)| `cog` | `uint12` | $0.1^\circ\text{ true}$ | `0–3599` ($0.0^\circ\text{–}359.9^\circ$); **`3600` (`360.0°`) = N/A** |
| `128..136` | `129..137` | 9 | True Heading (HDG) | `true_heading` | `uint9` | $1^\circ\text{ true}$ | `0–359°`; **`511` (`0x1FF`) = N/A** |
| `137..142` | `138..143` | 6 | Time Stamp | `timestamp` | `uint6` | UTC second | `0–59 s`; **`60`=N/A, `61`=Manual, `62`=DR, `63`=Inoperative** |
| `143..144` | `144..145` | 2 | Maneuver Indicator | `special_manoeuvre` | `uint2` | Enum | **`0` = N/A**, `1` = No special maneuver, `2` = Special (Blue Sign) |
| `145..147` | `146..148` | 3 | Spare | `spare` | `uint3` | — | `0` |
| `148..148` | `149..149` | 1 | RAIM Flag | `raim` | `bool` | Flag | `0` = RAIM not in use; `1` = RAIM in use |
| `149..167` | `150..168` | 19 | Communication State | `comm_state` | `uint19` | Table A.25 | SOTDMA (`Msg 1, 2`) or ITDMA (`Msg 3`) |

---

### Table A.2: Messages 4 and 11 — Base Station Report & UTC/Date Response
* **Total Length:** `168 bits` (1 slot; 28 NMEA 6-bit armor characters, `0` fill bits).
* **Access Scheme:** Message 4 = `FATDMA` / `SOTDMA` (SOTDMA Comm State); Message 11 = `ITDMA` (ITDMA Comm State).

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `4` (Base Station) or `11` (UTC/Date Response) |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | User ID (MMSI) | `mmsi` | `uint30` | ID | `00MIDxxxx` (Msg 4) or Mobile MMSI (Msg 11) |
| `38..51` | `39..52` | 14 | UTC Year | `year` | `uint14` | Year | `1–9999`; **`0` = Year not available** |
| `52..55` | `53..56` | 4 | UTC Month | `month` | `uint4` | Month | `1–12`; **`0` = Month not available** |
| `56..60` | `57..61` | 5 | UTC Day | `day` | `uint5` | Day | `1–31`; **`0` = Day not available** |
| `61..65` | `62..66` | 5 | UTC Hour | `hour` | `uint5` | Hour | `0–23`; **`24` = Hour not available** |
| `66..71` | `67..72` | 6 | UTC Minute | `minute` | `uint6` | Minute | `0–59`; **`60` = Minute not available** |
| `72..77` | `73..78` | 6 | UTC Second | `second` | `uint6` | Second | `0–59`; **`60` = Second not available** |
| `78..78` | `79..79` | 1 | Position Accuracy | `position_accuracy` | `bool` | Flag | `1` = High ($\le 10\text{ m}$ / surveyed); `0` = Low ($>10\text{ m}$) |
| `79..106` | `80..107` | 28 | Longitude ($\lambda$) | `x` / `longitude` | `int28` | $\frac{1}{600{,}000}^\circ$ | $[-180^\circ, +180^\circ]$; **`181.0°` (`0x6791AC0`) = N/A** |
| `107..133` | `108..134` | 27 | Latitude ($\phi$) | `y` / `latitude` | `int27` | $\frac{1}{600{,}000}^\circ$ | $[-90^\circ, +90^\circ]$; **`91.0°` (`0x3412140`) = N/A** |
| `134..137` | `135..138` | 4 | Type of EPFD | `fix_type` | `uint4` | Enum (Table A.27) | `0–15` (`7` = Surveyed for fixed Base Station) |
| `138..138` | `139..139` | 1 | Long-Range TX Control | `tx_ctl` | `bool` | Flag | `0` = Suppress auto Msg 27; `1` = Enable Msg 27 TX |
| `139..147` | `140..148` | 9 | Spare | `spare` | `uint9` | — | `0` |
| `148..148` | `149..149` | 1 | RAIM Flag | `raim` | `bool` | Flag | `0` = Not in use; `1` = In use |
| `149..167` | `150..168` | 19 | Communication State | `comm_state` | `uint19` | Table A.25 | SOTDMA (`Msg 4`) or ITDMA (`Msg 11`) |

---

### Table A.3: Message 5 — Static and Voyage Related Data (Class A)
* **Total Length:** `424 bits` (2 slots; 71 NMEA 6-bit armor characters across 2 fragments with `2` fill bits).
* **Access Scheme:** `RATDMA` or `ITDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `5` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | User ID (MMSI) | `mmsi` | `uint30` | ID | `000000000`–`999999999` |
| `38..39` | `39..40` | 2 | AIS Version Indicator | `ais_version` | `uint2` | Enum | `0`=M.1371-1, `1`=M.1371-3, `2`=M.1371-5, `3`=Future |
| `40..69` | `41..70` | 30 | IMO Number | `imo_num` | `uint30` | 7-digit ID | `1000000`–`999999999`; **`0` = N/A (Inland/Warship)** |
| `70..111` | `71..112` | 42 | Call Sign | `callsign` | `str6` | 7 chars | 6-bit ASCII; **`@@@@@@@` = N/A** |
| `112..231` | `113..232` | 120 | Vessel Name | `name` | `str6` | 20 chars | 6-bit ASCII; **`@@@@@@@@@@@@@@@@@@@@` = N/A** |
| `232..239` | `233..240` | 8 | Type of Ship and Cargo | `type_and_cargo` | `uint8` | Enum (Table A.28) | `10–99`; **`0` = Not available / default** |
| `240..248` | `241..249` | 9 | Dimension to Bow ($A$) | `dim_a` | `uint9` | $1\text{ m}$ | `0–511 m` (`511` = $\ge 511\text{ m}$); $A=B=0 \Rightarrow$ N/A |
| `249..257` | `250..258` | 9 | Dimension to Stern ($B$) | `dim_b` | `uint9` | $1\text{ m}$ | `0–511 m` (`511` = $\ge 511\text{ m}$) |
| `258..263` | `259..264` | 6 | Dimension to Port ($C$) | `dim_c` | `uint6` | $1\text{ m}$ | `0–63 m` (`63` = $\ge 63\text{ m}$); $C=D=0 \Rightarrow$ N/A |
| `264..269` | `265..270` | 6 | Dimension to Starboard ($D$) | `dim_d` | `uint6` | $1\text{ m}$ | `0–63 m` (`63` = $\ge 63\text{ m}$) |
| `270..273` | `271..274` | 4 | Type of EPFD | `fix_type` | `uint4` | Enum (Table A.27) | `1–15`; **`0` = Undefined (default)** |
| `274..277` | `275..278` | 4 | ETA Month (UTC) | `eta_month` | `uint4` | Month | `1–12`; **`0` = N/A (default)** |
| `278..282` | `279..283` | 5 | ETA Day (UTC) | `eta_day` | `uint5` | Day | `1–31`; **`0` = N/A (default)** |
| `283..287` | `284..288` | 5 | ETA Hour (UTC) | `eta_hour` | `uint5` | Hour | `0–23`; **`24` = N/A (default)** |
| `288..293` | `289..294` | 6 | ETA Minute (UTC) | `eta_minute` | `uint6` | Minute | `0–59`; **`60` = N/A (default)** |
| `294..301` | `295..302` | 8 | Max Present Static Draught | `draught` | `uint8` | $0.1\text{ m}$ | `1–255` ($0.1\text{–}25.5\text{ m}$); **`0` = N/A (default)** |
| `302..421` | `303..422` | 120 | Destination | `destination` | `str6` | 20 chars | 6-bit ASCII; **`@@@@@@@@@@@@@@@@@@@@` = N/A** |
| `422..422` | `423..423` | 1 | Data Terminal Equipment (DTE)| `dte` | `bool` | Flag | `0` = Available; **`1` = Not available (default)** |
| `423..423` | `424..424` | 1 | Spare | `spare` | `uint1` | — | `0` |

---

### Table A.4: Message 6 — Binary Addressed Message
* **Total Length:** `88 to 1008 bits` (1 to 5 slots; header is `88 bits` including `DAC`/`FI`, followed by up to `920 bits` of application data).
* **Access Scheme:** `RATDMA`, `FATDMA`, or `ITDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `6` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | Source ID (MMSI) | `mmsi` | `uint30` | ID | Sender MMSI |
| `38..39` | `39..40` | 2 | Sequence Number | `seq` | `uint2` | Counter | `0–3` (matched by Message 7 Acknowledge) |
| `40..69` | `41..70` | 30 | Destination ID (MMSI) | `dest_mmsi` | `uint30` | ID | Recipient MMSI |
| `70..70` | `71..71` | 1 | Retransmit Flag | `retransmit` | `bool` | Flag | `0` = No retransmission; `1` = Retransmitted |
| `71..71` | `72..72` | 1 | Spare | `spare` | `uint1` | — | `0` |
| `72..81` | `73..82` | 10 | Designated Area Code (DAC) | `dac` | `uint10` | Code | `1` = IMO International; `200` = EU Inland; `366` = USA |
| `82..87` | `83..88` | 6 | Function Identifier (FI) | `fi` | `uint6` | Code | `0–63` (Application-Specific Message ID — see Ch 16) |
| `88..1007` | `89..1008` | 0–920 | Binary Application Data | `binary_data` | `raw` | Bits | Variable-length payload (byte-aligned up to 920 bits) |

---

### Table A.5: Messages 7 and 13 — Binary Acknowledge & Safety-Related Acknowledgment
* **Total Length:** `72`, `104`, `136`, or `168 bits` (1 slot; acknowledges 1, 2, 3, or 4 received Message 6 or Message 12 packets).
* **Access Scheme:** `RATDMA`, `FATDMA`, or `ITDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `7` (Binary Ack) or `13` (Safety Ack) |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | Source ID (MMSI) | `mmsi` | `uint30` | ID | Acknowledging station's MMSI |
| `38..39` | `39..40` | 2 | Spare | `spare` | `uint2` | — | `0` |
| `40..69` | `41..70` | 30 | Destination ID 1 (MMSI) | `dest_mmsi_1` | `uint30` | ID | MMSI of station being acknowledged (#1, mandatory) |
| `70..71` | `71..72` | 2 | Sequence Number for ID 1 | `seq_num_1` | `uint2` | Counter | `0–3` (from received Msg 6 / Msg 12) |
| `72..101` | `73..102` | 30 | Destination ID 2 (MMSI) | `dest_mmsi_2` | `uint30` | ID | *Optional* (#2; present if total length $\ge 104\text{ bits}$) |
| `102..103` | `103..104` | 2 | Sequence Number for ID 2 | `seq_num_2` | `uint2` | Counter | *Optional* (`0–3`) |
| `104..133` | `105..134` | 30 | Destination ID 3 (MMSI) | `dest_mmsi_3` | `uint30` | ID | *Optional* (#3; present if total length $\ge 136\text{ bits}$) |
| `134..135` | `135..136` | 2 | Sequence Number for ID 3 | `seq_num_3` | `uint2` | Counter | *Optional* (`0–3`) |
| `136..165` | `137..166` | 30 | Destination ID 4 (MMSI) | `dest_mmsi_4` | `uint30` | ID | *Optional* (#4; present if total length $= 168\text{ bits}$) |
| `166..167` | `167..168` | 2 | Sequence Number for ID 4 | `seq_num_4` | `uint2` | Counter | *Optional* (`0–3`) |

---

### Table A.6: Message 8 — Binary Broadcast Message
* **Total Length:** `56 to 1008 bits` (1 to 5 slots; header is `56 bits` including `DAC`/`FI`, followed by up to `952 bits` of application data).
* **Access Scheme:** `RATDMA`, `FATDMA`, or `ITDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `8` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | Source ID (MMSI) | `mmsi` | `uint30` | ID | Sender MMSI |
| `38..39` | `39..40` | 2 | Spare | `spare` | `uint2` | — | `0` |
| `40..49` | `41..50` | 10 | Designated Area Code (DAC) | `dac` | `uint10` | Code | `1` = IMO International; `200` = EU Inland; `366` = USA |
| `50..55` | `51..56` | 6 | Function Identifier (FI) | `fi` | `uint6` | Code | `0–63` (e.g., `FI=22` Area Notice, `FI=31` Met/Hydro) |
| `56..1007` | `57..1008` | 0–952 | Binary Application Data | `binary_data` | `raw` | Bits | Variable-length payload (see Chapter 16 & Appendix D) |

---

### Table A.7: Message 9 — Standard SAR Aircraft Position Report
* **Total Length:** `168 bits` (1 slot).
* **Access Scheme:** `SOTDMA` (`commstate_flag = 0`) or `ITDMA` (`commstate_flag = 1`).

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `9` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | User ID (MMSI) | `mmsi` | `uint30` | ID | SAR Aircraft MMSI (`111MID1xx` fixed-wing, `111MID5xx` helo) |
| `38..49` | `39..50` | 12 | Altitude (GNSS or Baro) | `alt` | `uint12` | $1\text{ meter}$ | `0–4094 m` (`4094` = $\ge 4094\text{ m}$); **`4095` (`0xFFF`) = N/A** |
| `50..59` | `51..60` | 10 | Speed Over Ground (SOG) | `sog` | `uint10` | **$1\text{ knot}$** | `0–1022 knots` (`1022` = $\ge 1022\text{ kts}$); **`1023` = N/A** |
| `60..60` | `61..61` | 1 | Position Accuracy | `position_accuracy` | `bool` | Flag | `1` = High ($\le 10\text{ m}$); `0` = Low ($>10\text{ m}$) |
| `61..88` | `62..89` | 28 | Longitude ($\lambda$) | `x` / `longitude` | `int28` | $\frac{1}{600{,}000}^\circ$ | $[-180^\circ, +180^\circ]$; **`181.0°` (`0x6791AC0`) = N/A** |
| `89..115` | `90..116` | 27 | Latitude ($\phi$) | `y` / `latitude` | `int27` | $\frac{1}{600{,}000}^\circ$ | $[-90^\circ, +90^\circ]$; **`91.0°` (`0x3412140`) = N/A** |
| `116..127` | `117..128` | 12 | Course Over Ground (COG)| `cog` | `uint12` | $0.1^\circ\text{ true}$ | `0.0°–359.9°`; **`3600` (`360.0°`) = N/A** |
| `128..133` | `129..134` | 6 | Time Stamp | `timestamp` | `uint6` | UTC second | `0–59 s`; **`60`=N/A, `61`=Manual, `62`=Est, `63`=Inop** |
| `134..134` | `135..135` | 1 | Altitude Sensor | `alt_sensor` | `bool` | Flag | `0` = GNSS altitude; `1` = Barometric altitude sensor |
| `135..141` | `136..142` | 7 | Spare | `spare` | `uint7` | — | `0` |
| `142..142` | `143..143` | 1 | DTE Flag | `dte` | `bool` | Flag | `0` = Data terminal ready; `1` = Not available |
| `143..145` | `144..146` | 3 | Spare | `spare2` | `uint3` | — | `0` |
| `146..146` | `147..147` | 1 | Assigned Mode Flag | `assigned` | `bool` | Flag | `0` = Autonomous mode; `1` = Assigned mode |
| `147..147` | `148..148` | 1 | RAIM Flag | `raim` | `bool` | Flag | `0` = Not in use; `1` = In use |
| `148..148` | `149..149` | 1 | Comm State Selector Flag| `commstate_flag` | `bool` | Selector | `0` = SOTDMA state follows; `1` = ITDMA state follows |
| `149..167` | `150..168` | 19 | Communication State | `comm_state` | `uint19` | Table A.25 | SOTDMA (`flag=0`) or ITDMA (`flag=1`) |

---

### Table A.8: Message 10 — UTC and Date Inquiry
* **Total Length:** `72 bits` (1 slot; 12 NMEA 6-bit armor characters, `0` fill bits).
* **Access Scheme:** `RATDMA`, `FATDMA`, or `ITDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `10` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | Source ID (MMSI) | `mmsi` | `uint30` | ID | Inquiring station MMSI |
| `38..39` | `39..40` | 2 | Spare | `spare` | `uint2` | — | `0` |
| `40..69` | `41..70` | 30 | Destination ID (MMSI) | `dest_mmsi` | `uint30` | ID | Target station MMSI (responds with Message 11) |
| `70..71` | `71..72` | 2 | Spare | `spare2` | `uint2` | — | `0` |

---

### Table A.9: Message 12 — Addressed Safety-Related Message
* **Total Length:** `72 to 1008 bits` (1 to 5 slots; `72-bit` header + `1` to `156` 6-bit ASCII characters).
* **Access Scheme:** `RATDMA`, `FATDMA`, or `ITDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `12` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | Source ID (MMSI) | `mmsi` | `uint30` | ID | Sender MMSI |
| `38..39` | `39..40` | 2 | Sequence Number | `seq_num` | `uint2` | Counter | `0–3` (acknowledged by Message 13) |
| `40..69` | `41..70` | 30 | Destination ID (MMSI) | `dest_mmsi` | `uint30` | ID | Recipient MMSI |
| `70..70` | `71..71` | 1 | Retransmit Flag | `retransmit` | `bool` | Flag | `0` = No retransmission; `1` = Retransmitted |
| `71..71` | `72..72` | 1 | Spare | `spare` | `uint1` | — | `0` |
| `72..1007` | `73..1008` | 6–936 | Safety-Related Text | `text` | `str6` | 1–156 chars | 6-bit ASCII (+ `0–4` trailing pad bits to byte boundary) |

---

### Table A.10: Message 14 — Safety-Related Broadcast Message
* **Total Length:** `40 to 1008 bits` (1 to 5 slots; `40-bit` header + `1` to `161` 6-bit ASCII characters).
* **Access Scheme:** `RATDMA`, `FATDMA`, or `ITDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `14` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | Source ID (MMSI) | `mmsi` | `uint30` | ID | Sender MMSI (or `970/972/974xxxxxx` for SART/MOB/EPIRB) |
| `38..39` | `39..40` | 2 | Spare | `spare` | `uint2` | — | `0` |
| `40..1007` | `41..1008` | 6–966 | Safety-Related Text | `text` | `str6` | 1–161 chars | 6-bit ASCII (e.g., `"SART ACTIVE"` or `"SART TEST"`) |

---

### Table A.11: Message 15 — Interrogation
* **Total Length:** `88`, `110`, `112`, or `160 bits` (1 slot; interrogates 1 station for 1–2 message types, or 2 stations).
* **Access Scheme:** `RATDMA`, `FATDMA`, or `ITDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `15` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | Source ID (MMSI) | `mmsi` | `uint30` | ID | Interrogating Base Station or Ship MMSI |
| `38..39` | `39..40` | 2 | Spare | `spare` | `uint2` | — | `0` |
| `40..69` | `41..70` | 30 | Destination ID 1 (MMSI) | `mmsi_1` | `uint30` | ID | First interrogated MMSI |
| `70..75` | `71..76` | 6 | Message ID 1.1 | `msg_1_1` | `uint6` | Msg ID | Requested message type (`1–27`, e.g., `3` or `5`) |
| `76..87` | `77..88` | 12 | Slot Offset 1.1 | `slot_offset_1_1` | `uint12` | Slots | Response slot offset (`0` = autonomous slot selection) |
| `88..89` | `89..90` | 2 | Spare | `spare2` | `uint2` | — | *Optional* (present if $>88\text{ bits}$) |
| `90..95` | `91..96` | 6 | Message ID 1.2 | `msg_1_2` | `uint6` | Msg ID | *Optional* 2nd requested message from `mmsi_1` |
| `96..107` | `97..108` | 12 | Slot Offset 1.2 | `slot_offset_1_2` | `uint12` | Slots | *Optional* slot offset for `msg_1_2` |
| `108..109` | `109..110` | 2 | Spare | `spare3` | `uint2` | — | *Optional* |
| `110..139` | `111..140` | 30 | Destination ID 2 (MMSI) | `mmsi_2` | `uint30` | ID | *Optional* second interrogated MMSI (if $160\text{ bits}$) |
| `140..145` | `141..146` | 6 | Message ID 2.1 | `msg_2_1` | `uint6` | Msg ID | *Optional* requested message from `mmsi_2` |
| `146..157` | `147..158` | 12 | Slot Offset 2.1 | `slot_offset_2_1` | `uint12` | Slots | *Optional* slot offset for `msg_2_1` |
| `158..159` | `159..160` | 2 | Spare | `spare4` | `uint2` | — | *Optional* (`0`) |

---

### Table A.12: Message 16 — Assigned Mode Command
* **Total Length:** `96 bits` (1 target MMSI) or `144 bits` (2 target MMSIs) (1 slot).
* **Access Scheme:** `FATDMA` or `RATDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `16` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | Source ID (MMSI) | `mmsi` | `uint30` | ID | Commanding Base Station MMSI (`00MIDxxxx`) |
| `38..39` | `39..40` | 2 | Spare | `spare` | `uint2` | — | `0` |
| `40..69` | `41..70` | 30 | Destination ID A (MMSI) | `dest_mmsi_a` | `uint30` | ID | First assigned vessel MMSI |
| `70..81` | `71..82` | 12 | Offset A | `offset_a` | `uint12` | Slots or Rate | Slot offset (`0–3999`); or TXs per $10\text{ min}$ if `inc_a = 0` |
| `82..91` | `83..92` | 10 | Increment A | `inc_a` | `uint10` | Slots | Slot step per frame (`0` = rate assignment via `offset_a`) |
| `92..95` | `93..96` | 4 | Spare (if 96-bit) | `spare2` | `uint4` | — | Present **only** in 1-station (`96-bit`) variant! |
| `92..121` | `93..122` | 30 | Destination ID B (MMSI) | `dest_mmsi_b` | `uint30` | ID | Second assigned vessel MMSI (in `144-bit` variant) |
| `122..133` | `123..134` | 12 | Offset B | `offset_b` | `uint12` | Slots or Rate | Slot offset or TX rate for Station B (`144-bit` variant) |
| `134..143` | `135..144` | 10 | Increment B | `inc_b` | `uint10` | Slots | Slot step for Station B (`144-bit` variant) |

---

### Table A.13: Message 17 — DGNSS Broadcast Binary Message
* **Total Length:** `80 to 816 bits` (1 to 5 slots; `80-bit` AIS header + `0` to `29` 24-bit RTCM SC-104 v2.x words without parity).
* **Access Scheme:** `FATDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `17` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | Source ID (MMSI) | `mmsi` | `uint30` | ID | Base Station MMSI (`00MIDxxxx`) |
| `38..39` | `39..40` | 2 | Spare | `spare` | `uint2` | — | `0` |
| `40..57` | `41..58` | 18 | Ref Station Longitude | `x` / `longitude` | `int18` | $\frac{1}{10}\text{ min}$ ($\frac{1}{600}^\circ$) | $[-180^\circ, +180^\circ]$; **`181.0°` (`108600`) = N/A** |
| `58..74` | `59..75` | 17 | Ref Station Latitude | `y` / `latitude` | `int17` | $\frac{1}{10}\text{ min}$ ($\frac{1}{600}^\circ$) | $[-90^\circ, +90^\circ]$; **`91.0°` (`54600`) = N/A** |
| `75..79` | `76..80` | 5 | Spare | `spare2` | `uint5` | — | `0` |
| `80..85` | `81..86` | 6 | RTCM Message Type | `rtcm_type` | `uint6` | RTCM SC-104 | `1` (Full DGPS set) or `9` (Partial satellite set) |
| `86..95` | `87..96` | 10 | Reference Station ID | `station_id` | `uint10` | ID | `0–1023` (RTCM Reference Station ID) |
| `96..108` | `97..109` | 13 | Modified Z-Count | `z_count` | `uint13` | $0.6\text{ s}$ | `0–5999` ($0.0\text{–}3599.4\text{ s}$) |
| `109..111` | `110..112` | 3 | Sequence Number | `seq_num` | `uint3` | Counter | `0–7` |
| `112..116` | `113..117` | 5 | Length of Frame ($N_w$) | `word_count` | `uint5` | 24-bit words | Number of 24-bit RTCM words |
| `117..119` | `118..120` | 3 | Station Health | `health` | `uint3` | Enum | `0–5` = Scale factor; `6` = Unmonitored; `7` = Not working |
| `120..815` | `121..816` | $40 \times N_{\text{sat}}$ | Satellite Correction Blocks | `sat_corrections` | `raw` | 40b / sat | Each sat: `Scale`(1b), `UDRE`(2b), `SatID`(5b), `PRC`(`int16`), `RRC`(`int8`), `IOD`(`uint8`) |

---

### Table A.14: Message 18 — Standard Class B Equipment Position Report
* **Total Length:** `168 bits` (1 slot; 28 NMEA 6-bit armor characters, `0` fill bits).
* **Access Scheme:** `CSTDMA` (Class B "CS") or `SOTDMA` / `ITDMA` (Class B "SO").

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `18` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | User ID (MMSI) | `mmsi` | `uint30` | ID | `000000000`–`999999999` |
| `38..45` | `39..46` | 8 | Regional Reserved | `reserved_1` | `uint8` | — | `0` |
| `46..55` | `47..56` | 10 | Speed Over Ground (SOG) | `sog` | `uint10` | $0.1\text{ knot}$ | `0.0–102.1 kts` (`1022` = $\ge 102.2$); **`1023` = N/A** |
| `56..56` | `57..57` | 1 | Position Accuracy | `position_accuracy` | `bool` | Flag | `1` = High ($\le 10\text{ m}$); `0` = Low ($>10\text{ m}$) |
| `57..84` | `58..85` | 28 | Longitude ($\lambda$) | `x` / `longitude` | `int28` | $\frac{1}{600{,}000}^\circ$ | $[-180^\circ, +180^\circ]$; **`181.0°` (`0x6791AC0`) = N/A** |
| `85..111` | `86..112` | 27 | Latitude ($\phi$) | `y` / `latitude` | `int27` | $\frac{1}{600{,}000}^\circ$ | $[-90^\circ, +90^\circ]$; **`91.0°` (`0x3412140`) = N/A** |
| `112..123` | `113..124` | 12 | Course Over Ground (COG)| `cog` | `uint12` | $0.1^\circ\text{ true}$ | `0.0°–359.9°`; **`3600` (`360.0°`) = N/A** |
| `124..132` | `125..133` | 9 | True Heading (HDG) | `true_heading` | `uint9` | $1^\circ\text{ true}$ | `0–359°`; **`511` (`0x1FF`) = N/A** |
| `133..138` | `134..139` | 6 | Time Stamp | `timestamp` | `uint6` | UTC second | `0–59 s`; **`60`=N/A, `61`=Manual, `62`=DR, `63`=Inop** |
| `139..140` | `140..141` | 2 | Regional Reserved | `reserved_2` | `uint2` | — | `0` |
| `141..141` | `142..142` | 1 | Class B Unit Flag | `unit_flag` | `bool` | Enum | **`0` = Class B SOTDMA ("SO"); `1` = Class B CSTDMA ("CS")** |
| `142..142` | `143..143` | 1 | Class B Display Flag | `display_flag` | `bool` | Flag | `0` = No display; `1` = Integrated display for safety text |
| `143..143` | `144..144` | 1 | Class B DSC Flag | `dsc_flag` | `bool` | Flag | `0` = No DSC; `1` = Equipped with Ch 70 DSC function |
| `144..144` | `145..145` | 1 | Class B Band Flag | `band_flag` | `bool` | Flag | `0` = Upper $525\text{ kHz}$ only; `1` = Whole marine VHF band |
| `145..145` | `146..146` | 1 | Class B Msg 22 Flag | `m22_flag` | `bool` | Flag | `0` = AIS 1/2 only; `1` = Supports Msg 22 channel mgmt |
| `146..146` | `147..147` | 1 | Mode Flag | `mode_flag` | `bool` | Flag | `0` = Autonomous mode; `1` = Assigned mode |
| `147..147` | `148..148` | 1 | RAIM Flag | `raim` | `bool` | Flag | `0` = Not in use; `1` = In use |
| `148..148` | `149..149` | 1 | Comm State Selector Flag| `commstate_flag` | `bool` | Selector | `0` = SOTDMA; `1` = ITDMA (Always `1` for CSTDMA units) |
| `149..167` | `150..168` | 19 | Communication State | `comm_state` | `uint19` | Table A.25 | SOTDMA/ITDMA, or constant `0x30006` (`1100000000000000110`) for CS |

---

### Table A.15: Message 19 — Extended Class B Equipment Position Report
* **Total Length:** `312 bits` (2 slots; 52 NMEA 6-bit armor characters, `0` fill bits).
* **Access Scheme:** `ITDMA` or `CSTDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `19` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | User ID (MMSI) | `mmsi` | `uint30` | ID | `000000000`–`999999999` |
| `38..45` | `39..46` | 8 | Regional Reserved | `reserved_1` | `uint8` | — | `0` |
| `46..55` | `47..56` | 10 | Speed Over Ground (SOG) | `sog` | `uint10` | $0.1\text{ knot}$ | `0.0–102.1 kts`; **`1023` = N/A** |
| `56..56` | `57..57` | 1 | Position Accuracy | `position_accuracy` | `bool` | Flag | `1` = High ($\le 10\text{ m}$); `0` = Low ($>10\text{ m}$) |
| `57..84` | `58..85` | 28 | Longitude ($\lambda$) | `x` / `longitude` | `int28` | $\frac{1}{600{,}000}^\circ$ | $[-180^\circ, +180^\circ]$; **`181.0°` (`0x6791AC0`) = N/A** |
| `85..111` | `86..112` | 27 | Latitude ($\phi$) | `y` / `latitude` | `int27` | $\frac{1}{600{,}000}^\circ$ | $[-90^\circ, +90^\circ]$; **`91.0°` (`0x3412140`) = N/A** |
| `112..123` | `113..124` | 12 | Course Over Ground (COG)| `cog` | `uint12` | $0.1^\circ\text{ true}$ | `0.0°–359.9°`; **`3600` (`360.0°`) = N/A** |
| `124..132` | `125..133` | 9 | True Heading (HDG) | `true_heading` | `uint9` | $1^\circ\text{ true}$ | `0–359°`; **`511` = N/A** |
| `133..138` | `134..139` | 6 | Time Stamp | `timestamp` | `uint6` | UTC second | `0–59 s`; `60–63` = Special/N/A |
| `139..142` | `140..143` | 4 | Regional Reserved | `reserved_2` | `uint4` | — | `0` |
| `143..262` | `144..263` | 120 | Vessel Name | `name` | `str6` | 20 chars | 6-bit ASCII; **`@@@@@@@@@@@@@@@@@@@@` = N/A** |
| `263..270` | `264..271` | 8 | Type of Ship and Cargo | `type_and_cargo` | `uint8` | Enum (Table A.28) | `0–99` (`0` = N/A) |
| `271..279` | `272..280` | 9 | Dimension to Bow ($A$) | `dim_a` | `uint9` | $1\text{ m}$ | `0–511 m` |
| `280..288` | `281..289` | 9 | Dimension to Stern ($B$) | `dim_b` | `uint9` | $1\text{ m}$ | `0–511 m` |
| `289..294` | `290..295` | 6 | Dimension to Port ($C$) | `dim_c` | `uint6` | $1\text{ m}$ | `0–63 m` |
| `295..300` | `296..301` | 6 | Dimension to Starboard ($D$) | `dim_d` | `uint6` | $1\text{ m}$ | `0–63 m` |
| `301..304` | `302..305` | 4 | Type of EPFD | `fix_type` | `uint4` | Enum (Table A.27) | `0–15` |
| `305..305` | `306..306` | 1 | RAIM Flag | `raim` | `bool` | Flag | `0` = Not in use; `1` = In use |
| `306..306` | `307..307` | 1 | DTE Flag | `dte` | `bool` | Flag | `0` = Available; `1` = Not available |
| `307..307` | `308..308` | 1 | Assigned Mode Flag | `assigned` | `bool` | Flag | `0` = Autonomous; `1` = Assigned |
| `308..311` | `309..312` | 4 | Spare | `spare` | `uint4` | — | `0` |

---

### Table A.16: Message 20 — Data Link Management Message
* **Total Length:** `72`, `104`, `136`, or `160 bits` (1 slot; reserves 1, 2, 3, or 4 FATDMA slot blocks).
* **Access Scheme:** `FATDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `20` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | Source ID (MMSI) | `mmsi` | `uint30` | ID | Base Station MMSI (`00MIDxxxx`) |
| `38..39` | `39..40` | 2 | Spare | `spare` | `uint2` | — | `0` |
| `40..51` | `41..52` | 12 | Offset Number 1 | `offset_1` | `uint12` | Slots | `0–2249` (offset from current slot) |
| `52..55` | `53..56` | 4 | Number of Reserved Slots 1| `num_slots_1` | `uint4` | Slots | `1–5` consecutive slots (`0` = cancel reservation) |
| `56..58` | `57..59` | 3 | Time-Out 1 | `timeout_1` | `uint3` | Minutes | `1–7` minutes until reservation expires |
| `59..69` | `60..70` | 11 | Increment 1 | `incr_1` | `uint11` | Slots | `0–2047` slot spacing between repeating blocks |
| `70..99` | `71..100` | 30 | Reservation Block 2 | `offset_2`..`incr_2`| $12+4+3+11\text{b}$| — | *Optional* Block 2 (`offset_2`, `num_slots_2`, `timeout_2`, `incr_2`) |
| `100..129` | `101..130` | 30 | Reservation Block 3 | `offset_3`..`incr_3`| $12+4+3+11\text{b}$| — | *Optional* Block 3 |
| `130..159` | `131..160` | 30 | Reservation Block 4 | `offset_4`..`incr_4`| $12+4+3+11\text{b}$| — | *Optional* Block 4 (padded with `2/4/6/0` spare bits for 1/2/3/4 blocks) |

---

### Table A.17: Message 21 — Aids-to-Navigation (AtoN) Report
* **Total Length:** `272 to 360 bits` (2 slots; `272-bit` base message + `0` to `84` bits of `Name Extension` + `0–6` spare bits to byte boundary).
* **Access Scheme:** `FATDMA` or `RATDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `21` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | ID (MMSI) | `mmsi` | `uint30` | ID | `99MID1xxx` (Physical) or `99MID6xxx` (Virtual) |
| `38..42` | `39..43` | 5 | Type of Aid to Navigation | `aton_type` | `uint5` | Enum (Table A.29) | `0–31` (`0` = Default / not specified) |
| `43..162` | `44..163` | 120 | Name of Aid to Navigation | `name` | `str6` | 20 chars | 6-bit ASCII |
| `163..163` | `164..164` | 1 | Position Accuracy | `position_accuracy` | `bool` | Flag | `1` = High ($\le 10\text{ m}$); `0` = Low ($>10\text{ m}$) |
| `164..191` | `165..192` | 28 | Longitude ($\lambda$) | `x` / `longitude` | `int28` | $\frac{1}{600{,}000}^\circ$ | $[-180^\circ, +180^\circ]$; **`181.0°` (`0x6791AC0`) = N/A** |
| `192..218` | `193..219` | 27 | Latitude ($\phi$) | `y` / `latitude` | `int27` | $\frac{1}{600{,}000}^\circ$ | $[-90^\circ, +90^\circ]$; **`91.0°` (`0x3412140`) = N/A** |
| `219..227` | `220..228` | 9 | Dimension to Bow ($A$) | `dim_a` | `uint9` | $1\text{ m}$ | `0–511 m` (`0` for Virtual AtoN or circular buoy) |
| `228..236` | `229..237` | 9 | Dimension to Stern ($B$) | `dim_b` | `uint9` | $1\text{ m}$ | `0–511 m` |
| `237..242` | `238..243` | 6 | Dimension to Port ($C$) | `dim_c` | `uint6` | $1\text{ m}$ | `0–63 m` (if $A=B=0$, $C$ and $D$ encode diameter) |
| `243..248` | `244..249` | 6 | Dimension to Starboard ($D$) | `dim_d` | `uint6` | $1\text{ m}$ | `0–63 m` |
| `249..252` | `250..253` | 4 | Type of EPFD | `fix_type` | `uint4` | Enum (Table A.27) | `0–15` (`7` = Surveyed for fixed/virtual AtoN) |
| `253..258` | `254..259` | 6 | Time Stamp | `timestamp` | `uint6` | UTC second | `0–59 s`; `60`=N/A, `61`=Manual, `62`=Est, `63`=Inop |
| `259..259` | `260..260` | 1 | Off-Position Indicator | `off_position` | `bool` | Flag | `0` = On position; **`1` = Off position** (valid if `TS` $\le 59$) |
| `260..267` | `261..268` | 8 | AtoN Status | `aton_status` | `uint8` | Bitmask | Regional / IALA lantern & RACON health indicators |
| `268..268` | `269..269` | 1 | RAIM Flag | `raim` | `bool` | Flag | `0` = Not in use; `1` = In use |
| `269..269` | `270..270` | 1 | Virtual AtoN Flag | `virtual_aton` | `bool` | Flag | **`0` = Real/Synthetic AtoN; `1` = Virtual AtoN** |
| `270..270` | `271..271` | 1 | Assigned Mode Flag | `assigned` | `bool` | Flag | `0` = Autonomous/FATDMA; `1` = Assigned mode |
| `271..271` | `272..272` | 1 | Spare | `spare` | `uint1` | — | `0` |
| `272..359` | `273..360` | 0–88 | Name Extension + Pad | `name_ext` | `str6` | 0–14 chars | Up to 14 6-bit ASCII chars (`0–84b`) + `0, 2, 4, or 6` pad bits |

---

### Table A.18: Message 22 — Channel Management (Geographic Broadcast & Addressed Modes)
* **Total Length:** `168 bits` (1 slot).
* **Access Scheme:** `FATDMA` or `RATDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `22` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | Source ID (MMSI) | `mmsi` | `uint30` | ID | Base Station MMSI (`00MIDxxxx`) |
| `38..39` | `39..40` | 2 | Spare | `spare` | `uint2` | — | `0` |
| `40..51` | `41..52` | 12 | Channel A | `chan_a` | `uint12` | ITU-R M.1084 | VHF Channel number (`2087` = AIS 1 [$161.975\text{ MHz}$]) |
| `52..63` | `53..64` | 12 | Channel B | `chan_b` | `uint12` | ITU-R M.1084 | VHF Channel number (`2088` = AIS 2 [$162.025\text{ MHz}$]) |
| `64..67` | `65..68` | 4 | Tx/Rx Mode | `txrx_mode` | `uint4` | Enum | `0`=TxA/TxB, RxA/RxB; `1`=TxA, RxA/B; `2`=TxB, RxA/B |
| `68..68` | `69..69` | 1 | Power | `power_low` | `bool` | Flag | `0` = High power ($12.5\text{ W}$); `1` = Low power ($1\text{ W}$) |
| `69..86` | `70..87` | 18 | **If `Addressed=0`:** NE Lon 1 | `ne_lon` | `int18` | $\frac{1}{10}\text{ min}$ ($\frac{1}{600}^\circ$) | North-East corner Longitude ($[-180^\circ, +180^\circ]$) |
| `87..103` | `88..104` | 17 | **If `Addressed=0`:** NE Lat 1 | `ne_lat` | `int17` | $\frac{1}{10}\text{ min}$ ($\frac{1}{600}^\circ$) | North-East corner Latitude ($[-90^\circ, +90^\circ]$) |
| `104..121` | `105..122` | 18 | **If `Addressed=0`:** SW Lon 2 | `sw_lon` | `int18` | $\frac{1}{10}\text{ min}$ ($\frac{1}{600}^\circ$) | South-West corner Longitude ($[-180^\circ, +180^\circ]$) |
| `122..138` | `123..139` | 17 | **If `Addressed=0`:** SW Lat 2 | `sw_lat` | `int17` | $\frac{1}{10}\text{ min}$ ($\frac{1}{600}^\circ$) | South-West corner Latitude ($[-90^\circ, +90^\circ]$) |
| `69..98` | `70..99` | 30 | **If `Addressed=1`:** Dest MMSI 1| `dest_mmsi_1` | `uint30` | ID | Addressed MMSI 1 (plus 5 spare bits at `99..103`) |
| `104..133` | `105..134` | 30 | **If `Addressed=1`:** Dest MMSI 2| `dest_mmsi_2` | `uint30` | ID | Addressed MMSI 2 (plus 5 spare bits at `134..138`) |
| `139..139` | `140..140` | 1 | **Addressed Broadcast Flag** | `addressed` | `bool` | Selector | **`0` = Broadcast Geographic Box; `1` = Addressed MMSIs** |
| `140..140` | `141..141` | 1 | Channel A Bandwidth | `band_a` | `bool` | Flag | `0` = Default by channel number; `1` = $12.5\text{ kHz}$ |
| `141..141` | `142..142` | 1 | Channel B Bandwidth | `band_b` | `bool` | Flag | `0` = Default by channel number; `1` = $12.5\text{ kHz}$ |
| `142..144` | `143..145` | 3 | Transitional Zone Size | `zone_size` | `uint3` | $\text{Value} + 1\text{ NM}$| `0–7` $\rightarrow$ **$1\text{ to }8\text{ NM}$** (`4` = $5\text{ NM}$ default) |
| `145..167` | `146..168` | 23 | Spare | `spare2` | `uint23` | — | `0` |

---

### Table A.19: Message 23 — Group Assignment Command
* **Total Length:** `160 bits` (1 slot; 27 NMEA 6-bit armor characters with `2` fill bits).
* **Access Scheme:** `FATDMA` or `RATDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `23` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | Source ID (MMSI) | `mmsi` | `uint30` | ID | Base Station MMSI (`00MIDxxxx`) |
| `38..39` | `39..40` | 2 | Spare | `spare` | `uint2` | — | `0` |
| `40..57` | `41..58` | 18 | North-East Longitude 1 | `ne_lon` | `int18` | $\frac{1}{10}\text{ min}$ ($\frac{1}{600}^\circ$) | $[-180^\circ, +180^\circ]$ |
| `58..74` | `59..75` | 17 | North-East Latitude 1 | `ne_lat` | `int17` | $\frac{1}{10}\text{ min}$ ($\frac{1}{600}^\circ$) | $[-90^\circ, +90^\circ]$ |
| `75..92` | `76..93` | 18 | South-West Longitude 2 | `sw_lon` | `int18` | $\frac{1}{10}\text{ min}$ ($\frac{1}{600}^\circ$) | $[-180^\circ, +180^\circ]$ |
| `93..109` | `94..110` | 17 | South-West Latitude 2 | `sw_lat` | `int17` | $\frac{1}{10}\text{ min}$ ($\frac{1}{600}^\circ$) | $[-90^\circ, +90^\circ]$ |
| `110..113` | `111..114` | 4 | Station Type | `station_type` | `uint4` | Enum (Table A.30) | `0` = All stations; `2` = All Class B; `3` = SAR; `5` = Class B CS |
| `114..121` | `115..122` | 8 | Type of Ship and Cargo | `type_and_cargo` | `uint8` | Enum (Table A.28) | `0` = All ship types; `10–99` = Specific category |
| `122..143` | `123..144` | 22 | Spare | `spare2` | `uint22` | — | `0` |
| `144..145` | `145..146` | 2 | Tx/Rx Mode | `txrx_mode` | `uint2` | Enum | `0`=TxA/TxB; `1`=TxA only; `2`=TxB only; `3`=Reserved |
| `146..149` | `147..150` | 4 | Reporting Interval | `interval_raw` | `uint4` | Enum (Table A.30) | `0`=Autonomous; `1`=$10\text{m}$ .. `9`=$2\text{s}$; `10`=Class B CS $5\text{s}$ |
| `150..153` | `151..154` | 4 | **Quiet Time** | `quiet` | `uint4` | Minutes | **`0` = None; `1–15` = Silence all TX for $1\text{–}15\text{ min}$!** |
| `154..159` | `155..160` | 6 | Spare | `spare3` | `uint6` | — | `0` |

---

### Table A.20: Message 24 Part A — Static Data Report (`Part Number = 0`)
* **Total Length:** `160 bits` (or `168 bits` with 8 trailing spare bits; 1 slot).
* **Access Scheme:** `RATDMA`, `CSTDMA`, or `ITDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `24` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | User ID (MMSI) | `mmsi` | `uint30` | ID | `000000000`–`999999999` |
| `38..39` | `39..40` | 2 | Part Number | `part_num` | `uint2` | Selector | **`0` = Part A** |
| `40..159` | `41..160` | 120 | Vessel Name | `name` | `str6` | 20 chars | 6-bit ASCII; **`@@@@@@@@@@@@@@@@@@@@` = N/A** |
| `160..167` | `161..168` | 0 or 8 | Optional Spare | `spare` | `uint8` | — | Present only if transmitter pads Part A to `168 bits` |

---

### Table A.21: Message 24 Part B — Static Data Report (`Part Number = 1`)
* **Total Length:** `168 bits` (1 slot; 28 NMEA 6-bit armor characters, `0` fill bits).
* **Access Scheme:** `RATDMA`, `CSTDMA`, or `ITDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `24` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | User ID (MMSI) | `mmsi` | `uint30` | ID | `000000000`–`999999999` (`98MIDxxxx` = Auxiliary Craft) |
| `38..39` | `39..40` | 2 | Part Number | `part_num` | `uint2` | Selector | **`1` = Part B** |
| `40..47` | `41..48` | 8 | Type of Ship and Cargo | `type_and_cargo` | `uint8` | Enum (Table A.28) | `0–99` (`0` = Not available) |
| `48..65` | `49..66` | 18 | Vendor ID (Mfg ID) | `vendor_id` | `str6` | 3 chars | 3-char manufacturer code (or 7-char `48..89` in M.1371-3) |
| `66..69` | `67..70` | 4 | Unit Model Code | `model` | `uint4` | Code | `1–15`; `0` = Not available |
| `70..89` | `71..90` | 20 | Unit Serial Number | `serial` | `uint20` | Number | `1–1048575`; `0` = Not available |
| `90..131` | `91..132` | 42 | Call Sign | `callsign` | `str6` | 7 chars | 6-bit ASCII; **`@@@@@@@` = N/A** |
| `132..140` | `133..141` | 9 | **If Standard:** Dim to Bow ($A$)| `dim_a` | `uint9` | $1\text{ m}$ | `0–511 m` (when MMSI does **not** begin with `98`) |
| `141..149` | `142..150` | 9 | **If Standard:** Dim to Stern ($B$)| `dim_b` | `uint9` | $1\text{ m}$ | `0–511 m` |
| `150..155` | `151..156` | 6 | **If Standard:** Dim to Port ($C$)| `dim_c` | `uint6` | $1\text{ m}$ | `0–63 m` |
| `156..161` | `157..162` | 6 | **If Standard:** Dim to Stbd ($D$)| `dim_d` | `uint6` | $1\text{ m}$ | `0–63 m` |
| `132..161` | `133..162` | 30 | **If `98MIDxxxx`:** Mothership ID | `mothership_mmsi` | `uint30` | ID | **Parent ship 9-digit MMSI** (when sender is Auxiliary Craft!) |
| `162..167` | `163..168` | 6 | Spare | `spare` | `uint6` | — | `0` |

---

### Table A.22: Message 25 — Single Slot Binary Message
* **Total Length:** `40 to 168 bits` (1 slot; 4 header variants determined by `Addressed` [`bit 38`] and `Structured` [`bit 39`]).
* **Access Scheme:** `RATDMA`, `ITDMA`, `FATDMA`, or `CSTDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Condition (`Addressed` `A`, `Structured` `S`) |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `25` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | `0–3` |
| `8..37` | `9..38` | 30 | Source ID (MMSI) | `mmsi` | `uint30` | ID | Sender MMSI |
| `38..38` | `39..39` | 1 | Destination Indicator (`A`) | `addressed` | `bool` | Selector | `0` = Broadcast; `1` = Addressed (`dest_mmsi` present) |
| `39..39` | `40..40` | 1 | Binary Data Flag (`S`) | `use_app_id` | `bool` | Selector | `0` = Unstructured raw bits; `1` = 16-bit `DAC`+`FI` present |
| `40..69` | `41..70` | 30 | Destination MMSI (+2b spare)| `dest_mmsi` | `uint30`+`2b`| ID | Present **only if `A = 1`** (`bits 40..69` MMSI, `70..71` spare) |
| `40..55` or `72..87`| `41..56` or `73..88`| 16 | Application ID (`DAC`+`FI`) | `dac` (10b), `fi` (6b)| `uint16` | DAC/FI | Present **only if `S = 1`** (`40..55` if `A=0`; `72..87` if `A=1`) |
| `40/56/72/88..167` | `41/57/73/89..168` | 0–128 | Binary Payload | `binary_data` | `raw` | Bits | Up to `128b` (`A=0,S=0`), `112b` (`A=0,S=1`), `96b` (`A=1,S=0`), `80b` (`A=1,S=1`) |

---

### Table A.23: Message 26 — Multiple Slot Binary Message with Communication State
* **Total Length:** `60 to 1004 bits` (1 to 5 slots; identical header/payload to Message 25, followed by a mandatory **20-bit Communication State Footer** at the very end of the bitstring!).
* **Access Scheme:** `SOTDMA`, `ITDMA`, or `FATDMA`.

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Condition (`N` = Total Bit Length of Message 26) |
|---|---|---:|---|---|---|---|---|
| `0..39` | `1..40` | 40 | Header (`ID=26`, `Repeat`, `MMSI`, `A`, `S`) | `message_id`..`use_app_id` | — | — | Same layout as Message 25 (`bits 0..39`), with `message_id = 26` |
| `40..87` | `41..88` | 0–48 | Optional `dest_mmsi` & `DAC`/`FI`| `dest_mmsi`, `dac`, `fi` | — | — | Same conditional rules on `A` (`bit 38`) and `S` (`bit 39`) as Msg 25 |
| `hdr..N-21` | `hdr+1..N-20` | 0–944 | Binary Payload + Byte Pad | `binary_data` | `raw` | Bits | Variable-length payload up to 5 slots minus 20-bit footer |
| **`N-20..N-20`**| **`N-19..N-19`**| **1** | **Comm State Selector Flag**| `commstate_flag` | `bool` | Selector | **`0` = SOTDMA state follows; `1` = ITDMA state follows** |
| **`N-19..N-1`** | **`N-18..N`** | **19**| **Communication State** | `comm_state` | `uint19` | Table A.25 | **Final 19 bits of the message (`SOTDMA` or `ITDMA`)** |

---

### Table A.24: Message 27 — Position Report for Long-Range Applications (Satellite AIS)
* **Total Length:** `96 bits` (1 slot; 16 NMEA 6-bit armor characters, `0` fill bits; $15.83\text{ ms}$ total over-the-air frame).
* **Access Scheme:** Random unscheduled access (no slot reservation; transmitted on **Ch 75 [$156.775\text{ MHz}$] and Ch 76 [$156.825\text{ MHz}$]**).

| 0-Based Bits | 1-Based ITU Bits | Width | Field Name | `libais` / Variable Name | Type | Scale / Units | Valid Range & Sentinel ("Not Available") |
|---|---|---:|---|---|---|---|---|
| `0..5` | `1..6` | 6 | Message ID | `message_id` | `uint6` | Enum | `27` |
| `6..7` | `7..8` | 2 | Repeat Indicator | `repeat_indicator` | `uint2` | Hops | **`3` (Always `3` = Do not repeat!)** |
| `8..37` | `9..38` | 30 | User ID (MMSI) | `mmsi` | `uint30` | ID | `000000000`–`999999999` |
| `38..38` | `39..39` | 1 | Position Accuracy | `position_accuracy` | `bool` | Flag | `1` = High ($\le 10\text{ m}$); `0` = Low ($>10\text{ m}$) |
| `39..39` | `40..40` | 1 | RAIM Flag | `raim` | `bool` | Flag | `0` = Not in use; `1` = In use |
| `40..43` | `41..44` | 4 | Navigation Status | `nav_status` | `uint4` | Enum (Table A.26) | `0–14`; **`15` = Not defined (default)** |
| `44..61` | `45..62` | 18 | Longitude ($\lambda$) | `x` / `longitude` | `int18` | $\frac{1}{10}\text{ min}$ ($\frac{1}{600}^\circ$) | $[-180^\circ, +180^\circ]$; **`181.0°` (`108600` / `0x1A838`) = N/A** |
| `62..78` | `63..79` | 17 | Latitude ($\phi$) | `y` / `latitude` | `int17` | $\frac{1}{10}\text{ min}$ ($\frac{1}{600}^\circ$) | $[-90^\circ, +90^\circ]$; **`91.0°` (`54600` / `0xD548`) = N/A** |
| `79..84` | `80..85` | 6 | Speed Over Ground (SOG) | `sog` | `uint6` | $1\text{ knot}$ | `0–62 knots`; **`63` (`0x3F`) = N/A** |
| `85..93` | `86..94` | 9 | Course Over Ground (COG)| `cog` | `uint9` | $1^\circ\text{ true}$ | `0–359°`; **`511` (`0x1FF`) = N/A** |
| `94..94` | `95..95` | 1 | GNSS Position Status | `gnss` | `bool` | Latency Flag | **`0` = Current GNSS fix ($<5\text{ s}$); `1` = Not current ($>5\text{ s}$)** |
| `95..95` | `96..96` | 1 | Spare | `spare` | `uint1` | — | `0` |

---

## A.3 Standard Enumeration & Sub-Structure Lookup Tables

### Table A.25: 19-Bit SOTDMA and ITDMA Communication State Bit Layouts
*Applies to `bits 149..167` of Messages 1, 2, 3, 4, 9, 11, 18, and the final 19 bits of Message 26.*

| Scheme | Relative Bits (`0..18`) | 1-Slot Bits (`149..167`) | Width | Field Name | Type | Interpretation & Polymorphic Rules |
|---|---|---|---:|---|---|---|
| **SOTDMA** | `0..1` | `149..150` | 2 | `sync_state` | `uint2` | `0`=UTC Direct; `1`=UTC Indirect; `2`=Base Station; `3`=Peer Station Count |
| **SOTDMA** | `2..4` | `151..153` | 3 | `slot_timeout` | `uint3` | `0–7` frames remaining until slot change |
| **SOTDMA** | `5..18` | `154..167` | 14 | `received_stations` | `uint14`| **When `slot_timeout` $\in \{3, 5, 7\}$:** Count of received stations (`0–16383`) |
| **SOTDMA** | `5..18` | `154..167` | 14 | `slot_number` | `uint14`| **When `slot_timeout` $\in \{2, 4, 6\}$:** Current slot number (`0–2249`) |
| **SOTDMA** | `5..9`, `10..16`, `17..18` | `154..158`, `159..165`, `166..167` | $5+7+2$ | `utc_hour`, `utc_min`, `spare` | `uint5`, `uint7` | **When `slot_timeout` $= 1$:** UTC Hour (`0–23`) and UTC Minute (`0–59`) |
| **SOTDMA** | `5..18` | `154..167` | 14 | `slot_offset` | `uint14`| **When `slot_timeout` $= 0$:** Offset to next frame's new slot (`0` = release) |
| **ITDMA** | `0..1` | `149..150` | 2 | `sync_state` | `uint2` | `0`=UTC Direct; `1`=UTC Indirect; `2`=Base Station; `3`=Peer Station Count |
| **ITDMA** | `2..14` | `151..163` | 13 | `slot_increment` | `uint13`| Offset to next reserved slot (`0–8191`; `0` = autonomous / no reservation) |
| **ITDMA** | `15..17` | `164..166` | 3 | `num_slots` | `uint3` | `0–4` = 1 to 5 slots; `5–7` = 1 to 3 slots with `slot_increment + 8192` |
| **ITDMA** | `18..18` | `167..167` | 1 | `keep_flag` | `bool` | `1` = Keep current slot allocated for 1 additional frame; `0` = Release |
| **CSTDMA** | `0..18` | `149..167` | 19 | Constant (`0x30006`)| `uint19`| Fixed constant `1100000000000000110` (`sync=3`, `inc=0`, `slots=3`, `keep=0`) |

---

### Table A.26: Navigation Status Codes (`0–15`, Messages 1, 2, 3, and 27)

| Code | Navigation Status Description | Code | Navigation Status Description |
|---:|---|---:|---|
| `0` | Under way using engine | `8` | Under way sailing |
| `1` | At anchor | `9` | Reserved for future amendment of Navigational Status for HSC |
| `2` | Not under command (NUC) | `10` | Reserved for future amendment of Navigational Status for WIG |
| `3` | Restricted maneuverability (RAM) | `11` | Power-driven vessel towing astern (regional use) |
| `4` | Constrained by her draught (CBD) | `12` | Power-driven vessel pushing ahead or towing alongside (regional use) |
| `5` | Moored | `13` | Reserved for future use |
| `6` | Aground | `14` | **AIS-SART (active), AIS-MOB, or EPIRB-AIS** |
| `7` | Engaged in fishing | `15` | **Undefined = default** (also used by AIS-SART/MOB under test) |

---

### Table A.27: Electronic Position Fixing Device (EPFD) Type Codes (`0–15`, Messages 4, 5, 11, 19, 21)

| Code | EPFD System Type | Code | EPFD System Type |
|---:|---|---:|---|
| `0` | Undefined (default) | `8` | Galileo |
| `1` | GPS | `9–14` | Reserved for future use |
| `2` | GLONASS | `15` | Internal GNSS (or Not Available in legacy receivers) |
| `3` | Combined GPS/GLONASS | | *Note: Multi-constellation receivers (GPS+Galileo+BDS) typically report `1` or `3`.* |
| `4` | Loran-C | | |
| `5` | Chayka | | |
| `6` | Integrated Navigation System (INS) | | |
| `7` | **Surveyed** (Fixed shore Base Station or fixed/virtual AtoN) | | |

---

### Table A.28: Complete Ship and Cargo Type Lookup Table (`0–99`, Messages 5, 19, 23, 24 Part B)

| Code | Ship and Cargo Type Description | Code | Ship and Cargo Type Description |
|---:|---|---:|---|
| `0` | **Not available (default)** | `50` | **Pilot Vessel** |
| `1–19` | Reserved for future use | `51` | **Search and Rescue vessel** |
| `20` | Wing in ground (WIG), all ships of this type | `52` | **Tug** |
| `21` | WIG, Hazardous category X (DG/HS/MP) | `53` | **Port Tender** |
| `22` | WIG, Hazardous category Y (DG/HS/MP) | `54` | **Anti-pollution equipment** |
| `23` | WIG, Hazardous category Z (DG/HS/MP) | `55` | **Law Enforcement** |
| `24` | WIG, Hazardous category OS (Other Substances) | `56` | Spare — for assignments to local vessel |
| `25–28` | WIG, Reserved for future use | `57` | Spare — for assignments to local vessel |
| `29` | WIG, No additional information | `58` | **Medical Transport** (1949 Geneva Conventions / Prot.) |
| `30` | **Fishing** | `59` | **Noncombatant ship** according to RR Resolution No. 18 |
| `31` | **Towing** | `60` | **Passenger**, all ships of this type |
| `32` | **Towing: length exceeds 200 m or breadth exceeds 25 m** | `61–64` | Passenger, Hazardous category X (`61`), Y (`62`), Z (`63`), OS (`64`) |
| `33` | **Dredging or underwater ops** | `65–68` | Passenger, Reserved for future use |
| `34` | **Diving ops** | `69` | Passenger, No additional information |
| `35` | **Military ops** | `70` | **Cargo**, all ships of this type |
| `36` | **Sailing** | `71–74` | Cargo, Hazardous category X (`71`), Y (`72`), Z (`73`), OS (`74`) |
| `37` | **Pleasure Craft** | `75–78` | Cargo, Reserved for future use |
| `38–39` | Reserved | `79` | Cargo, No additional information |
| `40` | **High speed craft (HSC)**, all ships of this type | `80` | **Tanker**, all ships of this type |
| `41` | HSC, Hazardous category X | `81–84` | Tanker, Hazardous category X (`81`), Y (`82`), Z (`83`), OS (`84`) |
| `42` | HSC, Hazardous category Y | `85–88` | Tanker, Reserved for future use |
| `43` | HSC, Hazardous category Z | `89` | Tanker, No additional information |
| `44` | HSC, Hazardous category OS | `90` | **Other Type**, all ships of this type |
| `45–48` | HSC, Reserved for future use | `91–94` | Other Type, Hazardous category X (`91`), Y (`92`), Z (`93`), OS (`94`) |
| `49` | HSC, No additional information | `95–98` | Other Type, Reserved for future use |
| | | `99` | Other Type, no additional information |

---

### Table A.29: Complete Aid-to-Navigation (AtoN) Type Lookup Table (`0–31`, Message 21)

| Code | Category | IALA / ITU-R M.1371-5 Aid to Navigation Description |
|---:|---|---|
| `0` | Default | Default, Type of Aid to Navigation not specified |
| `1` | Fixed | Reference point |
| `2` | Fixed | RACON (radar transponder marking a navigation hazard) |
| `3` | Fixed | Fixed structure off-shore, such as oil platforms, wind farms, rigs |
| `4` | Emergency | **Emergency Wreck Marking Buoy** (IALA Recommendation O-133) |
| `5` | Fixed | Light, without sectors |
| `6` | Fixed | Light, with sectors |
| `7` | Fixed | Leading Light Front |
| `8` | Fixed | Leading Light Rear |
| `9` | Fixed | Beacon, Cardinal N |
| `10` | Fixed | Beacon, Cardinal E |
| `11` | Fixed | Beacon, Cardinal S |
| `12` | Fixed | Beacon, Cardinal W |
| `13` | Fixed | Beacon, Port hand |
| `14` | Fixed | Beacon, Starboard hand |
| `15` | Fixed | Beacon, Preferred Channel port hand |
| `16` | Fixed | Beacon, Preferred Channel starboard hand |
| `17` | Fixed | Beacon, Isolated danger |
| `18` | Fixed | Beacon, Safe water |
| `19` | Fixed | Beacon, Special mark |
| `20` | Floating | Cardinal Mark N |
| `21` | Floating | Cardinal Mark E |
| `22` | Floating | Cardinal Mark S |
| `23` | Floating | Cardinal Mark W |
| `24` | Floating | Port hand Mark |
| `25` | Floating | Starboard hand Mark |
| `26` | Floating | Preferred Channel Port hand |
| `27` | Floating | Preferred Channel Starboard hand |
| `28` | Floating | Isolated danger |
| `29` | Floating | Safe Water |
| `30` | Floating | Special Mark |
| `31` | Floating | Light Vessel / LANBY / Rigs (or ODAS buoy) |

---

### Table A.30: Message 23 Group Assignment Station Type (`0–15`) & Reporting Interval (`0–11`) Codes

| `station_type` (`bits 110..113`) | Target Station Group | `interval_raw` (`bits 146..149`) | Assigned Reporting Interval |
|---:|---|---:|---|
| `0` | All types of mobiles (default) | `0` | Autonomous mode (revert to Table 15.2) |
| `1` | Reserved for future use | `1` | $10\text{ minutes}$ ($600\text{ s}$) |
| `2` | All types of Class B mobile stations | `2` | $6\text{ minutes}$ ($360\text{ s}$) |
| `3` | SAR airborne mobile station | `3` | $3\text{ minutes}$ ($180\text{ s}$) |
| `4` | Aid to Navigation station | `4` | $1\text{ minute}$ ($60\text{ s}$) |
| `5` | Class B "CS" shipborne mobile station only | `5` | $30\text{ seconds}$ |
| `6` | Inland waterways (regional use) | `6` | $15\text{ seconds}$ |
| `7–9` | Regional use | `7` | $10\text{ seconds}$ |
| `10–15` | Reserved for future use | `8` | $5\text{ seconds}$ |
| | | `9` | $2\text{ seconds}$ (Not applicable to Class B "CS") |
| | | `10` | Next shorter reporting interval (or $5\text{ s}$ for Class B "CS") |
| | | `11` | Next longer reporting interval |
| | | `12–15` | Reserved for future use |
