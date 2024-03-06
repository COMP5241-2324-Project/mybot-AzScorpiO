import gradio, requests, json
import os
import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
redis_client.rpush('prompts', prompt)
redis_client.rpush('responses', resp)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

if OPENROUTER_API_KEY is None:
    print("Please set the OPENROUTER_API_KEY")
    exit(1)

def chat(prompt): 

    # Check if the user wants to know who is the author
    if "author" in prompt.lower():
        return "My author's name is [AzScorpiO-Zhuofan Zhao]."
    
    # Otherwise
    msg = [
        {"role": "system", "content": "Answer questions related to Software Engineering in funny tone with Emoji"},
        {"role": "user", "content": prompt}
    ]

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
        data=json.dumps({
            "messages": msg,
            "model": "mistralai/mistral-7b-instruct:free"
        })
    )
    resp =  response.json()['choices'][0]['message']['content'] # extract the bot's response from the JSON
    print(f"--------\n{resp}\n") # print the bot's response to the console
    
    return "Your prompt is: "+prompt

demo = gradio.Interface(fn=chat, inputs="text", outputs="text", title="😀 My Bot")

demo.launch(server_name="0.0.0.0")
