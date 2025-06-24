# Task-Tracker-CLI
Task Tracker (CLI) roadmap.sh project

# Adding a new task
python python.clı.py add "Buy apple"
# Output: Task added successfully (ID: 1)

# Updating and deleting tasks
python python.clı.py update 1 "Buy groceries and cook dinner"
task-cli delete 1

# Marking a task as in progress or done
python python.clı.py mark-in-progress 1
task-cli mark-done 1

# Listing all tasks
python python.clı.py list

# Listing tasks by status
python python.clı.py done
|
python python.clı.py todo
|
python python.clı.py in-progress
