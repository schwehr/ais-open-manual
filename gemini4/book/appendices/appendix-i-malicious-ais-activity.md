# Appendix I: Malicious AIS Activity and Adversarial Abuse

## 1. Operational & Conceptual Overview
The Automatic Identification System (AIS) was originally designed in the 1990s as a cooperative, unauthenticated collision avoidance and vessel tracking system. Because the underlying protocols (ITU-R M.1371) lack cryptographic authentication, message integrity checks, or sender non-repudiation mechanisms, the system is fundamentally vulnerable to adversarial abuse.

Malicious actors—ranging from state-sponsored naval units and organized crime syndicates to pirates and illegal fishers—routinely exploit these vulnerabilities. They transmit false ship identities, spoof their locations to hide illicit activities (such as illegal, unreported, and unregulated (IUU) fishing or sanctioned oil transfers), and deploy steganographic techniques to encode covert communications within standard AIS payloads. In addition to tactical deception, adversaries use AIS for cyber-kinetic attacks, attempting to crash VTS (Vessel Traffic Service) software, perform denial-of-service (DoS) on the RF link, or spoof navigational hazards to redirect shipping traffic. This appendix provides a comprehensive technical overview of how malicious actors manipulate AIS and the security implications for the maritime domain.

## 2. Historical Context & Evolution
The history of maritime deception predates radio, but the electronic spoofing of AIS began gaining documented prominence in the 2010s.
- **Early 2010s**: The primary abuse of AIS involved simple "dark fleet" operations, where vessels would power down their transponders to avoid detection during illegal fishing or smuggling.
- **2014-2016**: Security researchers began demonstrating software-defined radio (SDR) attacks against AIS at conferences, showing how easy it was to inject false vessels into ECDIS (Electronic Chart Display and Information System) using affordable equipment.
- **2017-2019**: State actors in the Black Sea and other conflict zones were observed conducting mass GPS/GNSS spoofing, which indirectly caused AIS transponders to report vessels at inland airports rather than at sea. Direct AIS spoofing was also used to create "phantom fleets" to mask the movement of sanctioned oil.
- **2020-Present**: The sophistication of attacks has increased. Malicious actors now manipulate specific AIS fields (like MMSI or dimensions), hijack legitimate ship identities (MMSI hijacking), and employ trajectory-preserving spoofing to make false tracks appear physically realistic to algorithmic anomaly detectors.

## 3. Deep Technical & Mathematical Foundations
### The Lack of Authentication
At the RF and bit level, an AIS message is simply a payload wrapped in HDLC framing with a 16-bit CRC for error detection, not security.
An adversary with a USRP or HackRF SDR can construct a perfectly valid AIS Message 1 (Position Report) by calculating the NMEA bitstream and generating the corresponding GMSK (Gaussian Minimum Shift Keying) modulated signal.

### Steganography in AIS
Steganography involves hiding data within legitimate-looking AIS messages. Attackers can leverage several fields:
1. **Padding Bits**: Up to 7 padding bits are available at the end of an AIS payload.
2. **Unused/Reserved Bits**: Fields marked as "spare" or "reserved for future use" in ITU-R M.1371.
3. **Binary Broadcast (Message 8) and Addressed (Message 6)**: The Application-Specific Messages (ASM) allow arbitrary binary payloads. While DAC/FI (Designated Area Code / Function Identifier) pairs dictate the structure, attackers can transmit unregistered DAC/FI codes carrying encrypted C2 (Command and Control) data, which VTS systems will log but fail to parse.
4. **Sub-LSB Position Manipulation**: A vessel's Longitude is encoded as a 28-bit integer ($1/10,000$ minute precision). An attacker can encode covert messages in the least significant bits of the position, causing sub-meter jitter that is invisible on an ECDIS display but easily decodable by a cooperating receiver.

