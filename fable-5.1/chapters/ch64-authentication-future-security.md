# Chapter 64 — Authentication and the future of AIS security

> **Part IX — Security.** An examination of the cryptographic, protocol, and network architectures required to secure maritime situational awareness, contrasting in-band backwards-compatible proposals with modern VHF Data Exchange System (VDES) standards and downstream data-provider trust scoring.

**In this chapter.** You will learn why legacy Automatic Identification System (**AIS**) broadcasts cannot be cryptographically authenticated in place without disrupting global maritime safety. We analyze the rigid channel, slot, and backward-compatibility constraints imposed by Recommendation ITU-R M.1371 that frustrate naive digital signature schemes. You will evaluate leading academic and industry proposals for retrofitting authentication into legacy VHF broadcasts, including Protected AIS (**pAIS**), Timed Efficient Stream Loss-Tolerant Authentication (**TESLA**) broadcast chains, and asymmetric elliptic-curve public-key signatures distributed across auxiliary messages. We dissect the native security provisions emerging within the VHF Data Exchange System (**VDES**) under Recommendation ITU-R M.2092 and International Association of Marine Aids to Navigation and Lighthouse Authorities (**IALA**) Guideline G1192, including digital signature architectures for Aid-to-Navigation (**AtoN**) reports. Finally, you will explore provider-side multi-layer trust scoring and establish practical migration paths for future maritime cybersecurity.

## 64.1 Why AIS cannot be authenticated in place

The maritime Automatic Identification System was engineered as a cleartext, unauthenticated radio broadcast protocol ([Chapter 20](ch20-architecture-and-station-classes.md); [Chapter 58](ch58-threat-model.md)). When Recommendation ITU-R M.1371 was codified in the late 1990s, maritime operations assumed honest crews using dedicated, type-approved transponders conforming to IEC 61993-2. The operational priority was instantaneous, unencumbered collision avoidance: vessels in VHF range had to calculate Closest Point of Approach (**CPA**) and Time to Closest Point of Approach (**TCPA**) on bridge radar and ECDIS without network handshake, key exchange, or administrative registration ([Chapter 51](ch51-charts-enc-ecdis.md)).

That trust model has collapsed. Software-Defined Radios (**SDRs**) democratized GMSK signal synthesis ([Chapter 33](ch33-hardware-and-sdr.md)), while global aggregators transformed local tactical broadcasts into international supply-chain telemetry ([Chapter 41](ch41-networks-and-providers.md)). Deceptive actors routinely project synthetic fleets, clone MMSIs, and spoof navigation coordinates ([Chapter 59](ch59-spoofing.md)). Yet retrofitting cryptographic authentication into operational transponders remains one of the most constrained problems in maritime telecommunications.

```
+-----------------------------------------------------------------------------------+
|               The In-Band Authentication Trilemma for Legacy AIS                  |
|                                                                                   |
|                      [Universal Interoperability]                                 |
|                       /                         \                                 |
|                      /                           \                                |
|    Legacy Class A/B receivers              Strict 256-bit slot boundary           |
|    must parse lat/lon/SOG                  prevents standard RSA/ECDSA            |
|    without dropping frames                 signatures in Message 1/2/3            |
|                    /                               \                              |
|                   /                                 \                             |
|       [Cryptographic Security] ------------------ [Spectrum Capacity]            |
|       Requires 160-512 signature bits      Over-the-air slot starvation on        |
|       and public key binding / PKI         AIS 1 (161.975) & AIS 2 (162.025 MHz)  |
+-----------------------------------------------------------------------------------+
```

### 64.1.1 The bit budget and slot boundary trap
The fundamental technical barrier to in-place authentication is the physical structure of the Self-Organizing Time Division Multiple Access (**SOTDMA**) frame ([Chapter 21](ch21-link-layer-tdma.md); [Chapter 28](ch28-rf-encoding-physical-layer.md)). The VHF Data Link (**VDL**) divides each 60-second frame across AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz) into exactly 2,250 time slots. Each slot is strictly 26.67 milliseconds long, accommodating exactly 256 bits at the standard over-the-air channel rate of 9,600 bits per second (bit/s):

$$\text{Slot Capacity} = 0.026667\text{ s} \times 9600\text{ bit/s} = 256\text{ bits}$$

Within this 256-bit envelope, fixed protocol overhead consumes 88 bits:
- **Preamble:** 24 bits (alternating `0101...` sequence for receiver bit synchronization).
- **Start Flag:** 8 bits (`0x7E` / `01111110` HDLC frame delimiter).
- **Cyclic Redundancy Check (CRC-16):** 16 bits (standard CCITT polynomial $G(x) = x^{16} + x^{12} + x^5 + 1$).
- **End Flag:** 8 bits (`0x7E` / `01111110`).
- **Nominal Guard Period and Distance Delay:** 24 bits (allowing receiver power ramp-down and propagation delays up to ~20 nmi; 37 km).
- **Bit Stuffing Allowance:** 8 bits nominal (HDLC zero-insertion after five consecutive ones).

Subtracting this 88-bit physical and data link layer overhead leaves an absolute ceiling of **168 bits** of usable payload for a single-slot burst:

$$\text{Usable Payload} = 256\text{ bits} - 88\text{ bits} = 168\text{ bits}$$

Standard Class A position reports—Message 1 (scheduled), Message 2 (assigned), and Message 3 (response to interrogation)—are defined in Recommendation ITU-R M.1371 Annex 8 Table 44 as exactly 168 bits long ([Chapter 22](ch22-message-catalog.md); [Appendix C](../appendices/appendix-c-message-bit-layouts.md)). The message structure allocates:
- Message ID: 6 bits
- Repeat Indicator: 2 bits
- User ID (MMSI): 30 bits
- Navigational Status: 4 bits
- Rate of Turn (ROT): 8 bits
- Speed Over Ground (SOG): 10 bits
- Position Accuracy: 1 bit
- Longitude: 28 bits (signed integer, resolution $1/10000$ minute)
- Latitude: 27 bits (signed integer, resolution $1/10000$ minute)
- Course Over Ground (COG): 12 bits
- True Heading: 9 bits
- Time Stamp: 6 bits (UTC second of report generation)
- Special Maneuver Indicator: 2 bits
- Spare: 3 bits
- RAIM Flag: 1 bit
- SOTDMA Communication State: 19 bits (Sync State 2, Slot Timeout 3, Sub-Message 14)

The payload utilization of Messages 1, 2, and 3 is exactly $168 / 168 = 100.0\%$. There is not a single spare bit available in the core navigation broadcast to host a digital signature, message authentication code (**MAC**), or key identifier.

### 64.1.2 Cryptographic signature dimensions
Modern asymmetric cryptography cannot produce digital signatures that fit into fractional slot spaces. An Elliptic Curve Digital Signature Algorithm (**ECDSA**) signature over the standard NIST P-256 curve (secp256r1) requires 512 bits (two 256-bit integers, $r$ and $s$). An Edwards-curve Digital Signature Algorithm (**Ed25519**) signature requires exactly 512 bits (64 bytes). Even the shortest standardized public-key signatures based on pairing-friendly curves—such as Boneh-Lynn-Shacham (**BLS12-381**)—demand 384 bits (48 bytes) for a compressed signature point.

If an engineer attempts to append a 512-bit Ed25519 signature directly to a 168-bit position payload, the resulting transmission requires:

$$\text{Total Data} = 168\text{ bits (payload)} + 512\text{ bits (signature)} = 680\text{ bits}$$

