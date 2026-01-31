from flask import Flask, jsonify, request
import sqlite3;

app = Flask(__name__)

DB_NAME = "budget_manager.db"

def inti_db():
    conn = sqlite3.connect(DB_NAME) #opens connection to database
    cursor = conn.cursor() #creates a curser/tool that let us send commands 

    #Users Table
    cursor.execute("""
     CREATE TABLE IF NOT EXISTS users (
        id INTERGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
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

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?,?)",(user, email ))
    conn.commit()
    conn.close()

    return jsonify({"message":"user registered successfully!"}),201


if __name__ == "__main__":
    inti_db()
    app.run(debug=True)