# Chapter 36 — Failure modes of AIS hardware and software

> **Part V — Radio.** Transponders, antennas, and interface pipelines fail in characteristic ways that corrupt bridge situational awareness, distort global vessel tracking, and evade conventional built-in integrity tests.

**In this chapter.** You will learn how to diagnose, detect, and mitigate physical, firmware, configuration, and data-pipeline failures in the Automatic Identification System (**AIS**). You will dissect hardware faults including antenna mismatch, high voltage standing wave ratio (**VSWR**), coaxial feeder degradation, and radio frequency (**RF**) desensitization from marine light-emitting diode (**LED**) fixtures. You will trace firmware timing faults, comparing the 2008 GPS PRN-32 constellation expansion, leap-second software anomalies, and GPS week number rollover (**WNRO**) manifestations against physical receiver operations. You will analyze human configuration errors, identifying invalid Maritime Mobile Service Identity (**MMSI**) assignments, geometric antenna dimension distortions, absent heading and rate-of-turn (**ROT**) sensors, and stale voyage entries. You will evaluate link-layer degradation such as Class B carrier-sense slot starvation and regional channel management mis-commands. Finally, you will audit the regulatory annual testing regime under International Maritime Organization (**IMO**) circular MSC.1/Circ.1252, implement automated data quality verification scripts, and separate genuine sensor faults from intentional RF deception.

## 36.1 The anatomy of AIS failures

The Automatic Identification System is an autonomous broadcast network operating in the maritime VHF band ([Chapter 28](ch28-rf-encoding-physical-layer.md)). Designed for collision avoidance, Vessel Traffic Services (**VTS**), and coastal surveillance, AIS integrates internal VHF transceivers with bridge navigation sensors, serial networks, and satellite constellations ([Chapter 20](ch20-architecture-and-station-classes.md)). Because AIS operates without centralized coordination, failures within the onboard sensor chain, transceiver electronics, antenna system, or link software directly corrupt the broadcast data stream.

Failures in AIS manifest across four distinct domains:
1. **Radio frequency and physical hardware:** Physical degradation of VHF antennas, coaxial feeders, splitters, power supplies, and localized electromagnetic interference (**EMI**) that degrades receiver sensitivity.
2. **Firmware and GNSS timing engines:** Clock drift, improper handling of satellite almanac expansions, leap-second offsets, and week-counter rollovers that destabilize Time Division Multiple Access (**TDMA**) frame synchronization.
3. **Sensor integration and cabling:** Loss of primary heading or Rate of Turn sentences, improper grounding, faulty NMEA 0183 / IEC 61162-1 serial multiplexers, and physical pilot-plug wiring defects.
4. **Human configuration and operational oversight:** Uninitialized factory-default identifiers, invalid MMSIs, erroneous GNSS antenna reference offsets, unupdated navigational status flags, and stale voyage destinations.

Crucially, modern transponders feature built-in integrity testing (**BIIT**). However, as noted in IMO Resolution A.1106(29), BIIT functions primarily monitor hardware power rails, microprocessor watchdog timers, and basic synthesizer lock. The built-in tester cannot validate the *semantic truth* or *physical plausibility* of sensor inputs. If an external gyrocompass transmits valid NMEA sentences indicating a frozen heading of $090^\circ$ while the vessel completes a $180^\circ$ turn, the transponder faithfully modulates the erroneous heading onto the VHF data link (**VDL**), triggering spurious alarms on Electronic Chart Display and Information Systems (**ECDIS**) and distorting global analytics pipelines.

## 36.2 RF, antenna, and hardware failures

The RF front end connects the transponder's digital signal processor to the physical maritime electromagnetic environment. Physical faults in the antenna assembly, transmission line, or surrounding RF environment degrade transmission range and elevate packet error rates without necessarily triggering an immediate alarm on the transponder's Minimum Keyboard and Display (**MKD**).

### 36.2.1 Voltage Standing Wave Ratio (VSWR) and antenna feeder degradation

Under Recommendation ITU-R M.1371-6 and IEC 61993-2, a Class A transponder delivers a nominal RF output power of 12.5 W ($+41\text{ dBm}$) in high-power mode and 2 W ($+33\text{ dBm}$) in low-power mode into a 50 $\Omega$ load across 156.025 MHz to 162.025 MHz. The match between transmission line and antenna is quantified by the **Voltage Standing Wave Ratio** (**VSWR**):
$$\text{VSWR} = \frac{1 + |\Gamma|}{1 - |\Gamma|},\quad \Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$$
Ideal matching ($Z_L = Z_0 = 50\ \Omega$) yields $|\Gamma| = 0$ and $\text{VSWR} = 1.0:1$. At sea, coaxial feeders and antennas suffer severe stress:
- **Saltwater ingress:** Water corrodes PL-259 or Type N connectors and braids, increasing attenuation and elevating VSWR above $3.0:1$.
- **Whip fracture:** Mast vibrations cause metal fatigue or delamination, shifting resonant frequency off 162 MHz.
- **Feeder crushing:** Cables pinched in watertight doors or cable trays create impedance discontinuities.

When $\text{VSWR} \ge 3:1$ (return loss $<6\text{ dB}$, $>25\%$ reflected power), the power amplifier overheats. IEC 61993-2 requires Class A transponders to monitor VSWR and throttle RF output to prevent component damage (`AIS: Antenna VSWR exceed limit`). The operational signature is **range asymmetry**: the ship receives distant targets normally, but its own broadcasts fail beyond 2 to 4 nautical miles (nmi).

### 36.2.2 Active VHF antenna splitters and relay failures

Active splitters share one mast antenna between an AIS transponder and a VHF voice radio using low-noise amplifiers (**LNAs**) and high-speed relays. Their failure modes include:
- **Power loss:** Active splitters fail-safe to the voice radio when unpowered. Dropped DC power isolates the AIS unit, which transmits into an open circuit and alarms on VSWR.
- **Relay latency:** The splitter must switch in milliseconds when the 25 W voice radio keys. Relay wear leaks voice RF into the AIS receiver, damaging front-end diodes or LNAs.
- **Passive splitters:** Unamplified passive splitters impose 3 dB insertion loss and lack port isolation ($>30\text{ dB}$ required), coupling destructive RF into the AIS receiver.

### 36.2.3 LED lighting and electromagnetic interference (EMI)

