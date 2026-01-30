import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import folium
import json
import os

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
    #Filter Data 
    filter = df.copy()
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
        return
        
    #Checking Data
    if filter.empty:
        st.warning("Tidak ada data untuk ditampilkan di peta.")
        return

    # Agregasi Data 
    agg_data = filter.groupby("Provinsi").agg(
        Jumlah_Peserta=("Provinsi", "count"),
        Bidang_Unggulan=("Bidang", lambda x: x.mode().iloc()[0]),
        Bidang_Terlemah=("Bidang", lambda x: x.value_counts().idxmin()),
        Latitude=("Latitude", "first"),
        Longitude=("Longitude", "first")
    ).reset_index()
    
    features = []

    for _, row in agg_data.iterrows():
        #Information Feature
        features.append({
            "type": "Feature",
            "properties": {
                "Provinsi": row["Provinsi"],
                "jumlah_peserta": int(row["Jumlah_Peserta"]),
                "bidang_unggulan": row["Bidang_Unggulan"],
                "bidang_terlemah": row["Bidang_Terlemah"]
            },
            "geometry": {
                "type": "Point",
                "coordinates": [row["Longitude"], row["Latitude"]]
            }
        })

    #GeoJSON Data
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    #Set Map Size
    m = folium.Map(location=[-2.5489, 118.0149],
                    zoom_start=5,
                    max_zoom=12,
                    min_zoom=2,
                    tiles="CartoDB positron")
    
    #Show Feature to Map
    folium.GeoJson(
        geojson_data,
        tooltip=folium.GeoJsonTooltip(
            fields=["Provinsi", "jumlah_peserta", "bidang_unggulan", "bidang_terlemah"],
            aliases=["Provinsi:", "Total Peserta:", "Bidang Unggulan:", "Bidang Terlemah:"]
        )
    ).add_to(m)

    # Marker Section
    for feature in geojson_data["features"]:
        lon, lat = feature["geometry"]["coordinates"]
        nama = feature["properties"]["Provinsi"]

        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size: 9px;
                    font-weight: bold;
                    color: black;
                    text-align: center;
                    text-shadow: 1px 1px 2px white;
                ">
                    {nama}
                </div>
                """
            )
        ).add_to(m)
        
    #Render Streamlit
    st.components.v1.html(
    m._repr_html_(),
    height=550,
    scrolling=False)

#Main Program 
st.subheader("Data Siswa OSN")
Table_Data(tahun , provinsi , df)
st.subheader("Grafik Jumlah total Peserta OSN 2022-2024 tiap Provinsi")
Bar_Data(tahun , provinsi , df)
st.subheader("Grafik Persentase tiap Bidang di Indonesia ")
Pie_Data(tahun , provinsi , df)
st.subheader("Peta Sebaran")
Map_Data(tahun, provinsi, df)