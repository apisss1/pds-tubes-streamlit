import pandas as pd

df = pd.read_csv("data_latlong.csv")

# Hapus index lama
df = df.drop(columns=["Unnamed: 0"], errors="ignore")

# Sort & filter data
df = df.drop_duplicates(subset=["Nama Peserta"])
df = df[df["Tahun"].isin([2022, 2023, 2024])]
df = df[df["Jenjang Sekolah"].str.contains("SMA", na=False)]
df = df.dropna(subset=["Kelas", "Latitude", "Longitude"])

# Reset index
df = df.reset_index(drop=True)

# Nomor di AWAL
df.insert(0, "No", range(1, len(df) + 1))

# Simpan ulang
df.to_csv("data_hapus_isi_kosong.csv", index=False)

print("Jumlah data final:", len(df))
