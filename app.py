from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'


def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'airline.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row):
    return dict(row)


@app.route('/')
def index():
    conn = get_db_connection()

    reservations = conn.execute('''
        SELECT r.id, r.name, r.age, r.phone, r.reservation_date, r.seat_number,
               f.flight_number, f.origin, f.destination
        FROM reservations r
        JOIN flights f ON r.flight_id = f.id
    ''').fetchall()

    flights = conn.execute('SELECT * FROM flights').fetchall()

    seats_raw = conn.execute('''
        SELECT s.seat_number, s.flight_id
        FROM seats s
        WHERE NOT EXISTS (
            SELECT 1 FROM reservations r
            WHERE r.seat_number = s.seat_number AND r.flight_id = s.flight_id
        )
    ''').fetchall()

    seats = [dict(row) for row in seats_raw]

    conn.close()
    return render_template('index.html', reservations=reservations, flights=flights, seats=seats)



@app.route('/add', methods=['POST'])
def add_reservation():
    name = request.form['name']
    age = request.form['age']
    phone = request.form['phone']
    date = request.form['date']
    seat = request.form['seat']
    flight_id = request.form['flight_id']

    if not all([name, age, phone, date, seat, flight_id]):
        flash('Please fill all fields', 'danger')
        return redirect(url_for('index'))

    conn = get_db_connection()
    existing = conn.execute(
        'SELECT 1 FROM reservations WHERE flight_id = ? AND seat_number = ?',
        (flight_id, seat)
    ).fetchone()

    if existing:
        flash(f'Seat {seat} already booked for this flight.', 'danger')
        conn.close()
        return redirect(url_for('index'))

    conn.execute(
        'INSERT INTO reservations (name, age, phone, reservation_date, seat_number, flight_id) VALUES (?, ?, ?, ?, ?, ?)',
        (name, age, phone, date, seat, flight_id)
    )
    conn.commit()
    conn.close()
    flash('Reservation added!', 'success')
    return redirect(url_for('index'))


@app.route('/delete/<int:res_id>')
def delete_reservation(res_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM reservations WHERE id = ?', (res_id,))
    conn.commit()
    conn.close()
    flash('Reservation deleted.', 'warning')
    return redirect(url_for('index'))


@app.route('/get_reservation/<int:res_id>')
def get_reservation(res_id):
    conn = get_db_connection()
    res = conn.execute('SELECT * FROM reservations WHERE id = ?', (res_id,)).fetchone()
    conn.close()

    if res is None:
        return jsonify({'error': 'Reservation not found'}), 404

    return jsonify(row_to_dict(res))


@app.route('/edit', methods=['POST'])
def edit_reservation():
    res_id = request.form['res_id']
    name = request.form['name']
    age = request.form['age']
    phone = request.form['phone']
    date = request.form['date']
    seat = request.form['seat']
    flight_id = request.form['flight_id']

    conn = get_db_connection()

    existing = conn.execute(
        'SELECT 1 FROM reservations WHERE flight_id = ? AND seat_number = ? AND id != ?',
        (flight_id, seat, res_id)
    ).fetchone()

    if existing:
        flash(f'Seat {seat} is already taken.', 'danger')
        conn.close()
        return redirect(url_for('index'))

    conn.execute('''
        UPDATE reservations
        SET name = ?, age = ?, phone = ?, reservation_date = ?, seat_number = ?, flight_id = ?
        WHERE id = ?
    ''', (name, age, phone, date, seat, flight_id, res_id))
    conn.commit()
    conn.close()
    flash('Reservation updated.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
