# Chapter 45 — Software for processing decoded AIS

> **Part VII — Decoding, software, and data engineering.** An architectural and operational survey of the open-source libraries, geospatial databases, analytical engines, enterprise maritime systems, and 3D visualization tools that transform raw decoded Automatic Identification System telemetry into structured spatio-temporal trajectories and maritime domain intelligence.

**In this chapter.** You will learn how to build and evaluate end-to-end data processing pipelines for decoded Automatic Identification System (**AIS**) telemetry. We survey the open-source scientific Python ecosystem—spanning `pandas`, `GeoPandas`, `MovingPandas`, `Trackintel`, and `scikit-mobility`—and examine relational and analytical spatial databases including PostGIS, DuckDB Spatial, Apache Sedona, and GeoMesa. You will evaluate high-density visualization frameworks including `kepler.gl`, `deck.gl`, and discrete global grid systems (**H3** and **S2**), alongside the open-source chartplotter OpenCPN and global routing engines. We then analyze commercial and industrial Vessel Traffic Services (**VTS**) systems, including GateHouse Maritime, Kongsberg Norcontrol, and Wärtsilä Navi-Harbour. Finally, you will master the mechanics of using the 3D Digital Content Creation tool Blender and its Python `bpy` API for incident reconstruction, bridge-perspective line-of-sight visibility analysis, and satellite sensor footprint animation, navigating local coordinate transformations and temporal interpolation pitfalls.

## 45.1 From decoded records to spatial intelligence

Decoding an AIS radio transmission—whether performed by hardware transponders or software-defined radio pipelines such as `AIS-catcher` or `libais` as explored in [Chapter 44](ch44-open-source-decoders-history.md)—yields discrete, timestamped telemetry records. A raw NMEA 0183 `!AIVDM` sentence is converted into structured attributes: a Maritime Mobile Service Identity (**MMSI**), navigation status, Rate of Turn (**ROT**), Speed Over Ground (**SOG**), Course Over Ground (**COG**), True Heading, geographic coordinates (latitude and longitude), and static vessel dimensions.

However, isolated position reports do not constitute maritime intelligence. A raw stream of decoded AIS messages presents severe architectural and analytical challenges:
1. **Unordered and interleaved streams:** Messages arrive out of chronological order from disparate terrestrial base stations, satellite downlinks, and crowdsourced internet protocol relays, often with duplicate payloads received by overlapping shore stations as examined in [Chapter 41](ch41-networks-and-providers.md).
2. **Variable temporal cadence:** Class A commercial vessels transmit dynamic position reports (Messages 1, 2, and 3) at intervals between 2 seconds and 3 minutes depending on speed and navigational status, while Class B craft transmit every 30 seconds down to 3 minutes under Carrier-Sense or Self-Organizing Time Division Multiple Access (**CSTDMA** or **SOTDMA**), as detailed in [Chapter 20](ch20-architecture-and-station-classes.md) and [Chapter 21](ch21-link-layer-tdma.md). Static voyage parameters (Message 5) arrive only every 6 minutes or upon request.
3. **Sensor noise and telemetry corruption:** Decoded records frequently contain invalid coordinates (such as default $+91^\circ$ latitude or $+181^\circ$ longitude sentinels), impossible speed spikes induced by multi-path Global Navigation Satellite System (**GNSS**) errors, and corrupted or default MMSIs, as explored in [Chapter 36](ch36-failure-modes.md).
4. **Relational detachment:** Positional telemetry is decoupled from vessel metadata, requiring stateful joins between high-frequency dynamic messages (Messages 1, 2, 3, 18, 19, 27) and low-frequency static messages (Messages 5, 24A, 24B).

Transforming these discrete packets into navigable trajectories requires specialized data processing software. Downstream applications—such as calculating vessel density grids in [Chapter 48](ch48-spatial-statistics.md), training machine learning behavior models in [Chapter 49](ch49-analytics-and-ml.md), or reconstructing maritime collisions for Admiralty courts in [Chapter 55](ch55-incidents-and-accidents.md) and [Chapter 56](ch56-vdr-forensics.md)—rely on a layered software stack spanning tabular manipulation, trajectory modeling, spatial database indexing, high-performance distributed computing, and multi-dimensional visualization.

```
+-----------------------------------------------------------------------------------+
|                        DOWNSTREAM APPLICATION LAYER                               |
|   Admiralty Court Reconstruction  |   Fisheries IUU & Dark Fleet Detection        |
|   VTS Port Operations & Safety    |   Global Trade & Economic Nowcasting          |
+-----------------------------------------------------------------------------------+
                                          ▲
                                          │
+-----------------------------------------------------------------------------------+
|                     VISUALIZATION & RECONSTRUCTION STACK                         |
|   Desktop Charting: OpenCPN (S-57/S-63) | WebGL: deck.gl, kepler.gl, CesiumJS     |
|   3D Physical DCC: Blender (bpy, Geometry Nodes, BlenderGIS, local tangent plane) |
+-----------------------------------------------------------------------------------+
                                          ▲
                                          │
+-----------------------------------------------------------------------------------+
|                    SPATIAL DATABASE & BIG DATA ENGINE LAYER                       |
|   Relational GIS: PostGIS (GEOS, GiST)   | Embedded OLAP: DuckDB Spatial (RTRee)  |
|   Distributed Engines: Apache Sedona     | Discrete Global Grids: Uber H3, S2     |
+-----------------------------------------------------------------------------------+
                                          ▲
                                          │
+-----------------------------------------------------------------------------------+
|                    TRAJECTORY & SPATIAL DATA SCIENCE LAYER                        |
|   Tabular Core: pandas, PyArrow          | Vector Geometry: GeoPandas, Shapely    |
|   Kinematic Trajectories: MovingPandas   | Mobility Science: scikit-mobility      |
+-----------------------------------------------------------------------------------+
                                          ▲
                                          │
+-----------------------------------------------------------------------------------+
|                      DECODING & DATA CLEANING INGEST LAYER                        |
|   NMEA Ingest: pyais, libais, AIS-catcher | Kinematic Filters, Deduplication      |
+-----------------------------------------------------------------------------------+
```

## 45.2 The open-source data science stack

The scientific Python ecosystem provides the foundational tools for batch analysis, exploratory data science, and academic research on historical AIS archives.

### 45.2.1 Tabular foundations: pandas, Apache Arrow, and GeoPandas

At the base of the modern data science pipeline sits `pandas` and `Apache Arrow` (via `pyarrow`). Decoded AIS records map naturally into columnar data frames, where rows represent individual position or static reports and columns capture discrete message fields. Arrow-backed columnar storage provides high compression ratios and zero-copy memory transfers, essential when processing billion-row archives released by agencies such as the US Marine Cadastre or the Danish Maritime Authority (**DMA**).

