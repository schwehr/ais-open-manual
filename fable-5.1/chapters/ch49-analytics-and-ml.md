# Chapter 49 — Analytics and machine learning on AIS

> **Part VII — Decoding, software, and data engineering.** Extracting operational intelligence, detecting kinematic anomalies, predicting maritime logistics, and quantifying environmental impacts through statistical modeling and machine learning on global AIS data.

**In this chapter.** You will learn how to design, train, and evaluate machine-learning models and analytical pipelines operating on raw and reconstructed Automatic Identification System (**AIS**) telemetry. You will implement spatial-temporal anomaly detection to flag spoofing, deliberate transponder blackouts, and corridor deviations. You will construct destination and Estimated Time of Arrival (**ETA**) predictors using gradient-boosted trees and sequence-to-sequence neural networks while avoiding temporal data leakage. You will examine the convolutional neural network architectures that classified global industrial fishing effort and detect refrigerated cargo transshipments at sea. You will analyze how satellite Synthetic Aperture Radar (**SAR**) and optical imagery fuse with broadcast AIS to unmask the global dark fleet. You will quantify anthropogenic environmental impacts by calculating vessel emissions inventories with the Ship Traffic Emission Assessment Model (**STEAM**), mapping underwater radiated noise footprints, and computing cetacean collision lethality curves. Finally, you will implement mathematical Collision Risk Indices (**CRI**) and evaluate public benchmarking datasets against label noise, telemetry jitter, and spatial coverage bias.

## 49.1 The paradigm shift: from tactical collision avoidance to planetary analytics

The Automatic Identification System was conceived as an unauthenticated VHF broadcast protocol to prevent collisions between ships in visual or radar contact and to assist coastal Vessel Traffic Services (**VTS**) ([Chapter 01](ch01-what-ais-is.md), [Chapter 04](ch04-vts-and-ports.md), and [Chapter 20](ch20-architecture-and-station-classes.md)). Over three decades, the proliferation of terrestrial receiver exchanges ([Chapter 41](ch41-networks-and-providers.md)) and Low Earth Orbit (**LEO**) satellite constellations ([Chapter 39](ch39-satellite-ais.md)) transformed AIS from an ephemeral local radio link into a planetary-scale telemetry stream.

Modern ingest platforms capture tens of billions of AIS position messages annually ([Chapter 50](ch50-big-data-architecture.md)). Downstream consumers—including maritime authorities, commodity traders, environmental scientists, and security analysts—rely on automated statistical inference and machine learning (**ML**) to transform disconnected spatial-temporal coordinates into operational intelligence.

Machine learning on AIS operates across four primary areas:

1. **Behavior segmentation:** Inferring vessel operational states (cruising, towing, trawling, drifting, or transshipping) from kinematic features without onboard logs.
2. **Predictive forecasting:** Estimating future positions, transit corridors, destination ports, and berth-level ETAs to optimize supply chains and port dispatch ([Chapter 05](ch05-traders-finance-nowcasting.md)).
3. **Anomaly and deception detection:** Identifying deviations from navigational corridors, unphysical kinematics indicative of Global Navigation Satellite System (**GNSS**) spoofing, and deliberate transponder blackouts ([Chapter 58](ch58-threat-model.md) and [Chapter 59](ch59-spoofing.md)).
4. **Physical impact modeling:** Coupling kinematic tracks with hydrodynamic, acoustic, and meteorological models to compute greenhouse gas inventories, underwater noise budgets, and wildlife collision risks.

Extracting reliable signals from AIS requires overcoming severe structural impediments. As shown in [Chapter 47](ch47-data-quality-track-reconstruction.md) and [Chapter 48](ch48-spatial-statistics.md), AIS is an observational sample governed by link-layer contention, line-of-sight limits, satellite footprint collisions, and human configuration errors. Naive models inevitably learn receiver topology artifacts rather than genuine maritime behaviors. Feature engineering, temporal cross-validation, and multi-sensor fusion are essential prerequisites.

## 49.2 Trajectory feature engineering and kinematic state extraction

Raw AIS broadcasts arrive as discrete messages containing static identifiers (Message 5 and 24) or kinematic snapshots (Messages 1, 2, 3, 18, and 19) ([Chapter 22](ch22-message-catalog.md)). Applying machine learning requires transforming raw point observations into structured trajectory vectors or spatial graph representations.

```
+-----------------------------------------------------------------------------+
|                     AIS FEATURE EXTRACTION PIPELINE                         |
+-----------------------------------------------------------------------------+
|  [ LAYER 1: Raw Dynamic & Static Telemetry ]                                |
|    - MMSI, Timestamp (t), Lat (phi), Lon (lambda), SOG (u), COG (theta)     |
|    - Vessel Type, Length, Beam, Static Draught (Message 5)                  |
|                                                                             |
|  [ LAYER 2: Kinematic Derivative Extraction ]                               |
|    - Great-circle distance: Delta_s = 2R * arcsin(...)                      |
|    - Time step: Delta_t = t_i - t_{i-1}                                     |
|    - Rate of Turn (ROT): d(theta)/dt; Acceleration: a = d(u)/dt             |
|    - Spatial Curvature: kappa = |d(theta)/ds| = |ROT / SOG|                 |
|                                                                             |
|  [ LAYER 3: Contextual & Environmental Covariates ]                          |
|    - Bathymetric depth from GEBCO (z); Distance to coastline / port (d_c)   |
|    - Metocean currents (u_curr, v_curr) and wave height (H_s) from ERA5     |
|    - Spatial discrete global grid cell (Uber H3 index, aperture 7-9)        |
+-----------------------------------------------------------------------------+
```

### 49.2.1 Kinematic derivatives

Let a vessel trajectory $\mathcal{T}$ be an ordered sequence of $N$ observations:
$$\mathcal{T} = \left\{ (\phi_i, \lambda_i, t_i, u_i, \theta_i) \right\}_{i=1}^N$$
where $\phi_i$ is latitude, $\lambda_i$ is longitude, $t_i$ is UTC timestamp, $u_i$ is Speed Over Ground (**SOG**) in knots, and $\theta_i$ is Course Over Ground (**COG**) in degrees clockwise from true north.

Between successive observations $i-1$ and $i$, with time elapsed $\Delta t_i = t_i - t_{i-1} > 0$, the spherical distance $\Delta s_i$ over an Earth of mean radius $R = 6{,}371{,}000\text{ m}$ is computed via the haversine formula:
$$\Delta s_i = 2R \arcsin \left( \sqrt{\sin^2\left(\frac{\phi_i - \phi_{i-1}}{2}\right) + \cos \phi_{i-1} \cos \phi_i \sin^2\left(\frac{\lambda_i - \lambda_{i-1}}{2}\right)} \right)$$

From this distance, analysts derive critical kinematic features:
1. **Implied trajectory speed:** $\bar{u}_i = \frac{\Delta s_i}{\Delta t_i}$. Discrepancies between broadcast instantaneous speed $u_i$ and implied trajectory speed $\bar{u}_i$ expose GNSS position spoofing, telemetry dropouts, or clock errors.
2. **Acceleration:** $a_i = \frac{u_i - u_{i-1}}{\Delta t_i}$. Commercial merchant vessels have bounded acceleration profiles ($|a| < 0.05\text{ m/s}^2$). Non-zero accelerations exceeding physical limits flag corrupted positions.
3. **Empirical Rate of Turn (ROT):** $\omega_i = \frac{\Delta \theta_i}{\Delta t_i}$, where angular difference $\Delta \theta_i = ((\theta_i - \theta_{i-1} + 180^\circ) \pmod{360^\circ}) - 180^\circ$. Broadcast ROT fields in Message 1 are frequently unpopulated or uncalibrated; empirical ROT derived from COG differencing provides a reliable signal.
4. **Trajectory curvature:** $\kappa_i = \frac{|\omega_i|}{u_i}$. High curvature at low speed indicates fishing maneuvers or docking; low curvature at high speed characterizes open-ocean cruising along great-circle fairways.

