from sqlite3 import connect

connection = connect("./files/database.db", check_same_thread=False)
cursor = connection.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()
    return inner

@with_commit
def build():
    scriptexec("./files/script.sql")


def commit():
    connection.commit()


def close():
    connection.close()


def field(command, *values):
    cursor.execute(command, tuple(values))
    if (fetch := cursor.fetchone()) is not None:
        return fetch[0]


def record(command, *values):
    cursor.execute(command, tuple(values))
    return cursor.fetchone()


def records(commands, *values):
    cursor.execute(commands, tuple(values))
    return cursor.fetchall()


def column(command, *values):
    cursor.execute(command, tuple(values))
    return [item[0] for item in cursor.fetchall()]


def execute(command, *values):
    cursor.execute(command, tuple(values))


def multiexec(command, valueset):
    cursor.execute(command, valueset)


def scriptexec(filename):
    with open (filename, "r") as script:
        cursor.executescript(script.read())
