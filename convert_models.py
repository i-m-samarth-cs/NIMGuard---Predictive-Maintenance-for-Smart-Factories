# from skl2onnx import convert_sklearn, update_registered_converter
# from lightgbm import LGBMClassifier
# from skl2onnx.common.data_types import FloatTensorType
# import joblib

# # Register LGBMClassifier converter without specifying inputs
# update_registered_converter(
#     LGBMClassifier,
#     'LGBMClassifier',
#     outputs=[('output', FloatTensorType([None, 1]))]
# )

# # Load your pre-trained model
# target_model = joblib.load('target_model.joblib')  # Ensure you have this model saved as a joblib file

# # Convert the model to ONNX format
# initial_type = [('input', FloatTensorType([None, target_model.n_features_in_]))]
# onnx_target_model = convert_sklearn(target_model, initial_types=initial_type)

# # Save the ONNX model
# with open("model.onnx", "wb") as f:
#     f.write(onnx_target_model.SerializeToString())

# print("Model successfully converted to ONNX format and saved as 'model.onnx'.")
