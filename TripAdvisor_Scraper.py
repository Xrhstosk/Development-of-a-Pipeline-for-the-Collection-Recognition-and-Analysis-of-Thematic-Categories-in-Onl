from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Το URL για το Electra Palace
url = "https://www.booking.com/hotel/gr/electrapalacehotelathens.el.html?aid=304142&label=gen173nr-10CBkoggI46AdICFgEaFyIAQGYATO4ARfIAQzYAQPoAQH4AQGIAgGoAgG4Ar2vn84GwAIB0gIkZmI4MjVkZTctOGFkYy00ZjlhLWIyMzMtMmVhMzUzYmQ2OTc12AIB4AIB&sid=39566560708d9afe84dfdf781f4a04c0&dest_id=95602&dest_type=hotel&dist=0&group_adults=2&group_children=0&hapos=1&hpos=1&no_rooms=1&req_adults=2&req_children=0&room1=A%2CA&sb_price_type=total&sr_order=popularity&srepoch=1774704584&srpvid=0b1e5ee2738a08a1&type=total&ucfs=1&#tab-reviews"

print("--- ΕΝΑΡΞΗ ΤΕΛΙΚΗΣ ΣΥΛΛΟΓΗΣ ---")

try:
    driver.get(url)
    
    print("\nΚΡΙΣΙΜΑ ΒΗΜΑΤΑ:")
    print("1. Πάτα 'Αποδοχή' στα Cookies.")
    print("2. ΣΚΡΟΛΑΡΕ αργά μέχρι κάτω να δεις τις κριτικές (να εμφανιστούν στην οθόνη).")
    print("3. Πάτα το κουμπί 'Διαβάστε όλα τα σχόλια' αν το δεις.")
    input("4. Μόλις βλέπεις τα κείμενα των κριτικών, πάτα ENTER εδώ...")

    # Χρησιμοποιούμε JavaScript για να πάρουμε όλα τα κείμενα που έχουν το σωστό data-testid
    # Αυτό παρακάμπτει πολλά προβλήματα του Selenium
    script = "return Array.from(document.querySelectorAll('[data-testid=\"review-body\"]')).map(el => el.innerText);"
    reviews_text = driver.execute_script(script)
    
    all_data = []
    
    for text in reviews_text:
        clean_text = text.strip()
        if len(clean_text) > 15:
            print(f"Συλλέχθηκε: {clean_text[:50]}...")
            all_data.append({
                'Hotel': 'Electra Palace',
                'Source': 'Booking',
                'Review_Text': clean_text,
                'Traveler_Type': 'Ζευγάρι'
            })

    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv('Booking_Electra_Final_Success.csv', index=False, encoding='utf-8-sig')
        print(f"\nΝΙΚΗ! Μαζεύτηκαν {len(all_data)} κριτικές.")
    else:
        print("\nΑποτυχία. Η σελίδα κρύβει τα στοιχεία. Δοκίμασε να πατήσεις 'Ανανέωση' (F5) και ξαναπροσπάθησε.")

except Exception as e:
    print(f"Σφάλμα: {e}")

finally:
    print("Κλείσιμο σε 5 δευτερόλεπτα...")
    time.sleep(5)
    driver.quit()