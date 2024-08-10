from flask import Flask, render_template, request, redirect, session
from scripts.search import get_word, check_none, search_dbs
from scripts.helpers import specified_color, wotd_gen
from flask_session import Session
from re import findall, M, I
from sqlite3 import *
from datetime import datetime
from flask_cors import CORS

DEFAULT_COLORS = ["#FFFFFF", "#D21404", "#0F52BA", "#028A0F"]

app = Flask(__name__)

app.jinja_env.filters["ord"] = ord # ord() function
app.jinja_env.filters["chr"] = chr # chr() function

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)

def merge(word_dict):
    global DEFAULT_COLORS
    pos_merge, def_merge, sentence_merge, syn_merge = "", "", "", ""
    span_br = "</span><br>"

    for i in range(len(word_dict)):
        
        word_dict[i] = check_none(word_dict[i]["pos"], word_dict[i])

        ip = (i + 1)
        if i == 0:
            num = (str(ip) + ". ")
        else:
            num = (" " + str(ip) + ". ")

        if get_colors() == 0:
            cur_colour = i % len(DEFAULT_COLORS)
        else:
            cur_colour = i % get_colors()

        span = specified_color(False, "color1" not in session, DEFAULT_COLORS, cur_colour, session)
        full = (span + num)

        if not (word_dict[i]["pos"] == "noun"):
            sentence_merge += (full + word_dict[i]["sentence"] + span_br)

        pos_merge += (full + word_dict[i]["pos"] + "</span>")
        def_merge += (full + word_dict[i]["definition"] + span_br)

    for j in range(len(word_dict[0]["synonyms"])):
        syn_split = findall(r"[^;|\s]+", word_dict[0]["synonyms"][j], I | M)
        syn_str = ""

        for syn in syn_split:
            syn_str += syn + " "

        span = specified_color(True, "color1" not in session, DEFAULT_COLORS, 0, session)

        syn_merge += (span + syn_str + span_br)

    return [pos_merge, def_merge, sentence_merge, syn_merge]

def get_colors():
    colors = 0
    print(session)
    for key in session.keys():
        print(key)
        if key[:5] == "color":
            colors += 1

    return colors

@app.route("/")
def index():
    db = connect("./dict.db")
    cur = db.cursor()
    
    wotd_q = wotd_gen()
    question = wotd_q[5]
    options = wotd_q[1:5] # 4 + 1 because of python's list slicing being [x:y-1]

    return render_template("index.html", colours=get_colors(), question=question, options=options, default_colors=DEFAULT_COLORS)

@app.route("/word", methods=["POST"])
def word():
    global redirects_word
    redirects_word = 0

    word = request.form.get("word").lower()

    if not word:
        return redirect("/")
    
    res = get_word(word)
    if res == []:
        return redirect("/")
    else:
        merge_res = merge(res)
        return render_template("word.html", word=word, pos=merge_res[0], definition=merge_res[1], sentence=merge_res[2], syn=merge_res[3])

@app.route("/color", methods=["POST"])
def colors():
    global redirects_color

    print(request.form)

    for i in range(len(request.form)):
        cur_color_index = "color" + str(i + 1)
        cur_color = request.form.get(cur_color_index)
        if cur_color[0] != "#":
            return redirect("/")
        session[cur_color_index] = request.form.get(cur_color_index)
    return redirect("/")

@app.route("/wotd", methods=["POST"])
def wotd():
    print("hello")
    usr_ans = request.form.get("wotd_answer")
    print(usr_ans)
    session["wotd_answer"] = usr_ans
    if (not usr_ans) or (usr_ans not in ["A", "B", "C", "D"]):
        return redirect("/")
    
    db = connect("./dict.db")
    cur = db.cursor()

    usr_ans_type = usr_ans.lower() + '_ans'
    print(usr_ans_type)
    cur.execute(f"UPDATE wotd SET {usr_ans_type}=? WHERE date=?", [(cur.execute(f"SELECT {usr_ans_type} FROM wotd").fetchall()[0][0]) + 1, datetime.now().strftime("%Y-%m-%d")])
    db.commit()
    cur.execute(f"UPDATE wotd SET total_ans=? WHERE date=?", [(cur.execute("SELECT total_ans FROM wotd").fetchall()[0][0]) + 1, datetime.now().strftime("%Y-%m-%d")])
    db.commit()
    
    return redirect("/wotd_overview")

@app.route("/wotd_overview")
def wotd_overview():
    db = connect("./dict.db")
    cur = db.cursor()

    word = cur.execute("SELECT question FROM wotd WHERE date=?;", [datetime.now().strftime("%Y-%m-%d")]).fetchall()
    word = word[0][0]

    if session["wotd_answer"] == cur.execute("SELECT answer FROM wotd WHERE date=?;", [datetime.now().strftime("%Y-%m-%d")]).fetchall()[0][0]:
        msg = "<h5>Congratulations, you got the Word of the Day question correct!</h5>"
    else:
        msg = "<h5>Unlucky, get it right next time.</h5>"


    wotd_word = findall(r"[a-zA-z]+", word, I | M)
    wotd_word = wotd_word[len(wotd_word) - 1]
    
    res = get_word(wotd_word)
    merge_res = merge(res)
        
    return render_template("wotd.html", word=word, msg=msg, wotd_word=wotd_word, pos=merge_res[0], definition=merge_res[1], sentence=merge_res[2], syn=merge_res[3])

@app.route("/back")
def back():
    return redirect("/")

@app.route("/autocomplete", methods=["POST"])
def autocomplete():
    query = request.get_json()["query"]
    db = connect("./dict.db")
    cur = db.cursor()
    possible_words = []
    
    for i in range(len(search_dbs)): 
        temp = cur.execute(f'SELECT Word FROM {search_dbs[i]} WHERE Word LIKE ? ORDER BY Word ASC;', ["%" + query + "%"]).fetchall()
        for item in temp:
            possible_words.append(item[0])
    print(possible_words)
    possible_words = list(set(possible_words))
    return possible_words[:20]