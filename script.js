console.log("Script loaded");

let symptomCount = 0;

const symptomBoxesContainer = document.getElementById('symptom-boxes');
const resultDiv = document.getElementById('result');
const addSymptomButton = document.getElementById('addSymptomButton');
const predictButton = document.getElementById('predictButton');

// Fetch symptoms from the backend
fetch('http://127.0.0.1:5000/symptoms')
    .then(response => response.json())
    .then(symptoms => {
        console.log("Symptoms fetched:", symptoms); // Add this line to check if symptoms are fetched
        // Add initial symptom boxes
        for (let i = 0; i < 3; i++) {
            addSymptomBox(symptoms);
        }

        // Event listener for adding a new symptom box
        addSymptomButton.addEventListener('click', () => {
            console.log("Add Symptom button clicked"); // Add this line to check if button is clicked
            addSymptomBox(symptoms);
        });

        // Event listener for predicting disease
        predictButton.addEventListener('click', () => {
            console.log("Predict button clicked"); // Add this line to check if button is clicked
            const selectedSymptoms = Array.from(document.querySelectorAll('select')).map(select => select.value);
            predictDisease(selectedSymptoms);
        });
    })
    .catch(error => {
        console.error('Error fetching symptoms:', error);
    });

function addSymptomBox(symptoms) {
    const div = document.createElement('div');
    div.className = 'symptom-box';

    const select = document.createElement('select');
    const defaultOption = document.createElement('option');
    defaultOption.textContent = 'Select a symptom';
    defaultOption.disabled = true;
    defaultOption.selected = true;
    select.appendChild(defaultOption);

    symptoms.forEach(symptom => {
        const option = document.createElement('option');
        option.value = symptom;
        option.textContent = symptom;
        select.appendChild(option);
    });

    div.appendChild(select);
    symptomBoxesContainer.appendChild(div);
}

function predictDisease(selectedSymptoms) {
    console.log("Selected symptoms:", selectedSymptoms); // Add this line to check selected symptoms
    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ symptoms: selectedSymptoms })
    })
    .then(response => response.json())
    .then(data => {
        console.log("Prediction result:", data); // Add this line to check the prediction result
        resultDiv.textContent = `The predicted disease is: ${data.disease}`;
    })
    .catch(error => {
        console.error('Error:', error);
        resultDiv.textContent = 'An error occurred during prediction.';
    });
}
