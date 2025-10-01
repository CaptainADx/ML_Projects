from flask import Flask, render_template, request
import pickle
import math

app = Flask(__name__)

# Load Model
model = pickle.load(open("Loan_Prediction_Analysis.sav", "rb"))

# Mapping for categorical columns (matching LabelEncoder)
gender_map = {'male': 1, 'female': 0}
married_map = {'yes': 1, 'no': 0}
dependents_map = {'0': 0, '1': 1, '2': 2, '3+': 3}
education_map = {'graduate': 1, 'not graduate': 0}
self_employed_map = {'yes': 1, 'no': 0}
credit_history_map = {'yes': 1, 'no': 0}
property_area_map = {'rural': 0, 'urban': 1, 'semiurban': 2}

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', result='')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get values from form
        gender = request.form.get('gender', '').strip().lower()
        married = request.form.get('married', '').strip().lower()
        dependents = request.form.get('dependents', '0').strip()
        education = request.form.get('education', '').strip().lower()
        self_employed = request.form.get('self_employed', '').strip().lower()
        credit_history = request.form.get('credit_history', '').strip().lower()
        property_area = request.form.get('property_area', '').strip().lower()

        # Convert numerical inputs to log
        applicant_income = float(request.form.get('applicant_income', 0))
        loan_amount = float(request.form.get('loan_amount', 0))
        loan_amount_term = float(request.form.get('loan_amount_term', 0))

        applicant_income_log = math.log(applicant_income) if applicant_income > 0 else 0
        loan_amount_log = math.log(loan_amount) if loan_amount > 0 else 0
        loan_amount_term_log = math.log(loan_amount_term) if loan_amount_term > 0 else 0

        # Convert categorical to numerical
        gender_num = gender_map.get(gender, 0)
        married_num = married_map.get(married, 0)
        dependents_num = dependents_map.get(dependents, 0)
        education_num = education_map.get(education, 0)
        self_employed_num = self_employed_map.get(self_employed, 0)
        credit_history_num = credit_history_map.get(credit_history, 0)
        property_area_num = property_area_map.get(property_area, 0)

        # Prepare input for model
        features = [
            gender_num, married_num, dependents_num, education_num,
            self_employed_num, credit_history_num, property_area_num,
            applicant_income_log, loan_amount_log, loan_amount_term_log
        ]

        # Predict
        pred = model.predict([features])[0]
        result = "Approved" if pred == 1 else "Rejected"

    except Exception as e:
        result = f"Error: {str(e)}"

    return render_template('index.html',
                       gender=gender, married=married, dependents=dependents,
                       education=education, self_employed=self_employed,
                       credit_history=credit_history, property_area=property_area,
                       applicant_income=request.form.get('applicant_income', ''),
                       loan_amount=request.form.get('loan_amount', ''),
                       loan_amount_term=request.form.get('loan_amount_term', ''),
                       result=result)

if __name__ == "__main__":
    app.run(debug=True)
