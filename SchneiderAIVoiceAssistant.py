import openai
import os
import speech_recognition as sr
from gtts import gTTS  # Use the Google Text-to-Speech library for speech synthesis

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
openai.api_key = 'YOUR_API_KEY'

# Function to generate a response using the OpenAI GPT-3 model
def generate_response(prompt, context=None):
    # Combine the user input and context for a comprehensive prompt
    full_prompt = context + "\n" + prompt if context else prompt

    # Request a completion from the OpenAI GPT-3 model
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        max_tokens=150,
        temperature=0.7,
        n=1
    )

    # Extract and return the generated text from the response
    return response.choices[0].text.strip()

# Function to convert text to speech using the Google Text-to-Speech library
def text_to_speech(text, filename='output.mp3'):
    # Create a gTTS object with the specified text and language
    tts = gTTS(text=text, lang='en', slow=False)
    # Save the synthesized speech to a file
    tts.save(filename)
    # Play the generated speech using the default audio player
    os.system(f"start {filename}")

# Function to convert speech to text using the SpeechRecognition library
def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        # Listen to audio from the microphone and store it
        audio = recognizer.listen(source)

    try:
        # Use Google Speech Recognition to convert audio to text
        user_input = recognizer.recognize_google(audio)
        print(f"You: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

# Main function to orchestrate the conversation
def main():
    # Context will be updated with data received from the analytical AI integrated with Ecostruxure.
    context = "In an industrial environment. The response should be like a voice assistant. Simulate a scenario in which when a person asks the AI model to tell him about the current status of the plant, it will give various analytical status regarding the operation, will tell him about some of the key decisions to be taken on that day, the AI algorithm has predicted that the Furnace 10 is going to exceed pollution limit due to the clog in the valve 2 near the inlet, ask him to replace the valve within 10 days."

    while True:
        print("\nYou can speak or type 'exit' to end the conversation.")

        # Use Automatic Speech Recognition (ASR) to get user input
        user_input = speech_to_text()

        if user_input.lower() == 'exit':
            print("Exiting conversation.")
            break

        # Generate GPT response based on user input and context
        gpt_response = generate_response(user_input, context)

        # Display GPT response
        print(f"GPT: {gpt_response}")

        # Use Text-to-Speech (TTS) to play GPT response
        text_to_speech(gpt_response)

# Entry point to the script
if __name__ == "__main__":
    main()
