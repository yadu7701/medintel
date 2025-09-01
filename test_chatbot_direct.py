"""
Test script for diagnosing issues with the Medical Chatbot
"""

import os
import sys
import traceback

# Ensure we're working from the project root
project_root = os.path.abspath(os.path.dirname(__file__))
os.chdir(project_root)

# Add the project root to the Python path
sys.path.insert(0, project_root)

try:
    from Utils.Chatbot import MedicalChatbot
    print("Successfully imported MedicalChatbot")
except Exception as e:
    print(f"Error importing MedicalChatbot: {e}")
    print("Traceback:")
    traceback.print_exc()
    sys.exit(1)

def test_chatbot():
    """Test the chatbot's functionality"""
    try:
        print("Initializing MedicalChatbot...")
        chatbot = MedicalChatbot()
        print("MedicalChatbot initialized successfully")
        
        # Test basic response
        print("\n--- Testing basic response ---")
        try:
            response = chatbot.get_response("Hello, I need medical advice.")
            print("Response:")
            print("-" * 40)
            print(response)
            print("-" * 40)
        except Exception as e:
            print(f"Error testing basic response: {e}")
            traceback.print_exc()
        
        # Test symptom processing
        print("\n--- Testing symptom processing ---")
        symptoms = """
        I've been experiencing chest pain and shortness of breath for 3 days.
        The pain is sharp and gets worse when I breathe deeply.
        I also feel anxious about my health situation.
        I'm having trouble sleeping and sometimes feel dizzy.
        """
        
        try:
            print("Processing symptoms...")
            response = chatbot.get_response(symptoms)
            print("Response:")
            print("-" * 40)
            print(response)
            print("-" * 40)
        except Exception as e:
            print(f"Error processing symptoms: {e}")
            traceback.print_exc()
        
        # Test treatment query
        print("\n--- Testing treatment query ---")
        try:
            response = chatbot.get_response("What treatment do you recommend for my condition?")
            print("Response:")
            print("-" * 40)
            print(response)
            print("-" * 40)
        except Exception as e:
            print(f"Error with treatment query: {e}")
            traceback.print_exc()
        
        # Test doctor recommendation
        print("\n--- Testing doctor recommendation ---")
        try:
            response = chatbot.get_response("Should I see a doctor about these symptoms?")
            print("Response:")
            print("-" * 40)
            print(response)
            print("-" * 40)
        except Exception as e:
            print(f"Error with doctor recommendation: {e}")
            traceback.print_exc()
            
    except Exception as e:
        print(f"Error in chatbot testing: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    # Print environment information
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    test_chatbot() 