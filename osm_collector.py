import requests
import pandas as pd
import time
import matplotlib.pyplot as plt

#γλώσσα Overpass QL.[out:json]: Λέμε στον server ότι θέλουμε την απάντηση σε μορφή JSON (όπως και στη Google).
#node["amenity"="police"](area_id);: Εδώ δίνουμε τις εντολές αναζήτησης.
#amenity=χρήσιμες εγκαταστάσεις ή υπηρεσίες ελευθερη μεταφραση- άνεση
#Namespace ή μια Κεντρική Κατηγορία / ομαδα μεταβλητων

url = "http://overpass-api.de/api/interpreter"

regions = {
    "Athens": "(37.85,23.60,38.10,23.85)",
    "Thessaloniki": "(40.58,22.90,40.68,23.00)"
}
#αποτρέπεται το rate-limiting και το αυτόματο IP blocking από τους μηχανισμούς anti-scraping του server, 
# ενώ παράλληλα διασφαλίζεται το traceability της εφαρμογής κατά το debugging.
headers = {'User-Agent': 'Diplomatiki_Pipeline_Project/2.0'}

all_data = []
#ισως all_data λειτουργεί ως ένας buffer (προσωρινή μνήμη).
for city, bbox in regions.items():
    print(f"Αντληση δεδομένων για: {city}...")
    # Προσθήκη τομέων Ασφάλειας και Υγείας
    query = f"""
    [out:json][timeout:60];
    (
      node["leisure"="park"]{bbox};
      node["tourism"="attraction"]{bbox};
      node["amenity"="police"]{bbox};
      node["amenity"="hospital"]{bbox};
      node["amenity"="pharmacy"]{bbox};
      node["amenity"="fire_station"]{bbox};
      node["amenity"="bench"]{bbox};
      node["highway"="bus_stop"]{bbox};
    );
    out body;
    """
    try:
        #Εδώ η Python στέλνει όλο το κείμενο του ερωτήματος στον server
        response = requests.get(url, params={'data': query}, headers=headers)
        if response.status_code == 200:
            elements = response.json().get('elements', [])
            for el in elements:
                tags = el.get('tags', {})
                p_type = tags.get('leisure') or tags.get('tourism') or tags.get('amenity') or tags.get('highway')
                
                # Pipeline Logic: Κατηγοριοποίηση
                name = tags.get('name')
                if not name:
                    name = f"Unnamed {p_type.replace('_', ' ').capitalize()}"
                
                all_data.append({
                    "City": city,
                    "Name": name,
                    "Category": p_type,
                    "Lat": el.get('lat'),
                    "Lon": el.get('lon')
                })
        time.sleep(2)
    except Exception as e: print(f"Σφάλμα: {e}")

if all_data:
    df = pd.DataFrame(all_data)
    df.to_csv("Enhanced_Safety_Dataset.csv", index=False, encoding="utf-8-sig")
    
    # ΔΗΜΙΟΥΡΓΙΑ ΓΡΑΦΗΜΑΤΟΣ
    print("\nΔημιουργία γραφήματος κατανομής δεδομένων...")
    plt.figure(figsize=(12, 6))
    df['Category'].value_counts().plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Κατανομή Δεδομένων ανά Κατηγορία (Pipeline Output)')
    plt.xlabel('Κατηγορία')
    plt.ylabel('Πλήθος Σημείων')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("data_distribution.png") # Αποθήκευση γραφήματος ως εικόνα
    print("Το γράφημα αποθηκεύτηκε ως 'data_distribution.png'")
    
    # Στατιστικά για την εργασία
    print("-" * 30)
    print("ΣΤΑΤΙΣΤΙΚΑ PIPELINE:")
    print(df.groupby(['City', 'Category']).size())