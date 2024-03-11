# For this project I wanted to create a working task manager but decided I wanted
# to implement a GUI. It was quite complicated and I'm not particularly pleased 
# with the actual code. I'm sure there are ways to simplfy but retain the functionality.
# However, as a working application, I am pleased with the results and look forward to 
# recieving feedback and aim to refine it with more time.

import customtkinter
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("600x500")

# Global variables to store the current user and username_password dictionary.
# We need to be able to access them due to having widgets, entry boxes and 
# multiple functions needing user entry validation. 
current_user = None
username_password = {}

# Refactored login function
def login():
    '''This code reads usernames and password from the user.txt file to 
        allow a user to login.
    '''
    global current_user  # Declare current_user as a global variable

    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    # Read in user_data
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Convert to a dictionary
    # Declare the password as a global variable for use outside this function.
    global username_password
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    # Clear previous messages
    message_label.configure(text="")

    logged_in = False
    while not logged_in:
        curr_user = entry1.get()
        curr_pass = entry2.get()
        if curr_user not in username_password.keys():
            message_label.configure(text="User does not exist")
            break
        elif username_password[curr_user] != curr_pass:
            message_label.configure(text="Wrong password")
            break
        else:
            message_label.configure(text="Login Successful!")
            logged_in = True
            current_user = curr_user  # Set the current user
            # Show the menu frame and hide the login frame
            menu_frame.pack(pady=20, padx=60, fill="both", expand=True)
            login_frame.pack_forget()

def username_checker(username):
    try:
        with open("user.txt", "r") as file:
            for line in file:
                name_taken, _ = line.strip().split(";")
                if name_taken == username:
                    return True  # Username already taken.
        return False  # Username is available.
    except FileNotFoundError:
        return False  # Assuming username is available when the file doesn't exist.

def reg_user():
    new_username = enter_new_username.get()
    
    if username_checker(new_username):
        message_label_reg_user.configure(text="That username is taken, please try again!")
        return

    new_password = enter_new_password.get()
    confirm_password = enter_confirm_password.get()
    
    # Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # If they are the same, add them to the user.txt file
        message_label_reg_user.configure(text="New user added")

        with open("user.txt", "a") as out_file: 
            out_file.write(f"\n{new_username};{new_password}")
    else:
        message_label_reg_user.configure(text="Passwords don't match")

def validate_due_date(task_due_date):
    try:
        due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
        return due_date_time
    except ValueError:
        message_label_add_task.configure(text="Incorrect Datetime Format Used")
        return None

def add_task():
    task_username = enter_task_username.get()
    task_title = enter_task_title.get()
    task_description = enter_task_description.get()
    task_due_date = enter_task_duedate.get()

    submit_task(task_username, task_title, task_description, task_due_date)

def submit_task(task_username, task_title, task_description, task_due_date):
    if username_checker(task_username):
        due_date_time = validate_due_date(task_due_date)
        if due_date_time:
            curr_date = date.today()

            new_task = {
                "task_number": len(task_list) + 1,
                "username": task_username,
                "title": task_title,
                "description": task_description,
                "due_date": due_date_time,
                "assigned_date": curr_date,
                "completed": False
            }

            task_list.append(new_task)
            with open("tasks.txt", "w") as task_file:
                task_list_to_write = []
                for t in task_list:
                    str_attrs = [
                        str(t['task_number']),
                        t['username'],
                        t['title'],
                        t['description'],
                        t['due_date'].strftime(DATETIME_STRING_FORMAT),
                        t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                        "Yes" if t['completed'] else "No"
                    ]
                    task_list_to_write.append(";".join(str_attrs))
                task_file.write("\n".join(task_list_to_write))
            message_label_add_task.configure(text="Task Successfully Added")
    else:
        message_label_add_task.configure(text="User does not exist. Please enter a valid username")

