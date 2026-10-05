# Notation, Bit-Level Conventions, RF Units, and Coordinate Reference Frames

> **Purpose:** Because AIS spans over-the-air VHF radio engineering, bit-oriented binary telecommand framing, shipboard serial/CAN bus protocols, geodetic surveying, and 3D computer graphics, subtle mismatches in bit numbering, integer sign extension, decibel reference antennas, or coordinate reference systems (CRS) routinely cause catastrophic bugs in decoders and spatial pipelines. This front-matter specification establishes the unambiguous conventions used throughout this handbook.

---

## 1. Bit-Indexing and Byte-Ordering Conventions

### 1.1 Over-the-Air HDLC Bit Order vs. Payload Bit Unpacking
An AIS transmission exists in two distinct bit-ordering domains depending on whether an engineer is inspecting a **raw demodulated RF bitstream** (Chapter 7) or an **unpacked NMEA 0183 `!AIVDM` payload** (Chapters 14–16):

1. **Over-the-Air VHF Physical / Link Layer (ITU-R M.1371-5 Annex 2, §3.2.2):**
   * Inside the HDLC frame (between the `0x7E` start and end flags), bytes of the binary payload are transmitted **Least Significant Bit (LSB) first** on the radio channel, whereas multi-bit parameter fields inside the payload message structure are defined **Most Significant Bit (MSB) first**.
   * Furthermore, the transmitter applies **HDLC zero-bit stuffing** (inserting a `0` bit after any five consecutive `1` bits) across the payload and 16-bit CRC-CCITT Frame Check Sequence (FCS) prior to NRZI encoding and GMSK modulation.
2. **NMEA 0183 `!AIVDM` / `!AIVDO` Unpacked Payload Layer (IEC 61162-1):**
   * The receiving AIS transponder or SDR demodulator (`AIS-catcher`, `rtl-ais`) strips the ramp, preamble, start/end flags, bit-stuffing zeros, and CRC-16 FCS.
   * It then partitions the clean payload bitstream (e.g., 168 bits for a single-slot Message 1, 2, or 3) into consecutive **6-bit groups** and encodes each 6-bit group (`0..63`) into a printable ASCII character (`'0'`–`'W'`, `` '`' ``–`'w'`).
   * When an open-source decoder (`libais`, `gpsd`, `pyais`, `aisparser`, Rust `nmea-parser`) de-armors each ASCII character back into 6 bits and concatenates them, the resulting bit array is strictly **MSB-first** from bit `0` to bit `N - 1`.

### 1.2 0-Based (`libais` / `AIVDM.txt`) vs. 1-Based (`ITU-R M.1371`) Bit Numbering
Throughout this book, all bit-layout tables list **both** conventions side by side:

| Convention | First Bit of Message | Last Bit of 1-Slot Message (168 bits) | Message ID Slice (6 bits) | MMSI Slice (30 bits) | Used By |
|---|---|---|---|---|---|
| **0-Based Indexing (Inclusive)** | `0` | `167` | `0–5` (Python `bits[0:6]`) | `8–37` (Python `bits[8:38]`) | `libais`, `gpsd` (`AIVDM.txt`), `pyais`, C/C++/Rust/Python code |
| **1-Based Indexing (Inclusive)** | `1` | `168` | `1–6` | `9–38` | ITU-R M.1371-5, IMO SN.1/Circ.289, IALA standards |

> [!IMPORTANT]
> In Python slice notation (`bits[start:stop]`), `stop` is **exclusive**, so a field spanning 0-based inclusive bits `b_start` through `b_end` of width $W = b_{\text{end}} - b_{\text{start}} + 1$ is sliced as `bits[b_start : b_start + W]`.

---

## 2. Unsigned and Two's Complement Signed Integer Extraction

### 2.1 Unsigned Integer (`uint`)
For an unsigned field of bit-width $W$ stored in MSB-first bits $(b_0, b_1, \dots, b_{W-1}) \in \{0,1\}^W$:

$$U = \sum_{k=0}^{W-1} b_k \, 2^{W - 1 - k}$$

### 2.2 Signed Two's Complement Integer (`int`)
ITU-R M.1371 encodes all signed quantities—specifically **Longitude** ($W=28$), **Latitude** ($W=27$), **Rate of Turn** ($W=8$), and ** Meteorological/Hydrographic temperatures and water levels**—using standard **two's complement**:

$$S = -b_0 \, 2^{W-1} + \sum_{k=1}^{W-1} b_k \, 2^{W - 1 - k} = \begin{cases} U & \text{if } U < 2^{W-1} \quad (b_0 = 0) \\ U - 2^W & \text{if } U \ge 2^{W-1} \quad (b_0 = 1) \end{cases}$$

### 2.3 Canonical Scaling Factors and Sentinel ("Not Available") Values
Never ingest decoded AIS fields without filtering out ITU-R M.1371 sentinel values, which indicate that an external sensor (GNSS, gyrocompass, ROT indicator) is disconnected or uninitialized:

