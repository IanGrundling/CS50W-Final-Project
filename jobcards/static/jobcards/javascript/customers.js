document.addEventListener('DOMContentLoaded', () => {
    var save_btn = document.querySelectorAll(".save-changes");
    save_btn.forEach((button) => {
        button.addEventListener('click', () => save_changes_customer(button.dataset.id));
    });
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}

function save_changes_customer(id) {
    // modal fields data
    const cust_name = document.querySelector(`#cust_name_${id}`).value;
    const cust_surname = document.querySelector(`#cust_surname_${id}`).value;
    const cust_number = document.querySelector(`#cust_number_${id}`).value;
    const cust_email = document.querySelector(`#cust_email_${id}`).value;

    // table html
    const cust_name_html = document.querySelector(`#table_name_${id}`);
    const cust_surname_html = document.querySelector(`#table_surname_${id}`);
    const cust_number_html = document.querySelector(`#table_number_${id}`);
    const cust_email_html = document.querySelector(`#table_email_${id}`);

    const modal = document.querySelector(`#modal_edit_${id}`);

    fetch(`/edit_customer/${id}`, {
        method: "POST",
        headers: {"Content-type":"application/json", "X-CSRFToken": getCookie('csrftoken')},
        body: JSON.stringify({
            name: cust_name,
            surname: cust_surname,
            number: cust_number,
            email: cust_email
        })
    })
    .then(repsone => repsone.json())
    .then(result => {
        cust_name_html.innerHTML = result.name;
        cust_surname_html.innerHTML = result.surname;
        cust_number_html.innerHTML = result.number;
        cust_email_html.innerHTML = result.email;
        
        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('style', 'display: none');

        const modalsBackdrops = document.getElementsByClassName('modal-backdrop');

        for(let i=0; i<modalsBackdrops.length; i++) {
            document.body.removeChild(modalsBackdrops[i]);}
        console.log(result.name)
    })
}