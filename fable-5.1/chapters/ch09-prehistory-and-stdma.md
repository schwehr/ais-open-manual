# Chapter 9 — Prehistory: radio, radar, transponders, and the road to a mandate

> **Part II — History.** Tracing the maritime navigational and radio technologies that preceded AIS, the convergence of national tracking trials, Håkan Lans's invention of STDMA, and the regulatory path to a global carriage mandate.

**In this chapter.** You will learn how maritime safety evolved from acoustic signaling and optical watchkeeping to the autonomous, cooperative VHF broadcast network known as the Automatic Identification System (AIS). We trace maritime safety from the loss of RMS *Titanic* in 1912 and the birth of SOLAS in 1914, through marine radar, racons, secondary surveillance transponders, and DGPS. You will examine the post-*Exxon Valdez* regulatory push under OPA-90 that directed the United States Coast Guard toward automated tracking, and analyze parallel tracking trials in the United Kingdom, Panama, and Scandinavia. We examine the architecture of Self-Organizing Time Division Multiple Access (STDMA) invented by Swedish innovator Håkan Lans, review early Swedish and Finnish "4S" field trials, explore the parallel development of VDL Mode 4 in aviation, and trace the patent royalty resolution that cleared the way for global standardization.

## 9.1 From Titanic to SOLAS: the roots of maritime safety

For centuries, collision avoidance on the high seas rested entirely upon human visual observation, the International Regulations for Preventing Collisions at Sea (**COLREGs**), and sound signals propagated through fog. Navigators relied on lookout watchstanders stationed on the forecastle head or bridge wings, peering through darkness and rain to spot oil lamps or listen for whistles, bells, and fog horns. The limitations of optical and acoustic detection were severe: sound waves bend erratically across thermal gradients at sea, and fog blankets can render high-powered lights invisible until a vessel is within hundreds of meters.

The watershed moment in international maritime safety regulation arrived on the night of 14–15 April 1912, when the British passenger liner RMS *Titanic* struck an iceberg in the North Atlantic and sank with the loss of more than 1,500 lives. While *Titanic* was equipped with a state-of-the-art Marconi spark-gap wireless telegraph installation that successfully transmitted distress calls (*CQD* and the newly adopted *SOS*), neighboring ships in the vicinity did not maintain continuous 24-hour radio watches. The SS *Californian*, lying stopped in the ice field less than 20 nautical miles (approximately 37 km) away, had shut down its wireless apparatus for the night when its lone telegraph operator went off duty. 

The disaster provoked immediate international outrage and galvanized the maritime nations of the world into collective diplomatic action. In 1913, the British government convened an international diplomatic conference in London, leading to the adoption on 20 January 1914 of the first **International Convention for the Safety of Life at Sea** (**SOLAS**). The 1914 convention laid down mandatory international requirements for hull subdivision, fireproof bulkheads, life-saving appliances (mandating lifeboats for all persons aboard), and critically, round-the-clock radio telegraphy watchkeeping on passenger ships. SOLAS established the fundamental principle that ships at sea are bound by an international compact to maintain electronic communication for mutual safety and assistance.

Although the outbreak of World War I delayed the formal entry into force of the 1914 treaty, revised iterations followed in 1929, 1948, 1960, and 1974. Across each iteration, safety of navigation evolved from passive rescue equipment toward active, cooperative electronic detection.

## 9.2 Radio, radar, and transponders at sea

The interwar and World War II periods witnessed rapid developments in high-frequency communications, radio direction finding (**RDF**), and microwave radio detection and ranging (**radar**). Centimetric cavity magnetron radars operating in the X-band (9 GHz, 3 cm) and S-band (3 GHz, 10 cm) migrated from naval warships to commercial merchant vessels in the late 1940s and 1950s.

Radar fundamentally transformed navigation: watch officers could now detect coastlines, navigational buoys, and other vessels through blinding fog, torrential rain, and total darkness. Yet marine radar suffered from three fundamental, unalterable physical limitations:
1. **Target anonymity:** Radar detects a physical echo (a primary skin return), not an identity. A blip on a Plan Position Indicator (**PPI**) screen reveals that an object is present, but gives no indication of its name, call sign, vessel type, dimensions, draft, or navigational status. Watch officers attempting to coordinate passing maneuvers over VHF voice radio (Channel 16 or 13) were forced to broadcast blind geographical queries—such as "Ship off my port bow on heading two-seven-zero"—frequently sparking confusion when multiple ships occupied the same quadrant.
2. **Kinematic lag:** Primary radar measures target range and bearing. To determine a target's course and speed over ground, the radar processor or watch officer must track the return over time, either manually on a reflection plotter or automatically via an Automatic Radar Plotting Aid (**ARPA**). Calculating a stable Closest Point of Approach (**CPA**) and Time to Closest Point of Approach (**TCPA**) typically requires one to three minutes of continuous radar observation. If the target maneuvers, alters course, or changes speed, the ARPA vector becomes temporarily invalid until the filter re-converges.
3. **Environmental degradation:** Radar signals are susceptible to sea clutter (returns from waves), rain attenuation, and blind sectors caused by shipboard superstructures, cranes, and container stacks. Furthermore, radar cannot see around blind river bends, islands, or headlands, leaving mariners blind to approaching traffic in winding inland channels.

To augment primary radar returns, hydrographic and lighthouse authorities developed **radar beacons** (**racons**). A racon is a receiver-transmitter transponder installed on a fixed aid to navigation (such as a lighthouse or offshore beacon) or a critical buoy. When an interrogation pulse from a marine radar hits the racon antenna, the unit responds by transmitting a burst on the same frequency that paints a distinctive Morse code character outward along the target's radar radial line on the ship's PPI display. Racons solved the identification problem for critical navigational hazards, but they were narrow in bandwidth, expensive to maintain, and inherently limited to shore infrastructure. They could not provide continuous, dynamic data exchange between moving ships.

