from app import app
from db import db

db.init_app(app)

# create table when starting app (only when it doesnt exist), no more
# manual execution of create_tables.py
@app.before_first_request
def create_tables():
    db.create_all()
