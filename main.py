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

def Map_Data(tahun, provinsi, df):
    import copy
    
    #filtering data 
    filter_df = df.copy()
    if tahun:
        filter_df = filter_df[filter_df["Tahun"].isin(tahun)]
    if filter_df.empty:
        st.warning("Tidak ada data untuk ditampilkan di peta.")
        return

    #normalize section
    def normalize(nama):
        if not isinstance(nama, str):
            return ""

        nama = nama.lower().replace("-", " ").strip()
        # hapus kata umum
        for k in ["provinsi", "propinsi", "daerah", "raya", "istimewa", "kepulauan"]:
            nama = nama.replace(k, "")

        nama = " ".join(nama.split()) #
        # normalisasi khusus
        if "jakarta" in nama:
            return "dki jakarta"
        if "yogyakarta" in nama:
            return "di yogyakarta"
        if "bangka" in nama and "belitung" in nama:
            return "bangka belitung"
        return nama
    
    #agregasi data
    agg_data = (
        filter_df
        .groupby("Provinsi")
        .agg(
            Jumlah_Peserta=("Provinsi", "count"),
            Bidang_Unggulan=("Bidang", lambda x: x.mode().iloc[0] if not x.mode().empty else "-"),
            Bidang_Terlemah=("Bidang", lambda x: x.value_counts().idxmin() if not x.empty else "-")
        )
        .reset_index()
    )

    #dictionary data
    data_dict = {
    normalize(row["Provinsi"]): row
    for _, row in agg_data.iterrows()
    }

    #read map data
    geojson_path = os.path.join("data", "indonesia.geojson")

    try:
        with open(geojson_path, "r", encoding="utf-8") as f:
            geojson_original = json.load(f)
    except Exception as e:
        st.error(f"Gagal memuat peta: {e}")
        return

    #copy map data
    geojson_data = copy.deepcopy(geojson_original)

    #filtering map data
    if provinsi:
        prov_norm = [normalize(p) for p in provinsi]

        geojson_data["features"] = [
            f for f in geojson_data["features"]
            if normalize(
                f["properties"].get("state")
                or f["properties"].get("name")
                or f["properties"].get("Propinsi")
            ) in prov_norm
        ]

        if not geojson_data["features"]:
            st.warning("Provinsi tidak ditemukan di peta.")
            return

    for f in geojson_data["features"]:
        p = f["properties"]

        nama_peta = (
            p.get("state")
            or p.get("name")
            or p.get("Propinsi")
            or "Tidak Diketahui"
        )

        key = normalize(nama_peta)
        d = data_dict.get(key)

        if d is not None:
            p.update({
                "state": nama_peta,
                "jumlah_peserta": int(d["Jumlah_Peserta"]),
                "bidang_unggulan": d["Bidang_Unggulan"],
                "bidang_terlemah": d["Bidang_Terlemah"],
                "color_status": "ada"
            })
        else:
            p.update({
                "state": nama_peta,
                "jumlah_peserta": 0,
                "bidang_unggulan": "-",
                "bidang_terlemah": "-",
                "color_status": "kosong"
            })

    m = folium.Map(
        location=[-2.5489, 118.0149],
        zoom_start=5,
        tiles="CartoDB positron"
    )

    geo_layer = folium.GeoJson(
        geojson_data,
        style_function=lambda f: {
            "fillColor": "#2a9d8f" if f["properties"]["color_status"] == "ada" else "#e9ecef",
            "color": "white",
            "weight": 1,
            "fillOpacity": 0.7 if f["properties"]["color_status"] == "ada" else 0.4
        },
        tooltip=folium.GeoJsonTooltip(
            fields=["state", "jumlah_peserta", "bidang_unggulan", "bidang_terlemah"],
            aliases=[
                "Provinsi:",
                "Total Peserta:",
                "Bidang Unggulan:",
                "Bidang Terlemah:"
            ],
            sticky=False
        )
    )

    geo_layer.add_to(m)

    #
    if provinsi and geojson_data["features"]:
        m.fit_bounds(geo_layer.get_bounds())

    #
    st.components.v1.html(
    m._repr_html_(),
    height=550,
    scrolling=False)


#Main Program 
st.subheader(f"Data Siswa OSN")
Table_Data(tahun , provinsi , df)
st.subheader("Grafik Bar")
Bar_Data(tahun , provinsi , df)
st.subheader("Grafik Pie")
Pie_Data(tahun , provinsi , df)
st.subheader("Peta Sebaran")
Map_Data(tahun , provinsi , df)