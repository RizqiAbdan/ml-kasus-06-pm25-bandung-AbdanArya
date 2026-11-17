
import streamlit as st
import pandas as pd
from datetime import datetime, date, time


# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="Prakiraan PM2.5 Bandung",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ==========================================
# 2. HEADER
# ==========================================

st.title("Prakiraan PM2.5 Bandung")

st.caption(
    "Prakiraan konsentrasi PM2.5 tiga jam ke depan "
    "berdasarkan kondisi pengamatan pada lima stasiun Bandung."
)

st.divider()


# ==========================================
# 3. DAFTAR STASIUN
# ==========================================

stations = [
    "Dago",
    "Soekarno-Hatta",
    "Cibeureum",
    "Antapani",
    "Ujungberung"
]


# ==========================================
# 4. FORM PENGAMATAN
# ==========================================

st.subheader("Data pengamatan")

st.caption(
    "Masukkan kondisi sensor pada waktu pengamatan. "
    "Seluruh waktu menggunakan WIB."
)

with st.form("observation_form"):

    # Lokasi dan waktu
    col1, col2, col3 = st.columns(3)

    with col1:
        station = st.selectbox(
            "Stasiun",
            stations
        )

    with col2:
        observation_date = st.date_input(
            "Tanggal",
            value=date.today()
        )

    with col3:
        observation_time = st.time_input(
            "Waktu",
            value=time(15, 0)
        )

    st.markdown("**Parameter sensor**")

    # Baris pertama
    col1, col2 = st.columns(2)

    with col1:
        pm25 = st.number_input(
            "PM2.5 (µg/m³)",
            min_value=0.0,
            value=25.0,
            step=0.1,
            help="Konsentrasi PM2.5 saat pengamatan."
        )

    with col2:
        temperature = st.number_input(
            "Suhu udara (°C)",
            value=27.0,
            step=0.1
        )

    # Baris kedua
    col1, col2 = st.columns(2)

    with col1:
        humidity = st.number_input(
            "Kelembapan (%)",
            min_value=0.0,
            max_value=100.0,
            value=70.0,
            step=0.1
        )

    with col2:
        wind_speed = st.number_input(
            "Kecepatan angin (m/s)",
            min_value=0.0,
            value=2.0,
            step=0.1
        )

    # Baris ketiga
    col1, col2 = st.columns(2)

    with col1:
        wind_direction = st.number_input(
            "Arah angin (derajat)",
            min_value=0.0,
            max_value=360.0,
            value=180.0,
            step=1.0
        )

    with col2:
        rainfall = st.number_input(
            "Curah hujan (mm)",
            min_value=0.0,
            value=0.0,
            step=0.1
        )

    submitted = st.form_submit_button(
        "Proses pengamatan",
        type="primary",
        use_container_width=True
    )


# ==========================================
# 5. VALIDASI INPUT
# ==========================================

if submitted:

    errors = []

    if humidity < 0 or humidity > 100:
        errors.append(
            "Kelembapan harus berada pada rentang 0–100%."
        )

    if wind_speed < 0:
        errors.append(
            "Kecepatan angin tidak boleh negatif."
        )

    if not 0 <= wind_direction <= 360:
        errors.append(
            "Arah angin harus berada pada rentang 0–360 derajat."
        )

    if rainfall < 0:
        errors.append(
            "Curah hujan tidak boleh negatif."
        )

    if errors:

        st.session_state.pop("observation_data", None)

        for error in errors:
            st.error(error)

    else:

        observation_data = {
            "waktu": datetime.combine(
                observation_date,
                observation_time
            ).strftime("%Y-%m-%d %H:%M:%S"),

            "stasiun": station,
            "pm25_ugm3": pm25,
            "suhu_C": temperature,
            "kelembaban_pct": humidity,
            "kecepatan_angin_ms": wind_speed,
            "arah_angin_deg": wind_direction,
            "curah_hujan_mm": rainfall
        }

        st.session_state["observation_data"] = observation_data

        st.success(
            f"Data pengamatan {station} berhasil divalidasi."
        )


# ==========================================
# 6. HASIL DAN RINGKASAN
# ==========================================

if "observation_data" in st.session_state:

    data = st.session_state["observation_data"]

    with st.expander("Tinjau data yang akan diproses"):

        st.json(data)

    st.divider()

    st.subheader("Prakiraan PM2.5 +3 jam")

    st.info(
        "Model Machine Learning belum terintegrasi. "
        "Hasil prakiraan akan ditampilkan setelah "
        "model dan preprocessing siap digunakan."
    )


# ==========================================
# 7. FOOTER
# ==========================================

st.divider()

st.caption(
    "Machine Learning Project · Kasus 06 · PM2.5 Bandung"
)
