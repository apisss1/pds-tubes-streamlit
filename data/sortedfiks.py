import pandas as pd

df = pd.read_csv("data_latlong_prov.csv")

#Sorted data
df = df.drop_duplicates(subset=["Nama Peserta"])
df = df[df["Tahun"].isin([2022,2023, 2024])]
df = df[df["Jenjang Sekolah"].str.contains("SMA", na=False)]
df = df.dropna(subset=["Kelas","Latitude","Longitude"])

#
df = df.reset_index(drop=True)
df["No"] = range(1, len(df) + 1) 

#Convert data
df.to_csv("data/osn_fiks.csv", index=False)

print("Jumlah data final:", len(df))