Receiver desensitization from shipboard LED fixtures and switch-mode supplies is a silent failure mode. As documented in USCG Marine Safety Alert 13-18 (*Potential Interference of VHF-FM Radio and AIS Reception from LED Lighting*), poorly filtered LED drivers emit broad-spectrum noise across 156 MHz to 163 MHz.

Buck/boost converters in unshielded floodlights and navigation lanterns radiate harmonics into the 162 MHz AIS band. The transmitter operates at full power without hardware alarms, but the receiver noise floor rises by 10 dB to 25 dB (degrading sensitivity from $-107\text{ dBm}$ to $-90\text{ dBm}$ or worse). The reception radius collapses from 20 nmi to under 2 nmi when lights are energized.

> **Rule of thumb.** If your AIS reception range drops significantly at dusk or whenever deck floodlights are energized, suspect LED switch-mode driver interference. Execute the Coast Guard squelch test: tune an analog VHF radio to an unused channel, open the squelch until background hiss is heard, tighten squelch just until silent, and turn on the vessel's LED lights. If the radio squelch breaks open with loud static, your LED fixtures are poisoning your VHF and AIS receiver front ends.

### 36.2.4 Receiver desensitization during own-ship transmissions

Class A units house two TDMA receivers (161.975 and 162.025 MHz) and a DSC Channel 70 receiver (156.525 MHz), blanking them during own-ship 26.667 ms bursts. However, external desensitization occurs when adjacent VHF voice antennas lack separation ([Chapter 32](ch32-antennas.md)). IMO SN/Circ.227 requires $\ge 2\text{ m}$ separation from 25 W voice antennas. With separation $<1.5\text{ m}$, voice transmissions saturate the AIS front end, driving LNAs into compression and dropping packets on both TDMA channels.

## 36.3 GNSS and timing anomalies

TDMA requires microsecond-level synchronization across all participating stations ([Chapter 21](ch21-link-layer-tdma.md)). A 1-minute AIS frame contains 2,250 time slots of 26.667 ms (256 bits at 9,600 bit/s). Under ITU-R M.1371-6 Annex 2, mobile transmission timing error must remain within $\pm 104\ \mu\text{s}$ ($\pm 1$ bit) of the synchronization source, with accumulated timing error not exceeding $312\ \mu\text{s}$ ($\pm 3$ bits).

Transponders derive synchronization from Coordinated Universal Time (**UTC**) via an internal GNSS engine ([Chapter 24](ch24-timing.md) and [Chapter 25](ch25-gnss-and-ais.md)). When GNSS fixes fail, link timing degrades through predictable stages.

### 36.3.1 GNSS signal loss and the synchronization hierarchy

Losing satellite signals from antenna blockage, line faults, or jamming ([Chapter 62](ch62-gnss-jamming-spoofing.md)) forces transponders down the ITU-R M.1371-6 Annex 2 hierarchy:
1. **UTC direct (State 0):** Direct UTC lock to the GNSS 1PPS pulse.
2. **UTC indirect (State 1):** Sync to nearby mobile or base stations broadcasting State 0 (limited to one indirect tier).
3. **Base direct (State 2):** Lock to a shore base station (Message 4) heard at least twice within 40 seconds.
4. **Base indirect / Semaphore (State 3):** Sync to a base-linked station or an elected mobile semaphore station.

During GNSS denial, position reports broadcast standard sentinels: Latitude $91^\circ$ (`0x1A83854`), Longitude $181^\circ$ (`0x6791AC0`), Time Stamp `63` (inoperative) or `62` (estimated mode), and Position Accuracy `0`. If all sync sources vanish and clock drift exceeds jitter budgets, IEC 61993-2 mandates that the transponder cease transmission to prevent slot collisions.

> **Case file.** On 27 February 2008, the US Air Force activated GPS satellite PRN-32. Legacy, non-USCG-approved transponders whose internal GPS receivers did not strictly implement IS-GPS-200 failed to parse the 32nd code. Constellation tracking crashed: units stopped transmitting valid position reports (sending latitude $91^\circ$ and longitude $181^\circ$ sentinels or falling silent) while continuing to receive data and text messages. Fleet-wide firmware updates were required to restore tracking.

### 36.3.2 Leap seconds and firmware synchronization crashes

Leap seconds are periodically inserted into UTC to compensate for the difference between International Atomic Time (**TAI**) and Earth's rotational speed. GPS time is a continuous atomic time scale established on 6 January 1980 that does not introduce leap seconds. The GPS navigation message broadcasts the current leap-second offset within its subframe almanac data.

In September 2005, a firmware defect struck Saab R3 and R4 Class A transponders (Saab Announcement PT-05-0078; Norwegian Maritime Directorate SM 10/2005; USCG Marine Safety Alert 5-05). GPS controllers broadcast advance notice that a leap second would occur on 31 December 2005. The transponder's internal receiver applied the offset immediately in July 2005—nearly six months early.

The 1.0 s offset equaled 37.5 slots:
$$\Delta t = \frac{1.0\text{ s}}{0.0266667\text{ s/slot}} = 37.5\text{ slots}$$
Bursts began in the physical center of slots rather than boundaries. Each packet straddled two TDMA slots, causing collisions and preventing decoding across local cells.

### 36.3.3 GPS Week Number Rollover (WNRO)

Legacy GPS messages carry a 10-bit week counter, rolling over every 1,024 weeks (~19.6 years). While modern receivers use 13-bit CNAV words, older transponders embed 10-bit engines. Many firmware builds hardcode 1,024-week epochs based on compilation dates, creating staggered rollover dates across manufacturers: Furuno FA-100 on 20 December 2020, Furuno FA-150 on 2 January 2022, and JRC JHS-182/183 on 3 August 2025 (reverting to 23 January 2005; JRC Notice 2023).

Crucially, positioning survives WNRO: pseudorange trilateration, coordinates, SOG, COG, and 1PPS slot timing remain unaffected. Only date registers regress by 19.6 years, corrupting Message 4/11 dates and voyage logs.

## 36.4 Sensor integration and serial interface failures

Class A transponders ingest heading (`HDT`), rate of turn (`ROT`), speed through water (`VBW`), and ground track (`RMC`/`VTG`) over IEC 61162-1 serial links ([Chapter 26](ch26-interfaces-and-logging.md)).

### 36.4.1 Missing or corrupted heading data

