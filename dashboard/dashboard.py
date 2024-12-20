import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Penyewaan Sepeda",
    layout="wide",
)

st.title("Dashboard Penyewaan Sepeda")

# Membuat tab / menu dashboard
tab1, tab2, tab3 = st.tabs(
    ["Tren Hari Libur vs Hari Kerja", "Musim dan Penyewa", "Waktu Favorit Penyewa"]
)

day_df = pd.read_csv("../data/day.csv")
hour_df = pd.read_csv("../data/hour.csv")

# Sidebar
st.sidebar.header("Filter")
start_date = st.sidebar.date_input(
    "Tanggal Mulai", pd.to_datetime(day_df["dteday"]).min()
)
end_date = st.sidebar.date_input(
    "Tanggal Akhir", pd.to_datetime(day_df["dteday"]).max()
)

# Filter berdasarkan musim
season = st.sidebar.selectbox(
    "Pilih Musim", ["Semua", "Spring", "Summer", "Fall", "Winter"]
)

# Pemetaan musim
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
day_df["season_name"] = day_df["season"].map(season_mapping)

# Menerapkan filter
filtered_day_df = day_df[
    (pd.to_datetime(day_df["dteday"]) >= pd.to_datetime(start_date))
    & (pd.to_datetime(day_df["dteday"]) <= pd.to_datetime(end_date))
]

if season != "Semua":
    filtered_day_df = filtered_day_df[filtered_day_df["season_name"] == season]

# Hari Libur vs Hari Kerja
with tab1:
    st.subheader("Tren Penyewaan Sepeda pada Hari Libur vs Hari Kerja")

    # Persiapan data
    workingday_group = filtered_day_df.groupby("workingday")[
        ["casual", "registered"]
    ].mean()
    workingday_group.index = ["Libur", "Kerja"]

    # Visualisasi
    fig, ax = plt.subplots(figsize=(8, 5))
    workingday_group.plot(kind="bar", ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda (Hari Libur vs Hari Kerja)")
    ax.set_xlabel("Hari")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

    st.markdown(
        "- Penyewa **terdaftar** lebih banyak menyewa sepeda pada hari kerja.\n"
        "- Penyewa **kasual** lebih banyak menyewa sepeda pada hari libur."
    )

# Musim dan Penyewa
with tab2:
    st.subheader("Musim yang Paling Diminati oleh Penyewa")

    # Persiapan data
    season_group = filtered_day_df.groupby("season_name")[
        ["casual", "registered"]
    ].mean()

    # Visualisasi
    fig, ax = plt.subplots(figsize=(8, 5))
    season_group.plot(kind="bar", ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda per Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

    st.markdown(
        f"- Musim **{season if season != 'Semua' else 'Fall'}** memiliki penyewaan tertinggi untuk penyewa **kasual** dan **terdaftar**."
    )

# Waktu Favorit Penyewa
with tab3:
    st.subheader("Waktu Favorit Penyewa Sepeda dalam Satu Hari")

    filtered_hour_df = hour_df[
        (pd.to_datetime(hour_df["dteday"]) >= pd.to_datetime(start_date))
        & (pd.to_datetime(hour_df["dteday"]) <= pd.to_datetime(end_date))
    ]

    # Persiapan data
    hourly_group = filtered_hour_df.groupby("hr")[["casual", "registered"]].mean()

    # Visualisasi
    fig, ax = plt.subplots(figsize=(8, 5))
    hourly_group.plot(kind="line", ax=ax, marker="o")
    ax.set_title("Rata-rata Penyewaan Sepeda per Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Penyewaan")
    ax.legend(["Casual", "Registered"])
    st.pyplot(fig)

    st.markdown(
        "- Penyewa **kasual** menyewa sepeda paling banyak sekitar jam **14:00**.\n"
        "- Penyewa **terdaftar** menyewa sepeda paling banyak sekitar jam **17:00**."
    )
