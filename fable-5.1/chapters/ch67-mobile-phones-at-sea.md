# Chapter 67 — Mobile phones at sea

> **Part X — Adjacent and complementary systems; the future.** Mobile phones, cellular networks, and satellite broadband form a ubiquitous communication layer that interacts with, complements, and frequently conflicts with the maritime VHF Data Link.

**In this chapter.** You will explore how mobile phones, cellular networks, and satellite broadband intersect with the maritime Automatic Identification System (**AIS**). We examine how smartphones have become bridge navigation tools through mobile charting applications, crowdsourced tracking platforms, and pseudo-AIS mobile broadcasts, analyzing the latency, network limits, and severe safety hazards of substituting consumer cellular feeds for line-of-sight VHF transponders. You will learn the physical architectures of cellular reception at sea, from high-site coastal base stations to shipboard picocells and cellular repeaters. We analyze network-side cellular location tracking, showing how mobile devices broadcast location telemetry across global cellular core networks via Signaling System No. 7 (**SS7**) and Diameter routing protocols, Home Location Register (**HLR**) and Home Subscriber Server (**HSS**) lookups, and offshore International Mobile Subscriber Identity (**IMSI**) catchers. Finally, you will evaluate satellite-direct smartphone connectivity, satellite broadband like Starlink Maritime, data protection regimes under GDPR and UNCLOS, and how cellular telemetry complements or contradicts authoritative AIS data.

## 67.1 The mobile phone on the modern bridge

The modern maritime bridge hosts a dual communication ecosystem. On one side stands statutory maritime electronics: SOLAS-mandated Type-Approved radar, Electronic Chart Display and Information Systems (**ECDIS**), Global Maritime Distress and Safety System (**GMDSS**) consoles, and Class A Automatic Identification System (**AIS**) transponders ([Chapter 20](ch20-architecture-and-station-classes.md)). On the other side sits a dense cluster of consumer smartphones, tablets, and cellular routers brought aboard by shipmasters, pilots, crew, and recreational mariners.

Smartphones have transformed daily operations. Master mariners inspect high-resolution weather models before departure. Marine pilots carry Portable Pilot Units (**PPUs**) connected via Wi-Fi or Bluetooth to the bridge pilot plug ([Chapter 03](ch03-at-sea-operations.md)). Tug masters coordinate maneuvers over mobile messaging applications. Recreational skippers navigate coastal archipelagoes using mobile apps like Navionics Boating, C-MAP, Savvy Navvy, and Orca. Concurrently, crowdsourced vessel-tracking applications—including MarineTraffic, VesselFinder, and FleetMon—display live ship movements over commercial cellular data connections ([Chapter 41](ch41-networks-and-providers.md)).

This convergence breaches core structural assumptions of maritime radio:
1. **Cooperative broadcast vs. routed IP client-server:** AIS operates as an autonomous, line-of-sight VHF broadcast network where every station transmits unencrypted telemetry directly to surrounding receivers ([Chapter 01](ch01-what-ais-is.md)). Cellular smartphones operate as closed, point-to-point, centrally routed clients dependent on carrier cores, base stations, and cloud servers.
2. **Deterministic TDMA vs. best-effort packet delivery:** The AIS VHF Data Link (**VDL**) uses Time Division Multiple Access (**TDMA**) synchronized to Universal Coordinated Time (**UTC**) via GNSS, allocating 2,250 fixed 26.67-millisecond time slots per minute per channel ([Chapter 21](ch21-link-layer-tdma.md)). Cellular IP networks operate on shared scheduling with variable packet latency, backhaul buffering, and non-deterministic drop rates.
3. **Intentional publicity vs. covert leakage:** AIS was engineered to broadcast public vessel identity, kinematics, and voyage parameters to enhance navigation safety ([Chapter 19](ch19-privacy-and-ethics.md)). Conversely, mobile phones are consumer devices whose users expect location privacy, yet cellular core signaling protocols and base station associations leak precise geographical telemetry to network operators, intelligence services, and commercial data brokers.

## 67.2 Navigation apps, crowdsourced feeds, and "pseudo-AIS"

Mobile devices interface with maritime tracking through two distinct mechanisms: receiving terrestrial or satellite AIS feeds relayed over the internet, and transmitting position fixes from the phone's internal GNSS receiver to commercial tracking databases.

```
       CELLULAR INTERNET RELAY VS. AUTONOMOUS VHF DATA LINK (VDL)

  [Target Vessel]                                       [Observing Vessel]
  Class A/B Transponder                                 Bridge / Cockpit
       |                                                       ^
       |--- Line-of-Sight VHF Broadcast (161.975 / 162.025 MHz) |  (Latency: < 2 s)
       |    Direct Ship-to-Ship VDL (Deterministic SOTDMA)     |
       |                                                       |
       v                                                       |
  [Shore AIS Base Station]                                     |
       | Internet Backhaul (UDP / TLS)                         |
       v                                                       |
  [Commercial Aggregator Cloud]                                |
       | Cellular IP Data Stream (4G/5G / Wi-Fi)               |
       v                                                       |
  [Cellular Base Station / Picocell]                           |
       | RF Downlink                                           |
       +-------------------------------------------------------+
            Mobile App (MarineTraffic, Boat Beacon, Navionics)
            (Latency: 30 s to 15+ minutes; UNRELIABLE FOR CPA)
```

### 67.2.1 Crowdsourced AIS display on mobile devices

Mobile charting applications frequently ingest AIS data from global crowdsourced aggregators. When a coastal pleasure craft navigates using a mobile phone, the device connects via Long Term Evolution (**LTE**) or 5G to commercial servers, downloading target vectors for display on a chart.

While visually similar to an ECDIS display, internet-relayed AIS data suffers from systemic latency and filtering:
- **Terrestrial aggregation delays:** A coastal base station receives an AIS position report (Message 1, 2, or 3) and forwards the raw NMEA encapsulation (`!AIVDM`) over a socket ([Chapter 26](ch26-interfaces-and-logging.md)). The aggregator ingests, deduplicates, parses, and redistributes the message, adding 1 to 5 seconds under optimal conditions.
- **Satellite revisit latency:** In offshore waters outside terrestrial VHF receiver coverage, aggregators rely on Low Earth Orbit (**LEO**) satellite constellations ([Chapter 39](ch39-satellite-ais.md)). Due to orbital geometry, message deconfliction, and ground station downlinks, satellite AIS latency ranges from 5 minutes to over an hour.
- **Client polling and push throttling:** To conserve cellular data and battery, mobile applications poll REST APIs or receive WebSockets updates throttled to intervals between 30 and 300 seconds.
- **Commercial filtering:** Aggregators apply heuristics that suppress perceived duplicate reports, filter stationary craft, or downsample high-speed Class A reporting intervals into 60-second updates.

Under COLREG Rule 7, "Every vessel shall use all available means appropriate to the prevailing circumstances and conditions to determine if risk of collision exists" (IMO COLREG 1972). Relying on a mobile tracking app with multi-minute latency to determine Closest Point of Approach (**CPA**) and Time to Closest Point of Approach (**TCPA**) violates prudent seamanship. A ship steaming at $24	ext{ kn}$ ($12.35	ext{ m/s}$) covers nearly $1.5	ext{ km}$ ($0.8	ext{ nmi}$) during a 2-minute latency window; a target showing $1	ext{ nmi}$ distant on a smartphone may already be within the vessel's turning circle.

