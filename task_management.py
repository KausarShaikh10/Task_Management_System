import sqlite3
import pwinput

# Connect to the database
conn = sqlite3.connect('C:\\Users\\user\\Desktop\\Python\\tasks.db')
cursor = conn.cursor()

# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
# Create the users table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL,
        date TEXT,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')
conn.commit()

# Function to register a new user
def register():
    username = input('Enter a username: ')
    password = pwinput.pwinput(prompt='Enter your password: ', mask='*')

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if user:
        print('Username already exists. Please choose a different username.')
    else:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        print('Registration successful!')

# Function to log in a user
def login():
    username = input('Enter your username: ')
    password = pwinput.pwinput(prompt='Enter your password: ', mask='*')

    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()

    if user:
        print('Login successful!')
        task_management(user[0])  # Pass the user ID to the task management function
    else:
        print('Invalid username or password.')

# Function to manage tasks for a logged-in user
def task_management(user_id):
    while True:
        print('-'*25)
        print('Task Management')
        print('1. Create Task')
        print('2. Update Task')
        print('3. Delete Task')
        print('4. View Tasks')
        print('5. Logout')

        choice = input('Enter your choice: ')

        if choice == '1':
            create_task(user_id)
        elif choice == '2':
            update_task(user_id)
        elif choice == '3':
            delete_task(user_id)
        elif choice == '4':
            view_tasks(user_id)
        elif choice == '5':
            print('Logged out successfully!')
            break
        else:
            print('Invalid choice. Please try again.')

# Function to create a new task
def create_task(user_id):
    title = input('Enter the task title: ')
    description = input('Enter the task description: ')
    status = input('Enter the task status: ')
    date = input('Assigned on: ')
    cursor.execute('INSERT INTO tasks (title, description, status, date, user_id) VALUES (?, ?, ?, ?, ?)', (title, description, status, date, user_id))
    conn.commit()
    print('Task created successfully!')

# Function to update an existing task
def update_task(user_id):
    task_id = input('Enter the task ID: ')
    print('What you want to update?: ')
    print('1. Title')
    print('2. Description')
    print('3. Status')
    choice = input('Enter your choice: ')
    if choice == '1':
        title = input('Enter the new task title: ')
        cursor.execute('UPDATE tasks SET title = ? WHERE id = ? AND user_id = ?', (title, task_id, user_id))
    elif choice == '2':
        description = input('Enter the new task description: ')
        cursor.execute('UPDATE tasks SET description = ? WHERE id = ? AND user_id = ?', (description, task_id, user_id))
    elif choice =='3':
        status = input('Enter the new task status: ')
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ? AND user_id = ?', (status, task_id, user_id))

    conn.commit()
    print('Task updated successfully!')

# Function to delete a task
def delete_task(user_id):
    task_id = input('Enter the task ID: ')

    cursor.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (task_id, user_id))
    conn.commit()
    print('Task deleted successfully!')

# Function to view all tasks
def view_tasks(user_id):
    cursor.execute('SELECT * FROM tasks WHERE user_id = ?', (user_id,))
    tasks = cursor.fetchall()
    if len(tasks)==0 :
        print('No tasks created! Add a new task please!')
        return
    else:
        for task in tasks:
            print(f'Task ID: {task[0]}')
            print(f'Date: {task[4]}')
            print(f'Title: {task[1]}')
            print(f'Description: {task[2]}')
            print(f'Status: {task[3]}')
            print('---')

# Group Member Information
print('Welcome to Task Management System')
print('N. K. Orchid College Of Engineering & Technology, Solapur')
print('Python Mini Project')
print('CSE SY A-4')
print('Group Members:')
print('Roll no\tName')
print('70\tKausar Shaikh')
print('71\tMahek Shahbad')
print('74\tShafin Zartar')
print('-'*25)
# Main loop
while True:
    print('-'*25)
    print('Task Management')
    print('1. Register')
    print('2. Login')
    print('3. Exit')

    choice = input('Enter your choice: ')

    if choice == '1':
        register()
    elif choice == '2':
        login()
    elif choice == '3':
        print('Exiting...')
        break
    else:
        print('Invalid choice. Please try again.')

# Close the connection
conn.close()
