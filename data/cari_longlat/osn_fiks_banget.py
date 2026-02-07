import pandas as pd


df = pd.read_csv("data_hapus_isi_kosong.csv")


# 2. DAFTAR PROVINSI RESMI

provinsi_resmi = [
"Aceh","Sumatera Utara","Sumatera Barat","Riau","Jambi","Sumatera Selatan",
"Bengkulu","Lampung","Bangka Belitung","Kepulauan Riau",
"DKI Jakarta","Jawa Barat","Jawa Tengah","DI Yogyakarta","Jawa Timur",
"Banten","Bali","Nusa Tenggara Barat","Nusa Tenggara Timur",
"Kalimantan Barat","Kalimantan Tengah","Kalimantan Selatan","Kalimantan Timur","Kalimantan Utara",
"Sulawesi Utara","Sulawesi Tengah","Sulawesi Selatan","Sulawesi Tenggara","Gorontalo","Sulawesi Barat",
"Maluku","Maluku Utara","Papua","Papua Barat","Papua Selatan","Papua Tengah","Papua Pegunungan","Papua Barat Daya"
]


# 3. BERSIHKAN SPASI

df["Provinsi"] = df["Provinsi"].str.strip()


# 4. CEK DATA ANEH

prov_aneh = df.loc[~df["Provinsi"].isin(provinsi_resmi), "Provinsi"].unique()
print("Provinsi aneh yang ditemukan:", prov_aneh)


# 5. FILTER DATA RESMI

df_bersih = df[df["Provinsi"].isin(provinsi_resmi)].reset_index(drop=True)


# 6. PERBAIKI NOMOR URUT

df_bersih["No"] = range(1, len(df_bersih) + 1)


cols = ["No"] + [col for col in df_bersih.columns if col != "No"]
df_bersih = df_bersih[cols]


# 7. SIMPAN FILE BARU

df_bersih.to_csv("data_osn_fiks_banget.csv", index=False)

print("Data berhasil dibersihkan & nomor sudah berurutan!")
print("Jumlah data akhir:", len(df_bersih))
