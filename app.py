from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Planeringsapp</h1><p>Version 1.0.0.</p>"

@app.route("/about")
def about():
    return "<p>Jesper Swärd</p>"

if __name__ == "__main__":
    app.run(debug=True)