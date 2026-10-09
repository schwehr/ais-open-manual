# Chapter 22 — The message catalog (Messages 1–27)

> **Part IV — The system: architecture and protocol.** Comprehensive field-by-field reference, bit-level semantics, sentinel values, and protocol mechanics for the foundational messages of the maritime VHF data link.

**In this chapter.** You will master the message catalog defined across Recommendation ITU-R M.1371, analyzing how information is formatted, packed, and exchanged over the VHF data link (VDL). We examine the bit layouts, scaling laws, signed representations, and invalid-data sentinels across the 27 operational message types, as well as the newly codified single-slot Aid to Navigation (Message 28) introduced in Recommendation ITU-R M.1371-6. You will understand how position coordinates are projected into signed fixed-point integers, why rate-of-turn encoding relies on a non-linear square-root transformation, and how timestamp sentinels communicate sensor degradation and positioning mode. We deconstruct multi-slot voyage announcements, binary encapsulation containers, base station coordination broadcasts, Class B position reports, and low-bandwidth long-range satellite frames. Through worked bit-level decodes and a verified multi-decoder test corpus, you will gain the forensic skill required to parse raw payload armor, identify edge cases, and eliminate silent data-corruption traps in marine data pipelines.

## 22.1 The message catalog and architecture

The Automatic Identification System (**AIS**) VHF data link (**VDL**) relies on a structured catalog of messages designed to balance real-time tracking, static ship identification, safety notifications, and link-layer network management. Defined internationally by the International Telecommunication Union Radiocommunication Sector (**ITU-R**) in **Recommendation ITU-R M.1371**, the message catalog assigns specific functional profiles, repetition rates, access schemes, and slot budgets to distinct maritime station classes.

The protocol design enforces strict separation of concerns across message identifiers. Message types are identified by an integer ID spanning bits 0 to 5 (a 6-bit unsigned integer permitting values 0 to 63). In the foundational standard **ITU-R M.1371-1** through **ITU-R M.1371-5**, message identifiers 1 through 27 were progressively assigned to operational roles, with IDs 0 and 28–63 left unassigned or reserved for future expansion. In **ITU-R M.1371-6** (approved in February 2026), Message 28 was formally standardized to introduce a compact, single-slot Aid to Navigation report, while identifiers 60 to 63 were dedicated to Autonomous Maritime Radio Devices (**AMRD**) under **Recommendation ITU-R M.2135**. Identifiers 29 through 59 remain unassigned and reserved for future international standardization.

```
+---------------+-----------------------------------------------+--------------+
| Message ID(s) | Functional Category                           | Transmitters |
+---------------+-----------------------------------------------+--------------+
| 1, 2, 3       | Class A Position Reports (SOTDMA, ITDMA)       | Class A      |
| 4, 11         | Base Station Report / UTC & Position Inquiry   | Base Station |
| 5             | Class A Static and Voyage-Related Data        | Class A      |
| 6, 8          | Addressed / Broadcast Binary Messages (ABM/BBM)| All stations |
| 7, 13         | Binary Acknowledgment / Safety Acknowledgment | Addressed rx |
| 9             | Standard SAR Aircraft Position Report         | SAR Aircraft |
| 10            | UTC and Date Inquiry                          | Any station  |
| 12, 14        | Addressed / Broadcast Safety-Related Messages | All stations |
| 15            | Interrogation                                 | Base, Mobiles|
| 16            | Assigned Mode Command                         | Base Station |
| 17            | GNSS Broadcast Binary Message (DGNSS)         | Base Station |
| 18, 19        | Class B Position Reports (Standard, Extended) | Class B      |
| 20            | Data Link Management Message                  | Base Station |
| 21            | Aid to Navigation (AtoN) Report               | AtoN Station |
| 22            | Channel Management                            | Base, Mobile |
| 23            | Group Assignment Command                      | Base Station |
| 24A, 24B      | Class B Static Data Report                    | Class B, All |
| 25, 26        | Single / Multi-Slot Binary Containers         | All stations |
| 27            | Long-Range Automatic Identification Broadcast | Class A, B   |
+---------------+-----------------------------------------------+--------------+
```

Every message broadcast on the VDL begins with an identical 38-bit preamble block:
1. **Message Identifier (6 bits):** Defines the message structure (values 1–28).
2. **Repeat Indicator (2 bits):** Controls message retransmission by intermediate coastal repeaters. Set to `0` by the originating transmitter; incremented by relay stations up to `3`, which indicates "do not repeat any more." In Message 27, this field is fixed permanently to `3`.
3. **Source MMSI (30 bits):** The 9-digit Maritime Mobile Service Identity (**MMSI**) uniquely identifying the transmitting station, formatted in accordance with **Recommendation ITU-R M.585**. Unsigned 30-bit integers accommodate decimal identities up to $1{,}073{,}741{,}823$, comfortably spanning valid 9-digit MMSIs ($000000000$ to $999999999$).

Message transmission priorities are grouped into four operational tiers within transponder transmission queues:
- **Priority 1 (Critical Real-Time):** Messages 1, 2, 3, 4, 7, 9, 13, 16, 18, 19, 20, 21, 22, 23, 27, and 28. These packets govern immediate collision avoidance vectors, link management, and emergency acknowledgments.
- **Priority 2 (Safety Information):** Messages 12, 14, and 17, delivering navigational warnings, urgent weather text, and differential GNSS corrections.
- **Priority 3 (System Inquiries):** Messages 10, 11, and 15, handling synchronization and polling requests. Message 5 is elevated to Priority 3 when transmitted directly in response to an interrogation.
- **Priority 4 (Background & Static):** Messages 5, 6, 8, 24A, 24B, 25, and 26. These carry static voyage records and routine application payloads.

## 22.2 Core physical and encoding conventions

Every bit transmitted over the GMSK physical link represents data organized under strict mathematical conventions. All coordinates are projected exclusively onto the World Geodetic System 1984 (**WGS 84**) reference datum. Multi-byte and multi-bit numeric fields are packed and transmitted most significant bit (**MSB**) first (network byte order), matching the serial bitstream produced by standard High-Level Data Link Control (**HDLC**) framing hardware.

Signed quantities—including latitude, longitude, and rate of turn—are encoded using standard two's complement binary representation. Decimal conversions must account for the explicit bit boundaries of each field to avoid sign inversion bugs during decoding.

Textual data across static announcements and safety notices is serialized using a dedicated **6-bit ASCII** alphabet (defined in ITU-R M.1371 Table 45). Standard 8-bit ASCII characters are mapped into 6-bit codes ranging from `0` to `63`:

```
+-----------+---------------+---------------------------------------+
| 6-bit Dec | Binary Nibble | Mapped Character Representation       |
+-----------+---------------+---------------------------------------+
| 0         | 000000        | '@' (Sentinel / Padding Character)   |
| 1–26      | 000001–011010 | Capital Letters 'A' through 'Z'       |
| 27–31     | 011011–011111 | Symbols: '[', '\', ']', '^', '_'     |
| 32        | 100000        | Space ' '                             |
| 33–47     | 100001–101111 | Symbols: '!', '"', '#', ..., '/', '-' |
| 48–57     | 110000–111001 | Digits '0' through '9'                |
| 58–63     | 111010–111111 | Symbols: ':', ';', '<', '=', '>', '?' |
+-----------+---------------+---------------------------------------+
```

