"""Stage `views`: (re)create the analysis views from db/views.sql."""
import os

from common import DB_DIR


def build(con):
    con.execute(open(os.path.join(DB_DIR, "views.sql")).read())
