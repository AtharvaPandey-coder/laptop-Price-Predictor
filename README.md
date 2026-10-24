# 💻 Laptop Price Predictor

An interactive Machine Learning web application that predicts laptop prices based on hardware specifications and helps users explore laptop options, evaluate value for money, and compare two laptops side by side.

🔗 **[🚀 Try the Live App](https://laptop-price-predictor-87jbwp4eqpbkdcxuzezxcv.streamlit.app/)**

## 📌 Project Overview

Choosing a laptop can be difficult when comparing brands, processors, RAM, storage, graphics, and display specifications across different price ranges.

This project uses a trained Machine Learning pipeline to estimate laptop prices from user-provided specifications. It also includes additional tools to help users discover laptops within a budget, evaluate a laptop's indicative deal score, and compare predicted prices.

## ✨ Key Features

### 1. 💰 Laptop Price Prediction
- Select the laptop brand and type.
- Specify RAM, weight, touchscreen support, IPS display, screen resolution, CPU, HDD, SSD, GPU, and operating system.
- Calculate pixel density (PPI) from screen resolution and screen size.
- Generate an estimated laptop price using the trained stacking regression pipeline.
- Display a price category based on the predicted price.

### 2. 📊 Deal Score
- Calculates a rule-based score out of 100 using RAM, SSD capacity, predicted price, and CPU information.
- Classifies the result into deal categories such as Excellent Deal, Good Deal, Average Deal, or Poor Value for Money.

*Note: The deal score is a custom heuristic, not a statistically validated measure of market value.*

### 3. 🔎 Similar Laptop Suggestions
- Finds laptops with the selected brand and RAM configuration.
- Displays available matching records, including laptop type, CPU, and actual dataset price.
- Falls back to laptops with the same RAM when no brand-and-RAM matches are available.

### 4. 💸 Find the Best Laptop Within a Budget
- Enter a budget in Indian Rupees.
- Find up to five dataset-listed laptops priced within the selected budget.
- View brand, laptop type, RAM, CPU, SSD, HDD, and listed price.

### 5. ⚖️ Laptop vs Laptop Comparator
- Configure two laptops independently.
- Estimate the price of each laptop using the same trained model.
- Compare hardware specifications and predicted prices in a side-by-side table.
- Identify which configuration has the lower predicted price.

## 🧠 Machine Learning Model

The application uses a **Stacking Regressor** with three base models and a Ridge Regression final estimator.

| Component | Model / Technique |
|---|---|
| Preprocessing | ColumnTransformer |
| Categorical encoding | OneHotEncoder |
| Base model 1 | Random Forest Regressor |
| Base model 2 | Gradient Boosting Regressor |
| Base model 3 | XGBoost Regressor |
| Final estimator | Ridge Regression |
| Prediction transformation | Exponential transformation using NumPy |

### Model Workflow

1. Prepare laptop features and target prices.
2. Encode selected categorical features using One-Hot Encoding.
3. Train Random Forest, Gradient Boosting, and XGBoost as base estimators.
4. Combine their predictions through Ridge Regression.
5. Evaluate model performance on the test set.
6. Save the trained pipeline and use it for predictions in the Streamlit application.

The application loads the serialized pipeline from `pipe.pkl` and the laptop dataset from `df.pkl`.

## 📈 Model Performance

The stacking model achieved the following results on the test set:

| Metric | Result |
|---|---:|
| R² Score | **0.8901** |
| Mean Absolute Error (MAE) | **0.1548** |

- **R² Score:** Approximately 0.89, indicating that the model explains about 89% of the variance in the test target values.
- **MAE:** Approximately 0.155 in the target variable's scale.

**Important:** The model predicts the logarithm of laptop prices, and the application applies an exponential transformation to obtain the displayed price. Therefore, the MAE above is in the transformed target's scale, not directly in Indian Rupees.

## 🛠️ Tech Stack

- **Programming Language:** Python
- **Web Framework:** Streamlit
- **Data Manipulation:** Pandas, NumPy
- **Machine Learning:** Scikit-learn
- **Gradient Boosting:** XGBoost
- **Model Explainability Library:** SHAP
- **Model Persistence:** Pickle
- **Deployment:** Streamlit Community Cloud

## 📂 Project Structure

```text
Laptop-Price-Predictor/
│
├── app_01.py
├── pipe.pkl
├── df.pkl
├── requirements.txt
└── README.md
```

- `app_01.py` — Streamlit application and interactive features.
- `pipe.pkl` — Serialized, trained machine learning pipeline.
- `df.pkl` — Serialized laptop dataset used by the application.
- `requirements.txt` — Python dependencies.
- `README.md` — Project documentation.

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

Replace the repository URL and directory with your actual GitHub repository details.

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the application

```bash
streamlit run app_01.py
```

Streamlit will provide a local URL where you can interact with the application.

## 🎯 Project Objectives

- Apply ensemble learning techniques to a real-world regression problem.
- Build a reusable preprocessing and prediction pipeline.
- Deploy a trained ML model as an interactive web application.
- Turn model predictions into practical tools for exploring laptop configurations.
- Demonstrate an end-to-end workflow from model evaluation to deployment.

## 🚀 Future Improvements

- Add model evaluation in actual currency units, including MAE and RMSE in rupees.
- Improve deal scoring using market prices and specification-aware comparisons.
- Add filters for processor generation, GPU performance, display quality, and storage.
- Improve similar-laptop recommendations using multiple matching features.
- Add automated tests for preprocessing, prediction, and application functionality.

## 👨‍💻 Author

**Atharva Pandey**

🔗 [GitHub Profile](https://github.com/AtharvaPandey-coder)

---

⭐ If you find this project interesting, consider starring the repository!
