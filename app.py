from flask import Flask, render_template, request, redirect
from sqlite3 import *
from search import get_word, check_none

redirects = 0

def merge(word_dict):
    pos_merge, def_merge, sentence_merge, syn_merge = "", "", "", ""

    for i in range(len(word_dict)):
        
        word_dict[i] = check_none(word_dict[i]["pos"], word_dict[i])

        ip = (i + 1)
        if i == 0:
            num = (str(ip) + ". ")
        else:
            num = (" " + str(ip) + ". ")

        span = '<span class="span-' + str(ip % 4) + '">'
        full = (span + num)

        if not (word_dict[i]["pos"] == "noun"):
            sentence_merge += (full + word_dict[i]["sentence"] + "</span><br>")

        pos_merge += (full + word_dict[i]["pos"] + "</span>")
        def_merge += (full + word_dict[i]["definition"] + "</span><br>")
        syn_merge += (full + word_dict[i]["synonyms"][0] + "</span><br>")

    return [pos_merge, def_merge, sentence_merge, syn_merge]

app = Flask(__name__)

@app.route("/")
def index():
    if redirects > 0:
        return render_template("index.html", not_found="<h5>Not a word!</h5>")
    else:
        return render_template("index.html", not_found="")

@app.route("/word", methods=["POST"])
def word():
    global redirects
    redirects = 0

    word = request.form.get("word").lower()

    if not word:
        redirects += 1
        return redirect("/")
    
    res = get_word(word)
    if res == []:
        redirects += 1
        return redirect("/")
    else:
        merge_res = merge(res)
        return render_template("word.html", word=word, pos=merge_res[0], definition=merge_res[1], sentence=merge_res[2], syn=merge_res[3])

@app.route("/back")
def back():
    return redirect("/")
