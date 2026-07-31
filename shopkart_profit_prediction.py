import datetime
import joblib
import pandas as pd
import streamlit as st


def main():
    st.set_page_config(
        page_title="ShopKart Profit Category Prediction",
        page_icon="🛒",
        layout="centered"
    )

    html_temp = """
    <div style='background-color:#1E88E5;padding:12px;border-radius:10px;margin-bottom:20px;'>
        <h2 style='color:white;text-align:center;margin:0;'>ShopKart Profit Category Prediction</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    st.markdown("### Predict whether an order will generate **High Profit** or **Low Profit** before dispatch.")

    # Sidebar model selector
    st.sidebar.header("Model Settings")
    model_choice = st.sidebar.selectbox(
        "Select Trained Model",
        ("Decision Tree", "Gradient Boosting")
    )

    if model_choice == "Gradient Boosting":
        model_file = "Gradient_Boodting_model.pkl"
    else:
        model_file = "decision_tree_model.pkl"

    # Load Model & Scaler
    try:
        model = joblib.load(model_file)
        scaler = joblib.load("scaler.pkl")
    except Exception as e:
        st.error(f"Error loading model or scaler files: {e}")
        return

    col1, col2 = st.columns(2)

    with col1:
        # Customer Age
        p1 = st.number_input(
            "Customer Age",
            min_value=18,
            max_value=100,
            value=30,
            step=1,
        )

        # Gender
        s1 = st.selectbox("Gender", ("Female", "Male"))
        p2 = 0 if s1 == "Female" else 1

        # Quantity
        p3 = st.number_input(
            "Quantity Ordered",
            min_value=1,
            max_value=100,
            value=2,
            step=1,
        )

        # Unit Price
        p4 = st.number_input(
            "Unit Price (₹)",
            min_value=1.0,
            max_value=100000.0,
            value=500.0,
            step=50.0,
        )

        # Discount
        p5 = st.number_input(
            "Discount (%)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=1.0,
        )

        # Shipping
        p6 = st.number_input(
            "Shipping Cost (₹)",
            min_value=0.0,
            max_value=10000.0,
            value=50.0,
            step=10.0,
        )

    with col2:
        # Delivery (days)
        p7 = st.number_input(
            "Delivery Time (Days)",
            min_value=1,
            max_value=30,
            value=3,
            step=1,
        )

        # Rating
        p8 = st.slider("Customer Rating", 1, 5, value=4)

        # Order Date
        order_date = st.date_input(
            "Order Date",
            value=datetime.date.today(),
        )
        p9 = order_date.month
        p10 = order_date.year
        p11 = order_date.weekday()  # Monday=0 ... Sunday=6
        p12 = 1 if p11 >= 5 else 0

        # City
        s2 = st.selectbox(
            "City",
            ("Bangalore", "Chennai", "Delhi", "Hyderabad", "Jaipur", "Lucknow", "Mumbai", "Pune"),
        )

        # Category
        s3 = st.selectbox(
            "Product Category",
            ("Beauty", "Electronics", "Fashion", "Furniture", "Grocery", "Sports"),
        )

    # One-Hot Encoding for City (Bangalore is dropped baseline category)
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

    # One-Hot Encoding for Category (Beauty is dropped baseline category)
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

    # Create DataFrame (24 features matching training pipeline)
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

    st.write("")
    if st.button("Predict Profit Category", use_container_width=True):
        data_scaled = scaler.transform(data_new)
        pred = model.predict(data_scaled)

        if pred[0] == 1:
            st.success("🎉 **Predicted Category: High Profit**")
        else:
            st.warning("⚠️ **Predicted Category: Low Profit**")


if __name__ == "__main__":
    main()