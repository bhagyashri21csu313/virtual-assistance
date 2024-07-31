#!/usr/bin/env python
# coding: utf-8

# In[8]:


pip install speechrecognition


# In[10]:


pip install pyttsx3


# In[13]:


pip install pyttsx3


# In[12]:


pip install wikipedia


# In[17]:


pip install pyaudio


# In[34]:


import speech_recognition as sr
import pyttsx3
import requests
import wikipedia

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
        return query

def fetch_weather(city):
    api_key = "key_no"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        temperature = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        weather_desc = data["weather"][0]["description"]
        return f"Temperature: {temperature}\nPressure: {pressure}\nHumidity: {humidity}\nDescription: {weather_desc}"
    else:
        return "City Not Found"

def fetch_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results

if __name__ == "__main__":
    while True:
        query = listen().lower()
        if 'weather' in query:
            city = query.split("in")[-1].strip()
            weather_info = fetch_weather(city)
            speak(weather_info)
        elif 'wikipedia' in query:
            query = query.replace("wikipedia", "")
            results = fetch_wikipedia(query)
            speak("According to Wikipedia")
            speak(results)
        elif 'exit' in query or 'stop' in query:
            speak("Goodbye!")
            break
        else:
            speak("I can only help with weather and Wikipedia searches at the moment.")


# In[35]:


import speech_recognition as sr
import pyttsx3
import requests
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError, WikipediaException

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
        return query

def fetch_weather(city):
    api_key = "14dfb89aa4d46a580298c85a4b2969b2"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(complete_url)
    data = response.json()
    if response.status_code == 200 and "main" in data:
        main = data["main"]
        temperature = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        weather_desc = data["weather"][0]["description"]
        return f"Temperature: {temperature}\nPressure: {pressure}\nHumidity: {humidity}\nDescription: {weather_desc}"
    elif data.get("message"):
        return f"Error: {data['message']}"
    else:
        return "An unexpected error occurred while fetching the weather information."

def fetch_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        return results
    except DisambiguationError as e:
        return f"Disambiguation error: {e.options}"
    except PageError:
        return "Page not found."
    except WikipediaException as e:
        return f"Wikipedia error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

if __name__ == "__main__":
    while True:
        query = listen().lower()
        if 'weather' in query:
            city = query.split("in")[-1].strip()
            weather_info = fetch_weather(city)
            speak(weather_info)
        elif 'wikipedia' in query:
            query = query.replace("wikipedia", "")
            results = fetch_wikipedia(query)
            speak("According to Wikipedia")
            speak(results)
        elif 'exit' in query or 'stop' in query:
            speak("Goodbye!")
            break
        else:
            speak("I can only help with weather and Wikipedia searches at the moment.")


# In[1]:


pip install googletrans==4.0.0-rc1


# In[ ]:


#Language Codes:
#Google Translate uses ISO 639-1 language codes. Here are some examples:

English: 'en'
Spanish: 'es'
French: 'fr'
German: 'de'
Chinese: 'zh-cn'
Japanese: 'ja'


# In[6]:


from googletrans import Translator

def translate_text(text, src_language, dest_language):
    translator = Translator()
    translation = translator.translate(text, src=src_language, dest=dest_language)
    return translation.text

if __name__ == "__main__":
    source_language = input("Enter the source language code (e.g., 'en' for English): ")
    destination_language = input("Enter the destination language code (e.g., 'es' for Spanish): ")
    text_to_translate = input("Enter the text to translate: ")

    translated_text = translate_text(text_to_translate, source_language, destination_language)
    print(f"Original text: {text_to_translate}")
    print(f"Translated text: {translated_text}")


# In[ ]:


---------------------------------------------------------------------------------------------------------------------------------


# In[11]:


pip install azure-cognitiveservices-speech


# In[18]:


import azure.cognitiveservices.speech as speechsdk

def text_to_speech(subscription_key, region, text):
    try:
        # Create an instance of a speech config with specified subscription key and service region.
        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

        # Set the voice name, refer to https://aka.ms/speech/voices/neural for full list.
        speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

        # Create a speech synthesizer using the default speaker as audio output.
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        # Synthesize the text to speech.
        result = speech_synthesizer.speak_text_async(text).get()

        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you update the subscription info and region correctly?")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Ensure these are correct
    subscription_key = "ead9967ad49248719cb350b9f5b3b608"  # Replace with your subscription key
    region = "eastus"  # Replace with your service region
    text = "Hello, how are you today?"

    text_to_speech(subscription_key, region, text)


# In[19]:


import azure.cognitiveservices.speech as speechsdk