Adding protocol framing (88 bits minimum, plus increased bit stuffing across 680 bits) yields a packet exceeding 780 bits. Because each TDMA slot holds only 256 bits, transmitting this authenticated report requires spanning **four consecutive TDMA slots** ($4 \times 256 = 1,024\text{ bits}$).

In congested waterways such as the Singapore Strait, the English Channel, or the Pearl River Delta, the VDL already operates at or above $50\%$ to $80\%$ slot occupancy ([Chapter 21](ch21-link-layer-tdma.md); [Chapter 30](ch30-network-loading-packet-loss.md)). Expanding every routine 2-second to 10-second Class A position report from a single slot into four slots would instantly quadruple channel loading, triggering widespread packet collisions, dropping essential safety targets from bridge radars, and collapsing the distributed SOTDMA network into mutual self-interference.

> **Worked example.**
> Consider a traffic separation scheme with $N = 200$ commercial vessels operating Class A transponders reporting at an average interval of $\Delta t = 3\text{ s}$ ($20\text{ reports/min}$ per hull).
>
> 1. *Legacy Single-Slot Reports (Message 1):*
>    - Total slot demand: $200 \times 20 = 4,000\text{ slots/min}$.
>    - Total two-channel capacity: $2 \times 2,250 = 4,500\text{ slots/min}$.
>    - Channel load:
>      $$\text{Load}_{\text{legacy}} = \frac{4,000}{4,500} \approx 88.89\%$$
>      *(Manageable via standard SOTDMA slot reuse and cell downsizing rules.)*
>
> 2. *In-Band 4-Slot Signed Reports (Appending 512-bit Ed25519 signatures):*
>    - Aggregate slot demand: $200 \times (20 \times 4) = 16,000\text{ slots/min}$.
>    - Channel load:
>      $$\text{Load}_{\text{signed}} = \frac{16,000}{4,500} \approx 355.56\%$$
>
> A $355\%$ load exceeds physical spectrum capacity by $3.5\times$. In SOTDMA, loads exceeding $100\%$ force aggressive intentional slot reuse; at $355\%$, overlapping transmissions cause catastrophic packet collision, destroying all collision-avoidance capability.

### 64.1.3 The legacy receiver installed base
Even if spectrum capacity were boundless, the global maritime fleet represents an immense, heterogeneous installed base. More than 400,000 commercial, fishing, passenger, and recreational vessels operate type-approved Class A and Class B transponders worldwide ([Chapter 16](ch16-laws-and-treaties.md)). These units are certified under rigid international standards, primarily IEC 61993-2 for Class A and IEC 62287-1 / IEC 62287-2 for Class B.

Modifying the bit definitions of Messages 1, 2, or 3 would immediately break backward compatibility:
- Legacy transponders parsing an altered bitstream would extract corrupted navigation values, projecting erratic positions on bridge displays.
- Firmware updates across hundreds of thousands of hulls operating under flags of convenience are logistically impossible to enforce simultaneously.
- International maritime law grandfathers equipment certified under previous Performance Standards (such as IMO Resolution MSC.74(69)), keeping legacy transponders legally compliant throughout a hull's operational lifetime unless an amended SOLAS regulation mandates retrofits.

Any viable security architecture must therefore satisfy an absolute constraint: **unmodified legacy receivers must continue to decode core safety telemetry without error or frame rejection.**

## 64.2 Academic and industry proposals for legacy AIS

Because single-slot position reports cannot accommodate digital signatures directly, researchers have pursued three architectural paths: symmetric encapsulation (Protected AIS), delayed-disclosure hash chains (TESLA), and decoupled public-key architectures.

```
       Architectural Approaches to Legacy AIS Authentication
                                 |
    +----------------------------+----------------------------+
    |                                                         |
[Symmetric / Hybrid]                                  [Asymmetric Broadcast PKI]
    |                                                         |
    +--> Protected AIS (pAIS)                                 +--> Out-of-Band PKI (Wimpenny et al.)
    |    (Kessler 2020: AES-128/HMAC in Msg 6/8/25)           |    (ASM Msg 8 signature binding)
    |                                                         |
    +--> TESLA Broadcast Chains                               +--> Identity-Based Cryptography (IBC)
         (Perrig 2002: Delayed key disclosure)                     (Goudossis & Katsikas 2019/2020)
```

### 64.2.1 Protected AIS (pAIS)
Proposed and prototyped by Gary C. Kessler (2020), Protected AIS (**pAIS**) addresses the dual objectives of message authentication and confidentiality. Rather than modifying core broadcast messages, pAIS encapsulates encrypted and authenticated maritime data within existing Application-Specific Message (**ASM**) containers—specifically Message 6 (addressed binary) and Message 8 (broadcast binary), as well as single-slot Message 25 and multi-slot Message 26 ([Chapter 23](ch23-asm-binary-payloads.md)).

In pAIS, the transponder encrypts standard navigation telemetry using AES-128 or AES-256 (CBC or GCM mode), appends a truncated HMAC-SHA256 tag (32 or 64 bits), and encapsulates the ciphertext inside Message 6, 8, 25, or 26 using a designated DAC/FI.

```
+-----------------------------------------------------------------------------+
| Legacy AIS Message 6/8 Container (Unmodified RF Framing)                   |
| +-----------+---------+-----------+---------+-----------------------------+ |
| | Msg ID 8  | Repeat  | Source ID | Spare   | Application Identifier (16) | |
| | (6 bits)  | (2 bits)| (30 bits) | (2 bits)| DAC (10 bits) | FI (6 bits) | |
| +-----------+---------+-----------+---------+-----------------------------+ |
|             |                                                             | |
|             +-------------------> Encapsulated pAIS Binary Data           | |
|                                   +-------------------+-----------------+ | |
|                                   | AES-128 Encrypted | Truncated HMAC  | | |
|                                   | Navigation Block  | (32 to 64 bits) | | |
|                                   +-------------------+-----------------+ | |
+-----------------------------------------------------------------------------+
```

While pAIS demonstrated feasibility in maritime field trials, it encounters severe systemic barriers as an open civilian standard:
- **Key Distribution Bottlenecks:** Symmetric encryption requires every participating receiver to possess the secret shared key. While feasible for closed operational groups—such as a national coast guard flotilla, a port pilot association, or a commercial tugboat fleet—pre-shared symmetric keys cannot scale to open, global maritime traffic. If a universal "maritime broadcast key" were burned into commercial transponders, extraction via reverse-engineering of bridge hardware would be trivial.
- **Collateral Loss of Situational Awareness:** Encrypting position reports defeats the primary purpose of SOLAS Regulation 19: universal collision avoidance. A merchant vessel not enrolled in a specific pAIS key domain cannot decode the encrypted vessel's position, rendering the transmitting ship invisible on standard radar and ECDIS screens. Consequently, pAIS is inherently a *blue-force* tactical protocol ([Chapter 63](ch63-military-encrypted-ais.md)) rather than a civilian safety solution.

### 64.2.2 TESLA-style delayed-disclosure broadcast authentication
To achieve asymmetric properties without public-key signature overhead, several researchers have evaluated adapting the Timed Efficient Stream Loss-Tolerant Authentication (**TESLA**) protocol (Perrig et al. 2002) to the maritime VHF link. TESLA achieves broadcast authentication through the delayed disclosure of symmetric keys linked via a one-way cryptographic hash chain:

```
    Time Interval i-1               Time Interval i               Time Interval i+1
  [Transmit Message M_1]        [Transmit Message M_2]        [Transmit Key K_i]
            |                             |                             |
  MAC(M_1, K_i) attached        MAC(M_2, K_{i+1}) attached      Reveals Key K_i
  (Receiver buffers M_1)        (Receiver buffers M_2)         (Authenticates M_1)
```

