"""
Modul Komponen & Template HTML untuk Diabetes Diagnostic Studio.
Menyimpan seluruh fungsi pembangun UI & metadata klinis.
"""

def get_diagnosis_database():
    """Katalog informasi klinis dan rekomendasi untuk 13 subtipe diabetes."""
    return {
        "Type 1 Diabetes": {
            "badge": "#dc2626", "bg": "rgba(254, 242, 242, 0.9)",
            "urgency": "Tinggi",
            "desc": "Kondisi autoimun di mana destruksi sel beta pankreas menyebabkan defisiensi insulin absolut.",
            "rec": "Inisiasi terapi insulin eksogen teratur dan rujukan ke dokter spesialis endokrinologi."
        },
        "Type 2 Diabetes": {
            "badge": "#059669", "bg": "rgba(236, 253, 245, 0.95)",
            "urgency": "Sedang",
            "desc": "Gangguan metabolik akibat resistensi insulin perifer disertai defisiensi sekresi insulin relatif.",
            "rec": "Intervensi diet rendah indeks glikemik, aktivitas fisik terstruktur, dan terapi obat hipoglikemik oral."
        },
        "Gestational Diabetes": {
            "badge": "#0284c7", "bg": "rgba(240, 249, 255, 0.95)",
            "urgency": "Tinggi",
            "desc": "Intoleransi glukosa dengan derajat bervariasi yang pertama kali teridentifikasi saat masa kehamilan.",
            "rec": "Monitoring glukosa darah berkala maternal-fetal dan konsultasi ke dokter spesialis obstetri (Sp.OG)."
        },
        "Prediabetic": {
            "badge": "#16a34a", "bg": "rgba(240, 253, 244, 0.95)",
            "urgency": "Pencegahan",
            "desc": "Kadar glukosa darah di atas batas normal namun belum memenuhi kriteria diagnostik diabetes.",
            "rec": "Modifikasi gaya hidup intensif dan penurunan berat badan 5-7% untuk mencegah progresi ke Tipe 2."
        },
        "LADA": {
            "badge": "#0d9488", "bg": "rgba(240, 253, 250, 0.95)",
            "urgency": "Sedang-Tinggi",
            "desc": "Latent Autoimmune Diabetes in Adults; diabetes autoimun dengan progresi onset lambat pada usia dewasa.",
            "rec": "Pemeriksaan antibodi anti-GAD dan pemantauan cadangan fungsi sel beta pankreas secara periodik."
        },
        "MODY": {
            "badge": "#0284c7", "bg": "rgba(240, 249, 255, 0.95)",
            "urgency": "Sedang",
            "desc": "Maturity-Onset Diabetes of the Young; kelompok heterogen akibat mutasi monogenik dominan autosomal.",
            "rec": "Skrining silsilah genetik keluarga dan pertimbangan respons terapi golongan sulfonilurea oral."
        },
        "Steroid-Induced Diabetes": {
            "badge": "#0369a1", "bg": "rgba(240, 249, 255, 0.95)",
            "urgency": "Sedang",
            "desc": "Hiperglikemia sekunder akibat efek samping pemberian terapi obat golongan glukokortikoid/kortikosteroid.",
            "rec": "Evaluasi dan penyesuaian dosis steroid bersama dokter perujuk serta kontrol glukosa aktif."
        },
        "Cystic Fibrosis-Related Diabetes (CFRD)": {
            "badge": "#059669", "bg": "rgba(236, 253, 245, 0.95)",
            "urgency": "Tinggi",
            "desc": "Komplikasi komorbiditas metabolik spesifik pada pasien yang terdiagnosis Cystic Fibrosis.",
            "rec": "Kolaborasi tim multidisiplin pulmonologi-nutrisi dengan perencanaan diet tinggi kalori terpadu."
        },
        "Type 3c Diabetes (Pancreatogenic Diabetes)": {
            "badge": "#0d9488", "bg": "rgba(240, 253, 250, 0.95)",
            "urgency": "Sedang",
            "desc": "Diabetes sekunder akibat kerusakan eksokrin dan endokrin parenkim pankreas (misal pasca pankreatitis).",
            "rec": "Suplementasi enzim pencernaan dan evaluasi berkala terhadap malabsorpsi mikronutrien."
        },
        "Wolcott-Rallison Syndrome": {
            "badge": "#b91c1c", "bg": "rgba(254, 242, 242, 0.9)",
            "urgency": "Kritis",
            "desc": "Sindrom genetik resesif langka ditandai diabetes onset neonatal dini dan displasia epifisis.",
            "rec": "Rujukan ke pusat rujukan genetika medis dan pemantauan fungsi hati/hepar berkala."
        },
        "Wolfram Syndrome": {
            "badge": "#0284c7", "bg": "rgba(240, 249, 255, 0.95)",
            "urgency": "Tinggi",
            "desc": "Gangguan neurodegeneratif multisistemik progresif (kompleks sindrom DIDMOAD).",
            "rec": "Evaluasi komprehensif oftalmologi, audiometri pendengaran, dan neurologi terpadu."
        },
        "Neonatal Diabetes Mellitus (NDM)": {
            "badge": "#0ea5e9", "bg": "rgba(240, 249, 255, 0.95)",
            "urgency": "Tinggi",
            "desc": "Diabetes monogenik langka yang bermanifestasi klinis pada bayi di bawah usia 6 bulan.",
            "rec": "Pemeriksaan mutasi gen KCNJ11/ABCC8 untuk eksplorasi potensi transisi ke obat sulfonilurea oral."
        },
        "Secondary Diabetes": {
            "badge": "#0f766e", "bg": "rgba(240, 253, 250, 0.95)",
            "urgency": "Sedang",
            "desc": "Hiperglikemia yang timbul sebagai manifestasi sekunder dari penyakit endokrinopati atau kondisi lain.",
            "rec": "Identifikasi dan terapi penyakit etiologi primer pemicu disregulasi metabolik."
        }
    }


