from flask import request, jsonify
from flask_api import FlaskAPI
from flask_cors import CORS

app = FlaskAPI(__name__)
CORS(app)

@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        print(request.json)
        return jsonify("Sent")

if __name__ == "__main__":
    app.run(debug=True)