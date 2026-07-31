# ShopKart Profit Category Prediction (Streamlit App)

An interactive Machine Learning web app built with **Streamlit** to predict whether a customer order will generate **High Profit (1)** or **Low Profit (0)** prior to order dispatch.

---

## 📁 Files Required for Streamlit Deployment

To deploy this app on **Streamlit Community Cloud** (or any server environment), ONLY the following **5 files** are required:

1. 📄 **`shopkart_profit_prediction.py`**
   - The main Streamlit web application script.
2. 📦 **`requirements.txt`**
   - Python dependencies (`streamlit`, `pandas`, `scikit-learn`, `joblib`).
3. 🤖 **`decision_tree_model.pkl`**
   - Trained Decision Tree Classification model.
4. 🤖 **`Gradient_Boodting_model.pkl`**
   - Trained Gradient Boosting Classification model.
5. ⚖️ **`scaler.pkl`**
   - Trained `StandardScaler` fitted on the 24 preprocessed training features.

---

## 🚀 How to Run Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the Streamlit App
streamlit run shopkart_profit_prediction.py
```

---

## ☁️ How to Deploy to Streamlit Community Cloud

1. Push the repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your GitHub repository.
4. Set Main File Path to: `shopkart_profit_prediction.py` (or `Project 7 - Ecommerce Sales Data Analysis/shopkart_profit_prediction.py`).
5. Click **Deploy**!