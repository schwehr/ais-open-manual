# Appendix G: Recommended Low-Budget Home AIS Station Bill of Materials, Schematics, Filter Curves, and Configuration Files

---

## G.1 Overview and End-to-End Physical Topology

This appendix provides the complete, ready-to-deploy hardware blueprints, coaxial connector matrices, filter specifications, Linux system configuration files, and automated **GeoParquet / DuckDB** archiving code referenced in **Chapter 9 (Section 9.3)**. Every configuration file and script below is designed for unattended 24/7 operation on Debian 12/13 (Bookworm/Trixie), Ubuntu 24.04 LTS, or Raspberry Pi OS (64-bit).

```
                     HOME AIS STATION PHYSICAL & RF TOPOLOGY
                     
  [Outdoor Mast]                                         [Indoor Compute Shelf]
  +-----------------------+
  | 162.000 MHz Antenna   |  (DIY Copper J-Pole or Marine 162 MHz Fiberglass Whip)
  +-----------+-----------+
              |  N-Male or PL-259 (Weatherproofed with 3M Coax Seal + Super 33+)
              v
  |  Low-Loss Coax Feedline (Times Microwave LMR-400 or LMR-240, 50 Ohm)
              |
              v
  +-----------------------+
  | Gas-Discharge Tube    |===[6 AWG Copper Wire]===> [8 ft Earth Ground Rod]
  | Lightning Arrestor    |   (Mounted at Building Entry Point)
  +-----------+-----------+
              |  Flexible SMA-Male Pigtail (30 cm RG-316 / LMR-195, Prevents Port Strain)
              v
  +-----------------------+
  | 162 MHz SAW Bandpass  |  (Passive SAW Filter OR SAW + LNA; Rejects FM & NWR)
  | Filter (SMA-F/SMA-M)  |
  +-----------+-----------+
              |  SMA-Male to SMA-Female (Direct Barrel or Short Pigtail)
              v
  +-----------------------+
  | RTL-SDR Blog V4 /     |  (Tuned to fc = 162.000 MHz, 0.5 ppm TCXO)
  | Airspy Mini / dAISy   |
  +-----------+-----------+
              |  USB 2.0 Port (Ferrite Choke on USB Cable)
              v
  +-----------------------------------------------------------------------+
  | Linux Host (Raspberry Pi 4B/5 or Refurbished x86-64 Mini-PC)          |
  |  - ais-catcher.service  --> Web UI (:8100), Prometheus (/metrics)     |
  |  - UDP 127.0.0.1:10110  --> gpsd / Signal K / OpenCPN (!AIVDM)        |
  |  - UDP 127.0.0.1:10111  --> ais-archiver.service (GeoParquet + DuckDB)|
  +-----------------------------------------------------------------------+
```

---

## G.2 Complete Bill of Materials (BOM) & Coaxial Connector Matrix

A frequent source of frustration when assembling an RF station is ordering incompatible coaxial connector genders (e.g., confusing standard `SMA-Male` with `RP-SMA` [Reverse Polarity SMA used on Wi-Fi routers], or connecting rigid $10.3\text{ mm}$ `LMR-400` directly into a fragile USB SDR jack, snapping the PCB solder joints). The tables below specify exact connector terminations for every link in the chain.

### G.2.1 Tier 1 BOM: Entry-Level High-Sensitivity SDR Station (~$110 USD)

| Item # | Component | Specification & Model | Input Port | Output Port | Approx. Cost (USD) |
|---|---|---|---|---|---|
| **1.1** | **Antenna** | DIY $162.000\text{ MHz}$ Copper-Pipe J-Pole ($15\text{ mm}$ / $1/2\text{''}$ Type M copper pipe, 1 tee, 1 elbow, 2 end caps) | Free Space ($162\text{ MHz}$) | Soldered Coax or `SO-239` Chassis Mount | $\$15$ |
| **1.2** | **Coaxial Feedline** | $10\text{ m}$ ($33\text{ ft}$) **Times Microwave LMR-240** (or `RG-8X`), $50\text{ }\Omega$ low-loss coaxial cable | `PL-259` (Male) | `SMA-Male` (Standard Polarity) | $\$18$ |
| **1.3** | **AIS Bandpass Filter** | **Sysmocom** or **Upronics $162\text{ MHz}$ Passive AIS SAW Filter** (Passband $161.5\text{–}162.5\text{ MHz}$, IL $\le 2.5\text{ dB}$, no DC power required) | `SMA-Female` | `SMA-Male` (connects to SDR) | $\$22$ |
| **1.4** | **SDR Receiver** | **RTL-SDR Blog V4** (R828D tuner + RTL2832U 8-bit ADC + $0.5\text{ ppm}$ TCXO + aluminum enclosure) | `SMA-Female` | `USB 2.0 Type-A Male` | $\$30$ |
| **1.5** | **Compute Host** | **Raspberry Pi Zero 2 W** (or Pi 4B) + Official $5.1\text{ V} / 2.5\text{ A}$ PSU + $32\text{ GB}$ SanDisk Max Endurance microSD + OTG adapter | `USB 2.0` | Wi-Fi / Ethernet | $\$25$ |
| | **Tier 1 Total** | | | | **$\approx \$110$** |

### G.2.2 Tier 2 BOM: High-Immunity Coastal & Urban Station (~$185 USD)