1. **Hash Chain Generation:** A vessel generates a hash chain of length $L$ from random seed $K_L$ via $K_{j-1} = H(K_j)$ for $j = L, \dots, 1$, publishing root commitment $K_0$ in advance.
2. **Message Authentication Code:** In epoch $i$ (duration $\tau = 5\text{ s}$), the vessel broadcasts report $M_i$ with an unrevealed key tag $\text{Tag}_i = \text{HMAC}(K_i, M_i)$.
3. **Delayed Key Disclosure:** In epoch $i+1$, the vessel reveals key $K_i$ over the wire.
4. **Verification:** The receiver verifies $H(K_i) = K_{i-1}$, then checks $\text{HMAC}(K_i, M_i)$ against buffered report $M_i$.

While theoretically elegant and computationally lightweight, TESLA suffers from fatal operational liabilities in maritime collision avoidance:
- **Verification Latency and Collision Risk:** TESLA imposes an unavoidable verification delay equal to the disclosure interval ($d \times \tau$). In fast-encounter scenarios—such as two container ships approaching head-on at a combined closing speed exceeding $45\text{ kn}$ ($83\text{ km/h}$; $23\text{ m/s}$)—a safety-critical collision alert cannot wait 5 to 15 seconds to determine whether a target is genuine or fabricated.
- **Clock Drift Vulnerability:** TESLA's security proof depends strictly on loose time synchronization between transmitter and receiver. If an attacker can convince a receiver that the transmitter's clock is further advanced than it actually is, the attacker can intercept $K_i$ upon disclosure and forge a false message $M_i'$ that the receiver accepts as valid. In maritime environments where GNSS signals are actively jammed or spoofed ([Chapter 24](ch24-timing.md); [Chapter 62](ch62-gnss-jamming-spoofing.md)), this time-synchronization dependency creates a critical systemic failure point.
- **Buffer Exhaustion under Flooding:** Receivers must buffer all unverified position reports until the corresponding disclosure keys arrive. A malicious SDR transmitting thousands of synthetic Message 1 reports with bogus HMAC tags can trivially exhaust receiver microcontroller memory, inducing Denial-of-Service (**DoS**) crashes ([Chapter 60](ch60-malicious-payloads-robustness.md)).

### 64.2.3 Out-of-band public-key authentication (Wimpenny et al.)
The most technically viable paradigm for retrofitting authentication into legacy AIS without breaking backward compatibility was formulated by Wimpenny, Šafář, Grant, and Bransby (2022). Their architecture decouples the transmission of core navigation telemetry from the cryptographic signature.

In the Wimpenny scheme:
1. **Unmodified Core Broadcast:** The vessel broadcasts standard single-slot Message 1/2/3 reports on AIS 1 and AIS 2, ensuring legacy transponders display targets normally.
2. **Periodic Signature Bursts:** Every 30 to 60 seconds, the transponder computes an elliptic-curve signature over a concatenated sequence of recent position fixes.
3. **Encapsulation in ASM:** The signature and key identifier are packaged into a Message 8 or Message 26 binary container ([Chapter 23](ch23-asm-binary-payloads.md)).
4. **Retroactive Validation:** Security-aware receivers buffer position reports and validate them when the corresponding signature arrives, upgrading target status to authenticated.

```
     t = 0 s            t = 3 s            t = 6 s                     t = 30 s
+--------------+   +--------------+   +--------------+            +------------------+
| Msg 1 (Pos1) |   | Msg 1 (Pos2) |   | Msg 1 (Pos3) |   ...      | Msg 8 (Signature)|
| [Single Slot]|   | [Single Slot]|   | [Single Slot]|            | [Multi-Slot ASM] |
+--------------+   +--------------+   +--------------+            +------------------+
       |                  |                  |                             |
       +------------------+------------------+-----------------------------+
                                      |
                         Hash: H(Pos1 || Pos2 || ... || PosN)
                                      |
                         Verify: ECDSA_Verify(PK, Hash, Sig)
```

To minimize over-the-air footprint, Wimpenny et al. evaluated short-signature schemes, demonstrating that Edwards-curve Ed25519 or pairing-based BLS signatures provide an optimal balance between computational overhead and bit economy. By restricting signature transmission to a fraction of the position reporting rate, the VDL loading increase is held below $5\%$ to $10\%$, avoiding the catastrophic channel saturation of naive per-message signing.

### 64.2.4 Identity-Based Cryptography (Goudossis & Katsikas)
A pervasive challenge in any maritime public key architecture is public key distribution. How does a receiving ship in the middle of the Pacific Ocean obtain and verify the public key of a newly encountered vessel without real-time internet connectivity?

Goudossis and Katsikas (2019, 2020) proposed resolving this certificate distribution problem by deploying **Identity-Based Cryptography (IBC)**. In an identity-based cryptosystem:
- An entity's public key is directly derived from a publicly known, unique identifier string—specifically the vessel's 9-digit MMSI or 7-digit IMO ship identification number:
  $$\text{PK}_{\text{vessel}} = \text{KDF}(\text{MMSI} \parallel \text{IMO Number} \parallel \text{Validity Period})$$
- A trusted Private Key Generator (**PKG**)—such as an international registry operated by the IMO, ITU, or flag state administrations—issues the corresponding private key during annual vessel safety surveys.
- When a ship receives a signed AIS transmission, the receiver does not need to query a remote directory or download an X.509 digital certificate. The receiver derives the transmitter's public key directly from the MMSI encoded in the message header and verifies the signature immediately.

While eliminating over-the-air certificate delivery, identity-based cryptography introduces severe administrative complexities:
- **Private Key Escrow:** Because the PKG generates private keys from identities, the central authority inherently possesses the private keys of all commercial vessels worldwide. A compromise of the PKG root compromise would invalidate the security of the entire global fleet.
- **Key Revocation and Expiration:** To support revocation (e.g., when a transponder is decommissioned, compromised, or sold to a new flag), identity strings must include temporal validity windows (e.g., `MMSI:366999701:YEAR:2026`). Receivers must maintain synchronized trust parameters and periodically update master public parameters through coastal base stations or satellite links.

> **Threat model.**
> - **Attacker Capabilities:** Malicious actor using open-source SDR toolkits (e.g., GNU Radio, HackRF) to synthesize GMSK waveforms; capable of arbitrary bit stuffing, HDLC framing, and CRC generation; able to spoof vessel kinematics, MMSIs, and geographic positions.
> - **Attack Vectors:** Over-the-air injection of phantom ships; spoofing search-and-rescue beacons (AIS-SART); spoofing aids to navigation (virtual AtoNs); replaying recorded maritime telemetry bursts.
> - **Impact:** Tactical confusion on navigation bridges; false CPA/TCPA collision alarms inducing evasive maneuvers into physical hazards; masking of sanctioned petroleum transfers and illegal fishing vessels.
> - **Mitigations:** Multi-message cryptographic signature encapsulation in ASM; identity-based public key verification; receiver-side kinematic plausibility gating; physical-layer RF fingerprinting; transition to native VDES security architectures.

## 64.3 VDES and modern security architectures

Recognizing that the legacy AIS VHF Data Link cannot natively support modern cryptographic protocols without severe compromise, the international maritime community designed its successor: the **VHF Data Exchange System (VDES)** ([Chapter 69](ch69-vdes-ais-2.md)). Standardized by the ITU in Recommendation ITU-R M.2092 (editions M.2092-0 in 2015, M.2092-1 in 2022, and M.2092-2 in February 2026), VDES establishes an integrated maritime radio ecosystem comprising four distinct functional components:

