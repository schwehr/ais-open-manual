# Chapter 26 — Interfaces and logging: NMEA 0183, TAG blocks, IEC 61162-450, NMEA 2000

> **Part IV — The system: architecture and protocol.** How AIS data exits transponders and receivers, traverses shipboard serial lines, Ethernet networks, and CAN buses, and enters forensic and archival logs.

**In this chapter.** You will learn how raw AIS radio bursts are transformed into standard digital data streams and captured across shipboard, coastal, and cloud logging architectures. We dissect the encapsulation protocol that carries the vast majority of terrestrial AIS data: NMEA 0183 and IEC 61162-1 serial sentences (`!AIVDM` and `!AIVDO`), their 6-bit ASCII payload armoring, fill-bit mechanics, and checksum verification. You will inspect the presentation-interface sentences used to interrogate transponders and broadcast binary payloads, and master the NMEA 4.10 and IEC 62320-1 TAG block metadata format that attaches station provenance and reception timestamps to raw sentences. We examine shipboard network encapsulation over Ethernet via IEC 61162-450 Lightweight Ethernet and IEC 61162-460 security gateways, as well as marine CAN-bus networks via NMEA 2000 Parameter Group Numbers (PGNs). Finally, we compare real-world archival formats, demonstrate multi-sentence reassembly pitfalls, and establish robust logging best practices.

## 26.1 The presentation interface and serial encapsulation

When an Automatic Identification System (**AIS**) transponder demodulates a Gaussian Minimum Shift Keying (**GMSK**) burst from the VHF data link (**VDL**), it strips the radio training sequence, frame start flags, and High-Level Data Link Control (**HDLC**) zero-bit stuffing, and validates the 16-bit Frame Check Sequence (**FCS**) CRC (see [Chapter 28](ch28-rf-encoding-physical-layer.md)). The resulting binary payload cannot be placed directly onto traditional shipboard serial links or navigation displays without encapsulation. Marine electronics interoperability relies on standard character-framed interfaces defined by the National Marine Electronics Association (**NMEA**) and the International Electrotechnical Commission (**IEC**).

The bridge between radio reception and shipboard consumers is known as the **Presentation Interface** (**PI**). Governed by IEC 61162-1 (and high-speed IEC 61162-2), and harmonized with NMEA 0183, the PI defines how navigation sensors—including the AIS transponder, gyrocompass, Electronic Position Fixing System (**EPFS**), and speed log—exchange data with shipboard consumers such as the Electronic Chart Display and Information System (**ECDIS**), radar, and Voyage Data Recorder (**VDR**).

```
+-------------------------------------------------------------------------+
|                  VHF Data Link (VDL) 161.975 / 162.025 MHz              |
+-------------------------------------------------------------------------+
                                    |
                                    v
+-------------------------------------------------------------------------+
|                         AIS Physical / MAC Layer                        |
|  - GMSK Demodulation (9600 bit/s)                                       |
|  - HDLC Destuffing & CRC-16 Verification                                |
+-------------------------------------------------------------------------+
                                    |
                                    v  Unpacked radio bit payload (e.g. 168 bits)
+-------------------------------------------------------------------------+
|                       Presentation Interface (PI)                       |
|  - 6-Bit ASCII Armoring                                                 |
|  - Sentence Fragmentation (max 82-byte NMEA boundary)                   |
|  - Encapsulation (!AIVDM / !AIVDO Formatter, Channel, Fill Bits)        |
+-------------------------------------------------------------------------+
         |                                |                       |
         v                                v                       v
+------------------+            +-------------------+   +--------------------+
| IEC 61162-1/-2   |            | IEC 61162-450     |   | NMEA 2000 (CAN)    |
| Point-to-point   |            | Lightweight       |   | ISO 11783 / J1939  |
| RS-422 Serial    |            | Ethernet (LWE)    |   | Fast Packet PGNs   |
| 38,400 baud      |            | UDP Multicast     |   | 250 kbit/s         |
+------------------+            +-------------------+   +--------------------+
         |                                |                       |
         v                                v                       v
+-------------------------------------------------------------------------+
|                       Consumers & Archival Logging                      |
|  - Bridge Displays (ECDIS, Radar Target Tracking, PPU)                  |
|  - Voyage Data Recorders (VDR / S-VDR)                                  |
|  - Coastal Networks (USCG NAIS, Kystverket, Digitraffic)                |
|  - Cloud Aggregators & Data Warehouses (Parquet, BigQuery)              |
+-------------------------------------------------------------------------+
```

Historically, NMEA 0183 specified point-to-point differential serial communications over EIA/RS-422 at 4,800 baud (8-N-1), delivering approximately 480 characters per second. In congested waterways where vessels broadcast position reports every two seconds and static voyage data every six minutes, an AIS transponder receiving bursts on both AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz) can experience peaks exceeding 30 to 40 packets per second. A 4,800-baud line rapidly saturates, dropping buffer queues.

Consequently, IEC PAS 61162-100 (in 2002) and subsequent editions of IEC 61162-1 and NMEA 0183 (specifically Appendix NMEA 0183-HS) mandated a transmission speed of **38,400 baud** for dedicated AIS presentation interfaces (IEC 61162-2 defines high-speed physical layer links operating at 38,400 baud and higher). At 38,400 baud, throughput expands to roughly 3,840 bytes per second, comfortably handling congested maritime VHF data link conditions.

## 26.2 `!AIVDM` and `!AIVDO` sentence anatomy

The primary sentences emitted by an AIS transponder or receiver are encapsulated under the `!AIVDM` and `!AIVDO` formatters:
- `!AIVDM` (**VHF Data-link Message**): Carries packets received over the radio link from *other* stations (ships, base stations, aids to navigation, SAR aircraft).
- `!AIVDO` (**VHF Data-link Own-vessel message**): Carries data transmitted, or queued for transmission, by *own ship's* transponder, allowing bridge displays and VDRs to monitor own-ship transmissions.

NMEA 0183 sentences conventionally start with a dollar sign (`$`). However, sentences encapsulating raw binary payloads into printable ASCII text use an exclamation mark (`!`) as the delimiter.

### 26.2.1 Sentence field structure

Every `!AIVDM` and `!AIVDO` sentence follows a comma-delimited structure ending with an asterisk, a two-digit hexadecimal checksum, and carriage return/line feed (`<CR><LF>`):

```
!AIVDM,count,frag,seq,channel,payload,fill*hh<CR><LF>
```

Consider the following single-sentence Class A position report (Message 1) recorded from coastal traffic:

```
!AIVDM,1,1,,B,177KQJ5000G?tO`K>RA1wUbN0TKH,0*5C
```

Breaking down each field in sequence:
1. `!AIVDM`: **Sentence Formatter and Talker Identifier.** Delimiter `!`, talker mnemonic `AI` (Automatic Identification System mobile station), and formatter mnemonic `VDM` (VHF Data-link Message).
2. `1`: **Total Sentence Count.** Total number of sentence fragments required to deliver the message payload (1 to 9).
3. `1`: **Sentence Fragment Number.** Sequence index of this fragment within the multi-sentence message (1 to `count`).
4. *(empty)*: **Sequential Message Identifier.** Sequential integer (`0` to `9`) linking multi-sentence fragments together. Empty for single-sentence messages.
5. `B`: **Radio Channel.** VHF data link channel: `A` represents AIS Channel 1 (161.975 MHz) and `B` represents AIS Channel 2 (162.025 MHz). Non-standard receivers sometimes emit `1` or `2`.
6. `177KQJ5000G?tO`K>RA1wUbN0TKH`: **6-Bit Armored Payload.** Radio payload converted into printable ASCII characters. Here, 28 armored characters encode 168 radio bits.
7. `0`: **Fill Bits (Padding).** Number of pad bits ($0 \dots 5$) appended to round the payload bit count up to a multiple of 6.
8. `*5C`: **Checksum Field.** Asterisk delimiter `*` followed by a two-character uppercase hexadecimal checksum (`5C`).