### 49.2.2 Contextual and environmental covariates

Kinematics alone cannot determine whether a ship is behaving legitimately. A vessel drifting at $1\text{ kn}$ in the open ocean might be awaiting orders, engaged in engine maintenance, or participating in an illegal bunkering transfer. In contrast, a vessel drifting at $1\text{ kn}$ over shallow shoals faces imminent grounding.

Robust analytical pipelines enrich kinematic vectors with external geospatial covariates:
- **Bathymetry:** Water depth $z$ extracted from global relief models (such as the General Bathymetric Chart of the Oceans, GEBCO). Under-keel clearance is computed as $UKC = z - T$, where $T$ is the static draught reported in Message 5. Negative or implausible clearances reveal false draught declarations or position spoofing onto drying banks.
- **Geographic proximity:** Orthodromic distance to nearest territorial sea baselines, Exclusive Economic Zone (**EEZ**) boundaries, Marine Protected Areas (**MPAs**), and designated anchorages.
- **Oceanographic current vectors:** Zonal and meridional surface currents $(u_{\text{curr}}, v_{\text{curr}})$ sourced from high-resolution ocean models (e.g., Copernicus Marine Service). Computing true Speed Through the Water (**STW**) and heading from SOG and COG vectors isolates active engine propulsion from passive drifting in ocean gyres.

## 49.3 Anomaly detection in maritime traffic

Maritime anomaly detection identifies vessel movements that deviate from established navigational norms, regulatory mandates, or physical laws. Applications range from detecting maritime smuggling and illegal border crossings to flagging disabled propulsion and cyber-physical attacks.

Following the maritime anomaly taxonomy established by Riveiro, Pallotta & Vespe (2018), analytical anomalies fall into three primary categories:

```
+-----------------------------------------------------------------------------+
|                       MARITIME ANOMALY TAXONOMY                             |
+-----------------------------------------------------------------------------+
|  [ SPATIAL ANOMALIES ]                                                      |
|    - Route deviation: Straying from established TSS or historical fairway   |
|    - Prohibited entry: Penetrating MPAs, safety fairways, or military zones |
|    - Kinematic impossibility: Land-crossing tracks, unphysical coordinates  |
|                                                                             |
|  [ KINEMATIC & BEHAVIORAL ANOMALIES ]                                       |
|    - Speed anomalies: Cruising in speed-restricted zones (e.g., whale SMAs) |
|    - Unscheduled stops: Loitering on high seas; unusual drifting or turning  |
|    - Draught shifts: Abrupt draught changes at sea indicating STS transfer   |
|                                                                             |
|  [ IDENTITY & SENSOR ANOMALIES ]                                            |
|    - Intentional AIS disabling: Gaps in terrestrial/satellite reception      |
|    - MMSI collisions / spoofing: Multiple vessels sharing one identity      |
|    - GNSS drift / manipulation: Coherent circular patterns, jump vectors    |
+-----------------------------------------------------------------------------+
```

### 49.3.1 Density-based spatial clustering and route graphs

Historical AIS traffic naturally clusters into high-density navigational corridors. Unsupervised clustering algorithms—specifically Density-Based Spatial Clustering of Applications with Noise (**DBSCAN**) and its hierarchical variant **HDBSCAN**—extract normal route networks without requiring labelled training sets.

In the foundational Traffic Route Extraction and Anomaly Detection (**TREAD**) framework developed by Pallotta, Vespe & Bryan (2013), raw AIS tracks are segmented into Waypoints (**WPs**)—representing ports, anchorages, and turning points—and Route Legs connecting them. An incoming vessel track $\mathcal{T}_{\text{query}}$ is tested against learned Gaussian Mixture Models (**GMMs**) representing the spatial cross-track distribution $\mathcal{N}(\mu_r, \sigma_r^2)$ and velocity profile of each route leg $r$. If the log-likelihood of the observed segment falls below an empirical confidence bound:
$$\ln p(\mathbf{x}_i \mid \text{Route}_r) < \tau_{\text{anomaly}}$$
the vessel is flagged for route deviation.

### 49.3.2 Deep generative anomaly detection

While density clustering extracts rigid spatial fairways, it struggles with complex multi-ship interactions and time-varying voyage dynamics. Modern systems employ deep generative models, notably Variational Autoencoders (**VAEs**) and sequence-to-sequence Recurrent Neural Networks (**RNNs** / **LSTMs**), to learn continuous latent probability distributions of normal maritime behavior.

A spatial-temporal trajectory window of length $W$, $\mathbf{X} = [\mathbf{x}_1, \dots, \mathbf{x}_W]$, is mapped by an encoder network $q_\phi(\mathbf{z} \mid \mathbf{X})$ to a low-dimensional latent Gaussian representation $\mathbf{z} \sim \mathcal{N}(\boldsymbol{\mu}_z, \boldsymbol{\Sigma}_z)$. A decoder network $p_\theta(\mathbf{X} \mid \mathbf{z})$ reconstructs the trajectory sequence $\hat{\mathbf{X}}$.

The model is trained exclusively on normal historical traffic by minimizing the evidence lower bound (**ELBO**):
$$\mathcal{L}(\theta, \phi; \mathbf{X}) = \mathbb{E}_{q_\phi(\mathbf{z} \mid \mathbf{X})}[\ln p_\theta(\mathbf{X} \mid \mathbf{z})] - D_{\text{KL}}(q_\phi(\mathbf{z} \mid \mathbf{X}) \parallel p(\mathbf{z}))$$
where $D_{\text{KL}}$ is the Kullback–Leibler divergence against a unit Gaussian prior $p(\mathbf{z})$.

When an anomalous trajectory—such as a vessel executing erratic evasive maneuvers or spoofing positions—is evaluated, the latent embedding falls outside the learned distribution, producing a large mean squared reconstruction error:
$$\text{Score}_{\text{anomaly}}(\mathbf{X}) = \frac{1}{W} \sum_{j=1}^W \|\mathbf{x}_j - \hat{\mathbf{x}}_j\|^2$$
Trajectories with reconstruction errors exceeding a calibrated validation threshold are dispatched to human watchstanders for operational inspection.

> **Definitions that bite.**
> **"AIS Gap" vs. "AIS Disabling":** An AIS gap is any period during which no messages are recorded from a vessel. A gap is caused either by RF link failures (such as satellite ALOHA packet collisions, high background noise, or antenna shading) or by deliberate transmitter shutdown. Concluding that a ship "went dark" to conduct illicit operations solely because an AIS gap exists is a frequent analytical failure. As established by Welch et al. (2022), intentional disabling must be statistically distinguished from reception loss by verifying whether neighboring vessels in the same satellite footprint were decoded during the identical orbital pass.

## 49.4 Destination and ETA prediction

Accurate prediction of a vessel's destination port and Estimated Time of Arrival (**ETA**) is fundamental to maritime logistics, port gate scheduling, and commodity flow forecasting ([Chapter 05](ch05-traders-finance-nowcasting.md)).

While Class A transponders broadcast destination and ETA fields in Message 5, these fields are manually keyed by bridge officers via the Minimum Keyboard and Display (**MKD**). As shown in [Chapter 47](ch47-data-quality-track-reconstruction.md), manual inputs suffer from severe data quality defects:
- Typographical errors (e.g., `ROTTERDAM`, `R'DAM`, `NL RTM`, or `ROTTEFDAM`).
- Ambiguous notations (e.g., `FOR ORDERS`, `ARMED GUARDS ON BOARD`, `CHANNEL`, or `SEA`).
- Stale configurations: ships frequently arrive at discharge ports broadcasting destinations from voyages completed months earlier.