## 4. Hardware, Standards, & Software Ecosystem
### Tools of the Trade
- **SDRs**: Software-Defined Radios (HackRF, BladeRF, USRP) paired with GNU Radio out-of-tree modules (e.g., `gr-ais`) allow full-duplex generation of AIS waveforms.
- **Custom Firmware**: Malicious firmware flashed onto commercial Class A or Class B transponders to bypass built-in GNSS modules and accept arbitrary NMEA `!AIVDM` sentences over the pilot port.
- **Open-Source Parsers**: Attackers study open-source parsers (`libais`, `gpsd`, OpenCPN) to find edge cases, buffer overflows, or logic bugs that can be triggered by malformed AIS packets.

### The Defensive Ecosystem
The defense against AIS spoofing relies on anomaly detection frameworks, satellite-based RF geolocation, and the emerging VDES (VHF Data Exchange System) standards which aim to introduce PKI (Public Key Infrastructure) authentication (e.g., SECOM). However, legacy AIS will remain in use for decades.

## 5. Security, Adversarial Abuse, & Failure Modes
### 5.1 Transmitting False Ships (Ghosting)
By transmitting crafted Message 1, 2, 3, or 5 payloads, an attacker can create "ghost ships" on a VTS or shipboard ECDIS. This can be used to:
- Overwhelm VTS operators.
- Trigger collision alarms (CPA/TCPA alerts) on target vessels to alter their course.
- Mask the presence of a real ship within a cluster of ghost contacts.

### 5.2 Location Manipulation and Spoofing
Instead of turning off AIS, vessels may broadcast fake coordinates. This is often achieved by feeding a spoofed GPS signal into the AIS transponder or altering the NMEA datastream.
- **Bouncing**: Rapidly alternating between true and false locations.
- **Offsetting**: Broadcasting a position translated by a fixed vector from the true position.
- **Trajectory Spoofing**: Simulating a realistic journey (e.g., sailing into a port) while the vessel is actually elsewhere (e.g., conducting an illegal ship-to-ship transfer).

### 5.3 Identity Masking (MMSI Spoofing)
Vessels involved in illicit acts frequently change their 9-digit MMSI number.
- **MMSI Hijacking**: Adopting the MMSI of a legitimate vessel of similar size and type to blend in.
- **Shared MMSI**: Multiple vessels using the same MMSI (e.g., `111111111` or `123456789`) to confuse tracking systems.

### 5.4 Software Crashing and Denial of Service (DoS)
Adversaries craft malformed messages to crash parsing software.
- **Buffer Overflows**: Sending Message 8 (Binary) with unexpectedly long payloads.
- **Logic Flaws**: Exploiting incorrect state machine handling in multi-part messages (Message 8/Message 6 fragments).
- **RF DoS (Slot Starvation)**: An attacker can monopolize the SOTDMA/CSTDMA time slots by broadcasting high-power signals across all slots, effectively jamming the 161.975 MHz and 162.025 MHz frequencies and preventing legitimate vessels from communicating.

### 5.5 Tricking Direction Finding (DF) Systems
Coastal authorities use RF Direction Finding (DF) or Time Difference of Arrival (TDOA) from satellites to verify a vessel's physical location against its reported AIS coordinates. Adversaries counter this by:
- Using directional antennas to beam their spoofed AIS signal toward specific terrestrial receivers.
- Modulating transmit power to confuse TDOA/FDOA algorithms.

### 5.6 Avoiding Pirates and Tracking Blueforce Ships
- **Pirate Evasion**: Vessels transiting high-risk areas (e.g., Gulf of Aden) may legitimately spoof their location or turn off AIS to avoid detection by pirates who use open internet AIS aggregators (MarineTraffic, VesselFinder) for targeting.
- **Blueforce Tracking**: Adversaries monitor Encrypted AIS (EAIS) or specific DAC/FI payloads used by military/coast guard vessels to track their patrol patterns and avoid interdiction.

## 6. Practical Engineering / Code Walkthrough
The following Python snippet demonstrates how an attacker might theoretically encode steganographic data into the least significant bits of an AIS position report. *Note: This is for educational and defensive analysis purposes only.*

