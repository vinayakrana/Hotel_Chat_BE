"""
SQLite Database Setup and Helper Functions
Manages rooms and bookings data
"""
import sqlite3
from typing import List, Dict, Optional
from datetime import datetime, date
import os

DB_PATH = "hotel.db"


def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn


def init_database():
    """Initialize database with tables and sample data"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create rooms table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT UNIQUE NOT NULL,
            room_type TEXT NOT NULL,
            price_per_night REAL NOT NULL,
            room_status TEXT DEFAULT 'available'
        )
    """)
    
    # Create bookings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            room_number TEXT NOT NULL,
            guest_email TEXT NOT NULL,
            check_in_date TEXT NOT NULL,
            check_out_date TEXT NOT NULL,
            status TEXT DEFAULT 'confirmed',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
    """)
    
    # Check if rooms already exist
    cursor.execute("SELECT COUNT(*) FROM rooms")
    if cursor.fetchone()[0] == 0:
        # Add sample rooms
        sample_rooms = [
            ("101", "Single", 80.0, "available"),
            ("102", "Single", 80.0, "available"),
            ("201", "Double", 120.0, "available"),
            ("202", "Double", 120.0, "available"),
            ("301", "Suite", 200.0, "available"),
            ("302", "Suite", 200.0, "cleaning"),
            ("401", "Deluxe", 280.0, "available"),
            ("402", "Deluxe", 280.0, "occupied"),
            ("501", "Presidential", 500.0, "available"),
            ("502", "Presidential", 500.0, "available"),
        ]
        
        cursor.executemany(
            "INSERT INTO rooms (room_number, room_type, price_per_night, room_status) VALUES (?, ?, ?, ?)",
            sample_rooms
        )
    
    conn.commit()
    conn.close()


def get_available_rooms() -> List[Dict]:
    """Get all available rooms"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, room_number, room_type, price_per_night, room_status
        FROM rooms
        WHERE room_status = 'available'
        ORDER BY price_per_night
    """)
    
    rooms = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rooms


def get_room_by_number(room_number: str) -> Optional[Dict]:
    """Get room details by room number"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, room_number, room_type, price_per_night, room_status
        FROM rooms
        WHERE room_number = ?
    """, (room_number,))
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None


def is_room_available(room_number: str, check_in: str, check_out: str) -> bool:
    """Check if room is available for given dates"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # First check if room exists and is available
    cursor.execute("""
        SELECT room_status FROM rooms WHERE room_number = ?
    """, (room_number,))
    
    room = cursor.fetchone()
    if not room or room['room_status'] != 'available':
        conn.close()
        return False
    
    # Check for overlapping bookings
    cursor.execute("""
        SELECT COUNT(*) as count
        FROM bookings
        WHERE room_number = ?
        AND status = 'confirmed'
        AND (
            (check_in_date <= ? AND check_out_date > ?)
            OR (check_in_date < ? AND check_out_date >= ?)
            OR (check_in_date >= ? AND check_out_date <= ?)
        )
    """, (room_number, check_in, check_in, check_out, check_out, check_in, check_out))
    
    result = cursor.fetchone()
    conn.close()
    
    return result['count'] == 0


def create_booking(room_number: str, guest_email: str, check_in: str, check_out: str) -> int:
    """Create a new booking"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get room ID
    cursor.execute("SELECT id FROM rooms WHERE room_number = ?", (room_number,))
    room = cursor.fetchone()
    
    if not room:
        conn.close()
        raise ValueError(f"Room {room_number} not found")
    
    # Create booking
    cursor.execute("""
        INSERT INTO bookings (room_id, room_number, guest_email, check_in_date, check_out_date, status)
        VALUES (?, ?, ?, ?, ?, 'confirmed')
    """, (room['id'], room_number, guest_email, check_in, check_out))
    
    booking_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return booking_id


def get_booking(booking_id: int) -> Optional[Dict]:
    """Get booking by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, room_id, room_number, guest_email, check_in_date, check_out_date, status, created_at
        FROM bookings
        WHERE id = ?
    """, (booking_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None


def cancel_booking_in_db(booking_id: int) -> bool:
    """Cancel a booking"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE bookings
        SET status = 'cancelled'
        WHERE id = ? AND status = 'confirmed'
    """, (booking_id,))
    
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return affected > 0


def get_bookings_by_email(email: str) -> List[Dict]:
    """Get all bookings for a guest"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, room_number, guest_email, check_in_date, check_out_date, status, created_at
        FROM bookings
        WHERE guest_email = ?
        ORDER BY created_at DESC
    """, (email,))
    
    bookings = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return bookings


def get_all_bookings_from_db(date_filter: Optional[str] = None) -> List[Dict]:
    """Get all bookings (staff only)"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if date_filter:
        cursor.execute("""
            SELECT id, room_number, guest_email, check_in_date, check_out_date, status, created_at
            FROM bookings
            WHERE check_in_date = ? OR check_out_date = ?
            ORDER BY check_in_date
        """, (date_filter, date_filter))
    else:
        cursor.execute("""
            SELECT id, room_number, guest_email, check_in_date, check_out_date, status, created_at
            FROM bookings
            WHERE status = 'confirmed'
            ORDER BY check_in_date
        """)
    
    bookings = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return bookings


def get_checkins_by_date(date_str: str) -> List[Dict]:
    """Get all check-ins for a specific date"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, room_number, guest_email, check_in_date, check_out_date, status
        FROM bookings
        WHERE check_in_date = ? AND status = 'confirmed'
        ORDER BY room_number
    """, (date_str,))
    
    checkins = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return checkins


def get_room_availability_counts() -> Dict[str, int]:
    """Get count of available rooms by type"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT room_type, COUNT(*) as count
        FROM rooms
        WHERE room_status = 'available'
        GROUP BY room_type
    """)
    
    counts = {row['room_type']: row['count'] for row in cursor.fetchall()}
    conn.close()
    return counts


def update_room_status_in_db(room_number: str, status: str) -> bool:
    """Update room status"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE rooms
        SET room_status = ?
        WHERE room_number = ?
    """, (status, room_number))
    
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return affected > 0


# Initialize database on import
if not os.path.exists(DB_PATH):
    init_database()
