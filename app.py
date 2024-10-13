from flask import Flask, request, render_template, jsonify
import pandas as pd
import requests
import joblib

app = Flask(__name__)

# Load the models and preprocessor
preprocessor = joblib.load('preprocessor.joblib')
label_encoder = joblib.load('label_encoder.joblib')
target_model = joblib.load('target_model.joblib')
failure_model = joblib.load('failure_model.joblib')
failure_encoder = joblib.load('failure_encoder.joblib')

# Function for predictive maintenance
def predict(air_temp, process_temp, rotational_speed, torque, tool_wear, type_value):
    try:
        # Create a DataFrame from the input parameters
        input_df = pd.DataFrame({
            'Air temperature [K]': [air_temp],
            'Process temperature [K]': [process_temp],
            'Rotational speed [rpm]': [rotational_speed],
            'Torque [Nm]': [torque],
            'Tool wear [min]': [tool_wear],
            'Type': [type_value]
        })

        # Add Combined_Temperature column
        input_df['Combined_Temperature'] = (input_df['Air temperature [K]'] + input_df['Process temperature [K]']) / 2

        # Encode the 'Type' column using the loaded label encoder
        input_df['Type'] = label_encoder.transform(input_df['Type'])

        # Select columns for preprocessing
        columns_to_process = ['Air temperature [K]', 
                              'Process temperature [K]', 
                              'Rotational speed [rpm]', 
                              'Torque [Nm]', 
                              'Tool wear [min]', 
                              'Combined_Temperature', 
                              'Type']

        # Apply the preprocessor
        input_processed = preprocessor.transform(input_df[columns_to_process])

        # Predict target and failure type
        target_prediction = target_model.predict(input_processed)
        failure_prediction = failure_model.predict(input_processed)
        
        # Decode failure prediction
        failure_prediction_decoded = failure_encoder.inverse_transform(failure_prediction)

        return target_prediction, failure_prediction_decoded

    except Exception as e:
        return str(e), str(e)

# Route for predictive maintenance predictions
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get input data from form
            air_temp = float(request.form['air_temp'])
            process_temp = float(request.form['process_temp'])
            rotational_speed = float(request.form['rotational_speed'])
            torque = float(request.form['torque'])
            tool_wear = float(request.form['tool_wear'])
            type_ = request.form['type']

            # Get predictions
            target, failure = predict(
                air_temp=air_temp,
                process_temp=process_temp,
                rotational_speed=rotational_speed,
                torque=torque,
                tool_wear=tool_wear,
                type_value=type_
            )

            return render_template('index.html', target=target, failure=failure)

        except ValueError:
            return "Invalid input data", 400

    return render_template('index.html')

# Route for the chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    # Get user input from JSON request
    user_input = request.json.get('message')

    if user_input:
        try:
            # Define the NIM API endpoint (replace the URL with your actual endpoint)
            nim_api_url = "https://integrate.api.nvidia.com/v1/chat/completions"

            # Prepare the payload for NIM service
            payload = {
                "model": "meta/llama-3.1-405b-instruct",
                "messages": [{"role": "user", "content": user_input}],
                "temperature": 0.2,
                "top_p": 0.7,
                "max_tokens": 1024
            }

            headers = {
                'Authorization': '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',  # Replace YOUR_API_KEY
                'Content-Type': 'application/json'
            }

            # Make the request to the NIM API
            response = requests.post(nim_api_url, json=payload, headers=headers)

            # Check if the request was successful
            if response.status_code == 200:
                response_data = response.json()
                chatbot_response = response_data['choices'][0]['message']['content']
                return jsonify({"response": chatbot_response})
            else:
                return jsonify({"response": "Failed to get a response from NIM API"}), 500

        except Exception as e:
            return jsonify({"response": str(e)}), 500

    else:
        return jsonify({"response": "No message received"}), 400

if __name__ == '__main__':
    app.run(debug=True)