# ShopKart Ecommerce Sales Data Analysis & Profit Prediction

A machine learning project that analyzes ShopKart's ecommerce sales data and predicts whether an order falls under **High Profit** or **Low Profit**, deployed as an interactive Streamlit web app.

## 📌 Project Overview

This project covers the complete ML pipeline:
1. Exploratory Data Analysis (EDA)
2. Data Cleaning (missing values, invalid entries)
3. Outlier Detection & Removal (IQR method)
4. Feature Engineering (Month, Year, Day of Week, Weekend, Profit Margin, Revenue per Item)
5. Encoding (Label Encoding & One-Hot Encoding)
6. Model Training & Comparison (Logistic Regression, Decision Tree, Random Forest, KNN, SVM, Gradient Boosting)
7. Model Deployment (Decision Tree Classifier via Streamlit)

## 🗂️ Project Structure

```
Project 7 - Ecommerce Sales Data Analysis/
│
├── shopkart_profit_prediction.py   # Streamlit app for deployment
├── decision_tree_model.pkl         # Trained Decision Tree model
├── scaler.pkl                      # StandardScaler used on training data
├── requirements.txt                # Python dependencies
├── shopkart_sales_dataset.csv      # Dataset used for training (not included in repo)
└── README.md                       # Project documentation
```

## ⚙️ Installation

1. Clone the repository:
   ```
   git clone https://github.com/kishanyadav5436/Ecommerce_Sales_Data_Analytics.git
   cd Ecommerce_Sales_Data_Analytics
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## 🚀 Running the App

```
streamlit run shopkart_profit_prediction.py
```

The app will open automatically in your browser at `http://localhost:8501`.

## 🧠 Model Details

- **Algorithm:** Decision Tree Classifier
- **Target Variable:** `Profit_Category` (0 = Low Profit, 1 = High Profit)
- **Preprocessing:** StandardScaler applied to all numerical & encoded features
- **Selected Model Reason:** Best accuracy among tested models (Logistic Regression, Decision Tree, Random Forest, KNN, SVM, Gradient Boosting) on the test set

## 📊 Features Used

| Feature | Description |
|---|---|
| Customer_Age | Age of the customer |
| Gender | Customer gender (Label Encoded) |
| Qty | Quantity ordered |
| Unit Price | Price per unit |
| Discount | Discount applied (%) |
| Shipping | Shipping cost |
| Delivery | Delivery time (days) |
| Sales | Total sales amount |
| Profit | Profit amount |
| Rating | Customer rating (1–5) |
| Month / Year / Day_of_Week / Weekend | Derived from Order Date |
| Profit_Margin | Profit / Sales × 100 |
| Revenue_per_Item | Sales / Qty |
| City (One-Hot) | Customer's city |
| Category (One-Hot) | Product category |

## 📝 Notes

- Ensure `decision_tree_model.pkl` and `scaler.pkl` are in the same directory as `shopkart_profit_prediction.py` before running the app.
- The One-Hot encoded City and Category columns must match the categories used during training.

## 🛠️ Tech Stack

- Python
- Pandas, NumPy
- Scikit-learn
- Matplotlib, Seaborn (EDA)
- Streamlit (Deployment)

## 👤 Author

Kishan Yadav
