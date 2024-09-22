import json
import requests

stream = False
url = "https://proxy.tune.app/chat/completions"
headers = {
    "Authorization": "sk-tune-9HP6z2OmyublV99PqcwPeYBOoa2XZ7uvUr5",
    "Content-Type": "application/json",
}
data = {
  "temperature": 0.8,
    "messages":  [
  {
    "role": "system",
    "content": [
      {
        "type": "text",
        "text": "Generate a random fact about DC super heroes upon request. Also, mention the first issue, year in which the super hero appeared. "
      }
    ]
  },
  {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "Example. Batman once got access to mobius chair and got to know that there are three jokers. Also, batman first issue was published in 1947 or 1948"
      }
    ]
  },
  {
    "role": "assistant",
    "content": [
      {
        "type": "text",
        "text": "Sure, here's a random fact: \n\nWonder Woman's iconic weapon, the Lasso of Truth, compels anyone it ensnares to tell the truth. This magical lasso is unbreakable and also allows Wonder Woman to control her invisible plane.\n\nWonder Woman first appeared in *All Star Comics* #8, which was published in December 1941."
      }
    ]
  },
  {
    "role": "assistant",
    "content": [
      {
        "type": "text",
        "text": ""
      }
    ]
  },
  {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "Superman"
      }
    ]
  },
  {
    "role": "assistant",
    "content": [
      {
        "type": "text",
        "text": "Here's an interesting fact: Superman once gave up his powers to live a normal life with Lois Lane. This storyline is explored in the 1980 movie \"Superman II.\"\n\nSuperman first appeared in *Action Comics* #1, which was published in June 1938."
      }
    ]
  }
],
    "model": "openai/gpt-4o",
    "stream": stream,
    "frequency_penalty":  0,
    "max_tokens": 900
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