| Item # | Component | Specification & Model | Input Port | Output Port | Approx. Cost (USD) |
|---|---|---|---|---|---|
| **2.1** | **Antenna** | **Shakespeare 5215-AIS** ($36\text{ in}$ stainless whip tuned specifically to $162\text{ MHz}$, $3\text{ dBi}$) or **Digital Antenna 528-VW-AIS** ($4\text{ ft}$ fiberglass, $4.5\text{ dBi}$) | Free Space ($162\text{ MHz}$) | `SO-239` (Female UHF) at base | $\$55$ |
| **2.2** | **Primary Feedline** | $15\text{ m}$ ($50\text{ ft}$) **Times Microwave LMR-400** ($50\text{ }\Omega$, $5.1\text{ dB/100m}$ attenuation @ $162\text{ MHz}$) + `3M Temflex 2155` rubber splicing tape | `PL-259` (or `N-Male`) | `N-Male` | $\$32$ |
| **2.3** | **Lightning Arrestor** | **Alpha Delta ATT3G50U** or **PolyPhaser VHFF50HN** inline gas-discharge surge protector (mounted on grounded entrance bulkhead) | `N-Female` | `N-Female` | $\$25$ |
| **2.4** | **Strain-Relief Pigtail** | $30\text{ cm}$ ($12\text{ in}$) flexible `RG-316` or `LMR-195` jumper cable | `N-Male` | `SMA-Male` | $\$8$ |
| **2.5** | **SAW Filter / LNA** | **Upronics $162\text{ MHz}$ AIS Filtered Preamp** (Front-end SAW filter $\rightarrow$ ultra-high-IP3 PGA-103+ LNA $\rightarrow$ second SAW filter; powered via $4.5\text{ V}$ SDR Bias-Tee) | `SMA-Female` | `SMA-Male` | $\$38$ |
| **2.6** | **SDR Receiver** | **RTL-SDR Blog V4** ($\$30$) *or* **Airspy Mini** (12-bit ADC, $\$99$) | `SMA-Female` | `USB 2.0 Type-A` | $\$30\text{–}\$99$ |
| **2.7** | **Compute Host** | **Refurbished x86-64 Thin Client / Mini-PC** (e.g., Dell Wyse 5070 Celeron J4105, $8\text{ GB}$ DDR4, $128\text{ GB}$ M.2 SSD, silent fanless chassis, $6\text{ W}$ idle) | `USB 3.0 / 2.0` | Gigabit Ethernet | $\$35\text{–}\$45$ |
| | **Tier 2 Total** | *(with RTL-SDR V4 / with Airspy Mini)* | | | **$\approx \$185\text{ / }\$254$** |

### G.2.3 Coaxial Cable Attenuation Reference at $162.000\text{ MHz}$

| Coaxial Cable Type | Outer Diameter | Velocity Factor ($v_f$) | Attenuation per $10\text{ m}$ ($33\text{ ft}$) @ $162\text{ MHz}$ | Attenuation per $30\text{ m}$ ($100\text{ ft}$) @ $162\text{ MHz}$ | Signal Power Remaining After $30\text{ m}$ Run |
|---|---|---|---|---|---|
| **`RG-174 / RG-316`** (Pigtails only!) | $2.5\text{ mm}$ | $0.66\text{ / }0.695$ | $3.6\text{ dB}$ | $10.8\text{ dB}$ | $8.3\%$ *(Never use for long runs!)* |
| **`RG-58C/U`** | $5.0\text{ mm}$ | $0.66$ | $2.05\text{ dB}$ | $6.15\text{ dB}$ | $24.3\%$ *(Avoid over $5\text{ m}$)* |
| **`RG-8X / Mini-8`** | $6.1\text{ mm}$ | $0.78\text{–}0.82$ | $1.35\text{ dB}$ | $4.05\text{ dB}$ | $39.4\%$ |
| **`Times LMR-240`** | $6.1\text{ mm}$ | $0.84$ | **$1.05\text{ dB}$** | **$3.15\text{ dB}$** | **$48.4\%$** *(Good up to $12\text{ m}$)* |
| **`RG-213 / U`** | $10.3\text{ mm}$ | $0.66$ | $0.88\text{ dB}$ | $2.64\text{ dB}$ | $54.5\%$ |
| **`Times LMR-400`** | $10.3\text{ mm}$ | $0.85$ | **$0.51\text{ dB}$** | **$1.53\text{ dB}$** | **$70.3\%$** *(Recommended $10\text{–}35\text{ m}$)* |
| **`Andrew LDF4-50A (1/2" Heliax)`** | $16.0\text{ mm}$ | $0.88$ | **$0.28\text{ dB}$** | **$0.84\text{ dB}$** | **$82.4\%$** *(VTS / Lighthouse Towers)* |

---

## G.3 $162.000\text{ MHz}$ Copper-Pipe J-Pole Dimensional Blueprint & VNA Tuning Guide

### G.3.1 Exact Cutting & Assembly Dimensions ($f_c = 162.000\text{ MHz}$)

Using standard **Type M or Type L $1/2\text{''}$ nominal rigid copper water pipe** ($15.875\text{ mm}$ [$0.625\text{ in}$] Outside Diameter, or European $15\text{ mm}$ OD plumbing pipe):

