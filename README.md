# Đề tài 36 - Vai trò của mật mã trong bảo mật IoT

Học phần: Bảo mật IoT (INT4410) - HK03 2025-2026
Sinh viên: Nguyễn Phước Hậu - MSSV 231A010774
GVHD: Hồ Nhựt Minh
Trường Đại học Văn Hiến - Khoa Công nghệ Thông tin

## Giới thiệu đề tài

Thiết bị IoT thường tài nguyên yếu (CPU, RAM thấp) nhưng vẫn phải truyền dữ liệu qua mạng không an toàn, nên rất dễ bị nghe lén, sửa dữ liệu hoặc giả mạo nếu không dùng mật mã đúng cách. Đề tài này tìm hiểu vai trò của 4 kỹ thuật mật mã cốt lõi - hash, HMAC, mã hóa đối xứng (AES-GCM), chữ ký số (RSA) - trong việc bảo vệ 3 yếu tố: tính bí mật, tính toàn vẹn và tính xác thực của dữ liệu cảm biến IoT. Đề tài mô phỏng bằng Python trên dữ liệu cảm biến giả lập, không triển khai trên thiết bị nhúng thật.

## Mục tiêu

- Giải thích đúng vai trò từng kỹ thuật mật mã (hash, HMAC, mã hóa, chữ ký số) trong IoT.
- Xây dựng mô hình áp dụng mật mã vào luồng dữ liệu cảm biến cụ thể.
- Viết chương trình minh họa, phát hiện được dữ liệu bị giả mạo qua nhiều kịch bản thử nghiệm.
- Phân tích rủi ro bảo mật và đề xuất biện pháp khắc phục, đối chiếu chuẩn OWASP ISVS.

## Cấu trúc thư mục

```
├── README.md
├── src/
│   ├── crypto_demo.py        # Hash, HMAC, AES-GCM, chữ ký số + mô phỏng tấn công
│   └── draw_diagrams.py      # Vẽ 3 sơ đồ minh họa
├── data/
│   └── sensor_data.json      # Dữ liệu cảm biến giả lập
├── results/
│   ├── crypto_demo_log.txt   # Log chạy chương trình
│   ├── hinh_2_1_kien_truc_he_thong.png
│   ├── hinh_2_2_vong_doi_khoa.png
│   └── hinh_3_1_mo_hinh_de_xuat.png
├── report/
│   ├── 231A010774_NguyenPhuocHau_DeTai36_BaoCao.docx
│   ├── 231A010774_NguyenPhuocHau_DeTai36_BaoCao.pdf
└── configs/                  # Chưa phát sinh cấu hình cho đề tài này
```

## Hướng dẫn chạy chương trình

**Bước 1 - Cài Python 3 và thư viện cần thiết:**
```bash
pip install cryptography
```

**Bước 2 - Clone repo và chạy script:**
```bash
git clone <link-repo-này>
cd <ten-repo>/src
python3 crypto_demo.py
```

**Bước 3 - Đọc kết quả in ra màn hình**, gồm 3 phần:
- Phần A: tính hash, HMAC, chữ ký số, mã hóa AES-GCM trên dữ liệu sensor gốc.
- Phần B: sửa 1 trường trong dữ liệu (mô phỏng tấn công), tính lại hash/HMAC/chữ ký để so sánh - kỳ vọng thấy hash đổi hoàn toàn và các bước xác minh trả về `False`.
- Phần C: kẻ tấn công không có khóa thật cố tạo HMAC giả - kỳ vọng server vẫn phát hiện ra (`False`).

**Bước 4 (tùy chọn) - Lưu lại log:**
```bash
python3 crypto_demo.py > ../results/crypto_demo_log.txt
```

## Kết quả

8/8 kịch bản thử nghiệm (KB-01 đến KB-08) cho kết quả đúng như thiết kế: phát hiện được dữ liệu bị sửa, từ chối HMAC/chữ ký giả mạo, giải mã AES-GCM round-trip thành công. Chi tiết xem Chương 4 báo cáo và `results/crypto_demo_log.txt`.

## Tài liệu tham khảo

- Mbed TLS - https://github.com/Mbed-TLS/mbedtls
- TinyCrypt - https://github.com/intel/tinycrypt
- OWASP IoT Security Verification Standard (ISVS) - https://github.com/OWASP/IoT-Security-Verification-Standard-ISVS
- NIST FIPS 198-1 (HMAC) - https://csrc.nist.gov/pubs/fips/198-1/final
- NIST SP 800-38D (AES-GCM) - https://www.nist.gov/publications/recommendation-block-cipher-modes-operation-galoiscounter-mode-gcm-and-gmac
- RFC 8446 (TLS 1.3) - https://www.rfc-editor.org/rfc/rfc8446

Danh mục đầy đủ xem trong báo cáo, thư mục `report/`.
