import sys
import os
from planner import app
from planner import db_model


PATH = os.path.dirname(__file__)

if __name__ == '__main__':
    db_model.connect()
    sys.exit(app.run())