Vector geometries are handled by `GeoPandas`, which extends pandas data frames with geospatial capabilities. `GeoPandas` delegates spatial geometry calculations to `Shapely`, which wraps the C++ Geometry Engine, Open Source (**GEOS**) library. A typical AIS ingestion pipeline converts longitude and latitude coordinates into point geometries, assigning the standard World Geodetic System 1984 coordinate reference system (**CRS**), designated as European Petroleum Survey Group code **EPSG:4326**:

```python
import geopandas as gpd

gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df["lon"], df["lat"]),
    crs="EPSG:4326"
)
```

While `GeoPandas` excels at static spatial operations—such as spatial joins against Marine Protected Areas (**MPAs**), Traffic Separation Schemes (**TSS**), or Exclusive Economic Zones (**EEZs**)—it treats every row as an independent spatial entity. It has no native understanding of the temporal continuity, vessel kinematics, or movement topology that define maritime voyages.

### 45.2.2 Movement data analysis: MovingPandas, Trackintel, and scikit-mobility

To model vessels as continuous spatio-temporal entities, researchers employ specialized trajectory analysis libraries:

- **MovingPandas:** Authored by Anita Graser (Graser 2019), `MovingPandas` integrates `GeoPandas` with temporal indexing to construct `Trajectory` and `TrajectoryCollection` objects. In `MovingPandas`, a trajectory consists of a time-ordered series of spatial geometries associated with an identifier (such as an MMSI or voyage ID). The library provides built-in methods for:
  - Kinematic derivation: computing segment speeds, headings, and accelerations from consecutive coordinates.
  - Trajectory cleaning and smoothing: Kalman filtering and Douglas–Peucker generalization.
  - Spatio-temporal segmentation: splitting continuous vessel pings into distinct voyages based on observation gaps (such as a 4-hour silence) or detected port stops.
  - Stop detection: identifying anchorages and terminal berthing using spatial bounding thresholds and dwell-time duration gates.
- **Trackintel:** Originally designed for human mobility, `Trackintel` provides structured data models for positions, staypoints, and triplegs. In maritime analytics, staypoints correspond to anchorage dwells, lightering operations, or dockside cargo loading, while triplegs represent active transit legs.
- **scikit-mobility:** Developed for statistical mobility physics, `scikit-mobility` provides tools for measuring collective flow, radius of gyration, and trajectory simulation. While less focused on maritime navigational physics than `MovingPandas`, it is widely used in macro-level transportation studies and trade flow modeling, such as those conducted by the International Monetary Fund (Cerdeiro et al. 2020).

> **Try it.** **Ingesting raw NMEA, cleaning kinematics, and extracting trajectories with MovingPandas.**
> Run this automated pipeline against the repository sample dataset using the provided virtual environment:
> ```bash
> . /usr/local/google/home/schwehr/sdd-books/ais/fable/.venv/bin/activate
> python code/analytics/moving_pandas_pipeline.py data/samples/synthetic_harbor.nmea
> ```
> Expected output:
> ```text
> cleaning report: {'position_reports': 1491, 'after_mmsi_filter_and_dedupe_and_speed': 1343, 'dropped': 148, 'vessels': 6}
> 6 trajectories
>   mmsi=244999703 fixes=126 length_km=26.5 start=12:00:46 end=12:59:56 mean_sog_reported=14.5 kn mean_speed_derived=14.5 kn
>   mmsi=316999704 fixes=301 length_km=37.1 start=12:00:09 end=12:59:59 mean_sog_reported=20.0 kn mean_speed_derived=20.1 kn
>   mmsi=338123456 fixes=121 length_km=11.1 start=12:00:00 end=13:00:00 mean_sog_reported=6.0 kn mean_speed_derived=6.0 kn
>   mmsi=338654321 fixes=120 length_km=13.8 start=12:00:20 end=12:59:50 mean_sog_reported=7.5 kn mean_speed_derived=7.5 kn
>   mmsi=338999702 fixes=349 length_km=33.3 start=12:00:03 end=12:59:43 mean_sog_reported=18.0 kn mean_speed_derived=18.1 kn
>   mmsi=366999701 fixes=326 length_km=22.3 start=12:00:00 end=13:00:00 mean_sog_reported=12.0 kn mean_speed_derived=12.0 kn
> 0 stops (>=5 min within 200 m)
> ```

## 45.3 Spatial databases and big-data engines

When AIS datasets scale beyond single-node system memory—exceeding tens of millions of records—in-memory Python dataframes become impractical. Production data engineering environments rely on spatial databases and distributed big-data engines.

### 45.3.1 Relational spatial engines: PostgreSQL and PostGIS

For two decades, the combination of PostgreSQL and its spatial extension **PostGIS** (PostGIS 2001) has served as the gold standard for relational maritime data storage. PostGIS introduces Open Geospatial Consortium (**OGC**) compliant geometric and geographic types.

In maritime pipelines, two spatial types predominate:
- `GEOMETRY`: Represents planar Euclidean coordinates. For local harbor analyses, planar geometry projected into a local Universal Transverse Mercator (**UTM**) zone allows fast cartesian calculations.
- `GEOGRAPHY`: Computes distances, azimuths, and intersections directly across the WGS 84 ellipsoidal surface using Great Circle and geodetic algorithms. While computationally more expensive than planar geometry, it avoids projection distortion when tracking ocean-crossing container vessels.

PostGIS accelerates spatial queries using Generalized Search Tree (**GiST**) R-Tree indexes on the spatial bounding box:
```sql
CREATE INDEX idx_ais_geom ON ais_fixes USING GIST (geom);
CREATE INDEX idx_ais_mmsi_time ON ais_fixes (mmsi, t);
```
Furthermore, the `pgRouting` extension enables network-constrained vessel tracking along established navigational fairways and maritime canals.

### 45.3.2 Embedded analytical OLAP: DuckDB and DuckDB Spatial

For analytical processing on local workstations or single cloud instances, **DuckDB** (Raasveldt & Mühleisen 2019) has transformed maritime data workflows. As an embedded, columnar vectorized SQL execution engine, DuckDB can execute complex analytical queries directly against raw Parquet, CSV, or GeoParquet files without requiring an external database server daemon.

The `spatial` extension in DuckDB integrates GEOS-compatible spatial functions and provides native reading of spatial vector formats:
```sql
INSTALL spatial;
LOAD spatial;

SELECT 
    mmsi,
    ST_Point(lon, lat) AS geom,
    t
FROM read_parquet('ais_2026_*.parquet')
WHERE ST_Within(
    ST_Point(lon, lat), 
    ST_GeomFromGeoJSON('{"type":"Polygon", ...}')
);
```
Because DuckDB operates using vectorized execution kernels and multi-threaded parallel aggregation, computing spatial density bins or vessel transit counts across hundreds of millions of AIS rows executes in seconds rather than hours, bridging the gap between lightweight exploratory scripts and heavy distributed clusters.

### 45.3.3 Distributed big data: Apache Sedona and GeoMesa

