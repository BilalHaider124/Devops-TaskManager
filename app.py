from flask import Flask, request, redirect
import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/health")
def health():
    return "OK", 200

def get_connection():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

def init_db():
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT FALSE
            )
        """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute("SELECT id, name, completed FROM tasks ORDER BY id")
        tasks = cur.fetchall()

    conn.close()

    task_list = ""

    for task in tasks:
        task_id, task_name, completed = task
        status = "✅" if completed else "⬜"

        task_list += f"""
        <li>
            {status} {task_name}

            <form method="POST" action="/complete/{task_id}" style="display:inline;">
                <button type="submit">Complete</button>
            </form>

            <form method="POST" action="/delete/{task_id}" style="display:inline;">
                <button type="submit">Delete</button>
            </form>
        </li>
        """

    return f"""
    <h1>Task Manager</h1>

    <form method="POST" action="/add">
        <input type="text" name="task" placeholder="Enter a task" required>
        <button type="submit">Add Task</button>
    </form>

    <h2>Tasks</h2>

    <ul>
        {task_list}
    </ul>
    """


@app.route("/add", methods=["POST"])
def add_task():
    task = request.form["task"]

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO tasks (name) VALUES (%s)",
            (task,)
        )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/complete/<int:task_id>", methods=["POST"])
def complete_task(task_id):
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute(
            "UPDATE tasks SET completed = TRUE WHERE id = %s",
            (task_id,)
        )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM tasks WHERE id = %s",
            (task_id,)
        )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)