In military aviation and civil air traffic control, secondary surveillance radar (**SSR**) solved the identification problem through cooperative transponders. During World War II, the Allies developed **Identification Friend or Foe** (**IFF**), which evolved into the civilian **Air Traffic Control Radar Beacon System** (**ATCRBS**). Under ATCRBS, an airborne transponder listens for ground radar interrogations at 1030 MHz and automatically replies at 1090 MHz, broadcasting a four-digit octal identity code (Mode A) and pressure altitude (Mode C). Later iterations, such as Mode S and Automatic Dependent Surveillance–Broadcast (**ADS-B**), incorporated digital data links and GPS-derived coordinates.

Maritime engineers recognized that if ships could carry an automated transponder analogous to an aviation secondary surveillance beacon, the perpetual ambiguity of primary radar blips would vanish. A bridge officer would instantly see a target's name, call sign, true heading, rate of turn, and GPS-derived position, refreshed multiple times every minute.

## 9.3 Exxon Valdez, OPA-90, and the American push for tracking

On 24 March 1989, the 987-foot crude oil tanker *Exxon Valdez* ran aground on Bligh Reef in Alaska's Prince William Sound, spilling approximately 11 million US gallons (260,000 barrels) of crude oil into pristine subarctic waters. The official accident investigation by the National Transportation Safety Board (NTSB 1990) revealed severe breakdowns in bridge resource management, watchkeeping discipline, and coastal vessel surveillance. 

At the time of the grounding, the United States Coast Guard operated a **Vessel Traffic Service** (**VTS**) in Valdez. However, the VTS radar installations had dead zones and limited range: the radar equipment at Potato Point could not track *Exxon Valdez* out to Bligh Reef, and the shore watchstanders had lost track of the tanker after it altered course outside the established Traffic Separation Scheme (**TSS**) lanes to avoid floating glacial ice. Coast Guard operators relied on periodic, voluntary VHF voice reports from vessel masters. When *Exxon Valdez* struck Bligh Reef, the VTS watchstanders were completely unaware that the vessel had strayed miles off course until the master radioed thirty minutes after the impact to report that the ship was hard aground.

The catastrophic environmental and economic damage prompted the United States Congress to enact the **Oil Pollution Act of 1990** (**OPA-90**, Public Law 101-380). OPA-90 enacted sweeping reforms, mandating double hulls for newly constructed oil tankers, establishing comprehensive oil spill liability regimes, and under Section 4107, directing the Secretary of Transportation to modernize vessel traffic services and examine automated tanker surveillance systems in Prince William Sound and other high-risk American waterways.

The United States Coast Guard Research and Development Center (**RDC**) and headquarters acquisition teams were charged with finding a technological solution that could automate vessel tracking. The Coast Guard needed a system capable of broadcasting accurate, continuous vessel tracks directly into shore VTS centers without requiring human radio operator intervention.

Under the Ports and Waterways Safety System (**PAWSS**) modernization program in the late 1990s, the Coast Guard evaluated transponder architectures to augment shore-based radar. In 1998, the Coast Guard designated the Port of New Orleans and the Lower Mississippi River—a dense, high-traffic, riverine waterway with treacherous currents and blind river bends—as the testbed for its first primarily transponder-based VTS network. Yet in the early 1990s, the international maritime community had no agreed data standard, no dedicated radio spectrum, and no common channel-access protocol for shipboard transponders.

> **Case file.** In its formal marine accident report on the *Exxon Valdez* disaster (NTSB 1990), the National Transportation Safety Board documented that the Coast Guard Vessel Traffic Center in Valdez had failed to maintain radar tracking of the tanker as it departed the designated traffic lanes. The NTSB emphasized that reliance on periodic voice position reports over VHF-FM radio was fundamentally inadequate for monitoring hazardous cargo vessels in restricted or environmentally sensitive waterways. This finding directly catalyzed the congressional mandate in OPA-90 to develop automated, non-voice electronic vessel tracking.

## 9.4 Parallel tracking trials: Dover, Panama, and Scandinavia

Between 1990 and 1996, several maritime administrations and waterway operators independently launched prototype transponder tracking experiments. Each trial reflected the specific operational geometry and local priorities of its sponsoring authority.

As recounted by USCG Program Analyst Jorge Arroyo in his historical survey of AIS origins (Cutlip 2017), four distinct technological streams emerged concurrently:

1. **The British Dover Strait VHF trials:** The United Kingdom Maritime and Coastguard Agency (**MCA**) and the Channel Navigation Information Service (**CNIS**) sought to manage the intense traffic flow transiting the Dover Strait—the world's busiest maritime bottleneck. The British conducted trials using maritime VHF-FM channels to pass automated data packets between ships and coastal monitoring stations. However, these systems relied on conventional polling from shore base stations or fixed time-division multiplexing, which degraded rapidly as vessel counts scaled upward.
2. **The Panama Canal Commission UHF trials:** The Panama Canal Commission faced the unique operational challenge of guiding Panamax vessels through the narrow, twisting cuts of Gaillard (Culebra) Cut and the lock chambers of Miraflores, Pedro Miguel, and Gatun. Dense jungle topography and mountainous terrain created severe radar masking and multipath reflections. The Canal Commission developed and trialed a transponder tracking system operating in the Ultra High Frequency (**UHF**) band (around 400–450 MHz) to track canal transits and assist canal pilots with precision positioning. Because UHF operates strictly within localized radio line of sight and required proprietary canal transponder installations, it was unsuitable as an open-ocean, global standard.
3. **The American VTS and DGPS developments:** Following OPA-90, the United States Coast Guard focused heavily on establishing an automated coastal radio infrastructure. A key technical enabler was the national **Differential GPS** (**DGPS**) beacon network, constructed across the U.S. coasts and inland rivers in the mid-1990s. The DGPS network broadcast pseudorange corrections from surveyed shore reference stations over maritime medium-frequency (**MF**) radiobeacons (285–325 kHz) using Minimum Shift Keying (**MSK**) per standard RTCM SC-104. This represented the first widespread civilian maritime digital broadcast system. It gave shipboard GPS receivers sub-meter positional accuracy, demonstrating the viability of digital data broadcasts for navigation.
4. **The Swedish and Scandinavian trials:** In Scandinavia, the Swedish Maritime Administration (**Sjöfartsverket**) took an entirely different architectural path. Rather than relying on shore-based radar polling or localized UHF links, Swedish engineers embraced an innovative peer-to-peer data link conceived by Swedish inventor **Håkan Lans**: Self-Organizing Time Division Multiple Access (**STDMA**).

