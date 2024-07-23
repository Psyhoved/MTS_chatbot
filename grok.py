import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Create the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

# Set the system prompt
system_prompt = {
    "role":
        "system",
    "content":
        "You are my assistant, follow my instructions. You can only write in Russian."
}

# Initialize the chat history
chat_history = [system_prompt]

while True:
    # Get user input from the console
    user_input = input("client: ")

    # Append the user input to the chat history
    chat_history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(model="llama3-8b-8192",
                                              messages=chat_history,
                                              max_tokens=500,
                                              temperature=1)
    # Append the response to the chat history
    chat_history.append({
        "role": "assistant",
        "content": response.choices[0].message.content
    })
    # Print the response
    print("assistant:", response.choices[0].message.content)