```
+-----------------------------------------------------------------------------+
|                  DESTINATION & ETA PREDICTION WORKFLOW                      |
+-----------------------------------------------------------------------------+
|  [ VOYAGE SEGMENTATION ]                                                    |
|    - Identify port departure stop (SOG < 0.5 kn for > 2 hours in berth polygon) |
|    - Extract ongoing kinematic sequence: { (lat_i, lon_i, SOG_i, COG_i) }   |
|                                                                             |
|  [ DESTINATION PORT CLASSIFICATION ]                                        |
|    - Candidate ports from World Port Index (Pub 150)                        |
|    - Multi-class classifier (Gradient-boosted decision trees / LSTM):       |
|        P(Port = k | Trajectory_history, Vessel_type, Draught)               |
|                                                                             |
|  [ REMAINING TRANSIT & ETA REGRESSION ]                                     |
|    - Orthodromic or maritime fairway routing: Distance to Go (DTG)          |
|    - Speed-over-ground profile forecasting: u(s) along fairway path         |
|    - Predicted Arrival: ETA = t_now + Integral_{0}^{DTG} (1 / u(s)) ds      |
+-----------------------------------------------------------------------------+
```

### 49.4.1 Port destination classification

Automated destination prediction reformulates the problem as multi-class classification over a discrete spatial dictionary of global ports $\mathcal{P} = \{p_1, p_2, \dots, p_K\}$, commonly indexed against the U.S. National Geospatial-Intelligence Agency (**NGA**) World Port Index (Pub 150) or European UN/LOCODE registers.

Feature vectors extracted from the initial portion of a voyage—including departure port, heading upon pilot disembarkation, current latitude/longitude, deadweight tonnage, and draught—feed into gradient-boosted decision tree ensembles (e.g., LightGBM or XGBoost) or trajectory sequence encoders. In addition to kinematic features, models condition predictions on vessel trade patterns: a Capesize bulk carrier departing Dampier, Australia with laden draught has an overwhelming prior probability of transiting to a discrete set of iron ore terminals in northern China or Japan.

### 49.4.2 ETA forecasting and fairway distance regression

Once the destination port $p^*$ is identified, predicting the remaining transit time requires routing along navigable waterways rather than Euclidean great circles. Navigational graphs (such as the open-source `searoute` network or customized A* marine routing fairways) calculate the Distance To Go (**DTG**), strictly avoiding land masses, shallow bathymetry, and traffic separation schemes.

Let $s \in [0, \text{DTG}]$ represent remaining distance along the fairway. The predicted time of arrival $t_{\text{ETA}}$ is:
$$t_{\text{ETA}} = t_{\text{current}} + \int_0^{\text{DTG}} \frac{1}{\hat{u}(s)} \, ds$$
where $\hat{u}(s)$ is the predicted speed profile. Machine-learning regressors forecast $\hat{u}(s)$ as a function of vessel design speed, seasonal metocean headwinds, and historical port congestion delays at anchorages fronting the destination terminal.

## 49.5 Fisheries classification, transshipment, and dark-fleet fusion

One of the most impactful applications of machine learning to AIS is the global monitoring of commercial fisheries, illegal, unreported, and unregulated (**IUU**) fishing, and high-seas transshipment.

### 49.5.1 The Global Fishing Watch convolutional architectures

Prior to 2016, quantifying global fishing effort was constrained by fragmented national logbooks and confidential Vessel Monitoring System (**VMS**) feeds. In landmark research published in *Science*, Kroodsma et al. (2018) developed a planetary-scale ML pipeline processing 22 billion AIS messages broadcast by over 70,000 commercial fishing vessels between 2012 and 2016.

```
+-----------------------------------------------------------------------------+
|                 GLOBAL FISHING WATCH CLASSIFIER PIPELINE                    |
+-----------------------------------------------------------------------------+
|  [ INPUT: Resampled 1D Trajectory Sequence (54 Dynamic Features) ]          |
|    - Lat, Lon, SOG, COG, Delta_t, Curvature, Local Hour, Solar Elevation    |
|                                                                             |
|  [ CONVOLUTIONAL NEURAL NETWORK (ResNet-style 1D Residual Blocks) ]         |
|    - Layer 1: 1D Conv (Kernel size 3, 64 filters) + Batch Normalization     |
|    - Residual Blocks 2-5: Dilated 1D Convolutions (Receptive field > 24 h)  |
|    - Global Average Pooling / Softmax Layer                                 |
|                                                                             |
|  [ DUAL CLASSIFICATION HEADS ]                                              |
|    1. Vessel Gear Type: Longliner, Trawler, Purse Seiner, Squid Jigger      |
|    2. Per-Point Fishing Score: P(Fishing = True | Window around t_i) in [0,1] |
+-----------------------------------------------------------------------------+
```

The GFW architecture operates in two stages:
1. **Vessel characterization:** Classifying vessel length, engine power (kW), and primary gear type (drifting longline, bottom/pelagic trawl, purse seine, pole and line, squid jigger).
2. **Point-wise fishing activity detection:** Labeling individual position reports as "active fishing" versus "steaming" or "drifting".

Rather than relying on hand-crafted heuristic rules, the pipeline resamples irregular AIS tracks to uniform temporal intervals (typically 10-minute bins) and feeds 54 extracted kinematic and astronomical variables (including solar elevation and local time) into a 1D residual convolutional neural network (**CNN**).

Trawlers, longliners, and purse seiners exhibit distinct kinematic signatures:
- **Trawlers:** Exhibit prolonged periods of reduced, steady speed ($2.5–4.5\text{ kn}$) and sustained heading while towing gear, often in straight lines or slight contours along bathymetric isobaths.
- **Drifting longliners:** Demonstrate complex, multi-stage speed profiles: high-speed transit while setting gear (up to tens of nautical miles of line), followed by slow drifting while the gear soaks, and slow, step-like stop-and-go movements during hauling.
- **Purse seiners:** Cruise at high searching speed ($10–14\text{ kn}$), execute tight circular sets at maximum speed to encircle fish schools, and then remain stationary or drift slowly for several hours while pursing and brailing the catch.

Validation against official VMS logbooks demonstrated classification accuracies exceeding 90% across major gear classes, revealing that commercial fishing spans over 55% of global ocean surface area—more than four times the spatial footprint of terrestrial agriculture (Kroodsma et al. 2018).

### 49.5.2 High-seas transshipment detection

Transshipment—the offloading of catch and refueling at sea between commercial fishing vessels and specialized refrigerated cargo ships ("reefers")—enables fishing vessels to remain on high-seas grounds for months or years without entering port. While legally permitted under certain Regional Fisheries Management Organizations (**RFMOs**), transshipment can facilitate fish laundering, sanctions evasion, and forced labor.

Building on the methodology of Miller et al. (2018) and Boerder, Miller & Worm (2018), analytical pipelines automatically flag transshipment encounters by identifying spatial-temporal co-occurrences meeting three rigorous physical criteria:

$$\begin{aligned}
\text{Separation Distance:} \quad & d(v_{\text{fish}}, v_{\text{reefer}}) \le 500\text{ m} \\
\text{Encounter Duration:} \quad & \Delta t_{\text{co-occur}} \ge 3.0\text{ hours} \\
\text{Median Velocity:} \quad & \tilde{u} \le 2.0\text{ kn} \quad (\text{often drifting passively in tandem})
\end{aligned}$$

Additionally, algorithms detect **loitering events**: situations where a refrigerated cargo ship anchors or drifts at low speed ($< 2\text{ kn}$) on the high seas for more than 4 hours without broadcasting an AIS-associated partner vessel. Loitering strongly correlates with rendezvous involving "dark" vessels whose transponders are switched off or non-operational.

### 49.5.3 Multi-sensor fusion with satellite SAR and optical imagery

Vessels engaged in illicit fishing, illegal bunkering, or sanctions-evading trade regularly switch off their AIS transponders to avoid detection. Identifying these uncooperative vessels requires fusing broadcast AIS feeds with non-cooperative remote sensing, primarily spaceborne Synthetic Aperture Radar (**SAR**) and high-resolution optical imagery ([Chapter 66](ch66-other-ways-to-track-ships.md)).

