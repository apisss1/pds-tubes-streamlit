import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import folium


#Set Layout Page
st.set_page_config(layout='wide' , initial_sidebar_state= 'expanded')

#Title
st.title("Dashboard Analisis Data OSN SMA Tahun 2022 - 2024")

#Read Data Function
def load_data():
    return pd.read_csv("data/osn_fiks.csv")
df = load_data()

#Column section
col1, col2, col3 = st.columns(3)
col1.metric("📄 Total Data", len(df))
col2.metric("🏫 Jumlah Provinsi", df["Provinsi"].nunique())
col3.metric("📚 Jumlah Bidang", df["Bidang"].nunique())

#Sidebar section
st.sidebar.header("Dashboard")
tahun = st.sidebar.multiselect(
    "Pilih Tahun",
    sorted(df["Tahun"].unique()),
)
provinsi = st.sidebar.multiselect(
    "Filter Provinsi",
    sorted(df["Provinsi"].unique()),
)

#Table Data Section
def Table_Data(tahun , provinsi , df):
    filter = df
    t = " - ".join(map(str , tahun))
    p = " , ".join(provinsi)

    if tahun and provinsi :
        filter = filter[(filter["Tahun"].isin(tahun)) & (filter["Provinsi"].isin(provinsi))]
        st.success(f"Data dari Provinsi {p} Tahun {t}")
    elif tahun :
        filter = filter[filter["Tahun"].isin(tahun)]
        st.success(f"Data Tahun {t}")
    elif provinsi :
        filter = filter[filter["Provinsi"].isin(provinsi)]
        st.success(f"Data Provinsi {p}")
    
    st.dataframe(filter , use_container_width = True)

#Grafik Bar Section
def Bar_Data(tahun , provinsi , df):
    filter = df
    t = " - ".join(map(str , tahun))
    p = " , ".join(provinsi)

    if tahun and provinsi :
        filter = filter [(filter["Tahun"].isin(tahun)) & (filter["Provinsi"].isin(provinsi))]
        st.success(f"Data dari Provinsi {p} Tahun {t}")
    elif tahun : 
        filter = filter [(filter["Tahun"].isin(tahun))]
        st.success(f"Data Tahun {t}")
    elif provinsi :
        filter = filter [(filter["Provinsi"].isin(provinsi))]
        st.success(f"Data Provinsi {p}")

    fig1, ax1 = plt.subplots(figsize=(10,5))
       
    prov_count = filter["Provinsi"].value_counts()
        
    prov_count.plot(kind="bar", ax=ax1)
    ax1.set_xlabel("Provinsi")
    ax1.set_ylabel("Jumlah Peserta")
    plt.xticks(rotation=75)

    st.pyplot(fig1)
    plt.close(fig1)

#Grafik Pie Section
def Pie_Data(tahun , provinsi , df):
    filter = df
    t = " - ".join(map(str , tahun))
    p = " , ".join(provinsi)

    if tahun and provinsi :
        filter = filter [(filter["Tahun"].isin(tahun)) & (filter["Provinsi"].isin(provinsi))]
        st.success(f"Data dari Provinsi {p} Tahun {t}")
    elif tahun : 
        filter = filter [(filter["Tahun"].isin(tahun))]
        st.success(f"Data Tahun {t}")
    elif provinsi :
        filter = filter [(filter["Provinsi"].isin(provinsi))]
        st.success(f"Data Provinsi {p}")

    bidang_count = filter["Bidang"].value_counts()

    fig2, ax2 = plt.subplots()
    ax2.pie(
        bidang_count,
        labels=bidang_count.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax2.axis("equal")

    st.pyplot(fig2)
    plt.close(fig2)

#Map Section
def Map_Data(tahun, provinsi, df):
    # ================= FILTER DATA =================
    filter = df.copy()
    t = " - ".join(map(str, tahun))
    p = " , ".join(provinsi)

    if tahun and provinsi:
        filter = filter[
            (filter["Tahun"].isin(tahun)) &
            (filter["Provinsi"].isin(provinsi))
        ]
        st.success(f"Data dari Provinsi {p} Tahun {t}")
    elif tahun:
        filter = filter[filter["Tahun"].isin(tahun)]
        st.success(f"Data Tahun {t}")
    elif provinsi:
        filter = filter[filter["Provinsi"].isin(provinsi)]
        st.success(f"Data Provinsi {p}")

    if filter.empty:
        st.warning("Tidak ada data untuk ditampilkan di peta.")
        return

    # ================= AGREGASI =================
    agg_data = filter.groupby("Provinsi").agg(
        Jumlah_Peserta=("Provinsi", "count"),
        Bidang_Unggulan=("Bidang", lambda x: x.mode().iloc[0]),
        Bidang_Terlemah=("Bidang", lambda x: x.value_counts().idxmin()),
        Latitude=("Latitude", "first"),
        Longitude=("Longitude", "first")
    ).reset_index()

    # ================= FUNGSI WARNA =================
    def color(jumlah):
        if jumlah >= 100:
            return "red"
        elif jumlah >= 50:
            return "orange"
        else:
            return "green"

    # ================= MAP =================
    m = folium.Map(
        location=[-2.5489, 118.0149],
        zoom_start=5,
        tiles="CartoDB positron"
    )

    # ================= TITIK BERWARNA =================
    for _, row in agg_data.iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=10,
            color=color(row["Jumlah_Peserta"]),
            fill=True,
            fill_color=color(row["Jumlah_Peserta"]),
            fill_opacity=0.8,
            tooltip=f"""
            <b>{row['Provinsi']}</b><br>
            Jumlah Peserta: {row['Jumlah_Peserta']}<br>
            Bidang Unggulan: {row['Bidang_Unggulan']}<br>
            Bidang Terlemah: {row['Bidang_Terlemah']}
            """
        ).add_to(m)

    # ================= RENDER =================
    st.components.v1.html(
        m._repr_html_(),
        height=550,
        scrolling=False
    )


#Main Program 
st.subheader("Data Siswa OSN")
Table_Data(tahun , provinsi , df)
st.subheader("Grafik Jumlah total Peserta OSN 2022-2024 tiap Provinsi")
Bar_Data(tahun , provinsi , df)
st.subheader("Grafik Persentase tiap Bidang di Indonesia ")
Pie_Data(tahun , provinsi , df)
st.subheader("Peta Sebaran")
Map_Data(tahun, provinsi, df)