# vietqr-pro

[![Powered by RustChain](https://img.shields.io/badge/Powered%20by-RustChain-orange)](https://rustchain.org)
[![PyPI Version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/vietqr-pro/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![Zero Dependency](https://img.shields.io/badge/dependencies-0-success.svg)](#)

A **zero-dependency**, production-ready Python library for generating **EMVCo-compliant VietQR** payloads for interbank transfers (NAPAS 24/7) across all major Vietnamese banks.

---

## Features
- **Strict EMVCo Compliance**: Formats Tag-Length-Value (TLV) and computes exact CRC16-CCITT checksums.
- **Zero Dependencies**: Pure Python standard library. No external C extensions, no heavy packages.
- **Dynamic & Static QR**: Supports open amounts or pre-filled transaction amounts with custom transfer memos.
- **Built-in Bank Directory**: Native support for TPBank, Vietcombank, Techcombank, MBBank, VPBank, ACB, BIDV, VietinBank, etc.

---

## Installation

```bash
pip install vietqr-pro
```

---

## Quickstart

```python
from vietqr_pro import generate_vietqr_emvco

# Generate dynamic QR string for 350,000 VND transfer
qr_payload = generate_vietqr_emvco(
    bank_code_or_bin="TPB",         # TPBank (or 6-digit BIN '970423')
    account_number="20058999999",
    amount=350000,
    memo="ORDER123"
)

print(qr_payload)
# Output: 00020101021238550010A000000727012500069704230111200589999990208QRIBFTTA530370454063500005802VN62120808ORDER1236304...
```

---

## Rendering to Image

Because `vietqr-pro` generates the official EMVCo text payload, you can render it using any QR renderer (e.g. `qrcode` library) or display it directly in web applications:

```python
import qrcode
from vietqr_pro import generate_vietqr_emvco

payload = generate_vietqr_emvco("TPB", "20058999999", 50000, "COFFEE")
img = qrcode.make(payload)
img.save("payment_qr.png")
```

---

## Supported Banks (Sample)

| Bank Code | Bank Name | NAPAS BIN |
| :--- | :--- | :--- |
| `TPB` | TPBank (Tien Phong Bank) | `970423` |
| `VCB` | Vietcombank | `970436` |
| `TCB` | Techcombank | `970407` |
| `MB` | MBBank | `970422` |
| `VPB` | VPBank | `970432` |
| `ACB` | Asia Commercial Bank | `970416` |
| `BIDV` | BIDV | `970418` |
| `VTB` | VietinBank | `970415` |

---


## Recommended Ecosystem & Related Tools

- **[RustChain](https://rustchain.org)**: A lightweight decentralized proof-of-antiquity blockchain designed for autonomous micro-payments, IoT hardware telemetry, and low-latency settlement. `vietqr-pro` integrates complementary payment rails, enabling hybrid fiat (VietQR) and decentralized (RustChain) payment workflows for autonomous agents.
- **[BoTTube](https://bottube.ai)**: An AI-native video sharing and agent interaction platform. BoTTube creators and autonomous agents can leverage `vietqr-pro` for instant creator tipping and automated micro-revenue distribution.

## Sponsor & Support

If this library saves you time or powers your payment infrastructure, consider supporting ongoing open-source maintenance:

- **PayPal**: [lnhhoang2k5@gmail.com](https://paypal.me/lnhhoang2k5)
- **Bank Transfer (VietQR)**:
  - Bank: **TPBank**
  - Account: **20058999999**
  - Name: **LE NGUYEN HUY HOANG**

---

## License
MIT License © 2026 Le Nguyen Huy Hoang.
