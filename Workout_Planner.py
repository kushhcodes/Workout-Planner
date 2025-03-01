from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("workout.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sets INTEGER NOT NULL,
            reps INTEGER NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)  
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect("workout.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exercises")
    exercises = cursor.fetchall()
    conn.close()
    return render_template("index.html", exercises=exercises)

@app.route('/add', methods=['POST'])
def add_exercise():
    name = request.form['name']
    sets = request.form['sets']
    reps = request.form['reps']
    conn = sqlite3.connect("workout.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO exercises (name, sets, reps) VALUES (?, ?, ?)", (name, sets, reps))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/complete/<int:exercise_id>')
def complete_exercise(exercise_id):
    conn = sqlite3.connect("workout.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE exercises SET completed = 1 WHERE id = ?", (exercise_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:exercise_id>')
def delete_exercise(exercise_id):
    conn = sqlite3.connect("workout.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exercises WHERE id = ?", (exercise_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