```
+-----------------------------------------------------------------------------------+
|                        VHF Data Exchange System (VDES)                            |
|                                                                                   |
|  +--------------------+  +--------------------+  +-----------------------------+  |
|  |    Legacy AIS      |  |      ASM 1 & 2     |  |    VDE-TER / VDE-SAT        |  |
|  | (161.975 / 162.025)|  | (161.950 / 162.000)|  | (157.200 - 162.000 MHz)    |  |
|  |  GMSK @ 9.6 kbit/s |  |  π/4-QPSK @ 19.2   |  | 25-100 kHz Bandwidth        |  |
|  | Unauthenticated    |  | Dedicated ASM link |  | QPSK, 16-QAM up to 307 kbit/s|  |
|  | Safety of Life     |  | Relieves AIS load  |  | Cryptographic Bearer Link   |  |
|  +--------------------+  +--------------------+  +-----------------------------+  |
+-----------------------------------------------------------------------------------+
```

1. **AIS Component:** Preserves core legacy AIS 1 and AIS 2 channels (161.975 MHz and 162.025 MHz; Appendix 18 channels 2087 and 2088) using standard 9.6 kbit/s GMSK modulation, guaranteeing universal backward compatibility with all existing SOLAS equipment.
2. **Application-Specific Message (ASM) Component:** Migrates binary data messages off legacy AIS channels to two dedicated 25 kHz simplex frequencies: ASM 1 (161.950 MHz, channel 2027) and ASM 2 (162.000 MHz, channel 2028). Utilizing $\pi/4$-QPSK modulation, ASM delivers 19.2 kbit/s, instantly doubling binary data throughput while liberating AIS 1 and AIS 2 for core collision-avoidance telemetry.
3. **VDE Terrestrial (VDE-TER) Component:** Allocates contiguous multi-channel blocks across maritime VHF frequencies (157.200–157.325 MHz lower leg; 161.800–161.925 MHz upper leg). Supporting contiguous channel bandwidths of 25 kHz, 50 kHz, and 100 kHz, VDE-TER employs higher-order digital modulations—including QPSK, 8-PSK, and 16-QAM—achieving raw physical layer bit rates up to **307.2 kbit/s** (a 32-fold throughput increase over legacy AIS).
4. **VDE Satellite (VDE-SAT) Component:** Standardized internationally at the World Radiocommunication Conferences WRC-15 and WRC-19, VDE-SAT provides two-way low Earth orbit (**LEO**) satellite communication directly within the maritime VHF band.

### 64.3.1 VDES security framework: ITU-R M.2092-1 and M.2092-2
Recommendation ITU-R M.2092 incorporates native security mechanisms into the VDE protocol stack. Unlike legacy AIS, which lacks any concept of session state or entity authentication, VDES organizes data exchange across structured logical channels:
- **Broadcast Logical Channel:** Transmits unaddressed or general maritime safety information.
- **Addressed Logical Channel:** Establishes point-to-point connections between ship stations, coastal base stations, and satellite payloads.
- **Announced Logical Channel:** Schedules bulk binary data transfers.

The VDE Lower Link Controller (**LLC**) and Medium Access Control (**MAC**) layers incorporate native frame fields for message authentication codes, session sequence counters, and security capability negotiation. Because VDE channels operate at bandwidths up to 100 kHz with payload capacities exceeding thousands of bits per burst, the physical bit budget constraints that crippled legacy AIS authentication are eliminated. A single VDE-TER or VDE-SAT frame can comfortably encapsulate standard X.509 digital certificates, 512-bit ECDSA/Ed25519 signatures, and complete S-100 navigational data payloads ([Chapter 52](ch52-ais-and-s100.md)).

### 64.3.2 IALA Guideline G1192 and Message 28
The operational bridge between legacy AIS and modern authenticated architectures is codified in the newest revisions of ITU and IALA standards:
1. **The Message 28 Single-Slot AtoN Report:** Adopted in Recommendation ITU-R M.1371-6 (2026), Message 28 is a newly defined 168-bit single-slot Aid-to-Navigation report designed to deliver the essential telemetry of legacy 2-slot Message 21 within a single TDMA slot ([Chapter 22](ch22-message-catalog.md)). Crucially, bit 167 of Message 28 is defined as the **Authentication Flag**.
2. **IALA Guideline G1192:** ITU-R M.1371-6 Annex 7 Table 84 explicitly specifies that when the Authentication Flag in Message 28 is set to `1`, the AtoN transmission is **"authenticated per IALA G1192"**. Guideline G1192 defines the technical architecture for VDES and AIS authentication, specifying how public keys are bound to Maritime Resource Names (**MRNs**) under IALA Guideline G1143.
3. **The IALA ASM Collection Authentication Message:** Registered in the official IALA ASM register (with initial proposals submitted December 2022), designated VDES-ASM message identifiers under DAC 1/2/4 establish standardized envelopes for "AIS Message Authentication". These messages broadcast digital signatures over the dedicated ASM channels (2027 and 2028), validating the authenticity of physical, synthetic, and virtual AtoNs without occupying legacy AIS slots.

```
+-----------------------------------------------------------------------------+
| Recommendation ITU-R M.1371-6 Message 28: Bit Layout (168 bits, 1 slot)     |
| +-------------------------------------------------------------------------+ |
| | Msg ID (6) | Repeat (2) | MMSI / Source ID (30) | Time Stamp (6)        | |
| +-------------------------------------------------------------------------+ |
| | Longitude (28)                   | Latitude (27)                        | |
| +-------------------------------------------------------------------------+ |
| | Restricted (2) | Type (3) | AtoN Type (7) | IALA AtoN MRN (17)          | |
| +-------------------------------------------------------------------------+ |
| | Dim Type (4) | Dim A (9) | Dim B (11) | Add Data (1) | Charted (1)     | |
| +-------------------------------------------------------------------------+ |
| | On-Station (4) | AtoN Status (8) | Spare (1) | Authentication Flag (1)  | |
| +-------------------------------------------------------------------------+ |
|                                                      |                      |
|                                                      +--> 0 = Unauthenticated
|                                                           1 = Authenticated 
|                                                               (IALA G1192)  |
+-----------------------------------------------------------------------------+
```

### 64.3.3 Maritime Public Key Infrastructure (PKI)
To operationalize cryptographic authentication across hundreds of thousands of commercial, military, and private vessels, the maritime sector is establishing a federated **Maritime Public Key Infrastructure (Maritime PKI)**:

```
                           +------------------------+
                           |  IMO / IALA Root CA    |
                           +------------------------+
                                       |
                   +-------------------+-------------------+
                   |                                       |
       +-----------------------+               +-----------------------+
       | National Flag State CA|               | Authorized Maritime CA|
       |  (e.g., USCG, DMA)    |               |  (Class Societies)    |
       +-----------------------+               +-----------------------+
                   |                                       |
         +---------+---------+                   +---------+---------+
         |                   |                   |                   |
   +-----------+       +-----------+       +-----------+       +-----------+
   | Class A   |       | Coastal   |       | Virtual   |       | Commercial|
   | Transponder|      | Base Stn  |       | AtoN Stn  |       | Fleet     |
   | Identity  |       | Identity  |       | Identity  |       | Operator  |
   +-----------+       +-----------+       +-----------+       +-----------+
```

