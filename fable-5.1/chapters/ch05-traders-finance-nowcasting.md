# Chapter 5 — Commodity traders, finance, and economic nowcasting

> **Part I — Why AIS? Uses and users.** How a navigational safety broadcast was co-opted by commodity trading desks, quantitative hedge funds, and international financial institutions to monitor floating energy inventories, predict physical supply-chain bottlenecks, and nowcast macroeconomic growth in real time.

**In this chapter.** You will learn how raw maritime VHF and satellite broadcasts are transformed into actionable financial market intelligence and macroeconomic nowcasting models. We dissect the technical mechanisms by which commodity traders extract physical cargo flows: translating static draught reports from Message 5 into displacement tons, detecting offshore floating storage from kinematic drifting patterns, and parsing unstandardized destination strings into geographic terminal nodes. You will trace how financial analytics providers—from Bloomberg and Kpler to Vortexa and S&P Global—integrate satellite telemetry with vessel registries and cargo manifests. We inspect the Bloomberg Terminal interface, contrasting its high-level analytical workflows (`BMAP`, `ECTR`, `GLCO`) documented in student curricula with the underlying engineering constraints of the AIS protocol. Furthermore, you will examine institutional nowcasting frameworks developed by the International Monetary Fund (such as PortWatch) and the United Nations to measure seaborne trade shocks, evaluate statistical corrections for bridge misreporting, and model the financial impact of illicit spoofing in sanctioned commodity trades.

## 5.1 From collision avoidance to alternative data

The primary purpose of the Automatic Identification System (**AIS**), as mandated in Chapter V of the International Convention for the Safety of Life at Sea (**SOLAS**), is the safety of life at sea, collision avoidance, and coastal Vessel Traffic Services (**VTS**) tracking ([Chapter 1](ch01-what-ais-is.md); [Chapter 4](ch04-vts-and-ports.md)). Nothing in the regulatory architecture crafted under IMO Resolution MSC.74(69) (IMO 1998) or ITU-R M.1371 (ITU-R M.1371-5 2014) was designed for macroeconomic surveillance or financial arbitrage.

Yet by the mid-2010s, AIS had become one of the most lucrative streams in the multibillion-dollar "alternative data" ecosystem. In quantitative finance, **alternative data** refers to non-traditional market signals—such as satellite imagery, credit-card transactions, mobile-app telemetry, and radio broadcasts—ingested to forecast asset prices, commodity supply shifts, and corporate earnings ahead of official reporting.

Global trade is fundamentally maritime: by volume, more than 80 percent of world merchandise trade moves across the oceans on merchant hulls. Historically, commodity traders, shipbrokers, and macro economists tracked these volumes through delayed customs declarations, port authority reports, national statistical releases, and informal dockside intelligence networks. Official merchandise statistics, such as monthly census trade reports from the US Census Bureau or Eurostat, typically suffer from a publication lag of 30 to 90 days. For an energy trader pricing Brent or West Texas Intermediate (**WTI**) futures, or an agricultural desk trading Chicago Board of Trade (**CBOT**) soybeans, waiting two months to confirm physical export volumes represents unacceptable market exposure.

The expansion of Low Earth Orbit (**LEO**) satellite AIS constellations in the late 2000s and 2010s (Høye et al. 2008; [Chapter 39](ch39-satellite-ais.md)) closed this information gap. By combining high-frequency dynamic position reports (Messages 1, 2, 3, 18, and 19) with voyage-related static metadata (Message 5 and Message 24), computational financial pipelines began tracking the global commercial fleet in near real time. What was broadcast across maritime VHF as an unencrypted, unauthenticated beacon became a continuous planetary scanner for physical bulk commerce.

## 5.2 Tanker tracking and floating storage

The energy sector—specifically crude oil, refined petroleum products, and Liquefied Natural Gas (**LNG**)—was the first financial domain to commercialize AIS telemetry. Crude oil is traded on paper futures exchanges (such as ICE and NYMEX) in volumes that dwarf physical production, but the physical marginal barrel ultimately dictates the clearing price.

### 5.2.1 Detecting floating storage
In energy economics, **floating storage** occurs when crude oil or refined product tankers remain stationary or drift in open water, holding inventory rather than immediately discharging at a refinery terminal. Floating storage arises under two distinct market conditions:
1. **Logistical friction:** Discharge port congestion, refinery outages, or pipeline bottlenecks force tankers to wait at anchorage before berthing.
2. **Economic contango:** When futures markets trade in severe **contango**—a price curve structure where future delivery prices exceed immediate spot prices ($P_{\text{future}} > P_{\text{spot}}$)—traders can execute a cash-and-carry arbitrage. If the price spread exceeds the time-charter rate of a Very Large Crude Carrier (**VLCC**), insurance, and financing costs, market participants charter tankers as floating storage tanks:

$$\text{Profit} = P_{\text{future}} - P_{\text{spot}} - (R_{\text{charter}} \times T) - C_{\text{bunker}} - C_{\text{insurance}}$$

where $R_{\text{charter}}$ is the daily vessel charter rate, $T$ is the holding duration in days, $C_{\text{bunker}}$ represents hoteling bunker costs, and $C_{\text{insurance}}$ is maritime cargo insurance.

Detecting floating storage via AIS requires algorithmic classification of kinematic and geospatial behavior. Tankers engaged in floating storage do not dock at terminals or standard harbor anchorages; they loiter in designated deepwater staging zones (such as off Singapore, Fujairah, the US Gulf Coast, or Rotterdam) for weeks or months (Adland, Cariou & Wolff 2020).

```
   Raw AIS Positions (LEO + Terrestrial)
                    │
                    ▼
   ┌───────────────────────────────────┐
   │ Kinematic Spatial Filtering       │
   │ Speed Over Ground: SOG < 1.0 kn   │
   │ Geographic Bounding Box Check     │
   └───────────────────────────────────┘
                    │
                    ▼
   ┌───────────────────────────────────┐
   │ Temporal Persistence Filter       │
   │ Duration > 14 consecutive days    │
   │ Navigation Status: 1, 3, or 5     │
   └───────────────────────────────────┘
                    │
                    ▼
   ┌───────────────────────────────────┐
   │ Hydrostatic Cargo Verification    │
   │ Message 5 Static Draught: d_t     │
   │ d_t >= 0.85 * d_max (Laden)       │
   └───────────────────────────────────┘
                    │
                    ▼
   Confirmed Floating Storage Volume
   Inventory (Barrels) = DWT * F_cargo * 7.33
```

