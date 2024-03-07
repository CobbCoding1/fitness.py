# import as necessary
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk
import csv
import os
import ast

# initialize global lists to track workouts and goals
workouts = list()
goals = list()

# Main class for the app
# The purpose of this is to handle all the sub pages
class WorkoutApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # init the window
        self.title("fitness.py")
        self.geometry("600x400")

        self.pages = {}
        self.current_page = None

        # List of pages and their names

        self.dashboard_page = DashboardPage(self)
        self.pages["Dashboard"] = self.dashboard_page
        
        self.workout_page = WorkoutPage(self)
        self.pages["Workout Log"] = self.workout_page

        self.goals_page = GoalsPage(self)
        self.pages["Personal Goals"] = self.goals_page

        self.create_navigation_bar()
        # Show dashboard on startup
        self.show_page("Dashboard")

    def create_navigation_bar(self):
        nav_frame = ttk.Frame(self)
        nav_frame.pack(side="top", fill="x")

        # loop over pages and display their names in the navbar
        for page_name in self.pages:
            ttk.Button(nav_frame, text=page_name, command=lambda page=page_name: self.show_page(page)).pack(side="left")

    def show_page(self, page_name):
        if self.current_page:
            self.current_page.pack_forget()
        # set current page
        self.current_page = self.pages[page_name]
        self.current_page.pack(fill="both", expand=True)

    def exit(self):
        # close the window
        self.destroy()

# Class for dashboard
# The purpose of this is to display the most recent exercise
class DashboardPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Init page information
        self.label = ttk.Label(self, text="Dashboard Page")
        self.label.pack(pady=10)

        # set most recent exercise
        self.most_recent = ""
        self.set_most_recent()

        # Labels
        self.recent_exercise_label = ttk.Label(self, text="Most Recently Tracked Exercise: " + self.most_recent)
        self.recent_exercise_label.pack()

        self.exit_button = ttk.Button(self, text="Exit", command=self.master.exit)
        self.exit_button.pack()

    def set_most_recent(self):
        if(workouts):
            self.most_recent = workouts[-1]

    def update_most_recent(self):
        # update the most recent exercise
        self.set_most_recent()
        most_recent = self.most_recent
        self.recent_exercise_label.config(text="Most Recently Tracked Exercise: " + most_recent)


# Class for workout
# The purpose of this is to allow the user to log workouts
class WorkoutPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Init page information
        self.label = ttk.Label(self, text="Workout Log/Calendar Page")
        self.label.pack(pady=10)

        # make sure image exists, if not display alt text
        if(os.path.isfile("dumbbell.png")):
            self.image = Image.open("dumbbell.png")
            self.image = self.image.resize((200, 200), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(self.image)
        else:
            self.photo = None
        self.image_label = ttk.Label(self, image=self.photo, text="ALT: Dumbbell Image")
        self.image_label.image = self.photo  # keep a reference
        self.image_label.pack()

        # Label
        self.date_label = ttk.Label(self, text="Date: " + datetime.now().strftime("%Y-%m-%d"))
        self.date_label.pack()

        # Input 
        self.workout_entry = ttk.Entry(self)
        self.workout_entry.pack()

        # Button
        self.log_button = ttk.Button(self, text="Log Workout", command=self.log_workout)
        self.log_button.pack()

        # workout info
        self.load_workouts()

        self.workouts_label = ttk.Label(self, text="Workouts: ")
        self.workouts_label.pack()

        self.workouts_text = tk.Text(self)
        self.display_workouts()

    def display_workouts(self):
        # display the workouts and update them if they get updated
        self.workouts_text.pack_forget()
        self.workouts_text = ttk.Frame(self)
        for workout in workouts:
            ttk.Label(self.workouts_text, text=workout).pack()
        self.workouts_text.pack()


    def save_workouts(self):
        # open the file and save workouts
        with open("workouts.txt", "w") as file:
            file.write(str(workouts))

    def load_workouts(self):
        # global variable
        global workouts
        # if file exists, load and read from it
        if(os.path.isfile("workouts.txt")):
            with open("workouts.txt", "r") as file:
                content = file.read()

            # convert the list read from the file to a list in the variable
            workouts = ast.literal_eval(content)
            if(self.master.dashboard_page):
                self.master.dashboard_page.update_most_recent()

    def log_workout(self):
        # handle logging of workouts
        self.load_workouts()
        workout = self.workout_entry.get()
        # if workout was empty, then stop here
        if(workout == ""): 
            return 
        workouts.append(workout)
        self.save_workouts()
        self.display_workouts()
        if(self.master.dashboard_page):
            self.master.dashboard_page.update_most_recent()

# Class for goals
# The prupose of this is to allow the user to set goals for themselves, that being a desired weight and a current max
class GoalsPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Init page information
        self.label = ttk.Label(self, text="Personal Goals Page")
        self.label.pack(pady=10)

        # Load and display image
        if(os.path.isfile("stretching-woman.png")):
            self.image = Image.open("stretching-woman.png")
            self.image = self.image.resize((200, 200), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(self.image)
        else:
            self.photo = None
        self.image_label = ttk.Label(self, image=self.photo, text="ALT: Stretching Woman Image")
        self.image_label.image = self.photo  # keep a reference
        self.image_label.pack()

        # Weight label & input
        self.weight_label = ttk.Label(self, text="Weight:")
        self.weight_label.pack()
        self.weight_entry = ttk.Entry(self)
        self.weight_entry.pack()

        # One rep max label & input
        self.max_label = ttk.Label(self, text="One Rep Maxes:")
        self.max_label.pack()
        self.max_entry = ttk.Entry(self)
        self.max_entry.pack()

        # Save button (not implemented yet)
        self.save_button = ttk.Button(self, text="Save Goals", command=self.save_goals)
        self.save_button.pack()

        # goals
        self.load_goals()

        self.goals_label = ttk.Label(self, text="goals: ")
        self.goals_label.pack()

        self.goals_text = tk.Text(self)
        self.display_goals()

    def display_goals(self):
        # display the goals and update if necessary
        self.goals_text.pack_forget()
        self.goals_text = ttk.Frame(self)
        for workout in goals:
            ttk.Label(self.goals_text, text=workout).pack()
        self.goals_text.pack()


    def save_goals_to_file(self):
        # open file and save the goals
        with open("goals.txt", "w") as file:
            file.write(str(goals))

    def load_goals(self):
        # global variable
        global goals
        # if file exists, then read from it
        if(os.path.isfile("goals.txt")):
            with open("goals.txt", "r") as file:
                content = file.read()
            # convert the list read from the file to a list in the variable
            goals = ast.literal_eval(content)

    def save_goals(self):
        weight = self.weight_entry.get()
        maxes = self.max_entry.get()

        # if any are empty or not numbers then end here
        if(maxes == "" or weight == "" or not maxes.isdigit() or not weight.isdigit()): 
            return 

        self.load_goals()
        # append info
        goals.append(f"Weight: {weight}, Max: {maxes}")
        self.save_goals_to_file()
        self.display_goals()
        if(self.master.dashboard_page):
            self.master.dashboard_page.update_most_recent()

# If the program is run as main, then run the mainloop
if __name__ == "__main__":
    app = WorkoutApp()
    app.mainloop()