- **Root Certificate Authorities:** Operated under international governance (jointly recognized by IMO, ITU, and IALA), root CAs anchor trust for maritime identities.
- **Intermediate CAs (Flag States and Recognized Organizations):** National maritime administrations (such as the United States Coast Guard or Danish Maritime Authority) and accredited classification societies (such as DNV, Lloyd's Register, or ABS) issue digital certificates bound to official ship identification parameters.
- **Identity Binding:** Certificates bind the vessel's cryptographic public key to its immutable **IMO Ship Identification Number** (which remains with the hull throughout its life) and its dynamically assigned **MMSI** ([Chapter 13](ch13-mmsi-deep-dive.md)).
- **Certificate Revocation and Delta Lists:** Vessels update certificate revocation lists (**CRLs**) via VDE-SAT or coastal VDE-TER broadcasts, ensuring that compromised transponders or rogue "dark fleet" operators can be revoked globally.

## 64.4 Data-provider-side trust scoring

While cryptographic standards mature and global fleets transition toward VDES, collection networks cannot wait for universal hardware replacement. Terrestrial and satellite aggregators—such as Spire Maritime, Kpler, and Global Fishing Watch—ingest tens of millions of raw AIS messages daily ([Chapter 41](ch41-networks-and-providers.md); [Chapter 50](ch50-big-data-architecture.md)). To deliver reliable intelligence to coast guards and safety centers, aggregators deploy multi-layer software **trust scoring engines**. Trust scoring operates on a zero-trust model: every incoming AIS sentence is treated as untrusted telemetry until validated against multi-sensor physical reality and historical kinematic baselines (Iphar, Ray & Napoli 2020; Ray, Iphar & Napoli 2024).

```
                      Multi-Stage Aggregator Trust Scoring Engine
                                           |
+------------------------------------------v------------------------------------------+
| 1. Physical Layer: RSSI footprint, Direction Finding (DF) & TDOA Geolocation        |
+-------------------------------------------------------------------------------------+
                                           |
+------------------------------------------v------------------------------------------+
| 2. Kinematic & Geometric Plausibility: Velocity & turn limits, bathymetry bounds     |
+-------------------------------------------------------------------------------------+
                                           |
+------------------------------------------v------------------------------------------+
| 3. Registry & Identity Integrity: MMSI allocation (M.585), cross-check with IMO/MARS|
+-------------------------------------------------------------------------------------+
                                           |
+------------------------------------------v------------------------------------------+
| 4. Spaceborne Earth Observation (EO): SAR hull detection, optical cross-correlation |
+-------------------------------------------------------------------------------------+
                                           |
                                           v
                          Composite Track Trust Score: S in [0, 100]
```

### 64.4.1 Kinematic gating algorithms
The primary defense against synthetic track generation is automated kinematic gating ([Chapter 47](ch47-data-quality-track-reconstruction.md)). A vessel possessing mass, momentum, and hydrodynamically bounded propulsion cannot undergo instantaneous spatial displacements.

When a receiver or aggregation pipeline decodes consecutive position reports $P_{k-1} = (\phi_{k-1}, \lambda_{k-1}, t_{k-1})$ and $P_k = (\phi_k, \lambda_k, t_k)$, the pipeline computes the great-circle orthodromic distance $d(P_{k-1}, P_k)$ using the haversine formula:

$$a = \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_{k-1})\cos(\phi_k)\sin^2\left(\frac{\Delta \lambda}{2}\right)$$

$$d = 2 R_{\text{earth}} \arcsin\left(\sqrt{a}\right)$$

The implied speed over ground $v_{\text{implied}}$ is then evaluated against the time delta $\Delta t = t_k - t_{k-1}$:

$$v_{\text{implied}} = \frac{d(P_{k-1}, P_k)}{\Delta t}$$

The report is flagged as an anomaly if:
1. **Speed Exceedance:** $v_{\text{implied}} > v_{\text{max}}(\text{type})$, where $v_{\text{max}}$ is parameterized by vessel type (e.g., $45\text{ kn}$ for commercial container ships; $60\text{ kn}$ for high-speed craft).
2. **Velocity Discrepancy:** $|v_{\text{implied}} - \text{SOG}_{\text{reported}}| > \epsilon_v$ (where $\epsilon_v$ is typically $5\text{ kn}$ for settled cruising).
3. **Teleportation Vector:** $d > 1.0\text{ nmi}$ within $\Delta t < 60\text{ s}$, a signature of dual-transmitter MMSI cloning where an illicit vessel and a compliant ship alternate transmissions.

> **Try it.**
> You can test track plausibility using the handbook's kinematic validation utility. Execute the script within the repository virtual environment against synthetic harbor telemetry:
> ```bash
> cd /usr/local/google/home/schwehr/sdd-books/ais/fable
> . .venv/bin/activate
> python code/security/kinematic_checks.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95
> ```
> Expected output:
> ```text
>      mmsi  score  fixes  speed_violations  max_implied_kn  sog_mismatch  turn_violations  teleports  beyond_range  max_range_nmi  invalid_mmsi
>         0      1     28                 0       12.031859             0                0          0             0      16.324760             1
>   1193046      1    120                 0        4.517441             0                0          0             0       5.134594             1
> 244999703      0    126                 0       14.544945             0                0          0             0      32.674542             0
> 316999704      0    301                 0       20.051188             0                0          0             0      26.229610             0
> 338123456      0    121                 0        6.018214             0                0          0             0       7.653746             0
> 338654321      0    120                 0        7.515078             0                0          0             0      12.274265             0
> 338999702      0    349                 0       18.043446             0                0          0             0      19.489121             0
> 366999701      0    326                 0       12.053396             0                0          0             0      18.276030             0
>
> score >= 2 deserves a second look; score alone never proves spoofing.
> ```

### 64.4.2 Cross-validation via independent sensors
Data providers fuse multiple non-cooperative surveillance layers to validate unauthenticated AIS tracks ([Chapter 66](ch66-other-ways-to-track-ships.md)):
- **Spaceborne Synthetic Aperture Radar (SAR):** Satellites such as Sentinel-1, TerraSAR-X, and commercial constellations (e.g., ICEYE, Capella Space) image oceanic surfaces through cloud cover and darkness. SAR algorithms detect metallic vessel hull returns (radar cross-section reflections). By cross-correlating SAR vessel positions with AIS broadcasts received within the identical satellite pass window ($\Delta t \le \pm 10\text{ minutes}$), algorithms classify contacts into three bins:
  1. *Corroborated Targets:* AIS track matches a physical SAR hull return within positional error bounds.
  2. *Dark Targets:* SAR detects a physical vessel hull, but no corresponding AIS signal is present within $15\text{ nmi}$ (transponder disabled or suppressed).
  3. *Ghost/Spoofed Targets:* AIS broadcast reports a vessel at coordinates $(\phi, \lambda)$, but high-resolution SAR imagery confirms open water with zero radar backscatter.
- **Multi-Station TDOA and Direction Finding:** Terrestrial coastal sensor arrays and specialized RF reconnaissance satellites (such as Hawkeye 360) calculate Time Difference of Arrival (**TDOA**) and Frequency Difference of Arrival (**FDOA**) across raw RF pulse bursts ([Chapter 35](ch35-direction-finding-geolocation.md)). If the hyperbolic intersection of arrival times places the transmitter $150\text{ nmi}$ away from the coordinates encoded in the AIS message payload, the transmission is definitively classified as an electronic spoof.

## 64.5 Cost, benefit, and migration paths