True heading ($0.0^\circ$ to $359.0^\circ$) is bow orientation, fundamentally distinct from Course Over Ground (**COG**). Without an interfaced gyrocompass, transponders broadcast sentinel $\text{Heading} = 511$ (`0x1FF`). When under way ($\text{SOG} \ge 3\text{ kn}$), missing heading forces ECDIS displays to orient targets along COG or render ambiguous symbols. In heavy cross-currents or towing, heading and COG can diverge by $>30^\circ$, depriving bridge officers and algorithms of true vessel aspect.

### 36.4.2 Rate of Turn (ROT) sensor failures and mis-scalings

Rate of Turn is reported as an 8-bit signed integer: $0$ for steady course, $\pm 1$ to $\pm 126$ for sensor values, $\pm 127$ for unmeasured turns $>5^\circ/30\text{ s}$, and $-128$ (`0x80`) for not available. Installers connecting gyrocompasses without ROT output frequently configure transponders to numerically differentiate incoming `HDT` sentences. Quantization and latency inject noise, causing transponders to oscillate between $-127$ and $+127$ and generating false turning alarms on VTS displays.

### 36.4.3 NMEA multiplexer buffer overruns and fragment reassembly errors

Multiplexer buffer overruns and interleaving create distinct failure signatures:
- **Baud mismatches:** Routing 38,400 baud presentation streams into 4,800 baud ports overflows FIFOs, truncating sentences and failing checksums (`*hh`).
- **Sentence interleaving:** Payloads $>373$ bits require multi-part encapsulation (e.g., Message 5). If a multiplexer interleaves unrelated sentences between fragments, decoders abort reassembly and discard static vessel data.

### 36.4.4 Pilot plug wiring, corrosion, and power receptacle defects

Under SOLAS Chapter V and IMO SN/Circ.227, Class A vessels must provide a 9-pin **pilot plug** for Portable Pilot Units (**PPUs**). Common faults include:
- **Reversed differential polarity:** Inverting `TxA` and `TxB` lines blocks data recovery.
- **Pin corrosion:** Corrosion attenuates signals below the $\pm 200\text{ mV}$ RS-422 differential threshold.
- **Missing power sockets:** 33 CFR 164.46 requires an adjacent 120 V AC receptacle. Unpowered plugs deplete pilot batteries during critical transits.

## 36.5 Human and configuration errors

While electronic hardware and firmware failures occur unpredictably, human operational and configuration errors represent the largest single source of corrupted AIS data in global tracking repositories.

### 36.5.1 Default, zero, and invalid MMSIs

The Maritime Mobile Service Identity is a unique 9-digit decimal number allocated by national administrations conforming to ITU-R Recommendation M.585 ([Chapter 13](ch13-mmsi-deep-dive.md)). A valid ship station MMSI must begin with a recognized 3-digit Maritime Identification Digit (**MID**) between 201 and 775.

In global traffic streams, thousands of vessels transmit invalid or unprogrammed MMSIs:
- **Factory default MMSIs:** Nauticast transponders ship with default MMSI `1193046` and vessel name `NAUT`. When installers fail to enter the assigned ship identity, the unit transmits using this default.
- **Patterned place-holders:** Operators or installers enter obvious sequences such as `000000000`, `111111111`, or `123456789`.
- **National documentation numbers:** In the United States, commercial operators frequently enter their official documentation or state registration number into the MMSI field, producing invalid identifiers that fail ITU-R M.585 formatting.

When multiple vessels share a default MMSI, shore VTS systems and shipboard ECDIS displays correlate all reports to a single target record. The target appears to "teleport" hundreds of miles across consecutive reporting intervals, triggering false kinematic tracking alarms and overwhelming display consoles. Under US FCC regulations (47 CFR 80.231), retail Class B transponders are locked against user modification. Static data must be entered by a certified technician; when a vessel is sold, owners cannot update the unit themselves, resulting in obsolete or abandoned identities.

### 36.5.2 Dimensional errors and GNSS antenna reference offsets

In Message 5 (Class A) and Message 24 Part B (Class B), vessels broadcast overall hull dimensions and the precise internal location of the primary GNSS positioning antenna using four dimension offsets: $A$ (distance from bow to antenna), $B$ (antenna to stern), $C$ (port to antenna), and $D$ (antenna to starboard). The total vessel length is $A + B$, and total beam is $C + D$. Common dimensional failure modes include:
- **Zero dimensions:** Transponders broadcast $A=B=C=D=0$. ECDIS displays cannot render a scaled ship symbol and default to rendering the vessel as a dimensionless point.
- **Inverted A and B parameters:** Installers invert bow and stern offsets. On a 300 m container ship with the bridge located 50 m forward of the stern, entering $A=50$ and $B=250$ shifts the rendered hull 200 m forward of its true physical position.
- **Reference point offset omission:** Installers enter total vessel length into $A$ and beam into $C$, leaving $B=0$ and $D=0$. When docking or operating in narrow waterways, the ship's rendered hull contour appears entirely offset from the actual berth or navigation channel.

### 36.5.3 Stale voyage-related data

Unlike dynamic position reports generated automatically by sensors, static and voyage-related data (Message 5) require manual entry by ship's officers under IMO Resolution A.1106(29). Bridge watchstanders routinely neglect to update:
- **Navigational Status:** The 4-bit status field frequently remains set to `0` (Under way using engine) while the vessel is swinging at anchor for days, or remains set to `1` (At anchor) hours after departing port.
- **Static Draught:** Maximum present static draught ($0.1\text{ m}$ steps) is rarely updated to reflect cargo loading or ballast discharge.
- **Destination and Estimated Time of Arrival (ETA):** Vessels frequently broadcast past ETAs or destinations from previous voyages months prior, or enter humorous text strings that corrupt automated port-logistics scheduling.

## 36.6 Link-layer and operational failure modes

Even when transceiver hardware and bridge sensors are operating correctly, external link-layer phenomena and RF spectrum commands can disrupt normal AIS communications.

### 36.6.1 Class B Carrier-Sense (CSTDMA) slot starvation

Class B transponders operate in two distinct variants ([Chapter 20](ch20-architecture-and-station-classes.md)):
- **Class B/SO (IEC 62287-2):** Uses Self-Organizing TDMA at 5 W output power, reserving slots identical to Class A stations.
- **Class B/CS (IEC 62287-1):** Uses Carrier-Sense TDMA at 2 W output power.

