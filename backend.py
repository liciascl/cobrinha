from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3

app = Flask(__name__, template_folder="templates")
CORS(app)

# Inicializa o banco de dados SQLite
def init_db():
    with sqlite3.connect("snake_game.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        """)
        conn.commit()

init_db()  # Chama a função ao iniciar a API

# Rota para exibir a interface do jogo
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

# Rota para obter as pontuações ordenadas do maior para o menor
@app.route("/scores", methods=["GET"])
def get_scores():
    with sqlite3.connect("snake_game.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT player, score FROM scores ORDER BY score DESC LIMIT 10")
        scores = cursor.fetchall()
    return jsonify([{"player": row[0], "score": row[1]} for row in scores])  # Formata os dados corretamente

# Rota para salvar uma nova pontuação
@app.route("/scores", methods=["POST"])
def add_score():
    data = request.json
    if "player" not in data or "score" not in data:
        return jsonify({"error": "Campos 'player' e 'score' são obrigatórios"}), 400
    
    with sqlite3.connect("snake_game.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO scores (player, score) VALUES (?, ?)", (data["player"], data["score"]))
        conn.commit()
    return jsonify({"message": "Score saved!"}), 201

if __name__ == "__main__":
    app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
