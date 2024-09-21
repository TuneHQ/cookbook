import tkinter as tk
from tkinter import Button, Label, Frame, Text
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import webbrowser
import psutil
import requests
from PIL import Image, ImageTk
import io
import re


# MongoDB connection
uri = "mongodb+srv://itsrohanvj:U2IZLM2Q6zY5mkck@innothon.su9fje6.mongodb.net/?retryWrites=true&w=majority&ssl=true&appName=Innothon"

client = MongoClient(uri, server_api=ServerApi('1'), tls=True)
try:
    client.admin.command('ping')
    print("You're successfully connected to MongoDB!")

    # Access the database
    db = client['innothon_db']

    # Access the collection
    collection = db['cyber']
    quiz_collection = db['cyber_quiz']

    # Fetch all documents from the collections
    documents = list(collection.find())
    quiz_documents = list(quiz_collection.find())
except Exception as e:
    print(e)

# GUI Application
class App:
    def __init__(self, root):
        self.count_right=1
        self.count_wrong=1
        self.root = root
        self.links = {}
        self.doc_index = 0
        self.key_index = 1  # Start from 1 to skip the first key
        self.quiz_doc_index = 0
        self.quiz_key_index = 1  # Start from 1 to skip the first key
        self.keys = list(documents[0].keys()) if documents else []
        self.quiz_keys = list(quiz_documents[0].keys()) if quiz_documents else []
        self.dnd_mode = False  # DND mode state
        self.window_open = False  # Track if a window is open
        self.start_prompting()
        self.schedule_check_updates()  # Schedule periodic checks for updates
        self.previous_apps = {}  # Track previously running apps with their states
        self.check_for_apps()  # Start monitoring for specific applications
        self.schedule_quiz_prompt()  # Schedule the quiz prompt
        self.reset_score_timer()  #Reset score
    def set_window_open_false(self):
        
        self.window_open = False
    def open_link(self,event):
        widget = event.widget
        index = widget.index("@%s,%s" % (event.x, event.y))
        tag_indices = widget.tag_ranges("link")
        for i in range(0, len(tag_indices), 2):
            if widget.compare(index, ">=", tag_indices[i]) and widget.compare(index, "<=", tag_indices[i+1]):
                url = self.links[widget.get(tag_indices[i], tag_indices[i+1])]
                webbrowser.open_new(url)
                break
    def show_info_window(self, title, message, url=None, img=None, show_learn_more=True, show_dnd=True):
        # Create a temporary Toplevel window
        info_window = tk.Toplevel(self.root)
        info_window.title(title)
        
        # Remove minimize and maximize buttons
        #info_window.wm_attributes('-toolwindow', True)
        
        # Set size of the window
        window_width = 300
        window_height = 310  # Adjusted height for image and buttons
        info_window.geometry(f"{window_width}x{window_height}")

        # Style the window
        info_window.configure(bg="#f0f0f0")  # Light gray background
        
        # Create a frame for better layout
        frame = Frame(info_window, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add message label
        message_label = Label(
            frame, 
            text=message, 
            wraplength=window_width-20, 
            font=("Helvetica", 12, "bold"), 
            #bg="#e6f7ff",  # Light blue background
            fg="gray",  # Dark gray text color
            padx=10, 
            pady=10, 
            relief="solid"
            #bd=1
        )
        message_label.pack(pady=5)
        string_type=str(type(img))
        # Add image if available
        if 'str' not in string_type :
            img_label = Label(frame, image=img, bg="#ffffff")
            img_label.image = img  # Keep a reference to avoid garbage collection
            img_label.pack(pady=5)
        else:
            img=img.split(': ')[1]
            
            
            text_widget = Text(
            frame,
            wrap="word",
            font=("Helvetica", 12, "bold"),
            bg="#e6f7ff",  # Light blue background
            fg="#333333",  # Dark gray text color
            padx=10,
            pady=40,
            relief="solid",
            bd=1,
            height=5,  # Adjust height as needed
            width=window_width-20  # Adjust width according to window width
            )

            # Insert the message text
            text_widget.insert("1.0", img)

            # Find the link in the message and tag it
            start_idx = img.find("http")
            if start_idx != -1:
                end_idx = img.find(" ", start_idx)
                if end_idx == -1:
                    end_idx = len(img)
                
                # Tag the link
                text_widget.tag_add("link", f"1.{start_idx}", f"1.{end_idx}")
                text_widget.tag_config("link", foreground="blue", underline=True)
                text_widget.tag_bind("link", "<Button-1>", self.open_link)
                self.links[img[start_idx:end_idx]] = img[start_idx:end_idx]

            # Make the Text widget read-only
            text_widget.config(state="disabled")
            
            # Pack the Text widget
            text_widget.pack(pady=5)
            frame.pack()
        
            '''
            #If it contains only textual data and not images
            message_label2 = Label(
            frame, 
            text=img.split(': ')[1], 
            wraplength=window_width-20, 
            font=("Helvetica", 12, "bold"), 
            bg="#e6f7ff",  # Light blue background
            fg="#333333",  # Dark gray text color
            padx=10, 
            pady=45, 
            relief="solid"
            #bd=1
            )
            message_label2.pack(pady=5)
            '''
        # Add buttons frame
        buttons_frame = Frame(frame, bg="#ffffff")
        buttons_frame.pack(pady=5)

        # Add "Learn More" button if URL is provided and show_learn_more is True
        if url and show_learn_more:
            learn_more_button = Button(
                buttons_frame, 
                text="Learn More", 
                command=lambda: webbrowser.open(url), 
                font=("Helvetica", 11, "bold"),
                bg="#00FF00",  # Green background
                fg="white",   # White text
                activebackground="#45a049",  # Darker green on click
                cursor="hand2"  # Hand cursor on hover
            )
            learn_more_button.pack(side=tk.LEFT, padx=5)

            # Add hover effect
            learn_more_button.bind("<Enter>", lambda e: learn_more_button.config(bg="#45a049"))
            learn_more_button.bind("<Leave>", lambda e: learn_more_button.config(bg="#00FF00"))

                
        # Add DND button if show_dnd is True
        if show_dnd:
            dnd_button = Button(
                buttons_frame,
                text="Do Not Disturb",
                command=self.activate_dnd_mode,
                font=("Helvetica", 11, "bold"),
                bg="red",  # Red background
                fg="white",  # White text
                activebackground="#d32f2f",  # Darker red on click
                cursor="hand2"  # Hand cursor on hover
            )
            dnd_button.pack(side=tk.LEFT, padx=5)

            # Add hover effect
            dnd_button.bind("<Enter>", lambda e: dnd_button.config(bg="#d32f2f"))
            dnd_button.bind("<Leave>", lambda e: dnd_button.config(bg="#f44336"))

        # Position the window at the bottom right corner above the taskbar
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        taskbar_height = 80  # Adjust this value based on your taskbar height

        x = screen_width - window_width - 10  # 10 pixels from the right edge
        y = screen_height - window_height - taskbar_height - 10  # 10 pixels from the bottom edge, above taskbar

        info_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Auto-close window after 10 seconds
        self.root.after(12000, info_window.destroy) #60000

    def activate_dnd_mode(self):
        self.dnd_mode = True
        self.show_info_window(
            title="DND Mode Activated",
            message="Do Not Disturb mode is now active for 2 minute.",
            show_learn_more=False,
            show_dnd=False
        )
        # Schedule reactivation of prompts after 1 minute (60000 milliseconds)
        self.root.after(120000, self.deactivate_dnd_mode)

    def deactivate_dnd_mode(self):
        self.dnd_mode = False
        self.show_info_window(
            title="DND Mode Deactivated",
            message="Do Not Disturb mode has ended. Prompts will resume.",
            show_learn_more=False,
            show_dnd=False
        )
        self.schedule_next_prompt()  # Resume prompting immediately
        self.schedule_next_quiz_prompt()
    def start_prompting(self):
        if documents:
            print(documents)
            self.show_prompt()
        else:
            self.show_info_window(
                title="Info",
                message="No documents found in the collection.",
                url="https://www.google.com"
            )
            self.root.quit()  # Close the application if no documents are found
        
    def show_prompt(self):
        
        if not documents or self.dnd_mode:
            return 
        if self.window_open:
            return self.schedule_next_prompt()
        
        document = documents[self.doc_index]
        if self.key_index < len(self.keys):
            key = self.keys[self.key_index]
            message = f"{key}: {document[key]}"
            self.key_index += 1
        else:
            self.key_index = 1  # Reset to 1 to skip the first key of the next document
            self.doc_index = (self.doc_index + 1) % len(documents)
            document = documents[self.doc_index]
            self.keys = list(document.keys())
            key = self.keys[self.key_index]
            message = f"{key}: {document[key]}"
            self.key_index += 1

        url, img = self.extract_url_and_image(message)
        if key=='Keylogger':

            custom_url = "https://www.mcafee.com/learn/what-is-a-keylogger/" 
        if key=='Phishing':
            custom_url='https://www.cloudflare.com/learning/access-management/phishing-attack/'
            
        else:
            custom_url=f"https://www.google.com/search?q={key}" # Set your custom URL here
    
        self.show_info_window(
            title=key,
            message=key,
            url=custom_url,
            img=img,
            show_learn_more=True,  # Show "Learn More" button for prompts
            show_dnd=True  # Show DND button for prompts
        )
        self.schedule_next_prompt()

    def extract_url_and_image(self, message):
        url_match = re.search(r'http[s]?://\S+', message)
        if url_match:
            url = url_match.group(0)
            img = self.fetch_image_from_url(url)
            if img:

                return url, img
            else:
                return None, message
        return None, None

    def fetch_image_from_url(self, url):
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((250, 250))  # Resize the image to fit the window
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"No Image: {e}")
            return None

    def schedule_next_prompt(self):
        
        self.root.after(18000, self.show_prompt)  # Schedule the next prompt in 18 seconds

    def check_for_updates(self):
        global documents, quiz_documents
        if self.dnd_mode:
            self.schedule_check_updates()
            return
        try:
            # Fetch all documents from the collections
            new_documents = list(collection.find())
            new_quiz_documents = list(quiz_collection.find())
            if new_documents != documents:
                documents = new_documents
                self.doc_index = 0
                self.key_index = 1  # Reset to start checking from the first new key
                self.keys = list(documents[0].keys()) if documents else []
            if new_quiz_documents != quiz_documents:
                quiz_documents = new_quiz_documents
                self.quiz_doc_index = 0
                self.quiz_key_index = 1  # Reset to start checking from the first new key
                self.quiz_keys = list(quiz_documents[0].keys()) if quiz_documents else []
        except Exception as e:
            print(e)
        finally:
            self.schedule_check_updates()  # Schedule the next update check

    def schedule_check_updates(self):
        print("CHECKING UPDATES ON MONGO DB")
        self.root.after(180000, self.check_for_updates)  # Check for updates every 4 minutes

    def check_for_apps(self):
        def check_apps():
            if self.dnd_mode:
                self.root.after(15000, check_apps)  #15 seconds
                return
            
            # List of apps to monitor
            apps = {
                "cmd.exe": "Beware of SQL injection! https://miro.medium.com/v2/resize:fit:1024/0*ErN7MyOU7wjQLSgM.jpg",
                #"msedge.exe": "Beware of phishing!",
                "outlook.exe": "Beware of malicious mails! https://calyxit.com/wp-content/uploads/2020/08/Calyx-malicious-email.png"
            }

            # Get list of running processes
            running_apps = {proc.name().lower() for proc in psutil.process_iter(attrs=['name'])}

            # Check for the start of new specific apps
            for app, message in apps.items():
                if app in running_apps and (app not in self.previous_apps or not self.previous_apps[app]):
                    url, img = self.extract_url_and_image(message)
                    self.show_info_window(
                        title="Warning",
                        message=message.split('http')[0],
                        url=None,
                        img=img,
                        show_learn_more=False,  # Do not show "Learn More" button for app checks
                        show_dnd=False  # Do not show DND button for app checks
                    )
                    self.previous_apps[app] = True

            # Update previously running apps
            for app in self.previous_apps.keys():
                if app not in running_apps:
                    self.previous_apps[app] = False

            # Check for apps every 15 seconds
            self.root.after(15000, check_apps)

        self.root.after(1000,check_apps())
    
    def show_quiz_prompt(self):
        if not quiz_documents or self.dnd_mode:
            return 

        quiz_document = quiz_documents[self.quiz_doc_index]
        if self.quiz_key_index < len(self.quiz_keys):
            question = self.quiz_keys[self.quiz_key_index]
            answer = quiz_document[question]
            self.quiz_key_index += 1
        else:
            self.quiz_key_index = 1  # Reset to 1 to skip the first key of the next document
            self.quiz_doc_index = (self.quiz_doc_index + 1) % len(quiz_documents)
            quiz_document = quiz_documents[self.quiz_doc_index]
            self.quiz_keys = list(quiz_document.keys())
            question = self.quiz_keys[self.quiz_key_index]
            answer = quiz_document[question]
            self.quiz_key_index += 1

        self.show_quiz_window(question, answer)
        self.schedule_next_quiz_prompt()

    def show_quiz_window(self, question, correct_answer):
    # Create a temporary Toplevel window for the quiz
        
        if self.window_open:
            return  # Skip if another window is open

        self.window_open = True
        # Create a temporary Toplevel window
        
        quiz_window = tk.Toplevel(self.root)
        quiz_window.title("Quiz Time!")
        def on_close():
            
            self.set_window_open_false()
            self.window_open = False
            quiz_window.destroy()

        quiz_window.protocol("WM_DELETE_WINDOW", on_close)
        
        # Remove minimize and maximize buttons
        #quiz_window.wm_attributes('-toolwindow', True)
        
        # Set size of the window
        window_width = 300 #400
        window_height = 310  # Adjusted height for buttons and message #210
        quiz_window.geometry(f"{window_width}x{window_height}")

        # Style the window
        quiz_window.configure(bg="#f0f0f0")  # Light gray background
        
        # Create a frame for better layout
        frame = Frame(quiz_window, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Add question label
        question_label = Label(
            frame, 
            text=question, 
            wraplength=window_width-20, 
            font=("Helvetica", 12, "bold"), 
            fg="gray30",  # Dark gray text color
            padx=10, 
            pady=25, 
            relief="solid"
        )
        question_label.pack(pady=5)
        
        # Add buttons frame
        buttons_frame = Frame(frame, bg="#ffffff")
        buttons_frame.pack(pady=5)

        # Result label to display the result message
        result_label = Label(frame, text="", font=("Helvetica", 12), fg="#333333", bg="#ffffff")
        result_label.pack(pady=10)

    


        # Function to check answer and show result
        def check_answer(user_answer):
            
            if user_answer == correct_answer:
                
                if self.count_right%3!=0:

                    result_message = "Correct. Good job!"
                    self.count_right+=1
                    self.root.after(5000, lambda: (self.set_window_open_false(), quiz_window.destroy()))

                elif self.count_right%3==0:
                    result_message = "Great Work!\n Keep up the streak!"
                    self.count_right+=1
                    self.root.after(7000, lambda: (self.set_window_open_false(), quiz_window.destroy()))
            else:
                if self.count_wrong%3!=0:

                    result_message = "Wrong! Try next time."
                    self.count_wrong+=1
                    self.root.after(5000, lambda: (self.set_window_open_false(), quiz_window.destroy()))
                elif self.count_wrong%3==0:
                    result_message = "Wrong Again!\n Take up a Cyber Security course."
                    self.count_wrong+=1
                    self.root.after(7000, lambda: (self.set_window_open_false(), quiz_window.destroy()))
            if 'Wrong' in result_message:
                result_label.config(
                                text=result_message,
                                wraplength=window_width-30,  # Ensure the text wraps within the window width
                                font=("Helvetica", 12, "bold"),  # Slightly larger and bold font
                                bg="#ffcccc",  # Light blue background color
                                fg="#333333",  # Dark gray text color
                                padx=10,  # Increased horizontal padding
                                pady=15,  # Increased vertical padding
                                relief="solid",  # Solid border
                                #bd=2  # Slightly thicker border
                            )
            else:
                result_label.config(
                                text=result_message,
                                wraplength=window_width-30,  # Ensure the text wraps within the window width
                                font=("Helvetica", 12, "bold"),  # Slightly larger and bold font
                                bg="#ccffcc",  # Light blue background color
                                fg="#333333",  # Dark gray text color
                                padx=10,  # Increased horizontal padding
                                pady=15,  # Increased vertical padding
                                relief="solid",  # Solid border
                                #bd=2  # Slightly thicker border
                            )

            true_button.config(state=tk.DISABLED)
            false_button.config(state=tk.DISABLED)

        # Add "True" button
        true_button = Button(
            buttons_frame,
            text="True",
            command=lambda: check_answer("True"),
            font=("Helvetica", 13, "bold"),  # Increased font size
            bg="#00FF00",  # Green background
            fg="white",   # White text
            activebackground="#45a049",  # Darker green on click
            cursor="hand2",  # Hand cursor on hover
            padx=25,  # Increased padding for better appearance
            pady=5  # Increased padding for better appearance
        )
        true_button.pack(side=tk.LEFT, padx=13)  # Adjusted spacing between buttons

        # Add "False" button
        false_button = Button(
            buttons_frame,
            text="False",
            command=lambda: check_answer("False"),
            font=("Helvetica", 13, "bold"),  # Increased font size
            bg="#f44336",  # Red background
            fg="white",   # White text
            activebackground="#d32f2f",  # Darker red on click
            cursor="hand2",  # Hand cursor on hover
            padx=25,  # Increased padding for better appearance
            pady=5  # Increased padding for better appearance
        )
        false_button.pack(side=tk.LEFT, padx=13)

        # Position the window at the bottom right corner above the taskbar
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        taskbar_height = 80  # Adjust this value based on your taskbar height

        x = screen_width - window_width - 10  # 10 pixels from the right edge
        y = screen_height - window_height - taskbar_height - 10  # 10 pixels from the bottom edge, above taskbar

        quiz_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Auto-close window after 10 seconds
        
        self.root.after(36000, lambda: (self.set_window_open_false(), quiz_window.destroy()))
        
    def reset_score_timer(self):
        self.root.after(2400000, self.reset_score)  # Reset score every 4 minutes
    
    def reset_score(self):
        self.count_wrong = 1
        self.count_right = 1
        print("RESETING SCORE")
        self.show_info_window(
            title="Score Reset",
            message="The score has been reset. \n The score gets reset everyday.",
            show_learn_more=False,
            show_dnd=False
        )
        self.reset_score_timer() 

    def schedule_next_quiz_prompt(self):
        
        self.root.after(45000, self.show_quiz_prompt)  # Schedule the next quiz prompt in 45 seconds

    def schedule_quiz_prompt(self):
        self.root.after(15000,self.show_quiz_prompt)
        
    

# Create the main window
root = tk.Tk()
root.withdraw()  # Hide the main window
app = App(root)
root.mainloop()