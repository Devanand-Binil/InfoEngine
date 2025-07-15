from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/")
def serve_search():
    return send_from_directory(".", "cse.html")  # assumes cse.html is in same folder

if __name__ == "__main__":
    app.run(port=8765)