A Class B CS station does not reserve slots in advance. Instead, it selects a candidate slot and executes carrier sensing in an $1,146\ \mu\text{s}$ detection window immediately following the slot start (from $833\ \mu\text{s}$ to $1,979\ \mu\text{s}$ after $T_0$). If detected RF power exceeds a dynamic threshold (typically $-107\text{ dBm}$ adjusted for local noise), the unit declares the slot busy, defers transmission, and searches for an alternative slot within its nomination window.

In dense waters (e.g., the Dover Strait or Singapore), Class A SOTDMA traffic claims available slots, causing Class B CS **slot starvation**. Units repeatedly detect carrier energy, exhaust nomination attempts, and drop reports. Cadence degrades from 30 s to minutes. As stated in UK MCA MGN 324 (M+F), this is designed protocol behavior: Class A safety broadcasts always take precedence over small craft.

### 36.6.2 Regional channel management mis-commands

Under ITU-R M.1371-6, coastal maritime authorities can remotely command AIS transponders to switch operating frequencies from default international channels (AIS 1 at 161.975 MHz and AIS 2 at 162.025 MHz) to designated regional channels via broadcast Message 22 or addressed DSC Channel 70 telecommands.

Regional channel transitions are subject to severe operational hazards:
- **Persistent transitional states:** Under M.1371, when a transponder enters the geographic boundary defined by a Message 22 broadcast, it switches to the designated regional channels. The transponder retains these channel assignments until overridden by another valid Message 22, until the vessel moves outside the specified geographic coordinates, or until manually cleared via the MKD.
- **USCG Safety Alert 07-10:** In 2010, the US Coast Guard issued Safety Alert 07-10 (*Caution to AIS Users*) following an incident where coastal stations in the Mid-Atlantic region inadvertently broadcast erroneous Message 22 channel management commands. Vessels navigating through the waters of Maryland, Delaware, Pennsylvania, New Jersey, and New York were automatically commanded onto non-standard frequencies. Affected transponders operated normally but became completely invisible to surrounding vessels and shore stations listening exclusively on default AIS 1 and AIS 2. Because rebooting the transponder does not clear non-volatile regional channel registers, the Coast Guard was forced to broadcast wide-area corrective Message 22 transmissions across multiple maritime districts to restore normal operations.

### 36.6.3 Silent mode and transmit inhibit oversights

Most marine transponders incorporate a hardware switch or software setting for "silent mode" (receive-only operation). While SOLAS permits shutting down AIS only when safety or security is compromised (IMO Res. A.1106(29) §22), crew members on fishing vessels or tugs occasionally engage silent mode to hide locations. Forgetting to disengage silent mode leaves the ship dark on the VDL while watchstanders assume they are tracked, eliminating AIS collision-avoidance buffers on nearby bridges.

## 36.7 Data ingestion, processing, and network failures

Once AIS packets leave the vessel's antenna, they travel through shore collection networks, satellite constellations, and terrestrial backhauls. Ingestion pipelines introduce systemic data errors before records ever reach analytics databases ([Chapter 47](ch47-data-quality-track-reconstruction.md) and [Chapter 50](ch50-big-data-architecture.md)).

### 36.7.1 Duplicate messages and multi-path receiver skew

A single AIS transmission burst travels via line-of-sight to multiple coastal shore stations, commercial receiver hubs, and low Earth orbit (**LEO**) satellites. Each receiver logs the packet, adds an internal reception timestamp via an NMEA TAG block (`c:` parameter), and streams the sentence to central aggregation servers:
```
\s:rRad1,c:1728115200*1A\!AIVDM,1,1,,A,13aEO:0P00000000000000000000,0*12
\s:rRad2,c:1728115201*19\!AIVDM,1,1,,A,13aEO:0P00000000000000000000,0*12
```
Because transmission paths and network backhauls have varying latency (ranging from tens of milliseconds over fiber to several minutes over satellite downlinks), central processors receive identical messages out of order with conflicting receiver timestamps. If a data pipeline sorts messages solely by arrival time rather than reconciling payload internal timestamps, tracks experience severe temporal jitter.

### 36.7.2 Satellite reception latency and track aliasing

Satellite AIS receivers aboard LEO constellations orbit at altitudes between 500 km and 800 km, covering footprints exceeding 5,000 km in diameter ([Chapter 39](ch39-satellite-ais.md)). Due to onboard buffer queuing and ground-station downlink scheduling, satellite-received AIS reports may be downlinked hours after transmission. When a downstream ingestion pipeline merges real-time terrestrial feeds with delayed satellite batches without proper temporal gating, vessels appear to jump backwards in time or execute impossible kinematic maneuvers across the open ocean.

### 36.7.3 Downstream software parser crashes on malformed sentences

Legacy AIS decoding libraries (such as unpatched versions of `gpsd`, `libais`, or custom corporate parsers) frequently assume incoming payloads conform strictly to specification bit lengths. 

As demonstrated in vulnerability research by Balduzzi, Pasta, and Wilhoit (2014) and documented across numerous CVE advisories ([Chapter 60](ch60-malicious-payloads-robustness.md)), malformed payloads—such as an over-length binary application message, truncated ASCII 6-bit armor, or out-of-bounds navigational status values—can trigger buffer overflows, unhandled null-pointer dereferences, or infinite loops in ingestion software, crashing upstream collection servers and halting data ingestion across entire geographic sectors.

## 36.8 Regulatory annual testing: SOLAS V/18.9 and MSC.1/Circ.1252

To identify and correct the hardware, sensor, and configuration defects cataloged in this chapter, the International Maritime Organization established a mandatory annual inspection regime. Under SOLAS Regulation V/18.9 (adopted via IMO Resolution MSC.308(88)), all shipborne AIS installations on SOLAS-compliant vessels must undergo annual testing by an approved radio inspector.

