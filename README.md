# 🧬 ReproAI — Intelligent Fertility Decision Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Prototype-purple?style=for-the-badge)

**A Doctor-in-the-Loop AI clinical decision support system for IVF treatment planning.**

*AI assists. Doctors decide. Always.*

</div>

---

## 📌 Overview

**ReproAI** is an AI-powered fertility treatment planning tool built for reproductive endocrinologists. It combines machine learning predictions, rule-based clinical safety checks, digital twin simulation, and cohort-based evidence to recommend the most suitable IVF protocol — while keeping the doctor in full control of every decision.

> ⚠️ **Disclaimer:** This is a research prototype. Not approved for clinical use. Requires physician oversight.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🛡️ **Clinical Safety Engine** | Rule-based checks for OHSS risk, ovarian reserve, age, and BMI before any ML prediction |
| 🤖 **ML Predictions** | Random Forest models predict pregnancy success, OHSS risk, and egg yield |
| 🔮 **Digital Twin Simulator** | Simulates patient response across 3 IVF protocols side-by-side |
| 👥 **Cohort Matching** | K-NN finds 50 most similar patients and shows their real outcomes |
| 🎯 **Multi-Objective Optimization** | Ranks protocols by success rate, safety, dose, and cost |
| 🧠 **Explainable AI** | Natural language explanations and feature importance charts |
| ⚕️ **Doctor Override System** | Accept, modify, or reject any recommendation with full audit trail |
| 📊 **Premium Dark UI** | Professional clinical dashboard built with Streamlit + Plotly |

---

## 🏗️ Architecture

```
ReproAI/
├── app/
│   ├── main.py                  # Streamlit application entry point
│   ├── ui.py                    # All UI components and visualizations
│   ├── safety_rules.py          # Clinical rule-based safety engine
│   ├── similarity_engine.py     # K-NN cohort matching
│   ├── optimization_engine.py   # Multi-objective protocol ranking
│   ├── digital_twin.py          # Protocol simulation engine
│   └── explainability.py        # AI explanation generator
│
├── models/
│   ├── train_model.py           # Model training pipeline
│   ├── predictor.py             # Prediction wrapper
│   └── saved/                   # Trained model files (.pkl)
│
├── data/
│   ├── generate_dataset.py      # Synthetic dataset generator
│   └── synthetic_fertility_dataset.csv
│
├── utils/
│   └── preprocessing.py         # Feature engineering pipeline
│
├── archive/                     # Raw PCOS source data
├── requirements.txt
└── README.md
```

---

## 🔬 System Flow

```
Patient Input (Full-Page Form)
        │
        ▼
Clinical Safety Rules  ──►  Alerts & Warnings
        │
        ▼
ML Predictions  ──►  Pregnancy % · OHSS Risk · Egg Yield
        │
        ▼
Digital Twin  ──►  Simulate 3 Protocols
        │
        ▼
Optimization Engine  ──►  Ranked Recommendations
        │
        ▼
Explainability  ──►  Natural Language + Feature Importance
        │
        ▼
Doctor Decision  ──►  Accept / Modify / Reject + Audit Log
```

---

## 🤖 Machine Learning Models

| Model | Algorithm | Metric | Performance |
|---|---|---|---|
| Pregnancy Success | Random Forest Classifier | AUC | 0.704 |
| OHSS Risk | Random Forest Classifier | AUC | 0.754 |
| Egg Yield | Random Forest Regressor | MAE | 1.43 eggs |

### Feature Engineering
- LH/FSH ratio (PCOS indicator)
- Age-adjusted AMH
- Follicle score (AMH × AFC)
- Ovarian reserve category
- Combined risk score

---

## 📊 Dataset

Synthetic dataset of **2,000 patients** generated with clinically realistic distributions:

| Variable | Range | Notes |
|---|---|---|
| Age | 25–44 years | Uniform distribution |
| AMH | 0.1–18.8 ng/mL | Age & PCOS correlated |
| BMI | 18–40 | Higher in PCOS patients |
| FSH | 2–20 mIU/mL | Increases with age |
| LH | 2–25 mIU/mL | Elevated in PCOS |
| AFC | 2–30 | Correlated with AMH |
| PCOS Prevalence | ~30% | — |
| Success Rate | ~32% | — |
| OHSS Rate | ~14% | — |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ReproAI.git
cd ReproAI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate synthetic dataset
python data/generate_dataset.py

