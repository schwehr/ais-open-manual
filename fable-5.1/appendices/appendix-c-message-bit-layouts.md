# Appendix C — Message bit-layout reference

This appendix provides the definitive bit-level specification for the maritime VHF Data Link (VDL) message catalog, spanning Messages 1 through 27 as codified in Recommendation ITU-R M.1371-5 and updated in ITU-R M.1371-6. It also details the compact single-slot Aid to Navigation report (Message 28) introduced in Recommendation ITU-R M.1371-6. For architectural and operational discussions of these message structures, see [Chapter 20](../chapters/ch20-architecture-and-station-classes.md) (station classes), [Chapter 21](../chapters/ch21-link-layer-tdma.md) (link layer and slot framing), [Chapter 22](../chapters/ch22-message-catalog.md) (message semantics), [Chapter 23](../chapters/ch23-asm-binary-payloads.md) (application-specific messages), [Chapter 26](../chapters/ch26-interfaces-and-logging.md) (NMEA 0183 encapsulation), [Chapter 44](../chapters/ch44-open-source-decoders-history.md) (open-source decoders), and [Chapter 68](../chapters/ch68-special-purpose-ais.md) (AtoN, SART, and MOB devices). Code lookup tables (navigational status, ship and cargo types, EPFD types, and AtoN classifications) are cross-referenced in [Appendix D](../appendices/appendix-d-code-tables.md).

---

## 1. Global framing conventions and standard headers

Every packet broadcast across the AIS VHF data link is transmitted most significant bit (MSB) first in network byte order. Unless specified otherwise:
- **Geographic Coordinates:** Project onto the WGS 84 ellipsoid. Standard resolution positions (Messages 1–4, 9, 11, 18, 19, 21, and 28) encode latitude and longitude as two's complement signed integers in units of $1/10{,}000$ of a minute ($1/600{,}000$ degree, $\approx 0.185\text{ m}$ meridional resolution). Low-resolution coordinates (Messages 17, 22, 23, 27, and binary area notices) encode coordinates in units of $1/10$ of a minute ($1/600$ degree, $\approx 185.2\text{ m}$).
- **Signed Numbers:** Encoded using standard two's complement representation across the exact bit width of the designated field.
- **6-bit ASCII Text:** Character strings (vessel names, call signs, destinations, and safety-related text) are encoded using the ITU 6-bit uppercase ASCII alphabet (ITU-R M.1371 Table 45). Trailing unused characters are filled with the sentinel padding character `@` (binary `000000`, 6-bit decimal `0`).
- **Common Header:** Every VDL message begins with a 38-bit standard preamble header:
  - `Message ID` (bits 0–5, 6 bits): Unsigned integer identifying message format (1–28).
  - `Repeat Indicator` (bits 6–7, 2 bits): Broadcast repeat counter (0 = default; 1, 2, or 3 = relayed by repeater; 3 = do not repeat any more). In Message 27, this field is permanently set to 3.
  - `Source MMSI` (bits 8–37, 30 bits): Maritime Mobile Service Identity of the transmitting station, formatted per Recommendation ITU-R M.585.

---

## 2. VDL message summary table (Messages 1–28)

The table below summarizes the operational attributes of Messages 1 through 28, listing transmitter station classes, typical slot budgets, channel access schemes, and transmission priorities.

| ID | Name / Description | Default Station Class | Slot Count | Access Scheme | Priority | ITU-R M.1371-6 Ref. |
|:---:|:---|:---|:---:|:---:|:---:|:---|
| 1 | Position report (scheduled) | Class A mobile | 1 | SOTDMA | 1 | Annex 7, §3.1, Table 46 |
| 2 | Position report (assigned) | Class A mobile | 1 | SOTDMA | 1 | Annex 7, §3.1, Table 46 |
| 3 | Position report (interrogation response / ITDMA) | Class A mobile | 1 | ITDMA | 1 | Annex 7, §3.1, Table 46 |
| 4 | Base station report | AIS Base Station | 1 | SOTDMA / FATDMA | 1 | Annex 7, §3.2, Table 49 |
| 5 | Static and voyage-related data | Class A mobile | 2 | SOTDMA / ITDMA / RATDMA | 4 (3 for query) | Annex 7, §3.3, Table 50 |
| 6 | Addressed binary message (ABM) | Any station | 1–5 | SOTDMA / ITDMA / RATDMA | 4 | Annex 7, §3.4, Table 52 |
| 7 | Binary acknowledge (addressed) | Mobile / Base | 1 | SOTDMA / ITDMA / RATDMA | 1 | Annex 7, §3.5, Table 54 |
| 8 | Broadcast binary message (BBM) | Any station | 1–5 | SOTDMA / ITDMA / RATDMA | 4 | Annex 7, §3.6, Table 55 |
| 9 | Standard SAR aircraft position report | SAR Aircraft | 1 | SOTDMA / ITDMA | 1 | Annex 7, §3.7, Table 60 |
| 10 | UTC and date inquiry (addressed) | Any station | 1 | SOTDMA / ITDMA / RATDMA | 3 | Annex 7, §3.8, Table 61 |
| 11 | UTC and date response | Base Station | 1 | SOTDMA / ITDMA / RATDMA | 3 | Annex 7, §3.9, Table 62 |
| 12 | Addressed safety-related message | Any station | 1–5 | SOTDMA / ITDMA / RATDMA | 2 | Annex 7, §3.10, Table 63 |
| 13 | Safety-related acknowledge | Addressed rx | 1 | SOTDMA / ITDMA / RATDMA | 1 | Annex 7, §3.11, Table 64 |
| 14 | Broadcast safety-related message | Any station | 1–5 | SOTDMA / ITDMA / RATDMA | 2 | Annex 7, §3.12, Table 65 |
| 15 | Interrogation | Base / Mobile | 1 | SOTDMA / ITDMA / RATDMA | 3 | Annex 7, §3.13, Table 66 |
| 16 | Assigned mode command | Base Station | 1 | SOTDMA / FATDMA | 1 | Annex 7, §3.14, Table 67 |
| 17 | DGNSS broadcast binary message | Base Station | 1–5 | SOTDMA / FATDMA | 2 | Annex 7, §3.15, Table 68 |
| 18 | Standard Class B position report | Class B mobile | 1 | SOTDMA / CSTDMA | 1 | Annex 7, §3.16, Table 69 |
| 19 | Extended Class B position report (deprecated) | Class B mobile | 2 | SOTDMA / CSTDMA | 1 | Annex 7, §3.17, Table 72 |
| 20 | Data link management message | Base Station | 1 | SOTDMA / FATDMA | 1 | Annex 7, §3.18, Table 73 |
| 21 | Aid to Navigation (AtoN) report | AtoN Station | 1–2 | FATDMA / RATDMA | 1 | Annex 7, §3.19, Table 74 |
| 22 | Channel management | Base / Mobile | 1 | SOTDMA / FATDMA | 1 | Annex 7, §3.20, Table 76 |
| 23 | Group assignment command | Base Station | 1 | SOTDMA / FATDMA | 1 | Annex 7, §3.21, Table 77 |
| 24 | Class B static data report (Parts A & B) | Class B / All | 1 per part | SOTDMA / CSTDMA | 4 | Annex 7, §3.22, Tables 79–81 |
| 25 | Single-slot binary message | Any station | 1 | RATDMA / ITDMA | 4 | Annex 7, §3.23, Tables 82–83 |
| 26 | Multi-slot binary message with comm-state | Any station | 1–5 | SOTDMA / ITDMA | 4 | Annex 7, §3.24, Tables 84–85 |
| 27 | Long-range AIS broadcast message | Class A / Class B | 1 | SOTDMA / RATDMA | 1 | Annex 7, §3.25, Table 86 |
| 28 | Single-slot Aid to Navigation report | AtoN Station | 1 | RATDMA / ITDMA / CSTDMA | 1 | Annex 7, §3.26, Tables 87–88 |

---

## 3. Bit-level layouts for Messages 1 through 27 and Message 28

