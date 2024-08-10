let opt = document.getElementById("options");
let search = document.getElementById("search");

search.addEventListener("keyup", function() {
    fetch("http://localhost:5000/autocomplete", {
        method: "POST",
        body: JSON.stringify({ "query": search.value }),
        headers: {
          "Content-type": "application/ld+json; charset=UTF-8"
        }
      }).then((response) => 
        response.json().then((json) => {
            let html = "";
            for (let i = 0; i < json.length; i++) {
              html += `<ul>${json[i]}</ul>\n`
            }

            opt.innerHTML = html
          }
        )
      );
});