The technical inspection procedure is defined in IMO circular MSC.1/Circ.1252 (*Guidelines on Annual Testing of the Automatic Identification System*). The annual test encompasses a comprehensive, seven-stage audit:
1. **Installation and antenna inspection:** Verifying physical antenna placement, masthead clearance, connector waterproofing, coaxial feeder condition, power supply redundancy, and pilot plug wiring/power availability.
2. **Static vessel information verification:** Cross-referencing programmed MMSI, IMO ship identification number, call sign, vessel name, and $A, B, C, D$ dimensional offsets against official registration certificates.
3. **Dynamic sensor interfaces:** Auditing primary and secondary GNSS inputs, checking gyrocompass `HDT` heading tracking, verifying rate-of-turn sensor scaling, and confirming failover behaviors when primary sensors are disconnected.
4. **Voyage data entry:** Assessing crew competence in updating navigational status flags, draught, hazardous cargo indicators, ETA, and destination.
5. **RF performance measurements:** Connecting a calibrated RF power meter and frequency counter directly to the transponder's antenna port to measure conducted RF power ($12.5\text{ W} \pm 1.5\text{ dB}$), frequency tolerance ($\le \pm 500\text{ Hz}$ on 161.975 MHz and 162.025 MHz), and transmission VSWR.
6. **On-air operational test:** Performing an over-the-air communication exchange with a local VTS shore station or an approved dedicated AIS test set (e.g., Aeroflex/Cobham or Futronic radio test boxes) to confirm two-way polling (Message 10 / Message 11 exchange).
7. **Issuance of test report:** Compiling a standardized AIS Annual Test Report conforming to the MSC.1/Circ.1252 model form, a copy of which must be retained permanently on the ship's bridge for Port State Control inspection.

While MSC.1/Circ.1252 serves as an essential compliance baseline, it represents a static, point-in-time assessment. The annual test cannot verify whether LED floodlights will desensitize the receiver when navigating coastal channels at night, whether the crew will faithfully update navigational status flags after dropping anchor, or whether internal GPS firmware will survive an upcoming leap second or week-number rollover. Consequently, comprehensive maritime safety demands continuous, automated data verification.

## Then & now

How the hardware, software, and operational failure modes of AIS evolved from early prototype deployments to modern global networks:

- ⟨H⟩ **1998–2002:** Universal AIS prototypes focused on proving TDMA slot synchronization and physical GMSK modulation. Transponders were bulky chassis requiring external GPS timing antennas and discrete gyro interface converters. Bridge crews received minimal training, leading to unprogrammed MMSIs and missing static parameters across first-generation installations.
- ⟨+⟩ **2005 (Saab leap-second anomaly):** Advance broadcast of the upcoming 31 December 2005 leap second caused Saab R3 and R4 Class A transponders to apply the timing adjustment six months early. Bursts were displaced by 37.5 slots, causing mid-slot transmissions and packet collisions (Saab Announcement PT-05-0078; Norwegian Maritime Directorate SM 10/2005).
- ⟨+⟩ **2007 (Harati-Mokhtari baseline study):** The first comprehensive academic survey of AIS data reliability evaluated 400,059 messages collected off the UK coast, revealing that approximately $8\%$ of all transmissions contained significant errors across MMSI, dimensions, navigational status, or draught (Harati-Mokhtari et al. 2007).
- ⟨+⟩ **2007–2012 (Adoption of mandatory annual testing):** IMO MSC.1/Circ.1252 established voluntary guidelines for annual AIS testing in October 2007, which became mandatory under SOLAS Regulation V/18.9 on 1 July 2012 following the adoption of Resolution MSC.308(88).
- ⟨+⟩ **2008 (GPS PRN-32 constellation expansion):** Activation of satellite PRN-32 on 27 February 2008 caused non-compliant internal GNSS receiver engines to crash, halting valid position broadcasts across thousands of vessels until firmware updates were applied (USCG NAVCEN FAQ).
- ⟨+⟩ **2010 (Mid-Atlantic Message 22 channel command error):** Erroneous channel management broadcasts across Maryland, Delaware, Pennsylvania, New Jersey, and New York commanded transponders onto non-standard channels, prompting USCG Safety Alert 07-10 and corrective broadcasts.
- ⟨+⟩ **2012 (USCG AVIS / VIVS deployment):** The US Coast Guard launched the Authoritative Vessel Identification Service (**AVIS**) and Vessel Information Verification Service (**VIVS**), cross-referencing live nationwide AIS broadcasts against federal registration databases to automatically flag misconfigured static data.
- ⟨+⟩ **2014 (Security and parser robustness revelations):** Academic and industry security evaluations demonstrated that malformed AIS sentences could trigger crashes, buffer overflows, and denials of service in commercial ECDIS and open-source ingestion engines (Balduzzi, Pasta & Wilhoit 2014).
- ⟨+⟩ **2018 (LED lighting interference):** Rising adoption of commercial LED fixtures led to widespread VHF and AIS receiver desensitization, prompting the US Coast Guard to publish Marine Safety Alert 13-18.
- ⟨+⟩ **2019–2025 (GPS week number rollover cycle):** Following the global GPS WNRO on 6 April 2019, vendor-specific 10-bit firmware rollover dates triggered clock regressions across Furuno (2020, 2022) and JRC (2025) transponders, corrupting date logs while leaving physical positioning unaffected.

## Validation, uncertainty & data quality

To prevent corrupted AIS data from contaminating navigational displays and analytical pipelines, data consumers must implement rigorous validation procedures. This section details automated filtering rules, quantifiable failure metrics, and a reproducible worked example.

### Verification procedures and quantitative bounds

An automated data-cleaning pipeline should execute multi-stage validation:
1. **Format and range gating:** Every incoming message must satisfy structural constraints:
   - Valid MMSI: $200000000 \le \text{MMSI} \le 775999999$ for standard ship stations (excluding valid coastal base stations, SAR aircraft, AtoNs, and craft associated with a parent vessel).
   - Valid Coordinates: $-90.0^\circ \le \text{Lat} \le +90.0^\circ$ and $-180.0^\circ \le \text{Lon} \le +180.0^\circ$. Discard explicit sentinel coordinates ($\text{Lat} = 91^\circ$, $\text{Lon} = 181^\circ$).
   - Valid SOG: $0.0 \le \text{SOG} \le 102.2\text{ kn}$. Flag $\text{SOG} = 102.3\text{ kn}$ (not available).
   - Valid COG: $0.0^\circ \le \text{COG} \le 359.9^\circ$. Flag $\text{COG} = 360.0^\circ$ (not available).
   - Heading Integrity: Flag $\text{Heading} = 511$ if $\text{SOG} \ge 3.0\text{ kn}$.