### Messages 1, 2, and 3: Class A position report
- **Total length:** 168 bits (1 slot).
- **Applicability:** Message 1 = scheduled autonomous SOTDMA; Message 2 = assigned SOTDMA; Message 3 = ITDMA / interrogation response.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (1, 2, or 3) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | 9-digit MMSI decimal | N/A |
| Navigational Status | 38–41 | 4 | uint | 0–15; nav status code | 15 = undefined / default |
| Rate of Turn (ROT) | 42–49 | 8 | int | $\text{ROT}_{\text{AIS}} = 4.733 \sqrt{\text{ROT}_{\text{sensor}}}$ | $-128$ (`0x80`) = no turn information; $\pm 127 = >5^\circ/30\text{ s}$ without TI |
| Speed Over Ground (SOG) | 50–59 | 10 | uint | $0.1\text{ kn}$ ($0.0$–$102.2\text{ kn}$) | $1023$ (`0x3FF`) = not available; $1022 = \ge 102.2\text{ kn}$ |
| Position Accuracy (PA) | 60 | 1 | bool | $1 = \text{high } (\le 10\text{ m})$, $0 = \text{low } (> 10\text{ m})$ | 0 = low / default |
| Longitude | 61–88 | 28 | int | $1/10{,}000\text{ min}$ ($\pm 180^\circ$) | $181^\circ = 1810000\text{ min} = \text{0x6791AC0}$ ($+181000000$ raw) |
| Latitude | 89–115 | 27 | int | $1/10{,}000\text{ min}$ ($\pm 90^\circ$) | $91^\circ = 910000\text{ min} = \text{0x3412140}$ ($+91000000$ raw) |
| Course Over Ground (COG) | 116–127 | 12 | uint | $0.1^\circ$ ($0.0^\circ$–$359.9^\circ$) | 3600 (`0xE10`) = not available; 3601–4095 should not be used |
| True Heading (HDG) | 128–136 | 9 | uint | Degrees ($0^\circ$–$359^\circ$) | 511 (`0x1FF`) = not available; 360–510 should not be used |
| Time Stamp | 137–142 | 6 | uint | UTC second of fix ($0$–$59$) | 60 = not available (default); 61 = manual; 62 = DR; 63 = error |
| Special Manoeuvre | 143–144 | 2 | uint | Regional manoeuvre status | 0 = not available (default); 1 = not engaged; 2 = engaged |
| Spare | 145–147 | 3 | uint | Reserved bits | 0 |
| RAIM Flag | 148 | 1 | bool | RAIM integrity monitoring | 0 = RAIM not in use (default); 1 = in use |
| Communication State | 149–167 | 19 | uint | SOTDMA (Msg 1/2) or ITDMA (Msg 3) | Sync state, slot timeout, and submessage / slot offset |

---

### Message 4: Base station report and Message 11: UTC / position response
- **Total length:** 168 bits (1 slot).
- **Applicability:** Message 4 = autonomous base station transmission; Message 11 = UTC response to Message 10 polling.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (4 or 11) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | 9-digit base station MMSI ($00\text{MID}XXXX$) | N/A |
| UTC Year | 38–51 | 14 | uint | Year ($1$–$9999\text{ AD}$) | 0 = not available |
| UTC Month | 52–55 | 4 | uint | Month ($1$–$12$) | 0 = not available |
| UTC Day | 56–60 | 5 | uint | Day ($1$–$31$) | 0 = not available |
| UTC Hour | 61–65 | 5 | uint | Hour ($0$–$23$) | 24 = not available |
| UTC Minute | 66–71 | 6 | uint | Minute ($0$–$59$) | 60 = not available |
| UTC Second | 72–77 | 6 | uint | Second ($0$–$59$) | 60 = not available |
| Position Accuracy (PA) | 78 | 1 | bool | $1 = \text{high } (\le 10\text{ m})$, $0 = \text{low}$ | 0 = default |
| Longitude | 79–106 | 28 | int | $1/10{,}000\text{ min}$ ($\pm 180^\circ$) | 181° (`0x6791AC0`) = not available |
| Latitude | 107–133 | 27 | int | $1/10{,}000\text{ min}$ ($\pm 90^\circ$) | 91° (`0x3412140`) = not available |
| EPFD Type | 134–137 | 4 | uint | Position sensor type (Table 49) | 0 = undefined (default) |
| Transmission Control (Msg 4) / Spare (Msg 11) | 138 | 1 | uint | In Msg 4: Msg 27 control; in Msg 11: spare | In Msg 4: 0 = stop Msg 27, 1 = request Msg 27; Msg 11: 0 |
| Spare | 139–147 | 9 | uint | Reserved bits | 0 |
| RAIM Flag | 148 | 1 | bool | RAIM monitoring | 0 = not in use (default); 1 = in use |
| Communication State | 149–167 | 19 | uint | SOTDMA comm-state | Sync state (bits 149–150), timeout (151–153), submessage (154–167) |

---

### Message 5: Class A static and voyage-related data
- **Total length:** 424 bits (2 slots).
- **Applicability:** Shipborne Class A mobile transponders (broadcast every 6 minutes or on demand).

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (5) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | 9-digit MMSI decimal | N/A |
| AIS Version Indicator | 38–39 | 2 | uint | Station capability edition | 0 = M.1371-1; 1 = M.1371-3; 2 = M.1371-5; 3 = M.1371-6+ |
| IMO Number | 40–69 | 30 | uint | 7-digit IMO ship identification | 0 = not available / not applicable |
| Call Sign | 70–111 | 42 | text | $7 \times 6\text{-bit}$ ASCII characters | `@@@@@@@` = not available; padded with `@` |
| Vessel Name | 112–231 | 120 | text | $20 \times 6\text{-bit}$ ASCII characters | `@@...@@` = not available; padded with `@` |
| Ship and Cargo Type | 232–239 | 8 | uint | Numerical classification code | 0 = not available / default; 1–99 standard |
| Dimension to Bow (A) | 240–248 | 9 | uint | Distance in metres ($0$–$511\text{ m}$) | 0 = not available; 511 = 511 m or greater |
| Dimension to Stern (B) | 249–257 | 9 | uint | Distance in metres ($0$–$511\text{ m}$) | 0 = not available; 511 = 511 m or greater |
| Dimension to Port (C) | 258–263 | 6 | uint | Distance in metres ($0$–$63\text{ m}$) | 0 = not available; 63 = 63 m or greater |
| Dimension to Starboard (D) | 264–269 | 6 | uint | Distance in metres ($0$–$63\text{ m}$) | 0 = not available; 63 = 63 m or greater |
| EPFD Type | 270–273 | 4 | uint | Electronic Position Fixing Device | 0 = undefined / default; 1 = GPS; 2 = GLONASS; etc. |
| ETA Month | 274–277 | 4 | uint | UTC month ($1$–$12$) | 0 = not available |
| ETA Day | 278–282 | 5 | uint | UTC day ($1$–$31$) | 0 = not available |
| ETA Hour | 283–287 | 5 | uint | UTC hour ($0$–$23$) | 24 = not available |
| ETA Minute | 288–293 | 6 | uint | UTC minute ($0$–$59$) | 60 = not available |
| Maximum Static Draught | 294–301 | 8 | uint | $1/10\text{ metre}$ ($0.1$–$25.5\text{ m}$) | 0 = not available; 255 = 25.5 m or greater |
| Destination | 302–421 | 120 | text | $20 \times 6\text{-bit}$ ASCII characters | `@@...@@` = not available; UN/LOCODE recommended |
| DTE Flag | 422 | 1 | bool | Data Terminal Equipment ready | 0 = data terminal ready; 1 = not ready (default) |
| Spare | 423 | 1 | uint | Reserved bit | 0 |

---

### Message 6: Addressed binary message (ABM)
- **Total length:** 88 to 1,008 bits (1 to 5 slots).
- **Slot capacities:** 1 slot $\le 8\text{ bytes}$ application data; 2 slots $\le 36\text{ B}$; 3 slots $\le 64\text{ B}$; 4 slots $\le 92\text{ B}$; 5 slots $\le 117\text{ B}$.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (6) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | Transmitting station MMSI | N/A |
| Sequence Number | 38–39 | 2 | uint | 0–3 sequence number | For acknowledgment matching |
| Destination MMSI | 40–69 | 30 | uint | Target station MMSI | Recipient address |
| Retransmit Flag | 70 | 1 | bool | Retransmission indicator | 0 = original transmission; 1 = retransmitted |
| Spare | 71 | 1 | uint | Reserved bit | 0 |
| Designated Area Code (DAC) | 72–81 | 10 | uint | Country / regional authority ID | 1 = International (IMO); regional codes per ITU MID |
| Function Identifier (FI) | 82–87 | 6 | uint | Specific sub-message identifier | 0–63 sub-message format |
| Application Binary Data | 88–varies | $\le 920$ | bits | Application-specific data payload | Up to 920 bits ($\le 1{,}008$ total message bits) |

