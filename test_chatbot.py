from Utils.Chatbot import MedicalChatbot

def test_chatbot():
    print("Initializing Medical Chatbot...")
    chatbot = MedicalChatbot()
    
    # Test basic response
    print("\nTesting basic response...")
    response = chatbot.get_response("Hello, I need medical advice.")
    print("Response:", response)
    
    # Test symptom processing
    print("\nTesting symptom processing...")
    symptoms = """
    I've been experiencing chest pain and shortness of breath for the past 2 days.
    The pain is sharp and gets worse when I take deep breaths.
    I also feel anxious and have trouble sleeping.
    """
    response = chatbot.get_response(symptoms)
    print("Response:", response)
    
    # Test treatment query
    print("\nTesting treatment query...")
    response = chatbot.get_response("What treatment do you recommend?")
    print("Response:", response)
    
    # Test doctor recommendation
    print("\nTesting doctor recommendation...")
    response = chatbot.get_response("Should I see a doctor?")
    print("Response:", response)

if __name__ == "__main__":
    test_chatbot() 