### 26.2.2 The NMEA checksum algorithm

The checksum in all NMEA 0183 sentences, including `!AIVDM`, is an 8-bit exclusive OR (**XOR**) of all characters between—but excluding—the leading delimiter (`!` or `$`) and the terminating asterisk (`*`).

Let $C$ represent the accumulated checksum byte, initialized to zero:
$$C = \bigoplus_{i=1}^{m} \text{ord}(s_i)$$
where $s_i$ is the $i$-th ASCII character in the substring. The result is formatted as a two-character zero-padded uppercase hexadecimal string.

```python
def nmea_checksum(sentence: str) -> str:
    content = sentence.lstrip("!$").split("*")[0]
    c = 0
    for char in content:
        c ^= ord(char)
    return f"{c:02X}"
```

For the example string `AIVDM,1,1,,B,177KQJ5000G?tO`K>RA1wUbN0TKH,0`, accumulating the XOR across character bytes yields `0x5C`. If a parser detects a mismatch against the transmitted `*hh`, the line suffered serial bit corruption and must be discarded.

### 26.2.3 Talker identifiers

While `AI` is the standard talker mnemonic for mobile transceivers, NMEA 0183 and IEC 61162-1 define prefixes identifying the originating station class (Raymond & Schwehr 2023):

| Talker ID | Originating Station Type | Standard / Status |
|:---|:---|:---|
| `AI` | Mobile AIS station (shipborne Class A or Class B) | Universal standard |
| `AB` | Base AIS station (shore-based AIS base station) | NMEA 4.00+ |
| `AD` | Dependent AIS base station | NMEA 4.00+ |
| `AN` | Aid to Navigation AIS station (physical or virtual AtoN) | NMEA 4.00+ |
| `AR` | AIS receiving station (receive-only coastal station) | NMEA 4.00+ |
| `AS` | Limited base station (provisional NMEA talker mnemonic) | NMEA 4.00+ |
| `AT` | AIS transmitting station (transceiver in transmit-directed service) | NMEA 4.00+ |
| `AX` | Repeater AIS station | NMEA 4.00+ |
| `BS` | Base station | Deprecated in NMEA 4.00 (replaced by `AB`) |
| `SA` | Physical shore AIS station (provisional NMEA talker mnemonic) | NMEA 4.00+ |

A common software pitfall in custom ingest engines is hardcoding a check for the literal string `!AIVDM`. When encountering coastal feeds from shore networks or Aids to Navigation, sentences starting with `!ABVDM`, `!ANVDM`, or `!ARVDM` are inadvertently discarded. Robust decoders match regex `^![A-Z]{2}VD[MO]`.

## 26.3 6-bit ASCII payload armoring and fill-bit mechanics

Radio data packets defined in ITU-R M.1371 consist of variable-length bit strings. Because serial lines historically reserved control codes (such as ASCII NUL, LF, CR, and commas), binary AIS data is encoded into printable ASCII characters.

### 26.3.1 The 6-bit armoring algorithm

The armoring algorithm packs six binary bits into a single printable ASCII character. The conversion maps a 6-bit integer $v \in [0, 63]$ to an ASCII character code $A$ according to the following transformation (IEC PAS 61162-100, Raymond & Schwehr 2023):

$$A = \begin{cases} 
v + 48 & \text{if } 0 \le v \le 39 \\
v + 56 & \text{if } 40 \le v \le 63 
\end{cases}$$

Conversely, to extract the 6-bit integer value $v$ from an armored ASCII character byte $A$:

$$v = \begin{cases} 
A - 48 & \text{if } A - 48 \le 40 \\
A - 56 & \text{if } A - 48 > 40 
\end{cases}$$

The character translation operates across two distinct contiguous ASCII segments:
1. **Values 0 through 39:** Mapped to ASCII 48 (`0`) through 87 (`W`), covering digits `0`–`9` (values 0–9), punctuation `:` through `?` (values 10–15), and uppercase letters `@` through `W` (values 16–39).
2. **Values 40 through 63:** Mapped to ASCII 96 (backtick `` ` ``) through 119 (`w`), covering grave accent `` ` `` (value 40) and lowercase letters `a` through `w` (values 41–63).

```
   6-Bit Value Range:  0 ------------ 39 | 40 ------------ 63
                       |                | |                 |
                       + 48             | + 56              |
                       v                v v                 v
      ASCII Character: '0' ----------- 'W' '`' ----------- 'w'
      ASCII Byte:      48 ------------- 87 96 ------------ 119
                                           ^
                                           | Unused Gap: ASCII 88 ('X') - 95 ('_')
```

ASCII values 88 (`X`) through 95 (`_`) are unused in 6-bit armoring. The character `w` (ASCII 119) is the maximum possible armored character (value 63). If a parser encounters characters outside the union of ranges `[0-W]` and ``[`-w]`` in field 5, the line is malformed.

### 26.3.2 Fill bits and boundary alignment

Because radio packets are structured around protocol fields whose total length is not always a multiple of 6 bits, the final armored character in a transmission may contain unused trailing bits.

The **Fill Bits** field (field 6) indicates how many bits in the final armored character are pad bits that must be ignored when extracting the radio payload.

> **Worked example.** Consider an AIS Message 5 (Class A Static and Voyage Related Data), as defined in ITU-R M.1371. The message specification requires exactly **424 bits**.
> 
> 1. Compute required 6-bit armored characters:
>    $$\lceil 424 / 6 \rceil = \lceil 70.6667 \rceil = 71 \text{ characters}$$
> 2. The 71 characters provide:
>    $$71 \times 6 = 426 \text{ bits}$$
> 3. The difference yields the fill bit count:
>    $$426 - 424 = 2 \text{ fill bits}$$
> 
> Therefore, the final sentence fragment of a Message 5 must carry a fill bit value of `2`. When decoding the 71st character, the two least significant bits are discarded.

A classic firmware defect occurs when a transponder or multiplexer reports a fill bit value of `0` instead of `2` for a 424-bit Message 5, yielding 426 bits. Decoders that strictly enforce length equality drop the static report. As documented by Raymond & Schwehr (2023), robust decoders must tolerate payloads that exceed theoretical message lengths by up to 5 padding bits, truncating the excess bits rather than aborting.

## 26.4 Multi-sentence message reassembly and hazards

Under NMEA 0183 and IEC 61162-1, no serial sentence may exceed **82 characters** from the initial delimiter to `<CR><LF>` inclusive. Because a single armored character encodes 6 bits, an 82-character sentence can carry at most 60 to 62 payload characters (roughly 360 to 372 bits). Messages exceeding 360 bits—such as a 424-bit Message 5 or multi-slot Application-Specific Messages (Messages 6, 8, 25, 26)—must be split across multiple sentence fragments:

```
!AIVDM,2,1,3,B,55P5TL01VIaAL@7WKO@mBplU@<PDhh000000001S;AJ::4A80?4i@E53,0*3E
!AIVDM,2,2,3,B,1@0000000000000,2*55
```

