import openai
import os
import speech_recognition as sr
#Use amazon poly tts for human like voice
from gtts import gTTS

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
openai.api_key = ''

def generate_response(prompt, context=None):
    full_prompt = context + "\n" + prompt if context else prompt

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=full_prompt,
        max_tokens=150,
        temperature=0.7,
        n=1
    )

    return response.choices[0].text.strip()

def text_to_speech(text, filename='output.mp3'):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(filename)
    os.system(f"start {filename}")

def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def main():
    #Context will be updated with data received from the analytical AI integrated with Ecostruxure.
    context = "In an industrial environment. The response should be like a voice assistant. Simulate a scenario in which when a person asks the AI model to tell him about the current status of the plant, it will give various analytical status regarding the operation, will tell him about some of the key decisions to be taken on that day, the AI algorithm has predicted that the Furnace 10 is going to exceed pollution limit due to the clog in the valve 2 near the inlet, ask him to replace the valve within 10 days."

    while True:
        print("\nYou can speak or type 'exit' to end the conversation.")
        
        # Use ASR to get user input
        user_input = speech_to_text()

        if user_input.lower() == 'exit':
            print("Exiting conversation.")
            break

        # Generate GPT response
        gpt_response = generate_response(user_input, context)

        # Display GPT response
        print(f"GPT: {gpt_response}")

        # Use TTS to play GPT response
        text_to_speech(gpt_response)

if __name__ == "__main__":
    main()
