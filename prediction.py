import sqlite3
import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# ---------------------------------
# Create models folder if needed
# ---------------------------------
os.makedirs("models", exist_ok=True)

# ---------------------------------
# Connect to SQLite Database
# ---------------------------------
conn = sqlite3.connect("analytics.db")

# Read sales table
df = pd.read_sql("SELECT * FROM sales", conn)

conn.close()

# ---------------------------------
# Check Data
# ---------------------------------
print("\nFirst 5 Records:\n")
print(df.head())

# ---------------------------------
# Features & Target
# ---------------------------------
X = df[["Quantity", "Price"]]
y = df["Total"]

# ---------------------------------
# Split Data
# ---------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ---------------------------------
# Train Model
# ---------------------------------
model = LinearRegression()

model.fit(X_train, y_train)

# ---------------------------------
# Evaluate Model
# ---------------------------------
predictions = model.predict(X_test)

score = r2_score(y_test, predictions)

print(f"\nModel Accuracy (R²): {score:.2f}")

# ---------------------------------
# Save Model
# ---------------------------------
joblib.dump(model, "models/sales_model.pkl")

print("\n✅ Model saved successfully!")
print("Location: models/sales_model.pkl")

# ---------------------------------
# Test Prediction
# ---------------------------------
sample_quantity = 2
sample_price = 100

prediction = model.predict([[sample_quantity, sample_price]])

print(f"\nSample Prediction")
print(f"Quantity: {sample_quantity}")
print(f"Price: ${sample_price}")
print(f"Predicted Revenue: ${prediction[0]:.2f}")