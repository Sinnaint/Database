from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Створення бази даних та таблиці
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        specialty TEXT NOT NULL,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        middle_name TEXT NOT NULL,
        experience INTEGER NOT NULL
    )
''')
conn.commit()
conn.close()

# Додаткова функція для взаємодії з базою даних
def execute_query(query, values=()):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute(query, values)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

# Головна сторінка
@app.route('/')
def index():
    employees = execute_query('SELECT * FROM employees')
    return render_template('index.html', employees=employees)

# Додавання нового медпрацівника
@app.route('/add_employee', methods=['POST'])
def add_employee():
    specialty = request.form['specialty']
    last_name = request.form['last_name']
    first_name = request.form['first_name']
    middle_name = request.form['middle_name']
    experience = request.form['experience']

    query = '''
        INSERT INTO employees (specialty, last_name, first_name, middle_name, experience)
        VALUES (?, ?, ?, ?, ?)
    '''
    values = (specialty, last_name, first_name, middle_name, experience)
    execute_query(query, values)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