## 9.5 Håkan Lans, STDMA, and the GP&C system

The breakthrough that made modern AIS technically feasible was the invention of **Self-Organizing Time Division Multiple Access** (**STDMA**) by Håkan Lans.

Lans, an accomplished Swedish independent inventor who had previously made foundational contributions to computer color graphics and digitizer pucks, turned his attention in the late 1980s to the challenge of tracking mobile craft in three-dimensional space without centralized ground control. In civil aviation and maritime transport, the traditional multiple-access radio schemes suffered from crippling bottlenecks:
- **Polling (interrogation-reply):** A central master station sequentially polls each mobile unit, which then replies. If the master station fails, the entire network collapses. Furthermore, polling scales linearly with population: as more craft enter the area, the polling cycle lengthens, reducing the position update rate to unacceptable levels. Polling cannot support autonomous ship-to-ship collision avoidance on the high seas outside shore radio coverage.
- **Random access (ALOHA / CSMA):** In pure ALOHA or Carrier Sense Multiple Access (**CSMA**), stations transmit when they have data to send, detecting or avoiding collisions. Under heavy network loading, packet collisions multiply exponentially, causing channel throughput to collapse into instability—a phenomenon well known in packet radio networks.
- **Fixed TDMA:** Fixed time-division networks require a central master to allocate specific time slots to specific users. While collision-free, fixed TDMA cannot accommodate mobile units constantly moving into and out of local radio cells.

Lans solved this fundamental dilemma by coupling two emerging technological revolutions: the microsecond-accurate atomic time standard broadcast globally by the **Global Positioning System** (**GPS**), and high-speed digital radio frequency modulation.

On 1 July 1991, Lans filed a patent application in Sweden (SE 9102034), followed by international applications under the Patent Cooperation Treaty (PCT/SE92/00485, filed 29 June 1992; published as WO 93/01576 on 21 January 1993). The invention was granted in Sweden as SE 468,452 B on 18 January 1993, in the United States as **US Patent 5,506,587 A** on 9 April 1996, and in Europe as **EP 0 592 560 B1** on 27 August 1997, with Lans assigning rights to his intellectual property holding entity, **GP&C Systems International AB** (Lans 1993, Lans 1996, Lans 1997).

> **Case file.** Lans's United States patent, US 5,506,587 A, titled *"Position indicating system,"* established the definitive architectural concept of STDMA in Claim 1. The patent claims a population of movable stations each equipped with a GPS navigation receiver and a radio transceiver. The stations derive an absolute, common time base from the satellite signals, establishing a continuously repeating "maximal frame" divided into standardized, enumerable time blocks (slots). Each station autonomously selects a free time block in the frame and transmits its identity and coordinates, embedding in that transmission an advance reservation announcing which time block it will occupy in subsequent frames.

By embedding the reservation for future transmission slots directly inside the payload of the current transmission, every listening station within radio horizon maintains an identical, real-time map of channel occupancy. A newly arriving vessel simply listens to the channel for one complete frame (one minute), builds an internal registry of occupied and free slots, and then autonomously claims unoccupied slots without causing interference to existing users.

```
       1-Minute TDMA Frame (2,250 Slots, 26.67 ms each)
+--------+--------+--------+--------+--------+-----+--------+
| Slot 0 | Slot 1 | Slot 2 | Slot 3 | Slot 4 | ... |Slot2249|
+--------+--------+--------+--------+--------+-----+--------+
    |                                   |
    v                                   v
[Transmission in Slot 0]          [Next Reserved Slot]
 Payload contains data +          (e.g., Slot 1125 announced
 advance reservation offset       in Slot 0 comm-state)
```

In 1990, the Swedish Maritime Administration, guided by visionary mariners and engineers including pilot Benny Pettersson, recognized the transformative safety potential of Lans's invention. Sjöfartsverket Director General Kaj Janérus approved an initial research grant of SEK 2 million to develop and test maritime transponders based on the Lans GP&C concept (SMA 2018).

The origin of Benny Pettersson's dedication to transponder tracking dated back to 1965, when as a young navigating officer aboard a Swedish merchant vessel in the harbor of Kobe, Japan, his ship was caught in a violent typhoon. Blinding torrential rain, driving sea spray, and violent wave motion completely blinded both optical lookouts and the ship's primitive marine radar. Pettersson realized that navigating in zero visibility demanded an autonomous, transponder-based system capable of broadcasting ship identity, position, and motion through any meteorological obstruction.

## 9.6 Swedish and Finnish trials: "4S" and Lake Vänern

Between 1991 and 1994, the Swedish Maritime Administration, in close technical collaboration with the Finnish Maritime Administration (under engineers Bertil Arvidsson, Rolf Zetterberg, and Rolf Bäckström), deployed prototype STDMA transponders in active maritime operations.