In a groundbreaking planetary study, Paolo et al. (2024) processed 2.0 petabytes of satellite imagery from the European Space Agency's Sentinel-1 C-band SAR and Sentinel-2 optical constellations spanning 2017 to 2021. The detection pipeline operates across three technical stages:

```
+-----------------------------------------------------------------------------+
|                  AIS-SAR MULTI-SENSOR FUSION PIPELINE                       |
+-----------------------------------------------------------------------------+
|  [ STAGE 1: Deep-Learning Object Detection in Satellite Footprints ]        |
|    - Sentinel-1 SAR (GRD tiles) / Sentinel-2 Optical RGB/NIR imagery        |
|    - Feature Pyramid Network (FPN) CNN identifies vessel candidates          |
|    - Estimates physical length, beam, and orientation angle (psi_SAR)       |
|                                                                             |
|  [ STAGE 2: Spatial-Temporal AIS Matching Window ]                          |
|    - Satellite overpass timestamp t_sat; Search radius r = u_max * Delta_t  |
|    - Extract candidate AIS tracks: t in [t_sat - 15 min, t_sat + 15 min]    |
|    - Interpolate AIS position to exact satellite imaging time t_sat         |
|                                                                             |
|  [ STAGE 3: Multi-Hypothesis Association Scoring ]                          |
|    - Mahalanobis spatial distance: d_M(x_SAR, x_AIS)                        |
|    - Heading vs. SAR orientation difference: Delta_theta = |theta - psi_SAR| |
|    - Vessel length consistency: |L_SAR - L_AIS| / L_AIS                     |
|                                                                             |
|  [ CLASSIFICATION RESULT ]                                                  |
|    - Associated: Cooperative vessel transmitting valid AIS                  |
|    - Unmatched SAR Target: "Dark vessel" operating with AIS deactivated     |
+-----------------------------------------------------------------------------+
```

Paolo et al. (2024) revealed that **72–76% of industrial fishing vessels** and **21–30% of transport and offshore energy vessels** operating globally are entirely invisible to public AIS tracking. Unmapped "dark fleets" cluster intensely around coastal Asia, West Africa, and South America, demonstrating that AIS alone cannot provide an exhaustive picture of maritime operations.

> **Try it.**
> Detecting encounters and vessel-to-vessel rendezvous in an AIS stream. Run the following DuckDB analytical query to find vessels that navigated within $1{,}500\text{ m}$ of each other at low speed in the included harbor sample:
> ```bash
> . .venv/bin/activate
> python -c '
> import duckdb, pandas as pd
> con = duckdb.connect()
> df = pd.read_csv("data/samples/synthetic_harbor_truth.csv")
> con.register("truth", df)
> q = """
> WITH valid_ships AS (
>   SELECT mmsi, CAST(time AS TIMESTAMP) as t, lat, lon, sog
>   FROM truth
>   WHERE mmsi NOT IN (0, 1193046) AND sog <= 15.0
> ),
> pairs AS (
>   SELECT a.mmsi as mmsi_a, b.mmsi as mmsi_b, a.t,
>          sqrt(pow((a.lat - b.lat) * 111139.0, 2) + 
>               pow((a.lon - b.lon) * 82190.0, 2)) as dist_m
>   FROM valid_ships a
>   JOIN valid_ships b ON a.mmsi < b.mmsi AND a.t = b.t
> )
> SELECT mmsi_a, mmsi_b, round(min(dist_m), 1) as closest_dist_m, count(*) as overlapping_reports
> FROM pairs
> WHERE dist_m <= 1500
> GROUP BY mmsi_a, mmsi_b
> ORDER BY closest_dist_m;
> """
> print(con.execute(q).df())
> '
> ```
> Expected output:
> ```
>       mmsi_a     mmsi_b  closest_dist_m  overlapping_reports
> 0  244999703  316999704           319.9                   11
> ```

## 49.6 Environmental impact analytics: emissions, underwater noise, and ship strikes

Beyond security and trade logistics, AIS data drives computational modeling of shipping's environmental footprint on the biosphere.

### 49.6.1 Emissions inventories and STEAM

Maritime shipping generates approximately 3% of total global greenhouse gas emissions (Faber et al. 2020). Modern emissions modeling has moved from top-down bunker fuel sales estimates to bottom-up, vessel-resolved computational inventories driven by dynamic AIS tracks.

The leading framework for AIS-based emissions modeling is the **Ship Traffic Emission Assessment Model (STEAM)** developed by Jalkanen et al. (2009, 2012) at the Finnish Meteorological Institute. STEAM calculates instantaneous exhaust emissions for individual ships at high spatial and temporal resolution.

```
+-----------------------------------------------------------------------------+
|                   STEAM EMISSIONS INVENTORY PIPELINE                        |
+-----------------------------------------------------------------------------+
|  [ DYNAMIC AIS TRACK ]           [ STATIC VESSEL SPECIFICATIONS (IHS) ]     |
|    - Speed Over Ground (u)         - Installed Engine Power (P_installed)   |
|    - Dynamic Draught (T)           - Engine Stroke, RPM, Fuel Type          |
|    - Metocean wind/waves (u_w)     - Hull Dimensions: Length, Beam, Block C_b|
|          |                                       |                          |
|          +-------------------+-------------------+                          |
|                              |                                              |
|                              v                                              |
|  [ HYDRODYNAMIC RESISTANCE & INSTANTANEOUS POWER CALCULATION ]              |
|    1. Frictional & Residual Hull Resistance: R_total(u, T, C_b)             |
|    2. Environmental Added Resistance (Waves, Wind): R_env(u_w)              |
|    3. Effective Propulsive Power: P_prop = (R_total * u) / eta_prop         |
|    4. Auxiliary Engine & Boiler Load Estimation: P_aux, P_boiler            |
|                              |                                              |
|                              v                                              |
|  [ EMISSION FACTOR APPLICATION ]                                            |
|    - Specific Fuel Oil Consumption: SFOC(Load Factor = P_inst / P_installed)|
|    - Emission Factors (g/kWh) by Engine Tier: EF_CO2, EF_NOx, EF_SOx, EF_PM |
|    - Mass Emitted: E_x = Integral [ P_total(t) * EF_x(t) ] dt               |
+-----------------------------------------------------------------------------+
```

Instantaneous engine power $P_{\text{req}}(t)$ is determined by the cubic relationship between vessel speed through water $u$ and hydrodynamic resistance:
$$P_{\text{req}}(t) = \frac{R_{\text{total}}(u, T) \cdot u}{\eta_{\text{prop}}} + P_{\text{aux}} + P_{\text{boiler}}$$
where $R_{\text{total}}$ is total hull resistance (decomposed into frictional, wave-making, and appendages resistance via the Holtrop & Mennen formulation), $\eta_{\text{prop}}$ is propulsive efficiency, $P_{\text{aux}}$ is auxiliary electrical load, and $P_{\text{boiler}}$ is hoteling boiler load.

Mass of pollutant $x$ emitted during a time interval $\Delta t$ is:
$$E_x = P_{\text{req}}(t) \cdot \text{SFOC}(\text{load}) \cdot \text{EF}_x \cdot \Delta t$$
where $\text{SFOC}$ is the Specific Fuel Oil Consumption (in $\text{g/kWh}$, varying non-linearly with engine load factor $P_{\text{req}} / P_{\text{installed}}$) and $\text{EF}_x$ is the fuel- and tier-dependent emission factor for $\text{CO}_2$, $\text{NO}_x$, $\text{SO}_x$, or particulate matter ($\text{PM}_{2.5}$).

The International Maritime Organization (**IMO**) Fourth GHG Study 2020 adopted an AIS-driven bottom-up inventory methodology, demonstrating that global shipping emissions grew from 977 million tonnes of $\text{CO}_2\text{e}$ in 2012 to 1,076 million tonnes in 2018 (Faber et al. 2020).

### 49.6.2 Underwater radiated noise modeling