```
         162.000 MHz COPPER-PIPE J-POLE FABRICATION BLUEPRINT
         
   [Cap]---> +---+
             |   |
             |   |   Radiating Half-Wave Section (A -> B):
             |   |   898.0 mm (35.35 in)
             |   |
   Total     |   |             [Cap]---> +---+
   Long      |   |                       |   |
   Section   |   |                       |   |  Quarter-Wave Matching Stub (B -> C):
   (A -> C)  |   |                       |   |  443.0 mm (17.44 in)
   1341.0 mm |   |                       |   |  (Measured from top of cap to
   (52.80")  |   |                       |   |   centerline of horizontal shorting bar)
             |   |   48.0 mm (1.89 in)   |   |
             |   | <-----[Feed Tap]----->|   |  <-- Stainless Hose Clamps + Brass Screws
             |   |   Coax Shield (Left)  |   |      Coax Center Conductor (Right)
   (Point C) +---+-----------------------+---+  <-- Copper Tee + 90-deg Elbow
             |   |<---- 50.0 mm C-to-C ----->|      (Center-to-Center Spacing = 50.0 mm)
             |   |
             |   |   Mast Mounting Extension (C -> D):
             |   |   300 - 500 mm (12 - 20 in)
             +---+
```

| Dimension Label | Description | Metric ($\text{mm}$) | Imperial ($\text{inches}$) | Tolerance |
|---|---|---|---|---|
| **$L_{\text{long}}$ (`A` $\rightarrow$ `C`)** | Total length of long vertical element from top cap to centerline of horizontal shorting bar | **$1,341.0\text{ mm}$** | **$52.80\text{ in}$** | $\pm 2.0\text{ mm}$ |
| **$L_{\text{rad}}$ (`A` $\rightarrow$ `B`)** | Upper $\frac{1}{2}\lambda$ radiating section above matching stub | **$898.0\text{ mm}$** | **$35.35\text{ in}$** | $\pm 2.0\text{ mm}$ |
| **$L_{\text{stub}}$ (`B` $\rightarrow$ `C`)** | Short vertical $\frac{1}{4}\lambda$ matching stub from top cap to centerline of horizontal shorting bar | **$443.0\text{ mm}$** | **$17.44\text{ in}$** | $\pm 1.5\text{ mm}$ |
| **$S_{\text{c2c}}$** | Center-to-center spacing between long element and short stub | **$50.0\text{ mm}$** | **$1.97\text{ in}$** | $\pm 1.5\text{ mm}$ |
| **$L_{\text{tap}}$** | Distance from centerline of horizontal shorting bar (`C`) up to $50\text{ }\Omega$ coax feed point | **$48.0\text{ mm}$** | **$1.89\text{ in}$** | Tunable ($44\text{–}54\text{ mm}$) |
| **$L_{\text{mast}}$ (`C` $\rightarrow$ `D`)** | Lower mounting pipe extension below the Tee fitting (clamp directly to grounded metal mast) | **$350.0\text{ mm}$** | **$13.78\text{ in}$** | Any convenient length |

### G.3.2 Step-by-Step NanoVNA Tuning Procedure
1. **Attach Temporarily with Stainless Hose Clamps:** Before permanently soldering the coaxial feed point, strip $15\text{ mm}$ of your coaxial jumper, solder brass ring terminals to the center conductor and shield braid (keep unshielded pigtails $<25\text{ mm}$ short!), and clamp them around the two copper pipes using stainless-steel worm-gear hose clamps at $L_{\text{tap}} = 48.0\text{ mm}$ above the shorting bar center.
2. **Add the Common-Mode Choke Balun:** Snap **3 to 4 Fair-Rite `Mix 43` (`0443164251`) ferrite suppression cores** onto the coax immediately below the feed tap (or wind 4 tight turns of coax around a $100\text{ mm}$ PVC form). Without this choke, RF current flows down the outside of the coaxial shield, skewing the vertical radiation pattern and making the VSWR change whenever you touch the cable.
3. **Sweep $158.0\text{ MHz}$ to $166.0\text{ MHz}$ on a NanoVNA:**
   * Set the **Dip Frequency** (where reactance $X = 0\text{ }\Omega$) by checking the resonant minimum. If the resonant dip is below $162.000\text{ MHz}$ (e.g., $160.8\text{ MHz}$), trim $2\text{–}3\text{ mm}$ equally off the top of both the radiator and the stub.
   * Set the **$50\text{ }\Omega$ Impedance Match** by sliding the two hose clamps slightly up (increases resistance toward $60\text{–}75\text{ }\Omega$) or down toward the shorting bar (decreases resistance toward $25\text{–}35\text{ }\Omega$) until the NanoVNA reads:
     $$\text{Return Loss } |S_{11}| \le -23\text{ dB}\quad (\text{VSWR} \le 1.15 : 1)\quad \text{at } 162.000\text{ MHz}$$
4. **Weatherproof:** Once tuned, solder the feed lugs directly to the copper pipe, coat the joint and coax entry in **3M Scotchkote / Coax-Seal**, and over-wrap with **3M Scotch Super 33+ vinyl tape**. Drill a $2\text{ mm}$ weep hole at the lowest point of the horizontal shorting bar so rainwater condensation cannot pool inside the tubing.

---

## G.4 $162\text{ MHz}$ AIS SAW Bandpass Filter Frequency Response Curve

The plot and specification table below illustrate the transmission response ($S_{21}$) of a dedicated $162.0\text{ MHz}$ AIS Surface Acoustic Wave (SAW) bandpass filter (such as the Sysmocom / Upronics / Tai-Saw TA1212A $162\text{ MHz}$ SAW element):

