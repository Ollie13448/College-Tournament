import tkinter as tk
import json
from tkinter import messagebox
from tkinter import ttk

# Initialize arrays for individuals, teams, events, and rankings
individuals = []
teams = []
events = ["Sporting Event 1", "Academic Event 1", "Sporting Event 2", "Academic Event 2", "Sporting Event 3"]
event_types = ["Individual", "Team"]
event_points = []  # Stores points awarded for each event
individual_choice = None

# Function to enter individual participant
def enter_individual():
    if len(individuals) < 5:
        participant = individual_entry.get()
        individuals.append({"Name": participant, "Scores": []})
        messagebox.showinfo("Success", f"Individual participant '{participant}' has been added.")
        save_data()
        update_individual_dropdown()
    else:
        messagebox.showinfo("Error", "No more spaces available for individual competitors.")

# Function to enter team
def enter_team():
    if len(teams) < 4:
        team_name = team_name_entry.get()
        members = []
        member_entries = []  # Added line to store member entries

        for i in range(4):
            member_entry = ttk.Entry(root, width=20)
            member_entry.grid(row=i+2, column=1, pady=5)
            members.append(member_entry.get())
            member_entries.append(member_entry)  # Store member entry in member_entries list

        # Assign scores to team members
        scores = []
        for member_entry in member_entries:
            score = assign_score(member_entry.get())  # Call the function to assign score for each team member
            scores.append(score)

        # Add team to the teams list
        teams.append({"Team Name": team_name, "Members": members, "Scores": scores})
        messagebox.showinfo("Success", f"Team '{team_name}' has been added.")
        save_data()
    else:
        messagebox.showinfo("Error", "No more spaces available for teams.")

# Function to enter event results
def enter_event_results():
    event = event_choice.current()
    event_name = events[event]
    event_type = event_types[event]

    if event_type == "Individual":
        for i, participant in enumerate(individuals):
            score = individual_scores[i].get()
            participant["Scores"].append(score)

    elif event_type == "Team":
        for i, team in enumerate(teams):
            for j, member in enumerate(team["Members"]):
                score = team_scores[i][j].get()
                # Your logic to handle team event results goes here
    messagebox.showinfo("Success", f"Results for {event_name} ({event_type}) have been entered.")
    save_data()

def calculate_team_score(team_name):
    team_scores = [participant["Scores"] for participant in individuals if participant["Name"] in teams[team_name]["Members"]]
    team_total_score = sum([score for scores in team_scores for score in scores])
    return team_total_score

# Function to calculate total points for a team or individual
def calculate_total_points(name):
    total_points = 0
    # Your logic to calculate total points goes here
    return total_points

# Function to update the individual dropdown box
def update_individual_dropdown():
    global individual_choice

    individual_choice['menu'].delete(0, 'end')  # Clear previous options

    for participant in individuals:
        name = participant["Name"]
        individual_choice['menu'].add_command(label=name, command=tk._setit(individual_var, name))

# Function to assign scores to the selected individual
def assign_scores():
    selected_individual = individual_var.get()
    if not selected_individual:
        messagebox.showinfo("Error", "No individual selected.")
        return

    for participant in individuals:
        if participant["Name"] == selected_individual:
            score = score_entry.get()
            participant["Scores"].append(score)
            messagebox.showinfo("Success", f"Score {score} assigned to {selected_individual}.")
            save_data()
            break

# Function to display details for a team or individual
def display_details():
    name = details_entry.get()
    found = False

    # Search for team details
    for team in teams:
        if team["Team Name"].lower() == name.lower():
            messagebox.showinfo("Team Details", f"Team Name: {team['Team Name']}\nMembersf: {', '.join(team['Members'])}")
            # Calculate and display total points for the team
            total_points = calculate_total_points(team["Team Name"])
            messagebox.showinfo("Team Details", f"Total Points: {total_points}")
            found = True
            break

    # Search for individual details
    if not found:
        for participant in individuals:
            if participant["Name"].lower() == name.lower():
                messagebox.showinfo("Individual Details", f"Individual: {participant['Name']}")
                scores = participant["Scores"]
                if scores:
                    messagebox.showinfo("Individual Details", f"Scores: {', '.join(map(str, scores))}")
                else:
                    messagebox.showinfo("Individual Details", "No scores assigned.")
                found = True
                break

    if not found:
        messagebox.showinfo("Error", "No details found for the entered name.")

# Function to display team details
def display_team_details():
    team_name = details_entry.get()
    if team_name in teams:
        messagebox.showinfo("Team Details", f"Team Name: {team_name}\nMembers: {', '.join(teams[team_name]['Members'])}")
        total_score = calculate_team_score(team_name)
        messagebox.showinfo("Team Details", f"Total Score: {total_score}")
    else:
        messagebox.showinfo("Error", "No details found for the entered team name.")