Commercial ship traffic represents the primary source of low-frequency anthropogenic noise ($10–500\text{ Hz}$) in the marine environment, overlapping critical communication and echolocation frequencies utilized by cetaceans.

Analytical acoustic frameworks—exemplified by the Vancouver Fraser Port Authority's Enhancing Cetacean and Habitat Observation (**ECHO**) program and regional models developed by JASCO Applied Sciences—synthesize dynamic AIS tracks with underwater acoustic propagation models.

The acoustic modeling pipeline follows a **Source-Path-Receiver** architecture:
1. **Source level characterization ($SL$):** Each vessel in the AIS stream is assigned an acoustic source level in $\text{dB re } 1\ \mu\text{Pa}^2\text{ m}^2/\text{Hz}$ based on vessel class, length $L$, and speed $u$. Empirical formulations (such as the Ross 1976 model or refined ECHO regression curves) characterize propeller cavitation and machinery noise:
   $$SL(f, u, L) = SL_0(f) + c_u \cdot \log_{10}\left(\frac{u}{u_{\text{ref}}}\right) + c_L \cdot \log_{10}\left(\frac{L}{L_{\text{ref}}}\right)$$
2. **Transmission loss ($TL$):** Sound propagation away from each vessel track is computed across a spatial grid using parabolic equation (**PE**) models (e.g., RAM) or ray-tracing code, accounting for frequency-dependent bathymetry, sub-bottom sediment geoacoustics, and seasonal sound speed profiles $c(z)$.
3. **Sound field accumulation:** The instantaneous Sound Pressure Level ($SPL$) at any receiver coordinate $(x, y, z)$ is computed by summing the insonified energy contributions from all $M$ active vessels:
   $$SPL(x, y, z, f) = 10 \log_{10} \left( \sum_{m=1}^M 10^{\frac{SL_m(f) - TL_m(x, y, z, f)}{10}} \right)$$

Accumulated monthly and annual noise dose maps identify chronic acoustic masking zones across critical whale habitats, establishing empirical justification for voluntary port vessel slowdown trials.

### 49.6.3 Cetacean collision lethality modeling

Collisions with commercial shipping ("ship strikes") are a leading cause of anthropogenic mortality for endangered baleen whales, including the North Atlantic right whale (*Eubalaena glacialis*) and blue whale (*Balaenoptera musculus*).

Analytical strike models combine AIS-derived vessel traffic density and speeds with cetacean aerial survey and satellite telemetry distributions. Lethality modeling hinges on empirical logistic regression functions relating vessel impact speed $u$ (in knots) to the probability of lethal injury $P(\text{Lethal} \mid u)$ given a physical strike.

In the foundational epidemiological model established by Vanderlaan & Taggart (2007) and extended by Conn & Silber (2013), strike lethality is expressed as:
$$P(\text{Lethal} \mid u) = \frac{1}{1 + \exp\left(-(\beta_0 + \beta_1 u)\right)}$$

Using empirical strike records, Vanderlaan & Taggart (2007) estimated parameters $\beta_0 = -4.893$ and $\beta_1 = 0.413$, establishing that the probability of mortality exceeds 50% at speeds greater than $11.8\text{ kn}$, escalating to $89\%$ at $15\text{ kn}$, but dropping below $20\%$ at speeds under $8.6\text{ kn}$. This empirical curve established the scientific baseline for mandatory $10\text{ kn}$ Seasonal Management Areas (**SMAs**) enforced by NOAA Fisheries along the U.S. Eastern Seaboard.

## 49.7 Collision risk indices and tactical encounter modeling

In tactical maritime navigation, automated collision risk prediction models evaluate multi-vessel encounter dynamics to support bridge watchstanders and autonomous collision-avoidance algorithms for Maritime Autonomous Surface Ships (**MASS**) ([Chapter 57](ch57-autonomous-ships.md)).

### 49.7.1 DCPA and TCPA kinematics

The classical geometric foundations of encounter risk are the Distance to Closest Point of Approach (**DCPA**) and Time to Closest Point of Approach (**TCPA**).

```
          Vessel 2 (Target)
              (x_2, y_2)  \
                           \  v_2
                            \
                             v
                              +  Encounter CPA Point
                             ^
                            /
                           /  v_1
                          /
          Vessel 1 (Own Ship)
              (x_1, y_1)
```

Let own ship be located at position $\mathbf{p}_1 = [x_1, y_1]^T$ with velocity vector $\mathbf{v}_1 = [u_1 \sin \theta_1, u_1 \cos \theta_1]^T$, and target ship at $\mathbf{p}_2 = [x_2, y_2]^T$ with velocity $\mathbf{v}_2 = [u_2 \sin \theta_2, u_2 \cos \theta_2]^T$.

Define the relative position vector $\mathbf{p}_r = \mathbf{p}_2 - \mathbf{p}_1$ and relative velocity vector $\mathbf{v}_r = \mathbf{v}_2 - \mathbf{v}_1$. The time remaining until closest approach $t_{\text{TCPA}}$ is:
$$t_{\text{TCPA}} = -\frac{\mathbf{p}_r \cdot \mathbf{v}_r}{\|\mathbf{v}_r\|^2}$$

A negative $t_{\text{TCPA}}$ indicates that the vessels have already passed their point of closest approach and are diverging. If $t_{\text{TCPA}} > 0$, the vessels are converging, and the minimum physical separation distance $d_{\text{DCPA}}$ is:
$$d_{\text{DCPA}} = \|\mathbf{p}_r + t_{\text{TCPA}} \mathbf{v}_r\| = \sqrt{\|\mathbf{p}_r\|^2 - \frac{(\mathbf{p}_r \cdot \mathbf{v}_r)^2}{\|\mathbf{v}_r\|^2}}$$

> **Worked example.**
> **Tactical encounter calculation for two converging merchant vessels:**
> Own Ship (Container vessel): Position $\mathbf{p}_1 = (0.0, 0.0)\text{ nmi}$, cruising due North ($\theta_1 = 000^\circ$) at $u_1 = 15.0\text{ kn}$. Velocity $\mathbf{v}_1 = (0.0, 15.0)$.
> Target Ship (Bulk carrier): Position $\mathbf{p}_2 = (2.0, 2.0)\text{ nmi}$ (distance $D = \sqrt{2^2 + 2^2} \approx 2.83\text{ nmi}$ on bearing $045^\circ$), steaming due West ($\theta_2 = 270^\circ$) at $u_2 = 15.0\text{ kn}$. Velocity $\mathbf{v}_2 = (-15.0, 0.0)$.
>
> 1. Compute relative vectors:
>    $$\mathbf{p}_r = \mathbf{p}_2 - \mathbf{p}_1 = (2.0 - 0.0, 2.0 - 0.0) = (2.0, 2.0)\text{ nmi}$$
>    $$\mathbf{v}_r = \mathbf{v}_2 - \mathbf{v}_1 = (-15.0 - 0.0, 0.0 - 15.0) = (-15.0, -15.0)\text{ kn}$$
> 2. Compute relative scalar magnitudes:
>    $$\|\mathbf{v}_r\|^2 = (-15.0)^2 + (-15.0)^2 = 225.0 + 225.0 = 450.0\text{ kn}^2 \implies \|\mathbf{v}_r\| \approx 21.21\text{ kn}$$
>    $$\mathbf{p}_r \cdot \mathbf{v}_r = (2.0 \cdot -15.0) + (2.0 \cdot -15.0) = -30.0 + (-30.0) = -60.0\text{ nmi}\cdot\text{kn}$$
> 3. Calculate TCPA:
>    $$t_{\text{TCPA}} = -\frac{-60.0}{450.0} = \frac{2}{15}\text{ hours} = 0.1333\text{ hours} = 8.0\text{ minutes}$$
> 4. Calculate position at $t_{\text{TCPA}}$:
>    $$\mathbf{p}_1(t_{\text{TCPA}}) = (0.0, 15.0 \cdot 0.1333) = (0.0, 2.0)\text{ nmi}$$
>    $$\mathbf{p}_2(t_{\text{TCPA}}) = (2.0 - 15.0 \cdot 0.1333, 2.0) = (0.0, 2.0)\text{ nmi}$$
> 5. Calculate DCPA:
>    $$d_{\text{DCPA}} = \|\mathbf{p}_2(t_{\text{TCPA}}) - \mathbf{p}_1(t_{\text{TCPA}})\| = \|(0.0, 0.0)\| = 0.00\text{ nmi}$$
> In 8.0 minutes, both ships will occupy the identical geographic coordinate $(0.0\text{ nmi}, 2.0\text{ nmi})$, representing an immediate collision threat requiring immediate COLREGS Rule 15/16 action.

