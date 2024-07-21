from flask import Flask, render_template, request, redirect, session
from scripts.search import get_word, check_none
from scripts.helpers import specified_color
from flask_session import Session
from re import findall, M, I

DEFAULT_COLORS = ["#FFFFFF", "#D21404", "#0F52BA", "#028A0F"]

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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
            
        print(cur_colour)

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
    return len(session)

@app.route("/")
def index():
    return render_template("index.html", colours=get_colors())

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
            # redirects_color += 1
            return redirect("/")
        session[cur_color_index] = request.form.get(cur_color_index)
    return redirect("/")

@app.route("/back")
def back():
    return redirect("/")