The earliest tests, known as the **Automatic Vessel Monitoring System** (**AVMS**), evaluated prototype transponders aboard commercial passenger and freight ferries operating between Stockholm, Sweden, and Turku and Helsinki, Finland. Concurrently, Sweden and Finland became the first maritime nations to establish operational coastal maritime DGPS networks conforming to the international standards of the International Association of Marine Aids to Navigation and Lighthouse Authorities (**IALA**). By integrating DGPS receivers with STDMA VHF transponders, the Swedish and Finnish teams achieved positional accuracies of 1 to 3 meters in real time.

In 1993, Sjöfartsverket launched extensive full-scale operational trials on the **Trollhätte Canal** and **Lake Vänern**, as well as aboard the archipelago passenger ferries of the **Styrsöbolaget** fleet operating in the congested rocky approaches to Gothenburg. Approximately ten commercial passenger ferries, tugs, and pilot cutters were outfitted with GP&C transponders developed jointly with the Swedish Space Corporation. Shore-based Vessel Traffic Service radar displays, developed by Norwegian marine electronics manufacturer **NorControl**, were modified to ingest the VHF data bursts. For the first time in maritime history, watch officers on ship bridges and operators in shore VTS centers watched electronic vector symbols move across nautical chart displays in real time, labeled with ship names, dimensions, and millimeter-precise GPS rates of turn.

The Scandinavian authorities designated the experimental architecture the **"4S" system**, signifying:
- **S**hip-to-**S**hip, and
- **S**hip-to-**S**hore communications.

The "4S" trials proved four decisive operational hypotheses:
1. **True autonomy:** Transponders operated reliably in peer-to-peer mode in open waters beyond any shore base station coverage.
2. **Channel resilience:** The STDMA slot-selection algorithms dynamically adapted to changing vessel concentrations without packet collapse or channel lockup.
3. **Display integration:** Integrating dynamic transponder vectors with electronic chart systems and radar PPI displays drastically reduced bridge workload during close-quarters encounters.
4. **VTS enhancement:** Shore operators could track vessels through radar blind spots created by fjord topography, islands, and canal locks.

## 9.7 The aviation parallel: VDL Mode 4

While the maritime community was trialing "4S" in the Baltic, the civil aviation sector was grappling with its own air traffic management crisis. Air traffic density was overwhelming traditional voice radio channels and secondary surveillance radar facilities in European and North American terminal airspace.

Håkan Lans and GP&C Systems International had originally designed STDMA primarily for aeronautical applications (Lans 1996). Under the auspices of the **International Civil Aviation Organization** (**ICAO**), European and international aviation bodies evaluated STDMA as a candidate for next-generation aeronautical digital data links, designating the standard **VHF Data Link Mode 4** (**VDL Mode 4**).

Operating in the civil aviation VHF communications band (118.000–136.975 MHz), VDL Mode 4 used Gaussian Filtered Frequency Shift Keying (**GFSK**) modulation and STDMA link-layer timing to provide:
- **Automatic Dependent Surveillance–Broadcast (ADS-B):** Aircraft continuously broadcasting altitude, identity, airspeed, and GPS position;
- **Traffic Information Services–Broadcast (TIS-B):** Ground stations relaying radar targets to aircraft cockpits;
- **Flight Information Services–Broadcast (FIS-B):** Meteorological and airspace warnings; and
- **Point-to-point data exchange:** Controller-pilot data link communications (CPDLC).

The technical parallels between maritime AIS and aeronautical VDL Mode 4 were extensive: both shared the identical STDMA slot map geometry, 1-minute frame cycle, and GPS-synchronized slot timing. 

However, civil aviation and commercial maritime navigation diverged sharply in their regulatory execution. In civil aviation, intense industrial competition and institutional resistance from major avionics manufacturers and the United States Federal Aviation Administration (**FAA**)—which favored the 1090 MHz Mode S Extended Squitter (1090ES) and 978 MHz Universal Access Transceiver (UAT) architectures—stalled the widespread deployment of VDL Mode 4. In contrast, the maritime world had no entrenched legacy transponder infrastructure equivalent to secondary radar. The International Maritime Organization was able to adopt the STDMA architecture cleanly as the sole, universal standard for the maritime mobile service.

> **Definitions that bite.**
> - **STDMA (Self-Organizing Time Division Multiple Access):** The overarching algorithmic principle patented by Håkan Lans wherein stations use a common time base (typically GNSS UTC) to divide a radio channel into discrete time slots and autonomously negotiate channel reservations without centralized arbitration.
> - **SOTDMA (Self-Organizing TDMA per ITU-R M.1371):** The specific international link-layer protocol standardized in Recommendation ITU-R M.1371 Annex 2 for maritime Class A transponders, operating at 9,600 bit/s GMSK across 2,250 slots per minute.
> - **CSTDMA (Carrier-Sense TDMA):** The polite, listen-before-transmit protocol standardized in IEC 62287-1 and ITU-R M.1371 Annex 6 for Class B recreational/small-craft transponders, designed specifically to avoid interfering with SOTDMA while evading the original Lans patent claims.

## 9.8 Four streams converge at IMO, ITU, and IALA

By 1994, it was clear to international safety regulators that the piecemeal proliferation of incompatible national vessel transponders threatened to fracture the global maritime industry. A container ship sailing from Rotterdam to New York and transiting the Panama Canal could not carry three separate transponder systems operating on different frequencies and protocols.

In 1994, the Swedish Maritime Administration submitted a formal proposal to the IMO Maritime Safety Committee (MSC) at its 40th Sub-Committee on Safety of Navigation (**NAV 40**), introducing the "4S" STDMA transponder concept. Over the next three years, intense technical debates occurred within the working groups of three key international bodies:
1. **The International Maritime Organization (IMO):** Setting international carriage mandates, functional requirements, and operational performance standards.
2. **The International Telecommunication Union Radiocommunication Sector (ITU-R):** Allocating worldwide radio spectrum and defining modulation, packet structures, and physical-layer radio characteristics.
3. **The International Association of Marine Aids to Navigation and Lighthouse Authorities (IALA):** Harmonizing shore station architecture, operational guidelines, and aids-to-navigation protocols.

