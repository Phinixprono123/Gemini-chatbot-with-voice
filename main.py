#imports 
import os
import json
import subprocess

#Setting variables
API_KEY = "GEMINI_API_KEY"
HISTORY_FILE = "ChatHist.json"
MODELS = ["gemini-2.5-pro-exp-03-25", "gemini-2.5-flash-preview-04-17", "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-flash", "gemini-1.5-flash-8b"]

# Function to handle voice capabilities
def speak(output):
    output = output.replace("*", " ")
    output = output.replace(":", ",")
    output = output.replace("#", " ")
    try:
        subprocess.run(['espeak', '-v', 'en-us+m3', '-p', '60', output], text=True)

    except:
        print("UNEXPECTED ERROR")


# Loads the conversation history from HIST_FILE 
def load_history():
    # Creates the file in HISTORY_FILE if it dosen't exists
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as file:
            json.dump([], file)
    with open(HISTORY_FILE, "r") as file:
        return json.load(file)
# saves the history to HISTORY_FILE uhhh im tired of typing bye
def save_history(history):
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=2)

#Function to interact with Gemini API and get response
def generate_text(promt, model, maxtokens=50):
    history = load_history()
    history.append({"text": promt})

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
    print(url)
    data = {
        "contents": [{
            "parts": history + [{"text": promt}]
        }],
        "generationConfig": {
            "maxOutputTokens": maxtokens
        }
    }
    command = ['curl', url, "-H", "Content-Type: application/json", "-X", "POST", "-d", json.dumps(data)]
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

# Main Function to setup chating system
 
def main():
    print("""Select a model from this list:
    1 Gemini 2.5 pro experamental 05 06
    2 Gemini 2.5 flash preview 04 17
    3 Gemini 2.0 flash
    4 Gemini 2.0 flash lite
    5 Gemini 1.5 flash
    6 Gemini 1.5 flash 8b

    * NOTE: more powerfull models such as 2.5 pro and 2.5 flash may not always work.
    """)
    model_num = int(input("Enter an number: "))
    model_num -= 1
    model = MODELS[model_num]
    print(f"{model} running")
    history = load_history()
    while True:
        userinput = input("You: ")
        if userinput == "/exit" or userinput == "/stop":
            break

        history.append({"text": f"You: {userinput}"})

        response = generate_text(userinput, model, 200)
        if "candidates" in response:
            ai_output = response["candidates"][0]["content"]["parts"][0]["text"]
            history.append({"text": f"Aissistant: {ai_output}"})
            save_history(history)
            print(ai_output)
            speak(ai_output)
        else:
            print(f"Unexpected response: {response}")

if __name__ == "__main__":
    main()