def text_to_speech(ead9967ad49248719cb350b9f5b3b608, eastus, text):
    try:
        # Create an instance of a speech config with specified subscription key and service region.
        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

        # Set the voice name, refer to https://aka.ms/speech/voices/neural for full list.
        speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

        # Create a speech synthesizer using the default speaker as audio output.
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

        # Synthesize the text to speech.
        result = speech_synthesizer.speak_text_async(text).get()

        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you update the subscription info and region correctly?")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace with your actual subscription key and region
subscription_key = "ead9967ad49248719cb350b9f5b3b608"
region = "eastus"
text = "Hello, how are you today?"

text_to_speech(subscription_key, region, text)


# In[26]:


import os, requests, uuid, json

subscription_key = 'be7df87f0c3448e4aa6349d1b3d7bd15'
endpoint = 'https://translator313.cognitiveservices.azure.com/'

path = '/translate?api-version=3.0'
params = '&to=fr&to=it'
constructed_url = endpoint + path + params

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

body = [{
    'text': 'Hello, how are you today?'
}]

request = requests.post(constructed_url, headers=headers, json=body)
response = request.json()

print(json.dumps(response, sort_keys=True, indent=4, separators=(',', ': ')))


# In[27]:


pip install pyttsx3 pydub


# In[42]:


import requests
import uuid
import json

# Replace with your Azure Translator Text API subscription key and endpoint
subscription_key = 'be7df87f0c3448e4aa6349d1b3d7bd15'
endpoint = 'https://translator313.cognitiveservices.azure.com/'

# Function to perform translation
def translate_text(text, to_lang):
    path = '/translate?api-version=3.0'
    params = '&to=' + to_lang
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Request body
    body = [{
        'text': text
    }]

    try:
        # Send POST request to Azure Translator API
        response = requests.post(constructed_url, headers=headers, json=body)
        response.raise_for_status()  # Raise HTTPError for bad responses
        translated_text = json.loads(response.content.decode('utf-8'))

        # Extract and return translated text
        if translated_text and len(translated_text[0]['translations']) > 0:
            return translated_text[0]['translations'][0]['text']
        else:
            return "Translation not available"
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return "HTTP error occurred"
    except Exception as err:
        print(f"Other error occurred: {err}")
        return "Other error occurred"

if __name__ == '__main__':
    # Example usage
    text_to_translate = "Hello, how are you?"
    target_language = "fr"  # French

    translated_text = translate_text(text_to_translate, target_language)
    print(f"Original text: {text_to_translate}")
    print(f"Translated text ({target_language}): {translated_text}")


# In[39]:


pip install uuid


# In[43]:


import os
import time
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load the speech key and region from the .env file
load_dotenv()
key = os.getenv("KEY")
region = os.getenv("REGION")

stop = False

# When a sentence is recognized, print it to the screen.
# If stop is said, stop the app
def recognized(args):
    global stop
    if args.result.reason == speechsdk.ResultReason.TranslatedSpeech:
        #       print("Any Variable   :", args.result.translations['Spoken Language will be converted to this language.'])
        print("Chinese   :", args.result.translations["zh-Hans"])
        print("English   :", args.result.translations["en"])
        print("French    :", args.result.translations["fr"])
        print("German    :", args.result.translations["de"])
        print()

        if args.result.translations["en"] == "Stop.":
            stop = True


# Create a speech translation configuration using the following:
#  The API key and region loaded from the .env file
#  The language that will be recognized, in this example Great British English (en-GB)
#  The languages to be translated to, in this case Chinese, English, French and German
#
# See https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?WT.mc_id=build2020_ca-github-jabenn
# for the list of supported languages that can be recognized and translated to
translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=key,
                                                                   region=region,
                                                                   speech_recognition_language="en-GB",
                                                                   target_languages=("zh-Hans", "en", "fr", "de"))

# Creates a translation recognizer
recognizer = speechsdk.translation.TranslationRecognizer(translation_config=translation_config)

# Connect up the recognized event
recognizer.recognized.connect(recognized)

# Start continuous recognition
# This happens in the background, so the app continues to run, hence the need for an infinite loop
recognizer.start_continuous_recognition()

print("Say something! Say stop when you are done.")

# Loop until we hear stop
while not stop:
    time.sleep(0.1)


# In[44]:


import random
from azure.cognitiveservices.speech import (
    AudioDataStream,
    SpeechConfig,
    SpeechSynthesizer,
    SpeechSynthesisOutputFormat,
)

# Subscription settings from Azure
# Region can be westeurope for example
subscription_key = "[AZURE_SPEECH_API_KEY]"
subscription_region = "[AZURE_SPEECH_API_REGION]"

# Input SSML file
# Open this file to change or fine-tune the pitch, pronunciation, speaking rate, volume, voice, language and more
# https://github.com/MicrosoftDocs/azure-docs/blob/master/articles/cognitive-services/Speech-Service/language-support.md#neural-voices
input_folder = "input/"
input_file = "ssml.xml"