The four experimental tracking streams that had emerged in the early 1990s converged. The British Dover Strait VHF trials and the American post-*Exxon Valdez* VTS initiatives recognized that centralized polling could not operate on the high seas. The Panama Canal Commission recognized that localized UHF systems could not serve international voyages. The Swedish STDMA system offered the only demonstrated, mathematically robust, peer-to-peer radio link layer capable of meeting all three foundational IMO requirements: ship-to-ship collision avoidance, coastal surveillance, and vessel traffic management.

In 1997, the World Radiocommunication Conference (**WRC-97**) convened by the ITU made a historic frequency allocation. The conference designated two worldwide, dedicated 25 kHz simplex channels in Appendix 18 of the Radio Regulations for international maritime transponders:
- **AIS 1:** Channel 87B, 161.975 MHz
- **AIS 2:** Channel 88B, 162.025 MHz

Dual-channel operation was deliberately chosen to ensure channel redundancy, mitigate multipath fading, and provide a combined capacity of 4,500 time slots per minute.

Concurrently, the IMO Maritime Safety Committee adopted **Resolution MSC.74(69), Annex 3** on 12 May 1998, formally establishing the *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (IMO 1998). In November 1998, the ITU published the foundational technical specification: **Recommendation ITU-R M.1371-0**, titled *Technical characteristics for a universal shipborne automatic identification system using time division multiple access in the VHF maritime mobile band* (ITU 1998a).

## 9.9 The patent royalty question: clearing the way for a mandate

Before the IMO could amend the SOLAS convention to make AIS installation legally mandatory across the world's commercial merchant fleet, a profound legal and intellectual property hurdle had to be resolved.

Under international treaty conventions and the common patent policies of the ITU, ISO, and IEC, international standards bodies generally prohibit mandating proprietary, patented technology unless the patent holder commits to licensing the essential intellectual property on reasonable and non-discriminatory (**RAND**) terms or royalty-free terms.

Håkan Lans held issued patents in Sweden, the United States, and Europe covering the core STDMA time-slot reservation mechanism (Lans 1993, Lans 1996, Lans 1997). While Lans formally accepted the ITU Code of Practice for standardized patented systems, several prominent IMO member states—most notably Japan, the United Kingdom, and the United States—strongly resisted the prospect of compelling sovereign and private shipowners by international law to purchase hardware encumbered by recurring patent royalty payments to a private inventor's holding company (SMA 2018). The consensus required to amend SOLAS was threatened with collapse.

To resolve the impasse and enable his technological vision to become a universal lifesaver at sea, Håkan Lans made a decisive historic concession. Working in cooperation with the Swedish Maritime Administration, Lans formally agreed to waive all compensation and royalty claims for the use of the STDMA patent on all commercial and passenger vessels covered by the IMO SOLAS mandatory carriage requirements (SMA 2018).

> **Worked example.**
> Consider the fundamental time-division slot budget defined by Lans's STDMA and codified in ITU-R M.1371 Annex 2:
> 
> 1. **Frame duration:** Exactly 1 minute (60 seconds), synchronized to the UTC second boundary via GPS.
> 2. **Slots per frame per channel:** Exactly 2,250 slots.
> 3. **Slot duration:**
>    $$T_{\text{slot}} = \frac{60\text{ s}}{2,250} = 0.026667\text{ s} = 26.67\text{ ms}$$
> 4. **Channel bit rate:** 9,600 bits per second (bit/s).
> 5. **Raw bit budget per slot:**
>    $$N_{\text{bits}} = 0.026667\text{ s} \times 9,600\text{ bit/s} = 256\text{ bits}$$
> 6. **Fixed protocol overhead:** 88 bits (8-bit power ramp-up, 24-bit preamble training sequence, 8-bit HDLC start flag `0x7E`, 16-bit CRC-CCITT frame check sequence, 8-bit HDLC end flag `0x7E`, and 24-bit buffer budget covering bit-stuffing, distance delay, and sync jitter).
> 7. **Available message payload:**
>    $$\text{Payload} = 256\text{ bits} - 88\text{ bits} = 168\text{ bits}$$
> 
> This elegant 168-bit slot payload accommodates standard dynamic position reports (Messages 1, 2, and 3) in a single burst, providing the exact capacity needed for global collision avoidance.

With the patent royalty roadblock dismantled, the IMO Maritime Safety Committee convened on 5 December 2000 to adopt **Resolution MSC.99(73)**, enacting a comprehensive overhaul of **SOLAS Chapter V** (*Safety of Navigation*) (IMO 2000). Under revised Regulation 19.2.4, the international carriage mandate was enacted into law, setting the world on an irreversible course toward universal electronic maritime tracking, as detailed in [Chapter 10](ch10-standardization-1996-2004.md).

> **Try it.**
> Verify the STDMA frame parameters and run a slot-allocation simulation using the companion code repository:
> ```bash
> cd /usr/local/google/home/schwehr/sdd-books/ais/fable
> . .venv/bin/activate
> python code/tdma/sotdma_sim.py --n-a 60 --n-b 40
> ```
> Expected simulation output:
> ```text
> {'a_tx': 985, 'a_collided': 0, 'b_tx': 280, 'b_deferred': 0, 'slots_used': 1265, 'slots_jammed': 0, 'occupancy': 0.112, 'a_loss_rate': 0.0, 'b_defer_rate': 0.0}
> ```
> This verifies that at moderate traffic density (60 Class A and 40 Class B vessels), SOTDMA maintains zero packet collisions (`a_collided: 0`) and zero Class B deferrals (`b_deferred: 0`) across 1,265 occupied slots (11.2% link occupancy).