def get_top_header_html() -> str:
    """Mengembalikan HTML untuk Top Header Bar."""
    return """
    <div class="app-header">
        <div class="app-title-box">
            <div class="app-title">Diabetes Diagnostic Studio</div>
            <div class="app-subtitle">Sistem Klasifikasi 13 Subtipe Gangguan Metabolik Berbasis Machine Learning</div>
        </div>
        <div class="header-tags">
            <span class="app-badge"><span class="pulse-dot"></span> Evaluasi Real-Time Aktif</span>
        </div>
    </div>
    """


def get_sidebar_brand_html() -> str:
    """Mengembalikan HTML untuk Header Sidebar."""
    return """
    <div class="sidebar-brand-box">
        <div class="sidebar-title">Diabetes Diagnostic</div>
        <div class="sidebar-subtitle">Sistem Pakar 13 Subtipe Diabetes</div>
    </div>
    """


def get_sidebar_card_html() -> str:
    """Mengembalikan HTML untuk kartu informasi sidebar."""
    return """
    <div class="sidebar-card">
        <span class="sidebar-badge">Real-Time Active</span>
        <div style="font-weight:600; color:#ffffff; font-size:11px;">Evaluasi 33 Parameter</div>
        <div style="color:#93c5fd; font-size:10px; margin-top:2px;">
            Semua nilai tersimpan otomatis. Hasil diagnosa dihitung secara real-time pada panel kanan.
        </div>
    </div>
    """


def get_card_header_html(title: str, status: str = "Data Tersinkronisasi") -> str:
    """Mengembalikan HTML untuk header kartu."""
    return f"""
    <div class="card-header-bar">
        <span class="card-header-title">{title}</span>
        <span class="card-header-status">{status}</span>
    </div>
    """


def get_diagnosis_panel_html(pred_label: str, confidence: float, top_3_results: list) -> str:
    """Mengembalikan HTML lengkap untuk panel hasil diagnosa klinis."""
    db = get_diagnosis_database()
    meta = db.get(pred_label, {
        "badge": "#059669", "bg": "rgba(236, 253, 245, 0.95)",
        "urgency": "Rutin",
        "desc": "Pola klinis teridentifikasi berdasarkan data parameter pasien yang dimasukkan.",
        "rec": "Lakukan verifikasi klinis dan konsultasi medis profesional lebih lanjut."
    })

    # Susun diferensial diagnosa
    diff_items = []
    for diag_name, prob in top_3_results:
        pct = min(max(prob, 0.0), 100.0)
        diff_items.append(
            f'<div class="diff-row">'
            f'<div class="diff-bar" style="width:{pct:.1f}%;"></div>'
            f'<span class="diff-name">{diag_name}</span>'
            f'<span class="diff-val">{prob:.1f}%</span>'
            f'</div>'
        )
    diff_html_str = "".join(diff_items)

    return f"""
    <div class="card-header-bar">
        <span class="card-header-title">Hasil Diagnosa Klinis</span>
        <span class="card-header-status">● Evaluasi Medis Real-Time</span>
    </div>
    <div class="diag-banner" style="background:{meta["bg"]}; border:1px solid {meta["badge"]}40; border-left:4px solid {meta["badge"]};">
        <div>
            <div style="font-size:10px; font-weight:700; color:{meta["badge"]}; text-transform:uppercase; letter-spacing:0.5px;">Subtipe Teridentifikasi</div>
            <div class="diag-name">{pred_label}</div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:10px; font-weight:700; color:{meta["badge"]}; text-transform:uppercase;">Skor Kepastian</div>
            <div style="font-size:21px; font-weight:800; color:{meta["badge"]};">{confidence:.1f}%</div>
        </div>
    </div>
    <div class="diag-desc">{meta["desc"]}</div>
    <div class="metric-grid">
        <div class="metric-pill">
            <div class="metric-pill-label">Subtipe Terdeteksi</div>
            <div class="metric-pill-value" style="color:{meta["badge"]};">{pred_label}</div>
        </div>
        <div class="metric-pill">
            <div class="metric-pill-label">Skor Kepastian</div>
            <div class="metric-pill-value">{confidence:.1f}%</div>
        </div>
        <div class="metric-pill">
            <div class="metric-pill-label">Tingkat Urgensi</div>
            <div class="metric-pill-value">{meta["urgency"]}</div>
        </div>
    </div>
    <div class="diff-header">
        <span>Diferensial Diagnosa Banding</span>
        <span style="font-size:9.5px; color:#0284c7;">Probabilitas</span>
    </div>
    {diff_html_str}
    <div class="rec-callout" style="background:{meta["bg"]}; border:1px solid {meta["badge"]}35;">
        <div class="rec-title" style="color:{meta["badge"]};">Rekomendasi Tindakan Klinis:</div>
        <div style="color:#334155;">{meta["rec"]}</div>
    </div>
    <div style="margin-top:8px; padding-top:6px; border-top:1px solid rgba(224, 242, 254, 0.9); font-size:9.5px; color:#94a3b8; text-align:center;">
        Sistem Pakar Machine Learning • Evaluasi Akademis & Riset Medis.
    </div>
    """