When global AIS feeds reach petabyte scales—such as continuous multi-year archives maintained by Spire, ORBCOMM, or Global Fishing Watch (**GFW**)—distributed computing engines become mandatory:

- **Apache Sedona (formerly GeoSpark):** Developed by Jia Yu et al. (Yu, Zhang & Sarwat 2019), Apache Sedona extends Apache Spark and Apache Flink with distributed spatial resilient distributed datasets (**Spatial RDDs**) and Spatial DataFrames. Sedona distributes spatial partitioners (such as K-D Trees and Quadtrees) across compute clusters, enabling massively parallel spatial joins between global ship trajectories and multi-polygon regional boundaries.
- **GeoMesa:** Created by James Hughes et al. (Hughes et al. 2015), GeoMesa provides spatio-temporal indexing on top of distributed NoSQL databases such as Apache Accumulo, Apache HBase, and Google Cloud Bigtable. GeoMesa implements space-filling curves—specifically 3D Z-Order and Hilbert curves that interleave latitude, longitude, and epoch timestamp bits into a single composite key. This architecture allows constant-time range lookups across simultaneous spatio-temporal bounds (for example, "retrieve all vessels within a 50 km bounding box during a 30-minute window").

### 45.3.4 Discrete global grid systems: H3 and S2

An increasingly prevalent alternative to traditional polygonal spatial boundaries is the use of **Discrete Global Grid Systems (DGGS)**, notably Uber's **H3** and Google's **S2**:

- **Uber H3:** H3 partitions the surface of the Earth into hierarchical hexagonal cells. Hexagons exhibit a critical topological property: every neighboring cell is equidistant, eliminating the diagonal distance distortions inherent in square Cartesian grids. Hexagonal binning is ideal for vessel traffic density mapping, marine noise modeling, and spatial aggregation, preventing visual and mathematical artifacting around grid corners.
- **Google S2:** S2 projects the Earth's sphere onto the six faces of an enclosing cube and maps those faces to a 1D sequence using a Hilbert space-filling curve. S2 cells are quadrilateral and hierarchically nested down to sub-centimeter resolutions (level 30). Because S2 cells map directly to 64-bit integers, spatial proximity queries, range queries, and bounding-box coverages reduce to high-speed integer range comparisons.

```
Cartesian Grid (Square)               Hexagonal Grid (H3)
+---------+---------+                 / \     / \
|         |         |                /   \___/   \
| (x-1,y) |  (x,y)  |               |  A  |  B  |
|         |         |               \     / \   /
+---------+---------+                \___/ C \_/
| Diagonal distance |                    \   /
| is sqrt(2)*d      |                     \_/
+-------------------+               All adjacent centers equidistant (d)
```

## 45.4 Visualization and maritime routing

AIS data visualization spans three distinct operational domains: navigational chartplotting aboard ship bridges, web-based analytical dashboards, and global maritime routing engines.

### 45.4.1 Desktop and bridge chartplotting: OpenCPN

For real-time navigational awareness and vessel tracking, **OpenCPN** (OpenCPN 2010) is the preeminent open-source Electronic Chart System (**ECS**). Created by David Register, OpenCPN runs across Linux, Windows, macOS, and ARM platforms (such as the Raspberry Pi).

OpenCPN ingests live NMEA 0183 and NMEA 2000 data streams over serial interfaces, USB virtual COM ports, and UDP/TCP network sockets. It renders official Electronic Navigational Charts (**ENCs**) adhering to the International Hydrographic Organization (**IHO**) S-57 and S-63 standards, as well as raster nautical charts (**RNCs**). For AIS processing, OpenCPN implements the symbol standards codified in **IEC 62288**:
- **Target symbology:** Vessels appear as isosceles triangles oriented according to their True Heading (when available) or Course Over Ground.
- **Dynamic motion vectors:** Predictor lines project a vessel's future position based on its current SOG and COG over a user-selected time interval (e.g., 6 or 12 minutes).
- **Collision avoidance computation:** The OpenCPN tracking engine continuously evaluates all active targets to compute Closest Point of Approach (**CPA**) and Time to Closest Point of Approach (**TCPA**), triggering visual and audible alarms when target vectors violate safety envelopes.

### 45.4.2 Web-based geospatial visualization: deck.gl and kepler.gl

For web browser visualization of massive historical datasets, traditional Document Object Model (**DOM**) mapping engines such as Leaflet or OpenLayers fail due to CPU rendering bottlenecks when rendering more than a few thousand points.

Modern maritime web dashboards leverage hardware-accelerated WebGL and WebGPU frameworks:
- **deck.gl:** An open-source framework developed by Uber and maintained under the Linux Foundation. `deck.gl` executes data transformation and rendering shaders directly on the client Graphical Processing Unit (**GPU**). Using specialized layers—such as the `TripsLayer`, `PathLayer`, and `H3HexagonLayer`—`deck.gl` can animate millions of dynamic vessel trajectories simultaneously at 60 frames per second.
- **kepler.gl:** Built on top of `deck.gl`, `kepler.gl` provides an interactive desktop and browser UI for geospatial data exploration. Analysts can drag and drop multi-gigabyte CSV or GeoJSON files, apply temporal playback filters, render heatmaps, and aggregate traffic density without writing frontend software.

### 45.4.3 Global maritime routing: searoute

When vessel trajectories exhibit long data gaps—such as transoceanic voyages where terrestrial coverage ends and satellite updates are sparse—analysts require realistic maritime routing engines. The open-source `searoute` library calculates shortest maritime paths between ports or waypoints. Unlike terrestrial routing engines (such as Open Source Routing Machine / OSRM) that traverse road networks, `searoute` routes vessels across an open maritime network mesh that honors nautical chokepoints (Panama Canal, Suez Canal, Strait of Malacca, English Channel) while avoiding shallow waters and land masses.

## 45.5 Enterprise and commercial VTS systems

While open-source tools dominate academic research and data engineering pipelines, commercial port operations, coastal coast guards, and national maritime administrations rely on proprietary, highly certified **Vessel Traffic Services (VTS)** platforms.

These commercial platforms are engineered to satisfy stringent operational availability requirements (often exceeding 99.999% uptime), support real-time sensor fusion with X-band and S-band coastal surveillance radars, and comply with standards established by the International Association of Marine Aids to Navigation and Lighthouse Authorities (**IALA**) under Recommendation **IALA V-128**:

