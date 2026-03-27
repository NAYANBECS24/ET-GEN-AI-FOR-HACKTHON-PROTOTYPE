from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/admin")
def admin_panel():
    return jsonify({"message": "Welcome admin", "build": "v2026.03-enterprise"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
