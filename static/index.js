let add_btn = document.getElementById("add_btn");
let color_form = document.getElementById("color_form");

let submit_btn = '<button type="submit" class="add_color">Change color settings</button>';

let color_cnt = 4

function add_color() {
    color_cnt += 1;
    let color_form_inner = color_form.innerHTML;
    let color_btn = `<input type="color" name="color${color_cnt}" class="search longer" value="#FFFFFF"><br>`;
    color_form_inner = color_form_inner.replace(submit_btn, color_btn + submit_btn);
    color_form.innerHTML = color_form_inner;
}

add_btn.addEventListener("click", add_color);