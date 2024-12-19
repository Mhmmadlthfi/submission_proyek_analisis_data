import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# Hari Libur vs Hari Kerja
with tab1:
    st.subheader("Tren Penyewaan Sepeda pada Hari Libur vs Hari Kerja")

    # Persiapan data / Data Preparation
    workingday_group = day_df.groupby("workingday")[["casual", "registered"]].mean()
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

# Tab 2: Musim dan Penyewa
with tab2:
    st.subheader("Musim yang Paling Diminati oleh Penyewa")

    # Data Preparation
    season_group = day_df.groupby("season")[["casual", "registered"]].mean()
    season_group.index = ["Spring", "Summer", "Fall", "Winter"]

    # Visualization
    fig, ax = plt.subplots(figsize=(8, 5))
    season_group.plot(kind="bar", ax=ax)
    ax.set_title("Rata-rata Penyewaan Sepeda per Musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan")
    st.pyplot(fig)

    st.markdown(
        "- Musim **Fall** memiliki penyewaan tertinggi untuk penyewa **kasual** dan **terdaftar**."
    )

# Tab 3: Waktu Favorit Penyewa
with tab3:
    st.subheader("Waktu Favorit Penyewa Sepeda dalam Satu Hari")

    # Data Preparation
    hourly_group = hour_df.groupby("hr")[["casual", "registered"]].mean()

    # Visualization
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