---

### Message 7 and Message 13: Acknowledgment messages
- **Total length:** 72, 104, 136, or 168 bits (1 slot). Message 7 acknowledges Message 6; Message 13 acknowledges Message 12.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (7 or 13) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | Acknowledging station MMSI | N/A |
| Spare | 38–39 | 2 | uint | Reserved bits | 0 |
| Destination MMSI 1 | 40–69 | 30 | uint | First target MMSI | N/A |
| Sequence Number 1 | 70–71 | 2 | uint | First acknowledged seqno (0–3) | Matches sequence number in Msg 6/12 |
| Destination MMSI 2 (optional) | 72–101 | 30 | uint | Second target MMSI | Omitted if acknowledging 1 packet |
| Sequence Number 2 (optional) | 102–103 | 2 | uint | Second acknowledged seqno | Omitted if acknowledging 1 packet |
| Destination MMSI 3 (optional) | 104–133 | 30 | uint | Third target MMSI | Omitted if acknowledging $\le 2$ packets |
| Sequence Number 3 (optional) | 134–135 | 2 | uint | Third acknowledged seqno | Omitted if acknowledging $\le 2$ packets |
| Destination MMSI 4 (optional) | 136–165 | 30 | uint | Fourth target MMSI | Omitted if acknowledging $\le 3$ packets |
| Sequence Number 4 (optional) | 166–167 | 2 | uint | Fourth acknowledged seqno | Omitted if acknowledging $\le 3$ packets |

---

### Message 8: Broadcast binary message (BBM)
- **Total length:** 56 to 1,008 bits (1 to 5 slots).
- **Slot capacities:** 1 slot $\le 12\text{ bytes}$ data; 2 slots $\le 40\text{ B}$; 3 slots $\le 68\text{ B}$; 4 slots $\le 96\text{ B}$; 5 slots $\le 121\text{ B}$.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (8) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | Transmitting station MMSI | N/A |
| Spare | 38–39 | 2 | uint | Reserved bits | 0 |
| Designated Area Code (DAC) | 40–49 | 10 | uint | Authority code | 1 = International (IMO SN.1/Circ.289) |
| Function Identifier (FI) | 50–55 | 6 | uint | Sub-message format (0–63) | e.g., FI 31 = Met/Hydro; FI 22 = Area Notice |
| Application Binary Data | 56–varies | $\le 952$ | bits | Application payload | Up to 952 bits ($\le 1{,}008$ total bits) |

---

### Message 9: Standard SAR aircraft position report
- **Total length:** 168 bits (1 slot).

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (9) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | SAR aircraft MMSI ($111\text{MID}XXX$) | N/A |
| Altitude | 38–49 | 12 | uint | Metres above sea level ($0$–$4094\text{ m}$) | 4095 = not available; 4094 = 4094 m or higher |
| Speed Over Ground (SOG) | 50–59 | 10 | uint | Whole knots ($0$–$1022\text{ kn}$) | 1023 = not available; 1022 = 1022 kn or higher |
| Position Accuracy (PA) | 60 | 1 | bool | $1 = \text{high } (\le 10\text{ m})$, $0 = \text{low}$ | 0 = default |
| Longitude | 61–88 | 28 | int | $1/10{,}000\text{ min}$ ($\pm 180^\circ$) | 181° (`0x6791AC0`) = not available |
| Latitude | 89–115 | 27 | int | $1/10{,}000\text{ min}$ ($\pm 90^\circ$) | 91° (`0x3412140`) = not available |
| Course Over Ground (COG) | 116–127 | 12 | uint | $0.1^\circ$ ($0.0^\circ$–$359.9^\circ$) | 3600 (`0xE10`) = not available |
| Time Stamp | 128–133 | 6 | uint | UTC second ($0$–$59$) | 60 = not available (default) |
| Altitude Sensor | 134 | 1 | bool | Altitude source sensor | 0 = GNSS altitude; 1 = barometric sensor  |
| Spare / Regional | 135–141 | 7 | uint | Reserved bits | 0 |
| DTE Flag | 142 | 1 | bool | Data Terminal Equipment | 0 = ready; 1 = not ready (default) |
| Spare | 143–145 | 3 | uint | Reserved bits | 0 |
| Assigned-Mode Flag | 146 | 1 | bool | Station operating mode | 0 = autonomous; 1 = assigned |
| RAIM Flag | 147 | 1 | bool | RAIM monitoring | 0 = not in use (default); 1 = in use |
| Communication State Selector | 148 | 1 | bool | Comm-state selector | 0 = SOTDMA; 1 = ITDMA |
| Communication State | 149–167 | 19 | uint | Comm-state bits | Sync state, timeout, submessage |

---

### Message 10: UTC and date inquiry
- **Total length:** 72 bits (1 slot).

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (10) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | Inquiring station MMSI | N/A |
| Spare | 38–39 | 2 | uint | Reserved bits | 0 |
| Destination MMSI | 40–69 | 30 | uint | Destination base station MMSI | Target station |
| Spare | 70–71 | 2 | uint | Reserved bits | 0 |

---

### Messages 12 and 14: Safety-related text messages
- **Total length:** Message 12 = 72 to 1,008 bits; Message 14 = 40 to 1,008 bits.
- **Payload:** 6-bit ASCII text string. Message 12 is addressed; Message 14 is broadcast.

| Field Name (Msg 12) | Bits (12) | Field Name (Msg 14) | Bits (14) | Width | Type | Sentinel / Notes |
|:---|:---:|:---|:---:|:---:|:---:|:---|
| Message ID | 0–5 | Message ID | 0–5 | 6 | uint | 12 (addressed) or 14 (broadcast) |
| Repeat Indicator | 6–7 | Repeat Indicator | 6–7 | 2 | uint | 0–3; 0 = default |
| Source MMSI | 8–37 | Source MMSI | 8–37 | 30 | uint | Transmitting station MMSI |
| Sequence Number | 38–39 | — | — | 2 | uint | 0–3 sequence number (Msg 12 only) |
| Destination MMSI | 40–69 | — | — | 30 | uint | Target station MMSI (Msg 12 only) |
| Retransmit Flag | 70 | — | — | 1 | bool | 0 = original, 1 = retransmitted (Msg 12) |
| Spare | 71 | Spare | 38–39 | 1 or 2 | uint | Reserved bits (0) |
| Safety Text | 72–varies | Safety Text | 40–varies | $\le 936$ / $\le 968$ | text | 6-bit ASCII text; trailing padded `@` |

---

### Message 15: Interrogation
- **Total length:** 88, 110, 160, or 162 bits (1 slot). Queries up to two interrogatee stations for up to three specific message types.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (15) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | Interrogating station MMSI | N/A |
| Spare | 38–39 | 2 | uint | Reserved bits | 0 |
| Interrogated MMSI 1 | 40–69 | 30 | uint | First target MMSI | Station to respond |
| Requested Message 1.1 | 70–75 | 6 | uint | First requested message ID | Message type requested (e.g. 3, 5) |
| Slot Offset 1.1 | 76–87 | 12 | uint | Response slot offset ($0$–$4095$) | 0 = use autonomous selection |
| Spare | 88–89 | 2 | uint | Reserved bits | 0 (omitted if message terminates here) |
| Requested Message 1.2 | 90–95 | 6 | uint | Second requested message ID | Optional second message request |
| Slot Offset 1.2 | 96–107 | 12 | uint | Response slot offset ($0$–$4095$) | 0 = autonomous selection |
| Spare | 108–109 | 2 | uint | Reserved bits | 0 |
| Interrogated MMSI 2 | 110–139 | 30 | uint | Second target MMSI | Optional second target |
| Requested Message 2.1 | 140–145 | 6 | uint | Message ID for station 2 | Message type requested |
| Slot Offset 2.1 | 146–157 | 12 | uint | Response slot offset ($0$–$4095$) | 0 = autonomous selection |
| Spare | 158–159 | 2 | uint | Reserved bits | 0 |

---