When character strings (such as a vessel name, radio call sign, or destination harbor) do not completely fill their allocated bit budget, unused trailing characters must be filled with the `@` symbol (code `000000`). Receiving decoders strip trailing `@` characters and spaces to recover clean text strings.

> **Definitions that bite.** In 6-bit ASCII, binary `000000` is the `@` symbol, representing the formal unpopulated padding character. It does not represent an empty string or null terminator. When uninitialized memory containing all zeros is converted by naive decoders without sentinel trimming, vessel names appear corrupted as `@@@@@@@@@@@@@@@@@@@@`.

## 22.3 Position and kinematic reporting (Messages 1, 2, 3)

Messages 1, 2, and 3 provide autonomous position reports for Class A shipborne mobile transponders. While sharing an identical 168-bit internal payload layout, their distinction lies in how the transmitter manages link-layer channel access:
- **Message 1 (SOTDMA):** Scheduled autonomously via Self-Organizing Time Division Multiple Access (**SOTDMA**), allocating slots recursively through slot timeouts and candidate offsets ([Chapter 21](ch21-link-layer-tdma.md)).
- **Message 2 (SOTDMA Assigned):** Broadcast when operating in response to an assigned reporting cadence dictated by a coastal Vessel Traffic Service (**VTS**) via Message 16.
- **Message 3 (ITDMA):** Broadcast during Incremental Time Division Multiple Access (**ITDMA**) operations, commonly used during startup, channel switching, or pre-announcing future slot reservations before an autonomous SOTDMA link state is established.

The 168-bit payload spans exactly one TDMA slot, structured into sixteen distinct fields:

```
+---------+------+--------------------------------+----------------------------+
| Bits    | Size | Field Description              | Engineering Units / Range  |
+---------+------+--------------------------------+----------------------------+
| 0–5     | 6    | Message Identifier             | Value 1, 2, or 3           |
| 6–7     | 2    | Repeat Indicator               | 0–3; default 0             |
| 8–37    | 30   | Transmitting MMSI              | 9-digit decimal identity   |
| 38–41   | 4    | Navigational Status            | 0–15; Table of nav status  |
| 42–49   | 8    | Rate of Turn (ROT)             | Signed two's complement    |
| 50–59   | 10   | Speed Over Ground (SOG)        | 0.1 kn; 0–102.2 kn         |
| 60      | 1    | Position Accuracy              | 1 = High (<=10m), 0 = Low  |
| 61–88   | 28   | Longitude                      | Signed 1/10,000 minute     |
| 89–115  | 27   | Latitude                       | Signed 1/10,000 minute     |
| 116–127 | 12   | Course Over Ground (COG)       | 0.1 deg; 0.0–359.9 deg     |
| 128–136 | 9    | True Heading                   | 1 deg; 0–359 deg           |
| 137–142 | 6    | UTC Second of Fix              | 0–59 s; 60–63 sentinels    |
| 143–144 | 2    | Special Manoeuvre Indicator    | 0 = n/a, 1 = no, 2 = yes   |
| 145–147 | 3    | Spare Bits                     | Reserved, set to 0         |
| 148     | 1    | RAIM Flag                      | 0 = RAIM inactive, 1 = on  |
| 149–167 | 19   | Communication State            | SOTDMA (1,2) or ITDMA (3)  |
+---------+------+--------------------------------+----------------------------+
```

### Navigational status semantics
Field bits 38–41 convey the current operational state of the vessel as confirmed by the bridge watch officer or automated bridge sensors:
- `0`: Under way using engine
- `1`: At anchor
- `2`: Not under command (NUC)
- `3`: Restricted in ability to manoeuvre (RAM)
- `4`: Constrained by her draught
- `5`: Moored
- `6`: Aground
- `7`: Engaged in fishing
- `8`: Under way sailing
- `9`: Reserved for future amendment of Hazardous Material transport rules
- `10`: Reserved for future amendment of Wing-in-Ground (WIG) craft
- `11`: Power-driven vessel towing astern (regional European inland definition)
- `12`: Power-driven vessel pushing ahead or towing alongside (regional inland)
- `13`: Reserved for future use
- `14`: Active AIS-SART, MOB device, or EPIRB-AIS emergency transmitter
- `15`: Undefined (default; also used by transponders undergoing test routines)

### The Rate of Turn encoding law
The Rate of Turn (**ROT**) field spans 8 bits, interpreted as a signed two's complement integer spanning the raw integer range $-128$ to $+127$. To compress a dynamic turning range up to hundreds of degrees per minute into 8 bits while retaining fine resolution during slight course corrections, ITU-R M.1371 specifies an intentional non-linear square-root relationship:

$$	ext{ROT}_{	ext{AIS}} = 	ext{round}\left(4.733 	imes \sqrt{	ext{ROT}_{	ext{sensor}}}ight)$$

Here, $	ext{ROT}_{	ext{sensor}}$ is expressed in degrees per minute ($^\circ/	ext{min}$). The sign of the sensor turn rate is preserved in the output: positive numbers indicate a turn to starboard (right), while negative numbers indicate a turn to port (left).

To invert an incoming raw AIS integer $	ext{ROT}_{	ext{AIS}}$ back to physical angular velocity:

$$	ext{ROT}_{	ext{sensor}} = \operatorname{sgn}(	ext{ROT}_{	ext{AIS}}) 	imes \left(rac{|	ext{ROT}_{	ext{AIS}}|}{4.733}ight)^2$$

This non-linear scale provides precise fidelity at gentle turn rates. An entry of $\pm1$ corresponds to approximately $0.045^\circ/	ext{min}$, while $\pm15$ yields $10.04^\circ/	ext{min}$. The continuous mathematical scale terminates at $\pm126$, representing a turning rate of:

$$\left(rac{126}{4.733}ight)^2 pprox 708.7^\circ/	ext{min}$$

Crucially, values outside $[-126, +126]$ are non-linear sentinel flags that must never be plugged into the squaring equation:
- **$+127$ (`0x7F`):** Turning right at more than $5^\circ$ per 30 seconds ($10^\circ/	ext{min}$), but the vessel is not equipped with an external rate-of-turn indicator (**TI**).
- **$-127$ (`0x81`):** Turning left at more than $5^\circ$ per 30 seconds ($10^\circ/	ext{min}$), with no rate-of-turn indicator available.
- **$-128$ (`0x80`):** Default sentinel indicating no turn information is available at all.

> **Worked example.** Consider an AIS position report with an ROT byte of `0x81`. In 8-bit signed two's complement, `0x81` is $-127$. A naive software decoder evaluating the inverse formula computes:
>
> $$	ext{ROT} = -\left(rac{127}{4.733}ight)^2 pprox -720.0^\circ/	ext{min}$$
>
> That result is physically wrong. The vessel is not spinning like a top at two full revolutions per minute; it is simply executing an ordinary port turn exceeding $10^\circ/	ext{min}$ without an approved IMO rate-of-turn gyro connected. Automated processing engines must trap $\pm127$ and $-128$ prior to applying mathematical transformations.

