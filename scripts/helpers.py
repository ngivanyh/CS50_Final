from sqlite3 import *
from datetime import datetime
from scripts.search import wotd_question
from app import session

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

def wotd_gen(): # Word of the Day
    db = connect("./dict.db")
    cur = db.cursor()

    cur_day = datetime.now().strftime("%Y-%m-%d")
    hasnt_wotd = cur.execute("SELECT * FROM wotd WHERE date=?", [cur_day]).fetchall() == []

    if hasnt_wotd:
        print("has not")
        if "wotd_answer" in session:
            print("ehhh")
            session["wotd_answer"] = ""
        wotd_question()
        wotd = cur.execute("SELECT * FROM wotd WHERE date=?", [cur_day]).fetchall()
        return wotd[0]
    else: 
        print("has")
        wotd = cur.execute("SELECT * FROM wotd WHERE date=?", [cur_day]).fetchall()
        return wotd[0]
