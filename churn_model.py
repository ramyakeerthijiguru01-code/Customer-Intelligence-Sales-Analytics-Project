import pandas as pd


### Load Rfm data

rfm = pd.read_csv("Data/Processed/rfm.csv")
print(rfm.head())

## Create Target Variable

rfm["churn"] = rfm["recency"].apply(lambda x: 1 if x > 90 else 0)

print(rfm["churn"].value_counts())

## recency > 90 → churn = 1
## recency ≤ 90 → churn = 0

##  Split Data
from sklearn.model_selection import train_test_split

X = rfm[["recency", "frequency", "monetary"]]
y = rfm["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train size:", X_train.shape)
print("Test size:", X_test.shape)

## Train model

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

print("Model trained successfully")

## Predict

y_pred = model.predict(X_test)

## Evaluate model

from sklearn.metrics import accuracy_score, classification_report

print("Accuracy:", accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))


## Feature Importanvce
import pandas as pd

importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

print("\nFeature Importance:")
print(importance.sort_values(by="importance", ascending=False))

## Save model

import joblib

joblib.dump(model, "Data/Processed/churn_model.pkl")

print("Model saved")

# Add predictions to dataframe
rfm["predicted_churn"] = model.predict(X)

# Save file
rfm.to_csv("Data/Processed/rfm_predictions.csv", index=False)

print("Predictions saved")