### 67.2.2 Pseudo-AIS and app-to-app position sharing

A more acute safety hazard arises from mobile applications marketing "pseudo-AIS" or internet-based position reporting (such as Boat Beacon, OnCourse by MarineTraffic, and proprietary app-to-app sharing functions).

In this paradigm, a vessel lacking a physical VHF transponder runs an application on a smartphone. The phone queries its internal GNSS receiver and uploads its latitude, longitude, Speed Over Ground (**SOG**), Course Over Ground (**COG**), and vessel particulars to the vendor's backend server over cellular data. The server injects this track into its database and displays the vessel as a target icon on other smartphones running the application.

> **Definitions that bite.**
> **AIS vs. "Pseudo-AIS" (Internet Position Reporting).**
> - **Autonomous AIS:** Position, identity, and kinematics transmitted directly over international maritime VHF frequencies (161.975 MHz and 162.025 MHz) using standardized ITU-R M.1371 TDMA protocols. Requires no internet connection, no cellular infrastructure, and no commercial subscription. Observable by all surrounding vessels and shore stations equipped with certified maritime VHF receivers.
> - **Pseudo-AIS (Internet Tracking):** Position telemetry transmitted over cellular IP networks to a commercial server. Visible *only* to users running compatible applications connected to the internet. **Completely invisible** to SOLAS Class A ECDIS displays, Class B transponders, shipborne marine radars, coastal VTS radars, and harbor traffic controllers lacking internet data injection.

Marketing cellular position apps as "AIS" creates a perilous illusion of electronic visibility. Small craft skippers operating in fog or congested channels frequently believe that because their boat appears on their smartphone screen, commercial cargo ships and ferry captains can see them. In reality, a merchant watchstander scanning an ARPA radar and type-approved ECDIS sees nothing: no VHF carrier burst exists on Channel 87B or 88B, no NMEA sentence enters the bridge multiplexer, and the small boat remains an unannounced radar target hidden within sea clutter.

> **Case file.**
> **The Phantom Visibility Hazard in Coastal Waters.**
> Marine casualty investigators (including the UK MAIB and US NTSB) have repeatedly documented recreational skippers in restricted visibility who neglected radar and visual lookouts under COLREG Rule 5, relying instead on mobile tracking apps. In several near-miss events, skippers without transponders assumed active subscriptions made them electronically visible to commercial traffic. Investigation reports reaffirmed that merchant ships navigate strictly by primary radar, visual lookouts, and certified VHF AIS transponders conforming to IMO Performance Standards (IMO Res. A.1106(29)). Internet-based mobile tracking apps provide zero collision-avoidance protection against commercial traffic.

## 67.3 Physical-layer cellular reception over sea water

The propagation of cellular radio frequencies over the ocean differs sharply from terrestrial propagation in urban topographies. Sea water acts as an electrically conductive ground plane, creating multipath reflections, extended line-of-sight propagation, and atmospheric ducting phenomena.

### 67.3.1 Line of sight, antenna elevation, and radio horizons

Cellular communications in coastal waters operate primarily in sub-1 GHz bands (e.g., 700 MHz Band 28/Band 13, 800 MHz Band 20, 900 MHz Band 8) and mid-bands (1.8 GHz Band 3, 2.1 GHz Band 1, 2.6 GHz Band 7).

In the absence of atmospheric refraction anomalies, the geometrical line-of-sight distance $d_{\text{LOS}}$ over a spherical Earth with an effective 4/3-Earth radius approximation is governed by the elevations of the base station antenna $h_{\text{BS}}$ and the mobile terminal $h_{\text{UE}}$ ([Chapter 27](ch27-rf-basics.md)):

$$d_{\text{LOS}} \approx 4.12 \cdot \left(\sqrt{h_{\text{BS}}} + \sqrt{h_{\text{UE}}}\right) \quad [\text{km}]$$

Converting to nautical miles ($1\text{ nmi} = 1.852\text{ km}$):

$$d_{\text{LOS}} \approx 2.22 \cdot \left(\sqrt{h_{\text{BS}}} + \sqrt{h_{\text{UE}}}\right) \quad [\text{nmi}]$$

Consider two typical operational scenarios:
1. **Recreational small craft:** A handheld smartphone operated on deck ($h_{\text{UE}} = 2\text{ m}$) communicating with a coastal base station mounted on a shoreline cliff or communications tower ($h_{\text{BS}} = 100\text{ m}$):
   $$d_{\text{LOS}} \approx 4.12 \cdot (\sqrt{100} + \sqrt{2}) \approx 47.03\text{ km} \quad (25.4\text{ nmi})$$
2. **Merchant cargo vessel:** An external cellular router antenna mounted on the bridge monkey island ($h_{\text{UE}} = 25\text{ m}$) communicating with the same $100\text{ m}$ coastal station:
   $$d_{\text{LOS}} \approx 4.12 \cdot (\sqrt{100} + \sqrt{25}) = 4.12 \cdot (10 + 5) = 61.80\text{ km} \quad (33.4\text{ nmi})$$

### 67.3.2 Propagation over sea water: two-ray reflection and tropospheric ducting

Over open water, the radio path between a coastal cell tower and a ship is dominated by the **two-ray ground reflection model** ([Chapter 29](ch29-propagation-modeling.md)). The receiver captures both a direct wave and a specular reflection bouncing off the sea surface. Because sea water has high dielectric permittivity ($\epsilon_r \approx 70\text{--}80$) and conductivity ($\sigma \approx 4\text{--}5\text{ S/m}$), the reflection coefficient approaches $-1$ at low grazing angles.

When path difference equals odd half-wavelengths ($\Delta d = (2k+1)\frac{\lambda}{2}$), constructive interference occurs. When it equals integer wavelengths ($\Delta d = k\lambda$), destructive interference causes multipath nulls exceeding $20\text{--}30\text{ dB}$. Beyond breakpoint distance $d_c \approx \frac{4 h_{\text{BS}} h_{\text{UE}}}{\lambda}$, attenuation shifts from free-space ($1/d^2$) to plane-earth ground loss ($1/d^4$).

Under temperature inversions trapping cool, moist marine air beneath warm, dry air, **evaporation ducting** forms along choke points (English Channel, Baltic, Persian Gulf). These wave-guides trap RF energy (700 MHz to 2.6 GHz), propagating signals hundreds of kilometers past the horizon while injecting co-channel interference into distant networks.

### 67.3.3 Uplink asymmetry and the power bottleneck

The key constraint on offshore cellular range is **link budget asymmetry**. Coastal base stations transmit with high Equivalent Isotropically Radiated Power (**EIRP**) ($40\text{--}80\text{ W}$, $+46\text{--}+49\text{ dBm}$) via directional panels ($+15\text{--}+18\text{ dBi}$), propagating downstream signals $25\text{ nmi}$ offshore.