# Function to save data to a JSON file
def save_data():
    data = {"individuals": individuals, "teams": teams}
    with open("data.json", "w") as file:
        json.dump(data, file)

# Function to load data from a JSON file
def load_data():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            individuals.extend(data.get("individuals", []))
            teams.extend(data.get("teams", []))
    except FileNotFoundError:
        pass

# Load data from the JSON file
load_data()

# Create the main Tkinter window
window = tk.Tk()
window.title("Tournament Management System")

# First Column
left_frame = ttk.Frame(window)
left_frame.grid(row=0, column=0, padx=10, pady=10)

individual_label = ttk.Label(left_frame, text="Add Individual Participant", font=("Arial", 12, "bold"))
individual_label.pack()

individual_entry = ttk.Entry(left_frame)
individual_entry.pack()

individual_button = ttk.Button(left_frame, text="Add Participant", command=enter_individual)
individual_button.pack()

# Add Team section
team_label = ttk.Label(left_frame, text="Add Team", font=("Arial", 12, "bold"))
team_label.pack()

team_name_label = ttk.Label(left_frame, text="Team Name:", font=("Arial", 10))
team_name_label.pack()

team_name_entry = ttk.Entry(left_frame)
team_name_entry.pack()

member_labels = []
member_entries = []
for i in range(5):
    member_label = ttk.Label(left_frame, text=f"Member {i+1}:", font=("Arial", 10))
    member_label.pack()
    member_labels.append(member_label)

    member_entry = ttk.Entry(left_frame)
    member_entry.pack()
    member_entries.append(member_entry)

team_button = ttk.Button(left_frame, text="Add Team", command=enter_team)
team_button.pack()

# Divider
divider = ttk.Separator(window, orient="vertical")
divider.grid(row=0, column=1, sticky="ns", padx=5)

# Second Column
right_frame = ttk.Frame(window)
right_frame.grid(row=0, column=2, padx=10, pady=10)

# Enter Event Results section
event_label = ttk.Label(right_frame, text="Enter Event Results", font=("Arial", 12, "bold"))
event_label.pack()

event_choice_label = ttk.Label(right_frame, text="Select Event:", font=("Arial", 10))
event_choice_label.pack()

event_choice = ttk.Combobox(right_frame, values=events)
event_choice.pack()

individual_scores = []
team_scores = []

event_type = event_types[event_choice.current()]

if event_type == "Individual":
    for i, participant in enumerate(individuals):
        label = ttk.Label(right_frame, text=participant["Name"] + ":")
        label.pack(pady=5)

        score_entry = ttk.Entry(right_frame)
        score_entry.pack()

        individual_scores.append(score_entry)

elif event_type == "Team":
    for team in teams:
        team_label = ttk.Label(right_frame, text=team["Team Name"], font=("Arial", 10, "bold"))
        team_label.pack(pady=5)

        team_scores_label = ttk.Label(right_frame, text="Member Scores:")
        team_scores_label.pack()

        scores = []
        for member in team["Members"]:
            member_label = ttk.Label(right_frame, text=member + ":")
            member_label.pack()

            member_score_entry = ttk.Entry(right_frame)
            member_score_entry.pack()

            scores.append(member_score_entry)

        team_scores.append(scores)

event_button = ttk.Button(right_frame, text="Enter Results", command=enter_event_results)
event_button.pack(pady=10)

# Calculate Total Points section
calculate_label = ttk.Label(right_frame, text="Calculate Total Points", font=("Arial", 12, "bold"))
calculate_label.pack()

individual_choice_label = ttk.Label(right_frame, text="Select Individual:", font=("Arial", 10))
individual_choice_label.pack()

individual_var = tk.StringVar()
individual_choice = ttk.OptionMenu(right_frame, individual_var, None, "")
individual_choice.pack()

score_label = ttk.Label(right_frame, text="Enter Score:", font=("Arial", 10))
score_label.pack()

score_entry = ttk.Entry(right_frame)
score_entry.pack()

assign_button = ttk.Button(right_frame, text="Assign Score", command=assign_scores)
assign_button.pack(pady=10)

# Display Details section
details_label = ttk.Label(right_frame, text="Display Details", font=("Arial", 12, "bold"))
details_label.pack()

details_entry_label = ttk.Label(right_frame, text="Enter Name:", font=("Arial", 10))
details_entry_label.pack()

details_entry = ttk.Entry(right_frame)
details_entry.pack()

display_button = ttk.Button(right_frame, text="Display", command=display_details)
display_button.pack(pady=10)

# Run the Tkinter event loop
window.mainloop()
