def mark_as_complete():           
    task_choice = int(edit_task_choice.get())
    task_found = False

    for t in task_list:
        if int(t['task_number']) == task_choice:
            disp_str = f"\nTask Number: \t {t['task_number']}\n" 
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"Task Complete? \n {t['completed']}\n"   
                
            if not t['completed'] and t['username'] == current_user:  # Check if the task is not already completed.
                t['completed'] = True
                message_label_mark_complete.configure(text="Task marked as complete successfully.")
                edit_task_button.configure(state="disabled")  # Disable the edit button for completed tasks.
            else:
                message_label_mark_complete.configure(text="Task is assigned elsewhere or is already complete!")

            task_found = True
            break

    if not task_found:
        message_label_mark_complete.configure(text="Task not found")

    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                str(t['task_number']),  # Write the task number to start of tasks.txt file.
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

# Validation function tied to edit task button.
def validate_task_number(current_user):
    task_number = edit_task_choice.get()
    if task_number.isdigit():
        task_choice = int(task_number)
        for t in task_list:
            if int(t['task_number']) == task_choice and t['username'] == current_user and not t['completed']:
                edit_task_button.configure(state="normal")
                return
        else:
            edit_task_button.configure(state="disabled")
    else:
        edit_task_button.configure(state="disabled")

def edit_task():
    task_choice = int(edit_task_choice.get())

    for t in task_list:
        if int(t['task_number']) == task_choice:
            disp_str = f"\nTask Number: \t {t['task_number']}\n" 
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"Task Complete? \n {t['completed']}\n"     

            new_user = assign_different_user.get()  # Getting new user input.
            new_date = change_date.get()  # Getting new date input.

            if new_user:  # Checking if new user input is provided.
                if new_user in username_password:  # Checking if the new user exists.
                    t['username'] = new_user  # Assigning the task to the new user.
                else:
                    message_label_edit_task.configure(text="User does not exist!")
                    return

            if new_date:  # Checking if new date input is provided.
                try:
                    new_due_date = datetime.strptime(new_date, DATETIME_STRING_FORMAT)
                    t['due_date'] = new_due_date  # Changing the due date of the task.
                except ValueError:
                    message_label_edit_task.configure(text=f"Incorrect date format. Please use {DATETIME_STRING_FORMAT}")
                    return

            message_label_edit_task.configure(text="Task updated successfully")
            break
    else:
        message_label_edit_task.configure(text="Task Not Found")

    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                str(t['task_number']), 
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

def view_all():
    '''Reads the tasks from task_list and displays them in the GUI.'''
    tasks_text = ""
    for t in task_list:
        task_text = f"\nTask Number: \t {t['task_number']}\n"
        task_text += f"Task: \t\t {t['title']}\n"
        task_text += f"Assigned to: \t {t['username']}\n"
        task_text += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        task_text += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        task_text += f"Task Description: \n {t['description']}\n\n"
        tasks_text += task_text

    all_tasks_box.insert(0.0, tasks_text)

def view_mine(current_user):
    '''Reads the task from task.txt file and prints to the console in the 
           format of Output 2 presented in the task pdf (i.e. includes spacing
           and labelling)
        '''
    tasks_text = ""
    for t in task_list:
        if t['username'] == current_user:
            disp_str = f"\nTask Number: \t {t['task_number']}\n" 
            disp_str += f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            tasks_text += disp_str

    my_tasks_box.insert(0.0, tasks_text)