### Message 16: Assigned mode command
- **Total length:** 96 bits (1 station) or 144 bits (2 stations). Transmitted by base stations to assign reporting rates and slot reservations.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (16) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | Assigning base station MMSI | N/A |
| Spare | 38–39 | 2 | uint | Reserved bits | 0 |
| Target MMSI A | 40–69 | 30 | uint | Assigned mobile station A | N/A |
| Slot Offset A | 70–81 | 12 | uint | First assigned slot offset | $0$–$4095$ TDMA slot offset |
| Increment A | 82–91 | 10 | uint | Slot allocation increment | $0$ = 1 burst; $>0$ = repetition rate |
| Target MMSI B (optional) | 92–121 | 30 | uint | Assigned mobile station B | Omitted in 96-bit 1-station assignment |
| Slot Offset B (optional) | 122–133 | 12 | uint | Second assigned slot offset | $0$–$4095$ TDMA slot offset |
| Increment B (optional) | 134–143 | 10 | uint | Second slot increment | Repetition interval for station B |
| Spare (1-station variant) | 92–95 | 4 | uint | Padding bits for 1 station | 0 (present only in 96-bit form) |

---

### Message 17: DGNSS broadcast binary message
- **Total length:** 80 to 816 bits (1 to 5 slots). Carries differential GNSS corrections formatted per RTCM 10402.x.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (17) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | DGNSS station MMSI ($00\text{MID}XXXX$) | N/A |
| Spare | 38–39 | 2 | uint | Reserved bits | 0 |
| Reference Longitude | 40–57 | 18 | int | Signed $1/10\text{ min}$ ($\pm 180^\circ$) | 181° (`0x1A838`) = not available |
| Reference Latitude | 58–74 | 17 | int | Signed $1/10\text{ min}$ ($\pm 90^\circ$) | 91° (`0xD548`) = not available |
| Spare | 75–79 | 5 | uint | Reserved bits | 0 |
| Differential Correction Data | 80–varies | $\le 736$ | bits | RTCM SC-104 correction records | N/A |

---

### Message 18: Standard Class B unit position report
- **Total length:** 168 bits (1 slot). Broadcast by Class B SOTDMA ("B+") and Class B CSTDMA ("CS") units.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (18) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | Class B mobile MMSI | N/A |
| Reserved / Regional | 38–45 | 8 | uint | Regional operating bits | 0 = default |
| Speed Over Ground (SOG) | 46–55 | 10 | uint | $0.1\text{ kn}$ ($0.0$–$102.2\text{ kn}$) | 1023 (`0x3FF`) = not available |
| Position Accuracy (PA) | 56 | 1 | bool | $1 = \text{high } (\le 10\text{ m})$, $0 = \text{low}$ | 0 = default |
| Longitude | 57–84 | 28 | int | $1/10{,}000\text{ min}$ ($\pm 180^\circ$) | 181° (`0x6791AC0`) = not available |
| Latitude | 85–111 | 27 | int | $1/10{,}000\text{ min}$ ($\pm 90^\circ$) | 91° (`0x3412140`) = not available |
| Course Over Ground (COG) | 112–123 | 12 | uint | $0.1^\circ$ ($0.0^\circ$–$359.9^\circ$) | 3600 (`0xE10`) = not available |
| True Heading (HDG) | 124–132 | 9 | uint | Degrees ($0^\circ$–$359^\circ$) | 511 (`0x1FF`) = not available |
| Time Stamp | 133–138 | 6 | uint | UTC second of fix ($0$–$59$) | 60 = not available (default); 61–63 not used by CS |
| Regional / Reserved | 139–140 | 2 | uint | Regional bits | 0 |
| Class B Unit Flag | 141 | 1 | bool | Transceiver design architecture | 0 = Class B SOTDMA; 1 = Class B CS |
| Class B Display Flag | 142 | 1 | bool | Integrated screen capability | 0 = no display; 1 = display attached |
| Class B DSC Flag | 143 | 1 | bool | Integrated DSC capability | 0 = no DSC; 1 = DSC receiver present |
| Class B Band Flag | 144 | 1 | bool | Frequency agility capability | 0 = top 525 kHz only; 1 = entire marine VHF band |
| Class B Message 22 Flag | 145 | 1 | bool | Channel management support | 0 = no Msg 22 frequency shift; 1 = supported |
| Mode Flag | 146 | 1 | bool | Operational mode | 0 = autonomous mode; 1 = assigned mode |
| RAIM Flag | 147 | 1 | bool | RAIM monitoring | 0 = not in use (default); 1 = in use |
| Comm-State Selector | 148 | 1 | bool | SOTDMA vs ITDMA / CS flag | 0 = SOTDMA; 1 = ITDMA (always 1 for CS units) |
| Communication State | 149–167 | 19 | uint | Comm-state or fixed CS sentinel | In CS units: fixed pattern `1100000000000000110` (`0x60006`, 393222) |

---

### Message 19: Extended Class B equipment position report (deprecated)
- **Total length:** 312 bits (2 slots). Deprecated in ITU-R M.1371-6 (superseded by Messages 18 and 24A/24B).

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (19) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | Class B mobile MMSI | N/A |
| Regional / Reserved | 38–45 | 8 | uint | Regional bits | 0 |
| Speed Over Ground (SOG) | 46–55 | 10 | uint | $0.1\text{ kn}$ ($0.0$–$102.2\text{ kn}$) | 1023 (`0x3FF`) = not available |
| Position Accuracy (PA) | 56 | 1 | bool | $1 = \text{high}$, $0 = \text{low}$ | 0 = default |
| Longitude | 57–84 | 28 | int | $1/10{,}000\text{ min}$ ($\pm 180^\circ$) | 181° (`0x6791AC0`) = not available |
| Latitude | 85–111 | 27 | int | $1/10{,}000\text{ min}$ ($\pm 90^\circ$) | 91° (`0x3412140`) = not available |
| Course Over Ground (COG) | 112–123 | 12 | uint | $0.1^\circ$ ($0.0^\circ$–$359.9^\circ$) | 3600 (`0xE10`) = not available |
| True Heading (HDG) | 124–132 | 9 | uint | Degrees ($0^\circ$–$359^\circ$) | 511 (`0x1FF`) = not available |
| Time Stamp | 133–138 | 6 | uint | UTC second ($0$–$59$) | 60 = not available |
| Regional / Reserved | 139–142 | 4 | uint | Regional bits | 0 |
| Vessel Name | 143–262 | 120 | text | $20 \times 6\text{-bit}$ ASCII characters | Padded with `@` |
| Ship and Cargo Type | 263–270 | 8 | uint | Ship type code (0–99) | 0 = not available / default |
| Dimension to Bow (A) | 271–279 | 9 | uint | Metres ($0$–$511\text{ m}$) | 0 = not available |
| Dimension to Stern (B) | 280–288 | 9 | uint | Metres ($0$–$511\text{ m}$) | 0 = not available |
| Dimension to Port (C) | 289–294 | 6 | uint | Metres ($0$–$63\text{ m}$) | 0 = not available |
| Dimension to Starboard (D) | 295–300 | 6 | uint | Metres ($0$–$63\text{ m}$) | 0 = not available |
| EPFD Type | 301–304 | 4 | uint | Sensor type | 0 = undefined |
| RAIM Flag | 305 | 1 | bool | RAIM monitoring | 0 = not in use (default); 1 = in use |
| DTE Flag | 306 | 1 | bool | Data Terminal Equipment | 0 = ready; 1 = not ready (default) |
| Assigned-Mode Flag | 307 | 1 | bool | Station operating mode | 0 = autonomous; 1 = assigned |
| Spare | 308–311 | 4 | uint | Reserved bits | 0 |

---

### Message 20: Data link management message
- **Total length:** 72, 102, 132, or 160 bits (1 slot). Broadcast by base stations to pre-reserve FATDMA slots.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (20) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | Base station MMSI | N/A |
| Spare | 38–39 | 2 | uint | Reserved bits | 0 |
| Offset Number 1 | 40–51 | 12 | uint | Slot offset to first reserved slot | $0$–$4095$ TDMA slots |
| Reserved Slots 1 | 52–55 | 4 | uint | Number of consecutive slots ($1$–$15$) | $0 = \text{invalid}$ |
| Time-out 1 | 56–58 | 3 | uint | Allocation validity timeout | $0$–$7$ frames ($0 = \text{last frame}$) |
| Increment 1 | 59–69 | 11 | uint | Slot repeat increment | $0$ = single allocation; $>0$ = recurrence interval |
| Block 2 (Offset, Num, Timeout, Inc) | 70–99 | 30 | — | Second reservation block | Optional; identical 30-bit structure |
| Block 3 (Offset, Num, Timeout, Inc) | 100–129 | 30 | — | Third reservation block | Optional; identical 30-bit structure |
| Block 4 (Offset, Num, Timeout, Inc) | 130–159 | 30 | — | Fourth reservation block | Optional; identical 30-bit structure |

