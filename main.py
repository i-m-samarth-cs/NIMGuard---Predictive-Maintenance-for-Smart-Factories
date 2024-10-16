from flask import Flask, request, render_template
import pandas as pd
import joblib

app = Flask(_name_)

# Load the models and preprocessor
preprocessor = joblib.load('preprocessor.joblib')
label_encoder = joblib.load('label_encoder.joblib')
target_model = joblib.load('target_model.joblib')
failure_model = joblib.load('failure_model.joblib')
failure_encoder = joblib.load('failure_encoder.joblib')

def predict(air_temp, process_temp, rotational_speed, torque, tool_wear, type_value):
    # Create a DataFrame from the input parameters
    input_df = pd.DataFrame({
        'Air temperature [K]': [air_temp],
        'Process temperature [K]': [process_temp],
        'Rotational speed [rpm]': [rotational_speed],
        'Torque [Nm]': [torque],
        'Tool wear [min]': [tool_wear],
        'Type': [type_value]  # Example Type
    })

    # Add Combined_Temperature column
    input_df['Combined_Temperature'] = (input_df['Air temperature [K]'] + input_df['Process temperature [K]']) / 2

    # Encode the 'Type' column using the loaded label encoder
    input_df['Type'] = label_encoder.transform(input_df['Type'])

    # Prepare the input DataFrame for preprocessing
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

    # Create a DataFrame for processed input
    input_processed_df = pd.DataFrame(input_processed, columns=columns_to_process)

    # Predict target and failure type
    target_prediction = target_model.predict(input_processed_df)
    failure_prediction = failure_model.predict(input_processed_df)
    
    # Decode the target and failure predictions if needed
    target_prediction_decoded = target_prediction
    failure_prediction_decoded = failure_encoder.inverse_transform(failure_prediction)

    return target_prediction_decoded, failure_prediction_decoded

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
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

    return render_template('index.html')

if _name_ == '_main_':
    app.run(debug=True)