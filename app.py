from flask import Flask
from config import Config
from database.db import db
from routes.routes import register_routes
from models.project import Project

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

register_routes(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)