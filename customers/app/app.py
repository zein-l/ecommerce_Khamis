from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to the Ecommerce API"

# Ensure this is only executed when running the app directly
if __name__ == "__main__":
    app.run(debug=True)