Conversely, standard 3GPP Class 3 smartphones transmit at only $+23\text{ dBm}$ ($200\text{ mW}$) with internal antenna gain of $-1\text{--}-3\text{ dBi}$. Even when receiving the tower broadcast, the smartphone's weak uplink cannot reach the base station, trapping the terminal in a "downlink-only" state that displays signal bars while failing radio resource connection (**RRC**) establishment. Stable offshore links require dedicated marine cellular routers with high-gain masthead antennas ($+6\text{--}+9\text{ dBi}$) and low-loss coaxial cabling.

### 67.3.4 The hard distance limit: Timing Advance

Beyond RF attenuation, cellular standards enforce strict geographical distance limits through **Timing Advance** (**TA**) mechanisms designed to synchronize uplink time slots.

```
       TIMING ADVANCE (TA) SYNCHRONIZATION OVER SEA WATER

  [Coastal Base Station]                                [Shipboard Mobile UE]
  (eNodeB / gNodeB)                                     (Smartphone at Sea)
        |                                                        |
        |--- Downlink Frame Start (t = 0) ---------------------->| (Travel time: t_prop)
        |                                                        | Received at t = t_prop
        |                                                        |
        |<-- Uplink Frame Transmission (t_advance) --------------| Must arrive at BS
        |    Advanced by 2 * t_prop to align with BS time slot   | precisely in slot
```

Because radio waves travel at the speed of light ($c \approx 299,792,458\text{ m/s}$), uplink bursts from mobile phones at varying distances would collide at the base station if transmitted simultaneously. The base station measures propagation delay and commands the terminal to advance its uplink timing:
- **GSM (2G):** In GSM (3GPP TS 45.010), the bit period is $T_{\text{bit}} = \frac{48}{13}\text{ \mu s} \approx 3.6923\text{ \mu s}$. Timing Advance is a 6-bit integer ($0 \le \text{TA} \le 63$). Each increment corresponds to a one-bit duration of round-trip time, representing a one-way distance step:
  $$\Delta d_{\text{GSM}} = \frac{c \cdot T_{\text{bit}}}{2} \approx 553.46\text{ m}$$
  The maximum allowable distance for standard GSM is:
  $$d_{\text{max, GSM}} = 63 \cdot 553.46\text{ m} \approx 34.87\text{ km} \quad (18.83\text{ nmi})$$
  Any mobile phone beyond $35\text{ km}$ cannot advance its timing sufficiently; its uplink bursts spill into adjacent time slots, causing the base station to drop the connection. Extended Range GSM overcomes this by halving active slots to allow an 8-bit TA value, extending theoretical range to $120\text{ km}$.
- **LTE (4G) and 5G NR:** In LTE (3GPP TS 36.211), the basic time unit is $T_s = \frac{1}{15,000 \cdot 2,048}\text{ s} \approx 32.552\text{ ns}$. Timing Advance is commanded via an 11-bit initial index ($0 \le T_A \le 1282$), with timing adjustments applied in units of $16 \cdot T_s \approx 0.5208\text{ \mu s}$:
  $$\Delta d_{\text{LTE}} = \frac{c \cdot (16 \cdot T_s)}{2} \approx 78.07\text{ m}$$
  The maximum theoretical range enabled by standard LTE initial timing advance is:
  $$d_{\text{max, LTE}} = 1282 \cdot 78.07\text{ m} \approx 100.09\text{ km} \quad (54.04\text{ nmi})$$
  However, standard commercial cell towers configure a smaller cell radius (typically $15\text{ km}$ to $30\text{ km}$) within their software to optimize handover and frequency reuse, rejecting preambles from offshore vessels exceeding the configured cell boundary.

## 67.4 Shipboard picocells, repeaters, and maritime mobile networks

When vessels sail beyond coastal coverage, connectivity transitions to shipboard cellular infrastructure. Cruise ships, ferries, offshore platforms, and cargo fleets deploy private shipboard cellular networks.

### 67.4.1 Maritime picocells and satellite backhaul

A shipboard maritime mobile network functions as a private cellular microcell or picocell installed throughout the vessel's superstructure. Specialized providers—such as Wireless Maritime Services (**WMS**) and Telenor Maritime—operate these networks under international roaming agreements.

The architecture comprises:
1. **Low-power Transceivers (BTS/eNodeB):** Antennas mounted in cabins and decks operating at $100\text{ mW}$ to $2\text{ W}$ to prevent coastal interference.
2. **Base Station Controller (BSC/EPC):** Local hardware managing radio resources and switching.
3. **Satellite Gateway:** Encapsulates voice, SMS, and data over satellite backhaul (geostationary C/Ku-band or LEO constellations) to terrestrial cores.
4. **Roaming Interconnect:** Authenticates mobile subscribers against home carriers via international signaling links.

### 67.4.2 Regulatory zoning and coastal geofencing

Transmitting on cellular frequencies inside a coastal state's territorial sea ($12\text{ nmi}$) violates spectrum sovereignty. Under **CEPT ECC/DEC/(08)08** and **ITU Radio Regulations Article 19**:
- **The 12-nmi shutoff:** Shipboard picocells must automatically deactivate inside the 12-nautical-mile territorial sea unless licensed by the coastal administration.
- **Power limits:** Between $12\text{ nmi}$ and $25\text{ nmi}$, picocells enforce emission caps protecting coastal networks from interference.
- **GNSS interlocks:** Picocell controllers ingest live NMEA position sentences (`$GPGGA`/`$GPRMC`), cross-referencing territorial boundaries and cutting RF transmission when entering the 12-nmi zone.

### 67.4.3 Bidirectional cellular repeaters and coastal interference

Recreational yachts, tugs, and fishing craft frequently install aftermarket cellular repeaters (bidirectional amplifiers / BDAs) to boost weak coastal signals. A high-gain donor antenna on the mast receives the coastal tower's signal, amplifies it, and re-radiates it via a service antenna in the cabin.

Improperly installed repeaters create acute interference: inadequate isolation between donor and service antennas causes self-oscillation, turning the booster into an uplink noise jammer that desensitizes coastal towers miles away. Communications regulators (e.g., US FCC under 47 CFR § 20.21) mandate automatic oscillation detection, automatic gain control (**AGC**), and carrier-specific shutdown circuits.

## 67.5 Network-side tracking: SS7, Diameter, and location queries

While mariners recognize that AIS broadcasts vessel movements to the world, carrying a mobile phone at sea turns the vessel into an involuntarily tracked target across global telecommunications networks.

Whenever a smartphone is powered on, it periodically registers with the nearest base station, transmitting its **IMSI** (**International Mobile Subscriber Identity**) and **IMEI** (**International Mobile Station Equipment Identity**). The visited cellular network records the terminal's location down to the specific Cell Global Identifier (**CGI**) and sector, storing this data in its Visitor Location Register (**VLR**) or Mobility Management Entity (**MME**).

To route calls, SMS messages, and data sessions, the visited network notifies the subscriber's home carrier, updating the **Home Location Register** (**HLR**) in 2G/3G networks or the **Home Subscriber Server** (**HSS**) in 4G/5G networks. This inter-carrier communication relies on core signaling protocols: **Signaling System No. 7** (**SS7**) and **Diameter**.