---

### Message 21: Aid to Navigation (AtoN) report
- **Total length:** 272 to 360 bits (1 or 2 slots). Broadcast by physical, synthetic, or virtual Aids to Navigation.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (21) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | AtoN MMSI ($99\text{MID}XXXX$) | N/A |
| Aid Type | 38–42 | 5 | uint | AtoN type code ($0$–$31$, Table 72) | 0 = default / unspecified |
| AtoN Name | 43–162 | 120 | text | $20 \times 6\text{-bit}$ ASCII characters | Padded with `@` |
| Position Accuracy (PA) | 163 | 1 | bool | $1 = \text{high } (\le 10\text{ m})$, $0 = \text{low}$ | 0 = default |
| Longitude | 164–191 | 28 | int | $1/10{,}000\text{ min}$ ($\pm 180^\circ$) | 181° (`0x6791AC0`) = not available |
| Latitude | 192–218 | 27 | int | $1/10{,}000\text{ min}$ ($\pm 90^\circ$) | 91° (`0x3412140`) = not available |
| Dimension to Bow (A) | 219–227 | 9 | uint | Metres ($0$–$511\text{ m}$) | For fixed/virtual: points North; 0 = n/a |
| Dimension to Stern (B) | 228–236 | 9 | uint | Metres ($0$–$511\text{ m}$) | 0 = not available |
| Dimension to Port (C) | 237–242 | 6 | uint | Metres ($0$–$63\text{ m}$) | 0 = not available |
| Dimension to Starboard (D) | 243–248 | 6 | uint | Metres ($0$–$63\text{ m}$) | 0 = not available |
| EPFD Type | 249–252 | 4 | uint | Positioning device type | 0 = undefined; 7 = surveyed |
| Time Stamp | 253–258 | 6 | uint | UTC second ($0$–$59$) | 60 = not available (default) |
| Off-Position Indicator | 259 | 1 | bool | On/off station status | 0 = on position; 1 = off position (or fixed GNSS anomaly) |
| AtoN Status (Regional) | 260–267 | 8 | uint | IALA R0126 status bits | Light failure, RACON error, battery low, etc. |
| RAIM Flag | 268 | 1 | bool | RAIM monitoring | 0 = not in use (default); 1 = in use |
| Virtual AtoN Flag | 269 | 1 | bool | Real vs. Virtual aid | 0 = real physical AtoN; 1 = virtual AtoN |
| Assigned-Mode Flag | 270 | 1 | bool | Operational mode | 0 = autonomous; 1 = assigned |
| Spare | 271 | 1 | uint | Reserved bit | 0 |
| Name Extension | 272–varies | $\le 84$ | text | $0$–$14 \times 6\text{-bit}$ ASCII characters | Optional; `@@@` prefix indicates display as chart label |
| Spare (Padding) | varies | 0/2/4/6 | uint | Byte alignment padding | 0 |

---

### Message 22: Channel management
- **Total length:** 168 bits (1 slot). Broadcast by base stations or mobile stations to control RF frequencies and power.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (22) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | Commanding station MMSI | N/A |
| Spare | 38–39 | 2 | uint | Reserved bits | 0 |
| Channel A | 40–51 | 12 | uint | ITU VHF channel number (e.g. 2087) | Primary assigned channel |
| Channel B | 52–63 | 12 | uint | ITU VHF channel number (e.g. 2088) | Secondary assigned channel |
| Tx/Rx Mode | 64–67 | 4 | uint | 0 = TxA/TxB, RxA/RxB; 1 = TxA; etc. | Operating transceive configuration |
| Power | 68 | 1 | bool | RF output power | 0 = high power ($12.5\text{ W}$); 1 = low power ($1\text{ W}$) |
| Geographic Area / MMSI (bits 69–138) | 69–138 | 70 | — | Broadcast Area vs. Addressed Stations | Addressed flag (bit 139) determines mapping: |
| — NE Longitude (Broadcast) | 69–86 | 18 | int | Signed $1/10\text{ min}$ NE corner | Used if addressed flag = 0 |
| — NE Latitude (Broadcast) | 87–103 | 17 | int | Signed $1/10\text{ min}$ NE corner | Used if addressed flag = 0 |
| — SW Longitude (Broadcast) | 104–121 | 18 | int | Signed $1/10\text{ min}$ SW corner | Used if addressed flag = 0 |
| — SW Latitude (Broadcast) | 122–138 | 17 | int | Signed $1/10\text{ min}$ SW corner | Used if addressed flag = 0 |
| — Addressed Destination 1 | 69–98 | 30 | uint | Target MMSI 1 | Used if addressed flag = 1; bits 99–103 spare |
| — Addressed Destination 2 | 104–133 | 30 | uint | Target MMSI 2 | Used if addressed flag = 1; bits 134–138 spare |
| Addressed Flag | 139 | 1 | bool | Addressing mode | 0 = broadcast regional area; 1 = addressed to MMSI 1 & 2 |
| Channel A Bandwidth | 140 | 1 | bool | Channel A bandwidth | 0 = default ($25\text{ kHz}$); 1 = narrow ($12.5\text{ kHz}$) |
| Channel B Bandwidth | 141 | 1 | bool | Channel B bandwidth | 0 = default ($25\text{ kHz}$); 1 = narrow ($12.5\text{ kHz}$) |
| Transitional Zone Size | 142–144 | 3 | uint | Buffer zone size in nautical miles | $1$–$8\text{ nmi}$ transition boundary width |
| Spare | 145–167 | 23 | uint | Reserved bits | 0 |

---

### Message 23: Group assignment command
- **Total length:** 160 bits (1 slot). Controls operating parameters for a designated subset of mobile stations.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (23) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | Commanding base station MMSI | N/A |
| Spare | 38–39 | 2 | uint | Reserved bits | 0 |
| NE Longitude | 40–57 | 18 | int | Signed $1/10\text{ min}$ NE corner | $181^\circ = \text{0x1A838}$ = not available |
| NE Latitude | 58–74 | 17 | int | Signed $1/10\text{ min}$ NE corner | $91^\circ = \text{0xD548}$ = not available |
| SW Longitude | 75–92 | 18 | int | Signed $1/10\text{ min}$ SW corner | $181^\circ = \text{0x1A838}$ = not available |
| SW Latitude | 93–109 | 17 | int | Signed $1/10\text{ min}$ SW corner | $91^\circ = \text{0xD548}$ = not available |
| Station Type | 110–113 | 4 | uint | Target station category | 0 = all; 1 = Class A; 2 = Class B; 6 = inland; etc. |
| Ship and Cargo Type | 114–121 | 8 | uint | Target ship/cargo type | 0 = all types; 1–99 match specific categories |
| Spare | 122–143 | 22 | uint | Reserved bits | 0 |
| Tx/Rx Mode | 144–145 | 2 | uint | 0 = TxA/TxB; 1 = TxA; 2 = TxB | Transceiver mode assignment |
| Reporting Interval | 146–149 | 4 | uint | Commanded update cadence code | 0 = default; 1 = 2 s; 2 = 10 s; 9 = next shorter; etc. |
| Quiet Time | 150–153 | 4 | uint | Commanded silent period | 0 = none; $1$–$15\text{ minutes}$ silence command |
| Spare | 154–159 | 6 | uint | Reserved bits | 0 |

---

### Message 24: Class B static data report (Parts A and B)
- **Total length:** Part A = 160 bits; Part B = 168 bits. Each part fits within 1 slot.
- **Part A:** Broadcasts vessel name.
- **Part B:** Broadcasts vessel dimensions, call sign, ship type, and equipment vendor identifiers.