```python
def encode_stego_position(true_lon_decimal: float, true_lat_decimal: float, secret_byte: int) -> tuple[float, float]:
    """
    Encodes an 8-bit secret into the LSBs of an AIS position.
    AIS Longitude is 28 bits (1/10000 minute). Latitude is 27 bits.
    """
    # Convert to AIS integer format
    lon_ais = int(true_lon_decimal * 600000.0)
    lat_ais = int(true_lat_decimal * 600000.0)
    
    # Split secret byte into two 4-bit nibbles
    secret_lon_nibble = (secret_byte >> 4) & 0x0F
    secret_lat_nibble = secret_byte & 0x0F
    
    # Clear the bottom 4 bits and insert secret
    spoofed_lon_ais = (lon_ais & ~0x0F) | secret_lon_nibble
    spoofed_lat_ais = (lat_ais & ~0x0F) | secret_lat_nibble
    
    # Convert back to decimal degrees
    spoofed_lon_decimal = spoofed_lon_ais / 600000.0
    spoofed_lat_decimal = spoofed_lat_ais / 600000.0
    
    return spoofed_lon_decimal, spoofed_lat_decimal

# Example usage
true_lon = -122.4194  # San Francisco
true_lat = 37.7749
secret = 0x5A # The character 'Z'

spoofed_lon, spoofed_lat = encode_stego_position(true_lon, true_lat, secret)
print(f"True Position:    {true_lon:.6f}, {true_lat:.6f}")
print(f"Spoofed Position: {spoofed_lon:.6f}, {spoofed_lat:.6f}")
```

This introduces an error of at most 15 units ($15 / 600000$ degrees $pprox 2.5 	imes 10^{-5}$ degrees), which is less than 3 meters—well within typical GPS jitter and invisible to human operators.

## 7. Key Takeaways & Operational Checklist
- [x] **Spoofing Detection**: VTS systems must correlate AIS data with primary radar tracks to identify ghost ships or spoofed trajectories.
- [x] **MMSI Verification**: Port state control must physically verify the vessel's MMSI programmed into the transponder against its IMO number and registration documents.
- [x] **Software Hardening**: Open-source and proprietary AIS parsers must be fuzzed against malformed HDLC/NMEA payloads to prevent DoS or remote code execution.
- [x] **TDOA/FDOA Validation**: Use space-based RF geolocation to detect discrepancies between the reported position and the physical RF emission source.
- [x] **Awareness**: Understand that AIS is an unauthenticated protocol; decisions affecting safety of life at sea should never rely *solely* on AIS if other sensors (Radar, visual) are available.

## 8. Cited References & Primary Sources
The analysis of AIS vulnerabilities relies on fundamental cybersecurity research and reports from maritime domain awareness organizations. See Appendix H for full bibliographical details.

- **Balduzzi et al. (2014)**: *A Security Evaluation of AIS*. Demonstrated practical SDR attacks, ghost ships, and CPA spoofing. [@balduzzi2014security]
- **Windward (2021)**: *The Dark Fleet's New Tactics*. Detailed analysis of MMSI hijacking and trajectory spoofing in the context of sanctioned trade. [@windward2021darkfleet]
- **Kessler (2020)**: *Steganography in the Maritime Domain*. Analysis of covert channels in AIS and other maritime RF protocols. [@kessler2020steganography]
- **IMO Res. A.1192(33) (2023)**: Urges Member States to address the "Shadow Fleet" and deceptive shipping practices, including AIS manipulation. [@imo2023a1192_33]


### 5.7 Extended Case Studies in Malicious AIS Activity

#### Case Study 1: The Black Sea GPS Spoofing Incidents
Beginning around 2017, numerous vessels operating in the Black Sea reported bizarre navigational anomalies. Their onboard GPS receivers, and consequently their AIS transmissions, suddenly indicated their positions as being miles inland, often centered exactly on the runway of a Russian airport (such as Gelendzhik Airport). This was not an attack on AIS itself, but rather an attack on the underlying GNSS (Global Navigation Satellite System) positioning infrastructure. Because AIS blindly trusts the position data fed to it by the GNSS receiver, the spoofed coordinates were broadcast over the VHF data link. This incident highlighted a critical failure mode: AIS is only as trustworthy as the sensors providing it with data. The cascading effect of GNSS spoofing means that VTS operators, nearby ships, and global tracking databases all receive corrupted data, creating a massive, coordinated false picture of the maritime domain.

