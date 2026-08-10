from database.db import db


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)

    project_name = db.Column(db.String(200), nullable=False)

    organization = db.Column(db.String(200), nullable=False)

    domain = db.Column(db.String(100), nullable=False)

    tech_stack = db.Column(db.String(200), nullable=False)

    team_size = db.Column(db.Integer)

    budget = db.Column(db.Numeric(15, 2))

    timeline = db.Column(db.Integer)

    description = db.Column(db.Text, nullable=False)