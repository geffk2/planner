import sys
import os
from planner import app
from planner import db_model

print(sys.argv)
# if getattr(sys, 'frozen', False):
PATH = os.path.dirname(sys.argv[0])
# elif __file__:
#    PATH = os.path.dirname(__file__)

if __name__ == '__main__':
    db_model.connect()
    sys.exit(app.run())