#### Case Study 2: Sanctions Evasion and the "Shadow Fleet"
In the wake of international sanctions against various nation-states, a vast "shadow fleet" of tankers emerged, dedicated to the illicit transport of oil. These vessels employ a wide array of AIS manipulation tactics to obfuscate their activities. 
- **Identity Laundering**: Vessels will change their names, flags, and MMSI numbers mid-voyage. They often hijack the MMSI of a derelict or scrapped vessel to maintain a veneer of legitimacy.
- **Location Laundering**: When conducting an illegal Ship-to-Ship (STS) transfer of oil, vessels will frequently broadcast a fake, offset location (e.g., claiming to be in the Sea of Japan while actually operating in the East China Sea). To make this believable, adversarial operators use software that generates realistic, physically possible trajectories, complete with simulated variations in speed and heading that mimic actual sea states and navigation.

#### Case Study 3: AIS Hijacking and VTS Confusion
In 2019, a targeted attack was observed where multiple ghost ships were projected onto the ECDIS displays of naval vessels and coastal VTS stations. These ghost ships were programmed to exhibit highly aggressive behavior, generating constant Collision Risk Alarms (CPA/TCPA). This type of attack is designed to induce alarm fatigue in operators and mask the movement of a real asset. If an operator is forced to acknowledge and dismiss hundreds of fake collision alerts, they may miss the single alert representing a genuine, physical threat.

### 5.8 Advanced Technical Mitigation Strategies

Mitigating AIS abuse requires a multi-layered approach spanning hardware, software, and international policy.

#### Cryptographic Authentication (VDES and SECOM)
The long-term solution to AIS vulnerabilities is the transition to the VHF Data Exchange System (VDES), which incorporates cryptographic authentication. The SECOM (Secure Communication) standard, defined under IEC 63173-2, provides a PKI framework for the maritime domain. Under SECOM, vessels will possess digital certificates issued by recognized maritime authorities. When transmitting sensitive data, the payload can be digitally signed, allowing the receiver to verify the sender's identity and ensure the message has not been tampered with. While this solves the problem of message integrity and authentication, it does not solve the problem of physical location spoofing (a signed message containing a fake GPS coordinate is still cryptographically valid).

#### Independent RF Geolocation
To combat location spoofing, defensive systems rely on independent verification of the signal's origin. Low Earth Orbit (LEO) satellite constellations equipped with AIS receivers can perform Time Difference of Arrival (TDOA) and Frequency Difference of Arrival (FDOA) analysis. When a vessel transmits an AIS message, the signal is received by multiple satellites at slightly different times and with varying Doppler shifts. By cross-correlating these signals, the satellite operator can calculate the physical origin of the RF emission. If this calculated location differs significantly from the coordinates reported inside the AIS payload, the vessel is flagged for spoofing.

#### Machine Learning and Anomaly Detection
With millions of AIS messages generated every day, manual detection of malicious activity is impossible. Advanced analytics platforms (e.g., Global Fishing Watch, Windward) ingest the global AIS data feed and apply machine learning algorithms to detect anomalies. These algorithms are trained to recognize patterns indicative of illicit behavior:
- Unexplained gaps in transmission (going dark).
- Unrealistic speeds or acceleration (e.g., a bulk carrier accelerating from 0 to 30 knots in one minute).
- "Loitering" behavior in areas known for illegal transshipment.
- Draught changes (reported in Message 5) that occur at sea rather than in port, indicating an STS transfer.

### 5.9 Future Threat Vectors

As the maritime industry becomes increasingly digital and reliant on autonomous systems, the threat landscape surrounding AIS and VDES will evolve.

- **Autonomous Surface Vehicles (ASVs)**: ASVs rely heavily on AIS for collision avoidance. A coordinated ghost ship attack against an autonomous vessel could force it to alter course, effectively steering it into a trap, a hazard, or territorial waters where it could be seized.
- **Cyber-Physical Cascades**: An attacker could use AIS to inject a malicious payload that exploits a vulnerability in a ship's ECDIS. Because modern shipboard networks are increasingly integrated, a compromise of the ECDIS could theoretically pivot into the ship's engine control or steering systems.
- **Quantum Computing and Cryptography**: As VDES and SECOM roll out, the cryptographic algorithms they rely on must be resilient against future advances in quantum computing. The maritime industry's long hardware replacement cycles (often 10-20 years) mean that systems deployed today must consider the threat of "harvest now, decrypt later" attacks.