Analytics engines apply a three-stage filter:
- **Kinematic spatial filter:** The vessel's Speed Over Ground (**SOG**) must remain below a drift threshold (typically $\text{SOG} \le 1.0\text{ kn}$) outside sheltered harbour limits.
- **Temporal persistence:** The low-speed behavior must persist beyond operational anchorage delays, conventionally defined as 14 to 21 consecutive days in an open-water staging area.
- **Hydrostatic validation:** The vessel's reported static draught ($d_t$) from Message 5 must exceed a laden threshold (typically $d_t \ge 0.85 \times d_{\text{max}}$), proving that the ship is not idling in ballast while waiting for an employment contract.

> **Definitions that bite.**
> **Deadweight Tonnage (DWT) vs. Gross Tonnage (GT).** Analysts unfamiliar with naval architecture frequently confuse these metrics. **Gross Tonnage** is a non-linear dimensionless volumetric measure of the vessel's internal enclosed spaces ($\approx 100\text{ ft}^3$ or $2.83\text{ m}^3$ per historic register ton), used by port authorities for pilotage and harbour dues. **Deadweight Tonnage** is a true physical mass measurement in metric tons (1,000 kg), representing the maximum allowable weight a vessel can carry—comprising cargo, fuel, ballast water, fresh water, and provisions—without submerging its Plimsoll load-line mark. Estimating cargo volume by multiplying GT by crude density generates nonsense; all displacement and cargo models must operate strictly on DWT.

### 5.2.2 Draught as a real-time cargo proxy
Under ITU-R M.1371-5, Annex 8, Class A transponders broadcast Message 5 every 6 minutes, or whenever static voyage parameters are altered on the Minimum Keyboard and Display (**MKD**). Bits 294–301 encode the "maximum present static draught" in tenths of a meter, spanning 0.1 m to 25.5 m (a value of 0 indicates "not available").

In physical commodity tracking, draught is the vital link between vessel movement and physical cargo weight. A ship's total displacement $\Delta$ (the total weight of water displaced by the hull, measured in metric tons) is a direct hydrostatic function of its draught $d$ and hull geometry:

$$\Delta(d) = \rho_{\text{water}} \times \nabla(d) = \rho_{\text{water}} \times L_{\text{pp}} \times B \times d \times C_b(d)$$

where $\rho_{\text{water}}$ is seawater density ($\approx 1.025\text{ t/m}^3$), $L_{\text{pp}}$ is length between perpendiculars, $B$ is beam width, and $C_b(d)$ is the block coefficient of the underwater hull at draught $d$.

For a standard commercial hull, the relationship between draught change and deadweight payload can be linearly approximated across the operational draught range between lightweight ballast ($d_{\text{ballast}}$) and fully laden summer draught ($d_{\text{design}}$):

$$\text{Payload}(d_t) \approx \text{DWT} \times \left( \frac{d_t - d_{\text{ballast}}}{d_{\text{design}} - d_{\text{ballast}}} \right)$$

When static draught increases following a port call at an export terminal (such as Ras Tanura or Corpus Christi), trading algorithms infer a cargo loading event. When the vessel arrives at an import terminal (such as Ningbo or Rotterdam) and the draught drops back to ballast levels ($d_t \approx d_{\text{ballast}}$), the model registers a physical discharge event.

> **Worked example.**
> **Estimating crude cargo volume from a VLCC static draught update.**
> A Very Large Crude Carrier (**VLCC**) with an IMO number confirmed in IHS Markit registries has a summer design deadweight of $300{,}000\text{ DWT}$, a maximum summer draught of $d_{\text{design}} = 22.0\text{ m}$, and an operational clean ballast draught of $d_{\text{ballast}} = 9.5\text{ m}$.
> 
> The vessel docks at Ju'aymah Offshore Terminal in Saudi Arabia. Before mooring, its Message 5 broadcast reports a static draught of $9.6\text{ m}$. Forty-eight hours later, the vessel unmoors and accelerates into the Persian Gulf, broadcasting a new static draught of $d_t = 21.8\text{ m}$.
> 
> We compute the estimated onboard cargo payload:
> 
> $$\text{Utilization} = \frac{d_t - d_{\text{ballast}}}{d_{\text{design}} - d_{\text{ballast}}} = \frac{21.8 - 9.5}{22.0 - 9.5} = \frac{12.3}{12.5} = 0.984\text{ (98.4\%)}$$
> 
> $$\text{Payload}_{\text{metric tons}} = 300{,}000 \times 0.984 = 295{,}200\text{ MT}$$
> 
> Crude oil volume is conventionally denominated in 42-gallon barrels. Assuming standard Arab Light crude with an API gravity of $33^\circ$ (density $\rho \approx 0.860\text{ t/m}^3$), one metric ton yields approximately 7.33 barrels:
> 
> $$\text{Crude Volume} \approx 295{,}200\text{ MT} \times 7.33\text{ bbl/MT} \approx 2{,}163{,}816\text{ barrels}$$
> 
> By capturing this Message 5 broadcast as the tanker enters the Strait of Hormuz, an energy trading desk prices the departure of $2.16\text{ million barrels}$ of crude 14 to 30 days before that oil discharges into an Asian refinery.

## 5.3 Dry bulk, LNG, and containerized freight

While crude oil pioneered maritime telemetry finance, the same computational techniques govern dry bulk, liquefied gas, and manufactured goods logistics.