Here fragment 1 carries 58 characters (348 bits, fill 0), and fragment 2 carries 13 characters (78 bits, fill 2). Combined payload: $58 + 13 = 71$ characters, giving $(71 \times 6) - 2 = 424$ bits.

Reassembling multi-fragment sentences requires maintaining an in-memory reassembly cache. A naive implementation that keys its cache purely on sequential message ID (field 4) fails when multiple coastal receivers feed a shared multiplexer:

```
Multiplexer Input:
Line 1: Receiver North: !AIVDM,2,1,1,A,53n8v6000001... ,0*..  (MMSI 3669001)
Line 2: Receiver South: !AIVDM,2,1,1,B,55?MbV01VI...   ,0*..  (MMSI 2112345)
Line 3: Receiver North: !AIVDM,2,2,1,A,00000000000...  ,2*..  (MMSI 3669001)
Line 4: Receiver South: !AIVDM,2,2,1,B,00000000000...  ,2*..  (MMSI 2112345)
```

If the state machine tracks only sequential ID `1`, Line 2 overwrites fragment 1 from Receiver North. When Line 3 arrives, the decoder splices Receiver South's fragment 1 with Receiver North's fragment 2, corrupting vessel names and IMO numbers.

To prevent buffer cross-contamination, a robust reassembly engine enforces three rules:
1. **Compound Cache Keying:** Key reassembly buffers on `(Source Station ID, Talker ID, Channel, Sequential ID)`.
2. **Sequential Fragment Enforcement:** Enforce ascending order ($1, 2, \dots, n$). If fragment 2 arrives without a matching fragment 1, evict the buffer.
3. **Strict Time-to-Live (TTL):** Transponders transmit sequential fragments back-to-back across serial lines within milliseconds. Expire reassembly buffers if subsequent fragments fail to arrive within 2.0 to 4.0 seconds.

## 26.5 Presentation-interface sentence suite

Beyond `!AIVDM` and `!AIVDO`, IEC 61162-1 and NMEA 0183 define sentences to configure transponders, query internal registers, command frequency handovers, and initiate transmissions.

> **Definitions that bite.** While `!AIVDM` and `!AIVDO` sentences use the exclamation mark delimiter (`!`) to signal encapsulated binary payloads, control and configuration sentences on the Presentation Interface use the standard NMEA dollar sign delimiter (`$`), such as `$AIABM` or `$AIVSD`. Decoders filtering strictly on `!` miss local transponder alarms, static voyage programming, and regional channel operating modes.

```
+-------------------------------------------------------------------------------+
|                       Presentation Interface Sentences                        |
+-------------------------------------------------------------------------------+
| Formatter | Full Standard Mnemonic              | Operational Purpose         |
|:----------|:------------------------------------|:----------------------------|
| ABM       | Addressed Binary Message            | Feed Msg 6 to PI for Tx     |
| BBM       | Broadcast Binary Message            | Feed Msg 8/14 to PI for Tx  |
| ABK       | Addressed Binary Acknowledgement    | Transponder Tx status/ack   |
| ACA       | AIS Regional Channel Assignment     | Query/set channel frequency |
| ACS       | Channel Management Source           | Identifies source of ACA    |
| AIR       | Interrogation Request               | Command Msg 15 inquiry      |
| AIQ       | Query Sentence                      | General register poll       |
| LRF / LRI | Long-Range Function / Interrogation | Satellite/Inmarsat-C poll   |
| SSD       | Ship Static Data                    | Sets vessel name, call sign |
| VSD       | Voyage Static Data                  | Sets draft, destination, ETA|
| TXT       | Text Message                        | Transponder status & alerts |
| ALR       | Alarm State                         | Bridge alert management     |
+-------------------------------------------------------------------------------+
```

The primary control formatters include:
- `ABM` / `BBM`: Transmit addressed binary (Message 6/12) and broadcast binary (Message 8/14/26) payloads.
- `ABK`: Autonomous transponder acknowledgement reporting transmission status of `ABM` or `BBM` requests.
- `ACA` / `ACS`: Inspect and command regional channel allocations and slot assignments via Message 22 (see [Chapter 28](ch28-rf-encoding-physical-layer.md)).
- `AIR`: Command transponder to broadcast Message 15 interrogations targeting other stations.
- `SSD`: Configure vessel callsign, name, hull dimensions, and GNSS antenna offsets.
- `VSD`: Program dynamic voyage parameters: navigational status, draught, hazardous cargo, destination UN/LOCODE, and ETA.

## 26.6 NMEA 4.10 and IEC 62320-1 TAG blocks

A fundamental limitation of traditional NMEA 0183 sentences is their lack of reception metadata. A raw `!AIVDM` sentence records the radio channel and payload, but omits:
- The exact UTC timestamp of radio reception.
- The identity, geographic location, or network IP of the receiving station.
- The signal strength, SNR, or RF slot number.

In 2012, NMEA 0183 Version 4.10 introduced **TAG blocks** (Timed Access Groups), harmonized with IEC 62320-1 base-station comment formatting.

### 26.6.1 TAG block syntax and framing

