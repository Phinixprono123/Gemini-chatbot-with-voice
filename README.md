## Gemini-chatbot-wih-voice
This is made to use Gemini ai without installing the python google-genai library. especially because on Android (termux) 
I don't if it's possible to install it. so after taking a look at the official documentation I made this script which uses `curl` 
to do API requests. plus i also added voice to the ai with espeak

## Requirements
- **Python 3 or higher**
- **`curl` installed**
- **A Gemini API key**
- **`espeak` installed**

## Usage
replace the GEMINI_API_KEY with you API key.

And run the main.py with
```python
python main.py
```

