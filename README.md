MedIntel 🧠⚕️
Multidisciplinary Medical Reasoning System with Agentic Intelligence
📌 Overview
MedIntel is an AI-powered project for medical diagnostics and reasoning. It combines specialist AI agents (Cardiologist, Psychologist, Pulmonologist) with a Multidisciplinary Team Agent to analyze medical reports and produce a final diagnosis.

The system supports two main workflows:
- Standalone script (Main.py) → Process a medical report and save the final diagnosis.
- Flask Web App (app.py) → Upload reports, chat with the AI, and receive treatment + doctor recommendations.

An additional module, random_forest_example.py, demonstrates integrating traditional ML (Random Forest) with medical data.

⚠️ Disclaimer: This project is for research and educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.
✨ Features
    • • Upload and analyze medical reports (.txt / .pdf)
    • • Specialist agents: Cardiologist, Psychologist, Pulmonologist
    • • Multidisciplinary Team Agent for integrated diagnosis
    • • Chatbot interface for follow-up Q&A, treatment suggestions, and doctor recommendations
    • • Concurrent execution for faster analysis
    • • Random Forest ML example for structured medical datasets
    • • Test scripts included for agents and chatbot
🛠️ Tech Stack
- Language: Python 3.9+
- Backend: Flask
- AI Agents: Custom rule/LLM-powered agents (Utils/)
- Libraries:
  • Core: Flask, PyPDF2, langchain, reportlab
  • ML (optional): scikit-learn, pandas, numpy, matplotlib, seaborn
- Concurrency: ThreadPoolExecutor
- Environment: API keys loaded from apikey.env
📂 Repository Structure
MedIntel/
│── app.py                   # Flask web backend
│── Main.py                  # Standalone script for medical report analysis
│── random_forest_example.py # Random Forest demo for medical data
│── Utils/
│   ├── Agents.py            # Specialist AI agents
│   ├── Chatbot.py           # Chatbot logic
│── templates/
│   ├── index.html           # Homepage UI
│   ├── chat.html            # Chatbot interface
│── Medical Reports/         # Sample input reports
│── results/                 # Diagnosis outputs
│── tests/
│   ├── test_agents.py       # Test specialist agents
│   ├── test_chatbot.py      # Test chatbot functionality
│   ├── test_chatbot_direct.py
│── requirements.txt         # Core dependencies
│── requirements_ml.txt      # ML dependencies (optional)
│── apikey.env               # API key configuration
│── README.md                # Documentation
🚀 Getting Started
1️⃣ Clone the repository:
git clone https://github.com/your-username/MedIntel.git
cd MedIntel
2️⃣ Install dependencies:
pip install -r requirements.txt
For ML demo (Random Forest):
pip install -r requirements_ml.txt
3️⃣ Add your API Key in apikey.env:
APIKEY="your_api_key_here"
ORGID="your_org_id_here"
▶️ Usage
Run as Flask Web App:
python app.py
Then open http://127.0.0.1:5000/ in your browser.
Run as Standalone Script:
python Main.py
Run the Random Forest Example:
python random_forest_example.py
📡 API Endpoints (from app.py)
    • • / → Homepage
    • • /chat → Chatbot UI
    • • POST /api/chat → Send message to chatbot
    • • GET /api/treatment → Get treatment recommendations
    • • GET /api/doctor → Get doctor recommendation
    • • POST /analyze → Upload and analyze medical report (TXT/PDF)
    • • GET /clear_session → Reset chatbot session
🧪 Running Tests
Agent tests:
python test_agents.py
Chatbot tests:
python test_chatbot.py
python test_chatbot_direct.py
📖 Future Enhancements
    • • Add more medical specialties (neurology, endocrinology, etc.)
    • • Support multi-modal input (reports + medical images)
    • • Deploy as a cloud-based service with authentication
    • • Deeper integration with EHR systems
