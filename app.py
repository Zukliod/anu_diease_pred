from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

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

@app.route('/symptoms', methods=['GET'])
def get_symptoms():
    symptoms = X.columns.tolist()
    return jsonify(symptoms)

@app.route('/predict', methods=['POST'])
def predict():
    symptoms = request.json['symptoms']
    symptoms_data = {symptom: 1 if symptom in symptoms else 0 for symptom in X.columns}
    symptoms_df = pd.DataFrame([symptoms_data])
    symptoms_scaled = scaler.transform(symptoms_df)
    prediction = model.predict(symptoms_scaled)
    return jsonify({'disease': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)