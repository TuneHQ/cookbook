import json
import requests

stream = False
url = "https://proxy.tune.app/chat/completions"
headers = {
    "Authorization": "sk-tune-Pjq12YXqaBrLsBWuWpWAZRdmcujr1GSvjEY",
    "Content-Type": "application/json",
}
data = {
  "temperature": 0.9,
    "messages":  [
      {
        "role": "system",
        "content": "You are transcriber and your only task is to convert the given text from english to the given language. You should respond only and only with the converted text. Do not return anything before and after the converted text. Your response should consist of text only and only in the given language."
      },
      {
        "role": "user",
        "content": "Conversion language: Hindi. Input text: hi everyone uh so in this presentation we're going to talk about F tuning llms and also something a bit more experimental called Model merging so at the end of the presentation you should have a good overview of all the main libraries to do fine tuning what's expected in terms of inputs what you're going to get in terms of outputs and also how to raise the quality of your model even further with model merging and we're going to see a lot of practical example that hopefully inspire you yeah um a bit about me so I'm indeed a staff machine learning scientist at liquid AI I'm also a gr developer expert I write blog post I've written the llm course on GitHub I've published a few uh models and data sets on Hing face and a few tools and also the author of Hands-On graph networks but also just announced a new book called the llm engineers uh handbook you might be."
      }
    ],
    "model": "mistral/mixtral-8x7b-instruct",
    "stream": stream,
    "frequency_penalty":  0.2
}
response = requests.post(url, headers=headers, json=data)
if stream:
    for line in response.iter_lines():
        if line:
            l = line[6:]
            if l != b'[DONE]':
              print(json.loads(l))
else:
  print(response.json())