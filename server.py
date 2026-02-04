from flask import Flask, jsonify, request
import sqlite3;

app = Flask(__name__)

DB_NAME = "budget_manager.db"

def init_db():
    conn = sqlite3.connect(DB_NAME) #opens connection to database
    cursor = conn.cursor() #creates a curser/tool that let us send commands 

    #Users Table
    cursor.execute("""
     CREATE TABLE IF NOT EXISTS users (
        id INTERGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        password TEXT NOT NULL DEFAULT ''
    )
    """)

    #expense table 
    cursor.execute("""
     CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)
       
    conn.commit() #save changes to the db
    conn.close() #Close the connection to the db

@app.get("/api/health")
def health_check():
    return jsonify({"status":"OK"}),200

@app.post("/api/register")
def register():
    data = request.get_json()
    print(data)
    user = data.get("name")
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (?,?,?)",(user, email, password ))
    conn.commit()
    conn.close()


    return jsonify({"message":"user registered successfully!"}),201

@app.get("/api/users")
def get_users():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users")
    rows = cursor.fetchall()
    print(rows)
    conn.close()

    users =[]
    for row in rows:
        user = {"id":row["id"], "name":row["name"]}
        users.append(user)

    return jsonify({"success":True,
            "message":"Users retrieved succesfully",
            "data":users}),200

@app.get("/api/users/<int:user_id>")
def user_id():
    conn =sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({
            "success":False,
            "message":"not found"
        }), 404
    
    print(row["name"])
    conn.close()


    return jsonify({"success":True,
                "message":"succesfully",
                "data": {"id":row["id"], "name":row["name"]}
    }),200

@app.delete("/api/users/<int:user_id>")
def delete_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM users WHERE id=?", (user_id,))

    if not cursor.fetchone():
        conn.close()

        return jsonify({
            "success":False,
            "message":"Not found"
        }), 404
    
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({
        "succes":True,
        "message":"success"
    }),200


@app.put("/api/users/<int:user_id>")
def update_user():
    data = request.json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    conn =sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name=?, email=? password=? WHERE id=?", (name, email, password, user_id))
    conn.commit()
    conn.close()

    return jsonify({
        "success":True,
        "message":"updated succeesful" 
    }), 200


#-----------EXPENSES------------
@app.get("/api/expense")
def get_expenses():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        ) 
    """)

    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Successful",
        "data": [dict(row) for row in rows]
    }), 200


@app.post("/api/expenses")
def add_expense():
    data = request.get_json()
    
    title = data.get("title")
    description = data.get("description")
    amount = data.get("amount")
    date = data.get("date")
    category = data.get("category")
    user_id = data.get("user_id")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (title, description, amount, date, category, user_id) VALUES (?,?,?,?,?,?)", (title, description, amount, date, category, user_id))
    conn.commit()
    conn.close()

    return jsonify({
            "success": True,
            "message": "Expense added successfully!"
        }), 201 


if __name__ == "__main__":
    init_db()
    app.run(debug=True)

