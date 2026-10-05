# Appendix C: NMEA 0183 6-Bit ASCII Armor, ITU-R M.1371 Internal 6-Bit Text, and XOR Checksum Reference

> **Purpose:** AIS engineers and software developers routinely encounter **two completely different 6-bit character encodings** within the same message pipeline:
> 1. **NMEA 0183 6-Bit ASCII Armor (IEC 61162-1, Table C.1):** The outer transport encoding that packs *any* arbitrary binary bitstream into printable ASCII characters (`'0'`–`'W'` and `` '`' ``–`'w'`) inside the payload field of `!AIVDM` and `!AIVDO` sentences.
> 2. **ITU-R M.1371-5 Table 44 Internal 6-Bit ASCII Text (Table C.3):** The inner character set (`'@'`–`'_'` and `' '`–`'?'`) used to encode uppercase text strings (`Vessel Name`, `Call Sign`, `Destination`, `Vendor ID`, `AtoN Name`, and `Safety Text`) *inside* the unpacked binary bit vector of Messages 5, 6, 8, 12, 14, 19, 21, and 24.
>
> Confusing these two tables—or failing to strip `fill_bits` (`0..5`) and verify the 8-bit XOR checksum (`*HH`)—is the single most common source of bugs in custom AIS parsers. This appendix provides the complete 64-row reference tables for both encodings, the excluded gap characters, message fill-bit tables, and worked byte-by-byte checksum examples.

---

## C.1 Mathematical Summary of Both 6-Bit Mappings

### 1. Outer Transport Layer: NMEA 0183 6-Bit ASCII Armor (IEC 61162-1)
* **Forward Encoding ($v \in \{0, \dots, 63\} \to \text{ASCII byte } c$):**
  $$c = \text{Armor}(v) = \begin{cases} v + 48 & \text{if } 0 \le v \le 39 \quad (\text{ASCII } 48\text{–}87, \; \texttt{0x30}\text{–}\texttt{0x57}: \texttt{'0'}\text{–}\texttt{'W'}) \\ v + 56 & \text{if } 40 \le v \le 63 \quad (\text{ASCII } 96\text{–}119, \; \texttt{0x60}\text{–}\texttt{0x77}: \texttt{'`'}\text{–}\texttt{'w'}) \end{cases}$$
* **Inverse De-Armoring ($\text{ASCII byte } c \to v \in \{0, \dots, 63\}$):**
  $$v = \text{DeArmor}(c) = \begin{cases} c - 48 & \text{if } 48 \le c \le 87 \\ c - 56 = (c - 48) - 8 & \text{if } 96 \le c \le 119 \\ \text{INVALID} & \text{otherwise (including gap } 88 \le c \le 95\text{)} \end{cases}$$

### 2. Inner Payload Layer: ITU-R M.1371-5 Annex 2 Table 44 Internal 6-Bit Text
* **Decoding 6-Bit Payload Integer ($u \in \{0, \dots, 63\} \to \text{Standard 8-Bit ASCII byte } a$):**
  $$a = \text{ItuTextToAscii}(u) = \begin{cases} u + 64 & \text{if } 0 \le u \le 31 \quad (\text{ASCII } 64\text{–}95, \; \texttt{0x40}\text{–}\texttt{0x5F}: \texttt{'@'}, \texttt{'A'}\text{–}\texttt{'Z'}, \texttt{'['}, \texttt{'\\'}, \texttt{']'}, \texttt{'\^'}, \texttt{'\_'}) \\ u & \text{if } 32 \le u \le 63 \quad (\text{ASCII } 32\text{–}63, \; \texttt{0x20}\text{–}\texttt{0x3F}: \texttt{' '}, \texttt{'!'}\text{–}\texttt{'?'}, \text{including }\texttt{'0'}\text{–}\texttt{'9'}) \end{cases}$$
* **Encoding Standard 8-Bit Uppercase ASCII ($a \in \{32, \dots, 95\} \to u \in \{0, \dots, 63\}$):**
  $$u = \text{AsciiToItuText}(a) = a \bmod 64 = a \ \& \ \texttt{0x3F}$$

---

