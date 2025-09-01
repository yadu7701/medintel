# MedIntel 🧠⚕️  
**Multidisciplinary Medical Reasoning System with Agentic Intelligence**

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
