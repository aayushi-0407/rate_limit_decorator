from flask import Flask
from rate_limiter import rate_limit

app = Flask(__name__)


@app.route("/login")
@rate_limit(algorithm="sliding_window", limit=3, window_seconds=60)
def login():
    return "Login successful"


@app.route("/search")
@rate_limit(algorithm="token_bucket", capacity=1, refill_rate=100)
def search():
    return "Search results"


if __name__ == "__main__":
    app.run(debug=True)
