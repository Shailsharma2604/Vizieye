# import tkinter as tk
# from tkinter import messagebox
# import subprocess

# def run_project(project_name):
#     """Function to run the selected project using subprocess."""
#     try:
#         subprocess.Popen(["python", project_name])  # Run the project script
#     except Exception as e:
#         messagebox.showerror("Error", f"Failed to launch {project_name}: {e}")

# def create_gui():
#     """Create a GUI with buttons to run different projects."""
#     # Initialize the Tkinter window
#     root = tk.Tk()
#     root.title("Project Launcher")
#     root.geometry("300x200")

#     # Create buttons for each project
#     button1 = tk.Button(root, text="Launch Project 1 (final1)", width=25, command=lambda: run_project('final.py'))
#     button1.pack(pady=10)

#     button2 = tk.Button(root, text="Launch Project 2 (final2)", width=25, command=lambda: run_project('final2.py'))
#     button2.pack(pady=10)

#     button3 = tk.Button(root, text="Launch Project 3 (final3)", width=25, command=lambda: run_project('final3.py'))
#     button3.pack(pady=10)

#     # Run the Tkinter event loop
#     root.mainloop()

# if __name__ == "__main__":
#     create_gui()



import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def run_project(project_name):
    """Function to run the selected project using subprocess."""
    try:
        # Get the absolute path of the project script
        project_path = os.path.join(os.getcwd(), project_name)
        
        # Check if the file exists
        if not os.path.exists(project_path):
            raise FileNotFoundError(f"File {project_name} not found in {os.getcwd()}")

        # Run the project script
        subprocess.Popen(["python", project_path])  # Run the project script
    except Exception as e:
        messagebox.showerror("Error", f"Failed to launch {project_name}: {e}")

def create_gui():
    """Create a GUI with buttons to run different projects."""
    # Initialize the Tkinter window
    root = tk.Tk()
    root.title("Project Launcher")
    root.geometry("300x200")

    # Create buttons for each project
    button1 = tk.Button(root, text="Launch Project 1 (final1)", width=25, command=lambda: run_project('final.py'))
    button1.pack(pady=10)

    button2 = tk.Button(root, text="Launch Project 2 (final2)", width=25, command=lambda: run_project('final2.py'))
    button2.pack(pady=10)

    button3 = tk.Button(root, text="Launch Project 3 (final3)", width=25, command=lambda: run_project('final3.py'))
    button3.pack(pady=10)

    # Run the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    create_gui()