2. **Kinematic speed-between-fixes gating:** For consecutive position reports $(t_1, \phi_1, \lambda_1)$ and $(t_2, \phi_2, \lambda_2)$ from the same MMSI:
   $$\Delta d = 2 R \arcsin \sqrt{\sin^2\left(\frac{\Delta \phi}{2}\right) + \cos \phi_1 \cos \phi_2 \sin^2\left(\frac{\Delta \lambda}{2}\right)}$$
   $$\bar{v}_{\text{implied}} = \frac{\Delta d}{t_2 - t_1}$$
   If $\Delta t = t_2 - t_1 < 60\text{ s}$ and $\Delta d > 1.0\text{ nmi}$, or if $\bar{v}_{\text{implied}} > 60\text{ kn}$ for conventional commercial vessels, flag the report as a kinematic violation or duplicate MMSI teleportation.
3. **Static dimension plausibility:** In Message 5 and Message 24 Part B:
   - Total length $L = A + B$, total beam $W = C + D$.
   - Flag if $L = 0$ or $W = 0$, if $L > 450\text{ m}$, or if $W > 70\text{ m}$.
   - Flag if the length-to-beam ratio $L/W < 1.5$ or $L/W > 15.0$ for conventional commercial hulls.

> **Try it.** You can execute automated failure-mode triage on raw NMEA logs using `pyais` and Python. The following script parses an AIS data stream, extracts physical and operational failure signatures, and tallies sentinel counts:
>
> ```python
> from collections import Counter
> from pyais.stream import FileReaderStream
>
> mmsi_counts = Counter()
> sentinels = Counter()
> invalid_mmsis = set()
>
> for msg in FileReaderStream("data/samples/synthetic_harbor.nmea"):
>     d = msg.decode()
>     mmsi = d.mmsi
>     mmsi_counts[mmsi] += 1
>
>     # Check for invalid or default MMSI
>     if mmsi in (0, 1193046, 123456789) or not (200000000 <= mmsi <= 775999999):
>         invalid_mmsis.add(mmsi)
>
>     # Check for absent heading sensor (sentinel 511)
>     if getattr(d, "heading", None) == 511:
>         sentinels[(mmsi, "heading_511")] += 1
>
>     # Check for absent Rate of Turn sensor (sentinel -128)
>     if getattr(d, "rot", None) == -128:
>         sentinels[(mmsi, "rot_not_available")] += 1
>
>     # Check for GNSS inoperative or manual time stamp (sentinels 61-63)
>     if getattr(d, "second", None) in (61, 62, 63):
>         sentinels[(mmsi, f"second_{d.second}")] += 1
>
> print(f"Analyzed {len(mmsi_counts)} distinct MMSIs.")
> print(f"Flagged Invalid MMSIs: {sorted(invalid_mmsis)}")
> print(f"Sentinel Counts (Top 5): {sentinels.most_common(5)}")
> ```
>
> Expected output on `data/samples/synthetic_harbor.nmea`:
> ```
> Analyzed 11 distinct MMSIs.
> Flagged Invalid MMSIs: [0, 1193046, 993672001, 993672002]
> Sentinel Counts (Top 5): [((338123456, 'heading_511'), 121), ((1193046, 'heading_511'), 120), ((338654321, 'heading_511'), 120), ((0, 'rot_not_available'), 28), ((1193046, 'rot_not_available'), 120)]
> ```

> **Worked example.** Consider an AIS position tracking log where an uninitialized Nauticast transponder transmits using default MMSI `1193046`. Two distinct vessels in different ports share this identifier: Vessel 1 is maneuvering in Boston Harbor ($42.36^\circ\text{ N}, 070.95^\circ\text{ W}$), and Vessel 2 is departing New York Harbor ($40.68^\circ\text{ N}, 074.04^\circ\text{ W}$).
>
> At $t_1 = 12\text{:}00\text{:}00\text{ UTC}$, Vessel 1 reports $\phi_1 = 42.3600^\circ\text{ N},\ \lambda_1 = -70.9500^\circ\text{ W}$.
> At $t_2 = 12\text{:}00\text{:}10\text{ UTC}$ ($\Delta t = 10\text{ s}$), Vessel 2 reports $\phi_2 = 40.6800^\circ\text{ N},\ \lambda_2 = -74.0400^\circ\text{ W}$.
>
> Calculating great-circle distance $\Delta d$:
> $$\Delta \phi = 40.6800^\circ - 42.3600^\circ = -1.6800^\circ = -0.02932\text{ rad}$$
> $$\Delta \lambda = -74.0400^\circ - (-70.9500^\circ) = -3.0900^\circ = -0.05393\text{ rad}$$
> Using mean latitude $\bar{\phi} = 41.5200^\circ$ ($0.72466\text{ rad}$, $\cos\bar{\phi} \approx 0.74872$):
> $$\Delta d \approx 6371.0 \times \sqrt{(-0.02932)^2 + (0.74872 \times -0.05393)^2} \approx 317.9\text{ km} \approx 171.6\text{ nmi}$$
>
> The implied speed between reports is:
> $$\bar{v}_{\text{implied}} = \frac{171.6\text{ nmi}}{10\text{ s}} \times \frac{3600\text{ s}}{1\text{ h}} = 61,776\text{ kn}$$
>
> Because $\bar{v}_{\text{implied}} \gg 60\text{ kn}$, the ingestion filter instantly flags a teleportation anomaly. Rather than corrupting the database with an impossible trajectory, a Kalman tracking filter splits MMSI `1193046` into two distinct spatial cluster tracks (`1193046_A` and `1193046_B`), preserving track integrity while logging an identity violation.

## Software

**Open source:**
- **pyais** (Python; MIT license; Cirrom / Peter W. / Habimm): Decoding library supporting NMEA 0183 AIVDM/AIVDO message suites, bit parsing, and stream filtering. *Caveat:* Python overhead limits multi-gigabit raw satellite throughput.
- **libais** (C++ with Python bindings; Apache-2.0; Kurt Schwehr): Compact decoding engine optimized for speed and fuzz-tested against malformed payloads. *Caveat:* Strict specification enforcement discards non-standard vendor extensions.
- **AIS-catcher** (C++; GPL-3.0; Jasper van de Gronde): High-performance SDR receiver and decoding engine featuring multi-antenna reception and RF diagnostics. *Caveat:* Designed for real-time reception rather than offline trajectory analytics.

