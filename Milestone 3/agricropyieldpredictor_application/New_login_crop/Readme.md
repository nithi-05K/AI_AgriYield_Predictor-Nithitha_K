🌾 AI-Based Crop Yield Predictor
This project is a Streamlit-based application that predicts crop yield using environmental and soil parameters.
It includes a secure login system, dataset processing, and a machine learning model for real-time prediction.

🎯 Project Objectives
Predict Crop Yield Accurately
Use machine learning to classify crop yield into High, Medium, or Low based on measurable parameters.

Enable User-Friendly Access
Provide a simple web interface where users can log in, input values, and instantly receive predictions.

Ensure Secure User Management
Implement a safe authentication system that stores passwords using SHA-256 hashing.

Support Multiple Crop Types
Handle predefined crop categories using numerical mapping for efficient model processing.

Provide Scalable Deployment Support
Structure files to allow deployment on platforms like Streamlit Community Cloud.

✅ Key Features
🔐 User Authentication
Login and signup system
Passwords stored securely using SHA-256 hashing
User records saved in data/users.csv

🤖 Machine Learning Prediction
Predicts yield category: High, Medium, or Low
Uses trained model stored in:
crop_yield_model.pkl
crop_yield_scaler.pkl

🌱 Crop Type Handling
Crop types mapped using:
crop_type_map.pkl
crop_yield_label_map.pkl

📥 Input Parameters Included

The user provides:
Rainfall
Temperature
Humidity
Soil pH
Soil Moisture
Nitrogen
Phosphorus
Potassium

Crop Type

📊 Dataset Integration
Original dataset included as your_dataset.csv
Used for:
matching existing values
mapping crop types

🔧 Technology Stack
Programming Language: Python
Framework: Streamlit
Machine Learning: Scikit-Learn
Data Handling: Pandas
Password Security: SHA-256 hashing
Model Persistence: Joblib
reference-based predictions

🎨 Modern UI
Streamlit interface
Background image styling
Three-column input layout
User-friendly parameter selection

📤 Output Provided
Predicted yield category:
High
Medium
Low
Displayed with a success message.

📂 Project Folder Structure
AI_AgriYield_Predictor-Nithitha_K/
│
├─ Milestone 3/
│   └─ agricropyieldpredictor_application/
│       ├─ data/
│       │   ├─ users.csv
│       │   ├─ crop_type_map.pkl
│       │   ├─ crop_yield_label_map.pkl
│       │   ├─ crop_yield_model.pkl
│       │   ├─ crop_yield_scaler.pkl
│       ├─ app.py
│       ├─ login.py
│       ├─ your_dataset.csv
│       ├─ Readme.md
│
├─ milestone1/
├─ Milestone2/
├─ LICENSE
├─ README.md
├─ requirements.txt

Acess this application here : https://1234crop.streamlit.app/
