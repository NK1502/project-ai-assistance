from flask import Flask, render_template, request
import math

app = Flask(__name__)

# Simulated Bank interest rates (can be connected to real APIs later)
BANK_INTEREST_RATES = {
    "SBI": 8.4,
    "HDFC": 9.1,
    "ICICI": 8.8,
    "Axis Bank": 9.0,
    "Punjab National Bank": 8.5,
    "Bank of Baroda": 8.6
}

# Caste-based Government schemes
CASTE_SCHEMES = {
    "SC": ["✅ Dr. Ambedkar Central Sector Scheme for Interest Subsidy", "✅ National Overseas Scholarship Scheme"],
    "ST": ["✅ Top Class Education Scholarship", "✅ National Fellowship for Higher Education"],
    "OBC": ["✅ Central Sector Scheme for OBCs", "✅ NBCFDC Loan Assistance"],
    "General": ["✅ No caste-based schemes, check income-based subsidies"],
    "EWS": ["✅ EWS Quota: Special education loan subsidy and scholarships"]
}

def calculate_emi(principal, rate, time_years):
    monthly_rate = rate / (12 * 100)
    time_months = time_years * 12
    emi = (principal * monthly_rate * (math.pow(1 + monthly_rate, time_months))) / (math.pow(1 + monthly_rate, time_months) - 1)
    return round(emi, 2)

def suggest_strategies(income, expenses, loan_amount, loan_duration, interest_rate):
    emi = calculate_emi(loan_amount, interest_rate, loan_duration)
    surplus = income - expenses

    strategies = []

    if surplus > emi:
        strategies.append("✅ You can easily afford EMI payments. Stick to the standard plan.")
    else:
        strategies.append("⚠️ EMI exceeds your surplus. Consider negotiating loan tenure or seeking subsidies.")

    if surplus - emi > emi * 0.5:
        strategies.append("💡 You can prepay loans to reduce total interest paid.")

    if income < expenses:
        strategies.append("🛑 Expenses exceed income. Focus on cost-cutting before taking a big loan.")

    if interest_rate > 9:
        strategies.append("📈 High-interest loan! Try to refinance after 2 years if rates drop.")

    return emi, strategies

@app.route('/')
def home():
    banks = list(BANK_INTEREST_RATES.keys())
    castes = list(CASTE_SCHEMES.keys())
    return render_template('index.html', banks=banks, castes=castes)

@app.route('/predict', methods=['POST'])
def predict():
    bank = request.form['bank']
    loan_amount = float(request.form['loan_amount'])
    loan_period = float(request.form['loan_period'])
    family_income = float(request.form['family_income'])
    family_expenses = float(request.form['family_expenses'])
    caste = request.form['caste']

    # Get bank interest rate
    interest_rate = BANK_INTEREST_RATES.get(bank, 9.0)  # default 9% if bank not found

    emi, strategies = suggest_strategies(family_income, family_expenses, loan_amount, loan_period, interest_rate)

    # Get government schemes
    schemes = CASTE_SCHEMES.get(caste, ["No specific schemes found."])

    return render_template('result.html', emi=emi, strategies=strategies, schemes=schemes, interest_rate=interest_rate, bank=bank)

if __name__ == '__main__':
    app.run(debug=True)
