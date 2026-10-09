# Chapter 25 — GNSS and AIS

> **Part IV — The system: architecture and protocol.** How global satellite navigation provides spatial coordinates and slot synchronization for maritime transponders, what shipborne hardware actually tracks, and how systems navigate when satellite signals degrade or fail.

**In this chapter.** You will learn how Global Navigation Satellite Systems (**GNSS**) integrate with the Automatic Identification System (**AIS**). You will examine the core constellations—GPS, GLONASS, Galileo, BeiDou, and regional overlays—and contrast technology-neutral operational standards from the International Maritime Organization (**IMO**) with strict internal receiver mandates from the International Electrotechnical Commission (**IEC**). You will analyze empirical survey data from 37 commercial transponders across four hardware generations to understand real-world constellation tracking, channel counts, and satellite-based augmentation support. You will trace how transponders derive position accuracy and Receiver Autonomous Integrity Monitoring (**RAIM**) flags, examine Differential GNSS (**DGNSS**) broadcasts over Message 17, and evaluate transponder behavior under satellite loss. Finally, you will identify jamming and spoofing signatures in AIS tracking data and explore GNSS-independent backup technologies including R-Mode, enhanced Loran (**eLoran**), and bridge sensor fusion.

## 25.1 Core constellations and augmentations

The Automatic Identification System is intimately linked to satellite radionavigation. Every positional broadcast transmitted over the maritime VHF Data Link (**VDL**)—from high-speed passenger craft broadcasting every two seconds to search-and-rescue beacons—relies on satellite navigation signals. To understand how AIS functions, we must first examine the constellations overhead.

Six satellite constellations provide operational Position, Navigation, and Timing (**PNT**) services to maritime users:
1. **Global Positioning System (GPS):** Operated by the US Space Force, GPS declared Full Operational Capability (**FOC**) on 17 July 1995. The discontinuance of Selective Availability (**SA**) on 2 May 2000 improved civilian accuracy from ~100 m to 3–5 m. GPS broadcasts civilian signals on L1 (1575.42 MHz, L1 C/A and L1C), L2 (1227.60 MHz, L2C), and L5 (1176.45 MHz).
2. **GLONASS:** Operated by the Russian Federation, GLONASS restored its 24-satellite baseline in 2011. Legacy GLONASS uses FDMA across the L1 sub-band (1598.0625–1605.375 MHz) and L2 sub-band, with newer satellites adding CDMA signals at 1575.42 MHz (L1OC) and 1207.14 MHz (L3OC).
3. **Galileo:** Operated by the EU via EUSPA, Galileo declared Initial Services on 15 December 2016. Its satellites carry rubidium atomic frequency standards (**RAFS**) and passive hydrogen maser (**PHM**) clocks, broadcasting open-service CDMA signals on E1 (1575.42 MHz), E5a, E5b, and E6.
4. **BeiDou Navigation Satellite System (BDS):** Operated by China, BeiDou completed its BDS-3 global network on 31 July 2020. BeiDou broadcasts civilian signals on B1I (1561.098 MHz), B1C (1575.42 MHz), B2a, B2b, and B3I.
5. **Quasi-Zenith Satellite System (QZSS):** Operated by Japan, QZSS augments GPS over East Asia and Oceania from inclined geosynchronous orbits, broadcasting signals compatible with GPS L1, L2, and L5.
6. **Navigation with Indian Constellation (NavIC):** Operated by India, NavIC provides regional coverage over South Asia, broadcasting civilian signals on L5 (1176.45 MHz), S-band (2492.028 MHz), and L1.

| Constellation | Operator | Orbit Architecture | Status / Baseline | Maritime Frequencies | Service Scope |
|---|---|---|---|---|---|
| **GPS** | United States | 24+ MEO (6 planes) | Operational (FOC 1995) | L1 (1575.42 MHz), L2, L5 | Global |
| **GLONASS** | Russian Fed. | 24 MEO (3 planes) | Restored baseline (2011) | L1 FDMA (1602 MHz), L2, L3 CDMA | Global |
| **Galileo** | European Union | 24+ MEO (3 planes) | Initial Services (2016) | E1 (1575.42 MHz), E5a, E5b, E6 | Global |
| **BeiDou (BDS-3)**| China | 30 MEO / IGSO / GEO | Global operational (2020) | B1I (1561.10 MHz), B1C, B2a, B3I | Global |
| **QZSS** | Japan | 4 QZO / GEO | Operational (2018) | L1 (1575.42 MHz), L2, L5, L6 | Regional (Asia-Pacific) |
| **NavIC** | India | 7 GEO / IGSO | Operational (2018) | L5 (1176.45 MHz), S-band, L1 | Regional (South Asia) |

*Table 25-1: Overview of core global and regional satellite navigation systems supporting maritime navigation.*

To correct for ionospheric delay, tropospheric refraction, and orbital ephemeris errors, satellite navigation can be augmented by regional **Satellite-Based Augmentation Systems (SBAS)**. SBAS networks deploy geostationary communication satellites that broadcast differential corrections and integrity status directly to shipborne receivers on GPS L1:
- **WAAS:** Commissioned by the US FAA on 10 July 2003, covering North America and adjacent waters.
- **EGNOS:** Declared operational for Open Service in 2009 and Safety-of-Life (**SoL**) service on 2 March 2011, covering Europe and the Mediterranean.
- **MSAS:** Operational in Japan since 27 September 2007.
- **GAGAN:** Certified for civil aviation in India in 2013, with full Approach with Vertical Guidance (**APV-1**) certified on 21 April 2015.

Modern maritime GNSS receivers decode SBAS signals, obtaining differential corrections without requiring dedicated terrestrial radio beacon receivers.

## 25.2 Standards vs. hardware reality: the EPFS and the internal GNSS

The regulatory framework governing how an AIS transponder acquires its position reveals an intentional split between high-level operational standards and equipment engineering specifications.

Under SOLAS, the primary performance standard for AIS is IMO Resolution MSC.74(69) Annex 3, adopted on 12 May 1998. When drafting MSC.74(69), the IMO avoided mandating GPS by name. Under §3.1.2, the IMO established that an AIS unit must incorporate:
> "a means of processing data from an electronic position-fixing system which provides a resolution of one ten thousandth of a minute of arc and uses the WGS-84 datum."

The resolution does not mandate an internal satellite receiver for positional tracking. On large commercial vessels, the primary position source feeding navigation displays is the vessel's centralized **Electronic Position-Fixing System (EPFS)**—typically a type-approved dual-redundant GPS or GNSS navigator mounted on the bridge deck, certified under the IEC 61108 series. The external EPFS delivers geographic coordinates, Speed Over Ground (**SOG**), and Course Over Ground (**COG**) across an IEC 61162-1 (NMEA 0183) serial interface or IEC 61162-450 Ethernet network to the AIS transponder, as explored in [Chapter 26](ch26-interfaces-and-logging.md).

```
+----------------------------------------------------------------------------+
|                          TYPICAL CLASS A INSTALLATION                      |
+----------------------------------------------------------------------------+
|  [ Bridge Main EPFS ]           [ Transponder Chassis ]                    |
|  (IEC 61108 Certified)          +---------------------------------------+  |
|  Position / SOG / COG           | Primary Link Processor                |  |
|           |                     | (Uses External EPFS for Dynamic Data) |  |
|           v                     +-------------------+-------------------+  |
|     IEC 61162 Serial                                |                      |
|   ($GPGGA / $GPRMC)                                 | Backup Position      |
|           |                                         | Switching            |
|           +---------------------------------------->+                      |
|                                                     |                      |
|  [ Dedicated AIS GNSS Antenna ]                     v                      |
|  (RF Coaxial Cable)             +---------------------------------------+  |
|           |                     | Internal GNSS Engine                  |  |
|           +-------------------->| - Slot-timing Clock (1PPS / UTC)      |  |
|                                 | - Fallback Position / COG / SOG       |  |
|                                 +---------------------------------------+  |
+----------------------------------------------------------------------------+
```