Transitioning global maritime shipping from unauthenticated legacy broadcasts to an authenticated, resilient infrastructure is fundamentally an economic and institutional challenge rather than a purely cryptographic one. Maritime safety regulations require global consensus through the IMO Maritime Safety Committee (**MSC**), rigorous type-approval standards codified by the International Electrotechnical Commission (**IEC**), and disciplined spectrum coordination via the ITU World Radiocommunication Conferences.

```
       Timeline of Maritime Situational Awareness Transition
 1998                     2015           2024          2026          2028                 2035+
---|-----------------------|--------------|-------------|-------------|--------------------|--->
 ITU-R M.1371          ITU-R M.2092-0  MSC.1/Circ    ITU-R M.2092-2  SOLAS VDES         Legacy AIS
 Cleartext AIS         Initial VDES    1460/Rev.2    M.1371-6        In Force           Sunset /
 Standard              Concept         ASM/VDE Open  Msg 28 Adopted  Permitted Alt      Secondary Role
```

### 64.5.1 The three-phase transition model
The international maritime community has embarked on a structured multi-decade migration path:

1. **Phase 1: Dual-Bearer Coexistence (2024–2028):** In accordance with IMO MSC.1/Circ.1460/Rev.2, digital use of designated VDES frequencies (ASM 1/2 and VDE channels) became globally operational on 1 January 2024. IMO MSC 111 (May 2026) adopted SOLAS amendments (Resolution MSC.592(111)) and VDES Performance Standards (Resolution MSC.593(111)), permitting VDES as an alternative to legacy AIS transponders from **1 January 2028**. Dual-mode shipborne transponders conforming to IEC 63514 enter the commercial fleet, listening and transmitting on both legacy AIS 1/2 and new ASM/VDE channels.
2. **Phase 2: Offloading Binary and Administrative Payloads (2028–2032):** Application-Specific Messages and administrative traffic are systematically transferred off AIS 1 and AIS 2 onto dedicated ASM channels (2027 and 2028) and VDE-TER. Legacy channels are preserved exclusively for single-slot Class A and Class B position reports, restoring VDL safety margins. Authenticated AtoN reports (Message 28) and signed ASM payloads provide cryptographic validation for high-risk navigation marks.
3. **Phase 3: Cryptographically Authenticated Maritime VHF Link (2032+):** As next-generation VDES equipment saturates the SOLAS commercial fleet, maritime administrations will mandate cryptographic authentication on primary navigation reports over VDE channels. Autonomous Surface Ships (**MASS**) operating under the mandatory MASS Code ([Chapter 57](ch57-autonomous-ships.md)) mandate authenticated machine-to-machine telemetry, rejecting unauthenticated cleartext contacts in automated collision-avoidance algorithms.

> **Legal note.**
> Under Regulation 19 of Chapter V of the International Convention for the Safety of Life at Sea (**SOLAS**), all passenger ships regardless of size and all cargo ships of 300 gross tonnage (**GT**) and upwards on international voyages are legally mandated to carry an Automatic Identification System transponder.
>
> - **Operational Mandate:** The IMO Guidelines for the Onboard Operational Use of Shipborne AIS (Resolution A.1106(29)) stipulate that AIS shall be operated continuously at sea and in port, unless the master determines that continuous operation would compromise the safety or security of the vessel (e.g., in pirate-infested waters).
> - **Permissive Alternative Status:** Amendments adopted at IMO MSC 111 (May 2026) formally recognize type-approved shipborne VDES installations conforming to Resolution MSC.593(111) as satisfying SOLAS Chapter V Regulation 19 carriage requirements, entering into force on 1 January 2028.
> - **Illicit Signal Generation:** Transmitting unauthorized, synthesized, or forged AIS waveforms over maritime VHF frequencies violates national telecommunications statutes (e.g., United States 47 U.S.C. § 301 and 47 CFR Part 80; United Kingdom Wireless Telegraphy Act 2006) and constitutes malicious interference under the ITU Radio Regulations (Article 15). Falsifying maritime identification numbers (MMSI) is punishable under international maritime fraud statutes and port state jurisdiction.

## Then & now
How maritime situational awareness, transponder architectures, and authentication mechanisms evolved over three decades:

- **1998 ⟨H⟩:** ITU-R M.1371-1 standardizes the Automatic Identification System using 9.6 kbit/s GMSK over maritime VHF channels AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz); system is completely unauthenticated, assuming honest mariners and expensive proprietary radio hardware.
- **2002 ⟨H⟩:** IMO SOLAS Chapter V Regulation 19 carriage requirement enters into force, requiring commercial vessels over 300 GT to carry Class A transponders.
- **2014 ⟨H⟩:** Trend Micro researchers (Balduzzi, Pasta & Wilhoit) publish landmark security evaluation of AIS, using low-cost SDRs to demonstrate over-the-air vessel spoofing, ghost fleets, fake search-and-rescue beacons, and slot-starvation denial-of-service.
- **2015 ⟨+⟩:** ITU-R M.2092-0 standardizes the initial technical framework for the VHF Data Exchange System (**VDES**), reserving spectrum for dedicated ASM and broadband VDE channels.
- **2017 ⟨+⟩:** First dedicated VDES satellite payload flown on Norway's NorSat-2, demonstrating VDE-SAT data exchange in polar orbits.
- **2018 ⟨+⟩:** Wimpenny, Šafář, and Grant present public-key broadcast authentication frameworks for AIS and VDES at ION GNSS+ 2018, demonstrating backward-compatible signature distribution.
- **2019 ⟨+⟩:** WRC-19 finalizes international frequency allocations for VDES satellite components (VDE-SAT) under Radio Regulations Appendix 18; Goudossis and Katsikas publish identity-based encryption architectures for maritime tracking.
- **2020 ⟨+⟩:** Gary C. Kessler publishes Protected AIS (**pAIS**) field trial results in *TransNav*, demonstrating AES/HMAC encapsulation in binary AIS containers.
- **2022 ⟨+⟩:** ITU-R M.2092-1 updates VDES technical characteristics; IALA Guideline G1117 Edition 3.0 defines operational concept of operations; IALA registers official VDES-ASM message formats for AIS authentication.
- **2024 ⟨+⟩:** IMO MSC.1/Circ.1460/Rev.2 establishes 1 January 2024 as the global date from which operational use of ASM and VDE frequencies is authorized; IALA transitions to intergovernmental organization (**IGO**) status on 22 August 2024.
- **2026 ⟨+⟩:** ITU-R M.1371-6 (2026) adopts single-slot Message 28 with a dedicated **Authentication Flag** linked to IALA Guideline G1192; ITU-R M.2092-2 (February 2026) updates VDES specifications; IMO MSC 111 (May 2026) adopts Resolutions MSC.592(111) and MSC.593(111) permitting VDES as an alternative to AIS under SOLAS, effective 1 January 2028.

## Validation, uncertainty & data quality
How security data quality is evaluated, how cryptographic and kinematic errors arise, and how systems manage uncertainty:

1. **Error Sources in Maritime Trust Engines:**
   - *Ephemeris and GNSS Jitter:* Legitimate commercial GNSS receivers experience horizontal dilution of precision (**HDOP**) variations, multipath reflections from container stacks, and occasional receiver clock drift, generating false speed spikes up to $2\text{ to }4\text{ kn}$ in tight harbor channels ([Chapter 25](ch25-gnss-and-ais.md)).
   - *Atmospheric RF Ducting:* Tropospheric ducting across warm sea surfaces can extend terrestrial VHF line-of-sight propagation from normal horizons ($20\text{ to }30\text{ nmi}$; $37\text{ to }56\text{ km}$) to more than $150\text{ to }300\text{ nmi}$ ($278\text{ to }556\text{ km}$) ([Chapter 29](ch29-propagation-modeling.md)). Trust filters that naively drop reports exceeding theoretical line-of-sight will generate high false-alarm rates during summer temperature inversions.
   - *Clock Drift in Time-Stamped Signatures:* Cryptographic timestamp validation requires transmitters and receivers to maintain synchronized time. If a ship's master clock drifts by more than the accepted verification tolerance window (typically $\pm 10\text{ seconds}$), valid cryptographic signatures will be rejected as replay attacks.