## Then & now

- ⟨H⟩ 1904 — Christian Hülsmeyer patents the *Telemobiloscope*, the earliest spark-gap radar device capable of detecting remote metallic objects to prevent ship collisions in fog.
- ⟨H⟩ 1912 — Sinking of RMS *Titanic* on 14–15 April demonstrates the catastrophic consequences of discontinuous radio watchkeeping and reliance on visual lookouts in ice-infested waters.
- ⟨H⟩ 1914 — First International Convention for the Safety of Life at Sea (SOLAS) adopted in London, establishing mandatory 24-hour radio telegraphy watches for passenger ships.
- ⟨+⟩ 1940 — Centimetric cavity magnetron radar developed, migrating to merchant shipping after World War II for primary skin-return collision detection.
- ⟨H⟩ 1973 — Air Traffic Control Radar Beacon System (ATCRBS) secondary surveillance radar transponders established in civil aviation, demonstrating automated identification and altitude reporting.
- ⟨H⟩ 1978 — First GPS Block I satellite launched, inaugurating the atomic-clock satellite constellation that provides microsecond-accurate global time synchronization.
- ⟨H⟩ 1984 — NMEA 0183 standard first released, establishing serial data exchange for marine navigational electronics.
- ⟨+⟩ 1989 — Grounding of the tanker *Exxon Valdez* in Prince William Sound, Alaska, leads to OPA-90 and the US Coast Guard mandate for automated vessel tracking.
- ⟨+⟩ 1991 — Håkan Lans files Swedish patent application SE 9102034 on 1 July for the STDMA autonomous position indicating system.
- ⟨+⟩ 1993 — Swedish Maritime Administration and Finnish Maritime Administration conduct "4S" maritime transponder trials on Lake Vänern, Trollhätte Canal, and Styrsöbolaget passenger ferries.
- ⟨+⟩ 1996 — US Patent 5,506,587 A granted to Håkan Lans on 9 April for STDMA; coastal DGPS networks establish high-accuracy positioning across Scandinavia and the United States.
- ⟨+⟩ 1997 — ITU World Radiocommunication Conference (WRC-97) allocates channels AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz) in Appendix 18 of the Radio Regulations.
- ⟨+⟩ 1998 — IMO adopts Resolution MSC.74(69) Annex 3 on 12 May establishing AIS performance standards; ITU publishes Recommendation ITU-R M.1371-0 in November defining technical characteristics; Lans waives patent royalties for SOLAS-mandated vessels.
- ⟨+⟩ 2000 — IMO adopts revised SOLAS Chapter V (Resolution MSC.99(73)) on 5 December, mandating universal AIS carriage for commercial shipping beginning 1 July 2002.
- ⟨+⟩ 2013 — Håkan Lans's US Patent 5,506,587 A reaches full statutory expiration on 9 April (following claim cancellation during ex parte reexamination in 2010), placing foundational STDMA architecture entirely in the public domain.
- ⟨+⟩ 2026 — ITU publishes Recommendation ITU-R M.1371-6, reflecting nearly three decades of worldwide operational maturity for maritime STDMA.

## Validation, uncertainty & data quality

In evaluating the historical and technical claims surrounding early maritime tracking systems, analysts and software engineers encounter three pervasive categories of error: revisionist chronology, patent scope conflation, and sensor-accuracy anachronisms.

### Historical document validation

When auditing historical regulatory timelines, researchers must distinguish between three distinct milestones:
1. **Adoption date:** When an international body (such as the IMO MSC) approves a resolution text.
2. **Entry-into-force date:** When a treaty amendment becomes binding international law upon contracting governments.
3. **Carriage phase-in date:** The specific calendar deadline by which a vessel of a particular class or tonnage must physically install and certify equipment.

For example, secondary literature frequently asserts that "AIS was mandated in 1998" (confusing the MSC.74(69) performance standard recommendation with a mandatory treaty carriage requirement), or that "9/11 caused the AIS mandate" (ignoring the fact that SOLAS Regulation 19.2.4 had already been adopted in December 2000, nine months prior to September 2001). As detailed in [Chapter 10](ch10-standardization-1996-2004.md), the post-9/11 diplomatic conference in December 2002 merely accelerated the phase-in schedule for existing mandates.

### Patent scope and claim validation

A frequent pitfall in technological history is treating broad patent abstracts as literal descriptions of deployed systems. Lans's US Patent 5,506,587 contains 13 claims. Crucially, the patent description is written almost entirely around aeronautical terminology (referencing Air Control Centers, Flight Information Centers, and Flight Information Regions), reflecting Lans's initial focus on aviation VDL Mode 4. 

Furthermore, researchers must maintain strict distinction between two separate legal proceedings involving Håkan Lans:
- **The color-graphics standing litigation (*Lans v. Digital Equipment Corp.*, 252 F.3d 1320 (Fed. Cir. 2001)):** A patent infringement suit involving US Patent 4,303,986 (computer color graphics) that Lans lost on procedural standing because he had assigned the patent to his holding company Uniboard AB. This case had no technical bearing on maritime STDMA.
- **The STDMA ex parte reexamination:** A patent reexamination proceeding at the United States Patent and Trademark Office (**USPTO**) in 2010 concerning US Patent 5,506,587, which resulted in the cancellation of patent claims in the United States prior to statutory expiration.

### Sensor accuracy and Selective Availability

When re-evaluating historical AIS and DGPS data logs from the 1990s and early 2000s, engineers must account for the state of the Global Positioning System at the time of transmission. 