def generate_reports():
    total_tasks = len(task_list)
    completed_tasks = sum(t['completed'] for t in task_list)
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'] < datetime.now())
    incomplete_and_overdue_tasks = sum(1 for t in task_list if not t['completed'] and t['due_date'] < datetime.now())

    # Write task overview report
    task_overview_text = f"Total number of tasks: {total_tasks}\n"
    task_overview_text += f"Total completed tasks: {completed_tasks}\n"
    task_overview_text += f"Total incomplete tasks: {incomplete_tasks}\n"
    task_overview_text += f"Total incomplete and overdue tasks: {incomplete_and_overdue_tasks}\n"
    task_overview_text += f"Percentage of tasks that are incomplete: {100 * incomplete_tasks / total_tasks}%\n"
    task_overview_text += f"Percentage of tasks that are overdue: {100 * overdue_tasks / total_tasks}%\n"

    # Write to GUI.
    total_task_box.insert(0.0, "Task Overview: \n\n" + task_overview_text)

    # Write to file.
    with open("task_overview.txt", "w") as file:
        file.write(task_overview_text)

    # Calculate user statistics
    user_statistics = {}
    for user in username_password.keys():
        tasks_assigned = sum(1 for t in task_list if t['username'] == user)
        tasks_completed = sum(1 for t in task_list if t['username'] == user and t['completed'])
        tasks_incomplete = tasks_assigned - tasks_completed
        tasks_overdue = sum(1 for t in task_list if t['username'] == user and not t['completed'] and t['due_date'] < datetime.now())
        if tasks_assigned != 0:
            percent_tasks_assigned = tasks_assigned / total_tasks * 100
            percent_tasks_completed = tasks_completed / tasks_assigned * 100
            percent_tasks_incomplete = tasks_incomplete / tasks_assigned * 100
            percent_tasks_overdue = tasks_overdue / tasks_assigned * 100
        else:
            percent_tasks_assigned = 0
            percent_tasks_completed = 0
            percent_tasks_incomplete = 0
            percent_tasks_overdue = 0
        user_statistics[user] = {
            'tasks_assigned': tasks_assigned,
            'percent_tasks_assigned': percent_tasks_assigned,
            'percent_tasks_completed': percent_tasks_completed,
            'percent_tasks_incomplete': percent_tasks_incomplete,
            'percent_tasks_overdue': percent_tasks_overdue
        }

    # Write user overview report
    user_overview_text = f"Total number of registered users: {len(username_password)}\n"
    user_overview_text += f"Total number of tasks that have been created: {total_tasks}\n"
    user_overview_text += "\nUser Statistics:\n\n"
    for user, stats in user_statistics.items():
        user_overview_text += f"User: {user}\n"
        user_overview_text += f"Total tasks assigned: {stats['tasks_assigned']}\n"
        user_overview_text += f"Percentage of total tasks assigned: {stats['percent_tasks_assigned']:.2f}%\n"
        user_overview_text += f"Percentage of assigned tasks complete: {stats['percent_tasks_completed']:.2f}%\n"
        user_overview_text += f"Percentage of tasks still to be completed: {stats['percent_tasks_incomplete']:.2f}%\n"
        user_overview_text += f"Percentage of tasks incomplete and overdue: {stats['percent_tasks_overdue']:.2f}%\n\n"

    # Write to GUI.
    total_task_box.insert(0.0, user_overview_text)

    # Write to file
    with open("user_overview.txt", "w") as file:
        file.write(user_overview_text)

def display_statistics():
    num_users = len(username_password.keys())
    num_tasks = len(task_list)
    
    if current_user == 'admin':
        view_statistics_box.insert(0.0, f"Number of users: {num_users}"
                                   f"\nNumber of Tasks: {num_tasks}")
        # Clear the message label
        message_label_stat.configure(text="")
    else: 
        message_label_stat.configure(text="Only Admin can view statistics. Sorry!")


# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['task_number'] = task_components[0]
    curr_t['username'] = task_components[1]
    curr_t['title'] = task_components[2]
    curr_t['description'] = task_components[3]
    curr_t['due_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[5], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[6] == "Yes" else False

    task_list.append(curr_t)




######## |||||||| FRAME CHANGE FUNCTIONS ########
        
def return_to_menu(current_frame):
    # Hide the current frame and show the main menu frame.
    current_frame.pack_forget()
    menu_frame.pack(pady=20, padx=60, fill="both", expand=True)
                
def show_reg_user_frame():
    # Hide the menu frame and show the register user frame.
    menu_frame.pack_forget()
    reg_user_frame.pack(pady=20, padx=60, fill="both", expand=True)

def show_add_task_frame():
    # Hide the menu frame and show the add task frame.
    menu_frame.pack_forget()
    add_task_frame.pack(pady=20, padx=60, fill="both", expand=True)

def show_view_all_tasks_frame():
    # Hide the menu frame and show the view all tasks frame.
    menu_frame.pack_forget()
    view_all_tasks_frame.pack(pady=20, padx=60, fill="both", expand=True)
    view_all()

def show_view_my_tasks_frame():
    # Hide the menu frame and show the view my tasks frame.
    menu_frame.pack_forget()
    view_my_tasks_frame.pack(pady=20, padx=60, fill="both", expand=True)
    view_mine(current_user)

def show_edit_task_frame():
    # Hide the view_my_tasks frame and show the edit task frame.
    view_my_tasks_frame.pack_forget()
    edit_task_frame.pack(pady=20, padx=60, fill="both", expand=True)
    # Disable the edit task button initially.
    edit_task_button.configure(state="disabled")

def show_reports_frame():
    # Hide the menu frame and show the reports frame.
    menu_frame.pack_forget()
    view_reports_frame.pack(pady=20, padx=60, fill="both", expand=True)
    generate_reports()

def show_statistics_frame():
    # Hide the menu frame and show the reports frame.
    menu_frame.pack_forget()
    view_statistics_frame.pack(pady=20, padx=60, fill="both", expand=True)
    display_statistics()

def logout_and_reset():
    # Hide all frames.
    menu_frame.pack_forget()
    reg_user_frame.pack_forget()
    add_task_frame.pack_forget()
    view_all_tasks_frame.pack_forget()
    view_my_tasks_frame.pack_forget()
    edit_task_frame.pack_forget()
    view_reports_frame.pack_forget()
    view_statistics_frame.pack_forget()
    login_frame.pack(pady=20, padx=60, fill="both", expand=True)
    
    # Clear any input fields or message labels.
    entry1.delete(0, 'end')  # Clear username entry.
    entry2.delete(0, 'end')  # Clear password entry.
    message_label.configure(text="")  # Clear login message label.
    message_label_reg_user.configure(text="")  # Clear register user message label.
    message_label_add_task.configure(text="")  # Clear add task message label.
    message_label_mark_complete.configure(text="")  # Clear mark complete message label.
    message_label_edit_task.configure(text="")  # Clear edit task message label.
    all_tasks_box.delete(0.0, 'end')  # Clear view all tasks box.
    my_tasks_box.delete(0.0, 'end')  # Clear view my tasks box.
    assign_different_user.delete(0, 'end')  # Clear assign different user entry.
    change_date.delete(0, 'end')  # Clear change date entry.
    view_statistics_box.delete(0.0, 'end')  # Clear view statistics box.
    if edit_task_choice:
        edit_task_choice.delete(0, 'end')  # Clear edit task choice entry only if filled.
    


######## |||||||| WIDGETS |||||||| ########

# Login Frame Widgets.
login_frame = customtkinter.CTkFrame(master=root)
login_frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=login_frame, text="Task Manager", font=("Roboto", 24))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=login_frame, placeholder_text="Username")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=login_frame, placeholder_text="Password", show="*")
entry2.pack(pady=12, padx=10)

button = customtkinter.CTkButton(master=login_frame, text="Login", command=login)
button.pack(pady=12, padx=10)

message_label = customtkinter.CTkLabel(master=login_frame, text="", font=("Roboto", 12))
message_label.pack(pady=12, padx=10)


# Main Menu Frame Widgets.
menu_frame = customtkinter.CTkFrame(master=root)

label = customtkinter.CTkLabel(master=menu_frame, text="Main Menu", font=("Roboto", 24))
label.pack(pady=12, padx=10)

menu_message_label = customtkinter.CTkLabel(master=menu_frame, text="Please Choose from the following options:", font=("Roboto", 12))
menu_message_label.pack(pady=8, padx=10)

reg_user_button = customtkinter.CTkButton(master=menu_frame, text="Register A User", command=show_reg_user_frame)
reg_user_button.pack(pady=8, padx=10)

add_task_button = customtkinter.CTkButton(master=menu_frame, text="Add A Task", command=show_add_task_frame)
add_task_button.pack(pady=8, padx=10)

view_all_button = customtkinter.CTkButton(master=menu_frame, text="View All Tasks", command=show_view_all_tasks_frame)
view_all_button.pack(pady=8, padx=10)

view_my_button = customtkinter.CTkButton(master=menu_frame, text="View My Tasks", command=show_view_my_tasks_frame)
view_my_button.pack(pady=8, padx=10)

generate_reports_button = customtkinter.CTkButton(master=menu_frame, text="Generate Reports", command=show_reports_frame)
generate_reports_button.pack(pady=8, padx=10)

display_statistics_button = customtkinter.CTkButton(master=menu_frame, text="View Statistics", command=show_statistics_frame)
display_statistics_button.pack(pady=8, padx=10)