```
   Transmission S21 (dB)
     0 dB +-----------------------------------***-----------------------------------+
          |                                  *   *   <- Passband: 161.5 - 162.3 MHz
   -10 dB +                                 *     *     Insertion Loss: -2.1 dB
          |                                *       *
   -20 dB +                               *         * <- NWR Roll-off (162.40+ MHz)
          |                              *           *
   -30 dB +                             *             *
          |                            *               *
   -40 dB +                           *                 *
          |                          *                   *
   -50 dB +      FM Broadcast       *                     *      UHF / Cellular
          |   ******************   *                       *   ******************
   -60 dB +---+----------------+---+-------+-------+-------+---+----------------+---> Freq
             88              108  156.8  161.975 162.025 162.55 300            900 (MHz)
```

| Frequency Band | Frequency ($\text{MHz}$) | Typical Passive SAW $S_{21}$ Attenuation | Filtered LNA ($S_{21}$ Net Gain) | Operational Purpose |
|---|---|---|---|---|
| **FM Broadcast Band** | $88.0\text{–}108.0\text{ MHz}$ | **$-52\text{ to }-60\text{ dB}$** | $-35\text{ to }-45\text{ dB}$ | Eliminates $100\text{ kW}$ FM broadcast overload & 3rd-order IMD |
| **VHF Airband** | $118.0\text{–}137.0\text{ MHz}$ | **$-48\text{ to }-55\text{ dB}$** | $-30\text{ to }-40\text{ dB}$ | Rejects nearby airport tower AM transmissions |
| **Marine VHF Ch 16** | $156.800\text{ MHz}$ | **$-32\text{ to }-40\text{ dB}$** | $-15\text{ to }-22\text{ dB}$ | Prevents shipboard/harbor $25\text{ W}$ Ch 16 distress/calling compression |
| **AIS 1 (Ch 87B)** | **$161.975\text{ MHz}$** | **$-2.1\text{ dB}$** (Passband) | **$+15.5\text{ dB}$** ($\text{NF} \approx 2.8\text{ dB}$) | Desired primary AIS Channel A |
| **AIS 2 (Ch 88B)** | **$162.025\text{ MHz}$** | **$-2.2\text{ dB}$** (Passband) | **$+15.4\text{ dB}$** ($\text{NF} \approx 2.8\text{ dB}$) | Desired primary AIS Channel B |
| **NOAA Weather Radio** | $162.400\text{–}162.550\text{ MHz}$ | **$-8\text{ to }-18\text{ dB}$** | $+5\text{ to }-2\text{ dB}$ | Attenuates nearby $1\text{ kW}$ NWR transmitters |
| **UHF / LTE / 5G** | $400.0\text{–}2,700.0\text{ MHz}$ | **$-45\text{ to }-65\text{ dB}$** | $-30\text{ to }-50\text{ dB}$ | Rejects cellular handsets, DMR, and radar harmonics |

---

## G.5 Ready-to-Deploy Linux System & `AIS-catcher` Configurations

### G.5.1 Kernel DVB-T Blacklist (`/etc/modprobe.d/blacklist-dvb-ais.conf`)
By default, the Linux kernel loads the digital television driver (`dvb_usb_rtl28xxu`) when an RTL2832U dongle is inserted, blocking userspace SDR access. Create `/etc/modprobe.d/blacklist-dvb-ais.conf`:

```ini
# /etc/modprobe.d/blacklist-dvb-ais.conf
# Prevent Linux kernel DVB-T TV drivers from claiming the RTL-SDR AIS receiver
blacklist dvb_usb_rtl28xxu
blacklist rtl2832
blacklist rtl2830
blacklist dvb_usb_v2
blacklist r820t
```

### G.5.2 Non-Root USB `udev` Rules (`/etc/udev/rules.d/20-rtlsdr-ais.rules`)
Allow the unprivileged `plugdev` / `ais` service user to open the RTL-SDR or Airspy Mini without root privileges:

```ini
# /etc/udev/rules.d/20-rtlsdr-ais.rules
# Realtek RTL2832U (RTL-SDR Blog V3 / V4)
SUBSYSTEM=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="2838", GROUP="plugdev", MODE="0660", SYMLINK+="rtlsdr-ais"
# Airspy Mini / Airspy R2
SUBSYSTEM=="usb", ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="60a1", GROUP="plugdev", MODE="0660", SYMLINK+="airspy-ais"
# Wegmatt dAISy USB (TI MSP430 CDC-ACM)
SUBSYSTEM=="tty", ATTRS{idVendor}=="2047", ATTRS{idProduct}=="0863", GROUP="dialout", MODE="0660", SYMLINK+="daisy-ais"
```

Reload rules and unload any active DVB module:
```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo rmmod dvb_usb_rtl28xxu rtl2832 2>/dev/null || true
```

---

### G.5.3 Production `AIS-catcher` Configuration (`/etc/ais-catcher/ais-catcher.conf`)

Create `/etc/ais-catcher/ais-catcher.conf` (compatible with `AIS-catcher` v0.64+):