Prior to 2 May 2000 (when President Bill Clinton ordered the termination of **Selective Availability** (**SA**)), the United States Department of Defense intentionally degraded civilian GPS satellite signals. Standalone, unaugmented GPS receivers exhibited horizontal 95% 2-dimensional root-mean-square ($2\text{drms}$) errors of up to 100 meters, accompanied by pseudorange velocity dithering. 

Consequently, early 1990s "4S" maritime trials in Sweden and Finland were strictly dependent on coastal **DGPS** beacon stations transmitting pseudorange corrections. Without DGPS corrections, autonomous GPS-derived rates of turn and close-quarters collision-avoidance vectors in 1993 would have suffered from intolerable positional jitter. Modern AIS datasets collected after May 2000 operate with unaugmented GPS horizontal accuracies of 3 to 5 meters, and sub-meter accuracy when augmented by Satellite-Based Augmentation Systems (**SBAS**) such as WAAS or EGNOS (as analyzed in [Chapter 25](ch25-gnss-and-ais.md)).

## Software

The software tools relevant to this historical chapter encompass open-source simulation scripts, historical protocol parsers, and commercial Vessel Traffic Service platforms:

**Open source:**
- `code/tdma/sotdma_sim.py` (The AIS Handbook companion repository) — Implements a discrete-event teaching model of SOTDMA slot allocation, candidate-slot selection, and CSTDMA carrier sensing over a 2,250-slot frame. Caveat: models single-cell slot contention; does not simulate RF propagation loss or multi-hop repeater networks.
- `libais` (Schwehr et al.) — Industry-standard open-source C++ library with Python bindings for decoding ITU-R M.1371 AIVDM/AIVDO NMEA sentence payloads. Caveat: decodes message payloads; does not parse raw physical-layer GMSK IQ waveforms.
- `AIS-catcher` (Jasper van de Erve) — High-performance Software Defined Radio (SDR) receiver and demodulator for decoding live VHF AIS signals from RTL-SDR and Airspy dongles. Caveat: requires physical SDR hardware and adequate RF antenna siting.

**Free but closed:**
- `OpenCPN` (Open Source Navigation Community) — Chartplotter and navigational display software supporting NMEA 0183/2000 AIS target visualization, CPA/TCPA calculations, and historical track rendering. Caveat: interface configurations vary widely across operating systems.

**Commercial:**
- `NorControl VTS` (now Kongsberg Norcontrol) — Commercial Vessel Traffic Service management and radar/AIS target tracking system deployed during the original 1993 Swedish Maritime Administration "4S" trials. Caveat: proprietary commercial software requiring enterprise licensing and specialized radar processor interfaces.
- `Transas Navi-Harbour` (now Wärtsilä) — Commercial shore-based VTS software platform integrating coastal radar tracking, direction finding, and AIS base station telemetry. Caveat: closed-source proprietary platform.

## Standards & guides

- **IMO Resolution MSC.74(69), Annex 3 (1998):** *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)*. Established the foundational functional requirements for autonomous ship-to-ship and ship-to-shore transponders.
- **IMO Resolution MSC.99(73) (2000):** *Adoption of Amendments to the International Convention for the Safety of Life at Sea (SOLAS), 1974, as Amended*. Codified mandatory AIS carriage under SOLAS Chapter V, Regulation 19.2.4.
- **ITU-R Recommendation M.1371-0 (1998):** *Technical characteristics for a universal shipborne automatic identification system using time division multiple access in the VHF maritime mobile band*. The original international technical specification for SOTDMA link-layer timing, GMSK modulation, and packet structures.
- **ITU-R Recommendation M.1371-5 (2014):** *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Widely deployed revision specifying Class A, Class B, AtoN, and SAR transmitter characteristics.
- **ITU-R Recommendation M.1371-6 (2026):** *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Current governing edition for maritime mobile TDMA characteristics.
- **ITU Radio Regulations, Appendix 18 (WRC-97):** *Table of transmitting frequencies in the VHF maritime mobile band*. Formally allocated simplex frequencies 161.975 MHz (AIS 1) and 162.025 MHz (AIS 2) for worldwide maritime mobile use.
- **RTCM Standard 10402.3 (RTCM SC-104):** *Recommended Standards for Differential NAVSTAR GPS Service*. Defined the digital correction messages broadcast over coastal MF radiobeacons that enabled high-precision positioning during early Scandinavian transponder trials.
- **US Public Law 101-380 (OPA-90) (1990):** *Oil Pollution Act of 1990*. Federal statute mandating automated vessel tracking evaluations and VTS modernization across the United States.

## Pitfalls

