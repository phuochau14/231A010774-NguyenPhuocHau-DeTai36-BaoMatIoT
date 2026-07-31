import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

plt.rcParams["font.family"] = "DejaVu Sans"

def box(ax, x, y, w, h, text, fc="#e8f0fe", ec="#3b5bdb", fontsize=10, weight="bold", textcolor="#1a1a2e"):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                        fc=fc, ec=ec, lw=1.8)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fontsize, fontweight=weight, color=textcolor, wrap=True)

def arrow(ax, x1, y1, x2, y2, color="#495057", style="-|>", lw=1.8, ls="-"):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=15,
                         color=color, lw=lw, linestyle=ls)
    ax.add_patch(a)

# =====================================================================
# HINH 2.1 - KIEN TRUC HE THONG + RANH GIOI TIN CAY
# =====================================================================
fig, ax = plt.subplots(figsize=(10, 5.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis("off")
ax.set_title("Hình 2.1 — Kiến trúc hệ thống và ranh giới tin cậy (trust boundary)",
              fontsize=12, fontweight="bold", pad=14)

# Trust boundary 1: thiết bị (vùng vật lý không kiểm soát được)
tb1 = mpatches.FancyBboxPatch((0.3, 3.6), 2.6, 1.8, boxstyle="round,pad=0.05",
                               fc="none", ec="#e03131", lw=2, linestyle="--")
ax.add_patch(tb1)
ax.text(1.6, 5.55, "Vùng KHÔNG tin cậy\n(thiết bị vật lý, dễ bị truy cập)",
        ha="center", fontsize=8.5, color="#e03131", style="italic")

box(ax, 0.6, 4.0, 2.0, 1.0, "Sensor Node\n(cảm biến +\nvi điều khiển)")

# Trust boundary 2: mang trung gian
tb2 = mpatches.FancyBboxPatch((3.4, 3.6), 3.2, 1.8, boxstyle="round,pad=0.05",
                               fc="none", ec="#f08c00", lw=2, linestyle="--")
ax.add_patch(tb2)
ax.text(5.0, 5.55, "Vùng tin cậy TRUNG BÌNH\n(mạng, gateway/broker trung gian)",
        ha="center", fontsize=8.5, color="#f08c00", style="italic")

box(ax, 3.7, 4.0, 2.6, 1.0, "Gateway / MQTT Broker", fc="#fff3bf", ec="#f08c00")

# Trust boundary 3: cloud
tb3 = mpatches.FancyBboxPatch((7.0, 3.6), 2.7, 1.8, boxstyle="round,pad=0.05",
                               fc="none", ec="#2f9e44", lw=2, linestyle="--")
ax.add_patch(tb3)
ax.text(8.35, 5.55, "Vùng tin cậy CAO\n(cloud server có kiểm soát)",
        ha="center", fontsize=8.5, color="#2f9e44", style="italic")

box(ax, 7.3, 4.0, 2.1, 1.0, "Cloud Server\n(xác thực & lưu trữ)", fc="#d3f9d8", ec="#2f9e44")

arrow(ax, 2.6, 4.5, 3.65, 4.5)
arrow(ax, 6.3, 4.5, 7.25, 4.5)

ax.text(3.1, 4.7, "①", fontsize=11, ha="center", fontweight="bold")
ax.text(6.75, 4.7, "②", fontsize=11, ha="center", fontweight="bold")

# Chu thich lop bao ve tai moi ranh gioi
box(ax, 0.6, 1.4, 2.0, 1.3,
    "① Kênh (1):\nHMAC/AES-GCM\nở payload (nhẹ)",
    fc="#f8f9fa", ec="#868e96", fontsize=8.7, weight="normal", textcolor="#212529")
box(ax, 3.5, 1.4, 3.0, 1.3,
    "② Kênh (2):\nTLS (gateway ↔ cloud,\ntài nguyên đủ mạnh)",
    fc="#f8f9fa", ec="#868e96", fontsize=8.7, weight="normal", textcolor="#212529")
box(ax, 7.0, 1.4, 2.7, 1.3,
    "OTA/Firmware:\nChữ ký số\n(non-repudiation)",
    fc="#f8f9fa", ec="#868e96", fontsize=8.7, weight="normal", textcolor="#212529")

arrow(ax, 1.6, 3.6, 1.6, 2.7, ls=":", color="#adb5bd")
arrow(ax, 5.0, 3.6, 5.0, 2.7, ls=":", color="#adb5bd")
arrow(ax, 8.35, 3.6, 8.35, 2.7, ls=":", color="#adb5bd")

plt.tight_layout()
plt.savefig("hinh_2_1_kien_truc_he_thong.png", dpi=200, bbox_inches="tight")
plt.close()

# =====================================================================
# HINH 2.2 - VONG DOI KHOA (KEY LIFECYCLE)
# =====================================================================
fig, ax = plt.subplots(figsize=(10, 3.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 3)
ax.axis("off")
ax.set_title("Hình 2.2 — Vòng đời khóa mật mã (key lifecycle) trong IoT",
              fontsize=12, fontweight="bold", pad=14)

stages = [
    ("1. Sinh khóa\n(Generate)", "#e8f0fe", "#3b5bdb"),
    ("2. Cấp phát\n(Provision)\nlúc sản xuất", "#d3f9d8", "#2f9e44"),
    ("3. Sử dụng\n(Use)\nmã hóa/ký/HMAC", "#fff3bf", "#f08c00"),
    ("4. Xoay vòng\n(Rotate)\nđịnh kỳ", "#ffe8cc", "#e8590c"),
    ("5. Thu hồi/Hủy\n(Revoke/\nDestroy)", "#ffe3e3", "#e03131"),
]
w = 1.7
gap = 0.35
x = 0.3
for label, fc, ec in stages:
    box(ax, x, 1.0, w, 1.2, label, fc=fc, ec=ec, fontsize=9)
    x_next = x + w + gap
    if label != stages[-1][0]:
        arrow(ax, x + w, 1.6, x_next, 1.6)
    x = x_next

ax.text(5, 0.3,
        "Mỗi thiết bị có khóa/định danh RIÊNG — key bị lộ ở bước nào cũng có thể thu hồi (bước 5)\n"
        "mà không ảnh hưởng các thiết bị khác trong hệ thống.",
        ha="center", fontsize=8.7, style="italic", color="#495057")

plt.tight_layout()
plt.savefig("hinh_2_2_vong_doi_khoa.png", dpi=200, bbox_inches="tight")
plt.close()

# =====================================================================
# HINH 3.1 - MO HINH DE XUAT: AP DUNG MAT MA O DAU
# =====================================================================
fig, ax = plt.subplots(figsize=(10, 6.2))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.5)
ax.axis("off")
ax.set_title("Hình 3.1 — Mô hình đề xuất: áp dụng kỹ thuật mật mã theo từng giai đoạn",
              fontsize=12, fontweight="bold", pad=14)

box(ax, 0.3, 4.9, 2.0, 0.9, "Sensor Node", fc="#e8f0fe", ec="#3b5bdb", fontsize=9.5)
box(ax, 4.0, 4.9, 2.2, 0.9, "Gateway/Broker", fc="#e8f0fe", ec="#3b5bdb", fontsize=9.5)
box(ax, 7.7, 4.9, 2.0, 0.9, "Cloud Server", fc="#e8f0fe", ec="#3b5bdb", fontsize=9.5)
arrow(ax, 2.3, 5.35, 3.95, 5.35)
arrow(ax, 6.2, 5.35, 7.65, 5.35)

box(ax, 0.2, 3.2, 2.9, 1.3,
    "① HMAC-SHA256\ntại payload\n(toàn vẹn + xác thực\nnguồn, nhẹ)",
    fc="#d3f9d8", ec="#2f9e44", fontsize=8.7)
box(ax, 3.55, 3.2, 3.0, 1.3,
    "② AES-256-GCM\n(mã hóa có xác thực:\nbí mật + toàn vẹn)",
    fc="#fff3bf", ec="#f08c00", fontsize=8.7)
box(ax, 6.9, 3.2, 2.9, 1.3,
    "③ TLS 1.2/1.3\ncho kênh gateway↔cloud\n(bảo vệ toàn kênh)",
    fc="#ffe8cc", ec="#e8590c", fontsize=8.7)

box(ax, 3.55, 1.2, 3.0, 1.3,
    "④ Chữ ký số RSA-PSS/\nECDSA cho firmware\n& OTA update\n(non-repudiation)",
    fc="#ffe3e3", ec="#e03131", fontsize=8.7)

arrow(ax, 1.65, 4.9, 1.65, 4.5, ls=":", color="#adb5bd")
arrow(ax, 5.1, 4.9, 5.1, 4.5, ls=":", color="#adb5bd")
arrow(ax, 8.7, 4.9, 8.7, 4.5, ls=":", color="#adb5bd")
arrow(ax, 5.1, 3.2, 5.1, 2.5, ls=":", color="#adb5bd")

ax.text(5, 0.35,
        "3 mục tiêu bảo mật đạt được: Bí mật (②) — Toàn vẹn (①②③④) — Xác thực/Không thể chối bỏ (①④)",
        ha="center", fontsize=9, fontweight="bold", color="#1a1a2e")

plt.tight_layout()
plt.savefig("hinh_3_1_mo_hinh_de_xuat.png", dpi=200, bbox_inches="tight")
plt.close()

print("Da tao xong 3 hinh: hinh_2_1, hinh_2_2, hinh_3_1")
