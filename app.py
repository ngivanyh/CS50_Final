from flask import Flask, render_template, request, redirect, session
from search import get_word, check_none
from flask_session import Session
from re import findall, M, I

# redirects_word = 0
# redirects_color = 0
colours = 4
DEFAULT_COLORS = ["#FFFFFF", "#D21404", "#0F52BA", "#028A0F"]

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

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

        cur_colour = i % colours
        print(cur_colour)

        if "color1" not in session:
            span = '<span style="color: ' + DEFAULT_COLORS[cur_colour] + ';">'
        else:
            span = '<span style="color: ' + session["color" + str(cur_colour + 1)] + ';">'
        full = (span + num)

        if not (word_dict[i]["pos"] == "noun"):
            sentence_merge += (full + word_dict[i]["sentence"] + "</span><br>")

        pos_merge += (full + word_dict[i]["pos"] + "</span>")
        def_merge += (full + word_dict[i]["definition"] + "</span><br>")
        syn_split = findall(r"[^;|\s]+", word_dict[i]["synonyms"][0], I | M)
        syn_str = ""

        for syn in syn_split:
            syn_str += syn + " "

        syn_merge += (full + syn_str + "</span><br>")

    return [pos_merge, def_merge, sentence_merge, syn_merge]

@app.route("/")
def index():
    global colours
    
    return render_template("index.html", colours=colours)

@app.route("/word", methods=["POST"])
def word():
    global redirects_word
    redirects_word = 0

    word = request.form.get("word").lower()

    if not word:
        # redirects_word += 1
        # # session["redirects_word"] = 1
        return redirect("/")
    
    res = get_word(word)
    if res == []:
        # redirects_word += 1
        return redirect("/")
    else:
        merge_res = merge(res)
        return render_template("word.html", word=word, pos=merge_res[0], definition=merge_res[1], sentence=merge_res[2], syn=merge_res[3])

@app.route("/color", methods=["POST"])
def colors():
    global redirects_color
    global colours
    colours = len(request.form)

    print(request.form)

    for i in range(colours):
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
