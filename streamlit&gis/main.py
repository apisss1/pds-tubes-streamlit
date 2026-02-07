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
st.title("Dashboard Analisis Data OSN Tingkat SMA Tahun 2022 - 2024")

#Read Data Function
df = pd.read_csv("data_osn_fiks_banget.csv")

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
    filter["Tahun"] = filter["Tahun"].astype(int)
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

# Map Section
def Map_Data(tahun, provinsi, df):
    t = " - ".join(map(str, tahun))
    p = " , ".join(provinsi)
    # Filtering data
    data_filter = df.copy()

    if tahun and provinsi:
        data_filter = data_filter[(data_filter["Tahun"].isin(tahun)) & (data_filter["Provinsi"].isin(provinsi))]
        st.success(f"Data dari Provinsi {p} Tahun {t}")
    elif tahun:
        data_filter = data_filter[data_filter["Tahun"].isin(tahun)]
        st.success(f"Data Tahun {t}")
    elif provinsi:
        data_filter = data_filter[data_filter["Provinsi"].isin(provinsi)]
        st.success(f"Data Provinsi {p}")

    #Checking Data
    if data_filter.empty:
        st.warning("Tidak ada data untuk ditampilkan di peta.")
        return

    # Aggregasi Data
    agg_data = data_filter.groupby("Provinsi").agg(
        Jumlah_Peserta=("Provinsi", "count"),
        Bidang_Unggulan=("Bidang", lambda x: x.mode()[0]),
        Bidang_Terlemah=("Bidang", lambda x: x.value_counts().idxmin()),
        Latitude=("Latitude", "first"),
        Longitude=("Longitude", "first")
    ).reset_index()
    agg_data["Jumlah_Peserta"] = agg_data["Jumlah_Peserta"].astype(int)

    # Read geojson
    with open("indonesia.geojson", "r", encoding="utf-8") as f:
        geo_prov = json.load(f)

    # Create Map
    m = folium.Map(location=[-2.5489, 118.0149], zoom_start=5, tiles="CartoDB positron")

    folium.GeoJson(
        geo_prov,
        style_function=lambda feature: {
            "fillColor": "#2984EC",
            "color": "black",    
            "weight": 1,
            "fillOpacity": 1
        }
    ).add_to(m)

    for _, row in agg_data.iterrows():
        if pd.notna(row["Latitude"]) and pd.notna(row["Longitude"]):

            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                icon=folium.DivIcon(
                    html=f"""
                    <div style="
                        position: relative;
                        transform: translate(-50%, -100%);
                    ">
                        <!-- Marker -->
                        <div style="
                            width:18px;
                            height:18px;
                            background:#191960;
                            border-radius:50% 50% 50% 0;
                            transform: rotate(-45deg);
                            box-shadow: 0 2px 6px rgba(0,0,0,0.3);
                        "></div>
                        <!-- Inner Marker -->
                        <div style="
                            position:absolute;
                            top:4px;
                            left:5px;
                            width:10px;
                            height:10px;
                            background:white;
                            border-radius:50%;
                        "></div>
                        <!-- Text Label -->
                        <div style="
                            margin-top:6px;
                            text-align:center;
                            font-size:10px;
                            font-weight:bold;
                            color:black;
                            white-space:nowrap;
                        ">
                            {row['Provinsi']}
                        </div>
                    </div>
                    """
                ),
                tooltip=(
                    f"Provinsi: {row['Provinsi']}<br>"
                    f"Jumlah Peserta: {row['Jumlah_Peserta']}<br>"
                    f"Bidang Unggulan: {row['Bidang_Unggulan']}<br>"
                    f"Bidang Terlemah: {row['Bidang_Terlemah']}"
                )
            ).add_to(m)
    
    #Rendering Streamlit Cloud
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