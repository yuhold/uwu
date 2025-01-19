from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/status")
def get_status():
    try:
        with open("../status.json", "r") as f:
            data = json.load(f)
        print("Data from status.json:", data) # 添加 print 语句
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Status file not found."})
    except json.JSONDecodeError:
        return jsonify({"error": "Status file is invalid."})


if __name__ == "__main__":
    app.run(debug=True)
