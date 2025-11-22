import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from math import radians, sin, cos, sqrt, atan2

# ----------------------------------------------------------
# 1. Charger le fichier Excel
# ----------------------------------------------------------
input_file = "Distance.xlsx"   # Mets ici ton fichier
df = pd.read_excel(input_file)

# ----------------------------------------------------------
# 2. Fonction Haversine pour calculer la distance en km
# ----------------------------------------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon Terre en km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

# ----------------------------------------------------------
# 3. Initialiser le géocodeur Nominatim
# ----------------------------------------------------------
geolocator = Nominatim(user_agent="distance_calculator")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# ----------------------------------------------------------
# 4. Fonction pour géocoder une commune
# ----------------------------------------------------------
def get_coordinates(commune):
    try:
        location = geocode(f"{commune}, Maroc")
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except:
        return None, None

# ----------------------------------------------------------
# 5. Géocodage des deux colonnes
# ----------------------------------------------------------
df["lat_boursier"], df["lon_boursier"] = zip(*df["Commune Boursier"].apply(get_coordinates))
df["lat_etab"], df["lon_etab"] = zip(*df["Commune Etablissement"].apply(get_coordinates))

# ----------------------------------------------------------
# 6. Calcul de la distance
# ----------------------------------------------------------
distances = []

for i, row in df.iterrows():
    if None in (row["lat_boursier"], row["lon_boursier"], row["lat_etab"], row["lon_etab"]):
        distances.append(None)
    else:
        d = haversine(row["lat_boursier"], row["lon_boursier"],
                      row["lat_etab"], row["lon_etab"])
        distances.append(round(d, 2))

df["Distance_km"] = distances

# ----------------------------------------------------------
# 7. Sauvegarde du résultat dans un nouveau fichier Excel
# ----------------------------------------------------------
output_file = "Distance_Resultat.xlsx"
df.to_excel(output_file, index=False)

print(f"Traitement terminé ! Fichier généré : {output_file}")
