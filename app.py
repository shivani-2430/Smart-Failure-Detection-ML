from flask import Flask
from flask_migrate import Migrate
from config import Config
from database.db import db
from routes.routes import register_routes
from models.project import Project

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

register_routes(app)

# Create tables on startup
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)