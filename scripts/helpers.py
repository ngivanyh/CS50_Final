from sqlite3 import *
from datetime import datetime

db = connect("./dict.db", isolation_level=None)
cur = db.cursor()

def specified_color(is_syn, check_arg, default_colors, index, session):
    span_start = '<span style="color: '; span_end = ';">'

    def checks():
        if check_arg:
            de_color = default_colors[index]
            return span_start + de_color + span_end
        else:
            se_color = session["color" + str(str(index + 1))]
            return span_start + se_color + span_end

    if not is_syn:
        return checks()
    else:
        return checks()        

def wotd(): # Word of the Day
    has_wotd = cur.execute("SELECT * FROM word_of_the_day WHERE date=?", [datetime.now().strftime("%Y-%m-%d")]).fetchall() == []
    print(has_wotd)