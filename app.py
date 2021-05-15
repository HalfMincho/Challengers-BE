from flask import Flask
import endpoints

app = Flask(__name__)

app.register_blueprint(endpoints.challenge_blueprint, url_prefix='/challenge')

if __name__ == "__main__":
    app.run()
