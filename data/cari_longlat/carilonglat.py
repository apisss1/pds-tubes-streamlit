import pandas as pd
from geopy.geocoders import Nominatim
import time

df = pd.read_csv("osn_2022_2024.csv")

# Siapkan kolom dulu
df['Latitude'] = None
df['Longitude'] = None

geolocator = Nominatim(user_agent="geo_peserta")

def get_lat_long(query):
    try:
        print("Mencari:", query)
        loc = geolocator.geocode(query, timeout=10)
        time.sleep(1)
        if loc:
            return loc.latitude, loc.longitude
        return None, None
    except Exception as e:
        print("Error:", e)
        return None, None

for i, row in df.iterrows():
    query = f"{row['Provinsi']}, Indonesia"
    lat, lon = get_lat_long(query)
    df.at[i, 'Latitude'] = lat
    df.at[i, 'Longitude'] = lon

    # SIMPAN SETIAP 10 BARIS
    if i % 10 == 0:
        df.to_csv("data_latlong_prov.csv", index=False)
        print(f"Disimpan sampai baris {i}")

# Simpan final
df.to_csv("data_latlong.csv", index=False)
print("Selesai total ")