### 49.7.2 The Collision Risk Index (CRI)

While DCPA and TCPA provide crisp geometric quantities, human watchstanders do not evaluate risk linearly. A DCPA of $0.5\text{ nmi}$ represents severe peril in open water for large crude carriers, but is routine in restricted port channels.

The unified **Collision Risk Index (CRI)**, originally formalized by Imazu (1983) and expanded across modern fuzzy logic and adaptive neuro-fuzzy systems (**ANFIS**), synthesizes multiple navigational variables into a normalized score $\text{CRI} \in [0.0, 1.0]$:

$$\text{CRI} = w_d f_d(d_{\text{DCPA}}) + w_t f_t(t_{\text{TCPA}}) + w_D f_D(D) + w_\theta f_\theta(\theta_{\text{rel}}) + w_K f_K(K)$$
where $D$ is instantaneous distance, $\theta_{\text{rel}}$ is relative bearing, $K = u_2 / u_1$ is velocity ratio, and $w_i$ are contextual weights derived via Analytic Hierarchy Process (**AHP**) methods reflecting COLREGS crossing, head-on, or overtaking geometries.

When integrated into modern VTS surveillance suites, automated CRI alerts trigger audible alarms whenever combined thresholds ($\text{CRI} > 0.75$) occur across multiple converging tracks.

## 49.8 Public benchmark datasets and empirical evaluation standards

Empirical research in maritime machine learning relies on standardized public benchmarks to evaluate trajectory prediction, anomaly detection, and vessel classification models.

### 49.8.1 Key public benchmarks

Prominent public datasets driving maritime data science include:

1. **Marine Cadastre AIS National Datasets (NOAA / BOEM):** Unfiltered archive of terrestrial NAIS and satellite AIS reports across United States coastal waters from 2009 onwards. Distributed as daily/monthly Parquet and CSV files, providing billions of standardized records.
2. **Global Fishing Watch Public Data Portals:** Open datasets hosted on Google BigQuery and Google Earth Engine. Contains 100-meter gridded daily fishing effort maps from 2012 onwards, alongside training sets of classified fishing events, reefer encounters, and loitering events.
3. **Ushant / Brittany Traffic Separation Scheme Benchmark:** Academic benchmark consisting of six months of high-density AIS data captured off the Ushant TSS in northwestern France. Standardized by the French Naval Academy Research Institute (IRENav) for trajectory clustering and anomaly evaluation.
4. **Danish Maritime Authority (DMA) Open Feeds:** Continuous open-access archive of raw AIS NMEA sentences and point CSVs covering Danish territorial waters and Baltic approaches. Serves as a primary test corpus for decoding and streaming ingestion pipelines.

### 49.8.2 Evaluation metrics for maritime ML

Standard ML classification metrics (accuracy, precision, recall, F1-score) must be applied cautiously in maritime applications due to extreme class imbalance:
- **Anomaly detection:** Illicit events (smuggling, AIS spoofing) represent less than $0.01\%$ of all observations. Naive accuracy is meaningless; models must report Area Under the Precision-Recall Curve (**PR-AUC**) rather than ROC-AUC, alongside explicit False Positive Rates per 1,000 tracked vessel-hours.
- **Trajectory prediction error:** Trajectory forecasting models must report Mean Absolute Error (**MAE**) and Root Mean Squared Error (**RMSE**) in physical distance (meters or nautical miles), rather than coordinate degrees:
  $$\text{FDE} = \|\mathbf{p}_{\text{true}}(t_{\text{end}}) - \hat{\mathbf{p}}(t_{\text{end}})\|, \quad \text{ADE} = \frac{1}{T} \sum_{t=1}^T \|\mathbf{p}_{\text{true}}(t) - \hat{\mathbf{p}}(t)\|$$
  where **FDE** is Final Displacement Error and **ADE** is Average Displacement Error.

## Then & now

- **⟨H⟩ 1960s–1980s:** Maritime traffic surveillance relied exclusively on manual radar plotting, shore-based VHF voice check-in reporting, and paper plotting sheets. Anomaly detection was confined to visual observation by watch officers or VTS radar operators.
- **⟨H⟩ 2002–2006:** Following the entry into force of the IMO SOLAS carriage requirements, initial digital AIS analytics aggregated raw NMEA sentences directly into desktop GIS packages (e.g., ArcView, GRASS GIS). Spatial analysis was restricted to static, unweighted point-density heatmaps.
- **⟨+⟩ 2009:** Jalkanen et al. introduce the Ship Traffic Emission Assessment Model (STEAM), demonstrating that dynamic AIS position broadcasts can be fused with naval architectural formulas to model atmospheric emissions at high spatiotemporal resolution.
- **⟨+⟩ 2013:** Pallotta, Vespe, and Bryan formalize the Traffic Route Extraction and Anomaly Detection (TREAD) framework, introducing unsupervised clustering and statistical waypoint modeling for maritime situational awareness.
- **⟨+⟩ 2018:** Global Fishing Watch publishes the first planetary analysis of commercial fisheries in *Science* (Kroodsma et al.), processing 22 billion AIS messages using deep convolutional neural networks to classify fishing behaviors across 55% of the ocean.
- **⟨+⟩ 2018:** Nathan Miller, Kristina Boerder, and Boris Worm establish automated spatial-temporal encounter algorithms to map global high-seas transshipment and refrigerated cargo loitering.
- **⟨+⟩ 2020:** The International Maritime Organization publishes the *Fourth IMO GHG Study 2020*, enshrining AIS-based bottom-up modeling as the international standard for assessing maritime greenhouse gas emissions.
- **⟨+⟩ 2024:** Fernando Paolo et al. publish planetary-scale satellite radar and optical fusion in *Nature*, proving that 75% of global industrial fishing vessels operate "dark" without broadcast AIS, establishing the necessity of multi-sensor fusion.

---

## Validation, uncertainty & data quality

To prevent machine learning models from learning spurious patterns or failing in mission-critical surveillance environments, analysts must enforce rigorous data validation and uncertainty auditing across five discrete failure dimensions:

```
+-----------------------------------------------------------------------------+
|                         ML DATA QUALITY AUDIT STACK                         |
+-----------------------------------------------------------------------------+
|  [ LAYER 5: Temporal Cross-Validation & Anti-Leakage Controls ]             |
|    - Split by chronological time blocks or isolated MMSIs                   |
|    - Discard models trained with random shuffle k-fold on trajectory points |
|                                                                             |
|  [ LAYER 4: Telemetry Plausibility & Sentinel Filtering ]                   |
|    - SOG <= 60.0 kn; ROT != -128; Heading != 511; Lat != 91; Lon != 181    |
|    - Acceleration |a| <= 0.2 m/s^2; Implied speed consistency: |u_s - u| <= 3|
|                                                                             |
|  [ LAYER 3: Reception Bias Normalization ]                                  |
|    - Weight observations by inverse empirical detection probability P(Rx)   |
|    - Normalize reporting intervals across Class A dynamic regimes (2s - 3m)  |
|                                                                             |
|  [ LAYER 2: Epistemic Uncertainty Quantification ]                          |
|    - Deep ensemble prediction variances; Monte Carlo dropout confidence     |
|    - Conformal prediction intervals for destination ETA bounds              |
|                                                                             |
|  [ LAYER 1: Multi-Sensor Ground Truth Auditing ]                            |
|    - Benchmark against uncorrupted VDR and shore radar tracks              |
|    - Validate satellite SAR detections against independent RF geolocation   |
+-----------------------------------------------------------------------------+
```