### Final Thoughts on Maritime Cybersecurity
The exploitation of AIS highlights a broader challenge in maritime cybersecurity: the tension between open, interoperable safety systems and the need for secure, authenticated communication. As the industry navigates this transition, a "defense in depth" strategy—combining independent sensor validation, robust software engineering, and cryptographic modernization—is essential to maintaining the integrity of global maritime domain awareness.


### 5.10 Technical Deep Dive: Fuzzer Development for AIS Parsers

To harden AIS software against adversarial abuse, security engineers use fuzzing techniques. A fuzzer generates massive amounts of malformed, unexpected, or random data and feeds it to the target application (the AIS parser) to identify memory leaks, buffer overflows, or unhandled exceptions.

#### Fuzzing Strategies for AIS

1. **Mutation-Based Fuzzing**: The fuzzer starts with a set of valid AIS NMEA sentences (e.g., captured from a real receiver). It then applies random mutations to the data:
   - Flipping bits in the payload.
   - Deleting or duplicating characters.
   - Modifying the checksum.
   - Changing the NMEA encapsulation (e.g., swapping `!AIVDM` for `!AIVDO`).

2. **Generation-Based Fuzzing**: The fuzzer understands the underlying AIS specification (ITU-R M.1371) and generates packets from scratch, deliberately violating the rules:
   - Setting enumerated fields to undocumented values (e.g., Navigation Status > 15).
   - Creating messages with invalid bit lengths (e.g., a Message 1 with 160 bits instead of 168).
   - Using reserved DAC/FI pairs in Message 6 and 8.

3. **Stateful Fuzzing**: AIS parsing involves state. For example, multi-part messages (indicated by the fragmentation fields in the NMEA sentence) require the parser to buffer the first part and wait for the second. A stateful fuzzer tests this mechanism by:
   - Sending Part 1, but never sending Part 2 (testing for memory leaks or timeout handling).
   - Sending Part 2 before Part 1.
   - Sending interleaved fragments from multiple different multi-part messages simultaneously.

#### Example Fuzzing Findings
Historically, fuzzing open-source AIS parsers has revealed numerous critical vulnerabilities. For example:
- **Out-of-bounds reads**: When parsing a string field (like the vessel name in Message 5), a missing null-terminator in the payload could cause the parser to read past the end of the allocated buffer, potentially crashing the application or exposing memory contents.
- **Integer Underflows**: Incorrect calculation of payload lengths when dealing with padding bits can lead to integer underflows, resulting in massive memory allocation attempts that exhaust system resources (DoS).
- **Infinite Loops**: Malformed linked lists or circular references in the handling of internal routing tables for addressed messages can cause the parser to enter an infinite loop, rendering the VTS system unresponsive.

By incorporating fuzz testing into the continuous integration (CI) pipelines of AIS software projects (such as `libais` and `gpsd`), the maritime community can proactively discover and patch these vulnerabilities before they are exploited by malicious actors.

### 5.10 Technical Deep Dive: Fuzzer Development for AIS Parsers

To harden AIS software against adversarial abuse, security engineers use fuzzing techniques. A fuzzer generates massive amounts of malformed, unexpected, or random data and feeds it to the target application (the AIS parser) to identify memory leaks, buffer overflows, or unhandled exceptions.

#### Fuzzing Strategies for AIS

1. **Mutation-Based Fuzzing**: The fuzzer starts with a set of valid AIS NMEA sentences (e.g., captured from a real receiver). It then applies random mutations to the data:
   - Flipping bits in the payload.
   - Deleting or duplicating characters.
   - Modifying the checksum.
   - Changing the NMEA encapsulation (e.g., swapping `!AIVDM` for `!AIVDO`).

