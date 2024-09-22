import json
import requests

stream = False
url = "https://proxy.tune.app/chat/completions"
headers = {
    "Authorization": "sk-tune-6tZfo3wx7Gl0cOCUAnIu5atRHouw3jrEuUT",
    "Content-Type": "application/json",
}
data = {
  "temperature": 0,
    "messages":  [
  {
    "role": "system",
    "content": "capital of India is New Delhi"
  },
  {
    "role": "user",
    "content": "what is the capital of India"
  },
  {
    "role": "user",
    "content": "Delhi is the capital of India"
  },
  {
    "role": "assistant",
    "content": "Yes, you are correct! New Delhi is the capital of India."
  },
  {
    "role": "user",
    "content": "what is famous in delhi?"
  },
  {
    "role": "assistant",
    "content": "Delhi is famous for its rich history, culture, and vibrant markets. Here are some of the famous attractions and features of Delhi:\n\n1. **Historical Monuments:**\n   - **Red Fort:** A UNESCO World Heritage Site and a symbol of India's rich history.\n   - **Qutub Minar:** Another UNESCO World Heritage Site, the tallest brick minaret in the world.\n   - **Humayun's Tomb:** A precursor to the Taj Mahal and a UNESCO World Heritage Site.\n   - **India Gate:** A war memorial dedicated to Indian soldiers.\n\n2. **Religious Sites:**\n   - **Lotus Temple:** A Bahá'í House of Worship known for its unique lotus flower-like shape.\n   - **Jama Masjid:** One of the largest mosques in India.\n   - **Akshardham Temple:** A modern temple complex known for its stunning architecture and spiritual exhibits.\n\n3. **Markets and Shopping:**\n   - **Chandni Chowk:** A bustling market area famous for its street food, spices, and traditional Indian goods.\n   - **Connaught Place:** A central commercial area with shops, restaurants, and cafes.\n   - **Sarojini Nagar:** Popular for its affordable fashion and accessories.\n\n. **Cultural Institutions:**\n   - **National Museum:** Houses a vast collection of artifacts from India's history.\n   - **National Gallery of Modern Art (NGMA):** Displays modern and contemporary Indian art.\n\n5. **Cuisine:**\n   - **Street Food:** Delhi is famous for its street food, including chaat, parathas, and kebabs.\n   - **Restaurants:** The city offers a wide variety of dining options, from traditional Indian cuisine to international flavors.\n\n6. **Parks and Gardens:**\n   - **Lodhi Gardens:** A beautiful park that contains ancient tombs and lush greenery.\n   - **Garden of Five Senses:** A park designed to stimulate the five senses through its landscaping and installations.\n\nThese are just a few highlights. Delhi offers a rich tapestry of experiences for both locals and tourists alike!"
  }
],
    "model": "kaushikaakash04/tune-blob",
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