from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
import sys
import os

# Handle imports properly whether file is run directly or imported as a module
if __name__ == "__main__":
    # Add the project root to the Python path when run directly
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
else:
    # Use relative import when imported as a module
    from .Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam

class MedicalChatbot:
    def __init__(self):
        self.memory = ConversationBufferMemory()
        self.model = Ollama(model="medllama2")
        self.current_diagnosis = None
        self.specialist_reports = None
        
        # Initialize the conversation prompt with strong anti-hallucination guidance
        self.prompt = PromptTemplate(
            input_variables=["history", "input"],
            template="""You are a medical AI assistant. Your primary goal is accuracy.

Previous conversation:
{history}

Current user input: {input}

CRITICAL INSTRUCTIONS:
1. ONLY discuss symptoms and conditions that the user has EXPLICITLY mentioned
2. NEVER assume medical conditions, history, or test results
3. If you don't know something, clearly say so
4. Keep your responses brief and focused
5. When discussing an ailment mentioned by the user, limit yourself to basic information

When replying:
- If the user hasn't described symptoms, ask for them
- Do not diagnose specific conditions unless they were explicitly mentioned by the user
- Avoid using medical jargon without explanation
- If the user asks about a condition they haven't mentioned symptoms for, provide general information without assuming they have it

Your responses should be factual, brief, and avoid creating anxiety.

Response:"""
        )
        
        # Create the conversation chain
        self.conversation = ConversationChain(
            llm=self.model,
            memory=self.memory,
            prompt=self.prompt,
            verbose=True
        )

    def process_symptoms(self, symptoms):
        """Process symptoms through medical agents and get diagnosis"""
        # First, validate and structure the symptoms with anti-hallucination prompting
        symptom_prompt = f"""
        Analyze the following patient report and extract ONLY symptoms that are EXPLICITLY mentioned:
        {symptoms}
        
        IMPORTANT INSTRUCTIONS:
        1. ONLY list symptoms explicitly mentioned by the patient
        2. DO NOT add or assume any symptoms, conditions, or medical history
        3. DO NOT include symptoms that might "typically" occur but aren't mentioned
        4. Structure the symptoms in a clear, concise format
        5. If a symptom category has no information, state "No information provided"
        
        Primary symptoms: 
        Secondary symptoms:
        Duration (if mentioned):
        Severity (if mentioned):
        Associated factors (if mentioned):
        """
        
        structured_symptoms = self.model.invoke(symptom_prompt)
        
        # Initialize agents with the structured symptoms
        agents = {
            "Cardiologist": Cardiologist(structured_symptoms),
            "Psychologist": Psychologist(structured_symptoms),
            "Pulmonologist": Pulmonologist(structured_symptoms)
        }
        
        # Get responses from all agents
        responses = {}
        for name, agent in agents.items():
            response = agent.run()
            responses[name] = response
        
        # Get team analysis
        team_agent = MultidisciplinaryTeam(
            cardiologist_report=responses["Cardiologist"],
            psychologist_report=responses["Psychologist"],
            pulmonologist_report=responses["Pulmonologist"]
        )
        
        final_diagnosis = team_agent.run()
        
        # Validate the diagnosis for consistency and prevent hallucination
        validation_prompt = f"""
        Review this medical analysis for accuracy and hallucination:
        {final_diagnosis}
        
        IMPORTANT INSTRUCTIONS:
        1. Remove any statements not directly supported by the specialist reports
        2. Check if the analysis invents or assumes any conditions not explicitly mentioned
        3. Ensure all recommendations follow directly from the mentioned symptoms
        4. Make the response concise (max 100 words)
        5. Avoid diagnostic terms unless clearly supported
        
        Corrected analysis:
        """
        
        validated_diagnosis = self.model.invoke(validation_prompt)
        
        # Store the validated diagnosis and reports
        self.current_diagnosis = validated_diagnosis
        self.specialist_reports = responses
        
        return validated_diagnosis

    def get_response(self, user_input):
        """Get response from the chatbot"""
        # Check for specific condition queries like flu
        specific_condition_match = self._check_for_specific_condition(user_input)
        if specific_condition_match:
            condition = specific_condition_match
            return self._get_condition_info(condition)
            
        # Check if the input is describing new symptoms
        if self._is_symptom_description(user_input):
            # Process new symptoms
            diagnosis = self.process_symptoms(user_input)
            return f"""Based on your described symptoms:

{diagnosis}

How can I help you further?"""
        
        # Handle follow-up questions about treatment or doctor visits
        if self._is_treatment_query(user_input) and not self.current_diagnosis:
            return """I can't provide treatment recommendations without knowing your symptoms. 

What symptoms are you experiencing? Please be specific about what you're feeling."""
        
        if self._is_doctor_query(user_input) and not self.current_diagnosis:
            return """To advise about seeing a doctor, I need to know your symptoms first.

What symptoms are you experiencing, and how long have they been present?"""
        
        # Use the conversation chain for follow-up questions
        response = self.conversation.predict(input=user_input)
        return response

    def _check_for_specific_condition(self, text):
        """Check if the user is asking about a specific condition"""
        # Common conditions that might be directly asked about
        conditions = {
            "flu": ["flu", "influenza"],
            "cold": ["cold", "common cold"],
            "covid": ["covid", "coronavirus", "covid-19", "covid19"],
            "headache": ["headache", "migraine"],
            "stomach": ["stomach ache", "stomach pain", "stomachache", "indigestion"],
            "allergy": ["allergy", "allergic", "allergies"],
            "fever": ["fever", "high temperature"]
        }
        
        text_lower = text.lower()
        
        # Check for direct questions about symptoms
        for condition, terms in conditions.items():
            for term in terms:
                if any(pattern in text_lower for pattern in [
                    f"symptoms of {term}",
                    f"signs of {term}",
                    f"what is {term}",
                    f"what are {term} symptoms",
                    f"how do i know if i have {term}",
                    f"do i have {term}"
                ]):
                    return condition
        
        # Check for phrases like "treatment for X" or "what about X"
        for condition, terms in conditions.items():
            for term in terms:
                if any(pattern in text_lower for pattern in [
                    f"treatment for {term}", 
                    f"treatment option for {term}",
                    f"what about {term}",
                    f"info on {term}",
                    f"about {term}",
                    f"if i have {term}",
                    f"{term} treatment",
                    f"{term} remedy",
                    f"{term} medicine"
                ]):
                    return condition
        
        return None
        
    def _get_condition_info(self, condition):
        """Get information about a specific condition without requiring symptoms"""
        condition_prompt = f"""
        Provide brief information about {condition}, including:
        
        1. Common symptoms (list these first and in detail)
        2. Basic home care recommendations
        3. When to see a doctor
        
        Keep this concise (under 100 words) and focus ONLY on {condition}.
        Do NOT mention other conditions or assume the patient has any other conditions.
        Start with the symptoms since that's what users are most interested in.
        """
        
        response = self.model.invoke(condition_prompt)
        
        # Limit response length
        words = response.split()
        if len(words) > 120:
            response = " ".join(words[:120]) + "..."
            
        return response

    def _is_symptom_description(self, text):
        """Check if the input appears to be describing symptoms"""
        symptom_keywords = [
            # Physical symptoms
            "pain", "ache", "sore", "discomfort", "pressure", "tight",
            "numb", "tingling", "burning", "sharp", "dull", "throbbing",
            "fever", "chill", "sweat", "fatigue", "tired", "weak",
            "dizzy", "faint", "nausea", "vomit", "diarrhea", "constipation",
            "cough", "breath", "wheeze", "chest", "heart", "palpitation",
            "stomach", "headache", "migraine", "vision", "hearing",
            "rash", "itch", "swelling", "bleeding", "bruise",
            
            # Psychological symptoms
            "anxiety", "stress", "worry", "fear", "panic", "depression",
            "mood", "angry", "irritable", "confused", "memory", "concentration",
            "sleep", "insomnia", "nightmare", "appetite", "energy",
            
            # Descriptive terms
            "symptom", "feel", "experiencing", "notice", "problem",
            "condition", "issue", "concern", "worse", "better",
            "started", "developed", "changed", "constant", "intermittent"
        ]
        
        text = text.lower()
        # Check for symptom keywords
        has_keywords = any(keyword in text for keyword in symptom_keywords)
        
        # Check for temporal markers that often indicate symptom descriptions
        temporal_markers = ["since", "for", "days", "weeks", "months", "years", "today", "yesterday"]
        has_temporal = any(marker in text for marker in temporal_markers)
        
        return has_keywords or has_temporal
    
    def _is_treatment_query(self, text):
        """Check if the input is asking about treatments"""
        treatment_keywords = [
            "treatment", "cure", "medicine", "medication", "drug", "pill", 
            "remedy", "heal", "therapy", "therapies", "care"
        ]
        
        text = text.lower()
        return any(keyword in text for keyword in treatment_keywords)
    
    def _is_doctor_query(self, text):
        """Check if the input is asking about seeing a doctor"""
        doctor_keywords = [
            "doctor", "physician", "specialist", "hospital", "clinic", 
            "appointment", "visit", "consult", "consultation"
        ]
        
        text = text.lower()
        return any(keyword in text for keyword in doctor_keywords)

    def get_treatment_recommendations(self):
        """Get treatment recommendations based on current diagnosis"""
        if not self.current_diagnosis:
            return "I don't have any current diagnosis to provide treatment recommendations for. Please describe your symptoms first."
        
        prompt = f"""Based on the following diagnosis, provide specific treatment recommendations:
        Diagnosis: {self.current_diagnosis}
        
        Please include:
        1. Immediate actions
        2. Medications (if applicable)
        3. Lifestyle changes
        4. When to seek emergency care
        5. Follow-up recommendations"""
        
        return self.model.invoke(prompt)

    def get_doctor_recommendation(self):
        """Get recommendation about seeing a doctor"""
        if not self.current_diagnosis:
            return "I don't have any current diagnosis to provide doctor visit recommendations for. Please describe your symptoms first."
        
        prompt = f"""Based on the following diagnosis, should the patient see a doctor?
        Diagnosis: {self.current_diagnosis}
        
        Please provide:
        1. Whether a doctor visit is necessary
        2. Urgency level (immediate, soon, routine)
        3. Which type of doctor to see
        4. What to bring to the appointment"""
        
        return self.model.invoke(prompt) 