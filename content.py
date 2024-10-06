from fasthtml.common import *

list_class = "m-body text-black list-disc pl-5"
db = database("data/todos.db")


class Todo:
    "Use any database system you like"
    id: int
    title: str
    done: bool

    def __ft__(self):
        "`__ft__` defines how FastHTML renders an object"
        return Li("✅ " if self.done else "", self.title)


todos = db.create(Todo)


def todos_table():
    "This example uses the `fastlite` DB lib"
    return Ul(*todos(), cls=list_class)


def startup():
    if not todos():
        todos.insert(title="Create sample todos", done=True)
        todos.insert(title="Create a sample FastHTML app", done=True)
        todos.insert(title="Read this todo list")


aboutme = [
    (
        "Some interesting question about you?",
        "I found a lion in my closet the other day! When I asked what it was doing there, it said “Narnia business.",
    ),
    (
        "Some interesting question about you?",
        "I found a lion in my closet the other day! When I asked what it was doing there, it said “Narnia business.”",
    ),
    (
        "Some interesting question about you?",
        "I found a lion in my closet the other day! When I asked what it was doing there, it said “Narnia business.”",
    ),
    (
        "Some interesting question about you?",
        "I found a lion in my closet the other day! When I asked what it was doing there, it said “Narnia business.”",
    ),
]