```
+------------+-------------+--------------------------------------------------+
| Raw Value  | Hex Pattern | Physical Interpretation                          |
+------------+-------------+--------------------------------------------------+
| +127       | 0x7F        | Turning right > 5 deg/30 s; no TI available     |
| +1 to +126 | 0x01 to 0x7E| Turning right at (ROT/4.733)^2 deg/min           |
| 0          | 0x00        | Turning at 0 deg/min (or straight ahead)         |
| -1 to -126 | 0xFF to 0x82| Turning left at -(ROT/4.733)^2 deg/min          |
| -127       | 0x81        | Turning left > 5 deg/30 s; no TI available      |
| -128       | 0x80        | No turn information available (default sentinel) |
+------------+-------------+--------------------------------------------------+
```

### High-resolution coordinate packing
Geographic position coordinates are transmitted as signed two's complement integers in units of $1/10{,}000$ of a minute of arc ($1/600{,}000$ of a degree):
- **Longitude (28 bits):** Valid geographic values span $-180.0^\circ$ to $+180.0^\circ$ (integer range $-108{,}000{,}000$ to $+108{,}000{,}000$). The unsigned binary container supports integers from $-134{,}217{,}728$ to $+134{,}217{,}727$. The sentinel for "longitude not available" is set to $+181.0^\circ$, encoded as exactly $+108{,}600{,}000$ (`0x06791AC0`).
- **Latitude (27 bits):** Valid geographic values span $-90.0^\circ$ to $+90.0^\circ$ (integer range $-54{,}000{,}000$ to $+54{,}000{,}000$). The sentinel for "latitude not available" is set to $+91.0^\circ$, encoded as exactly $+54{,}600{,}000$ (`0x03412140`).

At the equator, $1/10{,}000$ minute of latitude corresponds to exactly:

$$rac{1852	ext{ m}}{10{,}000} = 0.1852	ext{ m} pprox 18.52	ext{ cm}$$

This represents millimeter-level precision across global coordinates, ensuring that rounding errors within the protocol encoding remain negligible compared to differential GPS sensor inaccuracies.

### Kinematics and timestamp flags
- **Speed Over Ground (SOG):** 10-bit unsigned integer scaled in units of $0.1	ext{ kn}$. The range $0$ to $1{,}022$ represents speeds from $0.0$ to $102.2	ext{ kn}$. Any velocity equal to or exceeding $102.2	ext{ kn}$ saturates at $1{,}022$. The sentinel value $1{,}023$ (`0x3FF`) signifies "speed not available."
- **Course Over Ground (COG):** 12-bit unsigned integer scaled in units of $0.1^\circ$, ranging from $0$ to $3{,}599$ ($0.0^\circ$ to $359.9^\circ$). Value $3{,}600$ (`0xE10`) indicates "course not available." Values $3{,}601$ through $4{,}095$ are invalid and must not be generated.
- **True Heading:** 9-bit unsigned integer in degrees ($0^\circ$ to $359^\circ$) referenced to true north. Value $511$ (`0x1FF`) indicates "heading not available." Values $360$ through $510$ are forbidden.
- **Time Stamp:** 6-bit unsigned integer ($0$ to $63$). Values $0$ to $59$ indicate the exact UTC second when the positioning sensor generated the navigational fix. Sentinels communicate positioning equipment status:
  - `60`: Timestamp not available (default).
  - `61`: Positioning system operating in manual input mode.
  - `62`: Positioning system operating in dead reckoning mode.
  - `63`: Positioning system inoperative or failed.

## 22.4 Static and voyage-related data (Message 5)

Class A transponders broadcast Message 5 every 6 minutes, or immediately upon request via an interrogation message. Spanning 424 bits, Message 5 occupies exactly **two contiguous TDMA slots**, carrying vessel parameters, dimensions, and dynamic voyage destination records.

```
+---------+------+--------------------------------+----------------------------+
| Bits    | Size | Field Description              | Engineering Units / Coding |
+---------+------+--------------------------------+----------------------------+
| 0–5     | 6    | Message Identifier             | Constant 5                 |
| 6–7     | 2    | Repeat Indicator               | 0–3; default 0             |
| 8–37    | 30   | Transmitting MMSI              | 9-digit decimal identity   |
| 38–39   | 2    | AIS Version Indicator          | 0 = 1371-1, 1 = -3, 3 = -6 |
| 40–69   | 30   | IMO Ship Identification Number | 1,000,000–9,999,999 or ID  |
| 70–111  | 42   | Radio Call Sign                | 7 chars in 6-bit ASCII     |
| 112–231 | 120  | Vessel Name                    | 20 chars in 6-bit ASCII    |
| 232–239 | 8    | Type of Ship and Cargo         | Table 51 numeric code      |
| 240–269 | 30   | Dimension and Reference Point  | Bow (9), Stern (9), P/S (6)|
| 270–273 | 4    | Type of EPFD                   | 1 = GPS, 2 = GLONASS, etc. |
| 274–293 | 20   | Estimated Time of Arrival      | MMDDHHMM (Month/Day/Hr/Min)|
| 294–301 | 8    | Maximum Present Static Draught | 0.1 m; 0–25.5 m            |
| 302–421 | 120  | Destination Port / Area        | 20 chars in 6-bit ASCII    |
| 422     | 1    | Data Terminal Ready (DTE)      | 0 = available, 1 = not     |
| 423     | 1    | Spare Bit                      | Reserved, set to 0         |
+---------+------+--------------------------------+----------------------------+
```

### Identifier fields and IMO numbers
The **AIS Version Indicator** (bits 38–39) communicates the standard edition supported by the transponder: `0` denotes ITU-R M.1371-1; `1` denotes M.1371-3; `2` denotes M.1371-5; `3` denotes M.1371-6 or later.

The **IMO Number** field (bits 40–69) allocates 30 bits. Valid IMO ship identification numbers issued under IMO Resolution A.1117(30) span the 7-digit range $1{,}000{,}000$ to $9{,}999{,}999$. Unregistered or domestic commercial vessels lacking an official IMO number transmit their official national flag-state registration identity in the expanded integer range $10{,}000{,}000$ to $1{,}073{,}741{,}823$. Value `0` indicates that no IMO or national registration number is available.

### Ship and cargo classifications
The 8-bit **Type of Ship and Cargo** field (bits 232–239) provides high-level vessel classifications. Historically, the tens digit designated the broad operational class (e.g., `3` for special craft, `6` for passenger, `7` for cargo, `8` for tankers), while the units digit indicated the carriage of Dangerous Goods (**DG**), Harmful Substances (**HS**), or Marine Pollutants (**MP**) classified under IMO regulations (categories X, Y, Z, and OS).

