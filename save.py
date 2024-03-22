import csv
import tkinter as tk
from tkinter import filedialog
from datetime import timedelta

def duration_to_timedelta(duration_str):
    hours, minutes, seconds = map(int, duration_str.split(':'))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

def round_up_to_nearest_15_minutes(duration):
    if duration < timedelta(minutes=15):
        return timedelta(minutes=15)
    remainder = duration.total_seconds() % (15 * 60)
    if remainder == 0:
        return duration
    else:
        return duration + timedelta(seconds=(15 * 60 - remainder))

def read_csv(file_path):
    projects = []
    with open(file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        # Print the headers of the CSV file
        print("CSV Headers:", csvreader.fieldnames)
        
        for row in csvreader:
            duration = duration_to_timedelta(row['Duration'])
            rounded_duration = round_up_to_nearest_15_minutes(duration)
            projects.append({
                'Project': row['ï»¿Project'],
                'Client': row['Client'],
                'Description': row['Description'],
                'Duration_Original': row['Duration'],
                'Duration': rounded_duration
            })
    return projects

def select_files():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv")])
    return file_paths

def timedelta_to_str(duration):
    hours, remainder = divmod(duration.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def main():
    csv_files = select_files()
    if csv_files:
        for csv_file in csv_files:
            projects = read_csv(csv_file)
        
            print(f"Projects from CSV {csv_file}:")
            for project in projects:
                print(f"Project: {project['Project']}")
                print(f"Client: {project['Client']}")
                print(f"Description: {project['Description']}")
                print(f"Duration {project['Duration_Original']}")
                print(f"Duration (rounded up to nearest 15 minutes, minimum 15 minutes): {timedelta_to_str(project['Duration'])}")
                print()

if __name__ == "__main__":
    main()
