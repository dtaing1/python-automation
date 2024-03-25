import csv
import tkinter as tk
from tkinter import filedialog
from math import ceil

def duration_to_minutes(duration_str):
    hours, minutes, seconds = map(int, duration_str.split(':'))
    total_minutes = hours * 60 + minutes + (1 if seconds >= 30 else 0)  # Round up if seconds >= 30
    return total_minutes

def round_up_to_nearest_15_minutes(duration):
    if duration < 15:
        return 15
    remainder = duration % 15
    if remainder == 0:
        return duration
    else:
        return duration + (15 - remainder)

def read_csv(file_path):
    projects = []
    with open(file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            duration_minutes = duration_to_minutes(row['Duration'])
            rounded_duration = round_up_to_nearest_15_minutes(duration_minutes)
            projects.append({
                'Project': row['ï»¿Project'],
                'Description': row['Description'],
                'Duration': rounded_duration
            })
    return projects

def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    return file_path

def write_csv(projects, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Project', 'Description', 'Duration']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for project in projects:
            writer.writerow(project)

def main():
    csv_file = select_file()
    if csv_file:
        projects = read_csv(csv_file)
        
        print("Projects from CSV:")
        for project in projects:
            print(f"Project: {project['Project']}")
            print(f"Description: {project['Description']}")
            print(f"Duration (rounded up to nearest 15 minutes (Ceiling function)): {project['Duration']} minutes")
            print()
        
        # Output the rounded data to a new CSV file
        output_file = 'rounded_projects.csv'
        write_csv(projects, output_file)
        print(f"Rounded data written to {output_file}")

if __name__ == "__main__":
    main()