Under ITU-R M.1371-6 Table 51, previously reserved codes were formally allocated to specific vessel configurations:
- `01`: Research vessel
- `04`: Icebreaker
- `05`: Buoy tender
- `06`: Cable layer
- `07`: Pipe layer
- `11`: Floating Production Storage and Offloading (**FPSO**)
- `12`: Fish factory vessel
- `14`: Offshore support vessel
- `18`: Crew boat
- `38`: Trawler
- `39`: Patrol vessel
- `45`: High-Speed Craft (HSC) passenger
- `46`: High-Speed Craft (HSC) ro-ro
- `65`: Cruise ship
- `66`: Passenger ferry
- `75`: Bulk carrier
- `76`: Container ship
- `77`: Ro-ro cargo vessel
- `86`: Articulated Tug-Barge (**ATB**) or Integrated Tug-Barge (**ITB**)

### Dimensional reference point geometry
Ship dimensions and internal GNSS antenna placement are encoded within a 30-bit composite field:
- **Dimension A (9 bits, to bow):** Distance from the reference point to the forward-most extremity ($0$ to $511	ext{ m}$; $511$ indicates $\ge511	ext{ m}$).
- **Dimension B (9 bits, to stern):** Distance from the reference point to the aft extremity ($0$ to $511	ext{ m}$).
- **Dimension C (6 bits, to port):** Distance from the reference point to the port side ($0$ to $63	ext{ m}$; $63$ indicates $\ge63	ext{ m}$).
- **Dimension D (6 bits, to starboard):** Distance from the reference point to the starboard side ($0$ to $63	ext{ m}$).

The total vessel length is computed as $A + B$, while the total beam is $C + D$. When dimensions are unknown or unpopulated, $A = B = C = D = 0$. For vessels towing alongside or pushing ahead, the dimensions must encompass the overall length and beam of the entire composite flotilla.

```
                      Bow (Forward)
                          /                          /                           /                            |   A   |
                       |       |
            Port  <----+---x---+----> Starboard
             (C)       |   |   |        (D)
                       |   B   |
                       |       |
                       +-------+
                      Stern (Aft)
```

### Estimated Time of Arrival (ETA) decomposition
The 20-bit ETA field packs the intended UTC arrival time using four distinct sub-fields, each maintaining an independent sentinel value:
- **Month (bits 289–292, 4 bits):** $1$ to $12$; sentinel `0` = not available.
- **Day (bits 284–288, 5 bits):** $1$ to $31$; sentinel `0` = not available.
- **Hour (bits 279–283, 5 bits):** $0$ to $23$; sentinel `24` = not available.
- **Minute (bits 274–278, 6 bits):** $0$ to $59$; sentinel `60` = not available.

When an ETA is completely unknown, the entire 20-bit block evaluates to binary `0000 00000 11000 111100` (month 0, day 0, hour 24, minute 60). Ingestion pipelines must never assume that an invalid month implies an invalid minute; each sub-field must be validated independently.

## 22.5 Base stations and time synchronization (Messages 4, 10, 11)

Fixed coastal base stations provide geographic and timing anchors across the VDL:
- **Message 4 (Base Station Report):** A 168-bit broadcast occupying one slot, transmitted every 10 seconds by base stations. It delivers absolute UTC time (year, month, day, hour, minute, second) with microsecond precision derived from atomic GNSS receivers, accurate fixed station coordinates ($1/10{,}000	ext{ min}$ resolution), and the link-layer transmission control flag for Message 27.
- **Message 10 (UTC and Date Inquiry):** A 72-bit addressed polling frame used by mobile stations lacking operational GNSS clocks to request time synchronization from a coastal base station.
- **Message 11 (UTC and Date Response):** Broadcast by base stations answering a Message 10 request, carrying identical time and coordinate layouts to Message 4.

Mobile transponders monitor Message 4 broadcasts to determine whether they reside within 120 nautical miles ($222	ext{ km}$) of an active base station, modulating their autonomous transmission behaviors accordingly.

## 22.6 Binary and safety-related payloads (Messages 6, 7, 8, 12, 13, 14, 25, 26)

The message catalog provides standardized envelopes to transport arbitrary application data and safety notifications across the maritime network.

### Addressed and broadcast binary messages
- **Message 6 (Addressed Binary Message, ABM):** Transmits targeted payloads to a designated destination MMSI. Contains a 2-bit sequence number and a 1-bit retransmit flag. Accommodates up to 936 binary data bits across up to 3 slots under autonomous access, or up to 5 slots ($1{,}176	ext{ bits}$) when assigned fixed access under FATDMA.
- **Message 8 (Broadcast Binary Message, BBM):** Transmits omnidirectional payloads to all listening stations within radio horizon. Allocates up to 968 binary data bits across up to 3 slots ($1{,}008	ext{ bits}$ total frame size).

Both Message 6 and 8 payloads begin with a mandatory 16-bit **Application Identifier** (**AI**), composed of a 10-bit Designated Area Code (**DAC**) and a 6-bit Function Identifier (**FI**), governing Application-Specific Messages (**ASM**) ([Chapter 23](ch23-asm-binary-payloads.md)).

```
+------------+------------------+------------------+------------------+
| Slot Count | Message 6 Max    | Message 8 Max    | Message 26 Max   |
| Allocated  | Application Bits | Application Bits | Application Bits |
+------------+------------------+------------------+------------------+
| 1 Slot     | 64 bits (8 B)    | 96 bits (12 B)   | 56 bits (7 B)    |
| 2 Slots    | 288 bits (36 B)  | 320 bits (40 B)  | 280 bits (35 B)  |
| 3 Slots    | 512 bits (64 B)  | 544 bits (68 B)  | 504 bits (63 B)  |
| 4 Slots    | 736 bits (92 B)  | 768 bits (96 B)  | 728 bits (91 B)  |
| 5 Slots    | 936 bits (117 B) | 968 bits (121 B) | 952 bits (119 B) |
+------------+------------------+------------------+------------------+
```

### Acknowledgments and safety notifications
- **Messages 7 and 13 (Binary and Safety Acknowledgments):** Acknowledges receipt of addressed Messages 6 and 12. Each frame can acknowledge up to four separate transactions simultaneously, packing pairs of 30-bit destination MMSIs and their associated 2-bit sequence numbers.
- **Messages 12 and 14 (Addressed and Broadcast Safety-Related Messages):** Transport plain-text navigational warnings and emergency notifications formatted in 6-bit ASCII. Message 12 provides addressed delivery up to 936 text bits, while Message 14 broadcasts up to 968 text bits across 3 slots.

### Compact binary containers (Messages 25 and 26)
To minimize slot congestion caused by multi-slot binary messages, ITU-R M.1371 introduced compact single- and multi-slot containers:
- **Message 25 (Single-Slot Binary Message):** Employs dynamic structural flags to strip addressing overhead. Can broadcast unstructured data (up to 128 bits), broadcast structured ASM with a 16-bit AI (up to 112 bits), or address targeted stations with or without an AI (80 to 96 bits). Class B transponders operating under Carrier-Sense TDMA (**CSTDMA**) are strictly forbidden from transmitting Message 25.
- **Message 26 (Multi-Slot Binary Message with Comm State):** Extends Message 25 by appending a link-layer communication state block, permitting autonomous multi-slot reservations up to 5 slots ($1{,}064	ext{ bits}$ total) without requiring base station FATDMA pre-allocation.

