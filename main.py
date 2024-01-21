import itertools
import os
import shutil
import zipfile
import csv
import subprocess
import tkinter as tk
from tkinter import filedialog

class GradingApp:

    def __init__(self, root):
        self.ECLIPSE_WORKSPACE = ""
        self.selected_folder = ""
        self.root = root
        self.root.title("Automated Grading")

        self.grades = []

        self.label = tk.Label(root, text="Select the folder containing student submissions:")
        self.label.pack(pady=10)

        self.folder_button = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.folder_button.pack(pady=10)

        self.process_button = tk.Button(root, text="Start Grading", command=self.start_grading, state=tk.DISABLED)
        self.process_button.pack(pady=10)
        self.selected_folder_var = tk.StringVar()
        self.label2 = tk.Label(root, textvariable=self.selected_folder_var)
        self.label2.pack(pady=10)

    def select_folder(self):
        self.selected_folder = filedialog.askdirectory()
        self.selected_folder_var.set(self.selected_folder)  # Update label text
        self.process_button["state"] = tk.NORMAL

    def start_grading(self):
        if self.selected_folder:
            # Extract and process each student's submission
            grades = self.read_grades(os.path.join(self.selected_folder, 'grades.csv'))
            index = 0
            for student_folder in os.listdir(self.selected_folder):
                student_path = os.path.join(self.selected_folder, student_folder)
                if os.path.isdir(student_path):
                    self.extract_and_grade(student_path, grades[index]['ID'])
                    index += 1
            tk.messagebox.showinfo("Grading Complete", "Grading process completed successfully.")

    def extract_and_grade(self, student_folder, student_id):
        # Step 1: Extracting Zip Files
        zip_path = os.path.normpath(os.path.join(student_folder, 'Submission attachment(s)'))
        if not os.listdir(zip_path):
            return
        print(os.listdir(zip_path)[0])
        zip_path = os.path.join(zip_path, os.listdir(zip_path)[0])
        extract_path = os.path.normpath(os.path.join(student_folder, 'Feedback Attachment(s)'))
        self.extract_zip(zip_path, extract_path)
        self.flatten_all(destination=extract_path)
        shutil.rmtree(os.path.join(extract_path, student_id))
        # Step 2: Reading Grades from CSV

        # Steps 3-6: Automated Grading, Feedback Generation, Writing Feedback
        # (You need to implement your grading logic here)

        # Step 7: Opening Each Submission in Eclipse
        # project_path = os.path.join(student_folder, 'Feedback attachments(s)', "markcia\\")  # Adjust the path accordingly
        # self.open_in_eclipse(project_path)
        eclipse_path = "C:\\Users\\Vince\\eclipse-workspace-ics111\\ics111\\src\\edu\\ics111\\h01\\"
        self.copy_to(eclipse_path, extract_path)

        # Optional: Input grade and feedback using a GUI or prompt
        grade = tk.simpledialog.askstring("Input Grade", f"Enter grade for {student_folder}:")
        feedback = tk.simpledialog.askstring("Input Feedback", f"Enter feedback for {student_folder}:")

        # Update comments.txt
        feedback_path = os.path.join(student_folder, 'comments.txt')
        with open(feedback_path, 'w') as feedback_file:
            feedback_file.write(feedback)

    @staticmethod
    def extract_zip(zip_path, extract_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

    @staticmethod
    def read_grades(csv_file):
        students = []
        with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
            lines = csvfile.readlines()[2:]  # Skip the first two lines
            reader = csv.DictReader(lines)
            for row in reader:
                students.append(row)
        return students


    @staticmethod
    def write_grades(csv_file, grades):
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Display ID', 'ID', 'Last Name', 'First Name', 'grade', 'Submission date', 'Late submission']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for student_id, grade in grades.items():
                writer.writerow({'ID': student_id, 'grade': grade})

    @staticmethod
    def open_in_eclipse(project_path):
        eclipse_command = ''
        subprocess.run([eclipse_command, "-data" + project_path])

    @staticmethod
    def flatten_all(destination):
        all_files = []
        for top, _dirs, files in itertools.islice(os.walk(destination), 1, None):
            for filename in files:
                all_files.append(os.path.join(top, filename))
        for filename in all_files:
            shutil.move(filename, destination)

    @staticmethod
    def copy_to(destination, source):
        for filename in os.listdir(source):
            shutil.copy(os.path.join(source, filename), os.path.join(destination, filename))

if __name__ == "__main__":
    root = tk.Tk()
    app = GradingApp(root)
    root.mainloop()
