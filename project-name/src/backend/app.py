from flask import Flask, request, redirect, url_for, render_template
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="db",
            user="omer",
            password="12345",
            database="db"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


@app.route('/employees')
def show_employees():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT employees.id, employees.first_name, employees.last_name, employees.hire_date, employees.salary, departments.department_name
    FROM employees
    JOIN departments ON employees.department_id = departments.id
    """

    cursor.execute(query)
    employees = cursor.fetchall()
    conn.close()

    # render_template kullanarak HTML şablonunu çağırıyoruz
    return render_template('employees.html', employees=employees)

@app.route('/departments')
def show_departments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM departments")
    departments = cursor.fetchall()
    conn.close()

    return render_template('departments.html', departments=departments)

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        hire_date = request.form['hire_date']
        salary = request.form['salary']
        department_id = request.form['department_id']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
            INSERT INTO employees (first_name, last_name, hire_date, salary, department_id)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (first_name, last_name, hire_date, salary, department_id))
            conn.commit()
            conn.close()
        except Exception as e:
            return f"Error: {str(e)}"

        return redirect(url_for('show_employees'))

    return render_template('add_employee.html')



@app.route('/add_department', methods=['GET', 'POST'])
def add_department():
    if request.method == 'POST':
        department_name = request.form['department_name']
        
        try:
            conn = get_db_connection()
            if conn is not None:
                cursor = conn.cursor()
                query = "INSERT INTO departments (department_name) VALUES (%s)"
                cursor.execute(query, (department_name,))
                conn.commit()
                conn.close()
        except Exception as e:
            return f"Error: {str(e)}"  # Hata mesajını kullanıcıya döner
        
        return redirect(url_for('show_departments'))  # Departmanları gösteren bir sayfaya yönlendirme

    return render_template('add_department.html')  # HTML dosyasını render et





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