## 22.7 Search and rescue, polling, and link management (Messages 9, 15, 16, 17, 20, 22, 23)

Dedicated message formats support tactical coordination, dynamic spectrum allocation, and airborne search assets:
- **Message 9 (Standard SAR Aircraft Position Report):** A 168-bit single-slot frame broadcast by Search and Rescue (**SAR**) aircraft. Replaces shipboard parameters with a 12-bit altitude field ($0$ to $4{,}094	ext{ m}$; $4{,}095$ = not available), high-speed velocity ($0$ to $1{,}022	ext{ kn}$ in integer increments), and an altitude sensor origin flag ($0$ = GNSS, $1$ = barometric).
- **Message 15 (Interrogation):** Polling mechanism allowing base stations or mobile units to interrogate up to two target stations for specific message responses.
- **Message 16 (Assigned Mode Command):** Enables coastal authorities to assign specific transmission channels, slot offsets, and reporting intervals to up to two mobile stations.
- **Message 17 (DGNSS Broadcast Binary Message):** Broadcast by base stations connected to reference stations, transmitting differential pseudo-range corrections to enhance mobile GNSS navigation.
- **Message 20 (Data Link Management):** Base stations pre-announce reserved FATDMA slot allocations across future frames, warning mobile units not to schedule autonomous transmissions in those slots.
- **Message 22 (Channel Management):** Instructs transponders to shift operating frequencies, bandwidths (12.5 kHz vs. 25 kHz), and transmit power levels across defined geographic bounding boxes or via addressed commands.
- **Message 23 (Group Assignment Command):** Base stations broadcast operational parameters (quiet intervals, reporting cadences, station types) to targeted vessel groups within defined geographic areas.

## 22.8 The Class B family (Messages 18, 19, 24A, 24B)

To encourage universal AIS adoption across commercial fishing boats, recreational yachts, and small craft without congesting commercial Class A slot maps, regulatory bodies created the **Class B** transponder family.

```
+------------+-------------+-------+------------------------------------------+
| Message ID | Designation | Slots | Operational Mechanics                    |
+------------+-------------+-------+------------------------------------------+
| 18         | Standard B  | 1     | Dynamic position report (SOTDMA & CS)    |
| 19         | Extended B  | 2     | Position + static details (Deprecated)   |
| 24 Part A  | Static A    | 1     | Vessel name binding to MMSI (any station)|
| 24 Part B  | Static B    | 1     | Ship type, vendor ID, call sign, dims    |
+------------+-------------+-------+------------------------------------------+
```

### Message 18 (Standard Class B Position Report)
Message 18 spans 168 bits, delivering high-resolution dynamic reports. It includes true heading, course, speed, and positioning flags, but introduces hardware capability bits:
- **Class B Unit Flag (bit 141):** `0` = Class B SOTDMA unit; `1` = Class B Carrier Sense (CS) unit.
- **Class B Display Flag (bit 142):** Indicates whether the transponder is attached to an integrated navigation screen.
- **Class B DSC Flag (bit 143):** Indicates whether the unit incorporates a Digital Selective Calling receiver.
- **Class B Message 22 Flag (bit 145):** Indicates whether the unit can execute regional frequency switches via Message 22.

A critical signature arises within the 19-bit **Communication State** field (bits 149–167). When broadcast by a Carrier-Sense transponder (which does not participate in SOTDMA slot reservations), the communication state selector is set to `1`, and the remaining 19 bits are filled with a permanent, hard-coded bit pattern:

$$	ext{CommState}_{	ext{CS}} = 	exttt{1100000000000000110}_2 = 393{,}222_{10}$$

Decoding engines encounter this exact number in hundreds of millions of Class B transmissions; it is an invariant hardware signature confirming CS carrier-sense operation.

### Message 19 deprecation and the Message 24 split
Message 19 was introduced as an early 2-slot Class B position report that combined dynamic coordinates with static vessel names and dimensions. However, reserving two contiguous slots under CS access caused high packet loss in congested waters. Consequently, ITU-R M.1371-6 formally deprecated Message 19, stating that it "is not needed and should not be used" in modern equipment.

To eliminate two-slot Class B overhead, static data was decoupled into **Message 24**, split into two independent 1-slot broadcasts transmitted every 6 minutes:
- **Message 24 Part A (160 bits):** Contains the transmitting MMSI, part number (`0`), and 120 bits of vessel name (20 characters in 6-bit ASCII). Standard A7-3.22 allows any maritime station to broadcast Part A to bind a name to an identity.
- **Message 24 Part B (168 bits):** Contains part number (`1`), ship type (8 bits), vendor ID (42 bits, divided into a 3-character NMEA manufacturer code, unit model code, and serial number), radio call sign (42 bits), and dimensional reference offsets (30 bits).

In ITU-R M.1371-6 Table 77, bits 166–167 of Message 24B (formerly spare) were formally allocated to define **VDES Capabilities**:
- `0`: Standard AIS only
- `1`: Capable of VDES ASM operation
- `2`: Capable of VDES ASM and terrestrial VDE (VDE-TER)
- `3`: Capable of VDES ASM, VDE-TER, and satellite VDE (VDE-SAT)

## 22.9 Aids to Navigation and long-range reporting (Messages 21, 27, 28)

Fixed and floating aids to navigation, hazard markers, and open-ocean tracking require specialized message designs.

### Message 21 (Aids to Navigation Report)
Message 21 is a 2-slot broadcast spanning 272 to 360 bits, transmitted every 3 minutes by physical or synthetic Aids to Navigation (**AtoN**):
- **AtoN Type (5 bits):** Categorizes 32 standardized aid types defined in Table 72 (e.g., cardinal beacons, port/starboard lateral buoys, isolated danger marks, RACON installations, and offshore wind turbines).
- **AtoN Name (120 bits):** Up to 20 characters of base identification.
- **Name Extension (0 to 84 bits):** Optional additional text in increments of 6 bits, allowing long administrative buoy titles without requiring extra packets.
- **Off-Position Indicator (1 bit):** Transmitted as `1` when a floating buoy drags its mooring outside its designated watch circle. For fixed AtoN stations, transmitting `1` indicates an internal GNSS hardware anomaly.
- **Virtual AtoN Flag (1 bit):** Set to `0` when a physical navigation aid exists at the coordinate; set to `1` for synthetic or **Virtual AtoN** markers projected entirely via RF broadcast onto ECDIS displays where no physical marker exists.

### Message 28 (Single-Slot Aid to Navigation Report)
Because Message 21 consumes two full TDMA slots, coastal authorities operating dense networks of virtual AtoNs risked saturating local slot capacity. Introduced in ITU-R M.1371-6, **Message 28** provides a compressed, single-slot (168-bit) AtoN report. It replaces free-text name fields with an authoritative 32-bit Maritime Resource Name (**MRN**) integer identifier and incorporates a cryptographic **Authentication Flag** aligned with IALA Guideline G1192.

### Message 27 (Long-Range Automatic Identification Broadcast)
Standard AIS position reports (Message 1) consume 168 bits, exceeding the link budget and Doppler tolerance of low-bandwidth satellite receivers and dedicated long-range VHF channels ([Chapter 39](ch39-satellite-ais.md)).