| Field Name (Part A) | Bits (A) | Field Name (Part B) | Bits (B) | Width | Type | Sentinel / Notes |
|:---|:---:|:---|:---:|:---:|:---:|:---|
| Message ID | 0–5 | Message ID | 0–5 | 6 | uint | 24 |
| Repeat Indicator | 6–7 | Repeat Indicator | 6–7 | 2 | uint | 0–3; 0 = default |
| Source MMSI | 8–37 | Source MMSI | 8–37 | 30 | uint | Transmitting station MMSI |
| Part Number | 38–39 | Part Number | 38–39 | 2 | uint | 0 = Part A; 1 = Part B |
| Vessel Name | 40–159 | — | — | 120 | text | $20 \times 6\text{-bit}$ ASCII characters (padded with `@`) |
| Spare | 160–167 | — | — | 8 | uint | Reserved bits (0) |
| — | — | Ship and Cargo Type | 40–47 | 8 | uint | 0 = not available; 1–99 per Table 51 |
| — | — | Vendor ID (Mnemonic) | 48–65 | 18 | text | $3 \times 6\text{-bit}$ manufacturer mnemonic code |
| — | — | Unit Model Code | 66–69 | 4 | uint | Manufacturer model number ($0$–$15$) |
| — | — | Unit Serial Number | 70–89 | 20 | uint | Manufacturer serial number ($0$–$1{,}048{,}575$) |
| — | — | Call Sign | 90–131 | 42 | text | $7 \times 6\text{-bit}$ ASCII characters (padded with `@`) |
| — | — | Dimension to Bow (A) | 132–140 | 9 | uint | Metres ($0$–$511\text{ m}$); 0 = not available |
| — | — | Dimension to Stern (B) | 141–149 | 9 | uint | Metres ($0$–$511\text{ m}$); 0 = not available |
| — | — | Dimension to Port (C) | 150–155 | 6 | uint | Metres ($0$–$63\text{ m}$); 0 = not available |
| — | — | Dimension to Starboard (D)| 156–161 | 6 | uint | Metres ($0$–$63\text{ m}$); 0 = not available |
| — | — | Mothership MMSI (Auxiliary)| (132–161)| (30) | uint | Used only by daughter craft ($98\text{MID}XXXX$) |
| — | — | EPFD Type | 162–165 | 4 | uint | 0 = undefined; 1 = GPS; 2 = GLONASS; etc. |
| — | — | VDES Capabilities / Spare| 166–167 | 2 | uint | M.1371-6: 0 = AIS only; 1 = ASM; 2 = VDE-TER; 3 = VDE-SAT |

---

### Message 25: Single-slot binary message
- **Total length:** 40 to 168 bits (exactly 1 slot). Designed for short, unacknowledged burst telemetry.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (25) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | Transmitting station MMSI | N/A |
| Destination Indicator | 38 | 1 | bool | Addressing mode | 0 = broadcast; 1 = addressed to MMSI |
| Binary Data Flag | 39 | 1 | bool | Structuring mode | 0 = unstructured binary; 1 = structured (with DAC/FI) |
| Destination MMSI | 40–69 | 30 | uint | Target station MMSI | Present only when Destination Indicator = 1 |
| Designated Area Code (DAC) | varies | 10 | uint | Authority code | Present only when Binary Data Flag = 1 |
| Function Identifier (FI) | varies | 6 | uint | Sub-message format | Present only when Binary Data Flag = 1 |
| Binary Data Payload | varies | varies | bits | Application payload | Max 128 bits (broadcast unstructured); max 80 bits (addressed structured) |

---

### Message 26: Multi-slot binary message with communication state
- **Total length:** 60 to 1,064 bits (1 to 5 slots). Carries SOTDMA or ITDMA comm-state for scheduled multi-slot transfers.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (26) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | Transmitting station MMSI | N/A |
| Destination Indicator | 38 | 1 | bool | Addressing mode | 0 = broadcast; 1 = addressed to MMSI |
| Binary Data Flag | 39 | 1 | bool | Structuring mode | 0 = unstructured binary; 1 = structured (with DAC/FI) |
| Destination MMSI | 40–69 | 30 | uint | Target station MMSI | Present only when Destination Indicator = 1 |
| Designated Area Code (DAC) | varies | 10 | uint | Authority code | Present only when Binary Data Flag = 1 |
| Function Identifier (FI) | varies | 6 | uint | Sub-message format | Present only when Binary Data Flag = 1 |
| Binary Data Payload | varies | varies | bits | Application payload | Up to 1,004 bits (broadcast unstructured over 5 slots) |
| Comm-State Selector | end $-20$ | 1 | bool | SOTDMA vs ITDMA | 0 = SOTDMA; 1 = ITDMA |
| Communication State | end $-19$..end | 19 | uint | Comm-state bits | Sync state, slot timeout, and slot increment |

---

### Message 27: Long-range automatic identification broadcast
- **Total length:** 96 bits (1 slot). Optimized for satellite detection and long-range receiver decoding outside coastal VHF coverage.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (27) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | Always 3 (`11` binary) | Set to 3 by transmitter to prohibit terrestrial repeater relay |
| Source MMSI | 8–37 | 30 | uint | Mobile station MMSI | N/A |
| Position Accuracy (PA) | 38 | 1 | bool | $1 = \text{high } (\le 10\text{ m})$, $0 = \text{low}$ | 0 = default |
| RAIM Flag | 39 | 1 | bool | RAIM monitoring | 0 = not in use (default); 1 = in use |
| Navigational Status | 40–43 | 4 | uint | Nav status code ($0$–$15$) | 15 = undefined / default |
| Longitude | 44–61 | 18 | int | Signed $1/10\text{ min}$ ($\pm 180^\circ$) | $181^\circ = 108600\text{ raw} = \text{0x1A838}$ = not available / older than 6 h |
| Latitude | 62–78 | 17 | int | Signed $1/10\text{ min}$ ($\pm 90^\circ$) | $91^\circ = 54600\text{ raw} = \text{0xD548}$ = not available / older than 6 h |
| Speed Over Ground (SOG) | 79–84 | 6 | uint | Whole knots ($0$–$62\text{ kn}$) | 63 (`0x3F`) = not available; 62 = 62 kn or higher |
| Course Over Ground (COG) | 85–93 | 9 | uint | Whole degrees ($0^\circ$–$359^\circ$) | 511 (`0x1FF`) = not available; 360–510 should not be used |
| Position Latency | 94 | 1 | bool | GNSS fix freshness | 0 = fix latency $< 5\text{ s}$; 1 = latency $\ge 5\text{ s}$ (default) |
| Spare | 95 | 1 | uint | Reserved bit | 0 |

---

### Message 28: Aid-to-Navigation report (single-slot message)
- **Total length:** 168 bits (1 slot). Standardized in Recommendation ITU-R M.1371-6 (Annex 7, §3.26) to provide a compact, single-slot replacement for Message 21.

| Field Name | Bit Range | Width | Type | Units / Encoding | Not-Available Sentinel / Notes |
|:---|:---:|:---:|:---:|:---|:---|
| Message ID | 0–5 | 6 | uint | Identifier (28) | N/A |
| Repeat Indicator | 6–7 | 2 | uint | 0–3 repeat count | 0 = default |
| Source MMSI | 8–37 | 30 | uint | AtoN station MMSI ($99\text{MID}XXXX$) | N/A |
| Time Stamp | 38–43 | 6 | uint | UTC second of fix ($0$–$59$) | 60 = not available (default) |
| Longitude | 44–71 | 28 | int | $1/10{,}000\text{ min}$ ($\pm 180^\circ$) | 181° (`0x6791AC0`) = not available |
| Latitude | 72–98 | 27 | int | $1/10{,}000\text{ min}$ ($\pm 90^\circ$) | 91° (`0x3412140`) = not available |
| Restricted Use Indicator | 99–100 | 2 | uint | Station access / usage rights | 0 = public; 1 = restricted; 2/3 = reserved |
| AIS AtoN Station Type | 101–103 | 3 | uint | Physical / virtual classification | 0 = physical floating; 1 = physical fixed; 4 = virtual; 5 = mobile |
| Types of AtoN | 104–110 | 7 | uint | Extended AtoN type ($0$–$127$) | 0 = default; 1–31 match Msg 21; 32–50 mobile AtoNs (ODAS, hazard) |
| IALA AtoN MRN | 111–127 | 17 | uint | Maritime Resource Name index | Index into IALA MRN URN registry (`urn:mrn:iala:aton:...`) |
| AtoN Dimensions Type | 128–131 | 4 | uint | Geometric structural profile | 0–13 dimension type (point, circle, vector, polygon, sector) |
| Dimension A | 132–140 | 9 | uint | First dimension parameter | Interpretation governed by Dimensions Type |
| Dimension B | 141–151 | 11 | uint | Second dimension parameter | Interpretation governed by Dimensions Type |
| Additional Data Flag | 152 | 1 | bool | Extended geometry flag | 0 = no additional data; 1 = additional geometry follows |
| Charted Status | 153 | 1 | bool | Nautical chart depiction | 0 = charted; 1 = unchartered |
| On-Station Status | 154–157 | 4 | uint | Positional operational status | 0 = on position; 1 = off position; 9 = unmarked hazard |
| AtoN Status Bits | 158–165 | 8 | uint | Operating health indicators | Light failure, power failure, racon status, etc. |
| Spare | 166 | 1 | uint | Reserved bit | 0 |
| Authentication Flag | 167 | 1 | bool | Digital signature status | 0 = unauthenticated; 1 = authenticated per IALA G1192 |

