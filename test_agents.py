"""
Test script for diagnosing issues with Medical Agents
"""

import os
import sys
from pprint import pprint

# Ensure we're working from the project root
project_root = os.path.abspath(os.path.dirname(__file__))
os.chdir(project_root)

# Import the agents
try:
    from Utils.Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
    print("Successfully imported agents")
except Exception as e:
    print(f"Error importing agents: {e}")
    sys.exit(1)

def test_specialist_agent(agent_class, name, test_input="I'm experiencing chest pain and shortness of breath"):
    """Test an individual specialist agent"""
    print(f"\n--- Testing {name} Agent ---")
    try:
        agent = agent_class(test_input)
        print(f"Created {name} agent")
        
        print(f"Running {name} agent...")
        response = agent.run()
        
        print(f"{name} Response:")
        print("-" * 40)
        print(response)
        print("-" * 40)
        
        return response
    except Exception as e:
        print(f"Error with {name} agent: {e}")
        return None

def test_team_agent(specialist_responses):
    """Test the multidisciplinary team agent"""
    print("\n--- Testing MultidisciplinaryTeam Agent ---")
    try:
        team_agent = MultidisciplinaryTeam(
            cardiologist_report=specialist_responses.get("Cardiologist", "No report"),
            psychologist_report=specialist_responses.get("Psychologist", "No report"),
            pulmonologist_report=specialist_responses.get("Pulmonologist", "No report")
        )
        print("Created MultidisciplinaryTeam agent")
        
        print("Running MultidisciplinaryTeam agent...")
        response = team_agent.run()
        
        print("Team Response:")
        print("-" * 40)
        print(response)
        print("-" * 40)
        
        return response
    except Exception as e:
        print(f"Error with MultidisciplinaryTeam agent: {e}")
        return None

def main():
    """Run the tests"""
    # Check Python environment
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    
    # Use a consistent test input
    test_input = """
    Patient presents with the following symptoms:
    - Chest pain described as sharp and stabbing, especially when breathing deeply
    - Shortness of breath when walking up stairs
    - Feeling anxious and worried about health
    - Trouble sleeping for the past week
    - No previous medical conditions
    - No medications
    - Non-smoker
    """
    
    # Test each specialist agent
    specialist_responses = {}
    
    # Test Cardiologist
    cardiologist_response = test_specialist_agent(Cardiologist, "Cardiologist", test_input)
    if cardiologist_response:
        specialist_responses["Cardiologist"] = cardiologist_response
    
    # Test Psychologist
    psychologist_response = test_specialist_agent(Psychologist, "Psychologist", test_input)
    if psychologist_response:
        specialist_responses["Psychologist"] = psychologist_response
    
    # Test Pulmonologist
    pulmonologist_response = test_specialist_agent(Pulmonologist, "Pulmonologist", test_input)
    if pulmonologist_response:
        specialist_responses["Pulmonologist"] = pulmonologist_response
    
    # Test MultidisciplinaryTeam agent if we have specialist responses
    if specialist_responses:
        team_response = test_team_agent(specialist_responses)
        if team_response:
            print("\n--- Final Diagnosis ---")
            print(team_response)
    else:
        print("No specialist responses to analyze")

if __name__ == "__main__":
    main() 