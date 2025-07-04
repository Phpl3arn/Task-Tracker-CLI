import sys
import json
import os
from datetime import datetime

# Define the name of the JSON file where tasks will be stored.
TASK_FILE = 'tasks.json'


def _load_tasks():
    """
    Loads tasks from the JSON file.

    If the file does not exist, an empty list is returned.
    Handles potential JSON decoding errors (e.g., if the file is corrupted)
    by printing an error and returning an empty list, preventing the application from crashing.
    """
    if not os.path.exists(TASK_FILE):
        return []
    try:
        with open(TASK_FILE, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        return tasks
    except json.JSONDecodeError:
        print(
            f"Error: Could not decode JSON from {TASK_FILE}. The file might be corrupted. Starting with an empty task list.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading tasks: {e}")
        return []


def _save_tasks(tasks):
    """
    Saves the current list of tasks to the JSON file.

    Tasks are saved with an indentation of 4 spaces for readability.
    Handles potential errors during file writing.
    """
    try:
        with open(TASK_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=4)
    except Exception as e:
        print(f"Error: Could not save tasks to {TASK_FILE}: {e}")


def _get_next_id(tasks):
    """
    Generates the next unique integer ID for a new task.

    If there are no existing tasks, the first ID will be 1.
    Otherwise, it finds the maximum existing ID and increments it.
    """
    if not tasks:
        return 1
    # Ensure all task IDs are integers before finding the maximum
    return max(task['id'] for task in tasks if isinstance(task.get('id'), int)) + 1


def add_task(description):
    """
    Adds a new task with the given description.

    The task is initialized with 'todo' status and current timestamps for
    'createdAt' and 'updatedAt'.
    """
    tasks = _load_tasks()
    new_id = _get_next_id(tasks)
    now = datetime.now().isoformat()  # Store date and time in ISO 8601 format
    new_task = {
        'id': new_id,
        'description': description,
        'status': 'todo',  # Default status for new tasks
        'createdAt': now,
        'updatedAt': now
    }
    tasks.append(new_task)
    _save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")


def update_task(task_id, new_description):
    """
    Updates the description of an existing task.

    The 'updatedAt' timestamp is also updated.
    Prints an error if the task ID is not found.
    """
    tasks = _load_tasks()
    found = False
    for task in tasks:
        if task.get('id') == task_id:  # Use .get() for safer access, though 'id' is guaranteed
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            found = True
            break
    if found:
        _save_tasks(tasks)
        print(f"Task {task_id} updated successfully.")
    else:
        print(f"Error: Task with ID {task_id} not found.")


def delete_task(task_id):
    """
    Deletes a task by its ID.

    Prints an error if the task ID is not found.
    """
    tasks = _load_tasks()
    initial_len = len(tasks)
    # Filter out the task with the given ID
    tasks = [task for task in tasks if task.get('id') != task_id]
    if len(tasks) < initial_len:  # Check if a task was actually removed
        _save_tasks(tasks)
        print(f"Task {task_id} deleted successfully.")
    else:
        print(f"Error: Task with ID {task_id} not found.")


def mark_task(task_id, new_status):
    """
    Marks a task with a new status ('in-progress' or 'done').

    The 'updatedAt' timestamp is also updated.
    Prints an error if the task ID is not found.
    """
    tasks = _load_tasks()
    found = False
    for task in tasks:
        if task.get('id') == task_id:
            task['status'] = new_status
            task['updatedAt'] = datetime.now().isoformat()
            found = True
            break
    if found:
        _save_tasks(tasks)
        print(f"Task {task_id} marked as '{new_status}'.")
    else:
        print(f"Error: Task with ID {task_id} not found.")


def list_tasks(status_filter=None):
    """
    Lists tasks, optionally filtered by status.

    If status_filter is None, all tasks are listed.
    Accepts 'todo', 'in-progress', 'done' as filters.
    Formats the output for clear readability, including creation and update times.
    """
    tasks = _load_tasks()

    if not tasks:
        print("No tasks found.")
        return

    filtered_tasks = []
    if status_filter and status_filter != 'all':  # 'all' is treated as no filter
        for task in tasks:
            if task.get('status') == status_filter:
                filtered_tasks.append(task)
    else:
        filtered_tasks = tasks

    if not filtered_tasks:
        if status_filter:
            print(f"No tasks found with status '{status_filter}'.")
        else:
            # This case should ideally be caught by 'if not tasks:' but provides extra robustness.
            print("No tasks found.")
        return

    # Print header based on filter
    header = "All Tasks" if status_filter is None or status_filter == 'all' else f"{status_filter.capitalize()} Tasks"
    print(f"\n--- {header} ---")

    # Sort tasks by ID for consistent listing
    filtered_tasks.sort(key=lambda t: t.get('id', 0))

    for task in filtered_tasks:
        task_id = task.get('id', 'N/A')
        description = task.get('description', 'No description')
        status = task.get('status', 'unknown')
        createdAt_str = task.get('createdAt', 'N/A')
        updatedAt_str = task.get('updatedAt', 'N/A')

        # Attempt to format dates, handle errors if date string is invalid
        try:
            created_at = datetime.fromisoformat(createdAt_str).strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            created_at = createdAt_str  # Keep original if invalid format

        try:
            updated_at = datetime.fromisoformat(updatedAt_str).strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            updated_at = updatedAt_str  # Keep original if invalid format

        print(f"ID: {task_id}")
        print(f"  Description: {description}")
        print(f"  Status: {status}")
        print(f"  Created At: {created_at}")
        print(f"  Updated At: {updated_at}")
        print("-" * 20)  # Separator for tasks
    print("---------------------\n")


def print_usage():
    """
    Prints the command-line usage instructions for the Task Tracker CLI.
    This is displayed when incorrect commands or arguments are provided.
    """
    print("Usage:")
    print("  python task_cli.py add \"<description>\"")
    print("  python task_cli.py update <id> \"<new description>\"")
    print("  python task_cli.py delete <id>")
    print("  python task_cli.py mark-in-progress <id>")
    print("  python task_cli.py mark-done <id>")
    print("  python task_cli.py list [todo|in-progress|done|all]")
    print("\nExamples:")
    print("  python task_cli.py add \"Buy groceries\"")
    print("  python task_cli.py update 1 \"Buy groceries and cook dinner\"")
    print("  python task_cli.py list done")
    print("  python task_cli.py list all")


def main():
    """
    The main function that serves as the entry point for the CLI application.
    It parses command-line arguments and calls the appropriate task management function.
    Handles basic argument validation and error messages.
    """
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)  # Exit with an error code

    command = sys.argv[1].lower()  # The command (e.g., 'add', 'list')

    if command == 'add':
        if len(sys.argv) < 3:
            print("Error: Missing task description for 'add' command.")
            print_usage()
            sys.exit(1)
        description = sys.argv[2]
        add_task(description)
    elif command == 'update':
        if len(sys.argv) < 4:
            print("Error: Missing task ID or new description for 'update' command.")
            print_usage()
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
            new_description = sys.argv[3]
            update_task(task_id, new_description)
        except ValueError:
            print("Error: Task ID must be a number.")
            print_usage()
            sys.exit(1)
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Error: Missing task ID for 'delete' command.")
            print_usage()
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
            delete_task(task_id)
        except ValueError:
            print("Error: Task ID must be a number.")
            print_usage()
            sys.exit(1)
    elif command == 'mark-in-progress':
        if len(sys.argv) < 3:
            print("Error: Missing task ID for 'mark-in-progress' command.")
            print_usage()
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
            mark_task(task_id, 'in-progress')
        except ValueError:
            print("Error: Task ID must be a number.")
            print_usage()
            sys.exit(1)
    elif command == 'mark-done':
        if len(sys.argv) < 3:
            print("Error: Missing task ID for 'mark-done' command.")
            print_usage()
            sys.exit(1)
        try:
            task_id = int(sys.argv[2])
            mark_task(task_id, 'done')
        except ValueError:
            print("Error: Task ID must be a number.")
            print_usage()
            sys.exit(1)
    elif command == 'list':
        status_filter = None
        if len(sys.argv) >= 3:
            filter_arg = sys.argv[2].lower()
            if filter_arg in ['todo', 'in-progress', 'done', 'all']:
                status_filter = filter_arg
            else:
                print(f"Error: Invalid list filter '{filter_arg}'. Use 'todo', 'in-progress', 'done', or 'all'.")
                print_usage()
                sys.exit(1)
        list_tasks(status_filter)
    else:
        print(f"Error: Unknown command '{command}'.")
        print_usage()
        sys.exit(1)


# This ensures that main() is called only when the script is executed directly,
# not when imported as a module.
if __name__ == "__main__":
    main()
