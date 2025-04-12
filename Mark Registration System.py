import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from tkinter.filedialog import asksaveasfilename
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MarkRegistrationSystem:
    def __init__(self, root):
        self.update_form = None
        self.search = None
        self.root = root
        self.root.title("Mark Registration System")
        self.root.geometry("1650x870")  # Width * Length
        self.tree = ttk.Treeview(root)

        # Add a flag to track if marks have been updated
        self.marks_updated = False

        self.marks_data = []
        self.marks_viewed = False

        # Remove these since they won't be user input anymore
        self.num_students = tk.IntVar()
        self.num_modules = tk.IntVar()
        self.record1_saved = False

        self.module_code = tk.StringVar()
        self.module_name = tk.StringVar()
        self.coursework_1_mark = tk.IntVar()
        self.coursework_2_mark = tk.IntVar()
        self.coursework_3_mark = tk.IntVar()
        self.student_id = tk.StringVar()
        self.student_name = tk.StringVar()
        self.gender = tk.StringVar()
        self.date_of_entry = tk.StringVar()
        self.record2_saved = False

        self.view_module_code = tk.StringVar()
        self.module_code = tk.StringVar()
        self.student_id = tk.StringVar()
        self.student_name = tk.StringVar()
        self.coursework_1_mark = tk.IntVar()
        self.coursework_2_mark = tk.IntVar()
        self.coursework_3_mark = tk.IntVar()
        self.total = tk.IntVar()
        self.record3_saved = False

        self.module_code = tk.StringVar()
        self.student_id = tk.StringVar()
        self.date_of_entry = tk.StringVar()
        self.coursework_1_mark = tk.IntVar()
        self.coursework_2_mark = tk.IntVar()
        self.coursework_3_mark = tk.IntVar()
        self.record4_saved = False

        self.record5_saved = False

        self.current_page = tk.Frame(self.root)
        self.current_page.pack()
        self.show_update_marks()
        self.setup_navigation()
        self.show_home()

    def setup_navigation(self):
        nav_frame = tk.Frame(self.root, bg="#0288d1")
        nav_frame.pack(side=tk.TOP, fill=tk.X)

        nav_buttons = [
            ("Home", self.show_home),
            ("Input Marks", self.show_input_marks),
            ("View Marks", self.show_view_marks),
            ("Update Marks", self.show_update_marks),
            ("Visualisation", self.show_visualisation)
        ]

        for text, command in nav_buttons:
            btn = tk.Button(nav_frame, text=text, bg="#2980B9", fg="sky blue", font=("Arial", 25, "bold"), command=command)
            btn.pack(side=tk.LEFT, padx=50, pady=20)

    def clear_content(self):
        if self.current_page:
            self.current_page.pack_forget()
        self.current_page = tk.Frame(self.root)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_home(self):
        self.clear_content()

        tk.Label(self.current_page, text="Welcome to the Mark Registration System",
                 font=("Arial", 20), pady=30).pack()

        tk.Label(self.current_page, text="Number of Students:", font=("Arial", 15)).pack(pady=10)
        tk.Entry(self.current_page, textvariable=self.num_students).pack(pady=10)

        tk.Label(self.current_page, text="Number of Modules:", font=("Arial", 15)).pack(pady=10)
        tk.Entry(self.current_page, textvariable=self.num_modules).pack(pady=10)

        tk.Button(self.current_page, text="Save Records", command=self.save_records, bg="#00bcd4",
                  fg="black").pack(pady=40)

        tk.Button(self.current_page, text="Next", command=self.next_page1, bg="#4CAF50",
                  fg="white").pack(pady=12)

    def save_records(self):
        if not self.num_students.get() or not self.num_modules.get():
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        record_data = f"Number of Students: {self.num_students.get()}\nNumber of Modules: {self.num_modules.get()}\n"
        filename = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filename:
            try:
                with open(filename, 'a') as file:
                    file.write(record_data)
                    self.record1_saved = True
                messagebox.showinfo("Success", "Records saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Cancelled", "No file selected.")
            self.record1_saved = False

    def next_page1(self):
        if not self.record1_saved:
            messagebox.showerror("Error", "You must save the records before proceeding to the next page!")
            return
        self.show_input_marks()

    def show_input_marks(self):
        self.clear_content()

        tk.Label(self.current_page, text="Mark Entry Form", font=("Arial", 20), pady=1).pack()

        self.create_form_entry("Module Code", self.module_code)
        self.create_form_entry("Module Name", self.module_name)
        self.create_form_entry("Coursework 1 Mark", self.coursework_1_mark)
        self.create_form_entry("Coursework 2 Mark", self.coursework_2_mark)
        self.create_form_entry("Coursework 3 Mark", self.coursework_3_mark)
        self.create_form_entry("Student ID", self.student_id)
        self.create_form_entry("Student Name", self.student_name)
        self.create_form_entry("Date of Entry", self.date_of_entry)

        tk.Label(self.current_page, text="Gender", font=("Arial", 12)).pack(pady=5)
        tk.Radiobutton(self.current_page, text="Male", variable=self.gender, value="Male").pack()
        tk.Radiobutton(self.current_page, text="Female", variable=self.gender, value="Female").pack()

        button_frame = tk.Frame(self.current_page)
        button_frame.pack(pady=10)

        (tk.Button(button_frame, text="Submit Marks", command=self.submit_marks, bg="#00bcd4", fg="black")
         .pack(side=tk.LEFT, padx=10))
        (tk.Button(button_frame, text="Reset", command=self.reset_form, bg="#f44336", fg="black")
         .pack(side=tk.LEFT, padx=10))
        (tk.Button(button_frame, text="Next", command=self.next_page2, bg="#4CAF50", fg="white")
         .pack(side=tk.LEFT, padx=10))

    def create_form_entry(self, label_text, variable):
        tk.Label(self.current_page, text=label_text, font=("Arial", 12)).pack(pady=5)
        tk.Entry(self.current_page, textvariable=variable).pack(pady=5)

    def reset_form(self):
        self.module_code.set("")
        self.module_name.set("")
        self.coursework_1_mark.set(0)
        self.coursework_2_mark.set(0)
        self.coursework_3_mark.set(0)
        self.student_id.set("")
        self.student_name.set("")
        self.gender.set("")
        self.date_of_entry.set("")

    def submit_marks(self):
        if not all([self.module_code.get(), self.module_name.get(), self.coursework_1_mark.get(),
                    self.coursework_2_mark.get(), self.coursework_3_mark.get(), self.student_id.get(),
                    self.student_name.get(), self.gender.get(), self.date_of_entry.get()]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        marks_data = [
            [
                self.module_code.get(),
                self.module_name.get(),
                self.coursework_1_mark.get(),
                self.coursework_2_mark.get(),
                self.coursework_3_mark.get(),
                self.student_id.get(),
                self.student_name.get(),
                self.date_of_entry.get(),
                self.gender.get()  # Added gender to the data list
            ]
        ]

        filename = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filename:
            try:
                file_exists = os.path.isfile(filename)
                with open(filename, mode="a", newline="") as file:
                    writer = csv.writer(file)

                    if not file_exists:
                        writer.writerow(["Module Code", "Module Name", "Coursework 1 Mark", "Coursework 2 Mark",
                                         "Coursework 3 Mark", "Student ID", "Student Name", "Date of Entry", "Gender"])

                    writer.writerows(marks_data)

                self.record2_saved = True
                messagebox.showinfo("Success", "Marks submitted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showwarning("Cancelled", "No file selected.")
            self.record2_saved = False

    def next_page2(self):
        if not self.record2_saved:
            messagebox.showerror("Error", "You must submit the marks before proceeding to the next page!")
            return
        self.show_view_marks()

    def show_view_marks(self):
        self.clear_content()
        self.marks_viewed = False  # Reset the viewed flag when entering the page

        tk.Label(self.current_page, text="View Marks", font=("Arial", 20), pady=10).pack()

        # Search feature
        tk.Label(self.current_page, text="Module Code:", font=("Arial", 12)).pack(pady=5)
        self.search_code = tk.Entry(self.current_page)
        self.search_code.pack(pady=5)

        tk.Button(self.current_page, text="View", command=self.search_marks, bg="#00bcd4", fg="black").pack(pady=10)

        tk.Button(self.current_page, text="Next", command=self.next_page3, bg="#4CAF50", fg="white").pack(pady=10)

        self.tree = ttk.Treeview(self.current_page, columns=("Student ID", "Student Name", "Coursework 1 Mark",
                                                             "Coursework 2 Mark", "Coursework 3 Mark", "Total"),
                                 show="headings")
        self.tree.heading("Student ID", text="Student ID")
        self.tree.heading("Student Name", text="Student Name")
        self.tree.heading("Coursework 1 Mark", text="Coursework 1 Mark")
        self.tree.heading("Coursework 2 Mark", text="Coursework 2 Mark")
        self.tree.heading("Coursework 3 Mark", text="Coursework 3 Mark")
        self.tree.heading("Total", text="Total")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def search_marks(self):
        search_term = self.search_code.get().lower()

        if not search_term:
            messagebox.showerror("Error", "Please enter a module code to search!")
            return

        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            # Clear existing data in the Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Read data from the CSV file
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                found_records = False
                for row in reader:
                    if search_term in row.get("Module Code").lower():
                        found_records = True
                        # Calculate the total by adding the coursework marks
                        total = sum([int(row.get("Coursework 1 Mark", 0)),
                                     int(row.get("Coursework 2 Mark", 0)),
                                     int(row.get("Coursework 3 Mark", 0))])

                        # Insert the row data along with the calculated total
                        self.tree.insert("", tk.END, values=(row.get("Student ID"), row.get("Student Name"),
                                                             row.get("Coursework 1 Mark"), row.get("Coursework 2 Mark"),
                                                             row.get("Coursework 3 Mark"), total))

                if found_records:
                    self.marks_viewed = True  # Set the flag when records are found and displayed
                    messagebox.showinfo("Success", "Records found and displayed!")
                else:
                    messagebox.showinfo("No Results", "No matching records found.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {e}")

    def next_page3(self):
        if not self.marks_viewed:
            messagebox.showerror("Error", "You must view the marks by clicking the 'View' button before proceeding!")
            return
        self.show_update_marks()

    def show_update_marks(self):
        self.clear_content()
        # Reset the marks_updated flag when entering the page
        self.marks_updated = False

        tk.Label(self.current_page, text="Modify Marks", font=("Arial", 20), pady=30).pack()

        self.create_form_entries("Module Code", self.module_code)
        self.create_form_entries("Student ID", self.student_id)
        self.create_form_entries("Date of Entry", self.date_of_entry)
        self.create_form_entries("Coursework 1 Mark", self.coursework_1_mark)
        self.create_form_entries("Coursework 2 Mark", self.coursework_2_mark)
        self.create_form_entries("Coursework 3 Mark", self.coursework_3_mark)

        button_frame = tk.Frame(self.current_page)
        button_frame.pack(pady=50)

        tk.Button(button_frame, text="Search", command=self.search_mark, bg="#00bcd4",
                  fg="black").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Update", command=self.update_marks, bg="#00bcd4",
                  fg="black").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Delete", command=self.delete_record, bg="red",
                  fg="black").pack(side=tk.LEFT, padx=10)

        # Create Next button (initially disabled)
        next_button_frame = tk.Frame(self.current_page)
        next_button_frame.pack(pady=20)
        self.next_button = tk.Button(next_button_frame, text="Next", command=self.next_page4,
                                     bg="#4CAF50", fg="white", state=tk.DISABLED)
        self.next_button.pack()

    def create_form_entries(self, label_text, variable):
        tk.Label(self.current_page, text=label_text, font=("Arial", 12)).pack(pady=5)
        tk.Entry(self.current_page, textvariable=variable).pack(pady=5)

    def search_mark(self):
        search_term = self.student_id.get().strip()
        if not search_term:
            messagebox.showerror("Error", "Please enter a Student ID to search!")
            return

        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Student ID"].strip() == search_term:
                        self.module_code.set(row.get("Module Code", ""))
                        self.date_of_entry.set(row.get("Date of Entry", ""))
                        self.coursework_1_mark.set(int(row.get("Coursework 1 Mark", 0)))
                        self.coursework_2_mark.set(int(row.get("Coursework 2 Mark", 0)))
                        self.coursework_3_mark.set(int(row.get("Coursework 3 Mark", 0)))
                        messagebox.showinfo("Search Results", "Student record found and loaded.")
                        return
            messagebox.showinfo("Search Results", "No matching record found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV file: {e}")

    def update_marks(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            messagebox.showerror("Error", "No file selected!")
            return

        student_id = self.student_id.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Please enter a Student ID to update!")
            return

        updated = False
        updated_rows = []
        temp_file_path = file_path + ".tmp"

        try:
            # Read the original file
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames  # Store the column headers
                for row in reader:
                    if row["Student ID"].strip() == student_id:
                        row["Module Code"] = self.module_code.get()
                        row["Date of Entry"] = self.date_of_entry.get()
                        row["Coursework 1 Mark"] = str(self.coursework_1_mark.get())
                        row["Coursework 2 Mark"] = str(self.coursework_2_mark.get())
                        row["Coursework 3 Mark"] = str(self.coursework_3_mark.get())
                        updated = True
                    updated_rows.append(row)

            # If student ID is found, overwrite the CSV file
            if updated:
                with open(temp_file_path, 'w', newline='', encoding='utf-8') as temp_file:
                    writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(updated_rows)
                    self.record5_saved = True

                os.replace(temp_file_path, file_path)  # Replace the original file
                messagebox.showinfo("Success", "Marks updated successfully!")
                # Enable the Next button after successful update
                self.marks_updated = True
                self.next_button.config(state=tk.NORMAL)
            else:
                messagebox.showwarning("Not Found", "Student ID not found in the CSV file.")

        except Exception as e:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)  # Clean up the temporary file if something goes wrong
            messagebox.showerror("Error", f"Failed to update CSV file: {e}")
            self.record5_saved = False

    def delete_record(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            messagebox.showerror("Error", "No file selected!")
            return

        student_id = self.student_id.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Please enter a Student ID to delete!")
            return

        deleted = False
        updated_rows = []
        temp_file_path = file_path + ".tmp"

        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames  # Store the column headers

                for row in reader:
                    if row["Student ID"].strip() == student_id:
                        deleted = True  # Mark as found
                    else:
                        updated_rows.append(row)  # Keep all other records

            if deleted:
                with open(temp_file_path, 'w', newline='', encoding='utf-8') as temp_file:
                    writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(updated_rows)

                os.replace(temp_file_path, file_path)  # Replace original file
                messagebox.showinfo("Success", f"Student ID {student_id} deleted successfully!")
            else:
                messagebox.showwarning("Not Found", "Student ID not found in the CSV file.")

        except Exception as e:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)  # Clean up temp file if an error occurs
            messagebox.showerror("Error", f"Failed to delete record: {e}")

    def next_page4(self):
        if not self.record5_saved:
            messagebox.showerror("Error", "You need to update marks before proceeding to the next page!")
            return
        self.show_visualisation()

    def show_visualisation(self):
        self.clear_content()

        # Create main container
        viz_frame = tk.Frame(self.current_page)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Module code selection
        input_frame = tk.Frame(viz_frame)
        input_frame.pack(fill=tk.X, pady=10)

        tk.Label(input_frame, text="Enter Module Code:", font=("Arial", 14)).pack(side=tk.LEFT, padx=5)
        module_code_entry = tk.Entry(input_frame, font=("Arial", 14))
        module_code_entry.pack(side=tk.LEFT, padx=5)

        # Initialize graph index
        self.current_graph_index = 0

        def read_csv_data():
            file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
            if not file_path:
                return None

            try:
                with open(file_path, 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    return [row for row in reader]
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read CSV file: {e}")
                return None

        def calculate_grade_distribution(total_marks):
            # Define grade boundaries
            grades = {
                'A': 0,  # 70-100
                'B': 0,  # 60-69
                'C': 0,  # 50-59
                'D': 0,  # 40-49
                'F': 0  # 0-39
            }

            for mark in total_marks:
                if mark >= 70:
                    grades['A'] += 1
                elif mark >= 60:
                    grades['B'] += 1
                elif mark >= 50:
                    grades['C'] += 1
                elif mark >= 40:
                    grades['D'] += 1
                else:
                    grades['F'] += 1

            return grades

        def display_graph(module_data, graph_type):
            # Clear previous graph if exists
            for widget in graph_frame.winfo_children():
                widget.destroy()

            if not module_data:
                messagebox.showerror("Error", "No data available for visualization")
                return

            # Extract data
            student_names = [row['Student Name'] for row in module_data]
            coursework1 = [float(row.get('Coursework 1 Mark', 0)) for row in module_data]
            coursework2 = [float(row.get('Coursework 2 Mark', 0)) for row in module_data]
            coursework3 = [float(row.get('Coursework 3 Mark', 0)) for row in module_data]
            total_marks = [sum(marks) for marks in zip(coursework1, coursework2, coursework3)]

            # Create figure
            fig = plt.Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)

            if graph_type == 'bar':
                ax.bar(student_names, total_marks, color='blue')
                ax.set_title('Total Marks by Student')
                ax.set_xlabel('Student Name')
                ax.set_ylabel('Total Marks')
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

            elif graph_type == 'pie':
                # Calculate grade distribution
                grades = calculate_grade_distribution(total_marks)

                # Prepare data for pie chart
                labels = []
                sizes = []
                colors = ['#2ecc71', '#3498db', '#f1c40f', '#e67e22', '#e74c3c']  # Colors for A, B, C, D, F

                for grade, count in grades.items():
                    if count > 0:  # Only show grades that have students
                        labels.append(f'Grade {grade} ({count})')
                        sizes.append(count)

                if sum(sizes) > 0:  # Only create pie chart if there's data
                    patches, texts, autotexts = ax.pie(sizes,
                                                       labels=labels,
                                                       colors=colors[:len(sizes)],
                                                       autopct='%1.1f%%',
                                                       startangle=90)
                    ax.set_title('Grade Distribution')
                    # Equal aspect ratio ensures that pie is drawn as a circle
                    ax.axis('equal')
                else:
                    ax.text(0.5, 0.5, 'No grade data available',
                            horizontalalignment='center',
                            verticalalignment='center')

            elif graph_type == 'scatter':
                ax.scatter(range(len(student_names)), total_marks, color='orange')
                ax.set_xticks(range(len(student_names)))
                ax.set_xticklabels(student_names)
                ax.set_title('Marks Distribution')
                ax.set_xlabel('Student Name')
                ax.set_ylabel('Total Marks')
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

            elif graph_type == 'line':
                ax.plot(student_names, total_marks, marker='o', color='yellow')
                ax.set_title('Marks Trend')
                ax.set_xlabel('Student Name')
                ax.set_ylabel('Total Marks')
                plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

            fig.tight_layout()

            # Embed in tkinter window
            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        def submit():
            data = read_csv_data()
            if not data:
                return

            module_code = module_code_entry.get()
            module_data = [row for row in data if row['Module Code'] == module_code]

            if not module_data:
                messagebox.showerror("Error", "No data found for the provided module code")
                return

            # Display initial graph
            display_graph(module_data, 'bar')

            # Enable next graph button
            next_button.config(state=tk.NORMAL)

            # Store data for later use
            next_button.module_data = module_data

        def next_graph():
            graph_types = ['bar', 'line', 'scatter', 'pie']
            self.current_graph_index = (self.current_graph_index + 1) % len(graph_types)
            display_graph(next_button.module_data, graph_types[self.current_graph_index])

        # Create submit button
        tk.Button(input_frame, text="Submit", command=submit,
                  bg="#00bcd4", fg="black", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        # Create graph frame
        graph_frame = tk.Frame(input_frame)
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Create next graph button (initially disabled)
        next_button = tk.Button(input_frame, text="Next Graph Type", command=next_graph,
                                bg="#4CAF50", fg="white", font=("Arial", 12), state=tk.DISABLED)
        next_button.pack(side=tk.LEFT, padx=5)

        # Create close button
        tk.Button(input_frame, text="Close", command=self.show_home,
                  bg="#f44336", fg="black", font=("Arial", 12)).pack(side=tk.LEFT, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = MarkRegistrationSystem(root)
    root.mainloop()