- **GateHouse Maritime (AIS Server):** Headquartered in Denmark, GateHouse Maritime provides high-capacity AIS server software designed for national coastal administrations and satellite operators. The GateHouse platform ingests thousands of simultaneous base station feeds, filters duplicate transmissions in real time, validates payload checksums, and distributes normalized telemetry to downstream subscribers via standard protocols.
- **Kongsberg Norcontrol:** A foundational pioneer in maritime surveillance, Kongsberg Norcontrol's C-Scope VTS platform is deployed across major global shipping waterways. C-Scope integrates multi-sensor tracking, combining AIS reports with primary radar plots, electro-optical camera trackers, and VHF radio direction finders (**RDF**) to maintain verified situational awareness even when vessels fail to broadcast AIS.
- **Saab TransponderTech (Vessel Traffic Management and Information Systems / VTMIS):** Saab provides integrated maritime security platforms that link Class A transponder networks with shore-based coastal surveillance networks and automated port management systems.
- **SRT Marine Systems (GeoVS):** SRT manufactures marine transponder hardware and develops coastal surveillance software. Its GeoVS platform provides an interactive 3D virtual environment for maritime operators, rendering real-time ship models, terrain elevation, bathymetry, and radar overlays.
- **Wärtsilä Navi-Harbour (formerly Transas):** One of the most widely installed VTS platforms in the world, Wärtsilä's Navi-Harbour suite integrates harbor radar processing, AIS target association, automatic collision warning, and electronic navigational chart displays conforming to IEC 61174 ECDIS standards.

```
+------------------------------------+--------------------------+-----------------------+---------------------------------------+
| Software System                    | Primary Architectural Role | Source / Licensing   | Primary Operational Target            |
+------------------------------------+--------------------------+-----------------------+---------------------------------------+
| MovingPandas                       | Kinematic Trajectory Sci | Open Source (BSD-3)   | Academic Research, Spatial Analytics  |
| PostGIS                            | Relational Spatial DB    | Open Source (GPL-2)   | Enterprise Relational Warehousing     |
| DuckDB Spatial                     | Embedded Vectorized OLAP | Open Source (MIT)     | High-Speed Columnar Analytics         |
| Apache Sedona                      | Distributed Cluster RDD  | Open Source (Apache-2)| Multi-Node Big Data Ingest            |
| OpenCPN                            | Marine ECS Navigation    | Open Source (GPL-2)   | Vessel Bridge Navigation, Charting    |
| Blender (bpy)                      | 3D DCC & Kinematic Anim  | Open Source (GPL-2)   | Collision Forensics, Bridge Visuals   |
| GateHouse Maritime                 | Coastal Data Aggregation | Proprietary           | National Ingest, Satellite Processing |
| Kongsberg Norcontrol (C-Scope)     | Multi-Sensor VTS Display | Proprietary           | Port Authorities, Coastal Defense     |
| Wärtsilä Navi-Harbour              | Industrial VTMIS Server  | Proprietary           | Deep-Water Ports, Fairway Control     |
+------------------------------------+--------------------------+-----------------------+---------------------------------------+
```

## 45.6 3D visualization and incident animation with Blender

In maritime analytics, 2D planar maps frequently fail to capture the physical reality of maritime operations. When investigating a fatal collision, evaluating whether a bridge watchkeeper could visually detect an approaching craft, or analyzing satellite sensor coverage, analysts require a **3D Digital Content Creation (DCC)** environment.

**Blender**—originally released as an in-house tool in 1994 and open-sourced under GPL-2.0 in 2002—has emerged as a powerful engine in the maritime analyst's computational toolbox.

```
CSV / GeoParquet Trajectories
          │
          ▼
Local Tangent Plane Projection (to_local: WGS 84 -> Metres)
          │
          ▼
Blender Python (bpy) Headless Execution
   ├── Dimension Extraction (Msg 5: Length, Beam, draught)
   ├── Dynamic Heading vs COG Orientation (Euler Yaw)
   ├── Temporal Keyframing (Linear Interpolation)
   └── Geometry Nodes / Procedural Hull Proxy Generation
          │
          ▼
Render Output: Evidentiary Video, Bridge Sightlines, glTF Models
```

### 45.6.1 Why a 3D DCC belongs in an AIS toolbox

A complete maritime analysis often demands tools beyond standard Geographic Information Systems (**GIS**):
1. **Admiralty incident reconstruction:** Planar chart replays cannot convey relative vessel scale, blind arcs caused by deck cargo, or physical hull attitudes during dynamic maneuvering. Blender allows analysts to reconstruct multi-vessel encounters with physically scaled vessel hulls, accurate lighting conditions, and dynamic water surfaces.
2. **Bridge-view sightline analysis:** In maritime collision investigations (such as those conducted by the UK Marine Accident Investigation Branch / MAIB or the US National Transportation Safety Board / NTSB), courts must establish what was visually discernible from a bridge wing. By placing a virtual camera at the exact coordinates of the bridge wheelhouse, an investigator can render the watchkeeper's view, accounting for physical sightline obstructions created by container stacks, cranes, or ship superstructure.
3. **Sensor shadow and RF radar blockage:** AIS and radar antennas mounted aboard modern commercial vessels experience signal attenuation and physical shadowing caused by masts, funnels, and deck machinery, as explored in [Chapter 31](ch31-noise-and-interference.md) and [Chapter 32](ch32-antennas.md). In Blender, ray-tracing engines (such as Cycles) can simulate line-of-sight RF coverage and blind zones.
4. **Satellite footprint and orbital pass animation:** As detailed in [Chapter 39](ch39-satellite-ais.md), Low Earth Orbit (**LEO**) AIS satellites sweep circular footprints roughly 5,000 km in diameter across the globe. Blender can animate orbital mechanics, antenna footprints, and message collision zones for technical demonstrations and educational presentations.
5. **Open standard 3D export:** Blender can export animated scenes to standard formats such as **glTF 2.0**, allowing 3D animated trajectories to be rendered interactively inside web browsers via CesiumJS or Three.js.

### 45.6.2 The bpy Python API and Geometry Nodes

Blender features a complete, headless Python API exposed through the `bpy` module. This architecture allows developers to script the automated generation of 3D maritime animations directly from data processing pipelines without launching the graphical user interface.

An automated pipeline parses cleaned trajectory tables, instantiates vessel proxies, configures keyframes along the animation timeline, and assigns interpolation modes. For large fleets with thousands of simultaneous vessels, creating individual mesh objects can exhaust memory; modern pipelines leverage **Geometry Nodes**, instancing procedural hull proxies across point clouds driven by attribute buffers.

### 45.6.3 Spatial coordinate precision: Blender is not a GIS

A critical caveat governs all 3D DCC tools: **Blender is not a GIS**. 

Internally, Blender's graphics engine, viewport, and physics solvers execute using **single-precision 32-bit floating-point arithmetic (`float32`)**. Single-precision IEEE 754 floats provide only 24 bits of mantissa, yielding approximately 7 decimal digits of precision.

If a developer directly feeds global geographic coordinates into Blender:
- A longitude coordinate such as $-70.648189^\circ$ or UTM northing of $4,680,000\text{ m}$ consumes all available mantissa bits.
- At global coordinates, the spatial distance between representable floating-point numbers expands to tens of centimeters or even meters.
- This creates severe visual jitter, vertex tearing, matrix transformation instability, and camera clipping failures.

To preserve sub-millimeter precision, the processing software must project spherical coordinates into a **local tangent plane** (such as an equirectangular or East-North-Up / ENU projection) anchored at the mean center $(\text{lat}_0, \text{lon}_0)$ of the operational scene:

$$\Delta x = R \cdot (\lambda - \lambda_0) \cdot \cos(\phi_0) \cdot \frac{\pi}{180^\circ}$$

$$\Delta y = R \cdot (\phi - \phi_0) \cdot \frac{\pi}{180^\circ}$$

where $R = 6,371,000\text{ m}$ is the mean Earth radius, $\phi$ is latitude, and $\lambda$ is longitude. Within an operational harbor area of $100\text{ km} \times 100\text{ km}$, coordinate magnitudes remain below $50,000\text{ m}$, maintaining sub-millimeter geometric precision within the 32-bit floating-point budget.

### 45.6.4 Hull proxy scaling and orientation mechanics

To generate an accurate reconstruction, proxy 3D models must be correctly dimensioned and oriented:
- **Hull dimensioning:** Static AIS reports (Message 5 and Message 24B) broadcast four dimensional parameters: distance from the GNSS antenna reference point to the bow ($A$), to the stern ($B$), to the port side ($C$), and to the starboard side ($D$). Total vessel length is $A + B$, total beam is $C + D$, and the geometric center is offset from the GNSS antenna position. Software must scale the 3D proxy to these exact dimensions rather than applying arbitrary generic ship meshes.
- **Orientation mechanics:** In Blender's coordinate system, the $+X$ axis typically points East, $+Y$ points North, and $+Z$ points Up. Navigational azimuths (Heading and COG) are measured clockwise from True North ($0^\circ$). When converting maritime heading $\theta_{\text{nav}}$ to a mathematical counter-clockwise Euler rotation $\theta_{\text{euler}}$ around the $Z$-axis:

$$\theta_{\text{euler}} = 90^\circ - \theta_{\text{nav}}$$

Software must strictly evaluate the validity of True Heading. As codified in ITU-R M.1371, if a vessel lacks an operational gyrocompass or transmitting heading device, the heading field broadcasts sentinel `511` ("not available"). When heading is `511`, the pipeline must fall back to Course Over Ground (COG). Failing to implement this fallback rotates the ship hull to $90^\circ - 511^\circ = -421^\circ \equiv 299^\circ$, corrupting the visual reconstruction.

### 45.6.5 Temporal interpolation: the Bézier overshoot hazard

When keyframing vessel positions across time, 3D animation packages default to cubic **Bézier spline interpolation** to ensure smooth graphical transitions. 

In maritime reconstruction, Bézier interpolation introduces dangerous physical artifacts. Class A vessels transmitting every few seconds have sufficient ping density to constrain spline curvature. However, Class B craft or vessels undergoing intermittent radio shadowing may experience gaps of 3 to 10 minutes between reports. 

If a vessel alters course during a 5-minute telemetry gap, a cubic Bézier curve will "overshoot" the waypoint, swinging the vessel hull through impossible lateral excursions or causing it to visually slice through shoals, piers, or other vessels. Maritime visualization software must explicitly force **linear interpolation** (`LINEAR`) on all translation and rotation f-curves between discrete AIS observations.

> **Try it.** **Headless 3D trajectory reconstruction with Blender.**
> Using the headless script in `code/viz/blender_ais_animation.py`, inspect the track ingestion logic and verify scene parameters:
> ```bash
> . /usr/local/google/home/schwehr/sdd-books/ais/fable/.venv/bin/activate
> python code/viz/blender_ais_animation.py --csv data/samples/synthetic_harbor_truth.csv
> ```
> Expected output:
> ```text
> bpy not available — run inside Blender. Parsed 8 tracks; origin (42.29832586015538, -70.64818942286348)
> ```
> *(When executed in an environment with Blender installed via `blender --background --python code/viz/blender_ais_animation.py -- --csv data/samples/synthetic_harbor_truth.csv --out /tmp/harbor.blend`, the script compiles a complete 3D animated scene with linear keyframe interpolation).*

## Then & now

- ⟨H⟩ **1994 (Blender initial release):** Blender was developed by NeoGeo and Not a Number (NaN) as an in-house 3D animation suite, while maritime tracking was confined to dedicated coastal radar installations.
- ⟨H⟩ **2001 (PostGIS initial release):** Paul Ramsey and Refractions Research released PostGIS, establishing spatial object extensions and R-Tree indexing for PostgreSQL under GPL-2.0.
- ⟨H⟩ **2002 (Blender open-sourced & QGIS released):** Following the "Free Blender" crowdfunding campaign, Blender was released under the GNU General Public License; Gary Sherman began development of QGIS, enabling open-source desktop visualization of maritime spatial vectors.
- ⟨+⟩ **2007 (Harati-Mokhtari baseline):** Abbas Harati-Mokhtari and colleagues published the first comprehensive empirical study of AIS data quality, demonstrating that over 8% of operational fields contained severe errors, spurring the development of programmatic cleaning software.
- ⟨+⟩ **2010 (OpenCPN v2.1.0 on GitHub):** David Register published OpenCPN to GitHub, standardizing open-source NMEA 0183/2000 target tracking, CPA/TCPA collision alarms, and ENC chart display for recreational and commercial navigators.
- ⟨H⟩ **2013-06 (GeoPandas first commit):** Kelsey Jordahl initiated GeoPandas, bridging pandas dataframes with Shapely geometry objects and establishing the standard Python vector GIS environment.
- ⟨H⟩ **2015-04 (Apache Sedona / GeoSpark first commit):** Jia Yu created GeoSpark (later Apache Sedona), introducing spatial cluster computing and distributed spatial RDDs to process massive trajectory archives.
- ⟨H⟩ **2016-01 (deck.gl started):** Uber open-sourced deck.gl, utilizing WebGL GPU shader pipelines to render hundreds of thousands of dynamic vessel trajectories in web browsers at 60 fps.
- ⟨H⟩ **2018-07 (DuckDB first commit):** Hannes Mühleisen and Mark Raasveldt initiated DuckDB, creating an embedded vectorized columnar SQL engine capable of processing multi-gigabyte maritime Parquet archives on desktop workstations.
- ⟨H⟩ **2018-12 (MovingPandas first commit):** Anita Graser released MovingPandas, integrating GeoPandas with temporal trajectory modeling, kinematic stop detection, and spatio-temporal segmentation.
- ⟨H⟩ **2021 (GeoParquet specification):** The Open Geospatial Consortium initiated the GeoParquet specification, establishing an open columnar standard for storing vessel geometries and temporal attributes with high compression.

## Validation, uncertainty & data quality

Downstream processing software inherits every physical imperfection, transmission dropout, and human configuration error present on the VHF Data Link. If software accepts decoded AIS telemetry uncritically, downstream analytics—ranging from port congestion metrics to collision liability determinations—will be fundamentally flawed.

### 45.6.1 Systematic error propagation in trajectory analysis

