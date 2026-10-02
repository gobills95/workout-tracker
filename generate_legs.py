import sqlite3
import random
from datetime import date

def generate_legs():

    conn = sqlite3.connect("workouts.db")

    cursor = conn.cursor()

    today = date.today()

    cursor.execute("""
    SELECT name, muscle_group_area
    FROM exercises
    WHERE movement_type = 'Legs' AND muscle_group_area = 'quad'
    """)

    quads = cursor.fetchall()

    cursor.execute("""
    SELECT name, muscle_group_area
    FROM exercises
    WHERE movement_type = 'Legs' AND muscle_group_area = 'hamstring'
    """)

    hamstrings = cursor.fetchall()

    cursor.execute("""
    SELECT name, muscle_group_area
    FROM exercises
    WHERE movement_type = 'Legs' AND muscle_group_area = 'calves'
    """)

    calves = cursor.fetchall()

    quad_picks = random.sample(quads, 3)
    hamstring_picks = random.sample(hamstrings, 2)
    calve_picks = random.sample(calves, 1)


    legs_workout = (
        quad_picks + hamstring_picks + calve_picks
    )

    cursor.execute("""
    INSERT INTO workouts (workout_type, workout_date)
    VALUES (?, ?)
    """, ("Legs", str(today)))

    conn.commit()

    workout_id = cursor.lastrowid

    for exercise in legs_workout:
        cursor.execute("""
        INSERT INTO workout_exercises (workout_id, exercise_name)
        VALUES (?, ?) 
    """, (workout_id, exercise[0]))

    conn.commit()
    conn.close()

    return workout_id, legs_workout
