"""
Demo: Vai trò của mật mã trong bảo mật IoT
Đề tài 36 - Minh họa 4 kỹ thuật: Hash, HMAC, Encryption (AES-GCM), Digital Signature (RSA)

Yêu cầu: pip install cryptography
"""

import json
import hashlib
import hmac
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

SEPARATOR = "=" * 70


def load_sensor_data(path="sensor_data.json"):
    """Đọc dữ liệu sensor và chuẩn hóa thành chuỗi bytes cố định
    (sort_keys=True đảm bảo cùng dữ liệu -> luôn cùng 1 chuỗi bytes,
    tránh việc thứ tự key khác nhau làm hash khác nhau một cách vô nghĩa)."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    canonical_bytes = json.dumps(data, sort_keys=True).encode("utf-8")
    return data, canonical_bytes


# ---------------------------------------------------------------------------
# 1. HASH (SHA-256) - đảm bảo TÍNH TOÀN VẸN (Integrity)
#    Ai cũng tính được hash, không cần khóa bí mật -> không chống giả mạo
#    nếu kẻ tấn công có thể sửa cả dữ liệu lẫn hash gửi kèm.
# ---------------------------------------------------------------------------
def compute_hash(data_bytes: bytes) -> str:
    return hashlib.sha256(data_bytes).hexdigest()


# ---------------------------------------------------------------------------
# 2. HMAC-SHA256 - đảm bảo TÍNH TOÀN VẸN + XÁC THỰC NGUỒN GỐC (Authenticity)
#    Cần khóa bí mật dùng chung (shared secret) giữa sensor và server.
#    Kẻ tấn công không có khóa -> không thể tạo HMAC hợp lệ dù biết thuật toán.
# ---------------------------------------------------------------------------
def compute_hmac(data_bytes: bytes, key: bytes) -> str:
    return hmac.new(key, data_bytes, hashlib.sha256).hexdigest()


def verify_hmac(data_bytes: bytes, key: bytes, received_mac: str) -> bool:
    expected = compute_hmac(data_bytes, key)
    # dùng compare_digest để chống timing attack khi so sánh
    return hmac.compare_digest(expected, received_mac)


# ---------------------------------------------------------------------------
# 3. AES-GCM (Authenticated Encryption) - đảm bảo TÍNH BÍ MẬT + TOÀN VẸN
#    GCM = mã hóa đối xứng (che giấu nội dung) + tag xác thực tích hợp sẵn
#    (không cần ghép thêm HMAC riêng). Phù hợp IoT vì AES có hỗ trợ phần cứng
#    (AES-NI / ARM CryptoCell) trên nhiều vi điều khiển.
# ---------------------------------------------------------------------------
def aes_gcm_encrypt(data_bytes: bytes, key: bytes):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)  # nonce PHẢI unique cho mỗi lần mã hóa với cùng 1 key
    ciphertext = aesgcm.encrypt(nonce, data_bytes, None)
    return nonce, ciphertext


def aes_gcm_decrypt(nonce: bytes, ciphertext: bytes, key: bytes):
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)  # tự raise lỗi nếu tag sai


# ---------------------------------------------------------------------------
# 4. DIGITAL SIGNATURE (RSA-PSS) - đảm bảo TOÀN VẸN + XÁC THỰC + KHÔNG THỂ
#    CHỐI BỎ (Non-repudiation). Dùng khóa BẤT ĐỐI XỨNG: server/hãng sản xuất
#    giữ private key để ký (vd: ký firmware update), thiết bị chỉ giữ public
#    key để xác minh. Thường dùng cho secure boot / OTA update, KHÔNG dùng
#    cho từng gói tin sensor vì RSA chậm và tốn tài nguyên hơn HMAC nhiều.
# ---------------------------------------------------------------------------
def rsa_generate_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


def rsa_sign(data_bytes: bytes, private_key) -> bytes:
    return private_key.sign(
        data_bytes,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )


def rsa_verify(data_bytes: bytes, signature: bytes, public_key) -> bool:
    try:
        public_key.verify(
            signature,
            data_bytes,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False


def run_demo():
    key_hmac = hashlib.sha256(b"shared-secret-provisioned-at-manufacturing-time").digest()  # 32 bytes
    key_aes = os.urandom(32)  # AES-256

    print(SEPARATOR)
    print("BƯỚC A: DỮ LIỆU GỐC")
    print(SEPARATOR)
    data, data_bytes = load_sensor_data()
    print(json.dumps(data, indent=2, ensure_ascii=False))

    h1 = compute_hash(data_bytes)
    m1 = compute_hmac(data_bytes, key_hmac)
    print(f"\nSHA-256 hash : {h1}")
    print(f"HMAC-SHA256  : {m1}")

    priv, pub = rsa_generate_keypair()
    sig1 = rsa_sign(data_bytes, priv)
    print(f"RSA signature (rút gọn): {sig1.hex()[:64]}...")
    print(f"Xác minh chữ ký với dữ liệu gốc: {rsa_verify(data_bytes, sig1, pub)}")

    nonce, ct = aes_gcm_encrypt(data_bytes, key_aes)
    print(f"\nAES-GCM ciphertext (rút gọn): {ct.hex()[:64]}...")
    pt_back = aes_gcm_decrypt(nonce, ct, key_aes)
    print(f"Giải mã lại khớp dữ liệu gốc: {pt_back == data_bytes}")

    print("\n" + SEPARATOR)
    print("BƯỚC B: TẤN CÔNG GIẢ LẬP - SỬA 1 KÝ TỰ TRONG DỮ LIỆU")
    print("(vd: kẻ tấn công chỉnh temperature_c từ 27.4 -> 99.4 để đánh lừa hệ thống)")
    print(SEPARATOR)
    tampered_data = json.loads(data_bytes.decode())
    tampered_data["readings"]["temperature_c"] = 99.4  # chỉ sửa đúng 1 giá trị
    tampered_bytes = json.dumps(tampered_data, sort_keys=True).encode("utf-8")
    print(json.dumps(tampered_data, indent=2, ensure_ascii=False))

    h2 = compute_hash(tampered_bytes)
    m2 = compute_hmac(tampered_bytes, key_hmac)
    print(f"\nSHA-256 hash (sau khi sửa) : {h2}")
    print(f"HMAC-SHA256  (sau khi sửa) : {m2}")

    print(f"\n>> Hash gốc  : {h1}")
    print(f">> Hash mới  : {h2}")
    print(f">> Hash có thay đổi hoàn toàn không? {'CÓ (avalanche effect)' if h1 != h2 else 'KHÔNG'}")

    print(f"\n>> Server nhận dữ liệu ĐÃ BỊ SỬA nhưng MAC cũ (m1) đi kèm ->")
    print(f">> Kết quả xác minh HMAC: {verify_hmac(tampered_bytes, key_hmac, m1)}  (phải là False)")

    print(f"\n>> Xác minh chữ ký RSA (sig1 ký trên dữ liệu gốc) với dữ liệu ĐÃ SỬA:")
    print(f">> Kết quả: {rsa_verify(tampered_bytes, sig1, pub)}  (phải là False)")

    print("\n" + SEPARATOR)
    print("BƯỚC C: KẺ TẤN CÔNG KHÔNG CÓ KHÓA -> KHÔNG THỂ GIẢ MẠO HMAC HỢP LỆ")
    print(SEPARATOR)
    attacker_fake_key = os.urandom(32)
    fake_mac = compute_hmac(tampered_bytes, attacker_fake_key)
    print(f"Attacker tự tạo HMAC với khóa ĐOÁN MÒ: {fake_mac}")
    print(f"Server dùng khóa THẬT để xác minh: {verify_hmac(tampered_bytes, key_hmac, fake_mac)} (phải là False)")
    print("=> Chứng minh: chỉ hash không đủ (ai cũng tính được), phải cần HMAC/chữ ký (cần khóa bí mật).")


if __name__ == "__main__":
    run_demo()
