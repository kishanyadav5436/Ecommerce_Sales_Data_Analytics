import pandas as pd
import datetime
import joblib
import streamlit as st


def main():
    html_temp = """
    <h1 style='text-align:center;'>ShopKart Profit Category Prediction</h1>
    """

    # Load Model & Scaler
    model = joblib.load("decision_tree_model.pkl")
    scaler = joblib.load("scaler.pkl")

    st.markdown(html_temp, unsafe_allow_html=True)
    st.markdown("### This app will help you predict whether an order falls under Low Profit or High Profit.")

    # Customer Age
    p1 = st.number_input(
        "Please enter customer age",
        min_value=18,
        max_value=80,
        step=1,
    )

    # Gender
    s1 = st.selectbox("Select Gender", ("Female", "Male"))
    # NOTE: LabelEncoder sorts alphabetically -> Female=0, Male=1
    # Verify against data["Gender"].unique() in the notebook before deploying.
    p2 = 0 if s1 == "Female" else 1

    # Quantity
    p3 = st.number_input(
        "Please enter quantity ordered",
        min_value=1,
        max_value=100,
        step=1,
    )

    # Unit Price
    p4 = st.number_input(
        "Please enter unit price (₹)",
        min_value=1.0,
        max_value=100000.0,
        step=100.0,
    )

    # Discount
    p5 = st.number_input(
        "Please enter discount (%)",
        min_value=0.0,
        max_value=100.0,
        step=1.0,
    )

    # Shipping
    p6 = st.number_input(
        "Please enter shipping cost (₹)",
        min_value=0.0,
        max_value=10000.0,
        step=10.0,
    )

    # Delivery (days)
    p7 = st.number_input(
        "Please enter delivery time (in days)",
        min_value=1,
        max_value=30,
        step=1,
    )

    # Rating
    p8 = st.slider("Customer rating", 1, 5)

    # Order Date
    order_date = st.date_input(
        "Please select order date",
        value=datetime.date.today(),
    )
    p9 = order_date.month
    p10 = order_date.year
    p11 = order_date.weekday()  # Monday=0 ... Sunday=6
    p12 = 1 if p11 >= 5 else 0

    # City
    s2 = st.selectbox(
        "Select City",
        ("Bangalore", "Chennai", "Delhi", "Hyderabad", "Jaipur", "Lucknow", "Mumbai", "Pune"),
    )
    # NOTE: "Bangalore" assumed as the dropped baseline category (drop_first=True).
    # Verify against data["City"].unique() in the notebook before deploying.

    # Category
    s3 = st.selectbox(
        "Select Product Category",
        ("Beauty", "Electronics", "Fashion", "Furniture", "Grocery", "Sports"),
    )
    # NOTE: "Beauty" assumed as the dropped baseline category (drop_first=True).
    # Verify against data["Category"].unique() in the notebook before deploying.

    # Sales & Profit (required by the trained model's feature set)
    st.markdown("#### Sales & Profit Details")
    sales = st.number_input(
        "Please enter total sales amount (₹)",
        min_value=1.0,
        max_value=1000000.0,
        step=100.0,
    )
    profit = st.number_input(
        "Please enter profit amount (₹)",
        min_value=-100000.0,
        max_value=100000.0,
        step=100.0,
    )

    # Derived Features
    profit_margin = (profit / sales) * 100 if sales != 0 else 0
    revenue_per_item = sales / p3 if p3 != 0 else 0

    # One-Hot Encoding for City
    city_cols = {
        "City_Chennai": 0,
        "City_Delhi": 0,
        "City_Hyderabad": 0,
        "City_Jaipur": 0,
        "City_Lucknow": 0,
        "City_Mumbai": 0,
        "City_Pune": 0,
    }
    city_key = f"City_{s2}"
    if city_key in city_cols:
        city_cols[city_key] = 1

    # One-Hot Encoding for Category
    category_cols = {
        "Category_Electronics": 0,
        "Category_Fashion": 0,
        "Category_Furniture": 0,
        "Category_Grocery": 0,
        "Category_Sports": 0,
    }
    category_key = f"Category_{s3}"
    if category_key in category_cols:
        category_cols[category_key] = 1

    # Create DataFrame (column order must match training data)
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

    # Prediction
    if st.button("Predict"):
        data_scaled = scaler.transform(data_new)
        pred = model.predict(data_scaled)
        if pred[0] == 1:
            st.success("Predicted Profit Category: High Profit")
        else:
            st.warning("Predicted Profit Category: Low Profit")


if __name__ == "__main__":
    main()