Standardized in M.1371-4, **Message 27** compresses vessel navigation state into a compact **96-bit** frame:
1. **Message ID (6 bits):** Constant 27.
2. **Repeat Indicator (2 bits):** Invariant value `3` ("do not repeat").
3. **Source MMSI (30 bits):** Standard identity.
4. **Position Accuracy (1 bit) and RAIM (1 bit):** Positioning health.
5. **Navigational Status (4 bits):** Standard status codes.
6. **Longitude (18 bits) and Latitude (17 bits):** Compressed geographic coordinates scaled in units of **$1/10$ minute of arc** ($1/600$ degree, yielding approximately $185.2	ext{ m}$ resolution). Sentinels are `0x1A838` ($181^\circ$) and `0xD548` ($91^\circ$).
7. **Speed Over Ground (6 bits):** Unsigned integer in whole knots ($0$ to $62	ext{ kn}$; $62$ indicates $\ge62	ext{ kn}$; $63$ = not available).
8. **Course Over Ground (9 bits):** Unsigned integer in whole degrees ($0^\circ$ to $359^\circ$; $511$ = not available).
9. **GNSS / Position Latency (1 bit):** `0` = latency $<5	ext{ s}$; `1` = latency $\ge5	ext{ s}$ (default).
10. **Spare (1 bit):** Reserved.

Crucially, **Message 27 contains no internal timestamp**. Transmitting transponders omit clock fields to conserve bits; receiving satellite constellations and terrestrial base stations are required to attach the UTC receive timestamp upon packet capture.

## Then & now

- ⟨H⟩ **1998 (ITU-R M.1371-0):** The initial message catalog established Messages 1 through 19, standardizing Class A SOTDMA position reports, Message 5 static announcements, and basic addressed binary messaging.
- ⟨H⟩ **2001 (ITU-R M.1371-1):** Refined Class A slot allocation rules and formal timing states; added base station inquiry messages.
- ⟨+⟩ **2006 (ITU-R M.1371-2 & IEC 62287-1):** Standardized the Class B family, establishing Carrier-Sense TDMA (CSTDMA), Message 18, and the split Message 24A/24B structure to protect Class A slot maps.
- ⟨+⟩ **2010 (ITU-R M.1371-4):** Introduced Message 27 for low-bandwidth satellite uplinks; added compact binary containers (Messages 25 and 26); expanded navigation status code 14 for AIS-SART search devices.
- ⟨+⟩ **2014 (ITU-R M.1371-5):** Annex 8 consolidated the classic 27-message catalog, standardizing multi-slot ASM structures and EPFD receiver codes.
- ⟨+⟩ **2026 (ITU-R M.1371-6):** Formally introduced the single-slot AtoN (Message 28), deprecated Message 19, defined VDES capability bits in Message 24B, populated ship-type codes 1–19 and specialized commercial categories in Table 51, and reserved message IDs 60–63 for autonomous maritime radio devices under ITU-R M.2135.

## On the wire

To observe how message bits transition from raw RF bursts into ASCII encapsulation, we examine a real Class A position report recorded from coastal waters:

```text
!AIVDM,1,1,,A,15RTgt0PAso;90TKcjM8h6g208CQ,0*4A
```

This sentence represents a single-packet (`1,1`), unsequenced (empty sequential ID), Channel A transmission carrying 28 armored ASCII characters with 0 fill bits and checksum `*4A`.

```
Armored ASCII string:  1  5  R  T  g  t  0  P  A  s  o  ;  9  0  T  K  c  j  M  8  h  6  g  2  0  8  C  Q
```

Converting each ASCII character to its 6-bit numeric value via the NMEA armoring rule ($c - 48$, subtracting an additional 8 if result $> 40$) recovers the exact 168-bit binary payload:

```
Char '1' -> ord 49 - 48 = 1  -> 000001
Char '5' -> ord 53 - 48 = 5  -> 000101
Char 'R' -> ord 82 - 56 = 26 -> 011010
...
Full Bitstream (168 bits):
000001 00 010110001010010010111111110000 0000 10000001 0001111011 1
1011100101100100100000010010 001101110101111001001110100
100011000000 011010111 100001 00 000 0 00 010 00010011100001
```

