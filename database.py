import sqlite3

DB_NAME = "Tasky.db"

def init_bd():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Activation des clés étrangères
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Table Utilisateurs
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # 2. Table Taches
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT,
            status INTEGER DEFAULT 0,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES utilisateurs (id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Base de données Tasky initialisée avec succès.")

def connect_db():
    # Retourne une connexion active.
    return sqlite3.connect(DB_NAME)

def user_signin(pseudo, password):
    # Crée un nouvel utilisateur.
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (pseudo, password) VALUES (?, ?)", (pseudo, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Retourne False si le pseudo existe déjà
        return False

def login_check(pseudo, password):
    # Vérifie le login/mdp et retourne l'ID utilisateur si c'est bon.
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE pseudo=? AND password=?", (pseudo, password))
    resultat = cursor.fetchone()
    conn.close()
    
    if resultat:
        return resultat[0]
    else:
        return None

def add_task(title, user_id):
    # Ajoute une tâche liée à l'utilisateur connecté.
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (title, user_id) VALUES (?, ?)", (title, user_id))
    conn.commit()
    conn.close()

def get_tasks(user_id):
    # Récupère toutes les tâches d'un utilisateur.
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, status FROM tasks WHERE user_id=?", (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task_title(task_id, new_title):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET title = ? WHERE id = ?", (new_title, task_id))
    conn.commit()
    conn.close()

def update_task_status(task_id, new_status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = ? WHERE id = ?", (new_status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()