```json
{
  "config": "ais-catcher",
  "version": 1,
  "verbose": true,
  "verbose_time": 60,
  "rtlsdr": {
    "tuner": 38.6,
    "rtlagc": false,
    "biastee": false,
    "sample_rate": "1536K",
    "freqoffset": 0,
    "bandwidth": "0"
  },
  "model": {
    "type": "default",
    "afc_wide": false,
    "fp_ds": false,
    "droop": true
  },
  "udp": [
    {
      "address": "127.0.0.1",
      "port": 10110,
      "json": false,
      "comment": "Standard NMEA 0183 (!AIVDM) stream for local gpsd / Signal K / OpenCPN"
    },
    {
      "address": "127.0.0.1",
      "port": 10111,
      "json": true,
      "comment": "Full JSON + NMEA + RSSI/PPM metadata stream for local DuckDB/GeoParquet archiver"
    }
  ],
  "server": [
    {
      "port": 8100,
      "active": true,
      "station": "HOME-AIS-STATION-01",
      "station_link": "https://github.com/jvde-github/AIS-catcher",
      "lat": 37.8199,
      "lon": -122.4783,
      "share_loc": false,
      "prometheus": true,
      "backup": 60,
      "file": "/var/lib/ais-catcher/stat_backup.bin"
    }
  ]
}
```

---

### G.5.4 Hardened `systemd` Service Unit (`/etc/systemd/system/ais-catcher.service`)

```ini
# /etc/systemd/system/ais-catcher.service
[Unit]
Description=AIS-catcher Dual-Channel SDR AIS Demodulator Service
Documentation=https://github.com/jvde-github/AIS-catcher
After=network-online.target systemd-udev-settle.service
Wants=network-online.target

[Service]
Type=simple
User=ais
Group=plugdev
SupplementaryGroups=dialout
StateDirectory=ais-catcher
WorkingDirectory=/var/lib/ais-catcher
ExecStart=/usr/local/bin/AIS-catcher -C /etc/ais-catcher/ais-catcher.conf
Restart=always
RestartSec=5
TimeoutStopSec=10

# Security Hardening (Mitigates parser memory corruption CVEs like CVE-2025-66217)
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictSUIDSGID=true
LockPersonality=true
ReadWritePaths=/var/lib/ais-catcher

[Install]
WantedBy=multi-user.target
```

---

### G.5.5 `gpsd` Configuration (`/etc/default/gpsd`)

To expose both your local USB GPS receiver (if present) and the `AIS-catcher` UDP `10110` NMEA stream through `gpsd`:

```ini
# /etc/default/gpsd
# Start the gpsd daemon automatically at boot time
START_DAEMON="true"

# Do not probe random USB serial adapters automatically unless matching udev rules
USBAUTO="false"

# Listen to the local AIS-catcher UDP NMEA 0183 feed on port 10110
DEVICES="udp://127.0.0.1:10110"

# -n: Do not wait for a client to connect before polling the AIS stream
# -G: (Optional) Listen on LAN interface if serving OpenCPN on another laptop
GPSD_OPTIONS="-n"
```

---

## G.6 Production Python Daemon: Automated GeoParquet & DuckDB Archiver

The script below (`/usr/local/bin/ais_archiver.py`) listens continuously to the `AIS-catcher` JSON UDP stream on `127.0.0.1:10111`. It buffers decoded AIS records in memory and flushes them every 5 minutes (or every $10,000$ messages) into:
1. **Hive-Partitioned ZSTD-Compressed GeoParquet Files** (`/var/lib/ais-archive/parquet/year=YYYY/month=MM/day=DD/ais_YYYYMMDD_HHMMSS.parquet`) containing standard IEEE 754 `DOUBLE` coordinates, WKB Point geometry (`POINT (lon lat)`), RF telemetry (`rssi_dbm`, `ppm_offset`, `channel`), raw NMEA sentences, and full JSON attributes.
2. **A Local Analytical `DuckDB` Database** (`/var/lib/ais-archive/ais_station.duckdb`) maintaining a real-time `latest_vessels` state table (most recent position, SOG, COG, heading, ship name, call sign, and dimensions for every MMSI) and an `hourly_rf_stats` table tracking station performance.

### G.6.1 Complete Python Archiver Script (`/usr/local/bin/ais_archiver.py`)