2. **Generation-Based Fuzzing**: The fuzzer understands the underlying AIS specification (ITU-R M.1371) and generates packets from scratch, deliberately violating the rules:
   - Setting enumerated fields to undocumented values (e.g., Navigation Status > 15).
   - Creating messages with invalid bit lengths (e.g., a Message 1 with 160 bits instead of 168).
   - Using reserved DAC/FI pairs in Message 6 and 8.

3. **Stateful Fuzzing**: AIS parsing involves state. For example, multi-part messages (indicated by the fragmentation fields in the NMEA sentence) require the parser to buffer the first part and wait for the second. A stateful fuzzer tests this mechanism by:
   - Sending Part 1, but never sending Part 2 (testing for memory leaks or timeout handling).
   - Sending Part 2 before Part 1.
   - Sending interleaved fragments from multiple different multi-part messages simultaneously.

#### Example Fuzzing Findings
Historically, fuzzing open-source AIS parsers has revealed numerous critical vulnerabilities. For example:
- **Out-of-bounds reads**: When parsing a string field (like the vessel name in Message 5), a missing null-terminator in the payload could cause the parser to read past the end of the allocated buffer, potentially crashing the application or exposing memory contents.
- **Integer Underflows**: Incorrect calculation of payload lengths when dealing with padding bits can lead to integer underflows, resulting in massive memory allocation attempts that exhaust system resources (DoS).
- **Infinite Loops**: Malformed linked lists or circular references in the handling of internal routing tables for addressed messages can cause the parser to enter an infinite loop, rendering the VTS system unresponsive.

By incorporating fuzz testing into the continuous integration (CI) pipelines of AIS software projects (such as `libais` and `gpsd`), the maritime community can proactively discover and patch these vulnerabilities before they are exploited by malicious actors.

### 5.10 Technical Deep Dive: Fuzzer Development for AIS Parsers

To harden AIS software against adversarial abuse, security engineers use fuzzing techniques. A fuzzer generates massive amounts of malformed, unexpected, or random data and feeds it to the target application (the AIS parser) to identify memory leaks, buffer overflows, or unhandled exceptions.

#### Fuzzing Strategies for AIS

1. **Mutation-Based Fuzzing**: The fuzzer starts with a set of valid AIS NMEA sentences (e.g., captured from a real receiver). It then applies random mutations to the data:
   - Flipping bits in the payload.
   - Deleting or duplicating characters.
   - Modifying the checksum.
   - Changing the NMEA encapsulation (e.g., swapping `!AIVDM` for `!AIVDO`).

2. **Generation-Based Fuzzing**: The fuzzer understands the underlying AIS specification (ITU-R M.1371) and generates packets from scratch, deliberately violating the rules:
   - Setting enumerated fields to undocumented values (e.g., Navigation Status > 15).
   - Creating messages with invalid bit lengths (e.g., a Message 1 with 160 bits instead of 168).
   - Using reserved DAC/FI pairs in Message 6 and 8.

3. **Stateful Fuzzing**: AIS parsing involves state. For example, multi-part messages (indicated by the fragmentation fields in the NMEA sentence) require the parser to buffer the first part and wait for the second. A stateful fuzzer tests this mechanism by:
   - Sending Part 1, but never sending Part 2 (testing for memory leaks or timeout handling).
   - Sending Part 2 before Part 1.
   - Sending interleaved fragments from multiple different multi-part messages simultaneously.

#### Example Fuzzing Findings
Historically, fuzzing open-source AIS parsers has revealed numerous critical vulnerabilities. For example:
- **Out-of-bounds reads**: When parsing a string field (like the vessel name in Message 5), a missing null-terminator in the payload could cause the parser to read past the end of the allocated buffer, potentially crashing the application or exposing memory contents.
- **Integer Underflows**: Incorrect calculation of payload lengths when dealing with padding bits can lead to integer underflows, resulting in massive memory allocation attempts that exhaust system resources (DoS).
- **Infinite Loops**: Malformed linked lists or circular references in the handling of internal routing tables for addressed messages can cause the parser to enter an infinite loop, rendering the VTS system unresponsive.

By incorporating fuzz testing into the continuous integration (CI) pipelines of AIS software projects (such as `libais` and `gpsd`), the maritime community can proactively discover and patch these vulnerabilities before they are exploited by malicious actors.