However, as detailed in [Chapter 24](ch24-timing.md), AIS is a Time Division Multiple Access (**TDMA**) network dividing radio channels into 26.67 ms slots. To prevent packet collisions across the radio cell, transmitters must lock their physical slot boundaries to Coordinated Universal Time (**UTC**) within microsecond tolerances ($\pm 104\ \mu\text{s}$ for mobile stations, $\pm 52\ \mu\text{s}$ for base stations per ITU-R M.1371-6 §A2-3.2.2.8.3). An external bridge serial sentence arriving across an asynchronous RS-422 interface with tens of milliseconds of serial latency and buffering jitter cannot discipline a 9,600 bit/s radio burst.

Consequently, IEC equipment standards enforce strict hardware mandates:
- **Class A Transponders (IEC 61993-2):** Must incorporate an internal GNSS receiver connected to a dedicated antenna. It provides UTC slot timing and autonomous position fallback if bridge EPFS serial feeds sever. IMO Resolution A.1106(29) explicitly defines transponders as containing an internal "GNSS receiver for timing purposes and position redundancy."
- **Class B SOTDMA (IEC 62287-2):** For Class B "SO" units (5 W SOTDMA), IEC 62287-2 states: "only uses the internal GNSS – no position sensor input is allowed." External NMEA position feeds are prohibited.
- **Class B CSTDMA (IEC 62287-1):** Governed by ITU-R M.1371-6 Annex 6 (§A6-3.3): "The Class B 'CS' AIS should have an internal GNSS receiver as source for position, COG, and SOG." External position inputs are barred under IEC 62287-1 Edition 3.0.
- **Aids to Navigation (IEC 62320-2):** Type 1 AtoNs possess no VHF receiver and transmit on pre-reserved FATDMA slots. Under IEC 62320-2 Table 1, a Type 1 AtoN requires an internal GNSS receiver locked to "UTC Direct" for slot timing, broadcasting either live GNSS coordinates or surveyed coordinates.

> **Definitions that bite.** EPFS vs. Internal GNSS.
> Navigators and software developers frequently conflate the vessel's primary bridge navigation sensor with the transponder's internal receiver:
> - **EPFS (Electronic Position-Fixing System):** The vessel's central, type-approved navigation receiver (compliant with IMO Resolution MSC.401(95) and IEC 61108), located on the bridge. It feeds radar, ECDIS, autopilot, Voyage Data Recorders (**VDR**), and the AIS external sensor port.
> - **Internal GNSS:** A dedicated GNSS receiver module housed physically inside the AIS transponder casing, wired to an independent satellite antenna mounted on the ship's mast. It disciplines the physical slot transmission clock and provides autonomous position fallback. On Class B vessels, the internal GNSS is the *sole* legal position source.

## 25.3 Datasheet survey: what transponders actually contain

To determine which satellite constellations maritime hardware supports in practice, we conducted an empirical survey of 37 commercial transponder, AtoN, and search-and-rescue transmitter product manuals spanning four hardware generations manufactured between 2005 and 2026.

```
Hardware Evolution: Transponder GNSS Architectures (2005–2026)
=============================================================================
Generation 1 (2001–2010): 12–16 Channels, GPS-only (L1 C/A)
  [ Furuno FA-100/170 ] --> L1 C/A GPS only; DGPS via external RTCM SC-104 port
-----------------------------------------------------------------------------
Generation 2 (2011–2016): 50 Channels, GPS + SBAS Engine
  [ Saab R5, Vesper XB-8000 ] --> 50-ch engine; GPS + WAAS/EGNOS integration
-----------------------------------------------------------------------------
Generation 3 (2017–2022): 72 Channels, Multi-GNSS Concurrent Tracking
  [ em-trak A200/B900, Cortex ] --> 72-ch engine (u-blox M8 class); GPS+GLO+GAL+BDS
-----------------------------------------------------------------------------
Generation 4 (2023–Present): Multi-Band / Multi-Constellation VDES Platforms
  [ Saab R6 Supreme, AMEC B650 ] --> Multi-system type approval; Galileo/BDS default
=============================================================================
```

The survey reveals several distinct architectural trends:
- **Generation 1 (2001–2010):** Early Class A transponders deployed under original SOLAS mandates relied on 12-channel to 16-channel GPS L1 C/A modules. The Furuno FA-170 documents an internal 12-channel all-in-view GPS receiver. Differential corrections required wiring an external beacon receiver into an RTCM SC-104 / ITU-R M.823 input port.
- **Generation 2 (2011–2016):** Transponders transitioned to 50-channel commercial GNSS engines (predominantly u-blox 6/7 chipsets). Models like the Saab R5 Supreme, Nauticast A2, and Vesper XB-8000 incorporated integrated SBAS demodulators (WAAS/EGNOS). The Transas T-105 integrated dual GLONASS/GPS tracking for Russian domestic carriage rules.
- **Generation 3 (2017–2022):** Around 2017, hardware adopted 72-channel multi-constellation receivers (u-blox M8 series). Units like the em-trak A200, em-trak B900 series, Vesper Cortex M1, Raymarine AIS700, and AMEC A750 support concurrent reception of GPS, GLONASS, Galileo, and BeiDou. However, datasheets reveal concurrency limits: em-trak specifications state that the engine tracks "two of any combination, three including GPS, Galileo."
- **Generation 4 (2023–present):** Modern commercial equipment, typified by the Saab R6 Supreme AIS/VDES transponder and AMEC B650 series, incorporates full multi-system type-approval under IMO Resolution MSC.401(95) and IEC 61108, enabling Galileo and BeiDou tracking alongside GPS. Regional systems remain rare: QZSS appears in only two datasheets (AMEC N323 AtoN and Samyung SI-70A), while NavIC is absent.

| Manufacturer & Model | Station Class | Stated Constellations | Channels | Augmentation Support | Surveyed Documentation |
|---|---|---|:---:|---|---|
| **Furuno FA-170** | Class A | GPS (L1 C/A) | 12 | DGPS via RTCM SC-104 v2.1 port | Operator Manual |
| **Furuno FA-70** | Class B SO | GPS | 12+2 | SBAS (2 channels) | Product Brochure |
| **JRC JHS-183** | Class A | GPS (internal) | — | DGPS beacon port (M.823) | Technical Manual |
| **Saab R5 Supreme** | Class A | GPS (L1) | 50 | DGPS ready (external port) | Specification Sheet |
| **Saab R6 Supreme** | Class A / VDES | Multi-GNSS (GPS, Galileo) | — | Type-approved DGNSS kit | Product Catalog |
| **em-trak A200** | Class A | GPS, GLONASS, BeiDou, Galileo | 72 | IEC 61108-1/-2 compliant | Technical Datasheet |
| **em-trak B921/B954** | Class B CS / SO | GPS, GLONASS, BeiDou, Galileo | 72 | Dual concurrent tracking | Product Manual |
| **Vesper Cortex M1** | Class B SO | GPS, GLONASS, BeiDou, Galileo | 72 | SBAS, WAAS, EGNOS | Product Overview |
| **AMEC A750** | Class A | GPS, GLONASS, BeiDou, Galileo | 72 | WAAS, EGNOS, MSAS, GAGAN | Operation Manual |
| **AMEC N323** | AtoN Type 3 | GPS/QZSS, GLONASS, BeiDou, Galileo | 72 | WAAS, EGNOS, MSAS, GAGAN | Datasheet |
| **Samyung SI-70A** | Class A | GPS, QZSS, GLONASS, BDS, Galileo | 72 | WAAS, EGNOS, MSAS | Specification Sheet |
| **Icom MA-510TR** | Class B CS | GPS | 66 | SBAS | Instruction Manual |
| **Raymarine AIS700** | Class B SO | GPS, GLONASS | 72 | SBAS enabled | Installation Guide |
| **Digital Yacht AIT5000**| Class B SO | GPS, GLONASS | 72 | SBAS enabled | Specification Sheet |
| **McMurdo SmartFind M10**| Class B CS | GPS, Galileo | 72 | Factory default mode | User Manual |
| **Jotron Tron AIS-SART** | AIS-SART | GPS | — | 15-minute fix acquisition | User Manual |

