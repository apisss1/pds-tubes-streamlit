import pandas as pd

df = pd.read_csv("osn.csv")

df = df[df["Tahun"].isin([2022, 2023, 2024])]

df = df[df["Jenjang Sekolah"].str.contains("SMA", na=False)]

df = df.drop(columns=["Prize Tambahan"])

df.to_csv("osn_2022_2024.csv", index=False)

print("Jumlah data final:", len(df))