# https://docs.microsoft.com/nl-nl/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechsynthesisoutputformat?view=azure-python
audio_format = "Riff24Khz16BitMonoPcm"

# Output folder and file
output_folder = "output/"
output_file = f"file-{random.randint(10000,99999)}.wav"

speech_config = SpeechConfig(subscription=subscription_key, region=subscription_region)
speech_config.set_speech_synthesis_output_format(
    SpeechSynthesisOutputFormat[audio_format]
)
synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)

input = open(f"{input_folder}{input_file}", "r").read()
result = synthesizer.speak_ssml_async(input).get()

stream = AudioDataStream(result)
stream.save_to_wav_file(f"{output_folder}{output_file}")


# In[5]:


audio_output = speechsdk.audio.AudioOutputConfig(filename=r"C:\Users\bhagyashree\Desktop\microsoft azure\output_audio.wav")


# In[6]:


import azure.cognitiveservices.speech as speechsdk

# Set up the subscription info for the Speech Service:
subscription_key = "6380953120c4489da30f0312055db563"
service_region = "eastus"

# Create an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_config = speechsdk.SpeechConfig(subscription= "6380953120c4489da30f0312055db563", region="eastus")

# Specify the voice name (optional)
voice_name = "en-US-JennyNeural"  # You can choose different voices available

# Create a file handler to read the text
file_path = r"C:\Users\bhagyashree\Desktop\microsoft azure\textSpeech.txt"

with open(file_path, "r") as file:
    text = file.read()

# Create an audio configuration that points to an audio file
audio_output = speechsdk.audio.AudioOutputConfig(filename="output_audio.wav")

# Create the speech synthesizer with the specified voice
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

# Set the voice name
speech_synthesizer.voice_name = voice_name

# Synthesize the text
result = speech_synthesizer.speak_text_async(text).get()

# Check result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized to output_audio.wav")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print(f"Speech synthesis canceled: {cancellation_details.reason}")
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print(f"Error details: {cancellation_details.error_details}")


# In[8]:


import azure.cognitiveservices.speech as speechsdk

# Set up the subscription info for the Speech Service:
subscription_key = "YourAzureSubscriptionKey"
service_region = "YourServiceRegion"

# Create an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)

# Specify the voice name (optional)
voice_name = "en-US-JennyNeural"  # You can choose different voices available

# Create a file handler to read the text
file_path = r"C:\Users\bhagyashree\Desktop\microsoft azure\textSpeech.txt"
 # Use your actual text file path

with open(file_path, "r") as file:
    text = file.read()

# Create an audio configuration that points to an audio file in a specific directory
audio_output = speechsdk.audio.AudioOutputConfig(filename=r"C:\Users\bhagyashree\Desktop\microsoft azure\output_audio.wav")

# Create the speech synthesizer with the specified voice
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

# Set the voice name
speech_synthesizer.voice_name = voice_name

# Synthesize the text
result = speech_synthesizer.speak_text_async(text).get()

# Check result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized to C:\\Users\\bhagyashree\\Desktop\\microsoft azure\\output_audio.wav")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print(f"Speech synthesis canceled: {cancellation_details.reason}")
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print(f"Error details: {cancellation_details.error_details}")


# In[9]:


import time
import threading
import pyttsx3
import datetime

# Initialize the text-to-speech engine
def init_speech_engine():
    engine = pyttsx3.init()
    return engine

# Speak the given text
def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

# Listen to the user's input (stub function, replace with actual implementation if needed)
def listen():
    # Replace this with your speech recognition code if needed
    return input("Enter your reminder (format: 'remind me to [task] at [HH:MM]'): ").strip()

# Function to set a reminder
def set_reminder(reminders, task, reminder_time):
    reminders.append((task, reminder_time))
    print(f"Reminder set for {task} at {reminder_time.strftime('%H:%M')}")

# Check reminders in the background
def check_reminders(reminders, engine):
    while True:
        now = datetime.datetime.now()
        current_time = now.time()
        for reminder in reminders[:]:
            task, reminder_time = reminder
            if current_time >= reminder_time and now.date() == reminder_time.date():
                speak(engine, f"Reminder: {task}")
                reminders.remove(reminder)
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    engine = init_speech_engine()
    reminders = []

    # Start the background thread to check reminders
    reminder_thread = threading.Thread(target=check_reminders, args=(reminders, engine))
    reminder_thread.daemon = True
    reminder_thread.start()

    while True:
        query = listen()
        if 'remind me to' in query and 'at' in query:
            try:
                task_part, time_part = query.split('at')
                task = task_part.replace('remind me to', '').strip()
                reminder_time_str = time_part.strip()
                reminder_time = datetime.datetime.strptime(reminder_time_str, '%H:%M').time()

                now = datetime.datetime.now()
                reminder_datetime = datetime.datetime.combine(now.date(), reminder_time)
                if reminder_datetime < now:
                    reminder_datetime += datetime.timedelta(days=1)  # Set for the next day if the time has already passed

                set_reminder(reminders, task, reminder_datetime)
            except ValueError:
                speak(engine, "Sorry, I didn't understand the time format. Please use HH:MM.")
        elif 'exit' in query or 'stop' in query:
            speak(engine, "Goodbye!")
            break
        else:
            speak(engine, "I can only help with setting reminders at the moment.")


