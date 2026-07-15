import sqlite3

# Function to connect database
def get_connection():
    conn = sqlite3.connect("health.db")
    return conn


# Function to create table
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        dob TEXT,
        email TEXT,
        glucose REAL,
        haemoglobin REAL,
        cholesterol REAL,
        remarks TEXT
    )
    """)

    conn.commit()
    conn.close()


# Function to insert patient
def add_patient(full_name, dob, email, glucose, haemoglobin, cholesterol, remarks):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO patients(
        full_name,
        dob,
        email,
        glucose,
        haemoglobin,
        cholesterol,
        remarks
    )
    VALUES(?,?,?,?,?,?,?)
    """, (
        full_name,
        dob,
        email,
        glucose,
        haemoglobin,
        cholesterol,
        remarks
    ))

    conn.commit()
    conn.close()

def get_all_patients():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")

    patients = cursor.fetchall()

    conn.close()

    return patients


def delete_patient(patient_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (patient_id,)
    )

    conn.commit()
    conn.close()


# -------------------------------
# Update Patient Email
# -------------------------------
def update_patient_email(patient_id, new_email):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE patients
        SET email = ?
        WHERE id = ?
        """,
        (new_email, patient_id)
    )

    conn.commit()
    conn.close()
# -------------------------------
# Check Duplicate Patient
# -------------------------------
def patient_exists(full_name, dob, email, glucose, haemoglobin, cholesterol):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM patients
        WHERE full_name = ?
        AND dob = ?
        AND email = ?
        AND glucose = ?
        AND haemoglobin = ?
        AND cholesterol = ?
    """, (
        full_name,
        dob,
        email,
        glucose,
        haemoglobin,
        cholesterol
    ))

    patient = cursor.fetchone()

    conn.close()

    return patient is not None