*Table 25-2: Empirical survey of internal GNSS receiver specifications across commercial AIS transponders.*

## 25.4 The position accuracy flag and RAIM (Table 48)

Every positional AIS report carries two single-bit indicators reflecting positional integrity:
1. **Position Accuracy (PA) Flag (1 bit):** Bit value `1` indicates high accuracy ($\le 10\text{ m}$ estimated error); bit value `0` indicates low accuracy ($> 10\text{ m}$ error or unmonitored default).
2. **RAIM Flag (1 bit):** Bit value `1` indicates Receiver Autonomous Integrity Monitoring is active; bit value `0` indicates RAIM is not in use.

Under Recommendation ITU-R M.1371-6 Table 48, transponders derive these bits from NMEA 0183 sentences (`$GPGGA`, `$GPGNS`, and `$GPGBS`):
- **Autonomous Fix without RAIM:** If RAIM is inactive and no differential corrections are applied, the transponder sets **PA = 0** and **RAIM = 0**, regardless of satellite count.
- **RAIM Active with Error Bounds:** If the receiver outputs a valid `$GPGBS` sentence, the transponder computes expected horizontal error: $\sigma_H = \sqrt{\sigma_{\text{lat}}^2 + \sigma_{\text{lon}}^2}$. If $\sigma_H \le 10.0\text{ m}$, it sets **PA = 1** and **RAIM = 1**. If $\sigma_H > 10.0\text{ m}$, it sets **PA = 0** and **RAIM = 1**.
- **Differential Correction without RAIM:** If the fix is differentially corrected (SBAS or DGPS) but RAIM is absent, Table 48 dictates **PA = 1** and **RAIM = 0**.

| Differential Correction Applied? | RAIM Process Active in Receiver? | Expected Error from `$GPGBS` ($\sigma_H$) | Position Accuracy (PA) Flag | RAIM In-Use Flag |
|:---:|:---:|:---:|:---:|:---:|
| No | No | Not Available | `0` (Low, $> 10\text{ m}$) | `0` (RAIM Inactive) |
| No | Yes | $\le 10.0\text{ m}$ | `1` (High, $\le 10\text{ m}$) | `1` (RAIM Active) |
| No | Yes | $> 10.0\text{ m}$ | `0` (Low, $> 10\text{ m}$) | `1` (RAIM Active) |
| **Yes** | **No** | **Not Available** | **`1` (High, $\le 10\text{ m}$)** | **`0` (RAIM Inactive)** |
| Yes | Yes | $\le 10.0\text{ m}$ | `1` (High, $\le 10\text{ m}$) | `1` (RAIM Active) |
| Yes | Yes | $> 10.0\text{ m}$ | `0` (Low, $> 10\text{ m}$) | `1` (RAIM Active) |

*Table 25-3: ITU-R M.1371-6 Table 48 truth table for deriving AIS Position Accuracy and RAIM flags.*

> **Worked example.** Deriving PA and RAIM flags from NMEA sentence feeds.
> A vessel navigation receiver outputs standard IEC 61162-1 sentences to the transponder:
> ```text
> $GPGNS,120015.00,4220.0000,N,07036.0000,W,AA,08,1.1,5.2,12.0,,*42
> $GPGBS,120015.00,4.2,3.8,11.5,,,,*45
> ```
> 1. The `$GPGNS` sentence mode indicators are `AA` (Autonomous GPS/GLONASS). No differential corrections are active.
> 2. The `$GPGBS` sentence is valid, indicating active RAIM. It reports 1-sigma latitude error $\sigma_{\text{lat}} = 4.2\text{ m}$ and longitude error $\sigma_{\text{lon}} = 3.8\text{ m}$.
> 3. The transponder computes expected horizontal error:
> $$\sigma_H = \sqrt{4.2^2 + 3.8^2} = \sqrt{17.64 + 14.44} = \sqrt{32.08} \approx 5.66\text{ m}$$
> 4. Because RAIM is operational and $\sigma_H = 5.66\text{ m} \le 10.0\text{ m}$, the transponder encodes **PA = 1** and **RAIM = 1**. If satellite geometry degraded such that $\sigma_H = 11.01\text{ m}$, it would encode **PA = 0** and **RAIM = 1**.

Crucially, **PA = 1 does not guarantee sub-10 m error**. Any receiver with active SBAS corrections sets PA = 1 even when RAIM is inactive. Analysts must inspect both flags concurrently.

## 25.5 The EPFD type field

In addition to the single-bit PA flag, AIS carries a 4-bit **Type of Electronic Position-Fixing Device (EPFD)** field in static voyage reports (Message 5 for Class A, Message 19/24B for Class B) and Base Station Reports (Message 4).

Table 25-4 documents the standardized EPFD codes from ITU-R M.1371-6 Table 50:

| Code (Decimal) | Binary | Designated EPFD Source | Operational Significance |
|:---:|:---:|---|---|
| `0` | `0000` | Undefined (default) | Navigation sensor unclassified or missing |
| `1` | `0001` | **GPS** | Primary United States Global Positioning System |
| `2` | `0010` | **GLONASS** | Russian GLONASS constellation |
| `3` | `0011` | **Combined GNSS** | Combined fix (e.g. GPS + GLONASS / GPS + Galileo) |
| `4` | `0100` | **Loran-C** | Terrestrial low-frequency hyperbolic system |
| `5` | `0101` | **Chayka** | Russian low-frequency terrestrial system |
| `6` | `0110` | **Integrated navigation system** | Multi-sensor bridge fusion engine |
| `7` | `0111` | **Surveyed** | Centimeter-accurate surveyed coordinates (fixed AtoN / base) |
| `8` | `1000` | **Galileo** | European civilian constellation |
| `9` | `1001` | **BeiDou (BDS)** | Chinese global constellation |
| `10–11` | `1010–1011` | Reserved | Reserved for future allocation |
| `12` | `1100` | Integrated PNT system | Standardized under IMO MSC.401(95) |
| `13` | `1101` | Inertial navigation system (INS) | Autonomous gyro-accelerometer dead reckoning |
| `14` | `1110` | Terrestrial radio navigation | Terrestrial ranging systems (e.g. R-Mode) |
| `15` | `1111` | **Internal GNSS** | Fallback to internal transponder receiver |

*Table 25-4: Electronic Position-Fixing Device (EPFD) type codes under ITU-R M.1371-6 Table 50.*

**EPFD code 15 is a vital diagnostic flag**. On Class A vessels, the transponder normally broadcasts code `1` (GPS), `3` (combined GNSS), or `12` (integrated PNT) from the bridge EPFS. A sudden transition to EPFD `15` indicates that the bridge navigation feed has severed and the transponder has fallen back to its internal emergency GNSS engine.

## 25.6 DGNSS over AIS: Message 17 and beacon network retirement

Differential GNSS (**DGNSS**) overcomes atmospheric delays by broadcasting pseudo-range corrections computed at surveyed terrestrial coordinates. Historically, maritime DGNSS relied on medium-frequency radio beacons transmitting between 283.5 and 325 kHz under ITU-R M.823.