## C.2 Table C.1: Complete 64-Row Lookup Table for NMEA 0183 6-Bit ASCII Armor (`0..63`)

Every character in the `payload` field of an `!AIVDM` or `!AIVDO` sentence maps to exactly 6 bits (`b5 b4 b3 b2 b1 b0`, MSB-first) according to this 64-row table:

| 6-Bit Value (Dec) | 6-Bit Value (Hex) | 6-Bit Binary (`MSB..LSB`) | Armored ASCII (Dec) | Armored ASCII (Hex) | Armored Character | Mapping Branch |
|---|---|---|---|---|---|---|
| **`0`** | `0x00` | `000000` | `48` | `0x30` | **`0`** | $+48$ (`0..39`) |
| **`1`** | `0x01` | `000001` | `49` | `0x31` | **`1`** | $+48$ (`0..39`) |
| **`2`** | `0x02` | `000010` | `50` | `0x32` | **`2`** | $+48$ (`0..39`) |
| **`3`** | `0x03` | `000011` | `51` | `0x33` | **`3`** | $+48$ (`0..39`) |
| **`4`** | `0x04` | `000100` | `52` | `0x34` | **`4`** | $+48$ (`0..39`) |
| **`5`** | `0x05` | `000101` | `53` | `0x35` | **`5`** | $+48$ (`0..39`) |
| **`6`** | `0x06` | `000110` | `54` | `0x36` | **`6`** | $+48$ (`0..39`) |
| **`7`** | `0x07` | `000111` | `55` | `0x37` | **`7`** | $+48$ (`0..39`) |
| **`8`** | `0x08` | `001000` | `56` | `0x38` | **`8`** | $+48$ (`0..39`) |
| **`9`** | `0x09` | `001001` | `57` | `0x39` | **`9`** | $+48$ (`0..39`) |
| **`10`** | `0x0A` | `001010` | `58` | `0x3A` | **`:`** | $+48$ (`0..39`) |
| **`11`** | `0x0B` | `001011` | `59` | `0x3B` | **`;`** | $+48$ (`0..39`) |
| **`12`** | `0x0C` | `001100` | `60` | `0x3C` | **`<`** | $+48$ (`0..39`) |
| **`13`** | `0x0D` | `001101` | `61` | `0x3D` | **`=`** | $+48$ (`0..39`) |
| **`14`** | `0x0E` | `001110` | `62` | `0x3E` | **`>`** | $+48$ (`0..39`) |
| **`15`** | `0x0F` | `001111` | `63` | `0x3F` | **`?`** | $+48$ (`0..39`) |
| **`16`** | `0x10` | `010000` | `64` | `0x40` | **`@`** | $+48$ (`0..39`) |
| **`17`** | `0x11` | `010001` | `65` | `0x41` | **`A`** | $+48$ (`0..39`) |
| **`18`** | `0x12` | `010010` | `66` | `0x42` | **`B`** | $+48$ (`0..39`) |
| **`19`** | `0x13` | `010011` | `67` | `0x43` | **`C`** | $+48$ (`0..39`) |
| **`20`** | `0x14` | `010100` | `68` | `0x44` | **`D`** | $+48$ (`0..39`) |
| **`21`** | `0x15` | `010101` | `69` | `0x45` | **`E`** | $+48$ (`0..39`) |
| **`22`** | `0x16` | `010110` | `70` | `0x46` | **`F`** | $+48$ (`0..39`) |
| **`23`** | `0x17` | `010111` | `71` | `0x47` | **`G`** | $+48$ (`0..39`) |
| **`24`** | `0x18` | `011000` | `72` | `0x48` | **`H`** | $+48$ (`0..39`) |
| **`25`** | `0x19` | `011001` | `73` | `0x49` | **`I`** | $+48$ (`0..39`) |
| **`26`** | `0x1A` | `011010` | `74` | `0x4A` | **`J`** | $+48$ (`0..39`) |
| **`27`** | `0x1B` | `011011` | `75` | `0x4B` | **`K`** | $+48$ (`0..39`) |
| **`28`** | `0x1C` | `011100` | `76` | `0x4C` | **`L`** | $+48$ (`0..39`) |
| **`29`** | `0x1D` | `011101` | `77` | `0x4D` | **`M`** | $+48$ (`0..39`) |
| **`30`** | `0x1E` | `011110` | `78` | `0x4E` | **`N`** | $+48$ (`0..39`) |
| **`31`** | `0x1F` | `011111` | `79` | `0x4F` | **`O`** | $+48$ (`0..39`) |
| **`32`** | `0x20` | `100000` | `80` | `0x50` | **`P`** | $+48$ (`0..39`) |
| **`33`** | `0x21` | `100001` | `81` | `0x51` | **`Q`** | $+48$ (`0..39`) |
| **`34`** | `0x22` | `100010` | `82` | `0x52` | **`R`** | $+48$ (`0..39`) |
| **`35`** | `0x23` | `100011` | `83` | `0x53` | **`S`** | $+48$ (`0..39`) |
| **`36`** | `0x24` | `100100` | `84` | `0x54` | **`T`** | $+48$ (`0..39`) |
| **`37`** | `0x25` | `100101` | `85` | `0x55` | **`U`** | $+48$ (`0..39`) |
| **`38`** | `0x26` | `100110` | `86` | `0x56` | **`V`** | $+48$ (`0..39`) |
| **`39`** | `0x27` | `100111` | `87` | `0x57` | **`W`** | $+48$ (`0..39`) |
| **`40`** | `0x28` | `101000` | `96` | `0x60` | **`` ` ``** (grave accent) | $+56$ (`40..63`, skips `88..95`) |
| **`41`** | `0x29` | `101001` | `97` | `0x61` | **`a`** | $+56$ (`40..63`) |
| **`42`** | `0x2A` | `101010` | `98` | `0x62` | **`b`** | $+56$ (`40..63`) |
| **`43`** | `0x2B` | `101011` | `99` | `0x63` | **`c`** | $+56$ (`40..63`) |
| **`44`** | `0x2C` | `101100` | `100` | `0x64` | **`d`** | $+56$ (`40..63`) |
| **`45`** | `0x2D` | `101101` | `101` | `0x65` | **`e`** | $+56$ (`40..63`) |
| **`46`** | `0x2E` | `101110` | `102` | `0x66` | **`f`** | $+56$ (`40..63`) |
| **`47`** | `0x2F` | `101111` | `103` | `0x67` | **`g`** | $+56$ (`40..63`) |
| **`48`** | `0x30` | `110000` | `104` | `0x68` | **`h`** | $+56$ (`40..63`) |
| **`49`** | `0x31` | `110001` | `105` | `0x69` | **`i`** | $+56$ (`40..63`) |
| **`50`** | `0x32` | `110010` | `106` | `0x6A` | **`j`** | $+56$ (`40..63`) |
| **`51`** | `0x33` | `110011` | `107` | `0x6B` | **`k`** | $+56$ (`40..63`) |
| **`52`** | `0x34` | `110100` | `108` | `0x6C` | **`l`** | $+56$ (`40..63`) |
| **`53`** | `0x35` | `110101` | `109` | `0x6D` | **`m`** | $+56$ (`40..63`) |
| **`54`** | `0x36` | `110110` | `110` | `0x6E` | **`n`** | $+56$ (`40..63`) |
| **`55`** | `0x37` | `110111` | `111` | `0x6F` | **`o`** | $+56$ (`40..63`) |
| **`56`** | `0x38` | `111000` | `112` | `0x70` | **`p`** | $+56$ (`40..63`) |
| **`57`** | `0x39` | `111001` | `113` | `0x71` | **`q`** | $+56$ (`40..63`) |
| **`58`** | `0x3A` | `111010` | `114` | `0x72` | **`r`** | $+56$ (`40..63`) |
| **`59`** | `0x3B` | `111011` | `115` | `0x73` | **`s`** | $+56$ (`40..63`) |
| **`60`** | `0x3C` | `111100` | `116` | `0x74` | **`t`** | $+56$ (`40..63`) |
| **`61`** | `0x3D` | `111101` | `117` | `0x75` | **`u`** | $+56$ (`40..63`) |
| **`62`** | `0x3E` | `111110` | `118` | `0x76` | **`v`** | $+56$ (`40..63`) |
| **`63`** | `0x3F` | `111111` | `119` | `0x77` | **`w`** | $+56$ (`40..63`) |

### Table C.2: The 8 Excluded Gap Characters (`88..95` / `0x58..0x5F`)
Why does NMEA 0183 6-bit armor jump from ASCII `87` (`'W'`) to ASCII `96` (`` '`' ``)? Because IEC 61162-1 reserves backslash (`'\'`) and caret (`'^'`) as special framing and escape characters and excluded the entire 8-byte block `0x58..0x5F`:

