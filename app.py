from flask import Flask, render_template, request, jsonify, session
from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
from Utils.Chatbot import MedicalChatbot
from concurrent.futures import ThreadPoolExecutor, as_completed
from PyPDF2 import PdfReader
import os
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Dictionary to store chatbot instances
chatbot_instances = {}

# Ensure the upload and results directories exist
UPLOAD_FOLDER = 'Medical Reports'
RESULTS_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

def get_chatbot_instance():
    """Get or create a chatbot instance for the current session"""
    # Check if session has an ID
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    user_id = session['user_id']
    
    # Create a new chatbot instance if one doesn't exist
    if user_id not in chatbot_instances:
        chatbot_instances[user_id] = MedicalChatbot()
    
    return chatbot_instances[user_id]

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")

def read_file_content(file_path):
    """Read content from either PDF or text file"""
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        raise Exception("Unsupported file format. Please upload a PDF or TXT file.")

def process_medical_report(medical_report):
    """Process the medical report through all agents and return the diagnosis"""
    agents = {
        "Cardiologist": Cardiologist(medical_report),
        "Psychologist": Psychologist(medical_report),
        "Pulmonologist": Pulmonologist(medical_report)
    }
    
    # Function to run each agent and get their response
    def get_response(agent_name, agent):
        response = agent.run()
        return agent_name, response

    # Run the agents concurrently and collect responses
    responses = {}
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_response, name, agent): name for name, agent in agents.items()}
        
        for future in as_completed(futures):
            agent_name, response = future.result()
            responses[agent_name] = response

    # Create team analysis
    team_agent = MultidisciplinaryTeam(
        cardiologist_report=responses["Cardiologist"],
        psychologist_report=responses["Psychologist"],
        pulmonologist_report=responses["Pulmonologist"]
    )
    
    # Get final diagnosis
    final_diagnosis = team_agent.run()
    
    # Also update the chatbot's diagnosis if a session exists
    if 'user_id' in session and session['user_id'] in chatbot_instances:
        chatbot = chatbot_instances[session['user_id']]
        chatbot.current_diagnosis = final_diagnosis
        chatbot.specialist_reports = responses
    
    return {
        'specialist_reports': responses,
        'final_diagnosis': final_diagnosis
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    # Create a new chatbot instance for this session if it doesn't exist
    get_chatbot_instance()
    return render_template('chat.html')

@app.route('/api/chat', methods=['POST'])
def chat_message():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Get the chatbot instance for this session
        chatbot = get_chatbot_instance()
        response = chatbot.get_response(user_message)
        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/treatment', methods=['GET'])
def get_treatment():
    try:
        chatbot = get_chatbot_instance()
        response = chatbot.get_treatment_recommendations()
        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/doctor', methods=['GET'])
def get_doctor_recommendation():
    try:
        chatbot = get_chatbot_instance()
        response = chatbot.get_doctor_recommendation()
        return jsonify({
            'success': True,
            'response': response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'report' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['report']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ['.pdf', '.txt']:
        return jsonify({'error': 'Invalid file format. Please upload a PDF or TXT file'}), 400
    
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    try:
        # Read the medical report
        medical_report = read_file_content(file_path)
        
        # Process the report
        results = process_medical_report(medical_report)
        
        # Save the final diagnosis to a file
        diagnosis_filename = f"diagnosis_{os.path.splitext(file.filename)[0]}.txt"
        diagnosis_path = os.path.join(RESULTS_FOLDER, diagnosis_filename)
        with open(diagnosis_path, 'w', encoding='utf-8') as f:
            f.write("### Final Diagnosis:\n\n" + results['final_diagnosis'])
        
        return jsonify({
            'success': True,
            'results': results,
            'diagnosis_file': diagnosis_filename
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

@app.route('/clear_session', methods=['GET'])
def clear_session():
    """Clear the current session data and associated chatbot"""
    if 'user_id' in session and session['user_id'] in chatbot_instances:
        # Remove the chatbot instance
        del chatbot_instances[session['user_id']]
    
    # Clear the session
    session.clear()
    
    return jsonify({'success': True, 'message': 'Session cleared'})

if __name__ == '__main__':
    app.run(debug=True) 