### Concrete validation procedures and error statistics

1. **Temporal data leakage prevention:** In trajectory prediction and behavior modeling, applying standard random $k$-fold cross-validation is an catastrophic methodological error. Because successive AIS reports from a single vessel are spaced seconds apart, randomly partitioning points places point $t_i$ in the training set and $t_{i+1}$ in the test set. The model trivially memorizes the trajectory rather than learning predictive dynamics, reporting inflated $R^2 > 0.99$ that collapses to near-zero in production. Validation must be executed strictly via **temporal splits** (training on months $1–9$, testing on months $10–12$) or **vessel-isolated splits** (ensuring no MMSI appearing in the test partition ever appears in the training partition).
2. **Sentinel value purge:** As detailed in [Chapter 22](ch22-message-catalog.md), standard ITU-R M.1371 numerical sentinels must never be passed into numeric machine learning regressors. Reports containing SOG $= 102.3\text{ kn}$ (speed not available), Heading $= 511^\circ$ (heading not available), or coordinates $(91.0^\circ\text{ N}, 181.0^\circ\text{ E})$ represent missing sensor inputs. Passing SOG $= 102.3$ into a neural network skews normalized feature distributions and produces phantom high-speed anomaly alarms.
3. **Kinematic velocity consistency:** Every sequential pair of points must satisfy:
   $$|\bar{u}_{\text{implied}} - u_{\text{broadcast}}| \le 3.0\text{ kn} + 0.1 \cdot u_{\text{broadcast}}$$
   where $\bar{u}_{\text{implied}} = \Delta s / \Delta t$. Pairs failing this bound indicate GNSS position jumps, dropped intermediate sentences, or clock misalignments.
4. **Label noise auditing in supervised datasets:** Manually keyed static data contains high label noise: destination fields are misspelled or stale in 15–20% of transmissions, and vessel type codes (Message 5) misclassify specialized craft. Models trained on raw static labels must apply robust loss functions or automated cleaning pipelines prior to training.

---

## Software

### Open source
* **DuckDB Spatial:** In-process analytical SQL engine executing columnar spatial window queries, haversine cross-joins, and trajectory filtering at tens of millions of rows per second over Parquet files. *Caveat:* Spatial index construction is in-memory and non-persistent across restarts.
* **MovingPandas:** Trajectory analysis library built on GeoPandas and Shapely, offering standardized methods for spatial trajectory segmentation, stop detection, and temporal smoothing. *Caveat:* Memory-intensive; processing global AIS collections requires distributed partitioning via Dask.
* **Scikit-learn:** Python machine learning toolkit providing robust implementations of DBSCAN, HDBSCAN, One-Class SVM, and Isolation Forest algorithms for trajectory anomaly detection. *Caveat:* Coordinates must be projected to local planar CRS or transformed using haversine metric matrices.
* **PyTorch / TensorFlow:** Deep learning frameworks utilized for training 1D CNNs, sequence LSTMs, and Variational Autoencoders on resampled AIS trajectory sequences. *Caveat:* Requires significant GPU memory and specialized data loaders to handle variable-length trajectories.
* **searoute:** Python library calculating shortest marine routes across global oceanic networks avoiding land masses. *Caveat:* Coarse fairway graph resolution can produce unrealistic zig-zags in complex archipelagos.

### Free but closed
* **Google Earth Engine (GEE):** Cloud geospatial platform hosting public Global Fishing Watch daily rasterized fishing effort grids and environmental covariates. *Caveat:* Proprietary execution sandbox with strict runtime quotas.
* **Marine Cadastre National Viewer:** Interactive GIS viewer maintained by NOAA and BOEM providing pre-computed vessel tracklines, annual density rasters, and transit summaries for U.S. waters. *Caveat:* Cannot score real-time feeds or custom uploaded AIS data.

### Commercial
* **Spire Maritime AIS Analytics:** Commercial satellite/terrestrial fused AIS streaming API offering pre-computed voyage segmentation, destination prediction, and berth-level ETA calculations. *Caveat:* High licensing cost; proprietary ETA neural network weights are closed.
* **Kpler (MarineTraffic / FleetMon):** Enterprise commodity flow and vessel tracking platform providing automated port-call analytics, anchorage wait-time indices, and refinery discharge nowcasts. *Caveat:* Underlying model weights and receiver weightings are proprietary.
* **Windward:** Maritime AI intelligence platform specializing in automated sanctions compliance, predictive vessel risk profiling, and deceptive shipping practice detection. *Caveat:* Enterprise defense subscription; proprietary risk scoring models cannot be independently audited.

---

## Standards & guides

* **ITU-R Recommendation M.1371-6 (2026):** *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Frequency Band*. Governs reporting intervals, message payload bit allocations, and numeric sentinel definitions.
* **IMO Resolution MSC.74(69) Annex 3 (1998):** *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)*. Establishes core statutory requirements for vessel collision avoidance and operational broadcast behavior.
* **IMO Fourth GHG Study 2020 (Faber et al. 2020):** *Fourth IMO Greenhouse Gas Study*. International Maritime Organization reference standard governing bottom-up, AIS-driven naval architectural calculations of maritime carbon intensity and exhaust emissions.
* **IHO Publication S-52 / S-100 (2020):** *Specifications for Chart Content and Display Aspects of ECDIS / Universal Hydrographic Data Model*. Governs tactical target symbology, CPA/TCPA alarms, and electronic navigational chart boundaries.
* **NGA World Port Index (Pub 150, 2025):** National Geospatial-Intelligence Agency register of global port locations, physical characteristics, and terminal boundaries, serving as the canonical geographic dictionary for destination modeling.
* **ISO 19847:2018 / ISO 19848:2018:** *Ships and Marine Technology — Shipboard Data Servers to Share Field Data at Sea / Standard Data for Shipboard Machinery and Systems*. Establishes standard data structures for integrating onboard sensor networks with shoreside analytical models.

---

## Pitfalls

* **Training models on random point shuffles instead of temporal splits:** Applying standard random $k$-fold cross-validation on trajectory points causes catastrophic temporal data leakage. Successive observations from the same ship are strongly autocorrelated. Models trivially interpolate neighboring points, reporting inflated accuracies that fail completely in real-world deployment.
* **Ignoring ITU-R M.1371 sentinel values:** Treating missing-data flags (SOG $= 102.3$, Heading $= 511$, ROT $= -128$) as valid physical measurements injects extreme numerical outliers into regression and clustering pipelines, generating false anomaly alarms.
* **Confusing satellite reception gaps with intentional AIS disabling:** Low Earth Orbit satellites suffer from message collisions in high-density waterways, causing detection gaps of several hours. Assuming that a ship "went dark" to engage in illegal activity without verifying whether neighboring vessels in the footprint were detected is a major analytical error.
* **Calculating Euclidean distances on spherical geographic coordinates:** Computing distances, curvatures, or DBSCAN neighborhoods directly on $(\phi, \lambda)$ degrees without haversine or equal-area planar projection creates severe latitudinal distortion. A degree of longitude at $60^\circ\text{ N}$ represents half the physical distance of a degree at the equator.
* **Neglecting vessel operational priors in destination prediction:** Training pure kinematic sequence models to predict destination ports without conditioning on ship type, size, and draft ignores massive physical constraints. A 400-meter container ship cannot enter shallow bulk-export estuaries.
* **Over-interpreting manual Message 5 static declarations:** Static destination and ETA fields are keyed manually by human crews and are stale or misspelled in 15–20% of broadcasts. Treating broadcast destination as ground truth distorts model training.
* **Using pure point-density maps to infer vessel activity:** Raw AIS point density reflects transponder reporting cadence (which ranges from 2 seconds to 3 minutes under ITU-R M.1371) rather than true vessel presence. A maneuvering harbor tug generates 90 times more position points per hour than an anchored tanker.
* **Applying cubic power formulas without added resistance corrections:** Naive emissions models that estimate engine power solely from $u^3$ without modeling wave added resistance, ocean currents, and shallow-water bottom effects underestimate fuel consumption and emissions in rough weather by 15–35%.
* **Evaluating rare-event anomaly detection with ROC-AUC:** Because genuine maritime security anomalies represent less than $0.01\%$ of all observations, ROC-AUC yields misleadingly optimistic evaluations. Models must be audited using Precision-Recall curves and false positive rates per 1,000 operational tracking hours.
* **Failing to isolate multi-vessel MMSI collisions:** Multiple physical vessels broadcasting the identical default or duplicate MMSI generate impossible "ping-pong" jump tracks across oceans. Feeds must pass through MMSI trajectory disambiguation before feeding trajectory models.