To eliminate separate MF receivers, the AIS protocol established **Message 17 (DGNSS Broadcast Binary Message)**. Under ITU-R M.1371-6 §A7-3.15, coastal base stations broadcast differential corrections directly over the VHF Data Link. Message 17 wraps the binary format of ITU-R M.823 / RTCM SC-104 corrections, stripping beacon preambles. Under IEC 62287-2, Class B SO transponders are required to evaluate Message 17 corrections when received over the VDL.

Despite its technical elegance, Message 17 saw limited adoption. Broadcasting corrections consumed scarce VHF slot capacity in congested waters. Simultaneously, satellite navigation improved:
1. Selective Availability ended in 2000, boosting civilian accuracy.
2. SBAS networks (WAAS, EGNOS) matured, broadcasting free differential corrections directly from orbit.
3. Multi-constellation tracking eliminated single-constellation geometry weaknesses.

Consequently, terrestrial beacon networks became redundant. In the United States, the Coast Guard announced the phased shutdown of the Nationwide DGPS service in the Federal Register (83 FR 12402, 21 March 2018). The USCG decommissioned its final 38 maritime DGPS beacons between September 2018 and September 2020. Similar decommissioning programs across Europe and Asia relegated Message 17 to specialized local port operations.

## 25.7 Systems without GNSS

While tracking applications assume every AIS icon represents a live satellite receiver, the standard accommodates several operational exceptions:
1. **Fixed Aids to Navigation with Surveyed Position (Type 1 & 2 AtoN):** Under IEC 62320-2 Table 1, an AIS AtoN on a permanent marine structure may operate in "Surveyed position only (no EPFS)" mode, broadcasting EPFD code `7`. However, a Type 1 AtoN has no VHF receiver and still requires an internal GNSS engine to maintain UTC slot timing.
2. **Synthetic and Virtual AtoNs:** Synthetic AtoNs mark physical buoys via transmissions sent from onshore base stations, while virtual AtoNs mark underwater hazards where no buoy exists. The shore base station uses its own GNSS clock to format Message 21 without requiring physical sensors at sea.
3. **Shore Base Stations with Precision Time Protocols:** AIS base stations under IEC 62320-1 can discipline their slot clocks using external standards, including 1PPS reference lines, IRIG-B, or IEEE 1588 Precision Time Protocol (**PTP**) over fiber-optic networks.
4. **Receive-Only Stations:** Receivers deployed by coastal monitors, VTS facilities, and amateur tracking networks do not transmit RF bursts. Under ITU-R M.1371-6 §A2-3.1.1, receive-only stations require no slot synchronization and do not require GNSS hardware.

## 25.8 Transponder behavior in GNSS-denied environments

When satellite signals fail—whether from antenna damage, solar storms, jamming, or spoofing—transponders undergo a deterministic cascade of operational degradations governed by ITU-R M.1371-6 and IEC standards.

```
GNSS Signal Loss Cascade
=============================================================================
1. SENSOR TIMEOUT (0–5 seconds):
   - Satellite tracking ceases; NMEA position feed terminates.
-----------------------------------------------------------------------------
2. STATUS SENTINEL INSERTION (Next Position Report):
   - Time Stamp field sets status sentinel:
     * 61 = Manual input mode (coordinates typed into bridge MKD)
     * 62 = Dead Reckoning / Estimated mode (INS projection)
     * 63 = Positioning system inoperative (total failure)
   - Position Accuracy (PA) flag drops to 0 (Low).
-----------------------------------------------------------------------------
3. CLASS-SPECIFIC TRANSMISSION BEHAVIOR:
   - Class A: Falls back to internal GNSS. If internal also fails, transmits
     sentinels 61/62/63 with last known position or 181°/91° default.
   - Class B SO: Free-runs slot reservation clock; halts transmission if
     satellite sync cannot be maintained.
   - Class B CS: Under M.1371-6 §A6-3.3, MUST CEASE TRANSMISSION of
     Messages 18 and 24 immediately unless interrogated.
-----------------------------------------------------------------------------
4. SYNCHRONIZATION HIERARCHY DEGRADATION:
   - Sync State degrades: 0 (UTC direct) --> 1 (indirect) --> 2 (base) --> 3.
   - Fixed AtoN sets "Off-position" flag in Message 21 (GNSS Anomaly).
=============================================================================
```

In position reports (Messages 1, 2, 3, 18), the 6-bit `Time stamp` field represents the second of the UTC minute (0–59) when the fix was generated. Under Table 47, values 60 through 63 serve as operational sentinels:
- **60 (Default / Unavailable):** Time stamp unavailable.
- **61 (Manual Input Mode):** Positioning failed; bridge watchkeeper is manually typing coordinates into the Minimum Keyboard and Display (**MKD**).
- **62 (Estimated / Dead Reckoning Mode):** Satellite fix lost; inertial or gyro/log dead reckoning is projecting position.
- **63 (Positioning System Inoperative):** All satellite and dead reckoning systems have failed completely.

Under IEC standards, Class B CS transponders cannot broadcast sentinels 61–63; when the internal GNSS fails, M.1371-6 Annex 6 (§A6-3.3) dictates that the station **must cease transmitting Messages 18 and 24**.

If forced to broadcast dynamic reports with no fix available from switch-on, transponders transmit standardized **out-of-range sentinel coordinates**: Longitude $181^\circ$ (`0x6791AC0`), Latitude $91^\circ$ (`0x3412140`), SOG $102.3\text{ kn}$ (`1023`), and COG $360.0^\circ$ (`3600`).

Under Table 71, Message 21 broadcast by fixed AtoNs includes an **Off-Position Flag** set if internal GNSS position exceeds the installed threshold. Because fixed beacons cannot drift, this bit functions as an autonomous regional GNSS anomaly detector.

## 25.9 Jamming and spoofing signatures in AIS data

Maritime satellite receivers operate with weak signal levels (approximately $-127\text{ to }-130\text{ dBm}$), leaving them vulnerable to radio frequency interference (**RFI**). The IMO Maritime Safety Committee issued Circular MSC.1/Circ.1644 on 28 October 2021 (*Deliberate Interference with the Global Navigation Satellite System and Other Radionavigation Services*), urging Member States to refrain from jamming and adopt resilient PNT architectures per MSC.1/Circ.1575.

In AIS monitoring feeds, GNSS interference generates distinct signatures:

```
+----------------------------------------------------------------------------+
|                       GNSS JAMMING VS. SPOOFING IN AIS                     |
+----------------------------------------------------------------------------+
| INDICATOR                  | GNSS JAMMING (DENIAL) | GNSS SPOOFING (DECEPTION)|
+----------------------------+-----------------------+-----------------------+
| Position Jump              | Absent (Fix Ceases)   | Massive / Non-physical|
| Time Stamp Field           | Sentinels 60, 62, 63  | Plausible (0–59)      |
| Position Accuracy (PA) Flag| Drops from 1 to 0     | Frequently Remains 1  |
| RAIM Flag                  | Inactive (0)          | Discrepancy / Inactive|
| Vessel SOG / COG           | Drops to 102.3 kn     | Unrealistic Kinematics|
| Class B Station Count      | Abrupt Drop (Silent)  | Preserved (Drifting)  |
| Regional Spatial Pattern   | Disappearance of Craft| Flocking / Rings      |
+----------------------------------------------------------------------------+
```

### Signatures of GNSS jamming
1. **Disappearance of Class B Transponders:** Mandated to silence transmissions upon losing satellite lock, small craft vanish simultaneously from monitoring feeds.
2. **Sentinel Influx:** Class A vessels transition en masse to Time Stamp `63` (inoperative) or `62` (dead reckoning).
3. **Sync State Degradation:** Transponders abandon Sync State `0` (UTC direct), shifting to Sync State `1` (indirect) or `2` (base direct).

