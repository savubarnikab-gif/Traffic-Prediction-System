import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("ADAS Mobility Data.csv")

# Create traffic labels
def traffic_label(speed):
    if speed > 50:
        return "Low"
    elif speed >= 30:
        return "Medium"
    else:
        return "Heavy"

df['Traffic'] = df['Speed'].apply(traffic_label)

# Convert time into hour
df['Hour'] = pd.to_datetime(df['Time']).dt.hour

# Encode alert column
encoder = LabelEncoder()
df['AlertEncoded'] = encoder.fit_transform(df['Alert'])

# Features
X = df[['Hour', 'Lat', 'Long', 'AlertEncoded', 'Speed']]

# Target
y = df['Traffic']

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Prediction function
def predict_traffic(hour, lat, longi, alert, speed):

    try:
        alert_encoded = encoder.transform([alert])[0]
    except:
        alert_encoded = 0

    prediction = model.predict([
        [hour, lat, longi, alert_encoded, speed]
    ])

    return prediction[0]