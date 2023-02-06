document.addEventListener('DOMContentLoaded', () => {
    var add_btn = document.querySelectorAll(".add-product");
    add_btn.forEach((button) => {
        var id = button.dataset.id;
        var action = button.dataset.action;
        button.addEventListener('click', () => add_product(id, action))
    });
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}

function add_product(id, action) {
    fetch("/update_jobcard", {
        method: "POST",
        headers: {"Content-type":"application/json", "X-CSRFToken": getCookie('csrftoken')},
        body: JSON.stringify({
            id: id,
            action: action,
        })
    })
    .then(repsone => repsone.json())
    .then(result => {
        console.log(result)
    })
}