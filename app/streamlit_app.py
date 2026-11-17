import streamlit as st
import pandas as pd

from datetime import datetime, date, time


# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="PM2.5 Bandung Forecast",
    page_icon="",
    layout="wide"
)


# ==========================================
# 2. HEADER
# ==========================================

st.title("PM2.5 Bandung Forecast")

st.caption(
    "Sistem prakiraan konsentrasi PM2.5 "
    "tiga jam ke depan pada lima stasiun Bandung."
)

st.info(
    "Prototype aplikasi. Model Machine Learning "
    "belum diintegrasikan."
)


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
# 4. FORM INPUT
# ==========================================

st.header("Input Kondisi Udara")

with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:

        station = st.selectbox(
            "Stasiun Pemantauan",
            stations
        )

        observation_date = st.date_input(
            "Tanggal Pengamatan",
            value=date.today()
        )

        observation_time = st.time_input(
            "Waktu Pengamatan",
            value=time(15, 0)
        )

        pm25 = st.number_input(
            "PM2.5 Saat Ini (µg/m³)",
            min_value=0.0,
            value=25.0,
            step=0.1
        )

        temperature = st.number_input(
            "Suhu Udara (°C)",
            value=27.0,
            step=0.1
        )

        humidity = st.number_input(
            "Kelembapan (%)",
            min_value=0.0,
            max_value=100.0,
            value=70.0,
            step=0.1
        )

    with col2:

        wind_speed = st.number_input(
            "Kecepatan Angin (m/s)",
            min_value=0.0,
            value=2.0,
            step=0.1
        )

        wind_direction = st.number_input(
            "Arah Angin (derajat)",
            min_value=0.0,
            max_value=360.0,
            value=180.0,
            step=1.0
        )

        rainfall = st.number_input(
            "Curah Hujan (mm)",
            min_value=0.0,
            value=0.0,
            step=0.1
        )

    submitted = st.form_submit_button(
        "Periksa Input",
        use_container_width=True
    )


# ==========================================
# 5. VALIDASI DAN PENYIMPANAN INPUT
# ==========================================

if submitted:

    errors = []

    if pm25 < 0:
        errors.append("PM2.5 tidak boleh negatif.")

    if not -20 <= temperature <= 60:
        errors.append("Suhu di luar rentang pemeriksaan awal.")

    if not 0 <= humidity <= 100:
        errors.append("Kelembapan harus berada antara 0-100%.")

    if wind_speed < 0:
        errors.append("Kecepatan angin tidak boleh negatif.")

    if not 0 <= wind_direction <= 360:
        errors.append("Arah angin harus antara 0-360 derajat.")

    if rainfall < 0:
        errors.append("Curah hujan tidak boleh negatif.")

    if errors:

        for error in errors:
            st.error(error)

        st.session_state.pop("last_input", None)

    else:

        input_data = {
            "waktu": datetime.combine(
                observation_date,
                observation_time
            ).isoformat(),

            "stasiun": station,
            "pm25_ugm3": pm25,
            "suhu_C": temperature,
            "kelembaban_pct": humidity,
            "kecepatan_angin_ms": wind_speed,
            "arah_angin_deg": wind_direction,
            "curah_hujan_mm": rainfall
        }

        st.session_state["last_input"] = input_data

        st.success("Input berhasil divalidasi!")


# ==========================================
# 6. RINGKASAN INPUT
# ==========================================

if "last_input" in st.session_state:

    st.divider()

    st.header("Ringkasan Kondisi Pengamatan")

    data = st.session_state["last_input"]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "PM2.5 Saat Ini",
        f"{data['pm25_ugm3']} µg/m³"
    )

    col2.metric(
        "Suhu",
        f"{data['suhu_C']} °C"
    )

    col3.metric(
        "Kelembapan",
        f"{data['kelembaban_pct']}%"
    )

    st.subheader("Detail Data Input")

    display_data = pd.DataFrame(
        list(data.items()),
        columns=["Parameter", "Nilai"]
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

    st.warning(
        "Prediksi belum tersedia. "
        "Hubungkan aplikasi dengan model Machine Learning "
        "setelah artifact final selesai dibuat."
    )

    with st.expander("Lihat data JSON"):

        st.json(data)


# ==========================================
# 7. FOOTER
# ==========================================

st.divider()

st.caption(
    "Machine Learning Project · Kasus 06 "
    "| Prakiraan PM2.5 Bandung"
)