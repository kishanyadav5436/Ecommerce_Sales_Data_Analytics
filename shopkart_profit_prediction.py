import os
import pandas as pd
import datetime
import joblib
import streamlit as st


def main():
    st.set_page_config(
        page_title="ShopKart Profit Predictor",
        page_icon="💰",
        layout="centered",
        initial_sidebar_state="collapsed",
    )

    # ---------------- Custom CSS (dark themed UI) ----------------
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0d1117;
            background-image: radial-gradient(circle at 1px 1px, #1c2333 1px, transparent 0);
            background-size: 22px 22px;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 640px;
        }

        /* Header */
        .header-title {
            color: #f5f6fa;
            font-size: 2.1rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .badge {
            display: inline-block;
            background: linear-gradient(90deg, #6d5efc, #9b8cff);
            color: white;
            font-size: 0.68rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            padding: 3px 10px;
            border-radius: 999px;
            margin-bottom: 0.6rem;
        }
        .header-sub {
            color: #9aa3b2;
            font-size: 0.92rem;
            margin-bottom: 1.6rem;
        }

        /* Card container */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #131a29;
            border: 1px solid #232c3d;
            border-radius: 18px;
            padding: 8px 10px 16px 10px;
            margin-bottom: 1.5rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.02);
            position: relative;
            overflow: hidden;
            transition: box-shadow 0.25s ease, border-color 0.25s ease;
        }
        div[data-testid="stVerticalBlockBorderWrapper"]::before {
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, #6d5efc, #9b8cff, transparent);
        }
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            border-color: #313d55;
            box-shadow: 0 14px 36px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.03);
        }

        .card-heading {
            color: #e6e9f0;
            font-size: 1.05rem;
            font-weight: 700;
            letter-spacing: 0.01em;
            margin: 0.5rem 0 1.1rem 0;
            padding-bottom: 0.7rem;
            border-bottom: 1px solid #1f2738;
        }
        .card-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 26px;
            height: 26px;
            border-radius: 8px;
            background: rgba(109, 94, 252, 0.15);
            margin-right: 4px;
            font-size: 0.9rem;
        }

        /* Row spacing */
        div[data-testid="stHorizontalBlock"] {
            gap: 14px;
            margin-bottom: 0.35rem;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] div[data-testid="stVerticalBlock"] > div {
            margin-bottom: 0.55rem;
        }

        /* Labels */
        label, .stSlider label, .stDateInput label, .stSelectbox label, .stNumberInput label {
            color: #8f98a8 !important;
            font-size: 0.68rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            margin-bottom: 4px !important;
        }

        /* Inputs */
        div[data-baseweb="select"] > div,
        input[type="number"],
        input[type="text"],
        .stDateInput input {
            background-color: #1a2233 !important;
            border: 1px solid #2a3448 !important;
            border-radius: 10px !important;
            color: #f0f2f6 !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        div[data-baseweb="select"] > div:focus-within,
        input[type="number"]:focus,
        input[type="text"]:focus,
        .stDateInput input:focus {
            border-color: #6d5efc !important;
            box-shadow: 0 0 0 3px rgba(109, 94, 252, 0.18) !important;
            outline: none !important;
        }

        /* Number input +/- buttons */
        div[data-testid="stNumberInput"] button {
            background-color: #202b40 !important;
            border: 1px solid #2a3448 !important;
            color: #c3c9d6 !important;
            border-radius: 8px !important;
            transition: background-color 0.2s ease;
        }
        div[data-testid="stNumberInput"] button:hover {
            background-color: #2b3752 !important;
            color: #ffffff !important;
        }

        /* Slider */
        .stSlider [data-baseweb="slider"] {
            margin-top: 0.6rem;
        }
        .stSlider [role="slider"] {
            box-shadow: 0 0 0 5px rgba(109, 94, 252, 0.2) !important;
        }

        /* Summary rows (Gross Sales / Est. Profit) */
        .summary-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 9px 12px;
            font-size: 0.85rem;
            background-color: #0f1522;
            border-radius: 10px;
            margin-top: 6px;
            border: 1px solid #1c2536;
        }
        .summary-label { color: #9aa3b2; }
        .summary-value { color: #f0f2f6; font-weight: 700; }
        .summary-value.profit { color: #4ade80; }

        /* Predict button */
        .stButton > button {
            background: linear-gradient(90deg, #6d5efc, #8b7bff);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.85rem 0;
            font-weight: 700;
            font-size: 0.98rem;
            letter-spacing: 0.02em;
            width: 100%;
            box-shadow: 0 8px 24px rgba(109, 94, 252, 0.4);
            transition: transform 0.15s ease, box-shadow 0.2s ease, background 0.2s ease;
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #7c6dff, #9b8cff);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 12px 30px rgba(109, 94, 252, 0.5);
        }
        .stButton > button:active {
            transform: translateY(0px);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------------- Load Model & Scaler (robust) ----------------
    # Resolve paths relative to this script's own folder, not Streamlit's
    # working directory (which can differ on Streamlit Cloud).
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "Gradient_Boodting_model.pkl")
    SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")

    @st.cache_resource(show_spinner="Loading model...")
    def load_artifacts():
        missing = [p for p in (MODEL_PATH, SCALER_PATH) if not os.path.exists(p)]
        if missing:
            raise FileNotFoundError(
                "Missing file(s): " + ", ".join(missing) +
                ". Make sure the .pkl files are committed to the repo "
                "(check they aren't in .gitignore or over GitHub's 100MB limit)."
            )
        try:
            model = joblib.load(MODEL_PATH)
            scaler = joblib.load(SCALER_PATH)
        except ModuleNotFoundError as e:
            raise ModuleNotFoundError(
                f"{e}. The pickle file needs a Python package that isn't installed "
                "in this environment. Add it to requirements.txt (most likely "
                "'scikit-learn', or 'xgboost'/'lightgbm' if that's what trained the model)."
            ) from e
        return model, scaler

    try:
        model, scaler = load_artifacts()
    except Exception as e:
        st.error(f"Could not load model/scaler: {e}")
        st.stop()

    # ---------------- Header ----------------
    st.markdown('<div class="badge">FORECASTING ENGINE</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-title">Predict</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="header-sub">Predict whether an order falls under Low Profit or High Profit '
        'categories with AI-driven precision.</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

    # ---------------- Card 1: Order Identity ----------------
    with st.container(border=True):
        st.markdown(
            '<div class="card-heading"><span class="card-icon">📝</span>Order Identity</div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            p1 = st.number_input("Age", min_value=18, max_value=80, step=1, value=25)
        with col2:
            s1 = st.selectbox("Gender", ("Female", "Male"))
        p2 = 0 if s1 == "Female" else 1

        col3, col4 = st.columns(2)
        with col3:
            s3 = st.selectbox(
                "Category",
                ("Beauty", "Electronics", "Fashion", "Furniture", "Grocery", "Sports"),
            )
        with col4:
            s2 = st.selectbox(
                "City",
                ("Bangalore", "Chennai", "Delhi", "Hyderabad", "Jaipur", "Lucknow", "Mumbai", "Pune"),
            )

        col5, col6 = st.columns(2)
        with col5:
            p3 = st.number_input("Quantity", min_value=1, max_value=100, step=1, value=1)
        with col6:
            p7 = st.number_input("Delivery (days)", min_value=1, max_value=30, step=1, value=3)

        order_date = st.date_input("Order Date", value=datetime.date.today())
        p9 = order_date.month
        p10 = order_date.year
        p11 = order_date.weekday()
        p12 = 1 if p11 >= 5 else 0

        p8 = st.slider("Customer Rating", 1.0, 5.0, 3.0, step=0.1)

    # ---------------- Card 2: Financial Inputs ----------------
    with st.container(border=True):
        st.markdown(
            '<div class="card-heading"><span class="card-icon">💳</span>Financial Inputs</div>',
            unsafe_allow_html=True,
        )

        col7, col8 = st.columns(2)
        with col7:
            p4 = st.number_input("Unit Price (₹)", min_value=0.0, max_value=100000.0, step=100.0, value=0.0)
        with col8:
            p5 = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, step=1.0, value=0.0)

        p6 = st.number_input("Shipping Cost (₹)", min_value=0.0, max_value=10000.0, step=10.0, value=150.0)

    # ---------------- Derived Features ----------------
    city_cols = {
        "City_Chennai": 0, "City_Delhi": 0, "City_Hyderabad": 0, "City_Jaipur": 0,
        "City_Lucknow": 0, "City_Mumbai": 0, "City_Pune": 0,
    }
    city_key = f"City_{s2}"
    if city_key in city_cols:
        city_cols[city_key] = 1

    category_cols = {
        "Category_Electronics": 0, "Category_Fashion": 0, "Category_Furniture": 0,
        "Category_Grocery": 0, "Category_Sports": 0,
    }
    category_key = f"Category_{s3}"
    if category_key in category_cols:
        category_cols[category_key] = 1

    data_new = pd.DataFrame({
        "Customer_Age": [p1],
        "Gender": [p2],
        "Qty": [p3],
        "Unit Price": [p4],
        "Discount": [p5],
        "Shipping": [p6],
        "Delivery": [p7],
        "Rating": [p8],
        "Month": [p9],
        "Year": [p10],
        "Day_of_Week": [p11],
        "Weekend": [p12],
        **{k: [v] for k, v in city_cols.items()},
        **{k: [v] for k, v in category_cols.items()},
    })

    # ---------------- Predict ----------------
    if st.button("✨  Predict Profit Category"):
        try:
            data_scaled = scaler.transform(data_new)
            pred = model.predict(data_scaled)
        except Exception as e:
            st.error(f"Prediction failed: {e}")
            return

        if pred[0] == 1:
            st.success("Predicted Profit Category: High Profit")
        else:
            st.warning("Predicted Profit Category: Low Profit")


if __name__ == "__main__":
    main()
