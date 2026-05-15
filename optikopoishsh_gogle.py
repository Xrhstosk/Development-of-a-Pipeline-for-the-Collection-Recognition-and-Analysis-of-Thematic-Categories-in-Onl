import folium
from folium.plugins import MarkerCluster
import pandas as pd

# 1. Φόρτωση των δεδομένων
try:
    df = pd.read_csv("Enhanced_Safety_Dataset.csv")
    print("Το αρχείο φορτώθηκε επιτυχώς!")
except:
    print("Σφάλμα: Δεν βρέθηκε το αρχείο Enhanced_Safety_Dataset.csv")
    exit()

# Συντεταγμένες για το κέντρο των χαρτών
coords = {
    "Athens": [37.9838, 23.7275],
    "Thessaloniki": [40.6401, 22.9444]
}

# Χρώματα για τις βασικές κατηγορίες
color_map = {
    'park': 'green',
    'police': 'red',
    'hospital': 'darkred',
    'pharmacy': 'blue',
    'bench': 'gray',
    'bus_stop': 'orange',
    'attraction': 'purple'
}

#Η μέθοδος .items() είναι μια εντολή που λέει στην Python:
#"Πάρε αυτό το λεξικό και "σπάσε" το σε ζευγάρια, ώστε να μπορώ να δω και το όνομα (Key) και τις συντεταγμένες (Value) ταυτόχρονα
for city, center in coords.items():
    print(f"Δημιουργία χάρτη για: {city}...")
    
    # Δημιουργία του χάρτη
    m = folium.Map(location=center, zoom_start=13, tiles="cartodbpositron")
    
    #το MarkerCluster είναι ένα instance μιας κλάσης από το namespace folium.plugins. Λειτουργεί ως ένας wrapper πάνω από τη JavaScript βιβλιοθήκη Leaflet.
    #Η λογική του "Parent-Child" (add_to) μ γονεας , marker_cluster παιδι
    # Χρήση Κλάση Cluster ανήκει σε ένα Plugin (πρόσθετο) της βιβλιοθήκης folium (για να μην "μπουκώνει" ο χάρτης με 13.000 σημεία) μετηοδοσ add_to()
    marker_cluster = MarkerCluster().add_to(m)
    
    # Φιλτράρουμε τα δεδομένα για την πόλη / Η Γραμμή df[df['City'] == city]: Αυτό λέγεται Boolean Indexing. Η Pandas δημιουργεί μια προσωρινή λίστα από "True/False" 
    # για κάθε γραμμή (True αν η πόλη είναι η Αθήνα, False αν όχι)  και κρατάει μόνο τις γραμμές που είναι True. Έτσι, το city_data είναι ένα "υπο-σύνολο" (subset)
    city_data = df[df['City'] == city]

    # Το iterrows() (Το εργαλείο): Είναι μια γεννήτρια (generator).ΠΑΡΑΓΕΙ (ενα tuple ζευγάρι δεδομένων) Τον αριθμό της γραμμής (Index). Τα περιεχόμενα της γραμμής (Series).
    #ο idx (Index): Είναι η μεταβλητή που δέχεται τον αριθμό της γραμμής (π.χ. 0, 1, 2...).
    #Το row (Row): Είναι η μεταβλητή που δέχεται όλα τα δεδομένα εκείνης της γραμμής (Name, Category, Lat, Lon
    for idx, row in city_data.iterrows():
        # Επιλογή χρώματος βάση κατηγορίας
        color = color_map.get(row['Category'], 'blue')
        
        folium.CircleMarker(
            #λατ= πλατος λον= μηκος
            location=[row['Lat'], row['Lon']],
            #5 πιχλεσ 
            radius=5,
            popup=f"<b>{row['Name']}</b><br>Type: {row['Category']}",
            color=color,
            fill=True,
            fill_color=color
        ).add_to(marker_cluster)
    
    # Αποθήκευση του χάρτη
    file_name = f"map_{city.lower()}.html"
    m.save(file_name)
    print(f"Ο χάρτης αποθηκεύτηκε ως {file_name}")

print("\nΔιαδικασία ολοκληρώθηκε! Άνοιξε τα αρχεία HTML στον browser σου.")