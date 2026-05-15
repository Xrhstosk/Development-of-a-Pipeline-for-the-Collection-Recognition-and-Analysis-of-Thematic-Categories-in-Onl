import pandas as pd
import nltk
from nltk.corpus import stopwords
import re

# 1. Προετοιμασία NLP
nltk.download('stopwords', quiet=True)
greek_stopwords = set(stopwords.words('greek'))

def clean_text(text):
    if pd.isna(text): return "" # Διαχείριση κενών κελιών
    text = text.lower()
    text = re.sub(r'http\S+|www\S+|[^\w\s]', '', text)
    words = text.split()
    cleaned = [w for w in words if w not in greek_stopwords]
    return " ".join(cleaned)

# 2. Φόρτωση Δεδομένων
# Εδώ θα διάβαζε το αρχείο σου: df = pd.read_csv("reddit_sample.csv")
# Για το παράδειγμα, φτιάχνουμε ένα μικρό DataFrame
# Αντί για το data = {...}, γράψε:
df = pd.read_csv("reddit_sample.csv")

# Ο υπόλοιπος κώδικας παραμένει ίδιος!
df['cleaned_text'] = df['raw_text'].apply(clean_text)
df.to_csv("reddit_cleaned_data.csv", index=False)

#???χ
df = pd.DataFrame(data)

# 3. Εφαρμογή του Καθαρισμού σε ΟΛΕΣ τις σειρές
print("Ξεκινάει ο καθαρισμός...")
df['cleaned_text'] = df['raw_text'].apply(clean_text)

# 4. Αποθήκευση του αποτελέσματος
df.to_csv("reddit_cleaned_data.csv", index=False)

print("Επιτυχία! Δες τις πρώτες γραμμές:")
print(df[['raw_text', 'cleaned_text']].head())