| Field | Bit Width $W$ | Type | Raw-to-Physical Scaling | Valid Range | "Not Available" Sentinel (Raw / Physical) |
|---|---|---|---|---|---|
| **Longitude** | 28 | Signed (`int28`) | $\lambda = \frac{S}{600{,}000}\text{ deg}$ ($\frac{1}{10{,}000}\text{ min}$) | $[-180.0^\circ, +180.0^\circ]$ | `0x6791AC0` ($108{,}600{,}000$) = **`181.0°`** |
| **Latitude** | 27 | Signed (`int27`) | $\phi = \frac{S}{600{,}000}\text{ deg}$ ($\frac{1}{10{,}000}\text{ min}$) | $[-90.0^\circ, +90.0^\circ]$ | `0x3412140` ($54{,}600{,}000$) = **`91.0°`** |
| **Speed Over Ground (SOG)** | 10 | Unsigned (`uint10`) | $v = \frac{U}{10}\text{ knots}$ | $[0.0, 102.1]\text{ kts}$ (`1022` = $\ge 102.2\text{ kts}$) | `1023` (`0x3FF`) = **`102.3 kts`** |
| **Course Over Ground (COG)** | 12 | Unsigned (`uint12`) | $\chi = \frac{U}{10}\text{ deg true}$ | $[0.0^\circ, 359.9^\circ]$ | `3600` (`0xE10`) = **`360.0°`** |
| **True Heading (HDG)** | 9 | Unsigned (`uint9`) | $\psi = U\text{ deg true}$ | $[0^\circ, 359^\circ]$ | `511` (`0x1FF`) = **`511°`** |
| **Rate of Turn (ROT)** | 8 | Signed (`int8`) | $\text{ROT}_{\text{AIS}} = \text{sgn}(\omega)\cdot 4.733\sqrt{|\omega_{\text{deg/min}}|}$ | $[-126, +126]$ (`±127` = turning $>5^\circ/30\text{s}$ without TI) | `-128` (`0x80`) = **Not Available** |
| **UTC Second (Time Stamp)** | 6 | Unsigned (`uint6`) | Seconds of current UTC minute | $0\text{–}59\text{ s}$ | `60` = N/A; `61` = Manual; `62` = Dead Reckoning; `63` = Inoperative |
| **Static Draught (Msg 5)** | 8 | Unsigned (`uint8`) | $d = \frac{U}{10}\text{ meters}$ | $[0.1, 25.5]\text{ m}$ | `0` = **Not Available / Default** |

---

## 3. Radio Frequency (RF) and Link-Budget Units

| Symbol / Unit | Definition | Conversion / Formula |
|---|---|---|
| **$f$, $\lambda$** | Carrier frequency and free-space wavelength ($c = 299{,}792{,}458\text{ m/s}$) | At AIS 1 ($161.975\text{ MHz}$), $\lambda = 1.8509\text{ m}$; at AIS 2 ($162.025\text{ MHz}$), $\lambda = 1.8503\text{ m}$ |
| **$\text{dBW}$ vs. $\text{dBm}$** | Power relative to $1\text{ W}$ vs. $1\text{ mW}$ | $P_{\text{dBm}} = P_{\text{dBW}} + 30 = 10\log_{10}(P_{\text{W}} \times 1000)$. Class A ($12.5\text{ W}$) $= +40.97\text{ dBm}$; Class B SO ($5\text{ W}$) $= +36.99\text{ dBm}$; Class B CS ($2\text{ W}$) $= +33.01\text{ dBm}$ |
| **$\text{dBi}$ vs. $\text{dBd}$** | Antenna gain relative to an isotropic radiator ($\text{dBi}$) vs. a lossless half-wave dipole ($\text{dBd}$) | $G_{\text{dBi}} = G_{\text{dBd}} + 2.15\text{ dB}$. A standard $\frac{1}{2}\lambda$ marine whip has $0\text{ dBd} = 2.15\text{ dBi}$ (often marketed as "$3\text{ dB}$ marine gain") |
| **VSWR & Return Loss** | Voltage Standing Wave Ratio from impedance mismatch ($\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}$, $Z_0 = 50\text{ }\Omega$) | $\text{VSWR} = \frac{1 + |\Gamma|}{1 - |\Gamma|}$; Fraction of power radiated $= 1 - |\Gamma|^2$. At $\text{VSWR} = 1.5:1$, $4\%$ power is reflected; at $\text{VSWR} = 3.0:1$, $25\%$ is reflected |
| **Noise Figure ($NF$)** | Degradation of SNR through an RF front-end at $T_0 = 290\text{ K}$ | Thermal noise floor in $B = 25\text{ kHz}$ is $N_0 B = -174\text{ dBm/Hz} + 10\log_{10}(25{,}000) = -130.0\text{ dBm}$ |

---

## 4. Geodetic, Vessel Body, and 3D Scene (Blender) Coordinate Reference Frames