### Signatures of GNSS spoofing
Unlike brute-force jamming, spoofing emitters broadcast synthetic satellite signals. Victim receivers compute synthetic positions dictated by the attacker, leaving distinct forensic fingerprints (Androjna et al. 2021; Spravil et al. 2023):
- **Airport Relocation:** Commercial vessels operating in coastal waters report coordinates centered on inland airports due to terrestrial spoofers triggering drone geofencing firmware.
- **Vessel Flocking and Circular Drift:** Anchored vessels report synchronized circular drift tracks while physically stationary.
- **Kinematic Inconsistencies:** Vessels report 30-mile position jumps between consecutive reports (implied speeds exceeding $50,000\text{ kn}$) while reported SOG remains $0.1\text{ kn}$.

> **Case file.** The Black Sea GPS spoofing advisory (June 2017).
> On 22 June 2017, the US Maritime Administration issued Advisory 2017-005A (*Black Sea – GPS Interference*). A commercial tanker anchored off Novorossiysk reported that its GPS navigation receiver indicated it was located 25 nautical miles inland at Gelendzhik Airport ($44^\circ 35'\text{ N}, 038^\circ 00'\text{ E}$). At least 20 surrounding commercial vessels confirmed identical false airport coordinates. Their Class A transponders broadcast these coordinates over the VDL, populating ship-tracking databases with ghost vessels anchored on an airport runway.

> **Threat model.** Maritime GNSS spoofing and AIS position manipulation.
> - **Attacker:** Electronic warfare units, paramilitary forces, or coastal actors operating software-defined radios and RF power amplifiers.
> - **Capability:** Generation of phase-synchronized GNSS false signals (GPS L1, GLONASS) with higher received power than authentic satellite signals.
> - **Impact:** Manipulation of ECDIS displays, false CPA alarms, and corruption of regional maritime surveillance.
> - **Mitigation:** Shipborne deployment of multi-constellation multi-frequency (**MCMF**) receivers, Controlled Reception Pattern Antennas (**CRPA**), NMEA sentence integrity monitoring (`$GPGNS`, `$GPGBS`, `$GPRMC`), and radar cross-validation.

> **Legal note.** Electronic interference and radio safety treaties.
> Deliberate transmission of radio signals intended to jam or spoof GNSS violates Article 15 of the ITU Radio Regulations (*Interference*). Because GNSS is part of the Worldwide Radionavigation System (**WWRNS**) governed by IMO Resolution A.1046(27), jamming or spoofing navigation signals in international waters violates SOLAS Chapter V (Regulation 19) and subjects operators to criminal penalties under national maritime legislation.

## 25.10 GNSS-independent backups and alternative PNT

Vulnerability of satellite navigation has accelerated development of **Alternative Position, Navigation, and Timing (A-PNT)** systems capable of sustaining maritime navigation during satellite outages.

```
+----------------------------------------------------------------------------+
|                        MARITIME A-PNT RESILIENCE STACK                     |
+----------------------------------------------------------------------------+
| 1. SATELLITE TIER (Primary)                                                |
|    - Multi-constellation, multi-frequency GNSS (GPS + Galileo + BDS + GLO) |
|    - Satellite-based augmentations (WAAS, EGNOS, MSAS)                     |
+----------------------------------------------------------------------------+
| 2. TERRESTRIAL RADIO RANGING (Terrestrial A-PNT)                           |
|    - R-Mode on Medium Frequency (MF) Radio Beacons (10–30 m accuracy)      |
|    - R-Mode on VHF Data Exchange System (VDES) / AIS (~10 m accuracy)      |
|    - Enhanced Loran (eLoran) Dual-Chain Systems (< 20 m accuracy)          |
+----------------------------------------------------------------------------+
| 3. ONBOARD SENSOR FUSION (Dead Reckoning & Vision)                         |
|    - Inertial Navigation Systems (INS) with Ring Laser / Fiber-Optic Gyros |
|    - Doppler Velocity Logs (DVL) measuring acoustic sea-floor tracking     |
|    - Marine Radar Coastline Matching & Chart Correlation                   |
+----------------------------------------------------------------------------+
```

### R-Mode (Ranging Mode)
Ranging Mode (**R-Mode**) overlays precision ranging signals onto maritime radio infrastructure without new frequency allocations:
- **MF R-Mode:** Modifies existing DGNSS beacons (283.5–325 kHz). Gewies et al. (2023) demonstrated that eight synchronized MF beacons across the southern Baltic achieved 10–30 m horizontal positioning accuracy during daytime. Rizzi et al. (2023) confirmed optimal accuracy of 15.1 m (95%), degrading to 55.3 m under night-time sky-wave conditions.
- **VHF R-Mode (AIS & VDES):** Operates across the VHF band using AIS and VDES base station infrastructure. As investigated by Johnson and Swaszek (2014) in ACCSEAS and analyzed by Šafář et al. (2019), VDES waveforms provide superior ranging performance compared to AIS GMSK bursts, achieving horizontal accuracies of approximately 10 m under IALA Guideline G1158.

### Enhanced Loran (eLoran)
Operating in the 90–110 kHz low-frequency band, eLoran broadcasts megawatt-level groundwave pulses immune to low-power microwave GNSS jamming. While the US and UK terminated legacy operations in 2010 and 2015, Kim et al. (2021) documented the operational commissioning of the Republic of Korea's dual-chain eLoran system on 1 June 2021. Designed to counter persistent GPS jamming, the Korean network achieves horizontal accuracy under 20 m (95%). In the US, the National Timing Resilience and Security Act of 2018 (P.L. 115-282 §514) mandates development of a terrestrial timing backup.

### Bridge sensor fusion
Modern Integrated Navigation Systems (**INS**) governed by IMO MSC.1/Circ.1575 incorporate mathematical sensor fusion. By coupling multi-constellation GNSS with gyrocompasses, Doppler Velocity Logs (**DVL**), and inertial sensors, the navigation system maintains an autonomous track vector, switching AIS broadcasts to Estimated / Dead Reckoning mode (Time Stamp sentinel `62`) when satellite fixes degrade.

## Then & now

- **⟨H⟩ 1998:** IMO adopts Resolution MSC.74(69) Annex 3, defining AIS performance standards; specifies 1/10,000 minute resolution in WGS-84 but deliberately avoids mandating GPS by name.
- **⟨H⟩ 2000:** The United States discontinues GPS Selective Availability on 2 May 2000, improving civilian positioning accuracy from ~100 m to 3–5 m.
- **⟨+⟩ 2003:** The US FAA commissions WAAS on 10 July 2003; commercial maritime receivers begin incorporating SBAS demodulators for autonomous differential corrections.
- **⟨+⟩ 2006:** Recommendation ITU-R M.1371-1 introduces Message 17 for broadcasting DGNSS corrections over the AIS VHF Data Link.
- **⟨+⟩ 2011:** GLONASS restores its 24-satellite baseline; European EGNOS declares Safety-of-Life service.
- **⟨+⟩ 2015:** IMO adopts Resolution MSC.401(95), establishing performance standards for multi-system shipborne radionavigation receivers.
- **⟨+⟩ 2016:** Galileo declares Initial Services on 15 December 2016, launching the first civilian-governed global satellite constellation.
- **⟨+⟩ 2017:** MARAD Advisory 2017-005A reports widespread GPS spoofing in the Black Sea, documenting commercial ships broadcasting false airport coordinates over AIS.
- **⟨+⟩ 2018:** The US Coast Guard publishes 83 FR 12402, announcing the phased termination of the Nationwide DGPS beacon network due to high-accuracy satellite signals and SBAS.
- **⟨+⟩ 2020:** China formally commissions the completed BeiDou-3 global constellation on 31 July 2020.
- **⟨+⟩ 2021:** Republic of Korea declares operational status for its national eLoran dual-chain network on 1 June 2021 to ensure navigation resilience against regional GNSS denial.
- **⟨+⟩ 2026:** Recommendation ITU-R M.1371-6 formalizes modern AIS message structure, multi-constellation EPFD assignments, and timing discipline.