```
           GLOBAL CELLULAR CORE SIGNALING AND LOCATION LEAKAGE

  [Adversary / Intelligence Service]
  (Access to Global SS7 / Diameter Signaling Exchange)
       |
       | 1. MAP SRI / ATI (SS7) or S6a-IDR (Diameter) Query
       |    Target: Victim MSISDN (Phone Number)
       v
  [Subscriber Home Operator Core]
  (Home Location Register - HLR / Home Subscriber Server - HSS)
       |
       | 2. Query routed via international roaming interconnect
       v
  [Visited Maritime Network / Coastal Operator Core]
  (VLR / Serving MME / MSC)
       |
       | 3. Network queries serving Base Station / Picocell
       |    Captures: Cell Global Identity (CGI), Timing Advance (TA), Signal Levels
       v
  [Signaling Response: Exact Cell ID + Marine Sector]
       |
       +--> Adversary correlates Cell ID with Known Offshore Rig, Ferry, or Picocell
            Result: Pinpoint vessel tracking without radar, satellite imagery, or AIS.
```

### 67.5.1 SS7 MAP location attacks: SRI-SM and ATI

Signaling System No. 7 was designed under an implicit trust model among state-regulated national monopolies. Today, thousands of commercial aggregators, private operators, roaming brokers, and state entities possess global SS7 interconnect access (Engel 2013, 2014).

An adversary seeking to track a maritime target requires only the victim's phone number (**MSISDN**):
1. **Send Routing Information for Short Message (`SRI-SM`):** Under 3GPP TS 29.002 Mobile Application Part (**MAP**), an attacker sends an `SRI-SM` request with the victim's MSISDN. The home HLR returns the target's **IMSI** and serving Mobile Switching Center (**MSC**). If the MSC address belongs to a maritime carrier, the attacker confirms the target is at sea.
2. **Any Time Interrogation (`ATI`):** An `ATI` query asks the HLR for the subscriber's location. The HLR queries the visited network via `Provide Subscriber Info` (`PSI`), returning the **Cell Global Identifier** (**CGI**)—comprising MCC, MNC, LAC, and Cell Identity (**CI**).
3. **Offshore Cell Geolocation:** Because offshore base stations and shipboard picocells carry unique, cataloged Cell IDs assigned to specific vessels, an `ATI` response directly reveals the target's specific ship, ferry, or offshore platform. At sea, offshore base stations and maritime picocells have unique, cataloged Cell IDs assigned to specific vessels. A Cell ID query returning a maritime picocell identifies the exact IMO number and name of the cruise ship, car ferry, or offshore supply vessel upon which the target is traveling.

### 67.5.2 Diameter protocol vulnerabilities in 4G and 5G networks

Transitioning to 4G LTE and 5G Standalone networks replaced SS7 with IP-based **Diameter** (RFC 6733) and HTTP/2 interfaces (ENISA 2018, 2022). While supporting IPsec and TLS, Diameter inherited core routing vulnerabilities (Kholter & Kurbatov 2015):
- **Insert-Subscriber-Data-Request (`IDR`):** Attackers connected to international IPX roaming networks forge Diameter `IDR` messages over the **S6a** interface to query subscriber serving MMEs.
- **Location-Information-Request (`LIR`) / User-Data-Request (`UDR`):** Querying the subscriber's HSS reveals the serving tracking area identity (**TAI**) and Cell Global ID.
- **Timing Advance exploitation:** Cellular signaling attacks extract the terminal's live Timing Advance from the MME. Combining the coordinates and azimuth of a coastal cell tower with the target's TA index computes the vessel's exact range ring, geolocating a dark ship that has disabled its AIS transponder.

### 67.5.3 IMSI catchers in maritime choke points

In coastal maritime choke points, straits, and naval anchorages (such as the Bosporus, Gibraltar, Dover Strait, Singapore Strait, and the Persian Gulf), signals intelligence services deploy **IMSI catchers** (rogue base stations or "Stingrays").

An IMSI catcher broadcasts a fraudulent carrier signal with higher power and cell-selection priority than coastal towers. When vessels transit within range:
1. Mobile devices execute cell reselection toward the rogue tower.
2. The rogue station sends an `Identity Request` commanding the phone to return its unencrypted IMSI and IMEI.
3. In 2G/3G protocols, the terminal transmits its IMSI in cleartext; in 4G/5G networks, downgrade attacks force phones into legacy modes that bypass Subscription Concealed Identifiers (**SUCI**).
4. Correlating captured IMSIs with bridge AIS records links specific crew members or passengers to tracked vessels.

> **Threat model.**
> **Network-Side Mobile Phone Tracking at Sea.**
> - **Primary Assets:** Physical location privacy of shipboard personnel; operational security of naval, government, and commercial vessels; confidentiality of maritime supply chain voyages.
> - **Threat Actors:** Signals intelligence services; commercial intelligence brokers; maritime piracy syndicates; electronic warfare units.
> - **Attacker Capabilities:**
>   - *Signaling Core Intercept:* Access to global SS7/Diameter exchanges via compromised carriers, leased Global Titles, or roaming hubs.
>   - *IMSI Catchers:* Coastal or vessel-mounted SDR transceivers in maritime choke points.
>   - *Target Identification:* Possession of a victim MSISDN or passive IMSI harvesting.
> - **Impact:** Real-time tracking of vessels disabling AIS under SOLAS V/19.2.4.7 for security; deanonymization of law enforcement craft; pinpoint targeting of ships for boarding, seizure, or kinetic strike.
> - **Engineering Mitigations:**
>   - Deploying SS7/Diameter firewalls conforming to **GSMA FS.11** and **GSMA FS.19** to drop external queries (`ATI`, `SRI-SM`, `IDR`).
>   - Strict electronic emissions control (EMCON), placing crew devices in airplane mode or RF-shielded Faraday enclosures.
>   - Shipboard cellular monitoring detecting rogue base stations and anomalous timing commands.

## 67.6 Direct-to-cell satellites, Starlink Maritime, and RF signatures

The maritime mobile communications landscape is experiencing a paradigm shift driven by non-terrestrial networks (**NTN**) and commercial Low Earth Orbit satellite megaconstellations.

