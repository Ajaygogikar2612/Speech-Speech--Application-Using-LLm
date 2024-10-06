
This project is a voice-enabled bot that uses Large Language Model (LLM) technology to process spoken commands and deliver spoken responses. The bot allows users to interact entirely through voice, offering intelligent and context-aware answers to their queries for a smooth, voice-based experience.

Main Features:
Speech Recognition: Converts spoken input into text using Google's speech recognition API.
LLM Integration: Leverages the Gemini 1.5 LLM to generate relevant and insightful responses.
Text-to-Speech: Transforms the LLM-generated text into speech via pyttsx3, enabling complete voice interaction.
Interactive GUI: A simple, intuitive interface built with Tkinter for easy user engagement.

Installation Steps:
pip install tkinter
pip install SpeechRecognition
pip install pyttsx3
pip install google-generativeai

Key Components:
Tkinter GUI: Provides the primary interface for user interaction.
SpeechRecognition: Converts speech input to text.
Generative AI: Processes the text and generates a response.
Pyttsx3: Converts text output to speech for voice responses.