## On the wire

Let us examine how GNSS coordinates, status sentinels, and integrity flags appear within raw NMEA 0183 sentences transmitted across the VHF Data Link.

### Reading Position Accuracy and RAIM in Message 1
Consider a standard Class A position report (Message 1) broadcast by a commercial vessel in coastal waters:

```text
!AIVDO,1,1,,A,15MwpU@01prtlJ0H9J@<CanN0000,0*5B
```

Decoding the binary bitstream reveals the encoding of position and integrity flags:
- **Message Type (bits 0–5):** `000001` (Type 1 = Position Report Class A).
- **MMSI (bits 8–37):** `366999701`.
- **Position Accuracy (bit 60):** `1` (High accuracy, $\le 10\text{ m}$).
- **Longitude (bits 61–88):** `1110011111101111110000000000` (Two's complement signed integer = $-42,360,000$). Dividing by 600,000 yields $-70.60000^\circ$ ($70^\circ 36.0000'\text{ W}$).
- **Latitude (bits 89–115):** `000110000010111100011000000` (Two's complement signed integer = $25,320,000$). Dividing by 600,000 yields $+42.20000^\circ$ ($42^\circ 12.0000'\text{ N}$).
- **Time Stamp (bits 137–142):** `001111` (Decimal **15** = Fix generated at second 15 of the UTC minute).
- **RAIM Flag (bit 148):** `0` (RAIM not in use).

Because Position Accuracy is `1` while RAIM is `0`, reference to Table 25-3 reveals that this vessel operates with differential corrections (SBAS or DGPS) without active receiver fault exclusion monitoring.

### Reading the GNSS-Denied Inoperative Sentinel (Time Stamp 63)
When satellite signals fail completely and dead reckoning is unavailable, the transponder switches to sentinel values:

```text
!AIVDO,1,1,,A,15MwpU@01pJtlJ0H9J@<Caov0000,0*55
```

Decoding bits 137–142:
- **Time Stamp (bits 137–142):** `111111` (Decimal **63**).

The value 63 informs receiving stations and VTS surveillance centers that the navigation sensor is inoperative. The coordinates carried in the message represent stale buffered data or manual entry.

### Reading Default Sentinel Coordinates
If a transponder transmits dynamic reports with no position fix available from switch-on, it broadcasts standardized out-of-range coordinates:

```text
!AIVDO,1,1,,A,15MwpUOP?w<tSF0l4Q@>4?wv0000,0*78
```

Extracting positional bitfields:
- **Longitude (bits 61–88):** `0110011110010001101011000000` (Hex `0x6791AC0` = Decimal 108,600,000). Divided by 600,000, this yields $+181.0000^\circ$ (Longitude unavailable).
- **Latitude (bits 89–115):** `0011010000010010000101000000` (Hex `0x3412140` = Decimal 54,600,000). Divided by 600,000, this yields $+91.0000^\circ$ (Latitude unavailable).
- **SOG (bits 46–55):** `1111111111` (Decimal 1023 = $102.3\text{ kn}$, speed unavailable).
- **COG (bits 116–127):** `111000010000` (Decimal 3600 = $360.0^\circ$, course unavailable).
- **Heading (bits 128–136):** `111111111` (Decimal 511 = Heading unavailable).
- **Time Stamp (bits 137–142):** `111111` (Decimal 63 = Positioning system inoperative).

### Reading the EPFD Source in Message 4
Fixed base stations transmit Base Station Reports (Message 4) that carry the 4-bit EPFD type field:

```text
!AIVDO,1,1,,A,403Ovl1v`Gd00rs=oPH?A@?00000,0*38
```

Inspecting bits 134–137 of the 168-bit Message 4 payload:
- **EPFD Type (bits 134–137):** `1111` (Decimal **15**).

EPFD code 15 confirms that this base station is operating from its internal GNSS receiver rather than an external surveyed geodetic reference standard.

## Validation, uncertainty & data quality

Because AIS dynamic messages are populated from satellite navigation feeds, errors in the space segment, bridge serial interfaces, or transponder firmware propagate directly into telemetry archives. Data pipelines must implement validation procedures to isolate compromised fixes:

```
Raw AIS Stream  ----->  Sentinel Filter  ----->  Kinematic Gate  ----->  Trajectory Clean
(NMEA / Parquet)        (Drop 61-63, 181/91)     (Speed & Accel Caps)    (Clean Trajectory DB)
```

Data engineering pipelines should execute three concrete quality audits:
1. **Sentinel Coordinate Rejection:** Filter out position reports where Longitude equals $181.0^\circ$ or Latitude equals $91.0^\circ$. Naive spatial bounding box queries fail when these values are cast into projected coordinate reference systems (e.g. EPSG:3857), triggering database ingestion exceptions.
2. **Time Stamp Sentinel Isolation:** Never parse bits 137–142 as an integer second without range checking. Values 60, 61, 62, and 63 must be directed into status columns. Treating 63 as a numeric second introduces an artificial 63-second timestamp into time-series analysis.
3. **Kinematic Jump and Velocity Validation:** Calculate implied speed over water between consecutive fixes: $v_{\text{implied}} = d_{\text{haversine}}(p_k, p_{k-1}) / \Delta t$. If $v_{\text{implied}} > v_{\text{max}}$ ($45\text{ kn}$ for commercial vessels or $60\text{ kn}$ for high-speed craft), flag the fix as a candidate GNSS jump or spoofing event.

> **Try it.** Validating PA/RAIM flags and status sentinels using `pyais`.
> The following Python script decodes raw AIS position sentences, extracts Position Accuracy and RAIM integrity flags, and identifies GNSS operational sentinels.
>
> ```python
> import pyais
> 
> test_sentences = [
>     "!AIVDO,1,1,,A,15MwpU@01pJtlJ0H9J@<CanN0000,0*53",  # Uncorrected, no RAIM (PA=0, RAIM=0)
>     "!AIVDO,1,1,,A,15MwpU@01prtlJ0H9J@<CanN0000,0*5B",  # DGNSS corrected (PA=1, RAIM=0)
>     "!AIVDO,1,1,,A,15MwpU@01prtlJ0H9J@<CanN2000,0*59",  # RAIM active <= 10m (PA=1, RAIM=1)
>     "!AIVDO,1,1,,A,15MwpU@01pJtlJ0H9J@<Caov0000,0*55",  # GNSS Inoperative (Sec=63)
> ]
> 
> for s in test_sentences:
>     msg = pyais.decode(s)
>     sec = msg.second
>     status = "Normal" if sec < 60 else {60: "Unavailable", 61: "Manual", 62: "Estimated", 63: "Inoperative"}.get(sec)
>     print(f"MMSI: {msg.mmsi} | PA: {int(msg.accuracy)} | RAIM: {int(msg.raim)} | Fix Sec: {sec:2d} ({status:11s}) | Lat: {msg.lat:7.4f} Lon: {msg.lon:8.4f}")
> ```
>
> **Expected output:**
> ```text
> MMSI: 366999701 | PA: 0 | RAIM: 0 | Fix Sec: 15 (Normal     ) | Lat: 42.2000 Lon: -70.6000
> MMSI: 366999701 | PA: 1 | RAIM: 0 | Fix Sec: 15 (Normal     ) | Lat: 42.2000 Lon: -70.6000
> MMSI: 366999701 | PA: 1 | RAIM: 1 | Fix Sec: 15 (Normal     ) | Lat: 42.2000 Lon: -70.6000
> MMSI: 366999701 | PA: 0 | RAIM: 0 | Fix Sec: 63 (Inoperative) | Lat: 42.2000 Lon: -70.6000
> ```

## Software

Tooling for analyzing GNSS data, evaluating satellite integrity, and diagnosing AIS positioning errors spans open source, free specialized utilities, and commercial platforms:

**Open source:**
- **pyais:** Python library for decoding and encoding raw AIS NMEA sentences. Extracts 6-bit binary bitfields, decodes Position Accuracy and RAIM flags, parses EPFD types, and isolates status sentinels 60–63. *Caveat:* Parses fields as Python datatypes but does not perform kinematic trajectory smoothing.
- **RTKLIB:** Open-source program package for standard and precise positioning with GNSS (GPS, GLONASS, Galileo, BeiDou, QZSS, SBAS). Supports real-time positioning and RTCM stream decoding. *Caveat:* Designed for raw GNSS pseudo-range processing; does not parse AIS VDL packets directly.
- **GNSSTk:** Open-source C++ suite developed by Applied Research Laboratories at the University of Texas at Austin. Provides algorithms for GNSS processing, cycle slip detection, and ionospheric modeling. *Caveat:* Requires advanced knowledge of satellite orbital mechanics.

**Free but closed:**
- **u-center (u-blox):** Evaluation software for commercial GNSS receivers. Displays real-time satellite constellations, signal-to-noise ratios, deviation maps, and NMEA `$GPGBS` fault isolation messages. *Caveat:* Proprietary to u-blox hardware; cannot interface directly with third-party transponders.
- **OpenCPN:** Chartplotter and navigation display software. Reads live AIS NMEA data streams, displays vessel targets on electronic charts, and warns mariners of lost targets. *Caveat:* Relies on host PC operating system clocks to calculate CPA/TCPA alarms.

**Commercial:**
- **Spire Maritime Automated Interference Detection:** Satellite monitoring service that ingests global satellite-AIS telemetry, identifies spatial cluster anomalies, and flags regional GNSS jamming and spoofing activity. *Caveat:* Closed commercial dataset requiring enterprise subscription licensing.
- **Furuno FA-170 Diagnostic Tool:** Maintenance utility used by marine service technicians to inspect Class A transponder health, read internal GNSS signal lock status, and calibrate bridge EPFS serial inputs. *Caveat:* Proprietary field software restricted to authorized Furuno service dealerships.

## Standards & guides

- **International Maritime Organization (IMO):** *Resolution MSC.74(69), Annex 3 (1998)* — Recommendation on performance standards for a universal shipborne Automatic Identification System (AIS). Mandates position processing in WGS-84 with 1/10,000 minute resolution.
- **International Maritime Organization (IMO):** *Resolution A.1106(29) (2015)* — Revised guidelines for the onboard operational use of shipborne Automatic Identification Systems (AIS). Establishes internal GNSS requirements for timing purposes and position redundancy.
- **International Maritime Organization (IMO):** *Resolution A.1046(27) (2011)* — Worldwide Radionavigation System (WWRNS). Defines operational recognition criteria for satellite and terrestrial radionavigation systems.
- **International Maritime Organization (IMO):** *Resolution MSC.401(95) (2015)* — Performance standards for multi-system shipborne radionavigation receivers. Mandates multi-constellation processing for modern shipborne navigators.
- **International Maritime Organization (IMO):** *Circular MSC.1/Circ.1575 (2017)* — Guidelines for shipborne position, navigation and timing (PNT) data processing. Provides the resilience framework for multi-sensor data fusion.
- **International Maritime Organization (IMO):** *Circular MSC.1/Circ.1644 (2021)* — Deliberate interference with the Global Navigation Satellite System and other radionavigation services. Urges Member States to counter maritime jamming and spoofing.
- **International Telecommunication Union (ITU-R):** *Recommendation ITU-R M.1371-6 (2026)* — Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band. Governs Table 48 (PA/RAIM), Table 50 (EPFD types), Annex 6 (Class B CS internal GNSS), and Annex 7 (Message 17).
- **International Telecommunication Union (ITU-R):** *Recommendation ITU-R M.823-3 (2006)* — Technical characteristics of differential transmissions for global navigation satellite systems from maritime radio beacons. Governs DGNSS correction structures.
- **International Electrotechnical Commission (IEC):** *IEC 61993-2:2018 (Edition 3.0)* — Class A shipborne equipment: Operational and performance requirements, methods of test and required test results. Enforces internal GNSS requirements and position backup switching.
- **International Electrotechnical Commission (IEC):** *IEC 62287-1:2017 (Edition 3.0)* — Class B shipborne equipment: Carrier-sense TDMA (CSTDMA). Governs Class B CS internal GNSS mandates and cessation of transmission upon fix loss.
- **International Electrotechnical Commission (IEC):** *IEC 62287-2:2017 (Edition 2.0)* — Class B shipborne equipment: Self-organising TDMA (SOTDMA). Mandates exclusive reliance on internal GNSS and prohibits external position inputs.
- **International Electrotechnical Commission (IEC):** *IEC 62320-2:2016 (Edition 2.0)* — AIS Aids to Navigation (AtoN). Governs Type 1/2/3 AtoN positioning modes and surveyed position operations.
- **International Electrotechnical Commission (IEC):** *IEC 61108-1:2003 (Edition 2.0)* — Global navigation satellite systems (GNSS) -- Part 1: Global positioning system (GPS) -- Receiver equipment. Defines type-approval standards for shipborne GPS navigators.
- **International Electrotechnical Commission (IEC):** *IEC 61162-1:2016 (Edition 5.0)* — Digital interfaces: Single talker and multiple listeners. Governs NMEA 0183 sentences (`$GPGNS`, `$GPGGA`, `$GPGBS`).
- **International Association of Marine Aids to Navigation and Lighthouse Authorities (IALA):** *Guideline G1158 (2024, Edition 2.0)* — VDES R-Mode. Establishes technical guidance for VHF terrestrial ranging augmentations.
- **United States Coast Guard (USCG):** *83 FR 12402 (2018)* — Discontinuance of the Nationwide Differential Global Positioning System (NDGPS). Formal rulemaking governing the phased decommissioning of maritime DGPS beacons.

## Pitfalls

- **Assuming Position Accuracy 1 guarantees high precision:** Under Table 48, any receiver receiving SBAS corrections (or falsely flagged as DGPS) outputs PA = 1 even when RAIM is completely inactive.
- **Parsing status sentinels 60–63 as seconds:** Treating values $\ge 60$ as numeric elapsed seconds introduces severe 60-second spikes into trajectory reconstruction algorithms.
- **Treating out-of-range coordinates ($181^\circ / 91^\circ$) as geographic data:** Projecting sentinel coordinates ($181^\circ\text{ E}, 91^\circ\text{ N}$) into planar coordinate reference systems triggers geometry parsing exceptions in spatial databases.
- **Assuming Class B transponders broadcast external bridge GPS data:** Class B transponders are prohibited from accepting external NMEA position inputs; they broadcast only their internal receiver fix.
- **Believing Class B CS transponders broadcast dead reckoning:** Class B CS transponders cannot use status sentinels 61–63; when internal GNSS fails, they must cease broadcasting immediately.
- **Ignoring EPFD code 15 in Class A data:** A sudden switch from EPFD 1 (GPS) to EPFD 15 (Internal GNSS) indicates that the vessel's primary bridge navigation feed has severed.
- **Confusing multi-constellation support with four-constellation concurrent tracking:** Many 72-channel commercial transponders track only two or three constellations simultaneously due to internal baseband channel limits.
- **Relying on AIS positions to prove vessel presence during electronic warfare:** In contested coastal waters, spoofing emitters can project dozens of ghost vessels across inland terrain or generate false circular drift tracks.

## Key takeaways

- **Dual-role GNSS architecture:** Class A transponders require an internal GNSS engine for UTC slot timing and emergency position fallback, while normally broadcasting coordinates from the primary bridge EPFS.
- **Exclusive internal requirement for Class B:** Under IEC 62287, Class B SO and CS transponders rely exclusively on their internal GNSS receiver; external position sensor inputs are prohibited.
- **Global constellation transition:** Commercial hardware has evolved from legacy 12-channel GPS-only engines (pre-2011) to 72-channel multi-constellation receivers supporting GPS, GLONASS, Galileo, and BeiDou.
- **Table 48 integrity logic:** Transponders derive Position Accuracy and RAIM bits from receiver `$GPGBS` and `$GPGNS` sentences; PA = 1 can represent differential corrections without active RAIM fault exclusion.
- **Diagnostic value of EPFD 15:** EPFD code 15 flags that a Class A vessel has lost its primary bridge navigation feed and is broadcasting from its internal backup receiver.
- **Message 17 retirement:** As Selective Availability ended and SBAS matured, maritime administrations phased out terrestrial DGNSS radio beacons, rendering Message 17 largely obsolete.
- **Strict cessation rules:** When satellite positioning fails, Class A transponders broadcast sentinels 61–63, whereas Class B CS units must cease transmission entirely.
- **Fixed AtoNs as jamming detectors:** Message 21 off-position flags broadcast by fixed aids at surveyed coordinates serve as autonomous regional GNSS interference monitors.
- **Emergence of A-PNT backups:** Terrestrial R-Mode on MF beacons (10–30 m accuracy) and VDES (~10 m accuracy), alongside eLoran (< 20 m), provide essential sovereign backups against satellite denial.

## References

- ACCSEAS (2014). *Feasibility Study of R-Mode Using AIS Transmissions: Part 1 -- Concept Evaluation and Performance Bounds* (Report Issue 1.0 Final). Hamburg: ACCSEAS Project.
- Androjna, A., Perkovič, M., Pavić, I. & Mišković, L. (2021). AIS Data Vulnerability Indicated by a Spoofing Case-Study. *Applied Sciences*, 11(11):5015. doi:10.3390/app11115015
- Gewies, S., Hoppe, M., Rizzi, C., Grundhöfer, K. & Ziebold, R. (2023). R-Mode -- Terrestrial Navigation for Maritime Users. In *Proceedings of the 36th International Technical Meeting of the Satellite Division of The Institute of Navigation (ION GNSS+ 2023)*, pages 3125–3134. Denver: Institute of Navigation.
- Harati-Mokhtari, A., Wall, A., Brooks, P. & Wang, J. (2007). Automatic Identification System (AIS): Data Reliability and Human Error Implications. *The Journal of Navigation*, 60(3):373–389. doi:10.1017/S0373463307004298
- IALA (2024). *VDES R-Mode* (Guideline G1158, Edition 2.0). Saint-Germain-en-Laye: International Association of Marine Aids to Navigation and Lighthouse Authorities.
- IEC (2003). *IEC 61108-1:2003 -- Maritime navigation and radiocommunication equipment and systems -- Global navigation satellite systems (GNSS) -- Part 1: Global positioning system (GPS) -- Receiver equipment -- Performance standards, methods of testing and required test results*. Edition 2.0. Geneva: International Electrotechnical Commission.
- IEC (2016). *IEC 61162-1:2016 -- Maritime navigation and radiocommunication equipment and systems -- Digital interfaces -- Part 1: Single talker and multiple listeners*. Edition 5.0. Geneva: International Electrotechnical Commission.
- IEC (2016). *IEC 62320-2:2016 -- Maritime navigation and radiocommunication equipment and systems -- Automatic identification system (AIS) -- Part 2: AIS Aids to Navigation (AtoN) -- Minimum operational and performance requirements, methods of testing and required test results*. Edition 2.0. Geneva: International Electrotechnical Commission.
- IEC (2017). *IEC 62287-1:2017 -- Maritime navigation and radiocommunication equipment and systems -- Class B shipborne equipment of the automatic identification system (AIS) -- Part 1: Carrier-sense time division multiple access techniques (CSTDMA)*. Edition 3.0. Geneva: International Electrotechnical Commission.
- IEC (2017). *IEC 62287-2:2017 -- Maritime navigation and radiocommunication equipment and systems -- Class B shipborne equipment of the automatic identification system (AIS) -- Part 2: Self-organising time division multiple access (SOTDMA) techniques*. Edition 2.0. Geneva: International Electrotechnical Commission.
- IEC (2018). *IEC 61993-2:2018 -- Maritime navigation and radiocommunication equipment and systems -- Automatic Identification Systems (AIS) -- Part 2: Class A shipborne equipment of the automatic identification system (AIS) -- Operational and performance requirements, methods of test and required test results*. Edition 3.0. Geneva: International Electrotechnical Commission.
- IMO (1998). *Adoption of New and Amended Performance Standards for Navigation Technology: Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (Resolution MSC.74(69), Annex 3). London: International Maritime Organization.
- IMO (2011). *Worldwide Radionavigation System* (Resolution A.1046(27)). London: International Maritime Organization.
- IMO (2015). *Performance Standards for Multi-System Shipborne Radionavigation Receivers* (Resolution MSC.401(95)). London: International Maritime Organization.
- IMO (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). London: International Maritime Organization.
- IMO (2017). *Guidelines for Shipborne Position, Navigation and Timing (PNT) Data Processing* (Circular MSC.1/Circ.1575). London: International Maritime Organization.
- IMO (2021). *Deliberate Interference with the Global Navigation Satellite System (GNSS) and Other Radionavigation Services* (Circular MSC.1/Circ.1644). London: International Maritime Organization.
- ITU-R (2006). *Technical Characteristics of Differential Transmissions for Global Navigation Satellite Systems (DGNSS) from Maritime Radio Beacons in the Frequency Band 283.5-315 kHz in Region 1 and 285-325 kHz in Regions 2 and 3* (Recommendation ITU-R M.823-3). Geneva: International Telecommunication Union.
- ITU-R (2026). *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Band* (Recommendation ITU-R M.1371-6). Geneva: International Telecommunication Union.
- Kim, M.-U., Son, P.-H., Park, S.-H., Park, K.-H. & Seo, J. (2021). Development and Initial Operational Test and Evaluation of the First Dual-Chain eLoran System in the Republic of Korea. *IEEE Transactions on Aerospace and Electronic Systems*, 57(6):3938–3952. doi:10.1109/TAES.2021.3086968
- Koch, V. & Gewies, S. (2020). Worldwide Availability of Maritime Medium-Frequency Radio Infrastructure for R-Mode-Supported Navigation. *Journal of Marine Science and Engineering*, 8(3):209. doi:10.3390/jmse8030209
- Maritime Administration (2017). *Maritime Security Communications with Industry Advisory 2017-005A: Black Sea -- GPS Interference* (Advisory 2017-005A). Washington, DC: U.S. Department of Transportation, Maritime Administration.
- Rizzi, C., Grundhöfer, K., Gewies, S. & Ehlers, P. (2023). Performance Evaluation of R-Mode in the Southern Baltic Sea. *Applied Sciences*, 13(3):1872. doi:10.3390/app13031872
- Šafář, M., Grant, A., Williams, P. & Ward, N. (2019). Performance Bounds for VDES R-Mode. *The Journal of Navigation*, 73(1):103–118. doi:10.1017/S0373463319000559
- Spravil, J., Hemminghaus, D., von Rechenberg, A., Padilla, M. & Bauer, J. (2023). Detecting Maritime GPS Spoofing Attacks Based on NMEA Sentence Integrity Monitoring. *Journal of Marine Science and Engineering*, 11(5):928. doi:10.3390/jmse11050928
- United States Coast Guard (2018). Discontinuance of the Nationwide Differential Global Positioning System (NDGPS). *Federal Register*, 83(55):12402–12404.
