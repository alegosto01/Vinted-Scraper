import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib


sold_csv = "/home/ale/Desktop/Vinted-Web-Scraper/csv_definitivi/sold_items.csv"      # Update with your file path
not_sold_csv = "/home/ale/Desktop/Vinted-Web-Scraper/csv_definitivi/big_csv.csv"  # Update with your file path

# Features to use
features = ["Price", "Title", "Size", "Likes", "Brand"]

# Load datasets
sold_df = pd.read_csv(sold_csv, usecols=features)
not_sold_df = pd.read_csv(not_sold_csv, usecols=features)

# Add target column (1 = Sold, 0 = Not Sold)
sold_df["Sold"] = 1
not_sold_df["Sold"] = 0

# Combine both datasets
df = pd.concat([sold_df, not_sold_df], ignore_index=True)

# Handle missing values (fill with "Unknown" for categorical and median for numerical)
df["Brand"].fillna("Unknown", inplace=True)
df["Title"].fillna("Unknown", inplace=True)
df["Size"].fillna("Unknown", inplace=True)
df["Price"].fillna(df["Price"].median(), inplace=True)
df["Likes"].fillna(df["Likes"].median(), inplace=True)

# Encode categorical variables
label_encoders = {}
for col in ["Title", "Size", "Brand"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le  # Store encoders for future use

# Split data into features (X) and target (y)
X = df.drop(columns=["Sold"])
y = df["Sold"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scale numerical features
scaler = StandardScaler()
X_train[["Price", "Likes"]] = scaler.fit_transform(X_train[["Price", "Likes"]])
X_test[["Price", "Likes"]] = scaler.transform(X_test[["Price", "Likes"]])

# === Class Imbalance Handling ===

# ✅ 1. Apply SMOTE (Oversampling class 1)
smote = SMOTE(random_state=42)
X_train, y_train = smote.fit_resample(X_train, y_train)

# ✅ 2. Apply Undersampling (Reduce class 0)
under = RandomUnderSampler(random_state=42)
X_train, y_train = under.fit_resample(X_train, y_train)

# ✅ 3. Train a Random Forest model with class weighting
model = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
# ✅ Alternative: Train an XGBoost model with imbalance handling
# model = XGBClassifier(scale_pos_weight=len(y_train[y_train == 0]) / len(y_train[y_train == 1]))

model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Model Accuracy: {accuracy:.4f}")
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save the model and preprocessors
joblib.dump(model, "sold_prediction_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(label_encoders, "label_encoders.pkl")

print("\n🚀 Model and preprocessors saved!")