---

## 4. Worked hex decodes using pyais

This section walks through three verified end-to-end decodes using the `pyais` library (version 3.2.3) in the repository environment. Each example shows the raw NMEA 0183 encapsulation sentence, the recovered binary payload formatted as a hex dump, the exact bit-level slice boundaries, and the decoded fields.

### Worked Example 1: Class A position report (Message 1)
- **Raw NMEA Sentence:**
  ```text
  !AIVDM,1,1,,A,15RTgt0PAso;90TKcjM8h6g208CQ,0*4A
  ```
- **Hex Dump of 168-bit Payload:**
  ```text
  0000: 04 58 A4 BF C0 20 47 BD CB 24 09 1B AF 27 48 C0   .X... G..$...'H.
  0010: 6B C2 00 84 E1                                    k....
  ```
- **Field-by-Field Bit Decomposition:**

| Field Name | Bit Span | Width | Hex Value | Raw Decimal | Decoded Engineering Value |
|:---|:---:|:---:|:---:|:---:|:---|
| Message ID | 0–5 | 6 | `0x1` | 1 | Message 1 (Scheduled Class A position report) |
| Repeat Indicator | 6–7 | 2 | `0x0` | 0 | 0 (Original transmission, not repeated) |
| Source MMSI | 8–37 | 30 | `0x16292FF0` | 371798000 | MMSI 371798000 (Panama registered vessel) |
| Navigational Status | 38–41 | 4 | `0x0` | 0 | Under way using engine |
| Rate of Turn (ROT) | 42–49 | 8 | `0x81` | -127 | $-127$ (Turning left at $>5^\circ/30\text{ s}$ without TI) |
| Speed Over Ground (SOG) | 50–59 | 10 | `0x7B` | 123 | $12.3\text{ kn}$ |
| Position Accuracy (PA) | 60 | 1 | `0x1` | 1 | 1 (High accuracy, DGNSS / RAIM error $\le 10\text{ m}$) |
| Longitude | 61–88 | 28 | `0xB964812` | -74037230 | $-123.395383^\circ$ ($123^\circ 23.7230'\text{ W}$) |
| Latitude | 89–115 | 27 | `0x1BAF274` | 29028980 | $+48.381633^\circ$ ($48^\circ 22.8980'\text{ N}$) |
| Course Over Ground (COG) | 116–127 | 12 | `0x8C0` | 2240 | $224.0^\circ$ |
| True Heading (HDG) | 128–136 | 9 | `0xD7` | 215 | $215^\circ$ |
| Time Stamp | 137–142 | 6 | `0x21` | 33 | 33 seconds past the UTC minute |
| Special Manoeuvre | 143–144 | 2 | `0x0` | 0 | Not available / default |
| Spare | 145–147 | 3 | `0x0` | 0 | Reserved padding |
| RAIM Flag | 148 | 1 | `0x0` | 0 | RAIM not in use |
| Communication State | 149–167 | 19 | `0x84E1` | 34017 | Sync: 0 (UTC direct); Timeout: 2; Slot: 1249 |

- **pyais Python Verification Snippet:**
  ```python
  from pyais import decode

  msg = decode("!AIVDM,1,1,,A,15RTgt0PAso;90TKcjM8h6g208CQ,0*4A")
  print(msg)
  # Output:
  # MessageType1(msg_type=1, repeat=0, mmsi=371798000, status=<NavigationStatus.UnderWayUsingEngine: 0>,
  #              turn=<TurnRate.NO_TI_LEFT: -127.0>, speed=12.3, accuracy=True,
  #              lon=-123.395383, lat=48.381633, course=224.0, heading=215, second=33,
  #              maneuver=<ManeuverIndicator.NotAvailable: 0>, spare_1=b'\x00', raim=False, radio=34017)
  ```

---

### Worked Example 2: Class A static and voyage data (Message 5)
- **Raw NMEA Sentences (Two-part multi-sentence packet):**
  ```text
  !AIVDM,2,1,1,A,55?MbV02;H;s<HtKR20EHE:0@T4@Dn2222222216L961O5Gf0NSQEp6ClRp8,0*1C
  !AIVDM,2,2,1,A,88888888880,2*25
  ```
- **Hex Dump of 424-bit Payload (Padded to 53 bytes):**
  ```text
  0000: 14 53 DD AA 60 02 2D 82 FB 31 8F 1B 88 20 15 61   .S..`.-..1... .a
  0010: 52 80 42 41 10 53 60 82 08 20 82 08 20 46 70 91   R.BA.S`.. .. Fp.
  0020: 81 7C 55 EE 01 E8 E1 57 81 93 D2 2E 08 20 82 08   .|U....W..... ..
  0030: 20 82 08 20 80                                     .. .
  ```
- **Field-by-Field Bit Decomposition:**

| Field Name | Bit Span | Width | Hex Value | Raw Decimal | Decoded Engineering Value |
|:---|:---:|:---:|:---:|:---:|:---|
| Message ID | 0–5 | 6 | `0x5` | 5 | Message 5 (Class A static and voyage data) |
| Repeat Indicator | 6–7 | 2 | `0x0` | 0 | 0 (Original transmission) |
| Source MMSI | 8–37 | 30 | `0x14F76A98` | 351759000 | MMSI 351759000 |
| AIS Version | 38–39 | 2 | `0x0` | 0 | ITU-R M.1371-1 compliant station |
| IMO Number | 40–69 | 30 | `0x8B60BE` | 9134270 | IMO 9134270 |
| Call Sign | 70–111 | 42 | `0x3318F1B8820` | — | `"3FOF8  "` (Trailing spaces stripped) |
| Vessel Name | 112–231 | 120 | `0x15615...` | — | `"EVER DIADEM         "` |
| Ship and Cargo Type | 232–239 | 8 | `0x46` | 70 | 70 (Cargo vessel, all ships of this type) |
| Dimension to Bow (A) | 240–248 | 9 | `0xE1` | 225 | $225\text{ m}$ from reference point to bow |
| Dimension to Stern (B) | 249–257 | 9 | `0x46` | 70 | $70\text{ m}$ from reference point to stern |
| Dimension to Port (C) | 258–263 | 6 | `0x1` | 1 | $1\text{ m}$ from reference point to port |
| Dimension to Starboard (D) | 264–269 | 6 | `0x1F` | 31 | $31\text{ m}$ from reference point to starboard |
| EPFD Type | 270–273 | 4 | `0x1` | 1 | GPS positioning receiver |
| ETA Month | 274–277 | 4 | `0x5` | 5 | May |
| ETA Day | 278–282 | 5 | `0xF` | 15 | 15th day |
| ETA Hour | 283–287 | 5 | `0xE` | 14 | 14:00 UTC |
| ETA Minute | 288–293 | 6 | `0x0` | 0 | 00 minutes |
| Maximum Draught | 294–301 | 8 | `0x7A` | 122 | $12.2\text{ m}$ static draught |
| Destination | 302–421 | 120 | `0x3855E...` | — | `"NEW YORK            "` |
| DTE Flag | 422 | 1 | `0x0` | 0 | Data terminal ready |
| Spare | 423 | 1 | `0x0` | 0 | Padding bit |

- **pyais Python Verification Snippet:**
  ```python
  from pyais import decode

  p1 = "!AIVDM,2,1,1,A,55?MbV02;H;s<HtKR20EHE:0@T4@Dn2222222216L961O5Gf0NSQEp6ClRp8,0*1C"
  p2 = "!AIVDM,2,2,1,A,88888888880,2*25"
  msg = decode(p1, p2)
  print(msg)
  # Output:
  # MessageType5(msg_type=5, repeat=0, mmsi=351759000, ais_version=0, imo=9134270,
  #              callsign='3FOF8', shipname='EVER DIADEM', ship_type=<ShipType.Cargo: 70>,
  #              to_bow=225, to_stern=70, to_port=1, to_starboard=31, epfd=<EpfdType.GPS: 1>,
  #              month=5, day=15, hour=14, minute=0, draught=12.2, destination='NEW YORK',
  #              dte=False, spare_1=b'\x00')
  ```

---

### Worked Example 3: Standard Class B position report (Message 18)
- **Raw NMEA Sentence:**
  ```text
  !AIVDM,1,1,,A,B52K>;h00Fc>jpUlNV@ikwpUoP06,0*4C
  ```
- **Hex Dump of 168-bit Payload:**
  ```text
  0000: 48 50 9B 38 BC 00 01 6A CE CB 89 74 7A 64 31 CF   HP.8...j...tzd1.
  0010: FE 25 DE 00 06                                    .%...
  ```
- **Field-by-Field Bit Decomposition:**

| Field Name | Bit Span | Width | Hex Value | Raw Decimal | Decoded Engineering Value |
|:---|:---:|:---:|:---:|:---:|:---|
| Message ID | 0–5 | 6 | `0x12` | 18 | Message 18 (Standard Class B position report) |
| Repeat Indicator | 6–7 | 2 | `0x0` | 0 | 0 (Original transmission) |
| Source MMSI | 8–37 | 30 | `0x1426CE2F` | 338087471 | MMSI 338087471 (United States registered vessel) |
| Regional / Reserved | 38–45 | 8 | `0x0` | 0 | Reserved / default |
| Speed Over Ground (SOG) | 46–55 | 10 | `0x1` | 1 | $0.1\text{ kn}$ |
| Position Accuracy (PA) | 56 | 1 | `0x0` | 0 | 0 (Low accuracy, unaugmented GNSS $> 10\text{ m}$) |
| Longitude | 57–84 | 28 | `0xD59D971` | -44443279 | $-74.072132^\circ$ ($74^\circ 04.3279'\text{ W}$) |
| Latitude | 85–111 | 27 | `0x1747A64` | 24410724 | $+40.684540^\circ$ ($40^\circ 41.0724'\text{ N}$) |
| Course Over Ground (COG) | 112–123 | 12 | `0x31C` | 796 | $79.6^\circ$ |
| True Heading (HDG) | 124–132 | 9 | `0x1FF` | 511 | 511 (Heading sensor not available) |
| Time Stamp | 133–138 | 6 | `0x31` | 49 | 49 seconds past the UTC minute |
| Regional / Reserved | 139–140 | 2 | `0x0` | 0 | Reserved bits |
| Class B Unit Flag | 141 | 1 | `0x1` | 1 | 1 (Class B CS unit, carrier-sense architecture) |
| Class B Display Flag | 142 | 1 | `0x0` | 0 | 0 (No integrated display) |
| Class B DSC Flag | 143 | 1 | `0x1` | 1 | 1 (Equipped with DSC receiver) |
| Class B Band Flag | 144 | 1 | `0x1` | 1 | 1 (Capable of switching across entire marine band) |
| Class B Message 22 Flag | 145 | 1 | `0x1` | 1 | 1 (Responds to Message 22 channel commands) |
| Mode Flag | 146 | 1 | `0x0` | 0 | 0 (Autonomous and continuous mode) |
| RAIM Flag | 147 | 1 | `0x1` | 1 | 1 (RAIM in use) |
| Comm-State Selector | 148 | 1 | `0x1` | 1 | 1 (ITDMA comm-state format / CS unit indicator) |
| Communication State | 149–167 | 19 | `0x60006` | 393222 | Fixed Class B CS sentinel (`1100000000000000110`) |

- **pyais Python Verification Snippet:**
  ```python
  from pyais import decode

  msg = decode("!AIVDM,1,1,,A,B52K>;h00Fc>jpUlNV@ikwpUoP06,0*4C")
  print(msg)
  # Output:
  # MessageType18(msg_type=18, repeat=0, mmsi=338087471, reserved_1=0, speed=0.1,
  #               accuracy=False, lon=-74.072132, lat=40.68454, course=79.6, heading=511,
  #               second=49, reserved_2=0, cs=True, display=False, dsc=True, band=True,
  #               msg22=True, assigned=False, raim=True, radio=917510)
  ```

---

## References

- Harati-Mokhtari, A., Wall, A., Brooks, P., Wang, J. (2007). Automatic Identification System (AIS): Data Reliability and Human Error Implications. *The Journal of Navigation*, 60(3):373–389.
- IALA (2019). *The Use of the Automatic Identification System (AIS) in Marine Aids to Navigation Services*. IALA Recommendation R0126 (formerly A-126), Edition 1.5. Saint-Germain-en-Laye: International Association of Marine Aids to Navigation and Lighthouse Authorities.
- IEC (2015). *Maritime navigation and radiocommunication equipment and systems — Automatic identification systems (AIS) — Part 1: AIS Base Stations — Minimum operational and performance requirements, methods of testing and required test results*. IEC 62320-1:2015, Edition 2.0. Geneva: International Electrotechnical Commission.
- IEC (2016). *Maritime navigation and radiocommunication equipment and systems — Automatic identification systems (AIS) — Part 2: AIS AtoN Stations — Minimum operational and performance requirements, methods of testing and required test results*. IEC 62320-2:2016, Edition 2.0. Geneva: International Electrotechnical Commission.
- IEC (2017). *Maritime navigation and radiocommunication equipment and systems — Class B shipborne equipment of the automatic identification system (AIS) — Part 1: Carrier-sense time division multiple access (CSTDMA) techniques*. IEC 62287-1:2017, Edition 3.0. Geneva: International Electrotechnical Commission.
- IEC (2017). *Maritime navigation and radiocommunication equipment and systems — Class B shipborne equipment of the automatic identification system (AIS) — Part 2: Self-organising time division multiple access (SOTDMA) techniques*. IEC 62287-2:2017, Edition 2.0. Geneva: International Electrotechnical Commission.
- IEC (2018). *Maritime navigation and radiocommunication equipment and systems — Automatic Identification Systems (AIS) — Part 2: Class A shipborne equipment of the automatic identification system (AIS) — Operational and performance requirements, methods of test and required test results*. IEC 61993-2:2018, Edition 3.0. Geneva: International Electrotechnical Commission.
- IMO (1998). *Recommendation on Performance Standards for an Universal Shipborne Automatic Identification System (AIS)*. Resolution MSC.74(69), Annex 3. London: International Maritime Organization.
- IMO (2004). *Guidance on the Use of the UN/LOCODE in the Destination Field in AIS Messages*. SN/Circ.244. London: International Maritime Organization.
- IMO (2010). *Guidance on the Use of AIS Application-Specific Messages*. SN.1/Circ.289. London: International Maritime Organization.
- IMO (2017). *IMO Ship Identification Number Scheme*. Resolution A.1117(30). London: International Maritime Organization.
- ITU-R (2001). *Technical characteristics for a universal shipborne automatic identification system using time division multiple access in the VHF maritime mobile band*. Recommendation ITU-R M.1371-1. Geneva: International Telecommunication Union.
- ITU-R (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*. Recommendation ITU-R M.1371-5. Geneva: International Telecommunication Union.
- ITU-R (2019). *Technical characteristics of autonomous maritime radio devices operating in the frequency band 156–162.05 MHz*. Recommendation ITU-R M.2135-1. Geneva: International Telecommunication Union.
- ITU-R (2026). *Assignment and use of identities in the maritime mobile service*. Recommendation ITU-R M.585-10. Geneva: International Telecommunication Union.
- ITU-R (2026). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*. Recommendation ITU-R M.1371-6. Geneva: International Telecommunication Union.
- Neeb, M. (2023). *pyais: A pure Python library for decoding AIVDM/AIVDO maritime messages* (version 3.2.3). https://github.com/M0r13n/pyais.
- Raymond, E. S., Schwehr, K. (2023). *AIVDM/AIVDO Protocol Decoding* (version 1.58). GPSD Project. https://gpsd.gitlab.io/gpsd/AIVDM.html.
