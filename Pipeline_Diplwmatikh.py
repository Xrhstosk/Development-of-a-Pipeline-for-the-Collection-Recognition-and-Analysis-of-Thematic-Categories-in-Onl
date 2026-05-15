import requests
import pandas as pd
import time

# Βάλε εδώ το δικό σου Google API Key
API_KEY = "AIzaSyBDt8U1vJFqyPSE4j2yYJFdHI73YO7CT3g"

# Λίστα με τοποθεσίες που υπάρχουν και στο OSM για να έχουμε ταύτιση
locations = [
    # --- ΑΘΗΝΑ ---
    {"name": "National Garden", "city": "Athens"},
    {"name": "Pedion tou Areos", "city": "Athens"},
    {"name": "Philopappos Hill", "city": "Athens"},
    {"name": "Syntagma Square", "city": "Athens"},
    {"name": "Monastiraki Square", "city": "Athens"},
    {"name": "Acropolis Museum", "city": "Athens"},
    {"name": "Plaka District", "city": "Athens"},
    {"name": "Psyri", "city": "Athens"},
    {"name": "Lycabettus Hill", "city": "Athens"},
    {"name": "Stavros Niarchos Foundation", "city": "Athens"},
    {"name": "Omonia Square", "city": "Athens"},
    {"name": "Thiseio", "city": "Athens"},
    {"name": "Technopolis City of Athens", "city": "Athens"},
    {"name": "Mount Hymettus", "city": "Athens"},
    {"name": "Piraeus Port", "city": "Athens"},
    {"name": "Flisvos Marina", "city": "Athens"},
    {"name": "Zappeion Hall", "city": "Athens"},
    {"name": "Academy of Athens", "city": "Athens"},

    # --- ΘΕΣΣΑΛΟΝΙΚΗ ---
    {"name": "White Tower", "city": "Thessaloniki"},
    {"name": "Aristotelous Square", "city": "Thessaloniki"},
    {"name": "Navarinou Square", "city": "Thessaloniki"},
    {"name": "Nea Paralia", "city": "Thessaloniki"},
    {"name": "Ano Poli", "city": "Thessaloniki"},
    {"name": "Rotunda", "city": "Thessaloniki"},
    {"name": "Arch of Galerius Kamara", "city": "Thessaloniki"},
    {"name": "Ladadika", "city": "Thessaloniki"},
    {"name": "Church of Saint Demetrius", "city": "Thessaloniki"},
    {"name": "Kapani Market", "city": "Thessaloniki"},
    {"name": "Helexpo TIF", "city": "Thessaloniki"},
    {"name": "Agias Sofias Square", "city": "Thessaloniki"}
]

all_reviews = []

def get_place_id(name, city):
    search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": f"{name} {city}",
        #Ενημερώνουμε τη Google ότι αυτό που της στέλνουμε στο input είναι απλό, ελεύθερο κείμενο
        "inputtype": "textquery",
        #Θέλω ΜΟΝΟ το place_id (το αναγνωριστικό) και το geometry (δηλαδή το Latitude και το Longitude)".   
        "fields": "place_id,geometry",
        "key": API_KEY
    }
    #requests.get: Είναι η μέθοδος της βιβλιοθήκης requests που στέλνει ένα αίτημα στον server της Google. params: Είναι οι παράμετροι που "κολλάνε" στο URL
    #.json(): Η Google σου απαντάει με ένα τεράστιο κείμενο σε μορφή JSON. Αυτή η μέθοδος το μετατρέπει αυτόματα σε Python Dictionary, ώστε να μπορείς να γράψεις response["results"
    response = requests.get(search_url, params=params).json()
    if response.get("candidates"):
        return response["candidates"][0]["place_id"], response["candidates"][0]["geometry"]["location"]
    return None, None

#Συνάρτησης get_reviews
def get_reviews(place_id, city_name, place_name):
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,reviews,rating",
        "reviews_lang": "el", # Ζητάμε ελληνικές κριτικές
        "key": API_KEY
    }
    response = requests.get(details_url, params=params).json()
    # Ψάξε μέσα στο response να βρεις το κλειδί "result" , αν δεν το βρεις δωσε πισω ενα κενο( γιανα μην κρασαρει)
    result = response.get("result", {})
    #κοιτάζει μέσα στο result (που απομονώσαμε στην προηγούμενη γραμμή) και ψάχνει το κλειδί "reviews"
    reviews = result.get("reviews", [])
    
    output = []
    for r in reviews:
        # στην metablhth output ,pros8ese ta parakatw , ayto shmnainei append
        output.append({
            "City": city_name,
            "Place": place_name,
            "Author": r.get("author_name"),
            "Rating": r.get("rating"),
            "Text": r.get("text"),
            "Time": r.get("relative_time_description"),
            "Source": "Google"
        })
    return output

# Κύριο Loop συλλογής
for loc in locations:
    print(f"Αναζήτηση ID για: {loc['name']}...")
    p_id, coords = get_place_id(loc['name'], loc['city'])
    
    if p_id:
        print(f"Λήψη κριτικών για: {loc['name']}...")
        reviews = get_reviews(p_id, loc['city'], loc['name'])
        all_reviews.extend(reviews)
        time.sleep(1) # Delay για το rate limit
    else:
        print(f"Δεν βρέθηκε το: {loc['name']}")

# Αποθήκευση
if all_reviews:
    df_google = pd.DataFrame(all_reviews)
    df_google.to_csv("Google_Aligned_Reviews.csv", index=False, encoding="utf-8-sig")
    print(f"Ολοκληρώθηκε! Συλλέχθηκαν {len(df_google)} κριτικές για τις κοινές τοποθεσίες.")