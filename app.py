
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__, template_folder="src/presentation/templates",
                          static_folder="src/presentation/static")
    app.config.from_object(Config)

    from src.presentation.routes import bp
    app.register_blueprint(bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
