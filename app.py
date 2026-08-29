"""
Diabetes Diagnostic Studio
Sistem Pakar Klasifikasi Diabetes (13 Subtipe) Berbasis Machine Learning.
Arsitektur: Modular Clean Code (CSS & HTML Templates Terpisah).
"""

import os
import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Import template HTML dan metadata dari modul komponen
from components.ui_templates import (
    get_top_header_html,
    get_sidebar_brand_html,
    get_sidebar_card_html,
    get_card_header_html,
    get_diagnosis_panel_html
)

# ==============================================================================
# 0. DEFINISI NILAI DEFAULT RESMI SESUAI KELAS ENCODER
# ==============================================================================
DEFAULT_INPUTS = {
    # 13 Parameter Laboratorium & Vitalis
    'Blood Glucose Levels': 95.0,
    'Insulin Levels': 15.0,
    'BMI': 24.5,
    'Waist Circumference': 35.0,
    'Blood Pressure': 120.0,
    'Cholesterol Levels': 180.0,
    'Age': 45.0,
    'Pancreatic Health': 85.0,
    'Pulmonary Function': 90.0,
    'Neurological Assessments': 1.8,
    'Digestive Enzyme Levels': 80.0,
    'Weight Gain During Pregnancy': 0.0,
    'Birth Weight': 3100.0,
    
    # 10 Riwayat Klinis & Genetik
    'Genetic Markers': 'Negative',
    'Genetic Testing': 'Negative',
    'Autoantibodies': 'Negative',
    'Family History': 'No',
    'History of PCOS': 'No',
    'Previous Gestational Diabetes': 'No',
    'Pregnancy History': 'Normal',
    'Cystic Fibrosis Diagnosis': 'No',
    'Steroid Use History': 'No',
    'Early Onset Symptoms': 'No',
    
    # 10 Gaya Hidup & Penunjang
    'Physical Activity': 'Moderate',
    'Dietary Habits': 'Healthy',
    'Smoking Status': 'Non-Smoker',
    'Alcohol Consumption': 'Low',
    'Socioeconomic Factors': 'Medium',
    'Ethnicity': 'Low Risk',
    'Glucose Tolerance Test': 'Normal',
    'Liver Function Tests': 'Normal',
    'Environmental Factors': 'Absent',
    'Urine Test': 'Normal'
}