---

## Key takeaways

* **AIS is an observational sample, not a complete census:** The presence of an AIS broadcast is conditioned on link-layer slot availability, RF propagation, and receiver footprint geometry; models must account for sampling bias.
* **Feature engineering requires kinematic derivatives and environmental context:** Effective models augment raw $(\phi, \lambda, u, \theta)$ coordinates with Great-Circle speed consistency, empirical rate of turn, curvature, bathymetric depth, and distance to legal boundaries.
* **Unsupervised route clustering extracts normal shipping corridors:** Density-based clustering (DBSCAN/HDBSCAN) and Gaussian Mixture Models (TREAD) map global fairways and establish statistical bounds for real-time route deviation alarms.
* **Deep generative models flag complex behavioral anomalies:** Variational Autoencoders and sequence-to-sequence LSTMs trained on historical normal traffic identify deceptive maneuvering and GNSS manipulation via trajectory reconstruction error.
* **Global fishing effort can be mapped from 1D kinematics:** Residual convolutional neural networks classify vessel gear types and point-wise fishing activity from resampled speed and heading sequences with over 90% accuracy.
* **High-seas transshipment is detectable via spatial-temporal co-occurrence:** Tandem drifting within 500 meters at speeds under 2 knots for over 3 hours exposes vessel encounters and catch transfers between fishing fleets and refrigerated reefers.
* **Multi-sensor fusion is required to unmask the dark fleet:** Fusing broadcast AIS with satellite Synthetic Aperture Radar (SAR) reveals that up to 75% of global industrial fishing vessels operate without active AIS.
* **Bottom-up emissions modeling couples AIS with naval architecture:** The STEAM methodology integrates instantaneous AIS speed profiles with hydrodynamic hull resistance to produce high-resolution carbon, sulfur, and nitrogen emissions inventories.
* **Whale strike lethality scales non-linearly with ship speed:** Empirical epidemiological modeling demonstrates that collision lethality exceeds 80% at speeds above 15 knots but falls below 20% under 8.6 knots, justifying coastal speed restrictions.
* **Tactical collision risk requires relative motion synthesis:** Synthesizing DCPA and TCPA into non-linear Collision Risk Indices (CRI) provides actionable early warning for VTS watchstanders and autonomous navigation systems.

---

## References

* Boerder, K., Miller, N. A., Worm, B. (2018). Global hot spots of transshipment of fish catch at sea. *Science Advances*, 4(7):eaat7159. doi:10.1126/sciadv.aat7159
* Conn, P. B., Silber, G. K. (2013). Vessel speed restrictions reduce risk of collision-related mortality for North Atlantic right whales. *Ecosphere*, 4(4):art43. doi:10.1890/ES13-00004.1
* Faber, J., Hanayama, S., Zhang, S., Pereda, P., Comer, B., Hauerhof, E., Schim van der Loeff, W., Smith, T., Zhang, Y., et al. (2020). *Fourth IMO GHG Study 2020*. London: International Maritime Organization.
* Harati-Mokhtari, A., Wall, A., Brooks, P., Wang, J. (2007). Automatic Identification System (AIS): Data reliability and human error implications. *The Journal of Navigation*, 60(3):373–389. doi:10.1017/S0373463307004298
* Imazu, H. (1983). Collision risk assessment model for ships. *Journal of Japan Institute of Navigation*, 70:71–79.
* IMO (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)*. Resolution MSC.74(69), Annex 3. London: International Maritime Organization.
* ITU-R (2026). *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Frequency Band*. Recommendation ITU-R M.1371-6. Geneva: International Telecommunication Union. https://www.itu.int/rec/R-REC-M.1371-6-202602-I/en
* Jalkanen, J.-P., Brink, A., Kalli, J., Pettersson, H., Kukkonen, J., Stipa, T. (2009). A modelling system for the exhaust emissions of marine traffic and its application in the Baltic Sea area. *Atmospheric Chemistry and Physics*, 9(23):9209–9223. doi:10.5194/acp-9-9209-2009
* Jalkanen, J.-P., Johansson, L., Kukkonen, J., Brink, A., Kalli, J., Stipa, T. (2012). Extension of an assessment model of ship traffic exhaust emissions for particulate matter and carbon monoxide. *Atmospheric Chemistry and Physics*, 12(5):2641–2659. doi:10.5194/acp-12-2641-2012
* Kroodsma, D. A., Mayorga, J., Hochberg, T., Miller, N. A., Boerder, K., Ferretti, F., Wilson, A., Bergman, B., White, T. D., Block, B. A., Woods, P., Sullivan, B., Costello, C., Worm, B. (2018). Tracking the global footprint of fisheries. *Science*, 359(6378):904–908. doi:10.1126/science.aao5646
* Miller, N. A., Roan, A., Hochberg, T., Amos, J., Kroodsma, D. A. (2018). Identifying global patterns of transshipment behavior. *Frontiers in Marine Science*, 5:240. doi:10.3389/fmars.2018.00240
* NGA (2025). *World Port Index*. Publication 150, 31st Edition. Springfield, VA: National Geospatial-Intelligence Agency.
* Pallotta, G., Vespe, M., Bryan, K. (2013). Vessel pattern knowledge discovery from AIS data: A framework for anomaly detection and route prediction. *Entropy*, 15(6):2218–2245. doi:10.3390/e15062218
* Paolo, F. S., Kroodsma, D., Raynor, J., Hochberg, T., Davis, P., Cleary, J., Marsaglia, L., Orofino, S., Thomas, C., Halpin, P. N. (2024). Satellite mapping reveals extensive industrial activity at sea. *Nature*, 625:85–91. doi:10.1038/s41586-023-06825-8
* Riveiro, M., Pallotta, G., Vespe, M. (2018). Maritime anomaly detection: A review. *Wiley Interdisciplinary Reviews: Data Mining and Knowledge Discovery*, 8(5):e1266. doi:10.1002/widm.1266
* Ross, D. (1976). *Mechanics of Underwater Noise*. New York: Pergamon Press.
* Tu, E., Zhang, G., Rachmawati, L., Rajabally, E., Huang, G.-B. (2018). Exploiting AIS data for intelligent maritime navigation: A comprehensive survey from data to methodology. *IEEE Transactions on Intelligent Transportation Systems*, 19(5):1559–1582. doi:10.1109/TITS.2017.2724494
* Vanderlaan, A. S., Taggart, C. T. (2007). Vessel collisions with whales: The probability of lethal injury based on vessel speed. *Marine Mammal Science*, 23(1):144–156. doi:10.1111/j.1748-7692.2006.00098.x
* Welch, H., Clavelle, T., White, T. D., Cimino, M. A., Van Osdel, J., Hochberg, T., Kroodsma, D., Hazen, E. L. (2022). Hot spots of unseen fishing vessels. *Science Advances*, 8(44):eabq2109. doi:10.1126/sciadv.abq2109