> **On the wire.** Deconstructing the 168-bit binary payload by field:
> - **Bits [0:6] (6b):** `000001` $\implies$ Message ID = **1** (Class A SOTDMA Position Report).
> - **Bits [6:8] (2b):** `00` $\implies$ Repeat Indicator = **0** (original transmission).
> - **Bits [8:38] (30b):** `010110001010010010111111110000` $\implies$ MMSI = **371798000** (Panama-flagged merchant vessel).
> - **Bits [38:42] (4b):** `0000` $\implies$ Navigational Status = **0** (under way using engine).
> - **Bits [42:50] (8b):** `10000001` $\implies$ Rate of Turn = **$-127$** (two's complement signed: turning left at $>5^\circ/30	ext{ s}$, no TI).
> - **Bits [50:60] (10b):** `0001111011` $\implies$ Speed Over Ground = $123 	imes 0.1 = \mathbf{12.3	ext{ kn}}$.
> - **Bits [60:61] (1b):** `1` $\implies$ Position Accuracy = **1** (high accuracy, $\le10	ext{ m}$).
> - **Bits [61:89] (28b):** `1011100101100100100000010010` $\implies$ Longitude: two's complement integer $-74{,}037{,}230$. Dividing by $600{,}000$ yields $\mathbf{-123.395383^\circ}$ ($123^\circ 23.723'	ext{ W}$).
> - **Bits [89:116] (27b):** `001101110101111001001110100` $\implies$ Latitude: positive integer $+29{,}028{,}980$. Dividing by $600{,}000$ yields $\mathbf{+48.381633^\circ}$ ($48^\circ 22.898'	ext{ N}$).
> - **Bits [116:128] (12b):** `100011000000` $\implies$ Course Over Ground = $2{,}240 	imes 0.1 = \mathbf{224.0^\circ}$.
> - **Bits [128:137] (9b):** `011010111` $\implies$ True Heading = $\mathbf{215^\circ}$.
> - **Bits [137:143] (6b):** `100001` $\implies$ Timestamp = $\mathbf{33	ext{ s}}$ past the minute.
> - **Bits [143:145] (2b):** `00` $\implies$ Special Manoeuvre = **0** (not available).
> - **Bits [145:148] (3b):** `000` $\implies$ Spare bits = **0**.
> - **Bits [148:149] (1b):** `0` $\implies$ RAIM flag = **False** (RAIM not in use).
> - **Bits [149:151] (2b):** `00` $\implies$ Sync State = **0** (UTC direct clock synchronization).
> - **Bits [151:154] (3b):** `010` $\implies$ Slot Timeout = **2** (re-evaluate candidate slots in 2 frames).
> - **Bits [154:168] (14b):** `00010011100001` $\implies$ Sub-message = **$1{,}249$** (with timeout 2, defines the reserved slot number).

## Validation, uncertainty & data quality

Errors within decoded AIS streams originate from three distinct sources: sensor inaccuracies, operator misconfiguration at the shipboard Minimum Keyboard and Display (**MKD**), and parser corruption within ingestion pipelines.

### Kinematic sanity and sentinel leakage
The most prevalent software flaw in maritime analytics is **sentinel leakage**—treating unpopulated or error-flag values as genuine physical measurements:
- **Heading 511:** When a gyrocompass interface fails or is disconnected, transponders broadcast heading 511. Naive averaging of headings in a coastal basin produces massive artificial clusters around true north-northeast.
- **SOG 102.3 and COG 360.0:** Default sentinels must be mapped to `NULL` or discarded before performing trajectory dead reckoning or hydrodynamic drag computations.
- **ROT $\pm127$ and $-128$:** As proven in §22.3, treating $-127$ or $-128$ as mathematical degrees per minute causes vessels to appear to execute impossible $720^\circ/	ext{min}$ pirouettes.

```python
def clean_kinematics(raw_sog, raw_cog, raw_hdg, raw_rot):
    sog = None if raw_sog >= 1023 else min(raw_sog * 0.1, 102.2)
    cog = None if raw_cog >= 3600 else (raw_cog * 0.1)
    hdg = None if raw_hdg >= 511 else float(raw_hdg)
    
    if raw_rot == -128:
        rot = None
    elif abs(raw_rot) == 127:
        rot = "turning_indicator_unavailable"
    else:
        sign = 1.0 if raw_rot >= 0 else -1.0
        rot = sign * ((abs(raw_rot) / 4.733) ** 2)
        
    return sog, cog, hdg, rot
```

### Static parameter misconfiguration
Unlike dynamic GPS coordinates which flow automatically from internal sensors, static parameters in Message 5 are manually typed by shipboard operators:
- **Default Dimensions ($A=B=C=D=0$):** Studies across commercial shipping archives indicate that over $6\%$ of active merchant vessels broadcast zero dimensions, while another $3\%$ invert bow and stern offsets ($A < B$ on large container vessels where the bridge sits aft).
- **Draught Outliers:** Draught is encoded in units of $0.1	ext{ m}$. Operators frequently enter values in centimeters without scaling, resulting in small coasters claiming static draughts of $25.5	ext{ m}$ (the saturation maximum).
- **ETA Incoherence:** Transmitting month 0 or day 0 indicates an unconfigured voyage plan. Ingestion engines must cross-reference ETA timestamps against the receiver log timestamp to detect vessels broadcasting arrival dates months in the past.

> **Try it.** You can verify the multi-decoder test corpus locally. Activate the repository environment and execute the decoder comparison script against the synthetic harbor dataset:
>
> ```bash
> . .venv/bin/activate
> python code/decode/compare_decoders.py data/samples/synthetic_harbor.nmea
> ```
>
> Expected terminal output:
> ```text
> 2019 sentences
> pyais      decoded 1986 messages by type {1: 1130, 4: 361, 5: 33, 18: 361, 21: 41, 24: 60}
> libais     decoded 1953 messages by type {1: 1130, 4: 361, 18: 361, 21: 41, 24: 60}
> gpsdecode  not available
> ```
> Notice that `libais` discards multi-sentence Message 5 frames because `compare_decoders.py` feeds raw single-sentence streams without an external NMEA assembly state machine, whereas `pyais` handles multi-sentence buffering natively.

## Software

**Open source:**
- `pyais` (Python): Pure-Python library supporting complete decoding and encoding for Messages 1–28, including multi-sentence encapsulation and complex ASM payloads. Caveat: Pure-Python execution speed is slower when processing multi-gigabyte historical archive logs.
- `libais` (C++ with Python bindings): High-throughput C++ decoding library created by Kurt Schwehr. Caveat: Does not assemble multi-sentence NMEA strings automatically; does not support Message 28 in release 0.17.
- `gpsd` (C): Production-grade system daemon providing GPS and AIS decoding, exposing structured JSON interfaces over network sockets. Caveat: Output JSON abstractions occasionally collapse raw protocol sentinels into missing fields.
- `AIS-catcher` (C++): Fast software-defined radio receiver and message demodulator supporting RTL-SDR, Airspy, and HackRF hardware. Caveat: Advanced DSP filtering options require careful tuning to prevent dropped packets on low-power single-board computers.

**Free but closed:**
- `ShipPlotter` (Windows): Widely deployed legacy software for decoding and plotting marine traffic from audio or serial interfaces. Caveat: Proprietary license; lacks automated headless Linux server support.

**Commercial:**
- `Transas Navi-Sailor / Wärtsilä ECDIS`: Type-approved marine navigation software providing real-time target symbology and collision alerts. Caveat: Expensive proprietary marine hardware with closed software interfaces.
- `Astra Paging VTS`: Commercial coastal vessel traffic management platform. Caveat: Requires expensive enterprise server licenses and proprietary client software.

## Standards & guides

- **Recommendation ITU-R M.1371-6** (2026): *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*. The authoritative technical standard governing physical RF modulation, link-layer TDMA framing, and the complete bit-level message catalog (Messages 1–28).
- **Recommendation ITU-R M.1371-5** (2014): Preceding edition defining the classic 27-message catalog and Annex 8 message specifications.
- **Recommendation ITU-R M.585-10** (2026): *Assignment and use of identities in the maritime mobile service*. Governs allocation of 9-digit MMSIs and craft identification formats.
- **Recommendation ITU-R M.2135-1** (2019): *Technical characteristics of autonomous maritime radio devices operating in the frequency band 156–162.05 MHz*. Governs AMRD devices utilizing message IDs 60–63.
- **IMO Resolution MSC.74(69), Annex 3** (1998): *Recommendation on Performance Standards for an Universal Shipborne Automatic Identification System (AIS)*. Mandates international operational requirements.
- **IMO Resolution A.1117(30)** (2017): *IMO Ship Identification Number Scheme*. Defines the official 7-digit identification scheme for commercial vessels.
- **IMO SN/Circ.244** (2004): *Guidance on the Use of the UN/LOCODE in the Destination Field in AIS Messages*.
- **IMO SN.1/Circ.289** (2010): *Guidance on the Use of AIS Application-Specific Messages*. Defines standard DAC and FI payload structures for Messages 6 and 8.
- **IEC 61993-2:2018 (Edition 3.0)**: *Class A shipborne equipment of the automatic identification system (AIS) — Operational and performance requirements, methods of test and required test results*.
- **IEC 62287-1:2017 (Edition 3.0)**: *Class B shipborne equipment — Carrier-sense time division multiple access (CSTDMA)*.
- **IEC 62287-2:2017 (Edition 2.0)**: *Class B shipborne equipment — Self-organising time division multiple access (SOTDMA)*.
- **IEC 62320-1:2015 (Edition 2.0)**: *AIS Base Stations — Minimum operational and performance requirements*.
- **IEC 62320-2:2016 (Edition 2.0)**: *AIS AtoN Stations — Operational and performance requirements*.
- **IALA Recommendation R0126 (formerly A-126)** (2019): *The Use of the Automatic Identification System (AIS) in Marine Aids to Navigation Services*.

## Pitfalls

- **Squaring ROT sentinels:** Treating raw values $\pm127$ or $-128$ as mathematical numbers and applying the inverse formula $(|	ext{ROT}|/4.733)^2 \implies$ generates wild, physically impossible rotational velocities exceeding $700^\circ/	ext{min}$.
- **Assuming Message 27 carries a timestamp:** Expecting an internal time-of-fix field in long-range satellite frames $\implies$ Message 27 omits clock fields entirely; downstream parsers must use receiver arrival timestamps.
- **Collapsing ETA sentinels into invalid dates:** Treating month 0 or day 0 as January 1st $\implies$ produces corrupted voyage timelines; each sub-field must be validated independently.
- **Discarding Message 24A before Part B arrives:** Discarding single fragments because they lack complete static vessel records $\implies$ drops vessel names when Part B is lost to RF packet collisions.
- **Treating heading 511 as true north:** Failing to filter heading sentinel 511 $\implies$ distorts navigational alignment and polar distribution plots.
- **Misinterpreting Carrier-Sense comm state:** Flagging Class B CS units as malfunctioning because their communication state evaluates to constant $393{,}222$ $\implies$ this is the mandatory standard fill pattern for non-SOTDMA devices.
- **Ignoring 1/10-minute coordinate scaling:** Decoding Message 27 or Message 22 positions with the $1/10{,}000$-minute divisor used for Message 1 $\implies$ places vessels $1{,}000	imes$ farther from the equator or prime meridian than their true location.
- **Truncating trailing 6-bit ASCII `@` characters incorrectly:** Stripping `@` characters from middle positions of names $\implies$ corrupts valid commercial identities containing legitimate `@` symbols.
- **Failing to check repeat indicator in Message 27:** Expecting Message 27 repeat counts to increment $\implies$ standard M.1371 requires repeat indicator to remain permanently fixed at 3.
- **Assuming SOG 102.2 represents maximum vessel speed:** High-speed military craft and hovercraft exceed $102.2	ext{ kn}$ $\implies$ any physical speed at or above $102.2	ext{ kn}$ saturates at the integer value $1{,}022$.

## Key takeaways

- Recommendation ITU-R M.1371 defines the VDL message catalog, providing 28 operational message structures across Class A, Class B, Base Stations, AtoN, and SAR assets.
- Core dynamic reports (Messages 1, 2, 3) deliver 168-bit position fixes using signed two's complement coordinates with $1/10{,}000$-minute resolution ($18.52	ext{ cm}$ at the equator).
- Rate of Turn uses an intentional square-root relationship $	ext{ROT}_{	ext{AIS}} = 	ext{round}(4.733\sqrt{	ext{ROT}_{	ext{sensor}}})$, where $\pm127$ and $-128$ serve as critical non-linear operational sentinels.
- Message 5 spans two TDMA slots ($424	ext{ bits}$), carrying vessel names, IMO numbers, dimensional offsets, and independent four-part ETA fields.
- Class B transponders use Message 18 for dynamic reports and split static data into two single-slot frames (24A and 24B) to minimize slot map disruption.
- Message 27 compresses open-ocean dynamic reports into 96 bits with $1/10$-minute resolution, omitting internal timestamps to maximize satellite link budgets.
- All unused or invalid data fields must be strictly checked against standard sentinel values prior to downstream analysis to prevent severe data corruption.

## References

1. Harati-Mokhtari, A., Wall, A., Brooks, P. & Wang, J. (2007). Automatic Identification System (AIS): Data Reliability and Human Error Implications. *The Journal of Navigation*, 60(3):373–389. doi:10.1017/S037346330700429X.
2. International Association of Marine Aids to Navigation and Lighthouse Authorities (2019). *The Use of the Automatic Identification System (AIS) in Marine Aids to Navigation Services* (IALA Recommendation R0126, Edition 1.5). Saint-Germain-en-Laye: IALA.
3. International Electrotechnical Commission (2015). *Maritime navigation and radiocommunication equipment and systems – Automatic identification systems (AIS) – Part 1: AIS Base Stations – Minimum operational and performance requirements, methods of testing and required test results* (Standard No. IEC 62320-1:2015, Edition 2.0). Geneva: IEC.
4. International Electrotechnical Commission (2016). *Maritime navigation and radiocommunication equipment and systems – Automatic identification systems (AIS) – Part 2: AIS AtoN Stations – Minimum operational and performance requirements, methods of testing and required test results* (Standard No. IEC 62320-2:2016, Edition 2.0). Geneva: IEC.
5. International Electrotechnical Commission (2017). *Maritime navigation and radiocommunication equipment and systems – Class B shipborne equipment of the automatic identification system (AIS) – Part 1: Carrier-sense time division multiple access (CSTDMA) techniques* (Standard No. IEC 62287-1:2017, Edition 3.0). Geneva: IEC.
6. International Electrotechnical Commission (2017). *Maritime navigation and radiocommunication equipment and systems – Class B shipborne equipment of the automatic identification system (AIS) – Part 2: Self-organising time division multiple access (SOTDMA) techniques* (Standard No. IEC 62287-2:2017, Edition 2.0). Geneva: IEC.
7. International Electrotechnical Commission (2018). *Maritime navigation and radiocommunication equipment and systems – Automatic Identification Systems (AIS) – Part 2: Class A shipborne equipment of the automatic identification system (AIS) – Operational and performance requirements, methods of test and required test results* (Standard No. IEC 61993-2:2018, Edition 3.0). Geneva: IEC.
8. International Maritime Organization (1998). *Recommendation on Performance Standards for an Universal Shipborne Automatic Identification System (AIS)* (Resolution MSC.74(69), Annex 3). Adopted 12 May 1998. London: IMO.
9. International Maritime Organization (2004). *Guidance on the Use of the UN/LOCODE in the Destination Field in AIS Messages* (SN/Circ.244). London: IMO.
10. International Maritime Organization (2010). *Guidance on the Use of AIS Application-Specific Messages* (SN.1/Circ.289). London: IMO.
11. International Maritime Organization (2017). *IMO Ship Identification Number Scheme* (Resolution A.1117(30)). Adopted 6 December 2017. London: IMO.
12. International Telecommunication Union (2001). *Technical characteristics for a universal shipborne automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-1). Geneva: ITU Radiocommunication Sector.
13. International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-5). Geneva: ITU Radiocommunication Sector.
14. International Telecommunication Union (2019). *Technical characteristics of autonomous maritime radio devices operating in the frequency band 156–162.05 MHz* (Recommendation ITU-R M.2135-1). Geneva: ITU Radiocommunication Sector.
15. International Telecommunication Union (2026). *Assignment and use of identities in the maritime mobile service* (Recommendation ITU-R M.585-10). Geneva: ITU Radiocommunication Sector.
16. International Telecommunication Union (2026). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-6). Geneva: ITU Radiocommunication Sector.
17. Raymond, E. S. & Schwehr, K. (2023). *AIVDM/AIVDO Protocol Decoding* (Version 1.58). GPSD Project. https://gpsd.gitlab.io/gpsd/AIVDM.html.
