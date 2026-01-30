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
    import json

    # ================= FILTER DATA =================
    filter = df.copy()

    if tahun and print :
        filter = filter[filter["Tahun"].isin(tahun)] & filter[filter["Provinsi"].isin(provinsi)]
    elif tahun:
        filter = filter[filter["Tahun"].isin(tahun)]
    elif provinsi:
        filter = filter[filter["Provinsi"].isin(provinsi)]

    if filter.empty:
        st.warning("Tidak ada data untuk ditampilkan di peta.")
        return

    # ================= AGREGASI =================
    agg_data = filter.groupby("Provinsi").size().reset_index(name="Jumlah_Peserta")

    # ================= LOAD GEOJSON =================
    with open("data/indonesia_province.geojson", encoding="utf-8") as f:
        geojson_data = json.load(f)

    # ================= JOIN DATA =================
    peserta_map = dict(zip(agg_data["Provinsi"], agg_data["Jumlah_Peserta"]))

    def get_jumlah(feature):
        nama = feature["properties"]["NAME_1"]
        return peserta_map.get(nama, 0)

    def style_function(feature):
        jumlah = get_jumlah(feature)
        if jumlah >= 100:
            warna = "red"
        elif jumlah >= 50:
            warna = "orange"
        elif jumlah > 0:
            warna = "green"
        else:
            warna = "#dddddd"

        return {
            "fillColor": warna,
            "color": "black",
            "weight": 0.8,
            "fillOpacity": 0.8
        }

    # ================= MAP =================
    m = folium.Map(
        location=[-2.5489, 118.0149],
        zoom_start=5,
        tiles="CartoDB positron"
    )

    folium.GeoJson(
        geojson_data,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["NAME_1"],
            aliases=["Provinsi:"]
        )
    ).add_to(m)

    st.components.v1.html(m._repr_html_(), height=550)

#Main Program 
st.subheader("Data Siswa OSN")
Table_Data(tahun , provinsi , df)
st.subheader("Grafik Jumlah total Peserta OSN 2022-2024 tiap Provinsi")
Bar_Data(tahun , provinsi , df)
st.subheader("Grafik Persentase tiap Bidang di Indonesia ")
Pie_Data(tahun , provinsi , df)
st.subheader("Peta Sebaran")
Map_Data(tahun, provinsi, df)