Errors in AIS data processing propagate across three distinct operational layers:
1. **Geometric coordinate errors:** Telemetry packets broadcasting invalid coordinate sentinels ($+91^\circ$ lat, $+181^\circ$ lon), null coordinates ($0.0^\circ, 0.0^\circ$ off the coast of Ghana), or single-bit position flips create dramatic spatial jumps. In kinematic libraries such as `MovingPandas`, an unhandled coordinate jump spanning several hundred miles over a 10-second interval results in derived speed calculations exceeding thousands of knots, corrupting mean voyage statistics.
2. **Kinematic sentinel mishandling:** As codified in ITU-R M.1371, specialized values indicate unavailable sensor data. True Heading broadcasts `511` when unavailable; Speed Over Ground broadcasts `1023` ($102.3\text{ kn}$); Course Over Ground broadcasts `3600` ($360.0^\circ$); and Rate of Turn broadcasts `-128`. If software parses these fields as literal numerical values rather than converting them to `null` or `NaN`, trajectory averages and vector calculations will be severely distorted.
3. **Temporal misalignment and reception jitter:** Decoded AIS streams contain two distinct timestamps: the message generation timestamp (which in Class A position reports is merely a 6-bit second counter, $0$–$59$) and the receiver ingest timestamp (often stamped in an NMEA 4.10 TAG block `\c:` parameter). Multipath propagation, network latency, and buffer queuing across crowdsourced internet aggregators cause packets to arrive out of order. Ingest software that sorts records by arrival timestamp rather than GNSS epoch time creates apparent temporal reversals, resulting in negative derived speeds.

```
+------------------------------------+--------------------------+-----------------------+---------------------------------------+
| Telemetry Field                    | Raw Protocol Sentinel    | Corrupted Value       | Recommended Software Cleaning Action  |
+------------------------------------+--------------------------+-----------------------+---------------------------------------+
| Latitude                           | 91.0° (0x1A83854)        | 91.0° (Planar Error)  | Drop record if abs(lat) > 90.0°       |
| Longitude                          | 181.0° (0x3567E00)       | 181.0° (Planar Error) | Drop record if abs(lon) > 180.0°      |
| True Heading                       | 511 (0x1FF)              | 511° (Invalid Angle)  | Coerce to NaN; fall back to COG       |
| Speed Over Ground (SOG)            | 102.3 kn (1023)          | 102.3 kn              | Coerce to NaN; filter if speed > 60 kn|
| Course Over Ground (COG)            | 360.0° (3600)            | 360.0° (Invalid Angle)| Coerce to NaN                         |
| Rate of Turn (ROT)                 | -128 (0x80)              | -128 (Math Overflow)  | Coerce to NaN (indicates no turn info)|
| MMSI Identifier                    | 0, 1193046, 123456789    | Shared Collision ID   | Quarantine from individual tracks     |
+------------------------------------+--------------------------+-----------------------+---------------------------------------+
```

### 45.6.2 Concrete validation procedure: the kinematic gate

To ensure data integrity, every processing pipeline must enforce a strict **kinematic validation gate** before passing telemetry to trajectory or database models.

The validation procedure executes in five discrete stages:
1. **Static identity filtering:** Eliminate records broadcasting known default, test, or invalid MMSIs ($\text{MMSI} \in \{0, 111111111, 123456789, 999999999\}$ or the infamous Swedish test sentinel $1193046$).
2. **Spatial boundary validation:** Verify that $-90.0^\circ \le \text{lat} \le 90.0^\circ$ and $-180.0^\circ \le \text{lon} \le 180.0^\circ$. Exclude exact null coordinates $(0.0, 0.0)$ unless legitimate operations in the Gulf of Guinea are being deliberately monitored.
3. **Temporal deduplication:** Group records by MMSI and sort chronologically by GNSS receiver timestamp. Drop duplicate records where consecutive fixes share identical timestamps and coordinates.
4. **Great Circle distance computation:** For consecutive reports $(p_1, t_1)$ and $(p_2, t_2)$ from the same MMSI, compute the ellipsoidal or Great Circle distance $d$ using the Haversine formula:

$$a = \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)$$

$$d = 2 R \arcsin\left(\sqrt{a}\right)$$

5. **Implied kinematic speed gating:** Calculate the implied speed over ground $v_{\text{implied}} = \frac{d}{t_2 - t_1}$. If $v_{\text{implied}}$ exceeds a physically defensible threshold for commercial shipping (typically $60\text{ kn}$ for conventional merchant vessels, or $100\text{ kn}$ if including high-speed passenger catamarans), flag $p_2$ as a spatial outlier and discard it from the trajectory.

### 45.6.3 Worked example: detecting a GNSS multipath jump

Consider a container vessel ($\text{MMSI } 366999701$) underway along a coastal approach, reporting consecutive Class A position reports across a terrestrial base station:

- **Fix 1 ($p_1$):** Timestamp $t_1 = 12:00:00$, Latitude $\phi_1 = 42.20000^\circ\text{ N}$, Longitude $\lambda_1 = -70.60000^\circ\text{ W}$, Reported $\text{SOG} = 12.0\text{ kn}$.
- **Fix 2 ($p_2$):** Timestamp $t_2 = 12:00:10$, Latitude $\phi_2 = 42.24000^\circ\text{ N}$, Longitude $\lambda_2 = -70.60000^\circ\text{ W}$, Reported $\text{SOG} = 12.1\text{ kn}$.

The elapsed time between fixes is:
$$\Delta t = 10\text{ seconds} = \frac{10}{3600}\text{ hours} \approx 0.002778\text{ h}$$

The vessel's reported latitude shifted by $\Delta \phi = 0.04000^\circ$, while longitude remained constant. One degree of latitude equals approximately $60\text{ nautical miles}$ ($111.12\text{ km}$). The distance traveled is:
$$d = 0.04000^\circ \times 60\frac{\text{nmi}}{\text{deg}} = 2.40\text{ nmi} \approx 4.445\text{ km}$$

Evaluating the implied speed:
$$v_{\text{implied}} = \frac{d}{\Delta t} = \frac{2.40\text{ nmi}}{0.002778\text{ h}} = 864.0\text{ kn}$$

While the ship's reported internal SOG field claimed a plausible $12.1\text{ kn}$, the spatial coordinates implied an impossible velocity of $864\text{ kn}$. An unvalidated pipeline ingesting this record into a trajectory model would generate a massive displacement spike. The kinematic gate intercepts $v_{\text{implied}} > 60\text{ kn}$, quarantines Fix 2 as an erroneous jump, and preserves track continuity using Fix 1.

> **Rule of thumb.** **Spatial cleaning vs. Kinematic reality.**
> Never filter AIS trajectory outliers using spatial bounding boxes alone. A vessel reporting impossible positions in the middle of a continent is easily caught; a vessel jumping 2 nautical miles into the wrong traffic lane inside a busy harbor is lethal to maritime analytics. Always evaluate **implied velocity** ($v = \Delta d / \Delta t$) across consecutive temporal fixes.

