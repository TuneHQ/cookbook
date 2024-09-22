import json
from tune_studio_client import TuneStudioClient

class DnDGame:
    def __init__(self):
        self.client = TuneStudioClient()
        self.messages = [
            {"role": "system", "content": """
            You are an experienced Dungeons & Dragons (D&D) master, ready to guide players through a rich and immersive fantasy adventure. Your goal is to create a captivating story, complete with intriguing characters, challenging quests, and dynamic encounters. As the DM, you will narrate the setting, present challenges, and respond to players’ actions. Include ASCII art to enhance the atmosphere and visual storytelling.

            **Instructions:**

            1. **Setting the Scene:** Start with a vivid description of the world where the adventure takes place. Include details about the landscape, weather, and any notable landmarks. Use ASCII art to represent important locations (e.g., a castle, forest, or village).

            Example ASCII art for a castle:
            ```
                /\        
                /  \       
                /    \      
                /      \     
            /________\    
            |  __  __ |   
            ||  ||||  ||  
            ||__||||__||  
            |____________|  
            ```

            2. **Introducing Characters:** Present the main characters, including NPCs (non-player characters) that the players might encounter. Describe their appearance, personality, and motivations. You can use ASCII art for key NPCs to make them memorable.

            3. **Quest Hooks:** Provide several potential quests or missions for the players to embark on. Each quest should include a brief summary, possible rewards, and potential dangers.

            4. **Dynamic Encounters:** Create a series of encounters that can occur during the adventure. These can range from combat scenarios to puzzles and social interactions. Include descriptions and any necessary statistics for creatures or challenges.

            5. **Player Interaction:** Encourage players to interact with the world. Be prepared to adapt the story based on their choices, responding creatively to their actions.

            6. **ASCII Art for Combat:** When combat arises, describe the battlefield and the positioning of characters and enemies. Use ASCII art to illustrate the layout and provide clarity.

            Example ASCII art for a battlefield:
            ```
            Enemy: E      Player: P
            E E E E E E E E E
            E E E E E E E E E
            E E E E E E E E E
            P P P P P P P P P
            ```

            7. **Conclusion of the Session:** At the end of the session, summarize the players' accomplishments and set the stage for future adventures, teasing what lies ahead.

            Remember, your goal is to create an engaging and interactive experience that captivates the players and keeps them invested in the story. Use your creativity to weave together narrative, challenges, and ASCII art, making each session memorable.

        """}
        ]

    def send_message(self, content):
        self.messages.append({"role": "user", "content": content})
        response = self.client.generate_response(self.messages)
        if response:
            dm_response = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            self.messages.append({"role": "assistant", "content": dm_response})
            return dm_response
        return "No response from the Dungeon Master."

    def start_game(self):
        print("Welcome to the Dungeons & Dragons text-based game!")
        print("Type 'exit' to end the game.")
        
        # Storyline introduction
        print("\nYou are about to embark on a thrilling adventure in a mystical world filled with danger and treasure.\n")
        print("Choose your adventure:")
        print("1. The Haunted Forest")
        print("2. The Lost Temple")
        print("3. The Dragon's Lair")
        
        adventure_choice = input("Enter the number of your choice: ")
        if adventure_choice == "1":
            self.messages.append({"role": "user", "content": "Start the Haunted Forest adventure."})
            self.display_ascii_art_haunted_forest()
        elif adventure_choice == "2":
            self.messages.append({"role": "user", "content": "Start the Lost Temple adventure."})
            self.display_ascii_art_lost_temple()
        elif adventure_choice == "3":
            self.messages.append({"role": "user", "content": "Start the Dragon's Lair adventure."})
            self.display_ascii_art_dragons_lair()
        else:
            print("Invalid choice. Starting the default adventure: The Haunted Forest.")
            self.messages.append({"role": "user", "content": "Start the Haunted Forest adventure."})
            self.display_ascii_art_haunted_forest()

        print(self.send_message("Describe the beginning of the adventure."))

        while True:
            user_input = input("\nWhat do you want to do? ")
            if user_input.lower() == "exit":
                print("Thank you for playing!")
                break
            response = self.send_message(user_input)
            print(response)

    def display_ascii_art_haunted_forest(self):
        print(r"""
        🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲
         🌲    🎃     🌲
          🌲  👻  🌲
         🌲🌲🌲🌲🌲🌲🌲🌲🌲🌲
        """)

    def display_ascii_art_lost_temple(self):
        print(r"""
         ⛩️⛩️⛩️⛩️
          ⛩️  🐉  ⛩️
         ⛩️⛩️⛩️⛩️⛩️
        """)

    def display_ascii_art_dragons_lair(self):
        print(r"""
         🐉🐉🐉🐉🐉
          🏰🏰🏰🏰
         🏰🏰  🔥  🏰🏰
         🐉🐉🐉🐉🐉
        """)

if __name__ == "__main__":
    game = DnDGame()
    game.start_game()