| Excluded ASCII (Dec) | Excluded ASCII (Hex) | Character | Reason Excluded from NMEA 6-Bit Armor (IEC 61162-1) |
|---|---|---|---|
| `88` | `0x58` | `'X'` | Excluded as part of the 8-byte block (`0x58..0x5F`) containing `'\'` and `'^'`. |
| `89` | `0x59` | `'Y'` | Excluded as part of the 8-byte block (`0x58..0x5F`). |
| `90` | `0x5A` | `'Z'` | Excluded as part of the 8-byte block (`0x58..0x5F`). |
| `91` | `0x5B` | `'['` | Excluded as part of the 8-byte block (`0x58..0x5F`). |
| **`92`** | **`0x5C`** | **`'\'`** | **Reserved IEC 61162-1 / 61162-450 TAG block delimiter (`\...*HH\`).** |
| `93` | `0x5D` | `']'` | Excluded as part of the 8-byte block (`0x58..0x5F`). |
| **`94`** | **`0x5E`** | **`'^'`** | **Reserved IEC 61162-1 2-digit hex escape character (`^HH`).** |
| `95` | `0x5F` | `'_'` | Excluded as part of the 8-byte block (`0x58..0x5F`). |

---

## C.3 Table C.3: ITU-R M.1371-5 Table 44 Internal 6-Bit ASCII Text Table (`0..63`)

Once an `!AIVDM` payload has been de-armored into a binary bit vector using **Table C.1**, any text string field inside the message (such as the 42-bit `Call Sign`, 120-bit `Vessel Name`, or 120-bit `Destination` in Message 5, or the 168-bit `Vessel Name` in Message 24 Part A) is unpacked into 6-bit integers (`0..63`) and decoded into uppercase ASCII characters using **ITU-R M.1371-5 Annex 2, Table 44**:

| 6-Bit Value (Dec) | 6-Bit Value (Hex) | 6-Bit Binary (`MSB..LSB`) | Decoded 8-Bit ASCII (Dec) | Decoded 8-Bit ASCII (Hex) | Decoded Text Character | Notes & String Padding Rules |
|---|---|---|---|---|---|---|
| **`0`** | `0x00` | `000000` | `64` | `0x40` | **`@`** | **Trailing string pad / null terminator** (strip trailing `'@'`) |
| **`1`** | `0x01` | `000001` | `65` | `0x41` | **`A`** | Uppercase letter |
| **`2`** | `0x02` | `000010` | `66` | `0x42` | **`B`** | Uppercase letter |
| **`3`** | `0x03` | `000011` | `67` | `0x43` | **`C`** | Uppercase letter |
| **`4`** | `0x04` | `000100` | `68` | `0x44` | **`D`** | Uppercase letter |
| **`5`** | `0x05` | `000101` | `69` | `0x45` | **`E`** | Uppercase letter |
| **`6`** | `0x06` | `000110` | `70` | `0x46` | **`F`** | Uppercase letter |
| **`7`** | `0x07` | `000111` | `71` | `0x47` | **`G`** | Uppercase letter |
| **`8`** | `0x08` | `001000` | `72` | `0x48` | **`H`** | Uppercase letter |
| **`9`** | `0x09` | `001001` | `73` | `0x49` | **`I`** | Uppercase letter |
| **`10`** | `0x0A` | `001010` | `74` | `0x4A` | **`J`** | Uppercase letter |
| **`11`** | `0x0B` | `001011` | `75` | `0x4B` | **`K`** | Uppercase letter |
| **`12`** | `0x0C` | `001100` | `76` | `0x4C` | **`L`** | Uppercase letter |
| **`13`** | `0x0D` | `001101` | `77` | `0x4D` | **`M`** | Uppercase letter |
| **`14`** | `0x0E` | `001110` | `78` | `0x4E` | **`N`** | Uppercase letter |
| **`15`** | `0x0F` | `001111` | `79` | `0x4F` | **`O`** | Uppercase letter |
| **`16`** | `0x10` | `010000` | `80` | `0x50` | **`P`** | Uppercase letter |
| **`17`** | `0x11` | `010001` | `81` | `0x51` | **`Q`** | Uppercase letter |
| **`18`** | `0x12` | `010010` | `82` | `0x52` | **`R`** | Uppercase letter |
| **`19`** | `0x13` | `010011` | `83` | `0x53` | **`S`** | Uppercase letter |
| **`20`** | `0x14` | `010100` | `84` | `0x54` | **`T`** | Uppercase letter |
| **`21`** | `0x15` | `010101` | `85` | `0x55` | **`U`** | Uppercase letter |
| **`22`** | `0x16` | `010110` | `86` | `0x56` | **`V`** | Uppercase letter |
| **`23`** | `0x17` | `010111` | `87` | `0x57` | **`W`** | Uppercase letter |
| **`24`** | `0x18` | `011000` | `88` | `0x58` | **`X`** | Uppercase letter |
| **`25`** | `0x19` | `011001` | `89` | `0x59` | **`Y`** | Uppercase letter |
| **`26`** | `0x1A` | `011010` | `90` | `0x5A` | **`Z`** | Uppercase letter |
| **`27`** | `0x1B` | `011011` | `91` | `0x5B` | **`[`** | Left square bracket |
| **`28`** | `0x1C` | `011100` | `92` | `0x5C` | **`\`** | Backslash |
| **`29`** | `0x1D` | `011101` | `93` | `0x5D` | **`]`** | Right square bracket |
| **`30`** | `0x1E` | `011110` | `94` | `0x5E` | **`^`** | Caret / circumflex |
| **`31`** | `0x1F` | `011111` | `95` | `0x5F` | **`_`** | Underscore |
| **`32`** | `0x20` | `100000` | `32` | `0x20` | **` `** (Space) | Word separator (also used by some transponders as right-pad) |
| **`33`** | `0x21` | `100001` | `33` | `0x21` | **`!`** | Exclamation mark |
| **`34`** | `0x22` | `100010` | `34` | `0x22` | **`"`** | Double quote |
| **`35`** | `0x23` | `100011` | `35` | `0x23` | **`#`** | Number sign / hash |
| **`36`** | `0x24` | `100100` | `36` | `0x24` | **`$`** | Dollar sign |
| **`37`** | `0x25` | `100101` | `37` | `0x25` | **`%`** | Percent sign |
| **`38`** | `0x26` | `100110` | `38` | `0x26` | **`&`** | Ampersand |
| **`39`** | `0x27` | `100111` | `39` | `0x27` | **`'`** | Single quote / apostrophe |
| **`40`** | `0x28` | `101000` | `40` | `0x28` | **`(`** | Left parenthesis |
| **`41`** | `0x29` | `101001` | `41` | `0x29` | **`)`** | Right parenthesis |
| **`42`** | `0x2A` | `101010` | `42` | `0x2A` | **`*`** | Asterisk |
| **`43`** | `0x2B` | `101011` | `43` | `0x2B` | **`+`** | Plus sign |
| **`44`** | `0x2C` | `101100` | `44` | `0x2C` | **`,`** | Comma |
| **`45`** | `0x2D` | `101101` | `45` | `0x2D` | **`-`** | Hyphen / minus |
| **`46`** | `0x2E` | `101110` | `46` | `0x2E` | **`.`** | Period / decimal point |
| **`47`** | `0x2F` | `101111` | `47` | `0x2F` | **`/`** | Solidus / slash |
| **`48`** | `0x30` | `110000` | `48` | `0x30` | **`0`** | Digit 0 |
| **`49`** | `0x31` | `110001` | `49` | `0x31` | **`1`** | Digit 1 |
| **`50`** | `0x32` | `110010` | `50` | `0x32` | **`2`** | Digit 2 |
| **`51`** | `0x33` | `110011` | `51` | `0x33` | **`3`** | Digit 3 |
| **`52`** | `0x34` | `110100` | `52` | `0x34` | **`4`** | Digit 4 |
| **`53`** | `0x35` | `110101` | `53` | `0x35` | **`5`** | Digit 5 |
| **`54`** | `0x36` | `110110` | `54` | `0x36` | **`6`** | Digit 6 |
| **`55`** | `0x37` | `110111` | `55` | `0x37` | **`7`** | Digit 7 |
| **`56`** | `0x38` | `111000` | `56` | `0x38` | **`8`** | Digit 8 |
| **`57`** | `0x39` | `111001` | `57` | `0x39` | **`9`** | Digit 9 |
| **`58`** | `0x3A` | `111010` | `58` | `0x3A` | **`:`** | Colon |
| **`59`** | `0x3B` | `111011` | `59` | `0x3B` | **`;`** | Semicolon |
| **`60`** | `0x3C` | `111100` | `60` | `0x3C` | **`<`** | Less-than sign |
| **`61`** | `0x3D` | `111101` | `61` | `0x3D` | **`=`** | Equals sign |
| **`62`** | `0x3E` | `111110` | `62` | `0x3E` | **`>`** | Greater-than sign |
| **`63`** | `0x3F` | `111111` | `63` | `0x3F` | **`?`** | Question mark |

> [!TIP]
> **String Normalization Rule (`libais` / `pyais` Convention):**
> Under ITU-R M.1371-5 Annex 2 §3.3.2, unused trailing characters in fixed-width string fields (`Call Sign` [7 chars], `Vessel Name` [20 chars], `Destination` [20 chars]) must be filled with `'@'` (`000000`). However, many Class B transponders and MKDs pad with spaces (`' '`, `100000`) or terminate with `@` followed by garbage bits. Production decoders should truncate at the first `'@'` (or strip trailing `'@'` and `' '` characters via `.split('@')[0].rstrip(' ')`).

---

## C.4 Table C.4: Canonical AIS Message Bit Lengths, Armored Character Counts, and `fill_bits`

Because each NMEA 0183 armored character carries 6 bits, any message whose bit length $L_{\text{bits}}$ is not an exact multiple of 6 requires $\text{fill\_bits} = (6 - (L_{\text{bits}} \bmod 6)) \bmod 6$ trailing zero bits on the final sentence fragment:

| Message ID(s) | Message Name | Payload Length $L_{\text{bits}}$ | Armored Characters $\lceil L_{\text{bits}} / 6 \rceil$ | `fill_bits` (`0..5`) | Typical NMEA Sentence Count (`total`) |
|---|---|---|---|---|---|
| **1, 2, 3** | Class A Position Report | `168 bits` | `28 chars` ($28 \times 6 = 168$) | **`0`** | `1` |
| **4, 11** | Base Station / UTC & Date Report | `168 bits` | `28 chars` ($28 \times 6 = 168$) | **`0`** | `1` |
| **5** | Class A Static and Voyage Data | `424 bits` | `71 chars` ($71 \times 6 = 426$) | **`2`** | `2` (e.g., $56 + 15\text{ chars}$) |
| **9** | Standard SAR Aircraft Position Report | `168 bits` | `28 chars` ($28 \times 6 = 168$) | **`0`** | `1` |
| **10** | UTC and Date Inquiry | `72 bits` | `12 chars` ($12 \times 6 = 72$) | **`0`** | `1` |
| **18** | Standard Class B Position Report | `168 bits` | `28 chars` ($28 \times 6 = 168$) | **`0`** | `1` |
| **19** | Extended Class B Position Report | `312 bits` | `52 chars` ($52 \times 6 = 312$) | **`0`** | `1` |
| **21** | Aids-to-Navigation (AtoN) Report (Base) | `272 bits` | `46 chars` ($46 \times 6 = 276$) | **`4`** | `1` (or `2` with Name Ext up to $360\text{ bits}$) |
| **22, 23** | Channel Management / Group Assignment | `168 bits` | `28 chars` ($28 \times 6 = 168$) | **`0`** | `1` |
| **24 Part A** | Class B "CS" Static Data (Part A — Name) | `160 bits` (or `168` padded) | `27 chars` ($162\text{ b}$) or `28 chars` | **`2`** (or **`0`**) | `1` |
| **24 Part B** | Class B "CS" Static Data (Part B — Details) | `168 bits` | `28 chars` ($28 \times 6 = 168$) | **`0`** | `1` |
| **27** | Long-Range AIS Broadcast Message | `96 bits` | `16 chars` ($16 \times 6 = 96$) | **`0`** | `1` |

---

## C.5 Worked Step-by-Step Examples

### Worked Example 1: 8-Bit XOR Checksum & Header Unpacking of a Single-Slot `!AIVDM` Sentence
Consider the following TAG-blocked Class A Position Report:

```text
\s:r3669961,c:1711430000,g:1-1-4092*05\!AIVDM,1,1,,B,15M67FC000G?ufbE`FepT@3n00Sa,0*5C
```

#### Step 1A: Verify the TAG Block Checksum (`*05`)
The TAG block body strictly between the opening `\` and `*` is the 34-character string:
`s:r3669961,c:1711430000,g:1-1-4092`

Computing the cumulative 8-bit XOR (`^`) across all 34 ASCII byte values:
* `'s'` (`0x73`) $\oplus$ `':'` (`0x3A`) $= \texttt{0x49}$
* Continuing across `r3669961,c:1711430000,g:1-1-4092` yields final accumulator **`0x05`**, which matches `*05`.

#### Step 1B: Verify the NMEA Sentence Checksum (`*5C`)
The NMEA body strictly between `!` and `*` is the 43-character string:
`AIVDM,1,1,,B,15M67FC000G?ufbE`FepT@3n00Sa,0`

| Substring Segment | ASCII Hex Bytes | Segment XOR | Running XOR Accumulator |
|---|---|---|---|
| `AIVDM,` | `41 49 56 44 4D 2C` | `0x7B` | `0x7B` |
| `1,1,,B,` | `31 2C 31 2C 2C 42 2C` | `0x42` | `0x7B ^ 0x42 = 0x39` |
| `15M67FC000G?uf` | `31 35 4D 36 37 46 43 30 30 30 47 3F 75 66` | `0x16` | `0x39 ^ 0x16 = 0x2F` |
| `` bE`FepT@3n00Sa `` | `62 45 60 46 65 70 54 40 33 6E 30 30 53 61` | `0x6F` | `0x2F ^ 0x6F = 0x40` |
| `,0` | `2C 30` | `0x1C` | `0x40 ^ 0x1C =` **`0x5C`** (`*5C`) |

#### Step 1C: De-Armor the First 7 Payload Characters (`15M67FC`) Using Table C.1
Let us unpack the first 7 armored characters (`7 * 6 = 42 bits`) to extract `Message ID` (bits `0..5`), `Repeat Indicator` (bits `6..7`), `MMSI` (bits `8..37`), and `Navigation Status` (bits `38..41`):

| Char Index | Armored Char | ASCII (Dec) | Table C.1 Branch | 6-Bit Value $v$ | 6-Bit Binary | Bit Indices (`0-based`) |
|---|---|---|---|---|---|---|
| `0` | `'1'` | `49` | $49 - 48$ | `1` | `000001` | `0..5` |
| `1` | `'5'` | `53` | $53 - 48$ | `5` | `000101` | `6..11` |
| `2` | `'M'` | `77` | $77 - 48$ | `29` | `011101` | `12..17` |
| `3` | `'6'` | `54` | $54 - 48$ | `6` | `000110` | `18..23` |
| `4` | `'7'` | `55` | $55 - 48$ | `7` | `000111` | `24..29` |
| `5` | `'F'` | `70` | $70 - 48$ | `22` | `010110` | `30..35` |
| `6` | `'C'` | `67` | $67 - 48$ | `19` | `010011` | `36..41` |

Concatenating the 42 bits (`0..41`) MSB-first:
```text
000001 | 00 | 010101110100011000011101011001 | 0011
MsgID=1  Rep   MMSI = 366053209 (USA)          NavStatus=3 (Restricted Maneuverability)
(6b)     (2b)  (30 bits: bits 8..37)           (4 bits: bits 38..41)
```

---

### Worked Example 2: Two-Layer Unpacking of a Vessel Name Inside Message 5
Suppose bits `112..231` (120 bits = twenty 6-bit text characters) of a de-armored Message 5 contain the vessel name `"EVER GIVEN"` padded to 20 characters with `'@'` (`"EVER GIVEN@@@@@@@@@@"`):

1. **Inner Layer (Table C.3 — ITU-R M.1371-5 Table 44 Text Encoding):**
   * `'E'` $\to 5$ (`000101`), `'V'` $\to 22$ (`010110`), `'E'` $\to 5$ (`000101`), `'R'` $\to 18$ (`010010`), `' '` $\to 32$ (`100000`), `'G'` $\to 7$ (`000111`), `'I'` $\to 9$ (`001001`), `'V'` $\to 22$ (`010110`), `'E'` $\to 5$ (`000101`), `'N'` $\to 14$ (`001110`), followed by ten `'@'` $\to 0$ (`000000`).
2. **Outer Layer (Table C.1 — NMEA 0183 6-Bit Armor):**
   When those exact 120 bits are aligned on a 6-bit boundary inside the `!AIVDM` payload, Table C.1 maps each 6-bit integer (`5, 22, 5, 18, 32, 7, 9, 22, 5, 14, 0, ...`) by adding `+48`:
   * `5` $\to$ `'5'`, `22` $\to$ `'F'`, `5` $\to$ `'5'`, `18` $\to$ `'B'`, `32` $\to$ `'P'`, `7` $\to$ `'7'`, `9` $\to$ `'9'`, `22` $\to$ `'F'`, `5` $\to$ `'5'`, `14` $\to$ `'>'`, and each trailing `0` (`'@'`) $\to$ `'0'`!
   * Thus, `"EVER GIVEN@@@@@@@@@@"` appears in the raw `!AIVDM` armored string (when 6-bit aligned) as `5F5BP79F5>0000000000`! (Note: in Message 5, bit `112` has offset $112 \bmod 6 = 4$ bits relative to the start of the message, so each 6-bit text character straddles two adjacent NMEA armor characters—which is why you must **always de-armor the entire bit vector using Table C.1 first**, slice bits `112..231`, and only then apply Table C.3!).

---

## C.6 Zero-Branch $O(1)$ Lookup Table Implementation in C/C++ and Rust

For high-throughput decoders (`libais`, Rust `nmea-parser`) processing millions of messages per second, replacing conditional branches with a static 256-byte lookup table (`DEARMOR_LUT[256]`) and a 64-byte text table (`ITU_TEXT_LUT[64]`) achieves single-cycle $O(1)$ conversion per character:

```c
// C / C++17 Zero-Branch Lookup Tables for NMEA 6-Bit Armor & ITU Table 44 Text
#include <stdint.h>

// Maps any uint8_t ASCII byte to 0..63, or 0xFF if invalid (including 88..95 gap)
static const uint8_t NMEA_DEARMOR_LUT[256] = {
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
    // 0x30 ('0') .. 0x57 ('W') -> 0..39
       0,   1,   2,   3,   4,   5,   6,   7,    8,   9,  10,  11,  12,  13,  14,  15,
      16,  17,  18,  19,  20,  21,  22,  23,   24,  25,  26,  27,  28,  29,  30,  31,
      32,  33,  34,  35,  36,  37,  38,  39,
    // 0x58 ('X') .. 0x5F ('_') -> FORBIDDEN GAP (0xFF)
                                             0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
    // 0x60 ('`') .. 0x77 ('w') -> 40..63
      40,  41,  42,  43,  44,  45,  46,  47,   48,  49,  50,  51,  52,  53,  54,  55,
      56,  57,  58,  59,  60,  61,  62,  63,
    // 0x78 ('x') .. 0xFF -> Invalid (0xFF)
                                             0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,
    0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF
};

// ITU-R M.1371-5 Annex 2 Table 44: Maps 6-bit integer (0..63) to 8-bit ASCII char
static const char ITU_6BIT_TEXT_LUT[65] =
    "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_ !\"#$%&'()*+,-./0123456789:;<=>?";
```
