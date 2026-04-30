from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)


def get_db():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )


@app.route("/")
def hello():
    return f"Hello from {os.environ.get('HOSTNAME', 'unknown')}!"


@app.route("/health")
def health():
    try:
        conn = get_db()
        conn.close()
        return jsonify(status="ok", database="connected"), 200
    except Exception as e:
        return jsonify(status="degraded", error=str(e)), 503


@app.route("/db-version")
def db_version():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()[0]
    conn.close()
    return jsonify(version=version)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
