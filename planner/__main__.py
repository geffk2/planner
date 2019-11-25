import sys
from planner import app
from planner import db_model

if __name__ == '__main__':
    db_model.connect()
    sys.exit(app.run())