```python
#!/usr/bin/env python3
"""
Production Home AIS Station Archiver (ais_archiver.py)
Ingests AIS-catcher JSON UDP packets (127.0.0.1:10111) and writes:
  1. Hive-partitioned ZSTD Parquet / GeoParquet files (year=YYYY/month=MM/day=DD/)
  2. Real-time DuckDB analytical tables (latest_vessels & hourly_rf_stats)
"""

from __future__ import annotations
import datetime as dt
import json
import logging
import os
import signal
import socket
import struct
import time
from pathlib import Path
from typing import Any, Dict, List, Optional
import duckdb

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("ais_archiver")

UDP_HOST = os.environ.get("AIS_UDP_HOST", "127.0.0.1")
UDP_PORT = int(os.environ.get("AIS_UDP_PORT", "10111"))
ARCHIVE_DIR = Path(os.environ.get("AIS_ARCHIVE_DIR", "/var/lib/ais-archive"))
FLUSH_INTERVAL_SEC = int(os.environ.get("AIS_FLUSH_INTERVAL_SEC", "300"))
MAX_BATCH_SIZE = int(os.environ.get("AIS_MAX_BATCH_SIZE", "10000"))

RUNNING = True


def handle_sigterm(signum: int, frame: Any) -> None:
    global RUNNING
    log.info("Received signal %d; flushing remaining AIS batch before exit...", signum)
    RUNNING = False


signal.signal(signal.SIGTERM, handle_sigterm)
signal.signal(signal.SIGINT, handle_sigterm)


def lonlat_to_wkb_point(lon: Optional[float], lat: Optional[float]) -> Optional[bytes]:
    """Encodes WGS84 (lon, lat) into standard little-endian ISO WKB Point (21 bytes)."""
    if lon is None or lat is None:
        return None
    if not (-180.0 <= lon <= 180.0 and -90.0 <= lat <= 90.0):
        return None
    # Byte 0: 0x01 (little endian), UInt32: 1 (wkbPoint), Double: X (lon), Double: Y (lat)
    return struct.pack("<BIdd", 1, 1, float(lon), float(lat))


def init_duckdb(db_path: Path) -> duckdb.DuckDBPyConnection:
    """Initializes persistent DuckDB database and operational summary tables."""
    con = duckdb.connect(str(db_path))
    con.execute("""
        CREATE TABLE IF NOT EXISTS latest_vessels (
            mmsi BIGINT PRIMARY KEY,
            last_seen_utc TIMESTAMP,
            msg_type INTEGER,
            channel VARCHAR,
            lat DOUBLE,
            lon DOUBLE,
            sog_kts DOUBLE,
            cog_deg DOUBLE,
            heading_deg INTEGER,
            nav_status INTEGER,
            shipname VARCHAR,
            callsign VARCHAR,
            imo BIGINT,
            shiptype INTEGER,
            draught_m DOUBLE,
            destination VARCHAR,
            to_bow INTEGER,
            to_stern INTEGER,
            to_port INTEGER,
            to_starboard INTEGER,
            rssi_dbm DOUBLE,
            ppm_offset DOUBLE
        );

        CREATE TABLE IF NOT EXISTS hourly_rf_stats (
            hour_utc TIMESTAMP,
            channel VARCHAR,
            packet_count BIGINT,
            unique_mmsis BIGINT,
            avg_rssi_dbm DOUBLE,
            min_rssi_dbm DOUBLE,
            avg_ppm_offset DOUBLE,
            PRIMARY KEY (hour_utc, channel)
        );
    """)
    return con


def parse_ais_catcher_json(raw_bytes: bytes) -> Optional[Dict[str, Any]]:
    """Parses a single UDP JSON datagram emitted by AIS-catcher."""
    try:
        payload = json.loads(raw_bytes.decode("utf-8", errors="replace"))
    except json.JSONDecodeError:
        return None

    mmsi = payload.get("mmsi")
    msg_type = payload.get("type")
    if mmsi is None or msg_type is None:
        return None

    rx_time_str = payload.get("rxtime")
    if rx_time_str and len(rx_time_str) == 14:
        # Format: YYYYMMDDHHMMSS
        rx_utc = dt.datetime.strptime(rx_time_str, "%Y%m%d%H%M%S")
    else:
        rx_utc = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)

    lat = payload.get("lat")
    lon = payload.get("lon")
    # Filter ITU-R M.1371 sentinel values (91.0 deg lat, 181.0 deg lon)
    if lat is not None and (lat < -90.0 or lat > 90.0):
        lat = None
    if lon is not None and (lon < -180.0 or lon > 180.0):
        lon = None

    nmea_list = payload.get("nmea", [])
    raw_nmea = "\n".join(nmea_list) if isinstance(nmea_list, list) else str(nmea_list)

    return {
        "rx_utc": rx_utc,
        "mmsi": int(mmsi),
        "msg_type": int(msg_type),
        "channel": str(payload.get("channel", "?"))[:2],
        "rssi_dbm": float(payload["level"]) if "level" in payload and payload["level"] is not None else None,
        "ppm_offset": float(payload["ppm"]) if "ppm" in payload and payload["ppm"] is not None else None,
        "lat": float(lat) if lat is not None else None,
        "lon": float(lon) if lon is not None else None,
        "sog_kts": float(payload["speed"]) if "speed" in payload and payload["speed"] is not None else None,
        "cog_deg": float(payload["course"]) if "course" in payload and payload["course"] is not None else None,
        "heading_deg": int(payload["heading"]) if "heading" in payload and payload["heading"] is not None and payload["heading"] != 511 else None,
        "nav_status": int(payload["status"]) if "status" in payload and payload["status"] is not None else None,
        "shipname": str(payload["shipname"]).strip() if payload.get("shipname") else None,
        "callsign": str(payload["callsign"]).strip() if payload.get("callsign") else None,
        "imo": int(payload["imo"]) if payload.get("imo") else None,
        "shiptype": int(payload["shiptype"]) if payload.get("shiptype") is not None else None,
        "draught_m": float(payload["draught"]) if payload.get("draught") is not None else None,
        "destination": str(payload["destination"]).strip() if payload.get("destination") else None,
        "to_bow": int(payload["to_bow"]) if payload.get("to_bow") is not None else None,
        "to_stern": int(payload["to_stern"]) if payload.get("to_stern") is not None else None,
        "to_port": int(payload["to_port"]) if payload.get("to_port") is not None else None,
        "to_starboard": int(payload["to_starboard"]) if payload.get("to_starboard") is not None else None,
        "geom_wkb": lonlat_to_wkb_point(lon, lat),
        "raw_nmea": raw_nmea,
        "json_payload": json.dumps(payload, separators=(",", ":")),
    }


def flush_batch(con: duckdb.DuckDBPyConnection, batch: List[Dict[str, Any]], archive_dir: Path) -> None:
    """Writes buffered AIS records to partitioned ZSTD Parquet and updates DuckDB tables."""
    if not batch:
        return

    now_utc = dt.datetime.now(dt.timezone.utc)
    part_dir = (
        archive_dir
        / "parquet"
        / f"year={now_utc.year:04d}"
        / f"month={now_utc.month:02d}"
        / f"day={now_utc.day:02d}"
    )
    part_dir.mkdir(parents=True, exist_ok=True)
    parquet_file = part_dir / f"ais_{now_utc.strftime('%Y%m%d_%H%M%S_%f')}.parquet"

    con.execute("""
        CREATE TEMP TABLE IF NOT EXISTS staging_batch (
            rx_utc TIMESTAMP,
            mmsi BIGINT,
            msg_type INTEGER,
            channel VARCHAR,
            rssi_dbm DOUBLE,
            ppm_offset DOUBLE,
            lat DOUBLE,
            lon DOUBLE,
            sog_kts DOUBLE,
            cog_deg DOUBLE,
            heading_deg INTEGER,
            nav_status INTEGER,
            shipname VARCHAR,
            callsign VARCHAR,
            imo BIGINT,
            shiptype INTEGER,
            draught_m DOUBLE,
            destination VARCHAR,
            to_bow INTEGER,
            to_stern INTEGER,
            to_port INTEGER,
            to_starboard INTEGER,
            geom_wkb BLOB,
            raw_nmea VARCHAR,
            json_payload VARCHAR
        );
        DELETE FROM staging_batch;
    """)

    rows = [
        (
            r["rx_utc"], r["mmsi"], r["msg_type"], r["channel"],
            r["rssi_dbm"], r["ppm_offset"], r["lat"], r["lon"],
            r["sog_kts"], r["cog_deg"], r["heading_deg"], r["nav_status"],
            r["shipname"], r["callsign"], r["imo"], r["shiptype"],
            r["draught_m"], r["destination"], r["to_bow"], r["to_stern"],
            r["to_port"], r["to_starboard"], r["geom_wkb"],
            r["raw_nmea"], r["json_payload"],
        )
        for r in batch
    ]
    con.executemany(
        "INSERT INTO staging_batch VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        rows,
    )

    # 1. Export ZSTD-compressed Parquet file sorted by (mmsi, rx_utc) for optimal row-group pruning
    con.execute(f"""
        COPY (
            SELECT * FROM staging_batch ORDER BY mmsi, rx_utc
        ) TO '{parquet_file.as_posix()}' (FORMAT PARQUET, COMPRESSION ZSTD, ROW_GROUP_SIZE 100000);
    """)

    # 2. Upsert latest vessel state in DuckDB (preserving static fields when position reports arrive)
    con.execute("""
        INSERT INTO latest_vessels
        SELECT
            mmsi,
            LAST(rx_utc ORDER BY rx_utc),
            LAST(msg_type ORDER BY rx_utc),
            LAST(channel ORDER BY rx_utc),
            LAST(lat ORDER BY rx_utc) FILTER (WHERE lat IS NOT NULL),
            LAST(lon ORDER BY rx_utc) FILTER (WHERE lon IS NOT NULL),
            LAST(sog_kts ORDER BY rx_utc) FILTER (WHERE sog_kts IS NOT NULL),
            LAST(cog_deg ORDER BY rx_utc) FILTER (WHERE cog_deg IS NOT NULL),
            LAST(heading_deg ORDER BY rx_utc) FILTER (WHERE heading_deg IS NOT NULL),
            LAST(nav_status ORDER BY rx_utc) FILTER (WHERE nav_status IS NOT NULL),
            LAST(shipname ORDER BY rx_utc) FILTER (WHERE shipname IS NOT NULL),
            LAST(callsign ORDER BY rx_utc) FILTER (WHERE callsign IS NOT NULL),
            LAST(imo ORDER BY rx_utc) FILTER (WHERE imo IS NOT NULL),
            LAST(shiptype ORDER BY rx_utc) FILTER (WHERE shiptype IS NOT NULL),
            LAST(draught_m ORDER BY rx_utc) FILTER (WHERE draught_m IS NOT NULL),
            LAST(destination ORDER BY rx_utc) FILTER (WHERE destination IS NOT NULL),
            LAST(to_bow ORDER BY rx_utc) FILTER (WHERE to_bow IS NOT NULL),
            LAST(to_stern ORDER BY rx_utc) FILTER (WHERE to_stern IS NOT NULL),
            LAST(to_port ORDER BY rx_utc) FILTER (WHERE to_port IS NOT NULL),
            LAST(to_starboard ORDER BY rx_utc) FILTER (WHERE to_starboard IS NOT NULL),
            LAST(rssi_dbm ORDER BY rx_utc) FILTER (WHERE rssi_dbm IS NOT NULL),
            LAST(ppm_offset ORDER BY rx_utc) FILTER (WHERE ppm_offset IS NOT NULL)
        FROM staging_batch
        GROUP BY mmsi
        ON CONFLICT (mmsi) DO UPDATE SET
            last_seen_utc = EXCLUDED.last_seen_utc,
            msg_type = EXCLUDED.msg_type,
            channel = EXCLUDED.channel,
            lat = COALESCE(EXCLUDED.lat, latest_vessels.lat),
            lon = COALESCE(EXCLUDED.lon, latest_vessels.lon),
            sog_kts = COALESCE(EXCLUDED.sog_kts, latest_vessels.sog_kts),
            cog_deg = COALESCE(EXCLUDED.cog_deg, latest_vessels.cog_deg),
            heading_deg = COALESCE(EXCLUDED.heading_deg, latest_vessels.heading_deg),
            nav_status = COALESCE(EXCLUDED.nav_status, latest_vessels.nav_status),
            shipname = COALESCE(EXCLUDED.shipname, latest_vessels.shipname),
            callsign = COALESCE(EXCLUDED.callsign, latest_vessels.callsign),
            imo = COALESCE(EXCLUDED.imo, latest_vessels.imo),
            shiptype = COALESCE(EXCLUDED.shiptype, latest_vessels.shiptype),
            draught_m = COALESCE(EXCLUDED.draught_m, latest_vessels.draught_m),
            destination = COALESCE(EXCLUDED.destination, latest_vessels.destination),
            to_bow = COALESCE(EXCLUDED.to_bow, latest_vessels.to_bow),
            to_stern = COALESCE(EXCLUDED.to_stern, latest_vessels.to_stern),
            to_port = COALESCE(EXCLUDED.to_port, latest_vessels.to_port),
            to_starboard = COALESCE(EXCLUDED.to_starboard, latest_vessels.to_starboard),
            rssi_dbm = COALESCE(EXCLUDED.rssi_dbm, latest_vessels.rssi_dbm),
            ppm_offset = COALESCE(EXCLUDED.ppm_offset, latest_vessels.ppm_offset);
    """)

    log.info("Flushed %d AIS messages to %s", len(batch), parquet_file.name)


def main() -> None:
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    db_path = ARCHIVE_DIR / "ais_station.duckdb"
    con = init_duckdb(db_path)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 4 * 1024 * 1024)
    sock.bind((UDP_HOST, UDP_PORT))
    sock.settimeout(1.0)

    log.info("Listening for AIS-catcher JSON datagrams on udp://%s:%d ...", UDP_HOST, UDP_PORT)
    batch: List[Dict[str, Any]] = []
    last_flush = time.monotonic()

    try:
        while RUNNING:
            try:
                data, _ = sock.recvfrom(65535)
                for line in data.splitlines():
                    if not line.strip():
                        continue
                    rec = parse_ais_catcher_json(line)
                    if rec is not None:
                        batch.append(rec)
            except socket.timeout:
                pass

            now = time.monotonic()
            if len(batch) >= MAX_BATCH_SIZE or (batch and (now - last_flush) >= FLUSH_INTERVAL_SEC):
                flush_batch(con, batch, ARCHIVE_DIR)
                batch.clear()
                last_flush = now
    finally:
        if batch:
            flush_batch(con, batch, ARCHIVE_DIR)
        sock.close()
        con.close()
        log.info("AIS archiver shut down cleanly.")


if __name__ == "__main__":
    main()
```