### 4.1 Geodetic Frame (`EPSG:4326` / WGS84)
ITU-R M.1371 requires all positions to be referenced to the **World Geodetic System 1984 (WGS84)** ellipsoid ($a = 6{,}378{,}137.0\text{ m}$, $f = 1 / 298.257223563$):
* **Longitude ($\lambda$):** Positive East, negative West ($[-180^\circ, +180^\circ]$).
* **Latitude ($\phi$):** Positive North, negative South ($[-90^\circ, +90^\circ]$).
* **Nautical Mile ($1\text{ NM}$):** Exactly $1{,}852\text{ meters}$ ($\approx 1$ arc-minute of latitude); $1\text{ knot} = 1\text{ NM/hour} = 0.514444\text{ m/s}$.

### 4.2 Local Tangent Plane (East-North-Up [ENU]) for Metric Analytics and Blender 3D Scenes
In **Blender** (`bpy`), 3D vertex coordinates and object transformation matrices are stored in **single-precision IEEE 754 `float32`** (24 bits of significand $\approx 7.2$ decimal digits). If UTM coordinates ($N \approx 4{,}700{,}000\text{ m}$) or ECEF coordinates ($X \approx 4{,}000{,}000\text{ m}$) are loaded directly as vertex positions, the least-significant bit of a `float32` is $2^{\lfloor\log_2(4.7\times 10^6)\rfloor - 23} = 2^{22-23} = 0.5\text{ meters}$—causing severe visual mesh tearing and jerky ship animation!

Therefore, for all 3D reconstructions and local metric kinematics, we define a local scene origin $(\lambda_0, \phi_0, h_0)$ at the center of the area of interest (e.g., collision point or harbor entrance) and transform every AIS position $(\lambda_k, \phi_k, h_k)$ into local **East-North-Up (ENU)** meters $(x_{\text{E}}, y_{\text{N}}, z_{\text{U}})$ aligned with Blender's right-handed coordinate axes ($+X = \text{East}$, $+Y = \text{North}$, $+Z = \text{Up}$):

$$\begin{bmatrix} X_{\text{Blender}} \\ Y_{\text{Blender}} \\ Z_{\text{Blender}} \end{bmatrix} = \begin{bmatrix} x_{\text{E}} \\ y_{\text{N}} \\ z_{\text{U}} \end{bmatrix}, \qquad \psi_{\text{Blender, Z-Euler}} = \frac{\pi}{2} - \psi_{\text{True Heading (rad)}} \quad (\text{or } -\psi_{\text{True}} \text{ when mesh bow points along } +Y)$$

### 4.3 Vessel Body Frame and GNSS Antenna Reference Point Offsets (Message 5 & 24)
An AIS position report $(\lambda, \phi)$ does **not** report the center of gravity or geometric center of the ship; it reports the location of the **GNSS antenna** feeding the AIS transponder. Message 5 (Class A) and Message 24 Part B (Class B) specify four unsigned integer offsets (in meters) from the GNSS antenna reference point:
* $A = d_{\text{bow}}$ (9 bits, $0\text{–}511\text{ m}$): Distance from GNSS antenna to the bow.
* $B = d_{\text{stern}}$ (9 bits, $0\text{–}511\text{ m}$): Distance from GNSS antenna to the stern.
* $C = d_{\text{port}}$ (6 bits, $0\text{–}63\text{ m}$): Distance from GNSS antenna to the port beam.
* $D = d_{\text{starboard}}$ (6 bits, $0\text{–}63\text{ m}$): Distance from GNSS antenna to the starboard beam.

From $(A, B, C, D)$, the ship's **Length Overall ($L_{\text{OA}}$)**, **Beam ($W$)**, and the vector offset $(\Delta x_{\text{body}}, \Delta y_{\text{body}})$ from the **GNSS antenna (pivot origin)** to the **geometric hull center** in the vessel's local body frame ($+y_{\text{body}} = \text{Bow}$, $+x_{\text{body}} = \text{Starboard}$) are:

$$L_{\text{OA}} = A + B, \qquad W = C + D$$

$$\Delta x_{\text{center\_from\_antenna}} = \frac{D - C}{2}, \qquad \Delta y_{\text{center\_from\_antenna}} = \frac{A - B}{2}$$

Rotating by True Heading $\psi$ (clockwise from North) transforms any point $(x_{\text{body}}, y_{\text{body}})$ on the hull relative to the GNSS antenna into local East-North meters $(x_{\text{E}}, y_{\text{N}})$:

$$\begin{bmatrix} x_{\text{E}} \\ y_{\text{N}} \end{bmatrix} = \begin{bmatrix} x_{\text{E, ant}} \\ y_{\text{N, ant}} \end{bmatrix} + \begin{bmatrix} \cos\psi & \sin\psi \\ -\sin\psi & \cos\psi \end{bmatrix} \begin{bmatrix} x_{\text{body}} \\ y_{\text{body}} \end{bmatrix}$$
