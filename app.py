import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from generate_push import generate_push
from generate_pull import generate_pull
from generate_legs import generate_legs
from generate_hybrid import generate_hybrid

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/push")
def push():
    workout_id, workout = generate_push()
    
    return redirect(
        url_for(
            "workout",
            workout_id=workout_id
        )
    )

@app.route("/pull")
def pull():
    workout_id, workout = generate_pull()
    
    return redirect(
        url_for(
            "workout",
            workout_id=workout_id
        )
    )

@app.route("/legs")
def legs():
    workout_id, workout = generate_legs()
    
    return redirect(
        url_for(
            "workout",
            workout_id=workout_id
        )
    )

@app.route("/hybrid")
def hybrid():

    workout_id, workout = generate_hybrid()

    return redirect(
        url_for(
            "workout",
            workout_id=workout_id
        )
    )

@app.route("/start/<int:workout_id>/<int:exercise_number>", methods=["GET", "POST"])
def start(workout_id, exercise_number):

    conn = sqlite3.connect("workouts.db")
    cursor = conn.cursor()

    # Get every exercise belonging to this workout
    cursor.execute("""
    SELECT *
    FROM workout_exercises
    WHERE workout_id = ?
    """, (workout_id,))

    exercises = cursor.fetchall()

    message = None

    if request.method == "POST":

        # Find out which button was clicked
        action = request.form["action"]

        if action == "save":

            current_exercise = exercises[exercise_number]

            weight = request.form["weight"]
            reps = request.form["reps"]

            cursor.execute("""
            SELECT COUNT(*)
            FROM exercise_sets
            WHERE workout_id = ?
            AND exercise_name = ?
            """, (
                workout_id,
                current_exercise[2]
            ))

            set_number = cursor.fetchone()[0] + 1

            cursor.execute("""
            INSERT INTO exercise_sets
            (workout_id, exercise_name, set_number, weight, reps)
            VALUES (?, ?, ?, ?, ?)
            """, (workout_id,current_exercise[2], set_number, weight, reps)
            )

            conn.commit()
            conn.close()    

            # Return to the same exercise using a fresh GET request
            return redirect(
                url_for("start",
                        workout_id=workout_id,
                        exercise_number=exercise_number
                )
            )

        elif action == "next":

            conn.close()

            # Move to the next exercise using a fresh GET request
            return redirect(
                url_for(
                    "start",
                    workout_id=workout_id,
                    exercise_number=exercise_number + 1
                )
            )

    # If there are no more exercises, finish the workout
    if exercise_number >= len(exercises):

        exercise_count = len(exercises)

        cursor.execute("""
        SELECT COUNT(*)
        FROM exercise_sets
        WHERE workout_id = ?
        """, (workout_id,)
        )

        set_count = cursor.fetchone()[0]

        conn.close()

        return render_template(
            "workout_complete.html",
            workout_id=workout_id,
            exercise_count=exercise_count,
            set_count=set_count
        )


    # Select the exercise that should currently appear
    current_exercise = exercises[exercise_number]

    # Retrieve logged sets for the current exercise
    cursor.execute("""
    SELECT *
    FROM exercise_sets
    WHERE workout_id = ?
    AND exercise_name = ?
    """, (workout_id, current_exercise[2]))

    sets = cursor.fetchall()

    conn.close()

    return render_template(
        "start.html",
        workout_id=workout_id,
        current_exercise=current_exercise,
        exercise_number=exercise_number,
        sets=sets
    )

@app.route("/history")
def history():

    conn = sqlite3.connect("workouts.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM workouts
    ORDER BY workout_id DESC
    """)

    history = cursor.fetchall()

    return render_template(
        "history.html",
        history=history
    )

@app.route("/history/<int:workout_id>")
def workout_details(workout_id):

    conn = sqlite3.connect("workouts.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM workout_exercises
    WHERE workout_id = ?
    """, (workout_id,))

    exercises = cursor.fetchall()

    cursor.execute("""
    SELECT *
    FROM exercise_sets
    WHERE workout_id = ?
    ORDER BY exercise_name, set_number
    """, (workout_id,))

    sets = cursor.fetchall()

    conn.close()

    return render_template(
        "workout_details.html",
        workout_id=workout_id,
        exercises=exercises,
        sets=sets
    )

@app.route("/delete_workout/<int:workout_id>")
def delete_workout(workout_id):

    conn = sqlite3.connect("workouts.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM exercise_sets
    WHERE workout_id = ?
    """, (workout_id,))

    cursor.execute("""
    DELETE FROM workout_exercises
    WHERE workout_id = ?
    """, (workout_id,))

    cursor.execute("""
    DELETE FROM workouts
    WHERE workout_id = ?
    """, (workout_id,))

    conn.commit()
    conn.close()

    return redirect(url_for("history"))

@app.route("/workout/<int:workout_id>")
def workout(workout_id):

    conn = sqlite3.connect("workouts.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM workout_exercises
    WHERE workout_id = ?
    """, (workout_id,))

    workout = cursor.fetchall()

    conn.close()

    return render_template(
        "workout.html",
        workout=workout,
        workout_id=workout_id
    )

if __name__ == "__main__":
    app.run(debug=True)