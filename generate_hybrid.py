import sqlite3
import random
from datetime import date

def generate_hybrid():

    conn = sqlite3.connect("workouts.db")

    cursor = conn.cursor()

    today = date.today()

    cursor.execute("""
    SELECT name, muscle_group_area
    FROM exercises
    WHERE movement_type = 'Push' AND muscle_group = 'Chest'
    """)

    chest = cursor.fetchall()

    cursor.execute("""
    SELECT name, muscle_group_area
    FROM exercises
    WHERE movement_type = 'Pull' AND muscle_group = 'Back'
    """)

    back = cursor.fetchall()

    cursor.execute("""
    SELECT name, muscle_group_area
    FROM exercises
    WHERE movement_type = 'Push' AND muscle_group = 'Shoulders'
    """)

    shoulders = cursor.fetchall()

    cursor.execute("""
    SELECT name, muscle_group_area
    FROM exercises
    WHERE movement_type = 'Pull' AND muscle_group = 'Biceps'
    """)

    biceps = cursor.fetchall()

    cursor.execute("""
    SELECT name, muscle_group_area
    FROM exercises
    WHERE movement_type = 'Push' AND muscle_group = 'Triceps'
    """)

    triceps = cursor.fetchall()

    chest_picks = random.sample(chest, 2)
    back_picks =random.sample(back, 2)
    shoulder_picks = random.sample(shoulders, 1)
    biceps_picks = random.sample(biceps, 1)
    triceps_picks = random.sample(triceps, 1)

    hybrid_workout = (
        chest_picks + back_picks + shoulder_picks + biceps_picks + triceps_picks
    )

    cursor.execute("""
    INSERT INTO workouts (workout_type, workout_date)
    VALUES (?, ?)
    """, ("Hybrid", str(today)))

    conn.commit()

    workout_id = cursor.lastrowid

    for exercise in hybrid_workout:
        cursor.execute("""
        INSERT INTO workout_exercises (workout_id, exercise_name)
        VALUES (?, ?) 
    """, (workout_id, exercise[0]))

    conn.commit()
    conn.close()

    return workout_id, hybrid_workout