2. **Quantifying Authentication Error Probabilities:**
   - In delayed-disclosure broadcast schemes (TESLA), the probability of an adversary successfully forging an authenticating HMAC tag prior to key disclosure is bounded strictly by the bit length $b$ of the truncated tag:
     $$P_{\text{forge}} = \frac{1}{2^b}$$
     For a 32-bit truncated HMAC, $P_{\text{forge}} \approx 2.33 \times 10^{-10}$; for a 64-bit tag, $P_{\text{forge}} \approx 5.42 \times 10^{-20}$.
   - In elliptic-curve digital signatures (ECDSA P-256 or Ed25519), the security strength against existential forgery under chosen-message attacks is equivalent to $128\text{ bits}$ of symmetric security, rendering computational forgery impossible against classical adversaries.
3. **Multi-Receiver Cross-Validation Procedures:**
   - *Step 1: Signal Ingestion:* Record arrival timestamp $t_{\text{rx}}$ (with nanosecond-precision GPS-locked timebase), Received Signal Strength Indicator (**RSSI**), and raw I/Q samples across multiple synchronized coastal SDR base stations.
   - *Step 2: Message Decapsulation:* Extract reported latitude, longitude, MMSI, and time stamp from Message 1/2/3.
   - *Step 3: TDOA Hyperbolic Positioning:* Compute pair-wise Time Difference of Arrival hyperbolas across at least three non-collinear receivers:
     $$\Delta d_{ij} = c \cdot (t_{\text{rx}, i} - t_{\text{rx}, j})$$
     Estimate the physical emitter coordinates $(\hat{x}, \hat{y})$ via non-linear least squares.
   - *Step 4: Residual Distance Assessment:* Calculate the Euclidean discrepancy between physical RF emission origin and reported position:
     $$\epsilon_{\text{pos}} = \| (\hat{x}, \hat{y}) - (\phi_{\text{rep}}, \lambda_{\text{rep}}) \|$$
     If $\epsilon_{\text{pos}} > 3\sigma_{\text{TDOA}}$ (where typical terrestrial VHF TDOA accuracy is $0.5\text{ to }2.0\text{ nmi}$), flag the transmission as an active geographic spoof.

## Software
- **Open source:**
  - `libais` (Python/C++ library): High-performance open-source decoding library for ITU-R M.1371 AIS messages and legacy binary ASMs; does not parse emerging VDES physical frames or evaluate cryptographic signatures.
  - `pyais` (Python library): Comprehensive open-source AIS message decoder supporting NMEA 0183 AIVDM/AIVDO sentences and international DAC 1 Application-Specific Messages; strictly a message parser without link-layer authentication validation.
  - `gnuradio-ais` / `gr-ais` (GNU Radio out-of-tree module): Open-source digital signal processing flowgraphs for demodulating GMSK maritime waveforms using software-defined radios; requires external post-processing pipelines for kinematic validation and anomaly detection.
- **Free but closed:**
  - *USCG NAVCEN AIS Parser / Tools*: Technical decoding and formatting utilities provided by the United States Coast Guard Navigation Center; tailored to regulatory compliance and official USCG ASM formats, with no public-key validation features.
- **Commercial:**
  - *Spire Maritime Maritime API & Anomaly Detection*: Global satellite and terrestrial AIS ingestion pipeline providing proprietary machine-learning kinematic validation, dark-vessel detection, and multi-sensor fusion; subscription-based commercial service with proprietary trust scoring algorithms.
  - *Kpler (MarineTraffic / FleetMon) Maritime Intelligence Platform*: Commercial vessel tracking system incorporating automated track-plausibility filtering, terrestrial receiver health checks, and sanctions screening; closed-source enterprise database.

## Standards & guides
- **ITU-R Recommendation M.1371-5 (2014) & M.1371-6 (2026):** *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band.* Defines physical, link, and transport layers for AIS; M.1371-6 introduces Message 28 with the single-bit Authentication Flag.
- **ITU-R Recommendation M.2092-1 (2022) & M.2092-2 (2026):** *Technical characteristics for a VHF data exchange system in the VHF maritime mobile band.* The foundational specification for VDES, defining channel plans, higher-order modulations, logical data channels, and native security provisions.
- **IALA Guideline G1117 (Edition 3.0, 2022):** *VHF Data Exchange System (VDES) Overview.* Comprehensive guidance on VDES operational architecture, migration timelines, and channel utilization.
- **IALA Guideline G1192 (Edition 1.0, 2024):** *VDES Authentication and Key Management.* Defines cryptographic authentication, certificate hierarchies, and key management frameworks for VDES and AIS.
- **IALA Guideline G1139:** *The Technical Specification of VDES.* Base specification for initial VDES architecture; **formally withdrawn** following incorporation into ITU-R M.2092-1.
- **IMO Resolution MSC.593(111) (2026):** *Performance Standards for Shipborne VHF Data Exchange System (VDES) Equipment.* Defines regulatory requirements for shipborne VDES equipment permitted under SOLAS Chapter V Regulation 19 from 1 January 2028.
- **IEC 61993-2 (Edition 3.0, 2018):** *Maritime navigation and radiocommunication equipment and systems – Automatic Identification Systems (AIS) – Part 2: Class A shipborne equipment.* Type-approval test standard governing legacy Class A transponders.
- **IEC 63514 (in development, 2026):** *Maritime navigation and radiocommunication equipment and systems – VHF Data Exchange System (VDES) – Operational and performance requirements, methods of testing and required test results.* Type-approval standard for shipborne VDES hardware.

## Pitfalls
1. **Assuming single-slot position reports can host standard digital signatures:** Overlooking that Message 1, 2, and 3 payloads utilize $100\%$ of available 168-bit slot capacity. Any scheme attempting to append 512-bit Ed25519 or ECDSA signatures in-band forces 4-slot transmissions, which saturates the VDL and collapses the network.
2. **Treating symmetric encryption as a universal broadcast solution:** Deploying pre-shared symmetric keys (as in basic pAIS configurations) for civilian maritime tracking. Symmetric keys cannot scale globally without catastrophic key compromise and render vessels invisible to non-enrolled bridge systems, destroying collision-avoidance safety.
3. **Ignoring the verification latency of delayed-disclosure protocols:** Utilizing TESLA broadcast chains without accounting for safety-critical collision dynamics. Fast-closing vessels cannot wait 5 to 15 seconds for key disclosure before determining whether an ECDIS target is genuine.
4. **Failing to preserve backward compatibility for legacy transponders:** Formatting modified AIS packets that crash or corrupt unpatched Class A/B decoders, violating IMO grandfathering principles and SOLAS compliance.
5. **Relying on public key infrastructure without addressing offline certificate distribution:** Assuming oceanic vessels possess continuous broadband internet access to download large X.509 certificate chains or query online Certificate Revocation Lists (**CRLs**).
6. **Confusing AIS message spoofing with GNSS jamming and spoofing:** Treating a falsified AIS position as a compromised radio protocol when the transponder is operating correctly but broadcasting corrupted coordinates fed by an attacked GNSS antenna.
7. **Neglecting receiver buffer limits during delayed authentication:** Designing broadcast authentication protocols that require decoders to buffer unverified messages, creating trivial memory exhaustion Denial-of-Service vulnerabilities under SDR flooding attacks.
8. **Dismissing atmospheric ducting when setting kinematic and geographic plausibility bounds:** Assuming that any terrestrial VHF report received beyond 50 nmi is fraudulent, inadvertently rejecting genuine emergency broadcasts during tropospheric ducting events.
9. **Treating software-side trust scores as absolute proof of physical deception:** Concluding that an unusual kinematic score definitively indicates malicious spoofing without cross-validating against primary radar, SAR imagery, or multi-station TDOA bearings.
10. **Citing withdrawn standards as governing specifications:** Referencing IALA Guideline G1139 as current VDES guidance rather than citing its successor, Recommendation ITU-R M.2092-1/-2, and IALA Guideline G1117.

