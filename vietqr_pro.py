"""
vietqr_pro: A zero-dependency, production-grade EMVCo-compliant VietQR generator for Python.
Conforms to State Bank of Vietnam / NAPAS EMVCo Merchant-Presented Mode specifications.
"""

from typing import Optional

# Standard NAPAS BIN mapping for popular Vietnamese banks
BANK_BINS = {
    "TPB": "970423",   # TPBank (Tien Phong Bank)
    "VCB": "970436",   # Vietcombank
    "TCB": "970407",   # Techcombank
    "MB":  "970422",   # MBBank
    "VPB": "970432",   # VPBank
    "ACB": "970416",   # ACB
    "BIDV": "970418",  # BIDV
    "VTB": "970415",   # VietinBank
}

def _crc16_ccitt(data: str) -> str:
    """
    Computes standard CRC16-CCITT (polynomial 0x1021, init 0xFFFF) for EMVCo Tag 63.
    """
    crc = 0xFFFF
    for byte in data.encode('ascii'):
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"

def _tlv(tag: str, value: str) -> str:
    """Encodes a Tag-Length-Value (TLV) field according to EMVCo."""
    length = f"{len(value):02d}"
    return f"{tag}{length}{value}"

def generate_vietqr_emvco(
    bank_code_or_bin: str,
    account_number: str,
    amount: Optional[int] = None,
    memo: Optional[str] = None
) -> str:
    """
    Generates an official EMVCo QR string for Vietnamese interbank transfers.
    
    :param bank_code_or_bin: Bank acronym (e.g. 'TPB', 'VCB') or 6-digit BIN ('970423').
    :param account_number: Beneficiary account number.
    :param amount: Amount in VND (optional).
    :param memo: Transfer memo/purpose (optional, max 25 chars, alphanumeric recommended).
    :return: Formatted EMVCo string.
    """
    bin_code = BANK_BINS.get(bank_code_or_bin.upper(), bank_code_or_bin)
    if not (bin_code.isdigit() and len(bin_code) == 6):
        raise ValueError(f"Invalid Bank BIN or Code: {bank_code_or_bin}. Must be 6 digits or known acronym.")

    # 1. Payload Format Indicator (Tag 00)
    payload = _tlv("00", "01")

    # 2. Point of Initiation Method (Tag 01): 11 = Static, 12 = Dynamic
    point_of_init = "12" if amount else "11"
    payload += _tlv("01", point_of_init)

    # 3. Merchant Account Information (Tag 38 - NAPAS sub-tags)
    # Sub-tag 00: GUID (A000000727)
    # Sub-tag 01: Beneficiary Information (Sub-sub-tag 00: BIN, Sub-sub-tag 01: Account Number)
    # Sub-tag 02: Service Code (QRIBFTTA for transfer to account)
    napas_guid = _tlv("00", "A000000727")
    beneficiary_info = _tlv("00", bin_code) + _tlv("01", account_number)
    napas_beneficiary = _tlv("01", beneficiary_info)
    service_code = _tlv("02", "QRIBFTTA")
    merchant_info_38 = _tlv("38", napas_guid + napas_beneficiary + service_code)
    payload += merchant_info_38

    # 4. Transaction Currency (Tag 53): 704 = VND
    payload += _tlv("53", "704")

    # 5. Transaction Amount (Tag 54 - optional)
    if amount and amount > 0:
        payload += _tlv("54", str(int(amount)))

    # 6. Country Code (Tag 58): VN
    payload += _tlv("58", "VN")

    # 7. Additional Data Field (Tag 62 - optional memo)
    if memo:
        clean_memo = memo[:25]
        sub_memo = _tlv("08", clean_memo)
        payload += _tlv("62", sub_memo)

    # 8. CRC Checksum (Tag 63)
    crc_payload_prefix = payload + "6304"
    crc_value = _crc16_ccitt(crc_payload_prefix)
    return crc_payload_prefix + crc_value

if __name__ == '__main__':
    # Test on user's TPBank account
    qr_str = generate_vietqr_emvco(
        bank_code_or_bin="TPB",
        account_number="20058999999",
        amount=350000,
        memo="LEADSB2B"
    )
    print("EMVCo VietQR String:")
    print(qr_str)