# 4. Train ML models
python models/train_model.py

# 5. Launch the app
streamlit run app/main.py
```

Open your browser at **http://localhost:8501**

---

## 🖥️ Usage

### Step 1 — Patient Data Entry
Fill in the full-page clinical form:
- Demographics (Age, BMI)
- Hormone levels (AMH, FSH, LH, Estradiol)
- Ultrasound findings (AFC)
- Medical history (PCOS, Endometriosis, Male Factor)
- Previous IVF attempts

### Step 2 — Analyze
Click **Analyze Patient** to run the full pipeline.

### Step 3 — Review Results (5 Tabs)

| Tab | Content |
|---|---|
| 📊 Overview | Patient summary cards, safety alerts, AI predictions with gauge charts |
| 🔬 Protocols | Recommended protocol, radar chart comparison, digital twin simulation |
| 👥 Cohort | 50 similar patients, success rates, protocol distribution pie chart |
| 🧠 Explain | Natural language reasoning, feature importance, score breakdown |
| ⚕️ Decision | Accept / Modify / Reject with notes, full decision audit log |

### Step 4 — Make Decision
The doctor reviews all AI outputs and makes the final clinical decision. Every decision is logged with a timestamp.

---

## 🛡️ Clinical Safety Rules

| Rule | Trigger | Alert Level |
|---|---|---|
| Diminished Ovarian Reserve | AMH < 1.0 ng/mL | Warning |
| Severely Diminished Reserve | AMH < 0.5 ng/mL | Critical |
| OHSS Risk | AMH > 4 + PCOS | Alert |
| Advanced Maternal Age | Age ≥ 42 | Alert |
| Age-Related Decline | Age ≥ 38 | Warning |
| Elevated FSH | FSH > 12 mIU/mL | Warning |
| Elevated LH/FSH Ratio | Ratio > 2.0 | Warning |
| Obesity | BMI ≥ 30 | Warning |
| Multiple Failures | Previous IVF ≥ 3 | Alert |
| Combined Poor Prognosis | Age ≥ 38 + AMH < 1.5 + failures | Critical |

---

## 🎯 Optimization Scoring

Protocols are ranked using a weighted multi-objective function:

```
Score = 0.50 × Success Probability
      − 0.20 × OHSS Risk
      − 0.15 × Medication Dose (normalized)
      − 0.15 × Cost Index (normalized)
```

Sensitivity analysis runs 4 scenarios: Success-Focused, Safety-Focused, Cost-Focused, and Balanced.

---

## 🔮 Digital Twin Protocols

| Protocol | Dose Range | Cost Index | Best For |
|---|---|---|---|
| Mild Stimulation | 150–225 IU | 1 (Low) | Young patients, good reserve |
| Antagonist | 150–300 IU | 2 (Medium) | PCOS, high reserve |
| Long Agonist | 300–450 IU | 3 (High) | Diminished reserve, older patients |

---

## 📦 Dependencies

```
streamlit==1.28.0
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
matplotlib==3.7.2
plotly==5.17.0
openpyxl==3.1.2
```

---

## 🔮 Roadmap

### Short-term
- [ ] PGT-A recommendation logic
- [ ] Embryo quality prediction
- [ ] Transfer strategy optimization
- [ ] PDF report export

### Medium-term
- [ ] Real EMR data integration
- [ ] Deep learning models (LSTM for cycle history)
- [ ] Multi-center validation
- [ ] REST API backend

### Long-term
- [ ] Real-time cycle monitoring
- [ ] Automated protocol adjustment
- [ ] Regulatory approval pathway (FDA/CE)
- [ ] Mobile application

---

## 🛡️ Ethics & Safety

- All recommendations are **suggestions only**, not prescriptions
- Doctors maintain **full decision authority** at all times
- Safety rules **override** ML predictions when necessary
- Full **audit trail** for every clinical decision
- Designed as **Clinical Decision Support (CDS)**, not a diagnostic device
- No real patient data used — synthetic dataset only

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Synthetic data distributions based on published IVF literature
- Clinical safety rules derived from ASRM guidelines
- ML architecture inspired by healthcare AI best practices

---

<div align="center">

**Built for hackathon/research demonstration purposes.**

*ReproAI — Where Clinical Intelligence Meets Human Judgment*

</div>
