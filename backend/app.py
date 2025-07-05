from peewee import *
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

db = SqliteDatabase("todos.db")


class Todo(Model):
    todo_id = AutoField()
    message = CharField()
    is_completed = BooleanField(default=False)

    class Meta:
        database = db


db.connect()
db.create_tables([Todo])



@app.route("/health")
def hello_world():
    return {
        "status": "up"
    }


@app.route("/todos", methods=['POST', 'GET'])
def get_all_todos():
    if request.method == 'POST':
        message = request.json["todo"]
        Todo(message=message).save()
        return {
            "message": "Todo Added"
        }

    if request.method == 'GET':
        query = Todo.select()
        incomplete_todos = []
        completed_todos = []

        for todo in query:
            if todo.is_completed:
                todo_to_be_added = {
                    "id": todo.todo_id,
                    "message": todo.message
                }
                completed_todos.append(todo_to_be_added)
            else:
                todo_to_be_added = {
                    "id": todo.todo_id,
                    "message": todo.message
                }
                incomplete_todos.append(todo_to_be_added)

        return {
            "incompleted_todos": incomplete_todos,
            "completed_todos": completed_todos
        }


@app.route("/todos/complete", methods=['POST'])
def todo_completed():
    id = request.json["id"]
    todo = Todo.get_by_id(id)
    todo.is_completed = True
    todo.save()
    return {
        "message": "Todo Completed"
    }


@app.route("/todos/delete", methods=['POST'])
def todo_delete():
    try:
        id = request.json["id"]
        todo = Todo.get_by_id(id)
        todo.delete_instance()
        return {"message": "Todo Deleted"}
    except Todo.DoesNotExist:
        return {"error": "Todo not found"}, 404


@app.route("/todos/delete_all", methods=["POST"])
def delete_all_todos():
    Todo.delete().execute()
    return {"message": "All todos deleted"}



if __name__ == "__main__":
    app.run(debug=True)