> **Definitions that bite.** **Course Over Ground (COG) vs. True Heading.**
> - **Course Over Ground (COG):** The actual directional path of the vessel relative to the Earth's surface, derived from GNSS Doppler and carrier-phase tracking.
> - **True Heading:** The orientation of the ship's bow relative to True North, derived from a gyrocompass or transmitting magnetic heading device.
> In cross-currents, heavy wind, or crabbing maneuvers during pilotage, COG and Heading can diverge by $20^\circ$ or more. Visualizing a ship's hull rotated along its COG vector depicts the vessel sliding sideways through the water; software must orient ship models using True Heading, reserving COG solely for motion vector projection.

## Software

**Open source:**
- `MovingPandas` (Python): Anita Graser's trajectory analysis library built on GeoPandas, offering trajectory extraction, stop detection, and smoothing. Caveat: High memory overhead when handling massive unchunked trajectory collections on a single machine.
- `DuckDB Spatial` (C++, Python): Embedded analytical SQL database supporting fast spatial queries and vector geometries directly against Parquet. Caveat: Spatial indexing features (such as R-Tree indexes) are less mature than PostGIS for dynamic updates.
- `PostGIS` (C, SQL): Enterprise-grade spatial database extension for PostgreSQL implementing complete OGC standards and GiST spatial indexes. Caveat: Requires significant database administration, schema tuning, and storage overhead compared to flat columnar files.
- `Apache Sedona` (Java, Scala, Python): Distributed spatial computing framework for Apache Spark and Flink, enabling cluster-scale joins and trajectory partitioning. Caveat: High deployment complexity and JVM cluster infrastructure overhead.
- `OpenCPN` (C++): Desktop marine chartplotter supporting live NMEA decoding, S-57/S-63 chart rendering, and IEC 62288 target collision tracking. Caveat: Desktop GUI application not architected for headless, cloud-native automated processing.
- `Blender` (`bpy` API) (C, C++, Python): 3D modeling and animation suite providing headless Python scripting, local tangent projections, and keyframe generation for incident reconstruction. Caveat: Operates internally in single-precision float32, requiring manual geographic coordinate normalization to prevent floating-point jitter.

**Free but closed:**
- `Google Earth Pro` (Desktop): Visualizes KML/KMZ ship trajectories against global satellite bathymetry and terrain elevation. Caveat: Closed-source desktop software with limited capacity for multi-million-row dynamic temporal playback.

**Commercial:**
- `GateHouse Maritime AIS Server`: Industrial coastal data aggregation and filtering platform used by national maritime authorities. Caveat: Expensive enterprise proprietary software requiring dedicated server licensing.
- `Kongsberg Norcontrol C-Scope`: Commercial VTS platform providing real-time multi-sensor radar and AIS fusion for major international waterways. Caveat: Turnkey proprietary hardware and software ecosystem unavailable for third-party development.
- `Wärtsilä Navi-Harbour`: Industry-standard commercial port management and vessel traffic surveillance software. Caveat: Highly restricted proprietary licensing tied to type-approved marine consoles.

## Standards & guides

- **Recommendation ITU-R M.1371-5** (2014): *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*. Defines message field semantics, quantization units, and operational sentinels for Messages 1–27.
- **IEC 61162-1:2016 (Edition 5.0)**: *Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 1: Single talker and multiple listeners*. Standardizes the `!AIVDM` sentence format, 6-bit ASCII armoring, and TAG block encapsulation.
- **IEC 62288:2021 (Edition 3.0)**: *Maritime navigation and radiocommunication equipment and systems — Presentation of navigation-related information on shipborne navigational displays*. Governs visual symbology, operational target states (sleeping, activated, lost), and predictor vectors on marine displays.
- **IEC 61174:2015 (Edition 4.0)**: *Maritime navigation and radiocommunication equipment and systems — Electronic chart display and information system (ECDIS) — Operational and performance requirements*. Defines chart presentation, target integration, and route monitoring standards.
- **IEC 61996-1:2013 (Edition 2.0)**: *Maritime navigation and radiocommunication equipment and systems — Shipborne voyage data recorder (VDR) — Part 1: Performance requirements*. Governs the recording and extraction of navigational sensor feeds and AIS data for forensic investigation.
- **IALA Recommendation V-128**: *Operational and Technical Performance Requirements for VTS Systems*. Establishes international performance benchmarks, tracking accuracy, and data availability standards for coastal VTS software installations.
- **IHO S-57 / S-100**: *Transfer Standard for Digital Hydrographic Data*. Governs vector electronic navigational chart structures used by OpenCPN and commercial ECDIS displays.

## Pitfalls

- **Neglecting local origin shifts in 3D animation:** Feeding global geographic coordinates ($>4,000,000\text{ m}$ in projected space) directly into Blender or 3D DCC tools $\implies$ exhausts the 24-bit mantissa of 32-bit floating-point numbers, causing severe visual jitter and vertex tearing; software must project coordinates to a local tangent plane centered on the scene origin.
- **Permitting Bézier spline interpolation across sparse fixes:** Allowing animation packages to apply default Bézier smoothing between AIS reports separated by multiple minutes $\implies$ produces wild spatial overshoots where vessels swing unrealistically across shoals and piers; pipelines must strictly enforce linear (`LINEAR`) keyframe interpolation.
- **Treating heading sentinel 511 as a valid angle:** Failing to intercept True Heading `511` ("not available") $\implies$ rotates 3D vessel hulls to absurd geometric bearings; pipelines must convert `511` to `NaN` and fall back to Course Over Ground for orientation.
- **Confusing Course Over Ground with True Heading during cross-currents:** Orienting vessel models along their COG vector rather than True Heading $\implies$ eliminates visual crab angle, misrepresenting what bridge watchkeepers could see; software must orient models by True Heading and project future movement along COG.
- **Sorting multi-source streams solely by arrival timestamp:** Merging satellite, terrestrial, and crowdsourced feeds by arrival timestamp $\implies$ introduces false time reversals due to variable network backhaul latencies; records must be sequenced by internal GNSS epoch time.
- **Executing planar Cartesian distance formulas on global coordinates:** Computing distances with the Pythagorean theorem on longitude and latitude degrees $\implies$ introduces massive latitudinal distortion; software must use Haversine or geodetic Vincenty algorithms on an ellipsoidal model.
- **Omitting dimension offsets from the GNSS antenna reference point:** Placing a 400-meter container ship's 3D mesh symmetrically around its reported GNSS position $\implies$ displaces the bow and stern by hundreds of meters if the antenna is located on the wheelhouse aft; software must apply the $A, B, C, D$ dimension offsets defined in Message 5.
- **Ignoring MMSI reuse and test sentinels:** Ingesting reports from MMSI `0`, `123456789`, or `1193046` into trajectory models $\implies$ merges hundreds of distinct physical vessels into a single catastrophic "super-track"; cleaning pipelines must filter invalid MMSIs immediately upon ingest.
- **Applying stop detection thresholds without spatial bounding envelopes:** Relying solely on reported SOG $< 0.5\text{ kn}$ to detect port berthing $\implies$ misclassifies slow-drifting vessels or tug operations as moored; stop detection must combine speed gates with spatial dwell envelopes and duration thresholds.
- **Overlooking single-precision limits in spatial databases:** Storing high-precision geodetic coordinates in single-precision `float4` columns $\implies$ degrades spatial resolution to approximately 1 meter at the equator, corrupting precise berth alignment analysis; always use double-precision `float8` or native spatial types.