logout_button = customtkinter.CTkButton(master=menu_frame, text="Logout", command=logout_and_reset)
logout_button.pack(pady=15, padx=10)



# Register User Widgets.
reg_user_frame = customtkinter.CTkFrame(master=root)

label_reg_user = customtkinter.CTkLabel(master=reg_user_frame, text="Register User", font=("Roboto", 24))
label_reg_user.pack(pady=12, padx=10)

label = customtkinter.CTkLabel(master=reg_user_frame, text="Enter New Username (case sensitive)", font=("Roboto", 10))
label.pack(padx=5)
enter_new_username = customtkinter.CTkEntry(master=reg_user_frame)
enter_new_username.pack(pady=5, padx=5)

label = customtkinter.CTkLabel(master=reg_user_frame, text="Enter Password (case sensitive)", font=("Roboto", 10))
label.pack(padx=5)
enter_new_password = customtkinter.CTkEntry(master=reg_user_frame, show="*")
enter_new_password.pack(pady=5, padx=5)

label = customtkinter.CTkLabel(master=reg_user_frame, text="Confirm Password", font=("Roboto", 10))
label.pack(padx=5)
enter_confirm_password = customtkinter.CTkEntry(master=reg_user_frame, show="*")
enter_confirm_password.pack(pady=5, padx=5)

button_register_user = customtkinter.CTkButton(master=reg_user_frame, text="Register New User", command=reg_user)
button_register_user.pack(pady=12, padx=10)

message_label_reg_user = customtkinter.CTkLabel(master=reg_user_frame, text="", font=("Roboto", 12))
message_label_reg_user.pack(pady=12, padx=10)

return_to_menu_button = customtkinter.CTkButton(master=reg_user_frame, text="Return to Menu", 
                                                command=lambda: return_to_menu(reg_user_frame))
return_to_menu_button.pack(pady=15, padx=10)


# Add Task Widgets.
add_task_frame = customtkinter.CTkFrame(master=root)

label_reg_user = customtkinter.CTkLabel(master=add_task_frame, text="Add a task", font=("Roboto", 24))
label_reg_user.pack(pady=12, padx=10)

label = customtkinter.CTkLabel(master=add_task_frame, text="Name of person assigned to task (case sensitive)", font=("Roboto", 10))
label.pack(padx=5)
enter_task_username = customtkinter.CTkEntry(master=add_task_frame)
enter_task_username.pack(pady=5, padx=5)

label = customtkinter.CTkLabel(master=add_task_frame, text="Task Title", font=("Roboto", 10))
label.pack(padx=5)
enter_task_title = customtkinter.CTkEntry(master=add_task_frame)
enter_task_title.pack(pady=5, padx=5)

label = customtkinter.CTkLabel(master=add_task_frame, text="Task Description", font=("Roboto", 10))
label.pack(padx=5)
enter_task_description = customtkinter.CTkEntry(master=add_task_frame)
enter_task_description.pack(pady=5, padx=5)

label = customtkinter.CTkLabel(master=add_task_frame, text="Task Due Date", font=("Roboto", 10))
label.pack(padx=5)
enter_task_duedate = customtkinter.CTkEntry(master=add_task_frame)
enter_task_duedate.pack(pady=5, padx=5)

message_label_add_task = customtkinter.CTkLabel(master=add_task_frame, text="", font=("Roboto", 12))
message_label_add_task.pack(pady=12, padx=10)

submit_task_button = customtkinter.CTkButton(master=add_task_frame, text="Submit Task", command=add_task)
submit_task_button.pack()

return_to_menu_button = customtkinter.CTkButton(master=add_task_frame, text="Return to Menu", 
                                                command=lambda: return_to_menu(add_task_frame))
return_to_menu_button.pack(pady=15, padx=10)


# View All Tasks Widgets.
view_all_tasks_frame = customtkinter.CTkFrame(master=root)

all_tasks_box = customtkinter.CTkTextbox(master=view_all_tasks_frame)
all_tasks_box.pack(fill="both", expand=True)

return_to_menu_button = customtkinter.CTkButton(master=view_all_tasks_frame, text="Return to Menu", 
                                                command=lambda: return_to_menu(view_all_tasks_frame))