1. **Assuming AIS was invented in the United States post-9/11** → Many security and defense publications incorrectly trace the origin of AIS to post-September 11 homeland security initiatives → Examine the historical record: the technical standard (ITU-R M.1371-0) was approved in 1998 and the SOLAS carriage mandate was enacted in December 2000, both pre-dating 2001.
2. **Confusing STDMA with pure CSMA or ALOHA** → Engineers unfamiliar with time-division radio networks assume AIS transponders transmit randomly or simply "listen before talking" → Study ITU-R M.1371 Annex 2: Class A transponders use deterministic, synchronized time slots synchronized to GPS UTC, reserving future transmission slots in advance.
3. **Conflating the 1990s color-graphics patent suit with the STDMA patent** → Biographers and researchers frequently cite *Lans v. Digital Equipment Corp.* as proof that Lans's transponder patent was rejected by federal courts → Verify the patent numbers: *Lans v. DEC* concerned US Patent 4,303,986 (color graphics), which failed on procedural standing, not the STDMA patent (US 5,506,587).
4. **Asserting that OPA-90 explicitly created AIS** → Analysts assume Congress wrote the AIS technical standard into federal law in 1990 → Read OPA-90 Section 4107: the statute mandated automated vessel tracking evaluations and VTS improvements; the technical realization arrived through international convergence at IMO and ITU.
5. **Believing secondary radar transponders (ATCRBS) could be ported directly to sea** → Proposers suggested adopting aviation radar transponders for ships → Aviation SSR relies on rotating ground radar interrogators; ships on the open ocean require a peer-to-peer broadcast system that functions without any shore interrogation infrastructure.
6. **Overlooking the role of Selective Availability in early trials** → Modelers attempting to replicate 1993 trial data find extreme drift in uncorrected GPS coordinates → Account for Selective Availability, which was active until 2 May 2000; early maritime trials were universally dependent on coastal DGPS correction broadcasts.
7. **Assuming Lans held an active monopoly on AIS through 2020** → Commentators claim commercial shipping was forced to pay millions in patent royalties to GP&C → Review the 1998 IMO negotiations: Lans waived patent royalties for all SOLAS-mandated vessels to facilitate global adoption, and the patent expired in 2013.
8. **Treating primary radar and AIS as competing, mutually exclusive sensors** → Watchstanders or analysts treat AIS as an outright replacement for marine radar → Remember COLREGs Rule 5 and Rule 7: radar detects physical hazards (icebergs, non-transmitting vessels, debris) that AIS cannot see, while AIS identifies and tracks cooperative targets through blind turns and severe weather.
9. **Misunderstanding why two VHF channels are used** → Technicians assume AIS 1 is for ship-to-ship and AIS 2 is for ship-to-shore → Read ITU-R M.1371: transponders alternate transmissions packet-by-packet across both channels (AIS 1 and AIS 2) to mitigate interference, improve link reliability, and double capacity.

## Key takeaways

- The loss of RMS *Titanic* in 1912 produced the first SOLAS treaty in 1914, establishing the legal requirement for continuous radio watchkeeping that underpins modern maritime electronic safety.
- While post-WWII marine radar transformed navigation in low visibility, it suffered from target anonymity, tracking lag (ARPA convergence latency), sea clutter attenuation, and topographical line-of-sight masking.
- The 1989 *Exxon Valdez* disaster and OPA-90 compelled the United States Coast Guard to pioneer automated vessel tracking, modernizing Vessel Traffic Services with New Orleans serving as the first transponder-centric port.
- Concurrently, experimental tracking programs emerged in the UK (Dover Strait VHF trials) and Panama (Panama Canal Commission UHF trials), but localized and polled architectures failed to scale globally.
- Swedish inventor Håkan Lans solved the autonomous channel-access challenge by inventing Self-Organizing Time Division Multiple Access (STDMA), synchronizing radio transmission slots to GPS UTC.
- Full-scale operational trials by the Swedish and Finnish Maritime Administrations on Lake Vänern and the Trollhätte Canal in 1993 proved that the "4S" transponder system delivered unprecedented collision avoidance and VTS tracking.
- Civil aviation evaluated the identical STDMA link layer as VDL Mode 4, but commercial rivalries and institutional delays stalled deployment, allowing the maritime sector to become the premier global user of STDMA.
- To overcome member-state resistance to mandating patented technology in international treaties, Håkan Lans waived patent royalties for all SOLAS-mandated ships, clearing the regulatory path for IMO Resolution MSC.74(69) in 1998 and the revised SOLAS Chapter V mandate in 2000.
- Appendix 18 of the ITU Radio Regulations established dedicated worldwide frequencies on channels AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz), creating a synchronized global tracking commons operating across 4,500 time slots per minute.

## References

- Cutlip, K. (2017). *AIS for Safety and Tracking: A Brief History*. Global Fishing Watch. URL: https://globalfishingwatch.org/article/ais-brief-history/
- Ellison, B. (2015). *SRT acquires Class B AIS patent, consequences uncertain*. Panbo: The Marine Electronics Hub. URL: https://www.panbo.com/srt-acquires-class-b-ais-patent-consequences-uncertain/
- International Maritime Organization (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)*. Resolution MSC.74(69), Annex 3. London: IMO.
- International Maritime Organization (2000). *Adoption of Amendments to the International Convention for the Safety of Life at Sea, 1974, as Amended (SOLAS Chapter V)*. Resolution MSC.99(73). London: IMO.
- International Telecommunication Union (1998a). *Technical characteristics for a universal shipborne automatic identification system using time division multiple access in the VHF maritime mobile band*. Recommendation ITU-R M.1371-0. Geneva: ITU.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Recommendation ITU-R M.1371-5. Geneva: ITU.
- International Telecommunication Union (2026). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Recommendation ITU-R M.1371-6. Geneva: ITU.
- Johnson, M. M., Lesch, A. (2009). *Multiple access communication system for moveable objects*. US Patent 7,512,095 B2. Assigned in part to Software Radio Technology plc. Washington, DC: USPTO.
- Lans, H. (1993). *Position indicating system and position station for a position indicating system*. Swedish Patent SE 468,452 B. Stockholm: PRV.
- Lans, H. (1996). *Position indicating system*. US Patent 5,506,587 A. Assigned to GP & C Systems International AB. Washington, DC: USPTO.
- Lans, H. (1997). *Position indicating system*. European Patent EP 0 592 560 B1. Munich: EPO.
- National Transportation Safety Board (1990). *Grounding of the U.S. Tankship EXXON VALDEZ on Bligh Reef, Prince William Sound, near Valdez, Alaska, March 24, 1989*. Marine Accident Report NTSB/MAR-90/04. Washington, DC: NTSB.
- Swedish Maritime Administration (2018). *AIS — How a Swedish innovation became a global standard*. Texts by T. Gardebring, R. Zetterberg, and U. Svedberg. Norrköping: Sjöfartsverket. URL: https://www.sjofartsverket.se/globalassets/framtidens-sjofart/foi/ais_eng.pdf
