from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import json
import csv

app = Flask(__name__)
CORS(app)

# Load the dataset
df = pd.read_csv('disease_data.csv')

# Separate features and target
X = df.drop('disease', axis=1)
y = df['disease']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train the logistic regression model
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# Load the remedies data
with open('remedies.json', 'r') as f:
    remedies = json.load(f)

def get_symptoms():
    symptoms = set()
    with open('disease_data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            for symptom, value in row.items():
                if symptom != 'disease' and int(value) == 1:
                    symptoms.add(symptom)
    return list(symptoms)

@app.route('/symptoms', methods=['GET'])
def symptoms():
    symptoms = get_symptoms()
    return jsonify(symptoms)

@app.route('/predict', methods=['POST'])
def predict():
    symptoms = request.json['symptoms']
    symptoms_data = {symptom: 1 if symptom in symptoms else 0 for symptom in X.columns}
    symptoms_df = pd.DataFrame([symptoms_data])
    symptoms_scaled = scaler.transform(symptoms_df)
    prediction = model.predict(symptoms_scaled)
    return jsonify({'disease': prediction[0]})

@app.route('/remedies', methods=['POST'])
def get_remedies():
    disease = request.json['disease']
    remedy = remedies.get(disease, "No remedies found for this disease.")
    return jsonify({'remedy': remedy})

if __name__ == '__main__':
    app.run(debug=True)