# In[1]:


#You Say: "Hello" or "Hi"
#You Say: "Remind me to [task] at [HH:mm]"
#You Say: "What time is it?"
    #You Say: "Weather in [city]"
       # You Say: "Wikipedia [search term]"
            #You Say: "Read text [text]"
                #You Say: "Exit" or "Stop"
import speech_recognition as sr
import pyttsx3
import threading
import datetime
import time
import requests
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError, WikipediaException

# Initialize the text-to-speech engine
def init_speech_engine():
    engine = pyttsx3.init()
    return engine

# Speak the given text
def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

# Listen to the user's query
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that. Please say that again.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
    return None

# Function to set a reminder
def set_reminder(reminders, task, reminder_time):
    reminders.append((task, reminder_time))
    print(f"Reminder set for {task} at {reminder_time.strftime('%H:%M')}")
    return f"Reminder set for {task} at {reminder_time.strftime('%H:%M')}"

# Check reminders in the background
def check_reminders(reminders, engine, stop_event):
    while not stop_event.is_set():
        now = datetime.datetime.now()
        current_time = now.time()
        for reminder in reminders[:]:
            task, reminder_time = reminder
            if current_time >= reminder_time and now.date() == reminder_time.date():
                speak(engine, f"Reminder: {task}")
                reminders.remove(reminder)
        time.sleep(30)  # Check every 30 seconds

# Fetch weather information
def fetch_weather(city):
    api_key = "14dfb89aa4d46a580298c85a4b2969b2"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    if response.status_code == 200 and "main" in data:
        main = data["main"]
        temperature = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        weather_desc = data["weather"][0]["description"]
        return f"Temperature: {temperature}°C\nPressure: {pressure} hPa\nHumidity: {humidity}%\nDescription: {weather_desc}"
    elif data.get("message"):
        return f"Error: {data['message']}"
    else:
        return "An unexpected error occurred while fetching the weather information."

# Fetch Wikipedia summary
def fetch_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        return results
    except DisambiguationError as e:
        return f"Disambiguation error: {e.options}"
    except PageError:
        return "Page not found."
    except WikipediaException as e:
        return f"Wikipedia error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Simple chatbot responses
def chatbot_response(query, reminders, engine, stop_event):
    if 'hello' in query or 'hi' in query:
        return "Hello! How can I assist you today?"
    elif 'remind me to' in query and 'at' in query:
        try:
            task_part, time_part = query.split('at')
            task = task_part.replace('remind me to', '').strip()
            reminder_time_str = time_part.strip()
            reminder_time = datetime.datetime.strptime(reminder_time_str, '%H:%M').time()

            now = datetime.datetime.now()
            reminder_datetime = datetime.datetime.combine(now.date(), reminder_time)
            if reminder_datetime < now:
                reminder_datetime += datetime.timedelta(days=1)  # Set for the next day if the time has already passed

            return set_reminder(reminders, task, reminder_datetime)
        except ValueError:
            return "Sorry, I didn't understand the time format. Please use HH:MM."
    elif 'what time is it' in query:
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%H:%M')}"
    elif 'weather in' in query:
        city = query.split('in')[-1].strip()
        return fetch_weather(city)
    elif 'wikipedia' in query:
        search_term = query.replace('wikipedia', '').strip()
        return fetch_wikipedia(search_term)
    elif 'read text' in query:
        text_to_read = query.replace('read text', '').strip()
        return text_to_read
    elif 'exit' in query or 'stop' in query:
        stop_event.set()
        speak(engine, "Goodbye!")
        return None
    else:
        return "I'm sorry, I can only assist with setting reminders, telling the time, fetching weather information, Wikipedia searches, and reading text at the moment."

if __name__ == "__main__":
    engine = init_speech_engine()
    reminders = []
    stop_event = threading.Event()

    # Start the background thread to check reminders
    reminder_thread = threading.Thread(target=check_reminders, args=(reminders, engine, stop_event))
    reminder_thread.daemon = True
    reminder_thread.start()

    while True:
        query = listen()
        if query:
            response = chatbot_response(query, reminders, engine, stop_event)
            if response is None:
                break
            speak(engine, response)
        else:
            speak(engine, "Please say that again.")
    
    # Wait for the reminder thread to finish
    reminder_thread.join()
    print("Program exited cleanly.")


# In[ ]:




