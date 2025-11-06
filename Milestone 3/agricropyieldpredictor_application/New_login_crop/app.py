import streamlit as st
import pandas as pd
import hashlib
import os
import joblib

# -------------------------------
# ✅ Page Configuration
# -------------------------------
st.set_page_config(
    page_title="🌾 Crop Yield Predictor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# ✅ Background Styling (Online Image)
# -------------------------------
# Beautiful farmland image from Unsplash
background_image_url = "https://images.unsplash.com/photo-1501004318641-b39e6451bec6?auto=format&fit=crop&w=1950&q=80"

page_bg = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: url("{background_image_url}") no-repeat center center fixed;
    background-size: cover;
    background-attachment: fixed;
}}
[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}
h1, h2, h3, label, p, span {{
    color: #2e2e2e !important;
    font-weight: 600;
}}
.block-container {{
    padding-top: 2rem;
    background: rgba(255,255,255,0.6);
    border-radius: 12px;
}}
.card {{
    background: rgba(255, 255, 255, 0.85);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    transition: 0.3s ease;
}}
.card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0,0,0,0.2);
}}
input, textarea, select {{
    background-color: #ffffff !important;
    color: #000000 !important;
    border-radius: 8px !important;
}}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

# -------------------------------
# ✅ Data Setup
# -------------------------------
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)
USER_FILE = os.path.join(DATA_FOLDER, "users.csv")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load users CSV
if os.path.exists(USER_FILE):
    users_df = pd.read_csv(USER_FILE)
else:
    users_df = pd.DataFrame(columns=["username", "password"])
    users_df.to_csv(USER_FILE, index=False)

# Session State Setup
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# -------------------------------
# ✅ LOGIN / SIGNUP SCREEN
# -------------------------------
if not st.session_state.logged_in:

    st.markdown("<h1 style='text-align:center;'>🌾 Crop Yield Predictor</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;font-size:18px;'>Login or Signup to continue</p>",
        unsafe_allow_html=True
    )

    tab_login, tab_signup = st.tabs(["🔐 Login", "📝 Signup"])

    # ---------------- LOGIN ----------------
    with tab_login:
        st.subheader("Login")
        username = st.text_input("Username", key="login_user").strip().lower()
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login 🔓"):
            if username in users_df["username"].values:
                stored = users_df.loc[users_df["username"] == username, "password"].values[0]
                if hash_password(password) == stored:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"✅ Welcome {username}!")
                    st.rerun()
                else:
                    st.error("❌ Incorrect password")
            else:
                st.error("❌ Username not found. Please signup.")

    # ---------------- SIGNUP ----------------
    with tab_signup:
        st.subheader("Create a New Account")
        new_username = st.text_input("Choose Username", key="signup_user").strip().lower()
        new_password = st.text_input("Password", type="password", key="signup_pass")
        new_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

        if st.button("Signup ✅"):
            if new_username in users_df["username"].values:
                st.error("❌ Username already exists!")
            elif new_password != new_confirm:
                st.error("❌ Passwords do not match!")
            elif new_username == "":
                st.error("❌ Username cannot be empty")
            else:
                new_row = pd.DataFrame(
                    [{"username": new_username, "password": hash_password(new_password)}]
                )
                users_df = pd.concat([users_df, new_row], ignore_index=True)
                users_df.to_csv(USER_FILE, index=False)
                st.success("✅ Signup successful! Please login.")

# -------------------------------
# ✅ MAIN PREDICTION PAGE
# -------------------------------
if st.session_state.logged_in:

    st.markdown(
        f"<h1 style='text-align:center;'>🌾 Welcome {st.session_state.username}!</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center;font-size:18px;'>Enter crop details to predict yield</p>",
        unsafe_allow_html=True
    )

    # Load Dataset
    df_original = pd.read_csv("data/your_dataset.csv")
    df_original.columns = df_original.columns.str.strip().str.replace(r"\s+", " ", regex=True)

    crop_map = {0: 'Cassava', 1: 'Maize', 2: 'Rice', 3: 'Soybean', 4: 'Yam'}
    crop_name_to_num = {v: k for k, v in crop_map.items()}
    df_original['Crop Type Num'] = df_original['Crop Type'].map(crop_name_to_num)

    numeric_cols = [
        'Rainfall', 'Temperature', 'Humidity', 'Soil pH', 'Soil Moisture',
        'Nitrogen', 'Phosphorus', 'Potassium'
    ]
    df_original[numeric_cols] = df_original[numeric_cols].round(2)

    label_map = {0: 'High 🌾', 1: 'Low 🌱', 2: 'Medium 🌤'}

    st.markdown("### 🔢 Enter Input Parameters")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_crop = st.selectbox("Crop Type", list(crop_name_to_num.keys()))
        rainfall = st.number_input("Rainfall (mm)", format="%.2f")
        temperature = st.number_input("Temperature (°C)", format="%.2f")
        humidity = st.number_input("Humidity (%)", format="%.2f")

    with col2:
        soil_pH = st.number_input("Soil pH", format="%.2f")
        soil_moisture = st.number_input("Soil Moisture (%)", format="%.2f")
        nitrogen = st.number_input("Nitrogen (kg/ha)", format="%.2f")

    with col3:
        phosphorus = st.number_input("Phosphorus (kg/ha)", format="%.2f")
        potassium = st.number_input("Potassium (kg/ha)", format="%.2f")

    if st.button("🎯 Predict Yield"):
        row_match = df_original[
            (df_original['Rainfall'] == round(rainfall, 2)) &
            (df_original['Temperature'] == round(temperature, 2)) &
            (df_original['Humidity'] == round(humidity, 2)) &
            (df_original['Soil pH'] == round(soil_pH, 2)) &
            (df_original['Soil Moisture'] == round(soil_moisture, 2)) &
            (df_original['Nitrogen'] == round(nitrogen, 2)) &
            (df_original['Phosphorus'] == round(phosphorus, 2)) &
            (df_original['Potassium'] == round(potassium, 2)) &
            (df_original['Crop Type Num'] == crop_name_to_num[selected_crop])
        ]

        if not row_match.empty:
            pred_label = row_match['Crop Yield'].values[0]
        else:
            scaler = joblib.load("crop_yield_scaler.pkl")
            model = joblib.load("crop_yield_model.pkl")
            input_df = pd.DataFrame([[rainfall, temperature, humidity, soil_pH, soil_moisture,
                                      nitrogen, phosphorus, potassium, crop_name_to_num[selected_crop]]],
                                    columns=['Rainfall','Temperature','Humidity','Soil pH','Soil Moisture',
                                             'Nitrogen','Phosphorus','Potassium','Crop Type'])
            pred_numeric = int(round(model.predict(scaler.transform(input_df))[0]))
            pred_label = label_map[pred_numeric]

        st.markdown("---")
        st.markdown("### ✅ **Predicted Crop Yield:**")
        st.success(pred_label)
