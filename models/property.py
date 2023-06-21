from PUMWANIHOUSES\connections import *

# Create a payments table if it doesn't exist
cur.execute('''CREATE TABLE IF NOT EXISTS payments
             (id SERIAL PRIMARY KEY,
             firstname varchar(20),
             lastname varchar(20), 
             transaction_id TEXT,
             amount REAL,
             date datetime.now())''')

@app.route('/submit', methods=['POST'])
def process_payment():
    data = request.get_json()
    
    # Extract the transaction details from the request
    firstname=request.form["firstname"]
    lastname=request.form["lastname"]
    transaction_id = data.get('transaction_id')
    amount = data.get('amount')
    date=datetime.now()
    
    # Perform necessary validation on the transaction details
    
    # Generate a payment request to Safaricom's API
    safaricom_response = make_payment_request(transaction_id, amount)
    
    if safaricom_response.status_code == 200:
        # Store the payment details in the database
        cur.execute("INSERT INTO payments VALUES (?,?,?,?,?)", (firstname,lastname,transaction_id, amount,date))
        conn.commit()
        
        # Return a success response
        return 'Payment processed successfully'
    else:
        # Handle payment failure
        return 'Payment failed'

def make_payment_request(transaction_id, amount):
    # Make a request to Safaricom's payment API
    url = 'https://safaricom-payment-api-url'  # Replace with the actual API URL
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN'  # Replace with your access token
    }
    payload = {
        'transaction_id': transaction_id,
        'amount': amount,
        'paybill_number': '888880'
        # Include any additional required parameters
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    return response