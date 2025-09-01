
# MedIntel 🧠⚕️  
**Multidisciplinary Medical Reasoning System with Agentic Intelligence**

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)  
![Flask](https://img.shields.io/badge/Flask-Framework-lightgrey?logo=flask)  
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-RandomForest-green)  
![Status](https://img.shields.io/badge/Status-Research%20%26%20Education-orange)  
![License](https://img.shields.io/badge/License-Academic-lightblue)  

---

## 📌 Overview
**MedIntel** is an AI-powered project for medical diagnostics and reasoning.  
It combines specialist AI agents (**Cardiologist, Psychologist, Pulmonologist**) with a **Multidisciplinary Team Agent** to analyze medical reports and produce a final diagnosis.  

The system supports two main workflows:
- **Standalone script (`Main.py`)** → Process a medical report and save the final diagnosis.  
- **Flask Web App (`app.py`)** → Upload reports, chat with the AI, and receive treatment + doctor recommendations.  

An additional module (`random_forest_example.py`) demonstrates how to integrate traditional ML (**Random Forest**) with medical data.  

⚠️ **Disclaimer**: This project is for **research and educational purposes only**. It is **not a substitute** for professional medical advice, diagnosis, or treatment.  

---

## ✨ Features
- 📂 Upload and analyze medical reports (`.txt` / `.pdf`)  
- 🫀 Specialist agents: **Cardiologist, Psychologist, Pulmonologist**  
- 🧑‍⚕️ Multidisciplinary Team Agent for integrated diagnosis  
- 💬 Chatbot interface for Q&A, treatment suggestions, and doctor recommendations  
- ⚡ Concurrent execution for faster analysis  
- 🌲 Random Forest ML example for structured medical datasets  
- 🧪 Test scripts included for agents and chatbot  

---

## 🛠️ Tech Stack
- **Language**: Python 3.9+  
- **Backend**: Flask  
- **AI Agents**: Custom rule/LLM-powered agents (`Utils/`)  
- **Libraries**:  
  - Core: `Flask`, `PyPDF2`, `langchain`, `reportlab`  
  - ML (optional): `scikit-learn`, `pandas`, `numpy`, `matplotlib`, `seaborn`  
- **Concurrency**: `ThreadPoolExecutor`  
- **Environment**: API keys loaded from `apikey.env`  

---

## 📂 Repository Structure
```

MedIntel/
│── app.py                   # Flask web backend
│── Main.py                  # Standalone script for medical report analysis
│── random\_forest\_example.py # Random Forest demo for medical data
│── Utils/
│   ├── Agents.py            # Specialist AI agents
│   ├── Chatbot.py           # Chatbot logic
│── templates/
│   ├── index.html           # Homepage UI
│   ├── chat.html            # Chatbot interface
│── Medical Reports/         # Sample input reports
│── results/                 # Diagnosis outputs
│── tests/
│   ├── test\_agents.py       # Test specialist agents
│   ├── test\_chatbot.py      # Test chatbot functionality
│   ├── test\_chatbot\_direct.py
│── requirements.txt         # Core dependencies
│── requirements\_ml.txt      # ML dependencies (optional)
│── apikey.env               # API key configuration
│── README.md                # Documentation

````

---

## 🚀 Getting Started

### 1️⃣ Clone the repository
```bash
git clone https://github.com/your-username/MedIntel.git
cd MedIntel
````

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

For ML demo (Random Forest):

```bash
pip install -r requirements_ml.txt
```

### 3️⃣ Add your API Key

Create a file named `apikey.env`:

```bash
APIKEY="your_api_key_here"
ORGID="your_org_id_here"
```

---

## ▶️ Usage

### Run as Flask Web App

```bash
python app.py
```

Then open 👉 `http://127.0.0.1:5000/` in your browser.

### Run as Standalone Script

```bash
python Main.py
```

### Run the Random Forest Example

```bash
python random_forest_example.py
```

---

## 📡 API Endpoints (from `app.py`)

* `/` → Homepage
* `/chat` → Chatbot UI
* `POST /api/chat` → Send message to chatbot
* `GET /api/treatment` → Get treatment recommendations
* `GET /api/doctor` → Get doctor recommendation
* `POST /analyze` → Upload and analyze medical report (TXT/PDF)
* `GET /clear_session` → Reset chatbot session

---

## 🧪 Running Tests

Agent tests:

```bash
python tests/test_agents.py
```

Chatbot tests:

```bash
python tests/test_chatbot.py
python tests/test_chatbot_direct.py
```

---

## 📖 Future Enhancements

* ➕ Add more medical specialties (neurology, endocrinology, etc.)
* 🩻 Support **multi-modal input** (reports + medical images)
* ☁️ Deploy as a **cloud-based service with authentication**
* 🔗 Deeper integration with **EHR systems**

---

```

---

