var Mousetrap = require("mousetrap/mousetrap");

let search_bar = document.getElementById("search");

function search_focus() {
    search_bar.focus()
}

Mousetrap.bind("command+;", search_focus);