### 5.3.1 Dry bulk: iron ore, coal, and grain
Dry bulk shipping comprises capesize ($100{,}000\text{--}400{,}000\text{ DWT}$), panamax ($65{,}000\text{--}99{,}000\text{ DWT}$), and supramax/handysize ($10{,}000\text{--}64{,}000\text{ DWT}$) bulkers. Unlike crude tankers, which load and discharge liquid cargo via sealed manifold connections over 24 to 36 hours, dry bulkers exhibit distinct operational patterns:
- **Iron ore:** Capesize vessels loading at Port Hedland (Australia) or Ponta da Madeira (Brazil) deliver raw ore to Chinese steel mills. Monitoring waiting queues outside Tubarão or Dampier provides a direct physical nowcast of global steel manufacturing demand.
- **Grain flows and export seasonality:** Panamax bulkers loading soybeans in the Brazilian ports of Santos and Paranaguá, or grain across the US Gulf (Mississippi River terminals), display extreme seasonal surges. Delays at grain elevators appear immediately in AIS as sprawling anchorage clusters.
- **Hold cleaning and ballast transits:** Bulkers transitioning between dirty cargoes (coal) and food-grade cargoes (wheat) require extensive hold washing, visible as slow steaming or holding patterns in equatorial waters.

### 5.3.2 Liquefied Natural Gas (LNG)
LNG carriers are specialized, capital-intensive vessels operating under cryogenic containment ($-162^\circ\text{C}$). Tracking LNG movements via AIS differs fundamentally from crude or dry bulk tracking:
- **Boil-Off Gas (BOG):** LNG cannot be held indefinitely. Ambient heat causes cargo to vaporize at a rate of 0.10 to 0.15 percent of total volume per day. Modern LNG carriers burn this boil-off gas in dual-fuel propulsion engines or run reliquefaction plants. Idling an LNG carrier in floating storage incurs severe continuous cargo loss.
- **Cargo diversion arbitrage:** Because LNG pricing exhibits wide regional disparities between the European Title Transfer Facility (**TTF**), the US Henry Hub, and the Asian Japan Korea Marker (**JKM**), charterers frequently redirect laden LNG tankers mid-voyage. A sudden shift in AIS Course Over Ground and a modified destination string (e.g., from `SUEZ FOR ORDERS` to `ROTERDAM`) signals a cross-basin commercial diversion triggered by regional price spread differentials.

### 5.3.3 Containerized freight and supply chain velocity
Unlike bulkers and tankers that operate on tramp charters (point-to-point spot voyages), container ships operate on fixed liner schedules. Containerized AIS tracking focuses on:
- **Port turnaround and berth waiting times:** Tracking the exact interval between a container vessel entering port limits, dropping anchor, shifting to berth, and clearing the harbor channel.
- **Supply chain congestion indices:** During the 2021–2022 global supply chain disruption, quantitative funds tracked the count of container ships anchored in San Pedro Bay outside the ports of Los Angeles and Long Beach. The aggregate container capacity idle at anchor served as an empirical predictor of US consumer price inflation and retail inventory shortfalls.

## 5.4 The terminal desk: Bloomberg, Kpler, and analytics providers

To understand how financial institutions consume AIS data, one must distinguish between the physical transponder broadcast, the specialized maritime aggregators, and the multi-asset execution terminals used on trading desks.

### 5.4.1 The data pipeline: from radio bursts to commercial analytics
The raw AIS stream is unsuited for immediate consumption by an equity portfolio manager or commodity trader. A raw `!AIVDM` sentence contains bit-encoded integers requiring decoding, deduplication, geometric validation, and entity resolution ([Chapter 44](ch44-open-source-decoders-history.md); [Chapter 47](ch47-data-quality-track-reconstruction.md)).