return_to_menu_button.pack(pady=15, padx=10)


# View My Tasks Widgets.
view_my_tasks_frame = customtkinter.CTkFrame(master=root)

my_tasks_box = customtkinter.CTkTextbox(master=view_my_tasks_frame)
my_tasks_box.pack(fill="both", expand=True)

edit_task_choice = customtkinter.CTkEntry(master=view_my_tasks_frame, placeholder_text=" -Task num to edit- ")
edit_task_choice.pack(pady=5, padx=5)
# Bind the validate function to the edit task choice entry box.
edit_task_choice.bind("<KeyRelease>", lambda event: validate_task_number(current_user))

edit_task_button = customtkinter.CTkButton(master=view_my_tasks_frame, text="Edit Task", 
                                           command=show_edit_task_frame, state="disabled")
edit_task_button.pack(pady=5, padx=5)

mark_as_complete_button = customtkinter.CTkButton(master=view_my_tasks_frame, text="Mark As Complete", command=mark_as_complete)
mark_as_complete_button.pack(pady=5, padx=5)

message_label_mark_complete = customtkinter.CTkLabel(master=view_my_tasks_frame, text="", font=("Roboto", 12))
message_label_mark_complete.pack(pady=5, padx=5)

return_to_menu_button = customtkinter.CTkButton(master=view_my_tasks_frame, text="Return to Menu", 
                                                command=lambda: return_to_menu(view_my_tasks_frame))
return_to_menu_button.pack(pady=5, padx=5)


# Edit Tasks Widgets.
edit_task_frame = customtkinter.CTkFrame(master=root)

label_reg_user = customtkinter.CTkLabel(master=edit_task_frame, text="Edit a task", font=("Roboto", 24))
label_reg_user.pack(pady=12, padx=10)

label = customtkinter.CTkLabel(master=edit_task_frame, text="Assign task to another user", font=("Roboto", 10))
label.pack(padx=5)
assign_different_user = customtkinter.CTkEntry(master=edit_task_frame)
assign_different_user.pack(pady=5, padx=5)

label = customtkinter.CTkLabel(master=edit_task_frame, text="Change Task Due Date", font=("Roboto", 10))
label.pack(padx=5)
change_date = customtkinter.CTkEntry(master=edit_task_frame)
change_date.pack(pady=5, padx=5)

message_label_edit_task = customtkinter.CTkLabel(master=edit_task_frame, text="", font=("Roboto", 12))
message_label_edit_task.pack(pady=5, padx=5)

submit_changes_button = customtkinter.CTkButton(master=edit_task_frame, text="Submit Changes", command=edit_task)
submit_changes_button.pack()

return_to_menu_button = customtkinter.CTkButton(master=edit_task_frame, text="Return to Menu", 
                                                command=lambda: return_to_menu(edit_task_frame))
return_to_menu_button.pack(pady=50, padx=5)


# View Reports Widgets.
view_reports_frame = customtkinter.CTkFrame(master=root)

label = customtkinter.CTkLabel(master=view_reports_frame, text="Admin Reports", font=("Roboto", 24))
label.pack(pady=12, padx=10)

total_task_box = customtkinter.CTkTextbox(master=view_reports_frame)
total_task_box.pack(fill="both", expand=True)

return_to_menu_button = customtkinter.CTkButton(master=view_reports_frame, text="Return to Menu", 
                                                command=lambda: return_to_menu(view_reports_frame))
return_to_menu_button.pack(pady=15, padx=10)


# View Statistics Widgets.
view_statistics_frame = customtkinter.CTkFrame(master=root)

view_statistics_box = customtkinter.CTkTextbox(master=view_statistics_frame)
view_statistics_box.pack(fill="both", expand=True)

message_label_stat = customtkinter.CTkLabel(master=view_statistics_frame, text="", font=("Roboto", 12))
message_label_stat.pack(pady=5, padx=5)

return_to_menu_button = customtkinter.CTkButton(master=view_statistics_frame, text="Return to Menu", 
                                                command=lambda: return_to_menu(view_statistics_frame))
return_to_menu_button.pack(pady=15, padx=10)

root.mainloop()
