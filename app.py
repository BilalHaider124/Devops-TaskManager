from flask import Flask, request, redirect

app = Flask(__name__)

tasks = []


@app.route("/")
def home():
    task_list = ""

    for index, task in enumerate(tasks):
        status = "✅" if task["completed"] else "⬜"

        task_list += f"""
        <li>
            {status} {task["name"]}

            <form method="POST" action="/complete/{index}" style="display:inline;">
                <button type="submit">Complete</button>
            </form>

            <form method="POST" action="/delete/{index}" style="display:inline;">
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

    tasks.append({
        "name": task,
        "completed": False
    })

    return redirect("/")


@app.route("/complete/<int:index>", methods=["POST"])
def complete_task(index):
    tasks[index]["completed"] = True

    return redirect("/")


@app.route("/delete/<int:index>", methods=["POST"])
def delete_task(index):
    tasks.pop(index)

    return redirect("/")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)