```
+---------------------------------------------------------------------------------------------------+
|                        MARITIME BROADBAND AND CONNECTIVITY LAYERS                                 |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  [Satellite Direct-to-Cell]               [LEO Satellite Broadband]      [Coastal 4G/5G & Picocell]|
|  - Starlink D2C, AST SpaceMobile          - Starlink Maritime, OneWeb    - High-site coastal towers|
|  - Standard unmodified 3GPP phone         - High-gain phased array dish  - Onboard GSM/LTE picocell|
|  - Frequency: Sub-2 GHz (L/S/PCS)         - Frequency: Ku/Ka-band        - Frequency: 700-2600 MHz |
|  - Throughput: 2-4 Mbit/s per beam        - Throughput: 100-300+ Mbit/s  - Throughput: 10-100 Mbit/s|
|  - Function: SMS, Voice, Emergency        - Function: Complete ship IP   - Function: Coastal mobile|
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

### 67.6.1 Direct-to-cell (NTN) satellite communications

Traditional satellite phones (such as Iridium Extreme, Inmarsat IsatPhone, and Thuraya) require proprietary transceivers, bulky helical antennas, and dedicated airtime subscriptions.

Commercial satellite operators are now deploying **Direct-to-Cell** (**D2C**) and 3GPP Release 17/18 **Non-Terrestrial Network** (**NTN**) capabilities. Systems operated by AST SpaceMobile, Lynk Global, and SpaceX (Starlink Direct to Cell) deploy spaceborne phased array antennas communicating directly with unmodified standard LTE/5G smartphones:
- **RF Architecture:** Operating in standard mobile terrestrial frequency bands (e.g., 1.9 GHz PCS, 800 MHz), satellites in LEO ($500\text{ km}$ altitude) project steerable spot beams across ocean surfaces.
- **Doppler and delay compensation:** Spacecraft traveling at orbital velocities exceeding $7.5\text{ km/s}$ introduce severe Doppler shifts ($\pm 30\text{ kHz}$ to $\pm 50\text{ kHz}$) and round-trip propagation delays of $10\text{ ms}$ to $40\text{ ms}$. Advanced base station software aboard the satellite pre-compensates for orbital Doppler shifts, presenting the satellite footprint to the smartphone as a stationary terrestrial cell tower.
- **Operational impact:** Direct-to-cell eliminates maritime communication dead zones for recreational mariners, providing global emergency messaging and location sharing without specialized EPIRBs, PLBs, or satellite transceivers. However, it extends network-side tracking across every square mile of the high seas.

### 67.6.2 Starlink Maritime and high-bandwidth shipboard networks

The rapid deployment of Starlink Maritime has altered bridge systems. Utilizing electronically steered phased array antennas in Ku-band ($10.7\text{--}12.7\text{ GHz}$ downlink, $14.0\text{--}14.5\text{ GHz}$ uplink) and Ka-band, Starlink delivers low-latency ($25\text{--}50\text{ ms}$) broadband exceeding $200\text{ Mbit/s}$ across global oceans.

Cheap broadband introduces specific operational and RF interactions with bridge electronics:
1. **Cloud-synchronized bridge navigation:** ECDIS, chart plotters, and tablets maintain continuous IP connections, downloading weather overlays, notices to mariners, and crowdsourced AIS telemetry.
2. **RF noise and receiver desensitization:** While Starlink operates at microwave frequencies far removed from VHF AIS ($162\text{ MHz}$), switch-mode power supplies and unshielded Ethernet cables emit broadband interference ([Chapter 31](ch31-noise-and-interference.md)). Routing power units adjacent to VHF coax lines increases the noise floor by $10\text{--}20\text{ dB}$, degrading AIS sensitivity.
3. **Crew Wi-Fi and network segregation:** Inadequately segregated crew networks allow malware on mobile phones to traverse bridge subnets, creating pathways for attacks against navigational data buses ([Chapter 60](ch60-malicious-payloads-robustness.md)).

## 67.7 Data protection, maritime law, and surveillance ethics

The intersection of mobile phones and vessel tracking creates legal and regulatory tensions between international maritime safety conventions, telecommunications law, and data privacy frameworks.

### 67.7.1 GDPR and personal data aboard small craft

Under Regulation (EU) 2016/679 (GDPR), Article 4(1) defines **personal data** as any information relating to an identified or identifiable natural person. In commercial shipping, a Class A transponder broadcast from a 100,000 GT tanker owned by a corporation is not personal data. However, on small recreational yachts, sports fishing craft, and artisanal fishing boats, the vessel is owned, operated, and inhabited by a natural person or family.

When a mobile app records, transmits, or republishes a small craft's track—or when network operators log cellular base station associations—that telemetry constitutes personal location data:
- **Re-identification via public registries:** Even if an app suppresses names, the track reveals home berths, anchorages, and cruising patterns. Cross-referencing an anonymous track with public maritime registries (FCC ULS, ITU MARS, national registers) definitively identifies the owner ([Chapter 13](ch13-mmsi-deep-dive.md)).
- **Commercial scraping and terms of service:** Web-based vessel aggregators harvest mobile app positions, reselling historical tracks to commercial intelligence services. Under GDPR Recital 26, processing personal location data without unambiguous consent or a verified statutory basis violates European data protection law.

> **Legal note.**
> **Mobile Phone Interception and Maritime Law at Sea.**
> - **Flag State Jurisdiction on the High Seas:** Under UNCLOS Article 92, vessels on the high seas are subject to exclusive flag-state jurisdiction. Intercepting cellular communications, deploying IMSI catchers, or spoofing base stations aboard foreign-flagged ships violates flag sovereignty and international law.
> - **Coastal State Authority in the Territorial Sea:** Under UNCLOS Article 19, innocent passage through territorial seas ($12\text{ nmi}$) is breached by "any act aimed at collecting information to the prejudice of the defence or security of the coastal State" (Art. 19(2)(c)) or "interference with any systems of communication" (Art. 19(2)(k)). Operating unauthorized repeaters or picocells exposes vessels to interdiction, fines, and port detention.
> - **Telecommunications Intercept Statutes:** In the US, unauthorized cellular interception violates 47 U.S.C. § 605 and 18 U.S.C. § 2511. In the EU, unauthorized telecom location queries violate Directive 2002/58/EC (ePrivacy Directive).

### 67.7.2 Contrasting AIS transparency with cellular secrecy

The tension between AIS and cellular tracking reflects opposing paradigms of surveillance:
- **AIS is deliberately, radically transparent:** Established by the IMO to guarantee universal, unencrypted situational awareness, AIS intentionally excludes privacy to maximize navigational safety ([Chapter 19](ch19-privacy-and-ethics.md)). Every station possesses an equal right to decode broadcasts.
- **Cellular tracking is covert, commercialized, and asymmetric:** Built on closed networks, mobile telephony fosters privacy expectations while signaling infrastructure leaks geographical telemetry to state actors, brokers, and commercial aggregators.

When mariners intentionally turn off their AIS transponder—exercising the master's statutory discretion under IMO Resolution A.1106(29) to protect the vessel against pirate attacks or hostile boarding—the presence of active, unshielded mobile phones on the bridge frequently defeats their operational security, broadcasting their location to coastal towers and intelligence satellites.

## Then & now

- ⟨H⟩ 1985 — First commercial cellular telephone systems deployed in coastal urban centers.
- ⟨+⟩ 1998 — IMO adopts Performance Standards for Shipborne Automatic Identification Systems (Resolution MSC.74(69)), establishing universal unencrypted VHF broadcast as the global standard for maritime tracking.
- ⟨+⟩ 2004 — IMO Maritime Safety Committee (MSC 79) issues formal statement condemning the publication of shipborne AIS data on the open internet, citing maritime safety and security risks; web aggregation platforms proliferate regardless.
- ⟨H⟩ 2007 — MarineTraffic founded, initiating crowdsourced global terrestrial AIS aggregation.
- ⟨+⟩ 2008 — Security researcher Tobias Engel demonstrates fundamental location tracking vulnerabilities in SS7 MAP signaling protocols at the 25th Chaos Communication Congress (25C3) (Engel 2013).
- ⟨+⟩ 2008 — CEPT adopts Decision ECC/DEC/(08)08, establishing harmonized regulatory conditions and technical power limits for the operation of Mobile Communication Services on Board Vessels (MCV) in European waters.
- ⟨H⟩ 2010 — Smart device explosion: Apple iPad released; mobile marine charting apps (Navionics, Transas iSailor) begin widespread adoption among bridge watchstanders and recreational skippers.
- ⟨+⟩ 2013 — Security evaluation of AIS by Balduzzi, Pasta, and Wilhoit demonstrates software-side injection vulnerabilities into commercial crowdsourced AIS tracking aggregators via unauthenticated web endpoints (Balduzzi, Pasta & Wilhoit 2014).
- ⟨+⟩ 2015 — Black Hat USA presentation by Kholter and Kurbatov demonstrates that 4G Diameter protocols inherit severe core signaling location tracking flaws from SS7 (Kholter & Kurbatov 2015).
- ⟨+⟩ 2018 — Regulation (EU) 2016/679 (GDPR) enters into full enforcement, triggering debates over whether vessel positions of privately owned recreational craft constitute personal data.
- ⟨+⟩ 2022 — SpaceX launches Starlink Maritime, initiating the mass adoption of high-bandwidth, low-latency LEO satellite broadband across commercial and recreational shipping.
- ⟨+⟩ 2024 — 3GPP Release 18 freezes specifications for 5G Non-Terrestrial Networks (NTN), enabling direct satellite-to-cellular smartphone voice and data connectivity over international waters.

## On the wire

Network-side cellular location tracking and shipboard mobile data injection generate distinct packet structures across telecommunications signaling interfaces.

### 67.8.1 SS7 MAP Any Time Interrogation (ATI) message

In 2G and 3G mobile networks, an external entity connected to the international signaling network queries a subscriber's location using the Mobile Application Part (**MAP**) `AnyTimeInterrogation` service primitive (3GPP TS 29.002).

Below is an annotated hexadecimal walk-through of an SS7 MAP `ATI` request packet transmitted across a Signaling Transfer Point (**STP**):

```
MAP AnyTimeInterrogation Request (Hexadecimal Walk-through):
48 2b 02 01 01 02 01 3d 30 23 80 07 91 44 77 00 00 99 f9
81 01 00 82 01 00 83 07 91 44 99 11 22 33 f4