### G.6.2 Archiver `systemd` Service (`/etc/systemd/system/ais-archiver.service`)

```ini
# /etc/systemd/system/ais-archiver.service
[Unit]
Description=AIS-catcher to GeoParquet & DuckDB Archiver Service
After=ais-catcher.service
Requires=ais-catcher.service

[Service]
Type=simple
User=ais
Group=plugdev
StateDirectory=ais-archive
Environment="AIS_UDP_HOST=127.0.0.1"
Environment="AIS_UDP_PORT=10111"
Environment="AIS_ARCHIVE_DIR=/var/lib/ais-archive"
Environment="AIS_FLUSH_INTERVAL_SEC=300"
ExecStart=/usr/bin/python3 /usr/local/bin/ais_archiver.py
Restart=always
RestartSec=5
NoNewPrivileges=true
ProtectSystem=strict
ReadWritePaths=/var/lib/ais-archive

[Install]
WantedBy=multi-user.target
```

---

## G.7 Querying Your Home AIS Station Archive with DuckDB SQL

Once `ais_archiver.py` is running, you can query millions of archived rows directly from the Hive-partitioned Parquet directory without locking the live daemon:

```sql
-- Open an interactive DuckDB session: duckdb -readonly /var/lib/ais-archive/ais_station.duckdb
INSTALL spatial;
LOAD spatial;

-- 1. List the 15 most distant vessels received today with their signal strength (RSSI)
SELECT
    mmsi,
    MAX(shipname) AS vessel_name,
    COUNT(*) AS packets,
    ROUND(MIN(rssi_dbm), 1) AS weakest_rssi_dbm,
    ROUND(MAX(
        2.0 * 3440.065 * ASIN(SQRT(
            POWER(SIN(RADIANS(lat - 37.8199) / 2.0), 2) +
            COS(RADIANS(37.8199)) * COS(RADIANS(lat)) *
            POWER(SIN(RADIANS(lon - (-122.4783)) / 2.0), 2)
        ))
    ), 2) AS max_distance_nm
FROM read_parquet('/var/lib/ais-archive/parquet/*/*/*/*.parquet', hive_partitioning = true)
WHERE lat IS NOT NULL AND lon IS NOT NULL
GROUP BY mmsi
ORDER BY max_distance_nm DESC
LIMIT 15;
```