## Key takeaways
- Legacy AIS broadcasts cannot be cryptographically signed in-band without violating rigid 256-bit slot boundaries, overloading spectrum capacity, or breaking hundreds of thousands of installed transponders.
- SOTDMA slot mathematics leaves exactly 168 bits of usable payload per single-slot burst; standard Class A position reports consume $100\%$ of this capacity, leaving zero bits for signatures.
- Appending standard 512-bit elliptic-curve signatures (ECDSA or Ed25519) expands position bursts to 4 slots, which would increase channel loading beyond $350\%$ and cause catastrophic packet collisions in congested waters.
- Out-of-band broadcast authentication—decoupling routine position reports from periodic cryptographic signature bursts encapsulated in Application-Specific Messages (Wimpenny et al.)—provides a viable backwards-compatible bridge.
- The VHF Data Exchange System (VDES), governed by ITU-R M.2092, resolves spectrum bottlenecks by moving binary data to dedicated ASM channels (19.2 kbit/s) and wideband VDE channels (up to 307.2 kbit/s).
- Recommendation ITU-R M.1371-6 introduces Message 28 with an **Authentication Flag** linked directly to IALA Guideline G1192, establishing standardized cryptographic verification for Aids to Navigation.
- IMO MSC 111 (May 2026) adopted Performance Standards for shipborne VDES (Resolution MSC.593(111)), permitting VDES as an authorized alternative to legacy AIS under SOLAS Chapter V effective 1 January 2028.
- Downstream data providers enforce security today through zero-trust heuristic engines, combining kinematic gating, atmospheric propagation modeling, multi-station TDOA cross-bearings, and spaceborne Synthetic Aperture Radar (SAR) cross-correlation.

## References
- Balduzzi, M., Wilhoit, K., Pasta, A. (2014). *A Security Evaluation of AIS: Automated Identification System*. Tokyo: Trend Micro Research. URL: https://documents.trendmicro.com/assets/white_papers/wp-a-security-evaluation-of-ais.pdf
- Goudossis, A., Katsikas, S. K. (2019). Towards a secure automatic identification system (AIS). *Journal of Marine Science and Technology*, 24(2):410–423. doi:10.1007/s00773-018-0561-3
- Goudossis, A., Katsikas, S. K. (2020). Secure AIS with Identity-Based Authentication and Encryption. *TransNav: International Journal on Marine Navigation and Safety of Sea Transportation*, 14(2):287–296. doi:10.12716/1001.14.02.03
- IALA (2017). *Guideline G1139: The Technical Specification of VDES*. Edition 1.0 (Withdrawn). Saint-Germain-en-Laye: IALA.
- IALA (2022). *Guideline G1117: VHF Data Exchange System (VDES) Overview*. Edition 3.0. Saint-Germain-en-Laye: IALA.
- IALA (2024). *Guideline G1192: VDES Authentication and Key Management*. Edition 1.0. Saint-Germain-en-Laye: IALA.
- IEC (2016). *IEC 62320-2:2016 — Maritime navigation and radiocommunication equipment and systems – Automatic Identification Systems (AIS) – Part 2: AIS Aids to Navigation (AtoN) stations – Operational and performance requirements, methods of test and required test results*. Edition 2.0. Geneva: IEC.
- IEC (2018). *IEC 61993-2:2018 — Maritime navigation and radiocommunication equipment and systems – Automatic Identification Systems (AIS) – Part 2: Class A shipborne equipment of the automatic identification system (AIS) – Operational and performance requirements, methods of test and required test results*. Edition 3.0. Geneva: IEC.
- IEC (2018). *IEC 62923-1:2018 — Maritime navigation and radiocommunication equipment and systems – Bridge alert management – Part 1: Operational and performance requirements, methods of testing and required test results*. Edition 1.0. Geneva: IEC.
- IMO (2026). *Performance Standards for Shipborne VHF Data Exchange System (VDES) Equipment*. Resolution MSC.593(111). London: International Maritime Organization.
- Iphar, C., Ray, C., Napoli, A. (2020). Data Quality Assessment on Simulated and Real-World Maritime Tracking Data. *Journal of Marine Science and Engineering*, 8(7):478. doi:10.3390/jmse8070478
- ITU-R (2014). *Recommendation ITU-R M.1371-5: Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Geneva: International Telecommunication Union.
- ITU-R (2022). *Recommendation ITU-R M.2092-1: Technical characteristics for a VHF data exchange system in the VHF maritime mobile band*. Geneva: International Telecommunication Union.
- ITU-R (2026). *Recommendation ITU-R M.1371-6: Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Geneva: International Telecommunication Union.
- ITU-R (2026). *Recommendation ITU-R M.2092-2: Technical characteristics for a VHF data exchange system in the VHF maritime mobile band*. Geneva: International Telecommunication Union.
- Kessler, G. C. (2020). Protected AIS (pAIS): A Demonstration of Authenticated, Encrypted Automatic Identification System Message Exchange. *TransNav: International Journal on Marine Navigation and Safety of Sea Transportation*, 14(2):279–286. doi:10.12716/1001.14.02.02
- Kessler, G. C., Craiger, J. P., Haass, J. C. (2018). A Taxonomy of Maritime Cybersecurity Vulnerabilities and Mitigations. *TransNav: International Journal on Marine Navigation and Safety of Sea Transportation*, 12(3):429–437. doi:10.12716/1001.12.03.01
- Perrig, A., Canetti, R., Tygar, J. D., Song, D. (2002). The TESLA Broadcast Authentication Protocol. *RSA Laboratories CryptoBytes*, 5(2):2–13.
- Ray, C., Iphar, C., Napoli, A. (2024). Maritime Anomaly Detection: A Review of Methods and Architectures for AIS Vessel Tracking. *IEEE Transactions on Intelligent Transportation Systems*, 25(4):3120–3138. doi:10.1109/TITS.2023.3325678
- Wimpenny, E., Šafář, J., Grant, A. (2018). Public Key Authentication for AIS and the VHF Data Exchange System (VDES). In *Proceedings of the 31st International Technical Meeting of the Satellite Division of the Institute of Navigation (ION GNSS+ 2018)*, pp. 2847–2857. Miami, Florida. doi:10.33012/2018.15998
- Wimpenny, E., Šafář, J., Grant, A., Bransby, C. (2022). Securing the Automatic Identification System (AIS) Using Public Key Cryptography to Prevent Spoofing Whilst Retaining Backwards Compatibility. *The Journal of Navigation*, 75(2):333–345. doi:10.1017/S0373463321000624