Bit Layout Breakdown:
[48]       : TCAP Component Type (Invoke)
[2b]       : Component Length (43 bytes)
[02 01 01] : Invoke ID Tag, Length (1 byte), Value (0x01)
[02 01 3d] : Operation Code Tag, Length (1 byte), Operation: anyTimeInterrogation (0x3d = 61)
[30 23]    : Sequence Tag, Length (35 bytes)
  [80 07]  : Context Tag 0 (Target Subscriber Identity: MSISDN), Length 7 bytes
    [91]   : Nature of Address: International Number, ISDN/Telephony plan
    [44 77 00 00 99 f9] : BCD-encoded Phone Number (+44 7700 900999)
  [81 01 00] : Context Tag 1 (Requested Info: Location Information = True)
  [82 01 00] : Context Tag 2 (Requested Info: Subscriber State = False)
  [83 07]  : Context Tag 3 (GSM SCF Address), Length 7 bytes
    [91 44 99 11 22 33 f4] : Calling Entity Global Title (+44 9911223344)
```

The home HLR queries the visited network, which responds with an `AnyTimeInterrogationRes` containing the exact geographic location:

```
MAP AnyTimeInterrogation Response (Cell Global Identifier):
30 1c 80 07 91 44 77 00 00 99 f9 a1 11
  04 07 24 0f 99 01 2a 4e 20

Breakdown of Geographic Location Info:
[a1 11]    : Location Information Tag, Length 17 bytes
[04 07]    : Cell Global ID (CGI) Octet String, Length 7 bytes
  [24 0f]  : Mobile Country Code (MCC) = 240 (Sweden, MCC nibble-swapped)
  [99]     : Mobile Network Code (MNC) = 99 (Maritime Picocell Network)
  [01 2a]  : Location Area Code (LAC) = 0x012a (298)
  [4e 20]  : Cell Identity (CI)       = 0x4e20 (20000 -> "M/S Baltic Explorer" Bridge Cell)