**Free but closed:**
- **USCG Vessel Information Verification Service (VIVS)**: Federal service cross-referencing live NAIS broadcasts against official vessel documentation and FCC licenses. *Caveat:* Coverage restricted to US waters.

**Commercial:**
- **Aeroflex / Cobham / Viavi IFR 4000 / 6000 Series**: Benchtop RF test sets for executing IMO MSC.1/Circ.1252 annual radio surveys. *Caveat:* High capital equipment cost.
- **GateHouse Maritime AIS Hub**: Enterprise VTS platform providing real-time data cleansing, sensor anomaly detection, and track reconstruction. *Caveat:* Proprietary closed-source licensing.

## Standards & guides

- **IMO Resolution MSC.74(69), Annex 3 (1998)**: *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS).* London: IMO. Establishes functional carriage requirements and architecture.
- **IMO Resolution A.1106(29) (2015)**: *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS).* London: IMO. Governs operational usage, watchstander duties, and manual voyage data entry.
- **IMO MSC.1/Circ.1252 (2007)**: *Guidelines on Annual Testing of the Automatic Identification System (AIS).* London: IMO. Defines test procedures, RF measurements, and reporting forms for mandatory annual surveys.
- **IMO Resolution MSC.308(88) (2010)**: *Adoption of Amendments to the International Convention for the Safety of Life at Sea, 1974, as Amended.* London: IMO. Enacts mandatory annual AIS testing under SOLAS V/18.9.
- **ITU-R Recommendation M.1371-6 (2026)**: *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band.* Geneva: ITU. Normative standard for TDMA timing, slot allocation, and message layouts.
- **IEC 61993-2:2018 (Edition 3.0)**: *Class A Shipborne Equipment of the Automatic Identification System (AIS) — Operational and Performance Requirements, Methods of Test and Required Test Results.* Geneva: IEC. Governs type approval and BIIT monitoring.
- **IEC 62287-1:2017 (Edition 3.0)**: *Class B Shipborne Equipment of the Automatic Identification System (AIS) — Part 1: Carrier-Sense Time Division Multiple Access (CSTDMA) Techniques.* Geneva: IEC. Governs Class B CS carrier-sensing timing windows.
- **USCG Marine Safety Alert 13-18 (2018)**: *Potential Interference of VHF-FM Radio and AIS Reception from LED Lighting.* Washington, DC: USCG. Details EMI risks from LED fixtures and defines the VHF squelch test.
- **USCG Safety Alert 07-10 (2010)**: *Caution to AIS Users: Inadvertent Channel Management Commands.* Alexandria, VA: USCG NAVCEN. Documents regional frequency switching failures caused by erroneous Message 22 broadcasts.
- **UK MCA Marine Guidance Note MGN 324 (M+F)**: *Radio: Operational Guidance on the Use of VHF Radiotelephone and Automatic Identification Systems (AIS) at Sea.* Southampton: MCA. Covers operational limitations and Class B slot starvation.

## Pitfalls

