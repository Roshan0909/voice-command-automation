import speech_recognition as sr
import subprocess
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Configure the API with the provided key
genai.configure(api_key=API_KEY)

# Function to capture voice command using speech recognition
def capture_voice_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)  # Listen for up to 10 seconds

        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None

# Function to generate the Python script using the voice command
def generate_script(voice_command):
    prompt = f"""
    Generate a Python script to perform the following task:
    Task: {voice_command}

    Instructions:
    - Write clear and concise Python code for this task.
    - Don't give an explanation of the code.
    - Handle potential errors gracefully.
    """

    try:
        # Initialize the model (using Gemini)
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Generate content based on the prompt
        response = model.generate_content(prompt)
        
        # Remove any markdown syntax
        clean_script = response.text.replace("```python", "").replace("```", "").strip()
        print("Generated Python Script:\n", clean_script)

        return clean_script

    except Exception as e:
        print(f"Error generating script: {e}")
        return None

# Function to execute the generated script
def execute_script(script):
    with open('temp_script.py', 'w') as f:
        f.write(script)

    subprocess.run(['python', 'temp_script.py'], check=True)  # Execute the script

# Main function that will run the loop and listen for voice commands
def main():
    print("Say 'exit' to stop.")
    while True:
        voice_command = capture_voice_command()
        if voice_command:
            if voice_command.lower() == 'exit':
                print("Exiting...")
                break

            script = generate_script(voice_command)
            if script:
                print("Executing generated script...")
                execute_script(script)
            else:
                print("Script generation failed; skipping execution.")

if __name__ == '__main__':
    main()
