document.addEventListener('DOMContentLoaded', () => {
    var add_btn = document.querySelectorAll(".update_jobcard");
    add_btn.forEach((button) => {
        var id = button.dataset.id;
        var action = button.dataset.action;
        button.addEventListener('click', () => add_product(id, action))
    });
    var cust_input = document.querySelector("#cust_input");
    cust_input.addEventListener('change', () => select_customer(cust_input.value));
    
    document.querySelector("#submit-btn").addEventListener('click', () => submit_jobcard());
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
        var qty = document.querySelector(`#qty_${id}`);
        var item_price = document.querySelector(`#item_total_price_${id}`);
        var total_price = document.querySelector(`#total_price`);
        var total_items = document.querySelector(`#total_items`);

        if(qty.value == 1 && action == 'remove') {
            location.reload()
            console.log('remove')
        } else {
            item_price.innerHTML = `R ${result.item_price}`;
            total_price.innerHTML = `R ${result.total_price}`;
            total_items.innerHTML = `${result.total_items}`;
            document.querySelector(`#qty_${id}`).value = result.product_qty;
            console.log('add');
        }
        
    })
}

function select_customer(name) {
    fetch(`/select_customer`, {
        method: "POST",
        headers: {"Content-type":"application/json", "X-CSRFToken": getCookie('csrftoken')},
        body: JSON.stringify({
            name: name
        })
    })
    .then(repsone => repsone.json())
    .then(result => {
        var cust_name = document.querySelector("#customer_name");
        var cust_surname = document.querySelector("#customer_surname");
        var cust_number = document.querySelector("#customer_number");
        var cust_email = document.querySelector("#customer_email");
        
        cust_name.innerHTML = result.name;
        cust_surname.innerHTML = result.surname;
        cust_number.innerHTML = result.number;
        cust_email.innerHTML = result.email;
        console.log(result)
    })
}

function submit_jobcard() {
    var cust_name = document.querySelector("#customer_name");
    var description = document.querySelector("#description");

    if(cust_name.innerHTML === '' || description.value === '') {
        document.querySelector('#alert').style.display = 'block';
    } else {
        document.querySelector('#alert').style.display = 'none';

        fetch(`/submit_jobcard`, {
            method: "POST",
            headers: {"Content-type":"application/json", "X-CSRFToken": getCookie('csrftoken')},
            body: JSON.stringify({
                description: description.value
            })
        })
        .then(repsone => repsone.json())
        .then(result => {
            alert("Jobcard was created successfully.")
            if(confirm("Jobcard was created successfully.")){
                window.location.reload();  
            }
            console.log(result)
        })
    }
}