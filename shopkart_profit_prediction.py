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
            border-radius: 16px;
            padding: 6px 6px;
            margin-bottom: 1.2rem;
        }

        .card-heading {
            color: #e6e9f0;
            font-size: 1.02rem;
            font-weight: 600;
            margin-bottom: 0.9rem;
            padding-top: 0.4rem;
        }

        /* Labels */
        label, .stSlider label, .stDateInput label, .stSelectbox label, .stNumberInput label {
            color: #8f98a8 !important;
            font-size: 0.72rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.04em;
            text-transform: uppercase;
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
        }

        /* Slider */
        .stSlider [data-baseweb="slider"] {
            margin-top: 0.4rem;
        }

        /* Summary rows (Gross Sales / Est. Profit) */
        .summary-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 4px;
            font-size: 0.85rem;
        }
        .summary-label { color: #9aa3b2; }
        .summary-value { color: #f0f2f6; font-weight: 600; }
        .summary-value.profit { color: #4ade80; }

        /* Predict button */
        .stButton > button {
            background: linear-gradient(90deg, #6d5efc, #8b7bff);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 0;
            font-weight: 700;
            font-size: 0.95rem;
            width: 100%;
            box-shadow: 0 6px 18px rgba(109, 94, 252, 0.35);
        }
        .stButton > button:hover {
            background: linear-gradient(90deg, #7c6dff, #9b8cff);
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Load Model & Scaler
    model = joblib.load("decision_tree_model.pkl")
    scaler = joblib.load("scaler.pkl")

    # ---------------- Header ----------------
    st.markdown('<div class="badge">FORECASTING ENGINE</div>', unsafe_allow_html=True)
    st.markdown('<div class="header-title">Predict</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="header-sub">Predict whether an order falls under Low Profit or High Profit '
        'categories with AI-driven precision.</div>',
        unsafe_allow_html=True,
    )

    # ---------------- Card 1: Order Identity ----------------
    with st.container(border=True):
        st.markdown('<div class="card-heading">📝 &nbsp;Order Identity</div>', unsafe_allow_html=True)

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
        st.markdown('<div class="card-heading">💳 &nbsp;Financial Inputs</div>', unsafe_allow_html=True)

        col7, col8 = st.columns(2)
        with col7:
            p4 = st.number_input("Unit Price (₹)", min_value=0.0, max_value=100000.0, step=100.0, value=0.0)
        with col8:
            p5 = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, step=1.0, value=0.0)

        p6 = st.number_input("Shipping Cost (₹)", min_value=0.0, max_value=10000.0, step=10.0, value=150.0)

        sales = st.number_input("Gross Sales (₹)", min_value=0.0, max_value=1000000.0, step=100.0, value=0.0)
        profit = st.number_input("Est. Profit (₹)", min_value=-100000.0, max_value=100000.0, step=100.0, value=0.0)

        st.markdown(
            f"""
            <div class="summary-row">
                <span class="summary-label">Gross Sales</span>
                <span class="summary-value">₹{sales:,.2f}</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">Est. Profit</span>
                <span class="summary-value profit">+ ₹{profit:,.2f}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ---------------- Derived Features ----------------
    profit_margin = (profit / sales) * 100 if sales != 0 else 0
    revenue_per_item = sales / p3 if p3 != 0 else 0

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
        "Sales": [sales],
        "Profit": [profit],
        "Rating": [p8],
        "Month": [p9],
        "Year": [p10],
        "Day_of_Week": [p11],
        "Weekend": [p12],
        "Profit_Margin": [profit_margin],
        "Revenue_per_Item": [revenue_per_item],
        **{k: [v] for k, v in city_cols.items()},
        **{k: [v] for k, v in category_cols.items()},
    })

    # ---------------- Predict ----------------
    if st.button("✨  Predict Profit Category"):
        data_scaled = scaler.transform(data_new)
        pred = model.predict(data_scaled)
        if pred[0] == 1:
            st.success("Predicted Profit Category: High Profit")
        else:
            st.warning("Predicted Profit Category: Low Profit")


if __name__ == "__main__":
    main()
