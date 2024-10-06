import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai

key = "AIzaSyDmURTZJXO8FxgODKCoHW0CULbtI9gAmYs"

# Initializing the recognizer, r => recognizer
r = sr.Recognizer()

def record_text():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        user_input_field.delete(1.0, tk.END)
        output_field.delete(1.0, tk.END)
        try:
            status_label.config(text="Listening...", fg="blue")
            root.update_idletasks()
            audio = r.listen(source, timeout=5)
            user_text = r.recognize_google(audio)
            user_input_field.insert(tk.END, user_text)
            user_input_field.update_idletasks()

            if user_text.lower() == "quit from the application":
                text_to_speech("Goodbye!")
                root.quit()
                return

            response = getResponse(user_text)
            output_field.insert(tk.END, response)
            output_field.update_idletasks()
            text_to_speech(response)
            status_label.config(text="Processing complete", fg="green")

        except sr.UnknownValueError:
            user_input_field.insert(tk.END, "Sorry, I did not understand that.")
            status_label.config(text="Sorry, I did not understand that.", fg="red")
        except sr.RequestError as e:
            user_input_field.insert(tk.END, f"Could not request results; {e}")
            status_label.config(text=f"Request error: {e}", fg="red")
        except sr.WaitTimeoutError:
            user_input_field.insert(tk.END, "Listening timed out while waiting for phrase to start.")
            status_label.config(text="Listening timed out", fg="red")
        except Exception as e:
            user_input_field.insert(tk.END, f"An error occurred: {e}")
            status_label.config(text=f"An error occurred: {e}", fg="red")

def getResponse(txt):
    genai.configure(api_key=key)
    
    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 8192,
      "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
      model_name="gemini-1.5-flash",
      generation_config=generation_config,
    )
    
    chat_session = model.start_chat(
      history=[
        {
          "role": "user",
          "parts": [
            "Your name is Skye. Limit your responses to 4 sentences with a maximum of 100 words...",
          ],
        },
        {
          "role": "model",
          "parts": [
            "I understand that you're looking for support, and I'm here to listen...",
          ],
        },
      ]
    )
    
    response = chat_session.send_message(txt)
    
    return response.text

def text_to_speech(txt):
    text_speech = pyttsx3.init()
    text_speech.say(txt)
    text_speech.runAndWait()

# Setting up the main application window
root = tk.Tk()
root.title("TenosrGo Assignment Speech to Speech LLM BOT")
root.geometry("750x550")  # Set the window size
root.configure(bg='#2c3e50')  # Set background to dark blue

# Create a frame for better organization
frame = tk.Frame(root, bg='#34495e', bd=5, relief=tk.RAISED)
frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# User Input Field
tk.Label(frame, text="Message Bot:", font=('Helvetica', 14, 'bold'), bg='#34495e', fg='#ecf0f1').grid(row=0, column=0, padx=10, pady=5, sticky="w")
user_input_field = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=6, font=('Helvetica', 12), bg='#ecf0f1', fg='#2c3e50', bd=2, relief=tk.SUNKEN)
user_input_field.grid(row=1, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")

# Model Output Field
tk.Label(frame, text="Generated Response:", font=('Helvetica', 14, 'bold'), bg='#34495e', fg='#ecf0f1').grid(row=2, column=0, padx=10, pady=5, sticky="w")
output_field = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=6, font=('Helvetica', 12), bg='#ecf0f1', fg='#2c3e50', bd=2, relief=tk.SUNKEN)
output_field.grid(row=3, column=0, padx=10, pady=5, columnspan=2, sticky="nsew")

# Status Label
status_label = tk.Label(frame, text="", font=('Helvetica', 12, 'italic'), bg='#34495e', fg='#bdc3c7')
status_label.grid(row=4, column=0, padx=10, pady=5, columnspan=2, sticky="w")

# Record Button with custom styling
record_button = tk.Button(frame, text="Click To Speak", command=record_text, width=20, font=('Helvetica', 12, 'bold'), bg='#1abc9c', fg='#ffffff', bd=0, relief=tk.RAISED, activebackground='#16a085', activeforeground='#ecf0f1', padx=10, pady=10)
record_button.grid(row=5, column=0, padx=10, pady=20, columnspan=2)

# Configure grid expansion
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(3, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

# Start the GUI event loop
root.mainloop()
