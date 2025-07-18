# 🔄 Voice-Based AI Chat Assistant

This project is a **Voice-Activated AI Chat Assistant** built using Python. It enables real-time voice interaction with an AI model, allowing users to ask questions or have conversations through speech. The assistant converts speech to text, processes it using OpenAI's ChatGPT, and then responds via text-to-speech.

---

## 📁 Project Structure

.

├── main.py # Entry point – captures voice, interacts with GPT, and speaks the response

├── online.py # Handles OpenAI API calls to fetch AI-generated responses

├── conv.py # Handles voice input and text-to-speech output


---

## 💡 Features

- 🎙️ Converts speech to text using `speech_recognition`
- 🤖 AI responses generated by OpenAI's GPT model
- 🔊 Responds using text-to-speech via `pyttsx3`
- 🧠 Maintains context across multiple queries
- 🌐 Requires internet for real-time AI communication

---

## 🚀 How It Works

1. Run `main.py`
2. Speak into your microphone
3. Your speech is converted to text
4. The AI processes the text and responds
5. The response is spoken aloud via text-to-speech

---

## 📦 Requirements

Install the required libraries using pip:

pip install openai pyttsx3 speechrecognition

You may also need to install pyaudio. For macOS:

brew install portaudio

pip install pyaudio

## 🔐 API Key

This project uses OpenAI's GPT model.

Get your API key from OpenAI

Replace "YOUR_API_KEY" in online.py with your actual API key:

openai.api_key = "YOUR_API_KEY"

## 🧠 Sample Usage

python main.py

##📣 Example conversation:

You: "What's the capital of France?"

AI: "The capital of France is Paris."

## ✨ Customization Ideas

Add wake-word detection (e.g., "Hey Assistant")

GUI interface using tkinter or PyQt

Add memory or conversation history

Integrate with other APIs (weather, news, etc.)

## 🛠️ Troubleshooting

Microphone not working? Check permissions and device input settings.

Speech not recognized? Make sure you're speaking clearly in a quiet environment.

No voice output? Ensure your system's TTS engine is set up properly.

## 📄 License

This project is open-source and available under the MIT License.

## 🙋‍♂️ Author

Kshitij Singh

Feel free to reach out for feedback, contributions, or collaboration ideas!
