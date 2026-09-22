<div align="center">

# 🦴 Bone Health AI

### AI-Based Bone Health Monitoring for Postpartum Women After Caesarean Delivery

**An explainable machine-learning application for assessing bone health risk and generating personalized assessment reports.**

<br>

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)](https://bone-health-ai-6sunz4xsbqppzi6mbbduzv.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge\&logo=github\&logoColor=white)](https://github.com/jasminefloraa/bone-health-ai)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)

<br>

![Project Status](https://img.shields.io/badge/Status-Live%20%26%20Deployed-00C853?style=flat-square)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-Random%20Forest-8E44AD?style=flat-square)
![Explainable AI](https://img.shields.io/badge/Explainable%20AI-SHAP-F39C12?style=flat-square)

</div>

---

## Overview

**Bone Health AI** is an AI-powered web application designed to assess bone-health risk for **postpartum women after Caesarean delivery**.

The application combines a **Random Forest machine-learning model**, **SHAP-based explainability**, interactive data visualization, and automated **PDF report generation** into a single Streamlit application.

Instead of providing only a prediction, the application also helps users understand **which input factors contributed to the prediction**.

> **Predict → Explain → Report**

---

## Live Application

<div align="center">

### Try the deployed application

[![Open Bone Health AI](https://img.shields.io/badge/OPEN%20LIVE%20APPLICATION-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)](https://bone-health-ai-6sunz4xsbqppzi6mbbduzv.streamlit.app/)

**Live Demo:**
https://bone-health-ai-6sunz4xsbqppzi6mbbduzv.streamlit.app/

</div>

---

# Why This Project?

Postpartum recovery involves multiple physical and nutritional factors that can influence overall bone health.

A conventional application may simply display a risk category.

This project focuses on a more useful workflow:

```text
User Health Information
          ↓
Data Processing
          ↓
Machine Learning Model
          ↓
Risk Classification
          ↓
SHAP Explanation
          ↓
Visual Insights
          ↓
PDF Assessment Report
```

The goal is to demonstrate how machine learning can be integrated into an **interactive, explainable application** rather than remaining as an isolated model-training notebook.

---

# Key Features

<table>
<tr>
<td width="50%">

### 🧠 Machine Learning

* Random Forest classification
* Low / Medium / High risk prediction
* Structured health-data processing
* Model loaded directly into the application

</td>

<td width="50%">

### 🔍 Explainable AI

* SHAP-based explanations
* Feature contribution analysis
* Visual interpretation of model output
* Helps users understand prediction factors

</td>
</tr>

<tr>
<td>

### 📊 Interactive Application

* Streamlit web interface
* Interactive user inputs
* Real-time prediction
* Visual results

</td>

<td>

### 📄 PDF Reporting

* Automated assessment report
* Patient-specific input summary
* Prediction results
* Generated directly from the application

</td>
</tr>
</table>

---

# Machine Learning Workflow

The application follows a structured machine-learning pipeline:

```text
                 ┌─────────────────────┐
                 │   Health Information │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Data Processing   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Random Forest     │
                 │   Classification    │
                 └──────────┬──────────┘
                            │
                            ▼
              ┌─────────────────────────────┐
              │      Risk Classification    │
              │                             │
              │   LOW  •  MEDIUM  •  HIGH  │
              └──────────────┬──────────────┘
                             │
                             ▼
                 ┌─────────────────────┐
                 │   SHAP Explanation  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   PDF Report        │
                 └─────────────────────┘
```

---

# Explainable AI with SHAP

One of the main aspects of this project is that the model output is not treated as a black box.

The application uses **SHAP (SHapley Additive exPlanations)** to analyze feature contributions to the model prediction.

This provides an additional layer of interpretability:

```text
                    Prediction
                       │
                       ▼
              ┌─────────────────┐
              │ Random Forest    │
              └────────┬────────┘
                       │
                       ▼
                Model Prediction
                       │
                       ▼
              ┌─────────────────┐
              │      SHAP       │
              │   Explanation   │
              └────────┬────────┘
                       │
                       ▼
          Feature Contribution Analysis
```

This makes the project more than a simple classification interface by demonstrating the practical use of **Explainable AI**.

---

# Risk Classification

The model produces three risk categories:

| Risk Level | Meaning                                              |
| ---------- | ---------------------------------------------------- |
| **Low**    | Lower predicted risk based on the provided inputs    |
| **Medium** | Moderate predicted risk based on the provided inputs |
| **High**   | Higher predicted risk based on the provided inputs   |

The prediction is generated from the trained machine-learning model using the information entered into the application.

---

# PDF Assessment Reports

The application can generate a structured PDF assessment report directly from the entered information.

The report can include:

* Assessment information
* Entered health parameters
* Predicted risk category
* Model-based insights
* Assessment timestamp

PDF generation is implemented using **ReportLab**.

---

# Technology Stack

<div align="center">

### Programming & Application

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge\&logo=streamlit\&logoColor=white)

### Data & Machine Learning

![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge\&logo=pandas\&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge\&logo=numpy\&logoColor=white)
![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge\&logo=scikit-learn\&logoColor=white)

### Explainability & Visualization

![SHAP](https://img.shields.io/badge/SHAP-Explainable%20AI-8E44AD?style=for-the-badge)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge\&logo=python\&logoColor=white)

### Reporting

![ReportLab](https://img.shields.io/badge/ReportLab-PDF%20Generation-B71C1C?style=for-the-badge)

</div>

---

# Project Architecture

```text
bone-health-ai/
│
├─
```
