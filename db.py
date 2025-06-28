from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create DB and table if not exists
def init_db():
    with sqlite3.connect("todo.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL)")

@app.route("/", methods=["GET", "POST"])
def index():
    init_db()

    if request.method == "POST":
        task_content = request.form["content"]
        if task_content:
            with sqlite3.connect("todo.db") as conn:
                conn.execute("INSERT INTO tasks (content) VALUES (?)", (task_content,))
        return redirect(url_for("index"))

    with sqlite3.connect("todo.db") as conn:
        tasks = conn.execute("SELECT * FROM tasks").fetchall()

    return render_template("indexdb.html", tasks=tasks)

@app.route("/delete/<int:task_id>")
def delete(task_id):
    with sqlite3.connect("todo.db") as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
