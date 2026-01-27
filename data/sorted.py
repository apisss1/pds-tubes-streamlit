import pandas as pd

df = pd.read_csv("data/osn_fiks.csv")

#Sorte data
df = df[df["Tahun"].isin([2022, 2023, 2024])]
df = df[df["Jenjang Sekolah"].str.contains("SMA", na=False)]
#Delete data column
df = df.drop(columns=["Kelas","Latitude" , "Longitude"])
#
df = df.reset_index(drop=True)
df["No"] = range(1, len(df) + 1) 
#Convert data
df.to_csv("data/osn_sorted.csv", index=False)

print("Jumlah data final:", len(df))