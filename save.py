import csv
from redminelib import Redmine
from datetime import timedelta

# Redmine API endpoint
REDMINE_URL = 'https://your-redmine-instance.com'
# Redmine API access key
REDMINE_API_KEY = 'your-redmine-api-key'

# Function to read project mappings from a CSV file
def read_project_mappings(mapping_file):
    project_mappings = {}
    with open(mapping_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            project_mappings[row['Project']] = row['Identifier']  # Adjust 'Identifier' to match the column name in your CSV
    return project_mappings

# Function to create an issue in Redmine
def create_redmine_issue(redmine, project_id, subject, description, duration):
    redmine_project = redmine.project.get(project_id)
    issue = redmine.issue.new(project_id=redmine_project.id, subject=subject, description=description)
    issue.estimated_hours = duration.total_seconds() / 3600
    issue.save()

# Function to read CSV file and create issues in Redmine
def read_csv_and_create_issues(csv_file, mapping_file):
    redmine = Redmine(REDMINE_URL, key=REDMINE_API_KEY)
    project_mappings = read_project_mappings(mapping_file)
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            project_name = row['ï»¿Project']
            redmine_project_id = project_mappings.get(project_name)
            if redmine_project_id:
                subject = row['Description']
                description = row['Description']
                duration = duration_to_timedelta(row['Duration'])
                create_redmine_issue(redmine, redmine_project_id, subject, description, duration)
            else:
                print(f"No mapping found for project '{project_name}'")

# Function to convert duration string to timedelta object
def duration_to_timedelta(duration_str):
    hours, minutes, seconds = map(int, duration_str.split(':'))
    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

# Example usage
def main():
    csv_file = 'projects.csv'  # Change this to the path of your main CSV file
    mapping_file = 'project_mapping.csv'  # Change this to the path of your mapping CSV file
    read_csv_and_create_issues(csv_file, mapping_file)

if __name__ == "__main__":
    main()
