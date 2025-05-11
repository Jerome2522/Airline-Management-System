-- Create Flights Table
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_number TEXT NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    arrival_time TEXT NOT NULL,
    seats_available INTEGER NOT NULL
);

-- Create Reservations Table
CREATE TABLE IF NOT EXISTS reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    phone TEXT NOT NULL,
    reservation_date TEXT NOT NULL,
    seat_number TEXT NOT NULL,
    flight_id INTEGER,
    FOREIGN KEY (flight_id) REFERENCES flights(id)
);

-- Create Seats Table (with flight_id and is_booked)
CREATE TABLE IF NOT EXISTS seats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_id INTEGER,
    seat_number TEXT NOT NULL,
    is_booked INTEGER DEFAULT 0,
    FOREIGN KEY (flight_id) REFERENCES flights(id)
);

-- Insert Flight Data
INSERT INTO flights (flight_number, origin, destination, departure_time, arrival_time, seats_available)
VALUES
  ('AA101', 'New York', 'Los Angeles', '2025-06-01 08:00', '2025-06-01 11:00', 150),
  ('BA202', 'London', 'New York', '2025-06-02 09:30', '2025-06-02 13:45', 200),
  ('CA303', 'Toronto', 'Vancouver', '2025-06-03 12:15', '2025-06-03 14:45', 180),
  ('DA404', 'Paris', 'Dubai', '2025-06-04 20:00', '2025-06-05 04:00', 220),
  ('EA505', 'Tokyo', 'San Francisco', '2025-06-05 22:00', '2025-06-05 15:00', 160);

-- Insert Seat Data
INSERT INTO seats (flight_id, seat_number, is_booked) VALUES
  (1, '1A', 0), (1, '1B', 0), (1, '1C', 0), (1, '1D', 0), (1, '1E', 0),
  (2, '2A', 0), (2, '2B', 0), (2, '2C', 0), (2, '2D', 0), (2, '2E', 0), (2, '2F', 0),
  (3, '3A', 0), (3, '3B', 0), (3, '3C', 0), (3, '3D', 0), (3, '3E', 0), (3, '3F', 0), (3, '3G', 0),
  (4, '4A', 0), (4, '4B', 0), (4, '4C', 0), (4, '4D', 0), (4, '4E', 0), (4, '4F', 0), (4, '4G', 0), (4, '4H', 0),
  (5, '5A', 0), (5, '5B', 0), (5, '5C', 0), (5, '5D', 0), (5, '5E', 0), (5, '5F', 0), (5, '5G', 0), (5, '5H', 0), (5, '5I', 0);
