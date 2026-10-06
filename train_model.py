
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# ==========================================
# LOAD DATASET
# ==========================================

data = pd.read_csv("reviews.csv")

print("Columns in dataset:")
print(data.columns.tolist())


# ==========================================
# CHANGE THESE TWO NAMES IF NEEDED
# ==========================================

TEXT_COLUMN = "review"
LABEL_COLUMN = "label"


# ==========================================
# REMOVE EMPTY VALUES
# ==========================================

data = data.dropna(
    subset=[TEXT_COLUMN, LABEL_COLUMN]
)


# Convert to string

data[TEXT_COLUMN] = data[TEXT_COLUMN].astype(str)
data[LABEL_COLUMN] = data[LABEL_COLUMN].astype(str)


# ==========================================
# SHOW LABELS
# ==========================================

print("\nLabels found:")
print(data[LABEL_COLUMN].value_counts())


# ==========================================
# INPUT AND OUTPUT
# ==========================================

X = data[TEXT_COLUMN]
y = data[LABEL_COLUMN]


# ==========================================
# TRAIN / TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# ==========================================
# TF-IDF
# ==========================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    max_features=10000,
    min_df=2
)


X_train_tfidf = vectorizer.fit_transform(X_train)

X_test_tfidf = vectorizer.transform(X_test)


# ==========================================
# MODEL
# ==========================================

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)


model.fit(
    X_train_tfidf,
    y_train
)


# ==========================================
# TEST MODEL
# ==========================================

predictions = model.predict(
    X_test_tfidf
)


accuracy = accuracy_score(
    y_test,
    predictions
)


print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions
    )
)


# ==========================================
# SAVE MODEL
# ==========================================

with open("model.pkl", "wb") as file:
    pickle.dump(model, file)


with open("vectorizer.pkl", "wb") as file:
    pickle.dump(vectorizer, file)


print("\n==============================")
print("SUCCESS")
print("==============================")

print("model.pkl created")
print("vectorizer.pkl created")