# ==============================================================================
# 1. KONFIGURASI HALAMAN & LOAD EXTERNAL CSS
# ==============================================================================
def setup_page_configuration():
    """Mengatur konfigurasi halaman dan memuat file CSS eksternal dari assets/style.css."""
    st.set_page_config(
        page_title="Diabetes Diagnostic Studio",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    css_file_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    if os.path.exists(css_file_path):
        with open(css_file_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ==============================================================================
# 2. LOAD MODEL & ARTEFAK PIPELINE
# ==============================================================================
@st.cache_resource
def load_ml_artifacts():
    """Memuat model Machine Learning dan seluruh artefak preprocessing."""
    try:
        model = joblib.load('model.pkl')
        scaler = joblib.load('scaler.pkl')
        le_target = joblib.load('le_target.pkl')
        encoders_dict = joblib.load('encoders_dict.pkl')
        oe = joblib.load('ordinal_encoder.pkl')
        feature_columns = joblib.load('feature_columns.pkl')
        return {
            'model': model,
            'scaler': scaler,
            'le_target': le_target,
            'encoders_dict': encoders_dict,
            'oe': oe,
            'feature_columns': feature_columns
        }
    except Exception as err:
        st.error(f"Gagal memuat file artefak model (.pkl): {err}")
        st.stop()


# ==============================================================================
# 3. INFERENSI & PREPROCESSING PIPELINE
# ==============================================================================
def predict_diabetes_case(user_inputs: dict, artifacts: dict):
    """Menjalankan preprocessing pipeline dan prediksi model multiclass."""
    model = artifacts['model']
    scaler = artifacts['scaler']
    le_target = artifacts['le_target']
    encoders_dict = artifacts['encoders_dict']
    oe = artifacts['oe']
    feature_columns = artifacts['feature_columns']

    # 1. Konversi Input ke DataFrame
    input_df = pd.DataFrame([user_inputs])

    # 2. Ordinal Encoding
    ordinal_cols = ['Physical Activity', 'Socioeconomic Factors', 'Alcohol Consumption']
    input_df[ordinal_cols] = oe.transform(input_df[ordinal_cols])

    # 3. One-Hot Encoding untuk Urine Test
    input_df = pd.get_dummies(input_df, columns=['Urine Test'])

    # 4. Binary Encoding
    for col in encoders_dict.keys():
        input_df[col] = encoders_dict[col].transform(input_df[col])

    # 5. Standard Scaling
    num_cols = list(scaler.feature_names_in_)
    input_df[num_cols] = scaler.transform(input_df[num_cols])

    # 6. Kolom Reindexing sesuai urutan latih model
    input_df = input_df.reindex(columns=feature_columns, fill_value=0)

    # 7. Model Inference & Probabilitas
    pred_encoded = model.predict(input_df)[0]
    pred_label = le_target.inverse_transform([pred_encoded])[0]

    confidence = 0.0
    top_3_results = []
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_df)[0]
        confidence = float(np.max(probabilities) * 100)
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_3_results = [
            (le_target.inverse_transform([i])[0], float(probabilities[i] * 100))
            for i in top_indices
        ]

    return pred_label, confidence, top_3_results


# ==============================================================================
# 4. RENDER KOMPONEN SIDEBAR NAVIGATION
# ==============================================================================
def render_sidebar_navigation():
    """Merender bilah navigasi sidebar kiri."""
    with st.sidebar:
        st.markdown(get_sidebar_brand_html(), unsafe_allow_html=True)

        st.markdown("<p style='font-size:10.5px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px; color:#93c5fd; margin-bottom:4px;'>Kategori Parameter</p>", unsafe_allow_html=True)
        
        nav_choice = st.radio(
            "Pilih Kategori Parameter",
            options=[
                "1. Laboratorium & Vitalis (13)",
                "2. Riwayat Klinis & Genetik (10)",
                "3. Gaya Hidup & Penunjang (10)"
            ],
            index=0,
            label_visibility="collapsed"
        )

        st.markdown(get_sidebar_card_html(), unsafe_allow_html=True)
        return nav_choice


# ==============================================================================
# 5. RENDER FORMULIR INPUT (KOLOM KIRI)
# ==============================================================================
def render_category_inputs(nav_choice: str, artifacts: dict):
    """Merender formulir input sesuai kategori yang dipilih."""
    encoders_dict = artifacts['encoders_dict']
    ordinal_categories = {
        'Physical Activity': ['Low', 'Moderate', 'High'],
        'Socioeconomic Factors': ['Low', 'Medium', 'High'],
        'Alcohol Consumption': ['Low', 'Moderate', 'High']
    }
    urine_test_options = ['Normal', 'Glucose Present', 'Protein Present', 'Ketones Present']

    st.markdown(get_card_header_html(nav_choice), unsafe_allow_html=True)

    # 1. KATEGORI 1: PARAMETER LABORATORIUM & VITALIS (13 Fitur dalam 3 Kolom Kompak)
    if "Laboratorium" in nav_choice:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state.all_inputs['Blood Glucose Levels'] = st.number_input(
                "Gula Darah Puasa [30-400]",
                value=float(st.session_state.all_inputs['Blood Glucose Levels']), min_value=30.0, max_value=400.0, step=5.0,
                help="Rentang: 30 - 400 mg/dL | Normal: 70 - 99 mg/dL",
                key="widget_Blood Glucose Levels"
            )
            st.session_state.all_inputs['Insulin Levels'] = st.number_input(
                "Kadar Insulin [0-150]",
                value=float(st.session_state.all_inputs['Insulin Levels']), min_value=0.0, max_value=150.0, step=2.0,
                help="Rentang: 0 - 150 μU/mL | Normal: 5 - 25 μU/mL",
                key="widget_Insulin Levels"
            )
            st.session_state.all_inputs['BMI'] = st.number_input(
                "Indeks Massa Tubuh [10-60]",
                value=float(st.session_state.all_inputs['BMI']), min_value=10.0, max_value=60.0, step=0.5,
                help="Rentang: 10 - 60 kg/m² | Normal: 18.5 - 24.9 kg/m²",
                key="widget_BMI"
            )
            st.session_state.all_inputs['Waist Circumference'] = st.number_input(
                "Lingkar Pinggang [18-60]",
                value=float(st.session_state.all_inputs['Waist Circumference']), min_value=18.0, max_value=60.0, step=1.0,
                help="Rentang: 18 - 60 inci | Standar: <35 inci (W), <40 inci (P)",
                key="widget_Waist Circumference"
            )
            st.session_state.all_inputs['Age'] = st.number_input(
                "Usia Pasien (Tahun) [0-100]",
                value=float(st.session_state.all_inputs['Age']), min_value=0.0, max_value=100.0, step=1.0,
                help="Rentang Usia: 0 - 100 Tahun",
                key="widget_Age"
            )

        with c2:
            st.session_state.all_inputs['Blood Pressure'] = st.number_input(
                "Tekanan Darah [60-240]",
                value=float(st.session_state.all_inputs['Blood Pressure']), min_value=60.0, max_value=240.0, step=5.0,
                help="Rentang: 60 - 240 mmHg | Normal: 90 - 120 mmHg",
                key="widget_Blood Pressure"
            )
            st.session_state.all_inputs['Cholesterol Levels'] = st.number_input(
                "Kolesterol Total [80-400]",
                value=float(st.session_state.all_inputs['Cholesterol Levels']), min_value=80.0, max_value=400.0, step=5.0,
                help="Rentang: 80 - 400 mg/dL | Normal: < 200 mg/dL",
                key="widget_Cholesterol Levels"
            )
            st.session_state.all_inputs['Pancreatic Health'] = st.number_input(
                "Kesehatan Pankreas [0-100]",
                value=float(st.session_state.all_inputs['Pancreatic Health']), min_value=0.0, max_value=100.0, step=5.0,
                help="Skor: 0 - 100 | Optimal: > 60",
                key="widget_Pancreatic Health"
            )
            st.session_state.all_inputs['Pulmonary Function'] = st.number_input(
                "Fungsi Paru-Paru [0-100]",
                value=float(st.session_state.all_inputs['Pulmonary Function']), min_value=0.0, max_value=100.0, step=5.0,
                help="Skor: 0 - 100 | Normal: > 75",
                key="widget_Pulmonary Function"
            )

        with c3:
            st.session_state.all_inputs['Neurological Assessments'] = st.number_input(
                "Skor Neurologis [0-5]",
                value=float(st.session_state.all_inputs['Neurological Assessments']), min_value=0.0, max_value=5.0, step=0.1,
                help="Skor: 0.0 - 5.0 | Normal: 0.0 - 2.0",
                key="widget_Neurological Assessments"
            )
            st.session_state.all_inputs['Digestive Enzyme Levels'] = st.number_input(
                "Enzim Pencernaan [0-100]",
                value=float(st.session_state.all_inputs['Digestive Enzyme Levels']), min_value=0.0, max_value=100.0, step=5.0,
                help="Skor: 0 - 100 | Normal: > 60",
                key="widget_Digestive Enzyme Levels"
            )
            st.session_state.all_inputs['Weight Gain During Pregnancy'] = st.number_input(
                "Kenaikan BB Hamil [0-45]",
                value=float(st.session_state.all_inputs['Weight Gain During Pregnancy']), min_value=0.0, max_value=45.0, step=1.0,
                help="Rentang: 0 - 45 kg (0 jika tidak hamil)",
                key="widget_Weight Gain During Pregnancy"
            )
            st.session_state.all_inputs['Birth Weight'] = st.number_input(
                "Berat Badan Lahir [500-6000]",
                value=float(st.session_state.all_inputs['Birth Weight']), min_value=500.0, max_value=6000.0, step=50.0,
                help="Rentang: 500 - 6000 Gram | Normal: 2500 - 4000 Gram",
                key="widget_Birth Weight"
            )

    # 2. KATEGORI 2: RIWAYAT KLINIS & GENETIK (10 Fitur dalam 2 Kolom Seimbang)
    elif "Riwayat Klinis" in nav_choice:
        c1, c2 = st.columns(2)
        with c1:
            gen_options = list(encoders_dict['Genetic Markers'].classes_)
            idx_gen = gen_options.index(st.session_state.all_inputs['Genetic Markers']) if st.session_state.all_inputs['Genetic Markers'] in gen_options else 0
            st.session_state.all_inputs['Genetic Markers'] = st.selectbox("Penanda Genetik", options=gen_options, index=idx_gen, key="widget_Genetic Markers")

            gen_test_options = list(encoders_dict['Genetic Testing'].classes_)
            idx_gt = gen_test_options.index(st.session_state.all_inputs['Genetic Testing']) if st.session_state.all_inputs['Genetic Testing'] in gen_test_options else 0
            st.session_state.all_inputs['Genetic Testing'] = st.selectbox("Skrining Genetik", options=gen_test_options, index=idx_gt, key="widget_Genetic Testing")

            auto_options = list(encoders_dict['Autoantibodies'].classes_)
            idx_auto = auto_options.index(st.session_state.all_inputs['Autoantibodies']) if st.session_state.all_inputs['Autoantibodies'] in auto_options else 0
            st.session_state.all_inputs['Autoantibodies'] = st.selectbox("Antibodi Autoimun", options=auto_options, index=idx_auto, key="widget_Autoantibodies")

            fam_options = list(encoders_dict['Family History'].classes_)
            idx_fam = fam_options.index(st.session_state.all_inputs['Family History']) if st.session_state.all_inputs['Family History'] in fam_options else 0
            st.session_state.all_inputs['Family History'] = st.selectbox("Riwayat Diabetes Keluarga", options=fam_options, index=idx_fam, key="widget_Family History")

            pcos_options = list(encoders_dict['History of PCOS'].classes_)
            idx_pcos = pcos_options.index(st.session_state.all_inputs['History of PCOS']) if st.session_state.all_inputs['History of PCOS'] in pcos_options else 0
            st.session_state.all_inputs['History of PCOS'] = st.selectbox("Riwayat PCOS", options=pcos_options, index=idx_pcos, key="widget_History of PCOS")

        with c2:
            pgd_options = list(encoders_dict['Previous Gestational Diabetes'].classes_)
            idx_pgd = pgd_options.index(st.session_state.all_inputs['Previous Gestational Diabetes']) if st.session_state.all_inputs['Previous Gestational Diabetes'] in pgd_options else 0
            st.session_state.all_inputs['Previous Gestational Diabetes'] = st.selectbox("Riwayat DM Gestasional", options=pgd_options, index=idx_pgd, key="widget_Previous Gestational Diabetes")

            preg_options = list(encoders_dict['Pregnancy History'].classes_)
            idx_preg = preg_options.index(st.session_state.all_inputs['Pregnancy History']) if st.session_state.all_inputs['Pregnancy History'] in preg_options else 0
            st.session_state.all_inputs['Pregnancy History'] = st.selectbox("Riwayat Kehamilan", options=preg_options, index=idx_preg, key="widget_Pregnancy History")

            cf_options = list(encoders_dict['Cystic Fibrosis Diagnosis'].classes_)
            idx_cf = cf_options.index(st.session_state.all_inputs['Cystic Fibrosis Diagnosis']) if st.session_state.all_inputs['Cystic Fibrosis Diagnosis'] in cf_options else 0
            st.session_state.all_inputs['Cystic Fibrosis Diagnosis'] = st.selectbox("Diagnosis Cystic Fibrosis", options=cf_options, index=idx_cf, key="widget_Cystic Fibrosis Diagnosis")

            steroid_options = list(encoders_dict['Steroid Use History'].classes_)
            idx_st = steroid_options.index(st.session_state.all_inputs['Steroid Use History']) if st.session_state.all_inputs['Steroid Use History'] in steroid_options else 0
            st.session_state.all_inputs['Steroid Use History'] = st.selectbox("Riwayat Terapi Steroid", options=steroid_options, index=idx_st, key="widget_Steroid Use History")

            onset_options = list(encoders_dict['Early Onset Symptoms'].classes_)
            idx_onset = onset_options.index(st.session_state.all_inputs['Early Onset Symptoms']) if st.session_state.all_inputs['Early Onset Symptoms'] in onset_options else 0
            st.session_state.all_inputs['Early Onset Symptoms'] = st.selectbox("Gejala Onset Dini", options=onset_options, index=idx_onset, key="widget_Early Onset Symptoms")

    # 3. KATEGORI 3: GAYA HIDUP & PENUNJANG (10 Fitur dalam 2 Kolom Seimbang)
    else:
        c1, c2 = st.columns(2)
        with c1:
            pa_options = ordinal_categories['Physical Activity']
            idx_pa = pa_options.index(st.session_state.all_inputs['Physical Activity']) if st.session_state.all_inputs['Physical Activity'] in pa_options else 1
            st.session_state.all_inputs['Physical Activity'] = st.selectbox("Tingkat Aktivitas Fisik", options=pa_options, index=idx_pa, key="widget_Physical Activity")

            diet_options = list(encoders_dict['Dietary Habits'].classes_)
            idx_diet = diet_options.index(st.session_state.all_inputs['Dietary Habits']) if st.session_state.all_inputs['Dietary Habits'] in diet_options else 0
            st.session_state.all_inputs['Dietary Habits'] = st.selectbox("Pola Diet / Nutrisi", options=diet_options, index=idx_diet, key="widget_Dietary Habits")

            smoke_options = list(encoders_dict['Smoking Status'].classes_)
            idx_smoke = smoke_options.index(st.session_state.all_inputs['Smoking Status']) if st.session_state.all_inputs['Smoking Status'] in smoke_options else 0
            st.session_state.all_inputs['Smoking Status'] = st.selectbox("Status Merokok", options=smoke_options, index=idx_smoke, key="widget_Smoking Status")

            alc_options = ordinal_categories['Alcohol Consumption']
            idx_alc = alc_options.index(st.session_state.all_inputs['Alcohol Consumption']) if st.session_state.all_inputs['Alcohol Consumption'] in alc_options else 0
            st.session_state.all_inputs['Alcohol Consumption'] = st.selectbox("Konsumsi Alkohol", options=alc_options, index=idx_alc, key="widget_Alcohol Consumption")

            soc_options = ordinal_categories['Socioeconomic Factors']
            idx_soc = soc_options.index(st.session_state.all_inputs['Socioeconomic Factors']) if st.session_state.all_inputs['Socioeconomic Factors'] in soc_options else 1
            st.session_state.all_inputs['Socioeconomic Factors'] = st.selectbox("Status Sosioekonomi", options=soc_options, index=idx_soc, key="widget_Socioeconomic Factors")

        with c2:
            eth_options = list(encoders_dict['Ethnicity'].classes_)
            idx_eth = eth_options.index(st.session_state.all_inputs['Ethnicity']) if st.session_state.all_inputs['Ethnicity'] in eth_options else 0
            st.session_state.all_inputs['Ethnicity'] = st.selectbox("Kategori Risiko Etnis", options=eth_options, index=idx_eth, key="widget_Ethnicity")

            gtt_options = list(encoders_dict['Glucose Tolerance Test'].classes_)
            idx_gtt = gtt_options.index(st.session_state.all_inputs['Glucose Tolerance Test']) if st.session_state.all_inputs['Glucose Tolerance Test'] in gtt_options else 1
            st.session_state.all_inputs['Glucose Tolerance Test'] = st.selectbox("Uji Toleransi Glukosa (TTGO)", options=gtt_options, index=idx_gtt, key="widget_Glucose Tolerance Test")

            lft_options = list(encoders_dict['Liver Function Tests'].classes_)
            idx_lft = lft_options.index(st.session_state.all_inputs['Liver Function Tests']) if st.session_state.all_inputs['Liver Function Tests'] in lft_options else 1
            st.session_state.all_inputs['Liver Function Tests'] = st.selectbox("Uji Fungsi Hati (LFT)", options=lft_options, index=idx_lft, key="widget_Liver Function Tests")

            env_options = list(encoders_dict['Environmental Factors'].classes_)
            idx_env = env_options.index(st.session_state.all_inputs['Environmental Factors']) if st.session_state.all_inputs['Environmental Factors'] in env_options else 0
            st.session_state.all_inputs['Environmental Factors'] = st.selectbox("Faktor Paparan Lingkungan", options=env_options, index=idx_env, key="widget_Environmental Factors")

            idx_urin = urine_test_options.index(st.session_state.all_inputs['Urine Test']) if st.session_state.all_inputs['Urine Test'] in urine_test_options else 0
            st.session_state.all_inputs['Urine Test'] = st.selectbox("Hasil Analisis Urine", options=urine_test_options, index=idx_urin, key="widget_Urine Test")


# ==============================================================================
# 6. MAIN CONTROLLER
# ==============================================================================
def main():
    # 1. Setup Konfigurasi & Muat CSS Eksternal (assets/style.css)
    setup_page_configuration()
    artifacts = load_ml_artifacts()

    # 2. Inisialisasi State Permanen 33 Parameter
    if "all_inputs" not in st.session_state:
        st.session_state.all_inputs = dict(DEFAULT_INPUTS)

    # 3. Render Navigasi Sidebar di Sebelah Kiri
    nav_choice = render_sidebar_navigation()

    # 4. Top Header Banner Medis
    st.markdown(get_top_header_html(), unsafe_allow_html=True)

    # 5. Split 2 Kolom Sempurna dengan st.container(border=True) Native
    col_form, col_result = st.columns([1.35, 1.0], gap="medium")

    with col_form:
        with st.container(border=True):
            render_category_inputs(nav_choice, artifacts)

    with col_result:
        with st.container(border=True):
            # Eksekusi inferensi otomatis real-time
            pred_label, confidence, top_3_results = predict_diabetes_case(st.session_state.all_inputs, artifacts)
            # Render panel diagnosa dari template komponen
            st.markdown(get_diagnosis_panel_html(pred_label, confidence, top_3_results), unsafe_allow_html=True)


if __name__ == "__main__":
    main()