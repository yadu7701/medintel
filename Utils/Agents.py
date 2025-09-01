from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama

class Agent:
    def __init__(self, medical_report=None, role=None, extra_info=None):
        self.medical_report = medical_report
        self.role = role
        self.extra_info = extra_info
        # Initialize the prompt based on role and other info
        self.prompt_template = self.create_prompt_template()
        # Initialize the model using Ollama with MedLLaMA2
        self.model = Ollama(model="medllama2")

    def create_prompt_template(self):
        if self.role == "MultidisciplinaryTeam":
            templates = f"""
                You are a multidisciplinary medical team leader synthesizing specialist reports.
                
                Given Reports:
                Cardiologist Report: {self.extra_info.get('cardiologist_report', '')}
                Psychologist Report: {self.extra_info.get('psychologist_report', '')}
                Pulmonologist Report: {self.extra_info.get('pulmonologist_report', '')}
                
                IMPORTANT: Create a concise, accurate final diagnosis based ONLY on information explicitly mentioned in the specialist reports. DO NOT assume or invent any conditions not specifically mentioned in the reports.
                
                Please provide a brief analysis in this format:
                
                [Brief 1-3 sentence summary of the main findings and recommendations]
                • [Key finding 1]
                • [Key finding 2 (if present)]
                • [Key recommendation(s)]
                
                Your final diagnosis should be under 100 words total.
            """
        else:
            templates = {
                "Cardiologist": """
                    You are a cardiologist examining a patient report.
                    
                    Patient Report: {medical_report}
                    
                    IMPORTANT INSTRUCTIONS:
                    1. Analyze ONLY cardiovascular symptoms and concerns EXPLICITLY mentioned in this report
                    2. DO NOT assume or invent any medical history, conditions, or test results
                    3. If no cardiac symptoms are mentioned, clearly state this
                    4. Keep your report under 50 words
                    5. Be factual and avoid speculation
                    
                    Format your brief analysis as:
                    [1-2 sentences summarizing cardiac findings and recommendations only]
                """,
                "Psychologist": """
                    You are a psychologist examining a patient report.
                    
                    Patient Report: {medical_report}
                    
                    IMPORTANT INSTRUCTIONS:
                    1. Analyze ONLY psychological/behavioral symptoms EXPLICITLY mentioned in this report
                    2. DO NOT assume or invent any medical history, conditions, or test results
                    3. If no psychological symptoms are mentioned, clearly state this
                    4. Keep your report under 50 words
                    5. Be factual and avoid speculation
                    
                    Format your brief analysis as:
                    [1-2 sentences summarizing psychological findings and recommendations only]
                """,
                "Pulmonologist": """
                    You are a pulmonologist examining a patient report.
                    
                    Patient Report: {medical_report}
                    
                    IMPORTANT INSTRUCTIONS:
                    1. Analyze ONLY respiratory symptoms and concerns EXPLICITLY mentioned in this report
                    2. DO NOT assume or invent any medical history, conditions, or test results
                    3. If no respiratory symptoms are mentioned, clearly state this
                    4. Keep your report under 50 words
                    5. Be factual and avoid speculation
                    
                    Format your brief analysis as:
                    [1-2 sentences summarizing respiratory findings and recommendations only]
                """
            }
        templates = templates[self.role] if not isinstance(templates, str) else templates
        return PromptTemplate.from_template(templates)
    
    def run(self):
        print(f"{self.role} is running...")
        prompt = self.prompt_template.format(medical_report=self.medical_report)
        try:
            response = self.model.invoke(prompt)
            # Post-process the response to ensure it's brief and focused
            if self.role != "MultidisciplinaryTeam":
                # Limit specialist reports to 50 words
                words = response.split()
                if len(words) > 60:  # Allow a bit of buffer
                    response = " ".join(words[:60]) + "..."
            else:
                # Limit team diagnosis to 100 words
                words = response.split()
                if len(words) > 120:  # Allow a bit of buffer
                    response = " ".join(words[:120]) + "..."
            return response
        except Exception as e:
            print("Error occurred:", e)
            if self.role == "Cardiologist":
                return "No cardiovascular findings or concerns identified in the provided report."
            elif self.role == "Psychologist":
                return "No psychological symptoms or concerns identified in the provided report."
            elif self.role == "Pulmonologist":
                return "No respiratory findings or concerns identified in the provided report."
            else:
                return "Unable to generate a diagnosis due to insufficient information."

# Define specialized agent classes
class Cardiologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Cardiologist")

class Psychologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Psychologist")

class Pulmonologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Pulmonologist")

class MultidisciplinaryTeam(Agent):
    def __init__(self, cardiologist_report, psychologist_report, pulmonologist_report):
        extra_info = {
            "cardiologist_report": cardiologist_report,
            "psychologist_report": psychologist_report,
            "pulmonologist_report": pulmonologist_report
        }
        super().__init__(role="MultidisciplinaryTeam", extra_info=extra_info)
