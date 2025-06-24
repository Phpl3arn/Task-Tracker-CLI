!!! Task Tracker [CLI] Project RoadMap.SH !!!
!!! https://roadmap.sh/projects/task-tracker !!!

Sample solution for the Task Tracker challenge from roadmap.sh.

How to run

Clone the repository and run the following command:

git clone https://github.com/Phpl3arn/Task-Tracker-CLI.git

# Adding a new task
python python.clı.py add "Buy groceries"
# Output: Task added successfully (ID: 1)

# Updating and deleting tasks
python python.clı.py  update 1 "Buy groceries and cook dinner"
python python.clı.py  delete 1

# Marking a task as in progress or done
python python.clı.py  mark-in-progress 1
python python.clı.py  mark-done 1

# Listing all tasks
python python.clı.py  list

# Listing tasks by status
python python.clı.py  list done
python python.clı.py  list todo
python python.clı.py  list in-progress

Example Output:

┌──(.venv)─(root㉿kali)-[~/PycharmProjects/CLI]
└─# python python.clı.py list

--- All Tasks ---
ID: 1
  Description: Buy apple and cut grass
  Status: todo
  Created At: 2025-06-23 22:34:22
  Updated At: 2025-06-23 22:35:07
--------------------
ID: 2
  Description: walking
  Status: done
  Created At: 2025-06-23 22:36:05
  Updated At: 2025-06-23 22:36:21
--------------------
ID: 3
  Description: watching moovie
  Status: in-progress
  Created At: 2025-06-23 22:37:12
  Updated At: 2025-06-23 22:37:43
--------------------
---------------------