Commercial maritime intelligence firms (such as Kpler, Vortexa, ClipperData, Windward, Lloyd's List Intelligence, S&P Global Maritime, Signal Ocean, and VesselsValue) sit between raw data collectors and financial end-users. These firms ingest multi-source AIS feeds (terrestrial and satellite), fuse them with commercial datasets (customs bills of lading, port agent line-ups, charter fixtures, and satellite optical/SAR imagery), and output structured commodity flow tables:
- **Port-call parsing:** Converting raw latitude/longitude points into structured events: arrival, anchorage waiting time, pilot boarding, berth all-fast, loading/unloading duration, and departure.
- **Cargo grading:** Inferring whether a crude tanker loaded Urals, Arab Medium, or WTI based on export terminal berth identity, draught change, and historical charter intelligence.
- **Bilateral trade matrices:** Calculating real-time import and export matrices across countries, commodities, and vessel classes.

### 5.4.2 The Bloomberg Terminal as a teaching artifact
For hundreds of thousands of financial professionals, the primary gateway to market data is the **Bloomberg Terminal**, a closed financial software network operated by Bloomberg L.P. The architecture of the Bloomberg Terminal reflects its financial heritage: users navigate using four-letter mnemonic commands followed by the `<GO>` (Enter) key.

A widely circulated introductory document, the *Training Booklet* produced by the Alperin Financial Center at the University of Scranton's Kania School of Management (Scranton 2016), provides a revealing window into how finance students and junior analysts are introduced to Bloomberg's commodities interface. The Scranton manual documents core commodity functions:
- `GLCO <GO>`: Global commodity prices across energy, precious metals, agriculture, and industrial metals.
- `DES <GO>`: Security and contract description, detailing futures specifications such as WTI Light Sweet Crude Oil (`CL1 <Cmdty>`).
- `ECTR <GO>`: Interactive global trade-flow maps, depicting trade volumes and bilateral import/export balances by country.
- `SPLC <GO>`: Comprehensive supply-chain analysis, mapping supplier-customer dependencies for publicly traded corporations.

On page 59 of the manual, the curriculum introduces Bloomberg's geospatial mapping engine:
```
Bloomberg Maps — BMAP <Go> is a global mapping function that enables
the user to search for Oil and Gas Rigs, Pipelines, Weather related
events, mines etc. The following is a map of the natural gas pipelines
within the United States. It also includes a map of the Shale regions
in the United States.
```

The Scranton booklet documents `BMAP <GO>` purely as an energy-infrastructure visualization tool for pipelines, shale plays, and weather risks. It makes no mention of ship tracking, tankers, draught, or AIS. This absence illustrates an important operational reality: basic financial curricula teach geospatial maps as static infrastructure layers.

On advanced institutional trading desks, however, `BMAP <GO>` integrates commercial AIS vessel layers. On Bloomberg, commodity analysts track vessel movements alongside oil refinery outages, liquefied gas pipelines, and offshore production platforms. Furthermore, functions such as `AHOY <GO>` have provided specialized tanker-tracking and trade-flow analytics for petroleum markets.

In October 2019, Bloomberg expanded its maritime mapping capabilities by partnering with Global Fishing Watch (**GFW**). Under this initiative, Bloomberg Philanthropies and GFW integrated commercial fishing vessel activity tracking directly into the Terminal (GFW 2019). Accessed via the interactive map layer `{MAP FISH <GO>}`, this function allowed Terminal subscribers to evaluate industrial fishing effort, monitor compliance across marine protected areas, and screen maritime supply chains for environmental, social, and governance (**ESG**) investment risk. The press release described AIS to financial users in characteristic lay terms as "a GPS-like device that large ships use to broadcast their position in order to avoid collisions"—a simplification that masks the protocol's underlying radio broadcast architecture.

## 5.5 Macroeconomic nowcasting: from IMF PortWatch to central banks

Beyond private arbitrage on trading floors, AIS has transformed macroeconomic monitoring at central banks, multilateral development lenders, and national statistical agencies.

### 5.5.1 The nowcasting paradigm
In macroeconomics, **nowcasting** is the prediction of the very recent past, present, or near future state of an economic variable before official statistical agencies publish census data. Gross Domestic Product (**GDP**) and international trade balances are traditionally reported quarterly or monthly, with severe publication lags. During economic shocks—such as the 2008 financial crisis, the 2020 COVID-19 pandemic, or sudden geopolitical conflict—policymakers cannot wait months to measure economic contractions.

In December 2019, researchers at the International Monetary Fund published an econometric framework demonstrating that real-time AIS vessel tracking could nowcast official trade statistics with high statistical accuracy (Arslanalp, Marini & Tumbarello 2019). The authors analyzed maritime traffic in Pacific island economies and major global ports, proving that vessel arrival frequencies and deadweight-adjusted transit volumes correlated strongly with subsequent customs-cleared trade statistics.

Building on this proof of concept, Cerdeiro et al. (2020) constructed a global, real-time nowcast of world seaborne trade entirely from scratch using raw satellite AIS streams. The authors established automated tracking of over 100,000 commercial vessels across thousands of international ports, establishing:
1. Spatial port boundary polygons for every commercial maritime terminal on Earth.
2. Automated detection of port calls, measuring dwell time and berth shifts.
3. Voyage-level payload estimation utilizing static draught deltas ($\Delta d = d_{\text{arrival}} - d_{\text{departure}}$) linked to vessel DWT.

$$\Delta \text{Trade}_{\text{nowcast}}(t) = \sum_{i \in \text{Vessels}} \text{DWT}_i \times \Phi(\Delta d_{i,t}) \times \mathbf{P}_{\text{commodity}}(t)$$

where $\Phi(\Delta d_{i,t})$ represents the hydrostatic loading function, and $\mathbf{P}_{\text{commodity}}(t)$ deflates physical tonnage into monetary customs value.

### 5.5.2 The COVID-19 shipping shock and high-frequency trade indicators
The operational value of AIS nowcasting was tested during the outbreak of COVID-19 in early 2020. As national governments imposed lockdowns, factory closures, and quarantine restrictions, conventional economic data went blind.

Verschuur, Koks & Hall (2021) utilized empirical AIS vessel tracking across 1,123 global ports to construct a high-frequency daily indicator of global trade disruption. Their analysis revealed that global maritime trade contracted by 7.0 to 9.6 percent in the first eight months of 2020, equivalent to an unprecedented loss of 225 to 412 million metric tons of cargo. The AIS data captured the asymmetric nature of the shock: manufacturing exports collapsed first in East Asia, followed by sharp demand contractions in North America and Western Europe, and subsequent primary commodity export slumps in South America and Africa.

The success of these models led the IMF and the Environmental Change Institute at the University of Oxford to launch **PortWatch** (IMF 2023). PortWatch is an open platform monitoring international maritime trade, port activity, and supply-chain chokepoints in real time. Ingesting raw satellite AIS feeds distributed through the United Nations Global Platform (**UNGP**), PortWatch tracks physical shipment volumes across critical maritime bottlenecks—including the Suez Canal, the Panama Canal, the Strait of Malacca, the Bab el-Mandeb, and the Strait of Hormuz. When drought restricted daily vessel transits through the Panama Canal in 2023, or when Houthi missile and drone strikes forced commercial shipping away from the Red Sea and around the Cape of Good Hope in 2024, PortWatch provided immediate daily tonnage nowcasts of diverted trade flows to central banks worldwide.

## 5.6 Evasion, dark fleets, and sanctions risk

While AIS provides unprecedented transparency into global commerce, financial institutions face acute legal and regulatory hazards when transponder data is intentionally manipulated.

### 5.6.1 The regulatory mandate: the OFAC May 2020 Advisory
On May 14, 2020, the US Department of the Treasury's Office of Foreign Assets Control (**OFAC**), alongside the US Department of State and the US Coast Guard, issued a landmark global advisory titled *Sanctions Advisory for the Maritime Industry, Energy and Metals Sectors, and Related Communities* (OFAC 2020).

The advisory placed the global maritime finance sector—including commodity traders, ship charterers, marine insurers (P&I Clubs), flag registries, and trade-finance banks—on notice that they must monitor AIS signals to detect illicit trade evasion. OFAC identified seven deceptive shipping practices designed to evade US, UN, and European economic sanctions targeting Iran, North Korea, Venezuela, and later the Russian Federation:
1. **Disabling AIS:** Intentionally switching off transponders ("going dark") in violation of SOLAS Chapter V, Regulation 19, while conducting illicit loading or discharge operations.
2. **Manipulating AIS data:** Transmitting altered vessel names, falsified IMO numbers, bogus MMSIs, or manipulated static voyage data.
3. **GNSS position spoofing:** Broadcasting coherent, fabricated position reports to simulate legitimate transit across open water while the vessel is physically berthed at an embargoed export terminal.
4. **Ship-to-Ship (STS) cargo transfers:** Conducting off-record mid-sea crude or petroleum transfers in remote offshore zones outside coastal radar coverage to obscure cargo origin.
5. **False flags and flag hopping:** Repeatedly switching maritime flag registries or broadcasting false flag allocations.
6. **Physical hull alterations:** Painting over vessel names and IMO numbers to prevent optical identification.
7. **Document falsification:** Forging bills of lading, certificates of origin, and bunker receipts to claim non-sanctioned origins.

Under strict-liability sanctions regimes enforced by OFAC, financial institutions can incur multimillion-dollar civil penalties if they finance, insure, or trade a cargo transferred during an unmonitored AIS dark event or spoofing incident.

> **Threat model.**
> **Sanctions evasion via coordinated AIS manipulation and STS transfers.**
> - **Threat Actor:** State-sponsored petroleum exporters, rogue tanker operators, and illicit trading syndicates seeking to evade international crude oil embargoes.
> - **Capability:** Low-cost marine VHF transponders, programmable software-defined radios (SDRs), GPS spoofing hardware, and offshore ship-to-ship transfer apparatus.
> - **Attack Vector:** An illicit crude tanker enters a designated STS transfer zone (e.g., off the coast of Fujairah, Tanjung Pelepas, or Greece). The vessel disables its operational Class A transponder or injects a false position trajectory broadcasting a slow drift hundreds of miles away. Simultaneously, a shadow-fleet partner vessel conducts a ship-to-ship crude transfer under darkness. The receiving vessel updates its Message 5 static draught to reflect a fully laden cargo while claiming the crude originated from a legitimate regional producer.
> - **Financial Impact:** Commodity trading desks and financing banks unwittingly clear letters of credit and provide cargo insurance for sanctioned crude, exposing institutions to severe regulatory enforcement, asset seizures, and secondary sanctions bans.
> - **Mitigation:** Multilateral data fusion. Automated screening engines must cross-reference AIS tracks with synthetic aperture radar (**SAR**) satellite constellations (such as Sentinel-1), optical satellite passes, RF direction finding, and port customs agent line-ups. Any discrepancy between reported draught changes and observed berth events triggers an immediate compliance hold.

> **Legal note.**
> **Strict liability in maritime trade finance.**
> Under US Department of the Treasury regulations governing maritime sanctions, OFAC enforces a standard of **strict liability**. A commercial bank providing trade finance or a marine insurer underwriting hull and machinery coverage can be held legally and financially liable for sanctions violations even if the entity had no actual knowledge that the vessel engaged in deceptive shipping practices or AIS manipulation. Compliance programs cannot rely solely on basic ship-tracking maps; they must implement audit-ready, documented screening procedures capable of detecting AIS gaps, loitering anomalies, and illicit ship-to-ship transfers.

## Then & now

- **Pre-2000 ⟨H⟩:** Commodity flow monitoring relied entirely on manual dockside intelligence, weekly printed shipbroker fixtures, physical port agent line-ups, and customs declarations published weeks or months after cargo discharge.
- **2002–2004 ⟨H⟩:** The IMO SOLAS Chapter V mandate phased in Class A transponders for international merchant ships $\ge 300\text{ GT}$. Early AIS tracking was confined to local VHF line-of-sight shore stations operated by coastal VTS and port authorities.
- **2008 ⟨+⟩:** The launch of demonstration and commercial satellite AIS receivers (such as NTS/EV-0 and subsequent commercial constellations; Høye et al. 2008) broke the coastal horizon, enabling continuous open-ocean tracking of commercial tankers and bulkers.
- **2010–2015 ⟨+⟩:** Financial data firms (ClipperData, Genscape, Kpler) deployed proprietary terrestrial receiver networks around major oil export hubs (Strait of Hormuz, Singapore, Houston Ship Channel) to supply high-frequency crude export estimates to trading floors.
- **2016 ⟨+⟩:** Student finance curricula at institutions such as the University of Scranton documented the Bloomberg Terminal's geospatial mapping interface (`BMAP`) as an energy infrastructure map for pipelines, wells, and weather events (Scranton 2016).
- **2019 ⟨+⟩:** Bloomberg Philanthropies and Global Fishing Watch integrated commercial fishing vessel activity tracking directly into the Bloomberg Terminal via `{MAP FISH <GO>}` to support ESG risk evaluation (GFW 2019). Simultaneously, IMF economists established empirical methodologies nowcasting national trade statistics from AIS data (Arslanalp, Marini & Tumbarello 2019).
- **2020 ⟨+⟩:** The COVID-19 pandemic induced severe economic blindness; academic researchers and the IMF deployed AIS port tracking to calculate real-time trade contractions and container backlogs (Verschuur, Koks & Hall 2021). OFAC published its landmark maritime sanctions advisory, establishing AIS monitoring as a mandatory compliance duty for trade finance (OFAC 2020).
- **2023–2025 ⟨+⟩:** The IMF and Oxford University deployed PortWatch, tracking global trade shocks and canal transit disruptions in real time. Kpler consolidated the commercial maritime tracking space through major acquisitions, including MarineTraffic, FleetMon, and Spire Maritime.

## On the wire

Class A commercial merchant vessels broadcast static and voyage-related data using **Message 5**, a two-slot ITU-R M.1371 transmission comprising 424 bits of payload. In commodity trading and trade nowcasting, Message 5 is the sole protocol-level source for vessel dimensions, cargo draught, destination, and estimated time of arrival.

```
Message 5: Static and Voyage Related Data (424 bits total, 2 slots)
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Type  |Rep|      MMSI         |AIS|   IMO Number  |  Callsign |
| (6b)  |(2)|     (30b)         |(2)|      (30b)    |   (42b)   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       Vessel Name (120 bits, 20 six-bit ASCII chars)          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Type of Ship|   Dimension to Bow, Stern, Port, Starboard       |
|   (8b)     |      A(9b)     |    B(9b)    | C(6b) |  D(6b)    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|EPFS|   ETA Month/Day/Hour/Minute      | Draught | Destination |
|(4b)| (4b) | (5b) | (5b) |   (6b)      |  (8b)   |  (120 bits) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|DTE|Spare|
|(1)|(1b) |
+-+-+-+-+-+
```

### Bit-level layout of key financial fields

1. **IMO Number (Bits 40–69, 30 bits):**
   - Encodes the vessel's unique seven-digit International Maritime Organization identification number.
   - Unlike the 30-bit MMSI (Bits 8–37), which changes when a vessel switches flag states, the IMO number remains permanently attached to the hull throughout its operational life. Trading desks use the IMO number as the primary join key against commercial registries (IHS Markit, Lloyd's Register) to retrieve vessel deadweight tonnage, cargo cubic capacity, and ownership structure.
2. **Ship Type (Bits 232–239, 8 bits):**
   - Identifies vessel category per ITU-R M.1371-5 Table 48.
   - Values `80` to `89` denote Tankers; `70` to `79` denote Cargo ships (bulk carriers, container vessels); `60` to `69` denote Passenger ships. Commodity flow algorithms filter incoming feeds strictly by ship type before executing trade nowcasts.
3. **Maximum Present Static Draught (Bits 294–301, 8 bits):**
   - Encodes vessel draught in units of $0.1\text{ m}$ (range $0.1\text{ to }25.5\text{ m}$).
   - Binary value `00000000` indicates draught not available.
   - Binary value `01001110` ($78_{10}$) represents $7.8\text{ m}$.
   - Binary value `11011010` ($218_{10}$) represents $21.8\text{ m}$.
4. **Estimated Time of Arrival (Bits 274–293, 20 bits):**
   - Subfields: Month (4 bits, 1–12), Day (5 bits, 1–31), Hour (5 bits, 0–23), Minute (6 bits, 0–59). Default sentinel for unavailable month is `0`, day `0`, hour `24`, minute `60`.
5. **Destination (Bits 302–421, 120 bits):**
   - Encodes 20 six-bit ASCII characters representing declared discharge port.
   - Free-form text entered manually by bridge officers via the MKD. Common examples include `ROTTERDAM`, `SPORE_BUNKER`, or `FOR_ORDERS`.

> **Try it.**
> **Extract draught and cargo status from a synthetic Message 5 payload.**
> The following Python snippet decodes the draught bits from a raw 424-bit Message 5 bitvector, evaluates vessel loading status, and computes estimated cargo payload. Run this script in the book's Python virtual environment:
> 
> ```python
> def decode_draught_and_cargo(bits_draught_int, dwt, d_ballast, d_design):
>     """
>     Decodes 8-bit AIS static draught and estimates crude cargo payload.
>     """
>     if bits_draught_int == 0:
>         return None, "Draught not reported"
>     
>     draught_m = bits_draught_int / 10.0
>     if draught_m <= d_ballast:
>         cargo_tons = 0.0
>         status = "Ballast (Empty)"
>     elif draught_m >= d_design:
>         cargo_tons = float(dwt)
>         status = "Fully Laden"
>     else:
>         fraction = (draught_m - d_ballast) / (d_design - d_ballast)
>         cargo_tons = round(dwt * fraction, 1)
>         status = f"Partially Laden ({fraction*100:.1f}%)"
>     
>     return draught_m, cargo_tons, status
> 
> # Example: Suezmax tanker (160,000 DWT, d_ballast=8.5m, d_design=17.0m)
> # Binary draught from Message 5: 0b10011110 (158 decimal -> 15.8 m)
> raw_draught_byte = 158
> d_m, payload, state = decode_draught_and_cargo(raw_draught_byte, 160000, 8.5, 17.0)
> print(f"Reported Draught: {d_m:.1f} m")
> print(f"Voyage Status:    {state}")
> print(f"Estimated Cargo:  {payload:,.1f} Metric Tons")
> ```
> 
> **Expected output:**
> ```text
> Reported Draught: 15.8 m
> Voyage Status:    Partially Laden (85.9%)
> Estimated Cargo:  137,411.8 Metric Tons
> ```

## Validation, uncertainty & data quality

Constructing reliable financial and macroeconomic nowcasts from AIS requires rigorous statistical remediation of systematic errors inherent in the protocol.

### Error taxonomy in trade tracking

1. **Human error in static voyage data:** Message 5 voyage parameters are updated manually by deck officers using the transponder's Minimum Keyboard and Display (**MKD**). Bridge crews frequently prioritize navigational watchstanding over updating administrative data fields (Harati-Mokhtari et al. 2007). In historical tracking studies, between 15 and 30 percent of active commercial vessels broadcast stale destinations or static draught values that remain unchanged after full cargo discharge.
2. **Free-form destination string ambiguity:** The 20-character destination field lacks mandatory structure. Deck officers input non-standard abbreviations, phonetic spellings, terminal berth numbers, or navigational waypoints (e.g., `ROT`, `R-DAM`, `EUROPOORT`, `NLDAM`, `FOR ORDERS`, `SUEZ CANAL`). Trade engines must parse these strings through fuzzy string-matching libraries (such as Levenshtein distance) trained on international UN/LOCODE dictionaries (e.g., mapping `R-DAM` to `NLRTM`).
3. **Satellite packet collision in trade chokepoints:** In dense shipping corridors—such as the Singapore Strait, the Strait of Malacca, the English Channel, and the Gulf of Guinea—thousands of Class A and Class B transmitters compete for TDMA slots ([Chapter 21](ch21-link-layer-tdma.md); [Chapter 30](ch30-network-loading-packet-loss.md)). A LEO satellite whose footprint covers a 5,000 km diameter circle captures thousands of overlapping radio bursts, causing widespread packet collisions. While position reports (Messages 1–3) have high transmission frequencies (every 2 to 10 seconds), two-slot Message 5 transmissions occur only every 6 minutes and suffer disproportionately higher packet loss rates. An analytical pipeline cannot assume that a lack of satellite reception implies a vessel has gone dark.
4. **Hydrostatic trim and seasonal water density variations:** Seawater density varies by temperature and salinity, from $\approx 1.000\text{ t/m}^3$ in the brackish Baltic Sea to $\approx 1.030\text{ t/m}^3$ in the Red Sea. A vessel's draught naturally varies by several inches when transitioning from open ocean to fresh-water river terminals (such as Antwerp or New Orleans) without loading a single pound of cargo. Furthermore, vessels are frequently trimmed by the stern (aft draught exceeding forward draught) to optimize propeller immersion. Message 5 encodes only maximum draught; failing to adjust for trim induces significant cargo calculation bias.

### Procedural validation and cleaning pipeline

To prevent corrupted inputs from poisoning trading algorithms, quantitative platforms implement a multi-stage validation pipeline:

```
Raw AIS Stream ──► [1. Kinematic Gate] ──► [2. Geofenced Port Call] ──► [3. Backpropagation]
                        │                          │                          │
                        ▼                          ▼                          ▼
                   Drop >40 kn               Assign Berth ID             Correct Stale
                   or Multi-path             Arrival/Departure           Draught from
                   Coordinates               Timestamps                  Subsequent Port
```

- **Step 1: Kinematic gating.** Ingested dynamic records are filtered to discard multi-path GPS jumps and impossible speeds:
  $$\text{SOG} \le 40\text{ kn}, \quad |\mathbf{a}| \le 2.0\text{ m/s}^2$$
- **Step 2: Geofenced port call extraction.** Vessels are mapped against global polygonal port boundaries (UN/LOCODE terminals). A valid port call requires:
  $$\mathbf{p}(t) \in \text{Polygon}_{\text{port}}, \quad \text{SOG} \le 1.0\text{ kn}, \quad \Delta t_{\text{dwell}} \ge 6\text{ hours}$$
- **Step 3: Draught backpropagation.** When a vessel departs an export terminal with an unchanged static draught, the algorithm suspends cargo attribution. Upon arrival at the subsequent discharge port, if the crew finally updates Message 5 to reflect a ballast draught, the engine executes **backpropagation**: it retroactively updates the previous voyage leg's loading volume using the post-arrival draught observation. IMF PortWatch and major commodity analytics platforms rely heavily on backpropagation to maintain statistical accuracy across global trade matrices (IMF 2023).

## Software

**Open source:**
- **MovingPandas** (v0.17+; movingpandas.org; BSD-2-Clause). Python trajectory analysis library built on GeoPandas and Shapely. Provides spatio-temporal stop detection, trajectory smoothing, and port dwell-time aggregation for AIS research. *Caveat:* In-memory processing architecture scales poorly to global, multi-billion-row commercial AIS datasets without Dask or Spark distributed backbones.
- **pyais** (v2.7+; GitHub; MIT License). Fast, pure-Python AIVDM/AIVDO message decoder supporting the full ITU-R M.1371 catalog, including 2-slot Message 5 parsing. *Caveat:* Decoding millions of raw NMEA sentences per second requires C++ implementations (such as `libais`) or Cython acceleration to avoid CPU bottlenecks.
- **DuckDB** (v1.0+; duckdb.org; MIT License). In-process analytical SQL database with native spatial extensions. Highly optimized for executing geospatial aggregations, spatial bounding-box joins, and time-series port-call statistics on multi-gigabyte Parquet AIS files on single workstations. *Caveat:* Lacks distributed multi-node clustering for live streaming ingest of global feeds.

**Free but closed:**
- **IMF PortWatch Portal** (portwatch.imf.org). Interactive web portal and API providing daily, weekly, and monthly nowcasts of maritime trade flows, port calls, and chokepoint transits based on satellite AIS data from the UN Global Platform. *Caveat:* Aggregated public data is subject to statistical revisions and cannot be queried for individual confidential vessel payloads.
- **Global Fishing Watch Map** (globalfishingwatch.org/map). Web-based tracking platform visualizing industrial fishing effort, transshipments, and vessel identities worldwide. *Caveat:* Focused primarily on fishing and commercial carriers involved in transshipments; does not provide bulk commodity cargo flow tables.

**Commercial:**
- **Bloomberg Terminal / BMAP** (Bloomberg L.P.). Premier institutional financial market terminal providing integrated multi-asset execution, news, analytics, and geospatial mapping (`BMAP`, `ECTR`, `GLCO`, `{MAP FISH}`). Integrates commercial AIS tracking alongside energy infrastructure and equity analysis. *Caveat:* High annual subscription cost per terminal ($>\$25{,}000/\text{year}$) and proprietary data access restrictions.
- **Kpler** (kpler.com). Market-leading real-time commodity data platform tracking crude oil, refined products, LNG, LPG, dry bulk, and maritime freight flows. Integrates global satellite AIS feeds with port agent lineups and customs data. *Caveat:* Expensive enterprise data licensing model; opaque proprietary cargo attribution heuristics.
- **Vortexa** (vortexa.com). Specialized energy and freight market analytics platform utilizing deep learning and satellite AIS to track waterborne crude, petroleum products, and gas inventories in real time. *Caveat:* Primarily focused on wet markets (crude/refined products/gas); limited coverage of containerized manufactured goods.

## Standards & guides

- **International Maritime Organization (IMO)** (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (Resolution MSC.74(69), Annex 3). Adopted 12 May 1998. London: IMO. Governs the fundamental operational standards and transmission performance requirements for shipborne Class A AIS.
- **International Maritime Organization (IMO)** (2000). *Adoption of Amendments to the International Convention for the Safety of Life at Sea, 1974, as Amended (SOLAS Chapter V)* (Resolution MSC.99(73)). Adopted 5 December 2000. London: IMO. Establishes the mandatory carriage requirements for AIS on all ships $\ge 300\text{ GT}$ on international voyages.
- **International Maritime Organization (IMO)** (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). Adopted 2 December 2015. London: IMO. Details bridge operational procedures for maintaining operational status, updating voyage data, and operating under master discretion.
- **International Telecommunication Union (ITU)** (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-5). Geneva: ITU-R. Defines the physical layer, TDMA link layer, and bit-level message formatting for Messages 1 through 27, including Message 5 static draught encoding.
- **US Department of the Treasury (OFAC), US Department of State, and US Coast Guard** (2020). *Sanctions Advisory for the Maritime Industry, Energy and Metals Sectors, and Related Communities*. Issued 14 May 2020. Washington, DC. Governs compliance standards, AIS monitoring expectations, and strict-liability obligations for financial institutions involved in maritime trade.

## Pitfalls

1. **Treating static draught from Message 5 as an automated digital sensor readout.** Bridge watchstanders must manually enter static draught into the transponder MKD. Many crews fail to update draught upon departure. Calculating inventory flows without verifying against port arrival/departure events or using backpropagation generates massive false cargo estimates.
2. **Confusing Gross Tonnage (GT) with Deadweight Tonnage (DWT).** Gross Tonnage measures enclosed internal vessel volume; Deadweight Tonnage measures actual carrying capacity by weight. Using GT in hydrostatic cargo equations produces erroneous physical tonnage estimates.
3. **Assuming lack of satellite AIS reception proves intentional transponder switch-off.** In dense maritime corridors, TDMA slot saturation causes severe packet collisions, dropping Message 5 decodes at LEO receivers. Attributing a satellite coverage gap in the Malacca Strait to illicit sanctions evasion creates severe legal and operational false positives.
4. **Ignoring seawater density and hydrostatic trim adjustments.** Seawater salinity varies across geographic trading basins, shifting vessel draught by several inches without cargo modification. Failing to apply salinity and trim corrections skews bulk trade nowcasts.
5. **Relying on literal string matching for Message 5 destination fields.** The 20-character destination field contains unstructured, abbreviated, or misspelled port names. Robust trade analytics pipelines must employ fuzzy string distance matching mapped against UN/LOCODE registries.
6. **Failing to account for vessel lightering and mid-sea Ship-to-Ship transfers.** Ultra-large crude carriers often cannot navigate shallow draft channels and transfer cargo to smaller daughter tankers offshore. Recording an export or import solely at a coastal dock misses significant lightering volumes.
7. **Neglecting boil-off gas in LNG cargo tracking.** LNG carriers burn cryogenic cargo boil-off gas during voyages. Assuming 100 percent cargo retention between export loading and import discharge overstates delivered gas volumes.
8. **Treating AIS as an all-inclusive record of international trade.** AIS captures only waterborne freight. It provides zero visibility into overland pipelines, rail freight, road trucking, or air cargo. Macroeconomic nowcasting models must explicitly fuse maritime flows with overland trade indicators.
9. **Failing to maintain a strict-liability sanctions compliance screening model.** Commodity trading and trade-finance desks that rely on basic web map displays without audit-ready screening for AIS gaps, spoofed trajectories, and anomalous loitering expose their institutions to severe regulatory enforcement under OFAC and European sanctions laws.

## Key takeaways

- AIS is a vital component of quantitative finance and macroeconomic nowcasting, providing real-time visibility into over 80 percent of physical global merchandise trade.
- Energy traders extract physical crude oil and refined product inventory shifts by algorithmically monitoring offshore floating storage, vessel speeds, and static draught changes.
- Hydrostatic cargo calculations map reported static draught (Message 5) to vessel deadweight tonnage (DWT) to estimate physical cargo weight, though data pipelines must account for salinity, trim, and ballast limits.
- Advanced trading terminals like the Bloomberg Terminal integrate commercial AIS vessel layers alongside traditional financial analytics (`BMAP`, `ECTR`, `GLCO`, `{MAP FISH}`).
- International institutions, including the IMF and the United Nations, utilize satellite AIS data to construct real-time trade nowcasts (such as IMF PortWatch), bypassing the 30-to-90-day reporting lag of official trade statistics.
- The COVID-19 pandemic and subsequent geopolitical crises demonstrated that high-frequency AIS shipping metrics can quantify supply-chain shocks and chokepoint disruptions in real time.
- Unstructured destination strings and human error in updating Message 5 require automated remediation pipelines, including fuzzy UN/LOCODE matching and draught backpropagation.
- Compliance with global maritime sanctions mandates that financial institutions, insurers, and commodity traders screen AIS feeds for deceptive practices, including transponder switch-offs, position spoofing, and illicit mid-sea ship-to-ship transfers.

## References

- Adland, R., Cariou, P. & Wolff, F.-C. (2020). When Do Vessels Drift? Economic and Environmental Drivers of Floating Storage in Tanker Shipping. *Transportation Research Part E: Logistics and Transportation Review*, 141:102043. doi:10.1016/j.tre.2020.102043.
- Arslanalp, S., Marini, M. & Tumbarello, P. (2019). *Big Data on Vessel Traffic: Nowcasting Trade Flows in Real Time* (IMF Working Paper WP/19/275). Washington, DC: International Monetary Fund.
- Cerdeiro, D. A., Komaromi, A., Liu, Y. & Saeed, M. (2020). *World Seaborne Trade in Real Time: A Proof of Concept for Building AIS-based Nowcasts from Scratch* (IMF Working Paper WP/20/57). Washington, DC: International Monetary Fund.
- Global Fishing Watch (2019). *Data on Global Fishing Activity and Ocean Ecosystems Now Available on Bloomberg Terminal*. Press release, Our Ocean 2019, Oslo (published 24 October 2019).
- Harati-Mokhtari, A., Wall, A., Brooks, P. & Wang, J. (2007). Automatic Identification System (AIS): Data Reliability and Human Error Implications. *The Journal of Navigation*, 60(3):373–389. doi:10.1017/S037346330700429X.
- Høye, G. K., Eriksen, T., Meland, B. J. & Narheim, B. (2008). Space-Based AIS for Global Maritime Surveillance. *Acta Astronautica*, 62(2–3):240–245. doi:10.1016/j.actaastro.2007.07.001.
- International Maritime Organization (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (Resolution MSC.74(69), Annex 3). Adopted 12 May 1998. London: IMO.
- International Maritime Organization (2000). *Adoption of Amendments to the International Convention for the Safety of Life at Sea, 1974, as Amended (SOLAS Chapter V)* (Resolution MSC.99(73)). Adopted 5 December 2000. London: IMO.
- International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). Adopted 2 December 2015. London: IMO.
- International Monetary Fund & University of Oxford Environmental Change Institute (2023). *PortWatch: Monitoring Global Maritime Trade and Disruptions from Space*. Methodology and portal documentation. Washington, DC: IMF. https://portwatch.imf.org.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-5). Geneva: ITU Radiocommunication Sector.
- University of Scranton, Kania School of Management, Alperin Financial Center (2016). *Training Booklet: Bloomberg Training Manual*. Author metadata Vince Rocco. Scranton, PA: University of Scranton.
- US Department of the Treasury, US Department of State & US Coast Guard (2020). *Sanctions Advisory for the Maritime Industry, Energy and Metals Sectors, and Related Communities*. Issued 14 May 2020. Washington, DC: Office of Foreign Assets Control.
- Verschuur, J., Koks, E. E. & Hall, J. W. (2021). Global Economic Impacts of COVID-19 Lockdown Measures Stand Out in High-Frequency Shipping Data. *PLOS ONE*, 16(4):e0248820. doi:10.1371/journal.pone.0248820.
