import json
import requests

stream = False
url = "https://proxy.tune.app/chat/completions"
headers = {
    "Authorization": "sk-tune-RiuXzcHE8jUmY6nUifT05VwFop3zDvFCljp",
    "Content-Type": "application/json",
}
data = {
  "temperature": 0.8,
    "messages":  [
  {
    "role": "system",
    "content": "act like a game chatbot\n\nyou want to recommend a game to the user by asking few of their prefrences\n\n1) Do you like slow paced games or fast paced games. Also ask what type of gaming machine they have.\n2) if slow paced games then recommend story mode games\n3) if fast paced games then recommend fps games\n4) Also give the brief of those games and whats the learning curve in it\n5) Let the user know what minimum requirements is there to play it\n6) let yhe user know where to download it from"
  },
  {
    "role": "user",
    "content": "suggest me a game"
  },
  {
    "role": "assistant",
    "content": "Of course! Here are a variety of games across different genres that you might enjoy:\n\n### Action/Adventure:\n1. **The Legend of Zelda: Breath of the Wild** - An open-world adventure game with lots of exploration and puzzles.\n2. **Red Dead Redemption 2** - An epic tale of life in America’s unforgiving heartland.\n\n### Role-Playing Games (RPG):\n1. **The Witcher 3: Wild Hunt** - An expansive RPG with an immersive world and rich storytelling.\n2. **Final Fantasy VII Remake** - A modern take on the classic JRPG, with stunning graphics and gameplay.\n\n### Puzzle/Strategy:\n1. **Portal 2** - A first-person puzzle game with a dark sense of humor.\n2. **Civilization VI** - A turn-based strategy game where you build and expand an empire.\n\n### Multiplayer/Online:\n1. **Among Us** - A multiplayer game of teamwork and betrayal.\n2. **Fortnite** - A battle royale game with building mechanics and frequent updates.\n\n### Indie Games:\n1. **Hades** - A rogue-like dungeon crawler with a rich story and fast-paced combat.\n2. **Celeste** - A platformer about climbing a mountain, with tight controls and a touching narrative.\n\n### Casual/Relaxing:\n1. **Stardew Valley** - A farming simulation game with charming graphics and a relaxing pace.\n2. **Animal Crossing: New Horizons** - A life simulation game where you build and customize your own island.\n\nDo any of these catch your interest? If you have a specific genre or type of game in mind, let me know, and I can provide more tailored suggestions!"
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