import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime

model = joblib.load("Gradient_boosting_model.pkl")
scaler = joblib.load("scaler.pkl")

st.title("Ecommerce Profit Prediction System")

st.markdown("Predict whether an ecommerce order will generate High Profit or Low Profit using Machine Learning.")

st.header("Enter Order Details")

col1, col2 = st.columns(2)

with col1:

    customer_age = st.number_input("Customer Age",min_value=18,max_value=80,value=30)

    gender = st.selectbox("Gender",["Male", "Female"])

    city = st.selectbox("City",["Bengaluru","Chennai","Delhi","Hyderabad","Jaipur","Lucknow","Mumbai","Pune"])

    category = st.selectbox("Category",["Beauty","Electronics","Fashion","Furniture","Grocery","Sports"])

    qty = st.number_input("Quantity",min_value=1,value=2)


with col2:

    unit_price = st.number_input("Unit Price",min_value=1.0,value=500.0)

    discount = st.number_input("Discount (%)",min_value=0.0,max_value=100.0,value=10.0)

    shipping = st.number_input("Shipping Cost",min_value=0.0,value=100.0)

    delivery = st.number_input("Delivery Days",min_value=1,value=5)

    rating = st.slider("Customer Rating",1.0,5.0,4.0,step=0.1)

order_date = st.date_input("Order Date",datetime.today())

month = order_date.month
year = order_date.year
day_of_week = order_date.weekday()
weekend = 1 if day_of_week >= 5 else 0

gender = 1 if gender == "Male" else 0

input_data = {

    "Customer_Age": customer_age,
    "Gender": gender,
    "Qty": qty,
    "Unit Price": unit_price,
    "Discount": discount,
    "Shipping": shipping,
    "Delivery": delivery,
    "Rating": rating,
    "Month": month,
    "Year": year,
    "Day_of_Week": day_of_week,
    "Weekend": weekend,

    "City_Chennai":0,
    "City_Delhi":0,
    "City_Hyderabad":0,
    "City_Jaipur":0,
    "City_Lucknow":0,
    "City_Mumbai":0,
    "City_Pune":0,

    "Category_Electronics":0,
    "Category_Fashion":0,
    "Category_Furniture":0,
    "Category_Grocery":0,
    "Category_Sports":0

}

if city != "Bengaluru":
    input_data[f"City_{city}"] = 1

if category != "Beauty":
    input_data[f"Category_{category}"] = 1

input_df = pd.DataFrame([input_data])

feature_order = [

    'Customer_Age',
    'Gender',
    'Qty',
    'Unit Price',
    'Discount',
    'Shipping',
    'Delivery',
    'Rating',
    'Month',
    'Year',
    'Day_of_Week',
    'Weekend',
    'City_Chennai',
    'City_Delhi',
    'City_Hyderabad',
    'City_Jaipur',
    'City_Lucknow',
    'City_Mumbai',
    'City_Pune',
    'Category_Electronics',
    'Category_Fashion',
    'Category_Furniture',
    'Category_Grocery',
    'Category_Sports'

]

input_df = input_df[feature_order]
input_scaled = scaler.transform(input_df)

if st.button("Predict Profit Category"):
    prediction = model.predict(input_scaled)[0]
    probability = model.predict_proba(input_scaled)

    # st.markdown("---")
    st.subheader("Prediction Result")

    if prediction == 1:
        st.success("High Profit")
    else:
        st.error("Low Profit")