1. **Assuming built-in integrity testing (BIIT) validates data correctness.** A green "OK" indicator on the transponder's MKD confirms only that internal power rails, synthesizers, and microprocessors are operational. BIIT does not validate whether the connected gyrocompass is sending a frozen heading, whether the GPS antenna reference offsets are inverted, or whether the vessel is broadcasting a factory default MMSI.
2. **Treating Class B CS report gaps as hardware or antenna failures.** When a Class B CS transponder's reporting rate degrades from 30 seconds to several minutes in high-density waterways, technicians frequently replace antennas or cables unnecessarily. In congested waters, Class A SOTDMA traffic starves CSTDMA stations of quiet carrier-sense windows; the unit is functioning exactly as designed under IEC 62287-1.
3. **Overlooking LED deck floodlights during RF range troubleshooting.** Investigating complaints of poor AIS reception during daylight hours will fail to reproduce the fault if the vessel's unshielded LED navigation or deck lights are switched off. Always test VHF and AIS receiver sensitivity with all shipboard lighting and DC-DC converters fully energized.
4. **Ignoring Course Over Ground (COG) vs. True Heading disparities.** Confounding COG with heading in navigation displays. When a vessel is subjected to strong cross-currents, leeway, or towing forces, the vessel aspect can diverge from its vector of motion by tens of degrees. If heading is reported as sentinel 511, displaying the vessel hull aligned with COG creates severe collision hazards.
5. **Neglecting non-volatile memory in regional channel management.** Assuming that cycling transponder power will reset operating frequencies back to standard international channels (AIS 1 and AIS 2). Under ITU-R M.1371, regional channel settings programmed via Message 22 persist across power cycles until explicitly overridden by a new Message 22 or cleared manually in protected engineering menus.
6. **Failing to detect multi-station MMSI collisions in tracking databases.** Ingesting AIS data without automated speed-between-fixes validation. When multiple unprogrammed vessels transmit default MMSI `1193046`, a naive tracker connects the fixes into a single supersonic trajectory, polluting global shipping statistics and triggering false VTS alarms.
7. **Using unamplified passive RF splitters for AIS and VHF voice radios.** Installing cheap passive coax tees or non-isolated splitters drops signal strength by over 3 dB and risks catastrophic front-end damage to the AIS receiver when the 25 W VHF voice radiotelephone is keyed. Always install certified active splitters with fail-safe isolation relays.
8. **Treating GPS Week Number Rollover as an RF hardware failure.** Replacing transponders when internal system logs show dates shifted back 19.6 years. WNRO is an internal firmware calendar calculation error; physical satellite tracking, trilateration, and 1PPS TDMA slot synchronization remain fully functional.
9. **Discarding raw NMEA sentences and TAG blocks during data ingestion.** Stripping original `!AIVDM` sentences or dropping NMEA 4.10 TAG blocks (`\c:timestamp,s:station\*hh\`) in ingestion pipelines destroys essential forensic metadata, making it impossible to resolve duplicate messages, measure backhaul latency, or detect multi-receiver spoofing.
10. **Inverting GNSS antenna reference offsets A and B.** Entering the total vessel length into parameter $A$ (distance from bow to antenna) and zero into parameter $B$ on large commercial vessels. In docking and lock operations, this shifts the rendered vessel contour hundreds of meters forward of its actual hull location, rendering ECDIS positioning displays dangerously misleading.

## Key takeaways

- **AIS integrity testing is purely structural, not semantic.** Built-in transponder diagnostics monitor internal hardware health but cannot detect erroneous sensor inputs, inverted dimensions, or stale voyage data.
- **Physical RF degradation presents as range asymmetry.** High VSWR, corroded coaxial feeders, or crushed cables degrade transmission range down to 2–4 nmi while leaving receiver sensitivity comparatively unaffected.
- **LED lighting EMI is a pervasive silent hazard.** Unfiltered switch-mode power supplies in marine LED fixtures emit wideband RF noise at 162 MHz, collapsing receiver sensitivity by 10 dB to 25 dB whenever lights are energized.
- **Class B CS slot starvation is deliberate protocol behavior.** Under high TDMA channel loads, Class B CSTDMA units defer transmissions to prioritize commercial Class A traffic, degrading reporting intervals without hardware malfunction.
- **GNSS loss triggers standardized sentinel broadcasts.** Fix loss causes transponders to broadcast latitude $91^\circ$, longitude $181^\circ$, and time stamp sentinel `63`, while fallback synchronization transitions to indirect or base-station timing.
- **Firmware date anomalies spare physical positioning.** GPS Week Number Rollovers and leap-second bugs can distort calendar years in Messages 4 and 11, but physical satellite tracking, pseudorange positioning, and 1PPS slot timing remain operational.
- **Human configuration errors dominate global data quality issues.** Default MMSIs (`1193046`), missing heading sensors (`511`), and stale navigational status flags account for the vast majority of corrupt records in maritime repositories.
- **SOLAS annual testing provides a baseline, not a guarantee.** MSC.1/Circ.1252 annual surveys audit point-in-time compliance but fail to catch dynamic underway failures such as nighttime LED interference or post-survey configuration neglect.

## References

- Balduzzi, M., Pasta, A. & Wilhoit, K. (2014). A security evaluation of AIS automated identification system. In *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC '14)*, pp. 436–445. doi:10.1145/2664243.2664257
- Banyś, P., Noack, B. & Gewies, S. (2012). Assessment of AIS position-report reliability. *Annual of Navigation*, 19:5–16. doi:10.2478/v10367-012-0001-0
- Bošnjak, M., Šimunović, P. & Kavran, Z. (2012). AIS error analysis in maritime traffic. *Transactions on Maritime Science*, 1(2):77–84. doi:10.7225/toms.v01.n02.002
- Emmens, G., Amrit, C., Abdi, R. & Ghosh, B. (2021). The promises and perils of AIS data: A review of data-quality issues. *Expert Systems with Applications*, 178:114975. doi:10.1016/j.eswa.2021.114975
- Harati-Mokhtari, A., Wall, A., Brooks, P. & Wang, J. (2007). Automatic Identification System (AIS): Data reliability and human error implications. *The Journal of Navigation*, 60(3):373–389. doi:10.1017/S0373463307004298
- IEC (2017). *Maritime navigation and radiocommunication equipment and systems — Class B shipborne equipment of the automatic identification system (AIS) — Part 1: Carrier-sense time division multiple access (CSTDMA) techniques* (IEC Standard No. 62287-1:2017, Edition 3.0). Geneva: International Electrotechnical Commission.
- IEC (2018). *Maritime navigation and radiocommunication equipment and systems — Automatic identification systems (AIS) — Part 2: Class A shipborne equipment of the automatic identification system (AIS) — Operational and performance requirements, methods of test and required test results* (IEC Standard No. 61993-2:2018, Edition 3.0). Geneva: International Electrotechnical Commission.
- IMO (2007). *Guidelines on Annual Testing of the Automatic Identification System (AIS)* (Circular MSC.1/Circ.1252). London: International Maritime Organization.
- IMO (2010). *Adoption of Amendments to the International Convention for the Safety of Life at Sea, 1974, as Amended* (Resolution MSC.308(88)). London: International Maritime Organization.
- IMO (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). London: International Maritime Organization.
- Iphar, C., Ray, C. & Napoli, A. (2020). On the evaluation of data integrity: Application to AIS data. *Expert Systems with Applications*, 147:113219. doi:10.1016/j.eswa.2020.113219
- ITU-R (2026). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band* (Recommendation ITU-R M.1371-6). Geneva: International Telecommunication Union.
- Japan Radio Co., Ltd. (2023). *Notice: GPS Week Number Rollover for JHS-182 and JHS-183 AIS*. Tokyo: JRC. URL: https://www.jrc.co.jp/en/news/2023/0915-1/
- Kessler, G. C., Craiger, J. P. & Haass, S. C. (2018). A taxonomy of AIS vulnerabilities and attack scenarios. *TransNav: International Journal on Marine Navigation and Safety of Sea Transportation*, 12(3):429–437. doi:10.12716/1001.12.03.01
- Last, P., Bahlke, L., Hering-Bertram, C. & Linsen, C. (2014). Comprehensive analysis of AIS data quality for movement prediction. *The Journal of Navigation*, 67(5):791–809. doi:10.1017/S0373463314000253
- Last, P., Hering-Bertram, C. & Linsen, C. (2015). How AIS antenna setup affects AIS signal quality. *Ocean Engineering*, 100:83–89. doi:10.1016/j.oceaneng.2015.03.017
- Maritime and Coastguard Agency (2018). *Radio: Operational Guidance on the Use of VHF Radiotelephone and Automatic Identification Systems (AIS) at Sea* (Marine Guidance Note MGN 324 (M+F)). Southampton: MCA.
- Mazzarella, F., Vespe, M., Alessandrini, D., Tarchi, D., Aulicino, G. & Vollero, A. (2017). A novel anomaly detection approach to identify intentional AIS on/off switching. *Expert Systems with Applications*, 78:110–123. doi:10.1016/j.eswa.2017.02.011
- United States Coast Guard (2010). *Caution to AIS Users: Inadvertent Channel Management Commands* (Safety Alert 07-10). Alexandria, VA: USCG Navigation Center.
- United States Coast Guard (2018). *Potential Interference of VHF-FM Radio and AIS Reception from LED Lighting* (Marine Safety Alert 13-18). Washington, DC: USCG Office of Investigations and Casualty Analysis.
- United States Coast Guard Navigation Center (2026). *AIS Frequently Asked Questions*. Alexandria, VA: USCG NAVCEN. URL: https://www.navcen.uscg.gov/ais-frequently-asked-questions