## Key takeaways

- Processing decoded AIS data requires a layered architecture spanning vector geometry (`GeoPandas`), trajectory kinematics (`MovingPandas`), spatial databases (`PostGIS`, `DuckDB Spatial`), and 3D visual reconstruction (`Blender`).
- Raw AIS telemetry must never be ingested directly into analytical models without passing through a kinematic validation gate that filters invalid MMSIs, coordinate sentinels, and impossible velocity jumps.
- Discrete Global Grid Systems (**H3** and **S2**) eliminate projection distortions and boundary artifacts, providing equidistant hexagonal and hierarchical quadtree binning for maritime traffic density mapping.
- Desktop chartplotters like **OpenCPN** implement international display standards (**IEC 62288**), translating discrete NMEA sentences into live target vectors, CPA/TCPA calculations, and collision warnings.
- Commercial VTS platforms (GateHouse, Kongsberg Norcontrol, Wärtsilä Navi-Harbour) achieve five-nines operational reliability by fusing AIS with coastal surveillance radar, electro-optical tracking, and VHF radio direction finding.
- **Blender** serves as a vital tool for Admiralty court accident reconstruction, line-of-sight bridge sightline analysis, and satellite footprint animation via its headless `bpy` Python API.
- Because Blender operates internally using 32-bit floating-point math, global coordinates must be projected to a local tangent plane anchored at the scene origin to prevent destructive visual jitter.
- Trajectory keyframes in 3D animation software must enforce linear interpolation to avoid catastrophic Bézier overshoots during multi-minute telemetry gaps.
- True Heading and Course Over Ground represent fundamentally distinct physical properties; vessels must be oriented using True Heading while motion predictor vectors follow Course Over Ground.

## References

- Blender Online Community (2026). *Blender 4.x Reference Manual*. Blender Foundation. https://docs.blender.org/manual/en/latest/.
- Cerdeiro, D. A., Komaromi, A., Liu, Y., Saeed, M. R. (2020). World Seaborne Trade in Real Time: A Proof of Concept for Building AIS-based International Trade Indices. *IMF Working Papers*, 2020(057):1–39. doi:10.5089/9781513536835.001.
- Graser, A. (2019). MovingPandas: Efficient Analysis of Movement Data in Python. *GI_Forum*, 7(1):54–68. doi:10.1553/giscience2019_01_s54.
- Harati-Mokhtari, A., Wall, A., Brooks, P., Wang, J. (2007). Automatic Identification System (AIS): Data Reliability and Human Error Implications. *The Journal of Navigation*, 60(3):373–389. doi:10.1017/S0373463307004298.
- Hughes, J. N., Annex, A., Eichelberger, C. N., Fox, A., Hulbert, A., Ronquest, M. (2015). GeoMesa: a distributed architecture for spatio-temporal fusion. *Proceedings of the SPIE*, 9473:94730F. doi:10.1117/12.2177307.
- International Electrotechnical Commission (2013). *Maritime navigation and radiocommunication equipment and systems -- Shipborne voyage data recorder (VDR) -- Part 1: Performance requirements, methods of testing and required test results* (IEC Standard No. 61996-1:2013, Ed. 2.0). Geneva: IEC.
- International Electrotechnical Commission (2015). *Maritime navigation and radiocommunication equipment and systems -- Electronic chart display and information system (ECDIS) -- Operational and performance requirements, methods of testing and required test results* (IEC Standard No. 61174:2015, Ed. 4.0). Geneva: IEC.
- International Electrotechnical Commission (2016). *Maritime navigation and radiocommunication equipment and systems -- Digital interfaces -- Part 1: Single talker and multiple listeners* (IEC Standard No. 61162-1:2016, Ed. 5.0). Geneva: IEC.
- International Electrotechnical Commission (2021). *Maritime navigation and radiocommunication equipment and systems -- Presentation of navigation-related information on shipborne navigational displays -- General requirements, methods of testing and required test results* (IEC Standard No. 62288:2021, Ed. 3.0). Geneva: IEC.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-5). Geneva: ITU.
- Jalkanen, J.-P., Brink, A., Kalli, J., Pettersson, H., Kukkonen, J., Stipa, T. (2009). A modelling system for the exhaust emissions of maritime traffic and its application in the Baltic Sea area. *Atmospheric Chemistry and Physics*, 9(23):9209–9223. doi:10.5194/acp-9-9209-2009.
- Kroodsma, D. A., Mayorga, J., Hochberg, T., Miller, N. A., Boerder, K., Ferretti, F., Wilson, A., Bergman, B., White, T. D., Block, B. A., Woods, P., Sullivan, B., Costello, C., Worm, B. (2018). Tracking the global footprint of fisheries. *Science*, 359(6378):904–908. doi:10.1126/science.aao5646.
- Paolo, F. S., Kroodsma, D., Raynor, J., Hochberg, T., Davis, P., Cleary, J., Marsaglia, L., Orofino, S., Thomas, C., Halpin, P. (2024). Satellites reveal widespread unmonitored activity at sea. *Nature*, 625(7993):85–91. doi:10.1038/s441586-023-06825-8.
- PostGIS Development Team (2001). *PostGIS: Spatial and Geographic Objects for PostgreSQL*. https://postgis.net. GPL-2.0-or-later.
- QGIS Development Team (2002). *QGIS Geographic Information System*. https://qgis.org. GPL-2.0-or-later.
- Raasveldt, M., Mühleisen, H. (2019). DuckDB: an Embeddable Analytical Database. *Proceedings of the 2019 International Conference on Management of Data* (SIGMOD '19), 1981–1984. doi:10.1145/3299869.3320212.
- Register, D., OpenCPN Development Team (2010). *OpenCPN: Chart Plotter and Marine GPS Navigation Software*. https://github.com/OpenCPN/OpenCPN. GPL-2.0-or-later.
- Richter, L. M. (2019). *pyais: Pure Python AIS message decoding and encoding library*. https://github.com/M0r13n/pyais. MIT.
- Schwehr, K. (2010). *libais: C++ AIS decoding library with Python bindings*. https://github.com/schwehr/libais. Apache-2.0.
- Yu, J., Zhang, Z., Sarwat, M. (2019). Spatial Data Management in Apache Spark: The GeoSpark Approach and Beyond. *GeoInformatica*, 23(3):379–399. doi:10.1007/s10707-018-0331-2.
