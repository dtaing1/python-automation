from redminelib import Redmine 

redmine = Redmine('https://redmineb2b.silksoftware.com/', key='')
project = redmine.project.get('subproject-1')

print(project)