```

By decoding the Cell Identity `0x4e20`, the querier immediately maps the target to a specific passenger ferry transiting the Baltic Sea, completely bypassing any onboard AIS transponder.

### 67.8.2 Timing Advance bounding query

The following Python snippet illustrates how an analyst or network security tool processes a base station sector and Timing Advance index to calculate the bounding geographic sector of an offshore vessel.

> **Try it.**
> Run this Python snippet to compute the physical bounding sector of a ship communicating with a coastal LTE base station.
>
> ```python
> import math
> 
> def calculate_coastal_cell_range(cell_lat, cell_lon, azimuth_deg, beamwidth_deg, ta_index):
>     """Calculate geographic bounding coordinates for an LTE Timing Advance ring."""
>     c = 299792458.0
>     # 3GPP TS 36.211: N_TA step = 16 * Ts = 16 / (15000 * 2048) seconds ≈ 0.5208 µs
>     lte_step_m = (16.0 / (15000.0 * 2048.0)) * c / 2.0  # ~78.07 meters per TA unit
>     
>     r_inner = ta_index * lte_step_m
>     r_outer = (ta_index + 1) * lte_step_m
>     r_mid = (r_inner + r_outer) / 2.0
>     
>     theta = math.radians(azimuth_deg)
>     # Flat-earth approximation for coastal displacement (valid within 50 km)
>     delta_lat = (r_mid * math.cos(theta)) / 111139.0
>     delta_lon = (r_mid * math.sin(theta)) / (111139.0 * math.cos(math.radians(cell_lat)))
>     
>     arc_length_km = (math.radians(beamwidth_deg) * r_mid) / 1000.0
>     
>     return {
>         "r_inner_m": round(r_inner, 1),
>         "r_outer_m": round(r_outer, 1),
>         "target_lat": round(cell_lat + delta_lat, 5),
>         "target_lon": round(cell_lon + delta_lon, 5),
>         "sector_span_km": round(arc_length_km, 2)
>     }
> 
> # Example: Coastal tower at South Foreland (Dover Strait), Azimuth 135°, TA Index = 120
> fix = calculate_coastal_cell_range(51.140, 1.370, azimuth_deg=135.0, beamwidth_deg=65.0, ta_index=120)
> print(fix)
> ```
>
> **Expected output:**
> ```
> {'r_inner_m': 9368.5, 'r_outer_m': 9446.6, 'target_lat': 51.08015, 'target_lon': 1.4654, 'sector_span_km': 10.67}
> ```

## Validation, uncertainty & data quality

Integrating cellular telemetry and mobile application feeds into maritime spatial systems introduces significant uncertainty regimes that must be quantified before relying on the data for analysis or navigation.

### 67.9.1 Error propagation and spatial uncertainty comparison

The spatial uncertainty of mobile phone position tracking at sea varies across four orders of magnitude depending on the tracking mechanism employed:

| Positioning Mechanism | Primary Error Sources | Typical 95% Confidence Radius ($2\sigma$) | Latency / Update Rate | Suitability for Collision Avoidance |
|---|---|---|---|---|
| **Class A VHF AIS** | GNSS antenna offset, receiver noise, VDL channel load | $5\text{--}15\text{ m}$ | $2\text{--}10\text{ s}$ (maneuvering) | Fully certified (ECDIS / ARPA) |
| **Smartphone Internal GNSS** | Cabin multipath, consumer chip dilution of precision | $10\text{--}30\text{ m}$ | $1\text{ s}$ (local screen only) | Secondary reference only |
| **Crowdsourced App Relay** | Ingestion queue, database throttling, cellular dropouts | $10\text{ m} + \Delta t \cdot v$ (motion error: $100\text{--}1500\text{ m}$) | $30\text{ s}$ to $15+\text{ min}$ | **Hazardous**; strictly prohibited |
| **LTE Timing Advance (TA)** | Multipath delay spread, ducting refraction, $78\text{ m}$ range quantization | $78\text{ m}$ radial $\times$ $10\text{ km}$ sector arc | On-demand / network query | Non-navigational surveillance |
| **Cell Global ID (CGI)** | Coastal cell geometry, atmospheric propagation reach | $5\text{--}35\text{ km}$ radius | Dynamic handover ($5\text{--}60\text{ min}$) | Coarse presence detection only |

The motion error $\epsilon_{\text{motion}}$ introduced by crowdsourced app latency $\Delta t$ for a vessel steaming at speed $v$ is modeled as:

$$\epsilon_{\text{motion}} = v \cdot \Delta t$$

For a commercial ferry steaming at $22\text{ kn}$ ($11.32\text{ m/s}$) displayed on a mobile application with an average latency of $\Delta t = 180\text{ s}$:

$$\epsilon_{\text{motion}} = 11.32\text{ m/s} \cdot 180\text{ s} \approx 2,037.6\text{ m} \quad (\approx 1.1\text{ nmi})$$

A positional uncertainty exceeding one nautical mile renders internet-relayed mobile tracking completely invalid for bridge collision-risk assessment under COLREG Rule 7.

### 67.9.2 Concrete data cleaning and validation procedures

When fusing mobile phone telemetry with AIS data archives for research, law enforcement, or post-incident reconstruction ([Chapter 47](ch47-data-quality-track-reconstruction.md)), analysts must apply rigorous validation filters:
1. **Timestamp source verification:** Mobile position logs often carry two timestamps: the GNSS fix epoch generated by the phone (`$GPRMC` timestamp) and the server ingest epoch. In cellular networks subject to intermittent dead zones, mobile apps buffer fixes locally and upload batches upon reconnecting. Failing to distinguish between fix time and server ingest time creates artificial vessel speed spikes exceeding hundreds of knots.
2. **Kinematic jump detection:** Filter incoming mobile tracks using velocity and acceleration thresholds:
   $$v_{\text{calc}} = \frac{\text{haversine}(P_{i-1}, P_i)}{t_i - t_{i-1}} > v_{\text{max}}$$
   Where $v_{\text{max}}$ is set to $40\text{ kn}$ for conventional vessels. Any track segment exhibiting impossible accelerations ($a > 2.5\text{ m/s}^2$) indicates a cellular handover jump or GNSS multipath glitch.
3. **Identity correlation and MMSI scrubbing:** Crowdsourced tracking databases frequently assign pseudo-MMSI numbers (often beginning with `999` or custom 9-digit integers) to app users. These pseudo-identities must be segregated from authoritative ITU-allocated MMSI series ([Chapter 13](ch13-mmsi-deep-dive.md)) to prevent contaminating official maritime spatial planning datasets.

## Software

**Open source:**
- **Wireshark:** Premier open-source packet analyzer. Decodes and parses cellular signaling protocols including SS7 MAP, TCAP, SCCP, Diameter, and 3GPP RRC/NAS over captured PCAP traces. Caveat: Requires pre-configured dissectors and access to decrypted signaling captures.
- **Osmocom (OpenBSC / OsmoGSM):** Open-source implementation of GSM/GPRS mobile network infrastructure. Enables research into cellular radio protocols, base station handovers, and Timing Advance mechanics. Caveat: Strictly for lab and shielded RF environments; transmitting over the air without statutory licenses is illegal.
- **pyais:** Lightweight, pure-Python library for decoding and validating maritime AIS NMEA sentences. Caveat: Processes standard VHF AIS strings; does not ingest raw cellular core signaling packets.

**Free but closed:**
- **SDR# (SDRSharp):** Widely used software-defined radio receiver interface for Windows. Allows visualization of RF spectrum across sub-1 GHz cellular bands and maritime VHF channels. Caveat: Windows-only and closed-source.
- **MarineTraffic Mobile App (Basic Tier):** Widely used consumer smartphone application displaying global ship movements over cellular connections. Caveat: Throttled update rates, significant data latency, and downsampled vessel kinematics make it unsuitable for tactical navigation.

**Commercial:**
- **Cobham SAILOR 4300 / Sea Tel Cellular/VSAT Gateways:** Certified commercial maritime communications terminals managing satellite backhaul and shipboard cellular distribution. Caveat: Capital-intensive hardware requiring specialized installation and satellite airtime contracts.
- **WMS (Wireless Maritime Services) / Telenor Maritime Mobile Cores:** Carrier-grade private maritime cellular picocell networks deployed aboard cruise liners and merchant fleets. Caveat: Proprietary, closed systems accessible only through enterprise maritime telecommunications contracts.

## Standards & guides

- **3GPP TS 29.002:** *Mobile Application Part (MAP) specification*. 3rd Generation Partnership Project. Governs SS7 signaling messages, including `AnyTimeInterrogation`, `SendRoutingInfo`, and subscriber location parameters.
- **3GPP TS 29.272:** *Mobility Management Entity (MME) and Serving GPRS Support Node (SGSN) related interfaces based on Diameter protocol*. Governs 4G LTE core location queries across S6a/S6d interfaces.
- **3GPP TS 36.211:** *Evolved Universal Terrestrial Radio Access (E-UTRA); Physical channels and modulation*. Specifies LTE frame structure, physical channels, and Timing Advance quantization ($16 \cdot T_s$).
- **3GPP TS 45.010:** *Radio subsystem synchronization*. Specifies GSM time-slot alignment and 6-bit Timing Advance mechanics.
- **CEPT ECC/DEC/(08)08:** *Harmonised use of Mobile Communication Services on Board Vessels (MCV)*. European Communications Committee. Establishes technical power limits and the 12-nautical-mile automatic shutoff mandate for shipboard cellular picocells.
- **GSMA FS.11 / FS.19:** *SS7 and Diameter Interconnect Security Monitoring and Firewall Guidelines*. GSM Association. Details operator filtering practices to block malicious external location queries.
- **IMO Resolution A.1106(29):** *Revised Guidelines for the Onboard Operational Use of Shipborne AIS*. International Maritime Organization. Specifies the operational mandate and master's discretion for transponder operation.
- **IMO COLREG (1972):** *Convention on the International Regulations for Preventing Collisions at Sea*. Rules 5 (Look-out) and 7 (Risk of Collision). Mandates all available means appropriate to determine collision risk.
- **ITU Radio Regulations (Article 19):** *Identification of stations*. Governs international radio identification, allocation of MMSI numbers, and prohibitions against maritime frequency interference.
- **Regulation (EU) 2016/679 (GDPR):** *General Data Protection Regulation*. Governs personal data processing, identifiability under Article 4(1), and location privacy for natural persons.

## Pitfalls

- **Using mobile tracking apps for collision avoidance:** Treating a smartphone app with multi-minute latency as a real-time radar or AIS replacement. → App data depends on multi-stage internet routing and throttled cloud updates. → Verify collision risks exclusively with primary radar, line-of-sight VHF AIS on certified displays, and visual lookouts under COLREG Rule 5.
- **Assuming "pseudo-AIS" app broadcasts make craft visible:** Believing that entering a boat's name into a mobile app projects a signal to merchant ships. → Apps upload fixes to internet servers, not the maritime VHF Data Link. ECDIS and radar units cannot receive cellular feeds. → Install a type-approved Class B or B+ SOTDMA transponder to broadcast over international VHF channels.
- **Failing to account for Timing Advance cutoffs at sea:** Wondering why a phone showing full signal bars near the horizon cannot establish data connections. → Base station Timing Advance algorithms enforce strict cell range limits (15–35 km), dropping uplink packets outside the scheduled slot. → Deploy marine routers with high-gain antennas configured for extended-range operation.
- **Carrying active mobile phones during "dark" security transits:** Switching off AIS under IMO A.1106(29) while crew keep personal phones powered on. → Smartphones register with coastal towers or NTN satellites, leaking vessel position through SS7/Diameter networks. → Enforce strict electronic emissions control (EMCON), placing all cellular devices in airplane mode or Faraday enclosures.
- **Deploying oscillating cellular boosters aboard yachts:** Installing uncertified amplifiers with poorly isolated antennas to boost weak signals. → Feedback induces self-oscillation, transmitting broadband noise that jams coastal towers miles away. → Install certified boosters featuring automatic gain control, oscillation detection, and carrier-approved shutdown circuits.
- **Confusing phone GNSS fix timestamps with server ingest timestamps:** Calculating vessel speed from mobile app logs using database record creation time instead of the GPS epoch. → Cellular dead zones cause apps to buffer fixes locally, dumping hours of backlog in a second upon reconnecting, simulating impossible speed spikes. → Parse and sort tracks strictly by internal GNSS fix timestamps (`epoch_utc`).
- **Treating mobile app "vessel IDs" as statutory MMSIs:** Importing crowdsourced mobile tracking databases into spatial models without filtering synthetic identifiers. → Mobile vendors assign arbitrary 9-digit synthetic IDs that collide with national MMSI allocations. → Validate MMSI ranges against ITU-R M.585 series, scrubbing non-standard pseudo-identities.
- **Overlooking Starlink PSU noise on the AIS receiver:** Experiencing unexplained AIS packet loss after installing satellite terminals on the bridge mast. → Switch-mode power supplies and unshielded Ethernet cables emit broadband RF noise across 156–162 MHz. → Maintain 3-meter separation between satcom power units and VHF antennas, using double-shielded coax (RG-214) and ferrite chokes.

## Key takeaways

- Mobile phone applications and crowdsourced internet tracking platforms are **not** substitutes for certified maritime VHF AIS. Internet-relayed position data suffers from variable latencies ranging from 30 seconds to over 15 minutes, rendering it hazardous for collision avoidance under COLREG Rule 7.
- "Pseudo-AIS" apps that transmit a phone's GPS position over cellular networks report exclusively to commercial servers. These broadcasts are completely invisible to commercial shipborne ECDIS displays, marine radars, and coastal VTS stations.
- Over-water cellular propagation is governed by two-ray ground reflection and atmospheric ducting. While downlinks can be received at extended distances, uplink communication is severely constrained by the smartphone's low transmission power ($+23\text{ dBm}$) and strict base station Timing Advance distance cutoffs.
- Shipboard picocells operated on cruise ships and commercial vessels provide mobile connectivity via satellite backhaul, but are legally mandated under CEPT ECC/DEC/(08)08 to shut down automatically within 12 nautical miles of any coastal state.
- Carrying an active mobile phone at sea leaks precise geographical location through telecommunications signaling protocols. Vulnerabilities in SS7 (MAP `ATI` and `SRI-SM`) and 4G/5G Diameter protocols allow adversaries to geolocate vessels by querying public Cell Global Identifiers and Timing Advance parameters.
- Direct-to-cell satellite constellations and LEO broadband systems (such as Starlink Maritime) provide global connectivity to bridge systems, but require careful electromagnetic isolation to prevent switch-mode power supply noise from desensitizing maritime VHF transponders.
- Under data protection laws (such as GDPR), vessel tracking data from privately owned recreational craft and small fishing vessels constitutes personal data, creating legal liabilities for commercial platforms that harvest and republish cellular or mobile location tracks without statutory consent.

## References

- 3GPP (2024). *Mobile Application Part (MAP) specification* (TS 29.002, Release 18). Sophia Antipolis: ETSI.
- 3GPP (2024). *Evolved Packet System (EPS); Mobility Management Entity (MME) and Serving GPRS Support Node (SGSN) related interfaces based on Diameter protocol* (TS 29.272, Release 18). Sophia Antipolis: ETSI.
- 3GPP (2024). *Evolved Universal Terrestrial Radio Access (E-UTRA); Physical channels and modulation* (TS 36.211, Release 18). Sophia Antipolis: ETSI.
- 3GPP (2024). *Radio subsystem synchronization* (TS 45.010, Release 18). Sophia Antipolis: ETSI.
- Balduzzi, M., Pasta, A. & Wilhoit, K. (2014). A Security Evaluation of AIS Automated Identification System. *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC)*, 436–445. doi:10.1145/2664243.2664257
- Engel, T. (2008). *SS7: Locate. Track. Manipulate.* 25th Chaos Communication Congress (25C3), Hamburg, Germany.
- Engel, T. (2014). *SS7 of Nine: Locating, Tracking, and Redirection.* 31st Chaos Communication Congress (31C3), Hamburg, Germany.
- ENISA (2018). *Signalling Security in Telecoms: SS7/Diameter Security Vulnerabilities and Countermeasures*. Athens: European Union Agency for Cybersecurity.
- ENISA (2022). *Security in 5G Signalling Protocols*. Athens: European Union Agency for Cybersecurity.
- European Parliament and Council of the European Union (2016). *Regulation (EU) 2016/679 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data (General Data Protection Regulation)*. Official Journal of the European Union, L 119:1–88.
- GSM Association (2018). *SS7 Interconnect Security Monitoring and Firewall Guidelines* (FS.11). London: GSMA.
- GSM Association (2020). *Diameter Interconnect Security Guidelines* (FS.19). London: GSMA.
- Harati-Mokhtari, A., Wall, A., Brooks, P. & Wang, J. (2007). Automatic Identification System (AIS): Data Reliability and Human Error Implications. *The Journal of Navigation*, 60(3):373–389. doi:10.1017/S037346330700429X
- IMO (1972). *Convention on the International Regulations for Preventing Collisions at Sea (COLREGs)*. London: International Maritime Organization.
- IMO (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). London: International Maritime Organization.
- ITU-R (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band* (Recommendation ITU-R M.1371-5). Geneva: International Telecommunication Union.
- Kholter, S. & Kurbatov, A. (2015). *Diameter Security: The Next Generation of Telecom Vulnerabilities*. Black Hat USA 2015, Las Vegas, NV.
- Toonen, H. M. & Bush, S. R. (2020). The digital frontiers of fisheries governance: fish attraction devices, drones and satellites. *Journal of Environmental Policy & Planning*, 22(1):125–137. doi:10.1080/1523908X.2018.1461084
