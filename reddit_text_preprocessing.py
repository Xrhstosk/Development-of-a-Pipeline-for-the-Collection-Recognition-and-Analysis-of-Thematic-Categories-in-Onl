import nltk
from nltk.corpus import stopwords
import re

# Φορτώνουμε τις ελληνικές "άχρηστες" λέξεις (stop-words)
nltk.download('punkt')      # Κατεβάζει τον αλγόριθμο χωρισμού προτάσεων
nltk.download('stopwords')
greek_stopwords = set(stopwords.words('greek'))

def clean_reddit_text(text):
    # 1. Μετατροπή σε μικρά
    text = text.lower()
    
    # 2. Αφαίρεση URLs και αγγλικών χαρακτήρων/noise
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    text = re.sub(r'[^\w\s]', '', text) # Αφαίρεση σημείων στίξης
    
    # 3. Tokenization (Σπάσιμο σε λέξεις)
    words = text.split()
    
    # 4. Αφαίρεση Stop-words
    cleaned_words = [w for w in words if w not in greek_stopwords]
    
    return " ".join(cleaned_words)

# Παράδειγμα εφαρμογής στο δείγμα μας
sample_post = "Η κατάσταση στο Μεταξουργείο είναι επικίνδυνη! Δεν έχει φώτα και φοβάμαι."
print(clean_reddit_text(sample_post))
# Έξοδος: "κατάσταση μεταξουργείο επικίνδυνη φώτα φοβάμαι"