from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os

app = Flask(__name__)                                           #Flask app initialization
app.secret_key = 'your_secret_key'
db_path = os.path.abspath("airline_res.db")

def init_db():                                                  #Database initialization
    with sqlite3.connect(db_path) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                phone TEXT,
                reservation_date TEXT
            )
        ''')
init_db()

def query_db(query, args=(), one=False):
    with sqlite3.connect(db_path) as conn:
        cur = conn.execute(query, args)
        rv = cur.fetchall()
        conn.commit()
        return (rv[0] if rv else None) if one else rv

@app.route('/')                                             #Main page api                                      
def index():
    reservations = query_db("SELECT * FROM reservations")
    return render_template('index.html', reservations=reservations)

@app.route('/add', methods=['POST'])                                   #Add reservation api              
def add_reservation():
    data = request.form
    if not data['age'].isdigit() or not data['phone'].isdigit():
        flash("Age and Phone must be numeric.", "danger")
    else:
        query_db("INSERT INTO reservations (name, age, phone, reservation_date) VALUES (?, ?, ?, ?)",
                 (data['name'], data['age'], data['phone'], data['date']))
        flash("Reservation added.", "success")
    return redirect(url_for('index'))

@app.route('/delete/<int:res_id>')                                #Delete reservation api           
def delete_reservation(res_id):
    query_db("DELETE FROM reservations WHERE id = ?", (res_id,))
    flash("Reservation deleted.", "info")
    return redirect(url_for('index'))

@app.route('/edit', methods=['POST'])                                 #Edit reservation api
def edit_reservation():
    data = request.form
    query_db('''
        UPDATE reservations SET name=?, age=?, phone=?, reservation_date=? WHERE id=?
    ''', (data['name'], data['age'], data['phone'], data['date'], data['res_id']))
    flash("Reservation updated.", "primary")
    return redirect(url_for('index'))

@app.route('/get_reservation/<int:res_id>')                           #Get reservation api
def get_reservation(res_id):
    res = query_db("SELECT * FROM reservations WHERE id = ?", (res_id,), one=True)
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True)
