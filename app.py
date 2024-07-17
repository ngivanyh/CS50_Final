from flask import Flask, render_template, request, redirect, session
from sqlite3 import *
from search import get_word, check_none
from flask_session import Session
from string import digits, ascii_uppercase

redirects_word = 0
redirects_color = 0
colours = 3
DEFAULT_COLORS = ["#FFFFFF", "#D21404", "#0F52BA"]
changed_colors = False

def merge(word_dict):
    global colours
    global DEFAULT_COLORS
    pos_merge, def_merge, sentence_merge, syn_merge = "", "", "", ""

    for i in range(len(word_dict)):
        
        word_dict[i] = check_none(word_dict[i]["pos"], word_dict[i])

        ip = (i + 1)
        if i == 0:
            num = (str(ip) + ". ")
        else:
            num = (" " + str(ip) + ". ")

        cur_colour = ip % colours
        cur_colour += 1
        if not changed_colors:
            span = '<span style="color: ' + DEFAULT_COLORS[ip % colours] + ';">'
        else:
            span = '<span style="color: ' + session["color" + str(cur_colour)] + ';">'
        full = (span + num)

        if not (word_dict[i]["pos"] == "noun"):
            sentence_merge += (full + word_dict[i]["sentence"] + "</span><br>")

        pos_merge += (full + word_dict[i]["pos"] + "</span>")
        def_merge += (full + word_dict[i]["definition"] + "</span><br>")
        syn_merge += (full + word_dict[i]["synonyms"][0] + "</span><br>")

    return [pos_merge, def_merge, sentence_merge, syn_merge]

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
    if redirects_word > 0:
        return render_template("index.html", not_found="<h5>Not a word!</h5>")
    elif redirects_color > 0:
        return render_template("index.html", not_found="<h5>Invalid Color!</h5>")
    else:
        return render_template("index.html", not_found="")

@app.route("/word", methods=["POST"])
def word():
    global redirects_word
    redirects_word = 0

    word = request.form.get("word").lower()

    if not word:
        redirects_word += 1
        return redirect("/")
    
    res = get_word(word)
    if res == []:
        redirects_word += 1
        return redirect("/")
    else:
        merge_res = merge(res)
        return render_template("word.html", word=word, pos=merge_res[0], definition=merge_res[1], sentence=merge_res[2], syn=merge_res[3])

@app.route("/color", methods=["POST"])
def colors():
    global redirects_color
    global colours
    global changed_colors
    colours = len(request.form)
    print(colours)
    for i in range(colours):
        cur_color_index = "color" + str(i + 1)
        cur_color = request.form.get(cur_color_index)
        if (cur_color[0] != "#") or (not cur_color) or (not len(cur_color) == 7):
            print("first invalid")
            redirects_color += 1
            return redirect("/")
        hex_color_check = cur_color[1:].upper()
        for i in range(6):
            if hex_color_check[i] not in ascii_uppercase[:6]:
                if hex_color_check[i] not in digits:
                    print("second invalid")
                    redirects_color += 1
                    return redirect("/")
        session[cur_color_index] = request.form.get(cur_color_index)
    changed_colors = True
    return redirect("/")

@app.route("/back")
def back():
    return redirect("/")