A TAG block directly precedes the encapsulated NMEA sentence, beginning with a backslash (`\`), containing comma-separated `parameter:value` pairs, and terminating with an asterisk (`*`), a two-character hexadecimal checksum, and a closing backslash (`\`):

```
\parameter:value,parameter:value*hh\!AIVDM,...
```

Consider an authentic coastal station log entry carrying full TAG block metadata:

```
\g:1-2-73874,n:157036,s:r003669945,c:1241544035*4A\!AIVDM,1,1,,B,15N4cJ`005Jrek0H@9n`DW5608EP,0*13
```

The TAG block components:
- `g:1-2-73874`: **Sentence Grouping.** Sentence `1` of a `2`-sentence group with unique group identifier `73874`.
- `n:157036`: **Line Count.** Monotonically increasing line counter incremented by the receiving station to detect serial buffer or socket drops.
- `s:r003669945`: **Source Station ID.** Identifies the receiving coastal station (`r003669945`).
- `c:1241544035`: **Timestamp.** UNIX epoch timestamp marking reception.
- `*4A`: **TAG Block Checksum.** XOR sum of all characters between the delimiters: $\text{XOR}(\text{"g:1-2-73874,n:157036,s:r003669945,c:1241544035"}) = \text{0x4A}$.

### 26.6.2 Standard TAG block keys

NMEA 4.10 and IEC 62320-1 define the following core parameters (Raymond & Schwehr 2023):

| Tag Key | Meaning | Format / Value Constraints | Standard |
|:---|:---|:---|:---|
| `c` | Timestamp (UNIX epoch) | Numeric string; seconds or milliseconds | NMEA 4.10 / IEC 62320-1 |
| `d` | Destination identifier | Alphanumeric string ($\le 15$ characters) | NMEA 4.10 |
| `g` | Sentence grouping | `index-total-groupid` (e.g. `1-2-1044`) | NMEA 4.10 |
| `n` | Line count / sequence number | Monotonically increasing integer | NMEA 4.10 |
| `r` | Relative time | Offset in milliseconds from reference epoch | NMEA 4.10 |
| `s` | Source station identifier | Alphanumeric station ID ($\le 15$ characters) | NMEA 4.10 / IEC 62320-1 |
| `t` | Text string | Free text remark ($\le 15$ characters) | NMEA 4.10 |
| `T` | Human-readable UTC | Non-standard extension (e.g. GFW `YYYY-MM-DD HH.MM.SS`) | In the wild |

> **Definitions that bite.** What unit is stored in `c:`? In NMEA 4.10, `c:` was defined as UNIX epoch time in seconds. Modern high-rate processing pipelines require millisecond resolution. In practice, Global Fishing Watch (**GFW**) and modern SDR decoders emit `c:` in **milliseconds** (e.g., `\c:1599239526500...`), whereas legacy base stations emit `c:` in **seconds** (e.g., `\c:1241544035...`). Ingest parsers must inspect the value magnitude: values greater than $10^{11}$ represent milliseconds; smaller values represent seconds.

## 26.7 Network interfaces: IEC 61162-450 and IEC 61162-460

Integrated bridge systems (**IBS**) have phased out individual RS-422 serial cables in favour of switched Ethernet networks governed by **IEC 61162-450** (*Lightweight Ethernet* or **LWE**; Edition 3.0 published April 2024).

### 26.7.1 Framing and datagram structure

IEC 61162-450 uses UDP multicast over IPv4. Every datagram carrying navigation sentences begins with a mandatory 6-byte header: the ASCII token `UdPbC` followed by a binary NUL byte (`0x00`).

```
+-------------------------------------------------------------------------+
|                  IEC 61162-450 LWE UDP Multicast Datagram               |
+-------------------------------------------------------------------------+
| Byte Offset | Content                  | Value / Description            |
|:------------|:-------------------------|:-------------------------------|
| 0 .. 5      | Header Token             | 'UdPbC\0' (55 64 50 62 43 00)  |
| 6 .. k      | TAG Block                | \s:AI0001,n:48192*hh\          |
| k+1 .. end  | NMEA Sentence(s)         | !AIVDM,1,1,,A,...*hh<CR><LF>   |
+-------------------------------------------------------------------------+
```

Multiple sentences may be packed into a single UDP frame up to 1,472 bytes (avoiding MTU fragmentation). The source station identifier (`s:`) in the TAG block carries the **System Function Identifier** (**SFI**), a standard 6-character code (such as `AI0001` for the ship's primary AIS transponder).

### 26.7.2 Multicast transmission groups

IEC 61162-450 reserves IPv4 multicast groups to segment bridge traffic:

| Group Name | Multicast Address | Port | Data Traffic Description |
|:---|:---|:---|:---|
| `MISC` | `239.192.0.1` | 60001 | Miscellaneous bridge data |
| `TGTD` | `239.192.0.2` | 60002 | Target data: AIS (`!AIVDM`), ARPA radar tracked targets |
| `SATD` | `239.192.0.3` | 60003 | Satellite navigation data (GNSS fixes, RAIM status) |
| `NAVD` | `239.192.0.4` | 60004 | General navigation data (heading, speed log, depth) |
| `VDRD` | `239.192.0.5` | 60005 | Dedicated Voyage Data Recorder input channel |
| `RCOM` | `239.192.0.6` | 60006 | Radiocommunication equipment data |
| `TIME` | `239.192.0.7` | 60007 | Time synchronization messages |

AIS equipment streams to group **`TGTD`** (`239.192.0.2:60002`). ECDIS and radar displays subscribe to this multicast group, receiving real-time targets without serial multiplexers.

### 26.7.3 Cyber security gateways: IEC 61162-460

Because UDP multicast provides zero encryption and zero source authentication, connecting bridge networks to satellite communications terminals exposes navigation displays to packet spoofing.

To mitigate this vulnerability, **IEC 61162-460** (*Safety and security for Ethernet interconnection*; Edition 3.0 released April 2024) specifies mandatory firewall gateways and network isolation routers between the secure navigation bus and insecure external networks. Gateways enforce stateful packet inspection, deep packet inspection of NMEA syntax, multicast flood dampening, and cryptographic audit logging.

## 26.8 CAN-bus integration: NMEA 2000 and PGNs

On pleasure craft and workboats, RS-422 serial wiring has been largely replaced by **NMEA 2000** (harmonized as **IEC 61162-3**). NMEA 2000 uses Controller Area Network (**CAN 2.0B**) at **250 kbit/s**, using SAE J1939 framing and 29-bit CAN identifiers. Instead of ASCII sentences, devices communicate using binary **Parameter Group Numbers** (**PGNs**).

### 26.8.1 The Fast Packet protocol

A standard CAN 2.0B frame carries at most **8 bytes**. Because AIS position reports and static data records exceed 8 bytes (a Class A position report requires 28 bytes; static voyage data requires 76 bytes), NMEA 2000 uses the J1939 **Fast Packet** protocol (up to 223 bytes across sequential frames):
- **Frame 0 (Initial Frame):** Byte 1 carries sequence counter (bits 7–5) and frame index `00000` (bits 4–0). Byte 2 carries total payload byte count. Bytes 3–8 carry the start of the payload.
- **Frames 1 through $N$ (Consecutive Frames):** Byte 1 carries matching sequence counter and incrementing frame index ($1, 2, \dots, N$). Bytes 2–8 carry subsequent payload slices.

### 26.8.2 AIS Parameter Group Numbers (PGNs)

NMEA 2000 specifications are proprietary and copyrighted. The open-source community, through the **canboat** project, reverse-engineered the PGN database by inspecting bus traffic (canboat 2026):

| PGN | Length | Transmission | Description (per canboat) | Underlying AIS Message |
|:---|:---|:---|:---|:---|
| **129038** | 28 B | Fast Packet | AIS Class A Position Report | Messages 1, 2, 3 |
| **129039** | 27 B | Fast Packet | AIS Class B Position Report | Message 18 |
| **129040** | 54 B | Fast Packet | AIS Class B Extended Position Report | Message 19 |
| **129041** | 76 B | Fast Packet | AIS Aids to Navigation (AtoN) Report | Message 21 |
| **129792** | variable | Fast Packet | AIS DGNSS Broadcast Binary Message | Message 17 |
| **129793** | 11 B | Fast Packet | AIS UTC and Date Report | Message 4 |
| **129794** | 76 B | Fast Packet | AIS Class A Static and Voyage Related Data | Message 5 |
| **129795** | variable | Fast Packet | AIS Addressed Binary Message | Message 6 |
| **129796** | 8 B | Single Frame | AIS Acknowledge | Message 7 / 13 |
| **129797** | variable | Fast Packet | AIS Binary Broadcast Message | Message 8 |
| **129798** | 23 B | Fast Packet | AIS SAR Aircraft Position Report | Message 9 |
| **129800** | 8 B | Single Frame | AIS UTC/Date Inquiry | Message 10 |
| **129801** | variable | Fast Packet | AIS Addressed Safety Related Message | Message 12 |
| **129802** | variable | Fast Packet | AIS Safety Related Broadcast Message | Message 14 |
| **129803** | variable | Fast Packet | AIS Interrogation | Message 15 |
| **129804** | variable | Fast Packet | AIS Assignment Mode Command | Message 16 |
| **129805** | variable | Fast Packet | AIS Data Link Management Message | Message 20 |
| **129806** | variable | Fast Packet | AIS Channel Management | Message 22 |
| **129807** | variable | Fast Packet | AIS Class B Group Assignment | Message 23 |
| **129809** | 26 B | Fast Packet | AIS Class B Static Data (Part A - Name) | Message 24 Part A |
| **129810** | 44 B | Fast Packet | AIS Class B Static Data (Part B - Dimensions) | Message 24 Part B |
| **129813** | 16 B | Fast Packet | AIS Long-Range Broadcast Message | Message 27 |

In PGN 129038 (Class A Position Report), Longitude and Latitude are transmitted as 32-bit signed integers in units of $1 \times 10^{-7}$ degrees ($0.0000001^\circ$ precision), while Course Over Ground (**COG**) is stored as a 16-bit unsigned integer in units of $1 \times 10^{-4}$ radians.

### 26.8.3 Next-generation architectures: OneNet and Signal K

To overcome the 250 kbit/s CAN bandwidth limit, NMEA released **OneNet** in November 2020. OneNet is an IPv6-based protocol running over IEEE 802.3 Gigabit Ethernet, encapsulating NMEA 2000 PGNs inside IP datagrams while coexisting with IEC 61162-450 traffic on the same physical infrastructure.

Concurrently, the open-source community developed **Signal K**, a modern JSON-based open data format running over HTTP, WebSockets, and MQTT. Gateways translate incoming NMEA 0183 sentences and NMEA 2000 PGNs into structured Signal K deltas for web applications and mobile devices.

## 26.9 Archival and logging formats in the wild

Because raw serial streams must be stored for incident reconstruction, fisheries surveillance, and maritime analytics, an ecosystem of logging formats has evolved across public agencies and commercial providers.

```
+----------------------------------------------------------------------------------------------------+
|                                     Logging Formats in the Wild                                    |
+----------------------------------------------------------------------------------------------------+
| Format / Pipeline      | Raw Bits Kept? | Station ID? | Recv Time? | SOTDMA Slot? | Format Syntax  |
|:-----------------------|:---------------|:------------|:-----------|:-------------|:---------------|
| NMEA 4.10 TAG Block    | Yes            | Yes (`s:`)  | Yes (`c:`) | No           | ASCII text     |
| USCG Extended AIVDM    | Yes            | Yes (`r:`)  | Yes (epoch)| Yes (`S:`)   | ASCII text     |
| gpsd JSON Stream       | No             | Optional    | Optional   | No           | JSON           |
| Marine Cadastre CSV    | No             | No          | No         | No           | Tabular CSV    |
| DMA Daily CSV          | No             | No          | Base stn   | No           | Tabular CSV    |
| Kystverket TCP Feed    | Yes            | Base stn    | Yes        | No           | IEC 62320-1    |
| Digitraffic MQTT/REST  | No             | No          | Ingest ms  | No           | JSON           |
| GFW BigQuery / Parquet | Synthesized    | Yes         | Ingest ms  | No           | Columnar       |
+----------------------------------------------------------------------------------------------------+
```

### 26.9.1 USCG legacy "Extended AIVDM"

Before NMEA 4.10 TAG blocks, the United States Coast Guard (**USCG**) captured coastal data across its Nationwide Automatic Identification System (**NAIS**) by appending comma-delimited metadata fields after the checksum:

```
!AIVDM,1,1,,B,15Cjtd0Oj;Jp7ilG7=UkKBoB0<06,0*63,s1234,d-119,T12.34567123,r003669958,1085889680
```

Metadata fields (Raymond & Schwehr 2023):
- `s1234`: Received Signal Strength Indication (**RSSI**) value (0–65535).
- `d-119`: Received signal strength in **dBm** ($-119\text{ dBm}$).
- `T12.34567123`: Precise Time of Arrival (**TOA**), recorded as seconds into the current UTC minute.
- `S0042` (when present): TDMA transmission slot number ($0 \dots 2249$).
- `r003669958`: USCG receiver station identifier (`r`-prefixed).
- `1085889680`: 32-bit UNIX epoch timestamp (seconds since 1 January 1970).

The `T` and `S` parameters provide slot-level arrival timing invaluable for forensic analysis.

### 26.9.2 Open agency formats: Marine Cadastre, DMA, and Nordic feeds

1. **NOAA / BOEM Marine Cadastre:** Provides historical track data for U.S. waters. Prior to 2025, files used camel-case columns: `MMSI, BaseDateTime, LAT, LON, SOG, COG, Heading, VesselName, IMO, CallSign, VesselType, Status, Length, Width, Draft, Cargo, TransceiverClass`. In 2025, NOAA transitioned to snake-case columns: `mmsi, base_date_time, longitude, latitude, sog, cog, heading, vessel_name, imo, call_sign, vessel_type, status, length, width, draft, cargo, transceiver`.
2. **Danish Maritime Authority (DMA):** Publishes daily zipped CSV archives (`aisdk-YYYY-MM-DD.zip`) containing 26 columns. The DMA CSV formats geographic coordinates using **European decimal commas** (e.g., `57,8794`) and dates as `DD/MM/YYYY HH:MM:SS`.
3. **Kystverket (Norwegian Coastal Administration):** Operates a free public TCP stream (`153.44.253.27:5631`) providing real-time data across the Norwegian Exclusive Economic Zone, Svalbard, and Jan Mayen, formatted using IEC 62320-1 TAG blocks.
4. **Fintraffic Digitraffic:** Delivers Finnish maritime data via REST endpoints and MQTT over WebSockets (`wss://meri.digitraffic.fi:443/mqtt`). Metadata timestamps are emitted in **milliseconds**, whereas vessel location timestamps are in **seconds**.

### 26.9.3 JSON stream formats: gpsd and AIS-catcher

`gpsd` transforms incoming serial sentences into newline-delimited JSON objects:

```json
{"class":"AIS","device":"/dev/ttyUSB0","type":1,"repeat":0,"mmsi":366999999,"scaled":true,"status":0,"status_text":"Under way using engine","turn":0,"speed":12.4,"accuracy":true,"lon":-122.419417,"lat":37.774929,"course":184.2,"heading":185,"second":42,"maneuver":0,"raim":false,"radio":149201}
```

Similarly, **AIS-catcher** supports output modes including `-o 7` (NMEA with TAG blocks) and `-o 5` (full JSON). In JSON mode, AIS-catcher automatically suppresses undefined sentinel values (such as latitude $91^\circ$, heading $511^\circ$, or speed $102.3\text{ kn}$).

## 26.10 Logging best practices and the three timestamps

Every logged AIS message can carry up to three distinct timestamps:

```
[Satellite / Vessel GNSS Clock] ---> 1. EPFS Time Stamp (M.1371 radio payload, 0-59 s)
                                                 |
                                         (RF Transmission)
                                                 v
[Coastal Base Station Receiver]  ---> 2. Reception Time (TAG block 'c:', UNIX epoch)
                                                 |
                                         (Network Transfer)
                                                 v
[Central Cloud / Server Ingest]  ---> 3. Ingest Log Time (Database timestamp)
```

1. **EPFS Second (Radio Payload):** Messages 1, 2, 3, 18, and 19 carry a 6-bit integer field storing the UTC second of the fix ($0 \dots 59$). It carries no year, month, day, hour, or minute. Sentinels 60 (not available), 61 (manual), 62 (dead reckoning), and 63 (inoperative) carry special operational meanings.
2. **Receiver Station Arrival Time (`c:`):** Recorded by the receiving base station's clock when the RF preamble is detected. If the base station drifts or loses NTP lock, this timestamp slips.
3. **Ingest System Timestamp:** Generated by the central cloud database when the network socket writes the record, reflecting network transit jitter and buffering.

> **Rule of thumb.** Always log the raw, unparsed NMEA sentence alongside any parsed database columns. If an analytical model discovers a decoder bug, a corrupted coordinate scale, or a leap-second desynchronization months later, raw text with NMEA 4.10 TAG blocks allows 100% lossless forensic replay. If only the parsed database columns are retained, irreversible information loss is guaranteed.

## Then & now

- **⟨H⟩ 1983:** NMEA 0183 Standard for Interfacing Marine Electronic Devices Version 1.0 released; defines 4,800-baud point-to-point RS-422 communications for simple talker-listener navigation sentences.
- **⟨H⟩ 1998:** IMO Resolution MSC.74(69) mandates the universal shipborne Automatic Identification System, requiring a digital presentation interface to feed bridge navigation displays.
- **⟨+⟩ 2001:** NMEA 2000 standard released, providing CAN-bus 250 kbit/s networking for marine electronics using Parameter Group Numbers (PGNs).
- **⟨+⟩ 2002:** IEC PAS 61162-100 publishes the first formal specification of `!AIVDM` and `!AIVDO` sentences and the 6-bit payload armoring scheme for AIS.
- **⟨+⟩ 2008:** NMEA 0183 Version 4.00 standardizes new AIS talker prefixes (`AB`, `AD`, `AN`, `AR`, `AT`, `AX`) and deprecates legacy `BS`.
- **⟨+⟩ 2011:** IEC 61162-450 Edition 1.0 standardizes Lightweight Ethernet (LWE), wrapping NMEA sentences into UDP multicast packets with the `UdPbC` header.
- **⟨+⟩ 2012:** NMEA 0183 Version 4.10 standardizes TAG blocks (`\s:,c:,g:,n:\`), providing standardized reception timestamps and station provenance.
- **⟨+⟩ 2015:** IEC 62320-1 Edition 2.0 adopts standard TAG blocks for AIS base station networks, replacing legacy comment blocks.
- **⟨+⟩ 2018:** NMEA 0183 Version 4.11 published, refining sentence encapsulation and multi-fragment synchronization rules.
- **⟨+⟩ 2020:** NMEA releases OneNet Version 1.000, establishing IPv6 Gigabit Ethernet marine networking and encapsulating NMEA 2000 PGNs over IP.
- **⟨+⟩ 2023:** NMEA publishes NMEA 0183 Version 4.30, incorporating high-speed 38.4 kbaud serial operation and comprehensive multi-GNSS sentence suites.
- **⟨+⟩ 2024:** IEC releases Edition 3.0 of IEC 61162-450 (Lightweight Ethernet) and IEC 61162-460 (Safety and Security), alongside Edition 6.0 of IEC 61162-1.

## On the wire

Let us perform a complete bit-by-bit inspection of an authentic single-sentence Class A position report received over coastal VHF:

```
!AIVDM,1,1,,B,177KQJ5000G?tO`K>RA1wUbN0TKH,0*5C
```

### 1. Hexadecimal Checksum Verification
The checksum string is `5C`. We compute the bitwise XOR across the 42 ASCII bytes between `!` and `*`:
```
Byte   Char   ASCII Hex   Running XOR
 1      'A'      0x41        0x41
 2      'I'      0x49        0x08
 3      'V'      0x56        0x5E
 4      'D'      0x44        0x1A 
 5      'M'      0x4D        0x57
 6      ','      0x2C        0x7B
 7      '1'      0x31        0x4A
 8      ','      0x2C        0x66
 9      '1'      0x31        0x57
10      ','      0x2C        0x7B
11      ','      0x2C        0x57
12      'B'      0x42        0x15
13      ','      0x2C        0x39
14      '1'      0x31        0x08
...     ...      ...         ...
42      '0'      0x30        0x5C   <-- Exact match with transmitted *5C
```

### 2. 6-Bit Armored Payload Unpacking
The payload contains 28 characters. Applying the unarmoring rule ($A - 48$, and if result $> 40$, subtract 8):
- Char 1: `'1'` (ASCII 49) $\rightarrow 49 - 48 = 1 \rightarrow \mathbf{000001_2}$
- Char 2: `'7'` (ASCII 55) $\rightarrow 55 - 48 = 7 \rightarrow \mathbf{000111_2}$
- Char 3: `'7'` (ASCII 55) $\rightarrow 55 - 48 = 7 \rightarrow \mathbf{000111_2}$
- Char 4: `'K'` (ASCII 75) $\rightarrow 75 - 48 = 27 \rightarrow \mathbf{011011_2}$
- Char 5: `'Q'` (ASCII 81) $\rightarrow 81 - 48 = 33 \rightarrow \mathbf{100001_2}$
- Char 6: `'J'` (ASCII 74) $\rightarrow 74 - 48 = 26 \rightarrow \mathbf{011010_2}$
- Char 7: `'5'` (ASCII 53) $\rightarrow 53 - 48 = 5 \rightarrow \mathbf{000101_2}$
- Char 8: `'0'` (ASCII 48) $\rightarrow 48 - 48 = 0 \rightarrow \mathbf{000000_2}$
- ...
- Char 15: `` '`' `` (ASCII 96) $\rightarrow 96 - 48 - 8 = 40 \rightarrow \mathbf{101000_2}$

Concatenating the 28 unarmored 6-bit symbols yields exactly 168 binary bits:
```
000001 000111 000111 011011 100001 011010 000101 000000 ...
```

### 3. Field Slicing per ITU-R M.1371
- **Message Type (bits 1–6):** `000001` $\rightarrow$ **Message 1** (Position Report Class A).
- **Repeat Indicator (bits 7–8):** `00` $\rightarrow$ `0` (transmissions executed without repeater).
- **MMSI (bits 9–38):** 30-bit integer $\rightarrow$ User ID.
- **Navigational Status (bits 39–42):** `0000` $\rightarrow$ `0` ("Under way using engine").
- **Rate of Turn (bits 43–50):** `00000000` $\rightarrow$ `0 deg/min`.
- **Speed Over Ground (bits 51–60):** 10-bit integer $\rightarrow 12.3\text{ knots}$ ($0.1\text{ kn}$ resolution).
- **Position Accuracy (bit 61):** `1` $\rightarrow$ High accuracy ($< 10\text{ m}$ DGNSS/SBAS).
- **Longitude (bits 62–89):** 28-bit signed two's complement integer in units of $1/10000\text{ min}$.
- **Latitude (bits 90–116):** 27-bit signed two's complement integer in units of $1/10000\text{ min}$.
- **Course Over Ground (bits 117–128):** 12-bit unsigned integer $\rightarrow$ degrees with $0.1^\circ$ resolution.
- **True Heading (bits 129–137):** 9-bit unsigned integer $\rightarrow$ degrees ($511 = \text{not available}$).
- **Time Stamp (bits 138–143):** 6-bit unsigned integer $\rightarrow$ UTC second ($0 \dots 59$).
- **Radio Status / SOTDMA Comm State (bits 149–168):** 19-bit communication state field.

> **Try it.** Validate the TAG block and sentence checksums from this chapter using Python and `code/decode/tagblock.py`:
> 
> ```python
> from code.decode.tagblock import parse_line, nmea_checksum
> 
> raw = r"\g:1-2-73874,n:157036,s:r003669945,c:1241544035*4A\!AIVDM,1,1,,B,15N4cJ`005Jrek0H@9n`DW5608EP,0*13"
> tb, sentence = parse_line(raw)
> 
> print(f"Tag checksum verified: {tb.checksum_ok}")
> print(f"Source station:        {tb.source}")
> print(f"UNIX timestamp:        {tb.unix_time}")
> print(f"Sentence checksum:     {nmea_checksum(sentence[1:].split('*')[0]):02X}")
> ```
> Expected output:
> ```
> Tag checksum verified: True
> Source station:        r003669945
> UNIX timestamp:        1241544035.0
> Sentence checksum:     13
> ```

## Validation, uncertainty & data quality

Errors in interface and logging pipelines arise through three primary pathways: physical serial link corruption, fragment reassembly desynchronization, and timestamp drift.

### 1. Physical Serial Bit Errors and Checksum Integrity
RS-422 and RS-232 serial cables installed in vessel engine rooms or antenna masts are exposed to severe electromagnetic interference (**EMI**) from radar magnetrons and variable-frequency drives. The 8-bit XOR NMEA checksum has an undetected bit-error vulnerability: any even number of identical bit flips at the same bit position across characters cancels out in the XOR accumulation.
- **Procedure:** Always validate both the NMEA checksum and the internal structural constraints of the decoded radio message. For example, if an uncorrupted XOR checksum delivers a Message 1 whose Latitude exceeds $\pm 90^\circ$ or whose Speed Over Ground exceeds 102.2 knots without hitting the 102.3 sentinel, the payload has suffered undetected serial corruption and must be flagged as invalid.

### 2. Multi-Fragment Interleaving Metrics
In high-density receiver networks aggregating data over TCP/UDP without source tagging, fragment collisions corrupt static voyage data.
- **Procedure:** Calculate the reassembly failure rate $R_{\text{drop}}$:
  $$R_{\text{drop}} = \frac{N_{\text{orphaned\_fragments}}}{N_{\text{total\_expected\_fragments}}} \times 100\%$$
  In healthy coastal networks utilizing compound keying `(station, talker, channel, seq_id)`, $R_{\text{drop}}$ remains below $0.05\%$. In misconfigured networks stripping station metadata before reassembly, $R_{\text{drop}}$ frequently exceeds $12\%$, creating artificial "ghost" vessels and corrupted ship registries.

### 3. Timestamp Discrepancy Analysis
A systematic worked procedure must be applied to isolate clock drift across coastal receivers:
- Let $t_{\text{recv}}$ be the receiver TAG block timestamp (`c:`).
- Let $t_{\text{epfs}}$ be the UTC second broadcast in Message 1 ($0 \dots 59$).
- Compute the second-modulo residual:
  $$\Delta t = (t_{\text{recv}} \pmod{60}) - t_{\text{epfs}}$$
  Accounting for circular boundary wrap-around at 60 seconds:
  $$\Delta t_{\text{wrapped}} = (\Delta t + 30 \pmod{60}) - 30$$
- In a synchronized receiver with low serial latency ($< 100\text{ ms}$ buffer delay), $\Delta t_{\text{wrapped}}$ clusters tightly within $[0.0, +1.5\text{ s}]$. If a coastal station exhibits a constant offset $\Delta t_{\text{wrapped}} \approx 14\text{ s}$ or wanders steadily over time, the receiver's host system has lost NTP synchronization or has suffered an uncompensated leap-second offset.

## Software

**Open source:**
- **gpsd** (C, BSD): The gold standard open-source GPS and AIS service daemon. Converts NMEA 0183, NMEA 2000, and AIS sentences into JSON streams. *Caveat:* Reassembly buffer timeouts can drop fragments under severe system CPU starvation.
- **canboat** (C / Python, Apache-2.0): Toolkit for reading and reverse-engineering NMEA 2000 CAN-bus traffic; contains the most complete open database of AIS PGN definitions. *Caveat:* Field definitions are reverse-engineered from public traffic and may diverge from proprietary NMEA amendments.
- **AIS-catcher** (C++, GPL-3.0): High-performance SDR receiver and multi-protocol forwarder supporting raw NMEA, TAG block injection, and JSON streaming. *Caveat:* Automatically strips undefined sentinel values in JSON mode, which may alter downstream outlier filtering.
- **libais** (C++ / Python, Apache-2.0): High-speed decoding library developed by Kurt Schwehr, providing comprehensive bit-level validation of ITU-R M.1371 messages and ASM payloads. *Caveat:* Requires pre-reassembled payload strings; does not perform multi-fragment sentence reassembly internally.

**Free but closed:**
- **OpenCPN AIS Decoder Engine** (GPL base with proprietary binary plugin distributions): Embedded navigation display engine decoding serial and network AIS streams. *Caveat:* GUI rendering threads can drop bursts during heavy chart redraw operations.

**Commercial:**
- **Furuno / Saab Class A Presentation Interfaces** (Firmware): Certified type-approved transponder presentation engines delivering dual-channel 38,400-baud IEC 61162-2 serial streams. *Caveat:* Proprietary diagnostic sentences are vendor-specific and undocumented in public manuals.

## Standards & guides

- **IEC 61162-1:2024 (Ed. 6.0):** *Maritime navigation and radiocommunication equipment and systems – Digital interfaces – Part 1: Single talker and multiple listeners.* Governs NMEA 0183 serial physical, link, and sentence formatting.
- **IEC 61162-2:2024 (Ed. 2.0):** *Digital interfaces – Part 2: Single talker and multiple listeners, high-speed transmission.* Defines the 38,400-baud electrical interface used for AIS Presentation Interfaces.
- **IEC 61162-450:2024 (Ed. 3.0):** *Digital interfaces – Part 450: Multiple talkers and multiple listeners – Ethernet interconnection.* Specifies Lightweight Ethernet (LWE), UDP multicast encapsulation, and the `UdPbC` header.
- **IEC 61162-460:2024 (Ed. 3.0):** *Digital interfaces – Part 460: Ethernet interconnection – Safety and security.* Specifies security gateway architectures, firewall rules, and stateful inspection on shipboard bridge networks.
- **IEC 62320-1:2015 (Ed. 2.0):** *Automatic identification system (AIS) – Part 1: AIS Base Stations.* Defines coastal station operational requirements, NMEA presentation, and TAG block comment formatting.
- **ITU-R M.1371-5 (2014):** *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band.* Defines core message structures and 6-bit binary layouts.
- **NMEA 0183 Version 4.30 (2023):** *Standard for Interfacing Marine Electronic Devices.* Governing standard for marine serial communications, talker mnemonics, and TAG blocks.
- **NMEA 2000 Version 3.000 (2020):** *Standard for Serial-Data Networking of Marine Electronic Devices.* Specifies CAN-bus marine architectures and Fast Packet AIS PGNs.
- **NMEA OneNet Version 1.000 (2020):** *Standard for IP Networking of Marine Electronic Devices.* Governs IPv6 Gigabit Ethernet marine networks.

## Pitfalls

1. **Filtering on hardcoded `!AIVDM`:** Discards valid coastal traffic transmitted under shore base station (`!ABVDM`), Aid to Navigation (`!ANVDM`), or receiver (`!ARVDM`) talker prefixes. Match sentences using regex `^![A-Z]{2}VD[MO]` to preserve all station classes.
2. **Reassembling fragments using only Sequential ID:** Interleaved fragments from multiple coastal receivers sharing the same sequential ID ($0 \dots 9$) corrupt vessel static records. Reassembly caches must key on `(Station ID, Talker, Channel, Sequential ID)`.
3. **Strict payload length rejection on fill-bit errors:** Faulty transponders frequently report fill bits as `0` instead of `2` for 424-bit Message 5 records, yielding 426 bits. Decoders that enforce strict length equality drop static voyage data; allow up to 5 trailing padding bits.
4. **Assuming TAG block `c:` is always seconds:** Modern SDR receivers and cloud aggregators emit `c:` in milliseconds, while legacy base stations emit seconds. Inspect the magnitude: values above $10^{11}$ are milliseconds.
5. **Ignoring European decimal commas in public archives:** Archives such as the Danish Maritime Authority (DMA) format latitude and longitude with commas (`57,8794`). Standard CSV parsers split coordinates across columns or parse them as integers.
6. **Operating AIS Presentation Interfaces at 4,800 baud:** The legacy NMEA 0183 speed of 4,800 baud saturates during high-density VHF traffic, causing serial buffer overflows. AIS presentation links must operate at 38,400 baud.
7. **Discarding raw NMEA lines in database ingest pipelines:** Storing only parsed database fields makes it impossible to re-evaluate data after discovering parser bugs or schema drift. Always archive raw NMEA lines with TAG blocks alongside analytical tables.
8. **Treating EPFS time stamp (bits 138–143) as a complete time:** The 6-bit time field carries only the UTC second ($0 \dots 59$). Attempting to construct full datetime objects without external receiver timestamps causes multi-day date ambiguity.
9. **Failing to handle sentinels 60–63 in position reports:** Treating time stamp sentinels 60 (not available), 61 (manual), 62 (dead reckoning), or 63 (inoperative) as literal seconds causes periodic spikes in time-series plots.
10. **Dropping leading zeros in armored payload unpacking:** 6-bit binary unpacking must retain all leading zeros. Stripping leading zeros shifts every subsequent bit in the message, destroying MMSI numbers and coordinates.
11. **Assuming NMEA 2000 CAN IDs match NMEA 0183 sequential IDs:** CAN frame sequence counters in Fast Packet protocols operate independently of the underlying AIS sequential message counter.
12. **Assuming UDP multicast delivery is lossless:** High-traffic Ethernet networks without Quality of Service (**QoS**) drop UDP datagrams under burst conditions. Ingest monitors must track TAG block line counts (`n:`) to detect dropped packets.

## Key takeaways

- AIS radio bursts are encapsulated into ASCII serial strings using NMEA 0183 and IEC 61162-1 `!AIVDM` (received targets) and `!AIVDO` (own-ship) sentences.
- AIS serial presentation interfaces must operate at **38,400 baud** to prevent buffer saturation in dense maritime waterways.
- Payloads are converted to ASCII using **6-bit armoring** ($A = v + 48$, or $v + 56$ if $> 40$), spanning characters `0`–`W` and `` ` ``–`w`.
- Multi-fragment messages must be reassembled using compound keys `(Station ID, Talker, Channel, Sequential ID)` with strict 2-to-4-second timeouts to avoid buffer cross-contamination.
- Presentation interface control sentences (`ABM`, `BBM`, `ACA`, `SSD`, `VSD`) use the standard `$` delimiter to configure transponders and schedule transmissions.
- **NMEA 4.10 TAG blocks** (`\s:...,c:...*hh\`) provide essential reception provenance, including receiving station ID and UNIX epoch timestamps.
- **IEC 61162-450 (Lightweight Ethernet)** encapsulates sentences into UDP multicast frames led by the 6-byte header `UdPbC\0`, routed to group `TGTD` (`239.192.0.2:60002`).
- **NMEA 2000** networks transmit AIS binary data over CAN buses at 250 kbit/s using Fast Packet PGNs (e.g., 129038 for Class A, 129794 for static data).
- Logging pipelines must distinguish between the 6-bit EPFS second, the receiver arrival timestamp (`c:`), and the central database ingest timestamp.
- Always retain raw, unparsed NMEA sentences with TAG block envelopes in cold storage to guarantee forensic reproducibility.

## References

* AIS-catcher (2026). *AIS-catcher: A multi-platform AIS receiver for SDR and NMEA streams* (v0.62). https://github.com/jvde-github/AIS-catcher. GPL-3.0.
* canboat (2026). *canboat: A boat-load of NMEA and CAN-bus utilities* (v8.3.0). https://github.com/canboat/canboat. Apache-2.0.
* Danish Maritime Authority (2023). *AIS Data Information and CSV File Format Specification*. Technical Documentation. Copenhagen: DMA. https://www.dma.dk/safety-at-sea/navigational-information/ais-data
* Fintraffic (2026). *Digitraffic Marine Real-Time AIS API*. Helsinki: Fintraffic Open Data Service. https://www.digitraffic.fi/en/marine-traffic/
* Global Fishing Watch (2026). *ais-tools: Tools for processing AIS messages*. https://github.com/GlobalFishingWatch/ais-tools. Apache-2.0.
* International Electrotechnical Commission (2002). *Maritime navigation and radiocommunication equipment and systems – Digital interfaces – Part 100: Single talker and multiple listeners – Extra requirements to IEC 61162-1 for the UAIS* (IEC/PAS 61162-100:2002). Geneva: IEC.
* International Electrotechnical Commission (2008). *Maritime navigation and radiocommunication equipment and systems – Digital interfaces – Part 3: Serial data network* (IEC 61162-3:2008). Geneva: IEC.
* International Electrotechnical Commission (2015). *Automatic identification system (AIS) – Part 1: AIS Base Stations – Minimum operational and performance requirements, methods of testing and required test results* (IEC 62320-1:2015, Ed. 2.0). Geneva: IEC.
* International Electrotechnical Commission (2024a). *Maritime navigation and radiocommunication equipment and systems – Digital interfaces – Part 1: Single talker and multiple listeners* (IEC 61162-1:2024, Ed. 6.0). Geneva: IEC.
* International Electrotechnical Commission (2024b). *Maritime navigation and radiocommunication equipment and systems – Digital interfaces – Part 2: Single talker and multiple listeners, high-speed transmission* (IEC 61162-2:2024, Ed. 2.0). Geneva: IEC.
* International Electrotechnical Commission (2024c). *Maritime navigation and radiocommunication equipment and systems – Digital interfaces – Part 450: Multiple talkers and multiple listeners – Ethernet interconnection* (IEC 61162-450:2024, Ed. 3.0). Geneva: IEC.
* International Electrotechnical Commission (2024d). *Maritime navigation and radiocommunication equipment and systems – Digital interfaces – Part 460: Multiple talkers and multiple listeners – Ethernet interconnection – Safety and security* (IEC 61162-460:2024, Ed. 3.0). Geneva: IEC.
* International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-5). Geneva: ITU.
* Kystverket (2026). *Access to AIS Data*. Arendal: Norwegian Coastal Administration. https://www.kystverket.no/en/sea-transport-and-ports/ais/access-to-ais-data/
* National Marine Electronics Association (2012). *Standard for Interfacing Marine Electronic Devices* (NMEA 0183 Version 4.10). Severna Park, MD: NMEA.
* National Marine Electronics Association (2020a). *Standard for Serial-Data Networking of Marine Electronic Devices* (NMEA 2000 Version 3.000). Severna Park, MD: NMEA.
* National Marine Electronics Association (2020b). *Standard for IP Networking of Marine Electronic Devices* (OneNet Version 1.000). Severna Park, MD: NMEA.
* National Marine Electronics Association (2023). *Standard for Interfacing Marine Electronic Devices* (NMEA 0183 Version 4.30). Severna Park, MD: NMEA. https://www.nmea.org/nmea-0183.html
* NOAA and BOEM (2026). *Marine Cadastre AIS Data Dictionary*. Charleston, SC: NOAA Office for Coastal Management. https://coast.noaa.gov/data/marinecadastre/ais/data-dictionary.pdf
* Raymond, E. S., and Schwehr, K. (2023). *AIVDM/AIVDO Protocol Decoding* (Version 1.58). The GPSD Project. https://gpsd.gitlab.io/gpsd/AIVDM.html
* Raymond, E. S. (2025). *NMEA Revealed*. The GPSD Project. https://gitlab.com/gpsd/gpsd/-/raw/master/www/NMEA.adoc
