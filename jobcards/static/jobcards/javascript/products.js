document.addEventListener('DOMContentLoaded', () => {
    var save_btn = document.querySelectorAll(".save-changes");
    save_btn.forEach((button) => {
        button.addEventListener('click', () => save_changes_product(button.dataset.id));
    });
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}

function save_changes_product(id) {
    // modal fields data
    const product_manufacturer = document.querySelector(`#product_manufacturer_${id}`).value;
    const product_model = document.querySelector(`#product_model_${id}`).value;
    const product_price = document.querySelector(`#product_price_${id}`).value;

    // table html
    const product_manufacturer_html = document.querySelector(`#table_manufacturer_${id}`);
    const product_model_html = document.querySelector(`#table_model_${id}`);
    const product_price_html = document.querySelector(`#table_price_${id}`);

    const modal = document.querySelector(`#modal_edit_${id}`);

    fetch(`/edit_product/${id}`, {
        method: "POST",
        headers: {"Content-type":"application/json", "X-CSRFToken": getCookie('csrftoken')},
        body: JSON.stringify({
            manufacturer: product_manufacturer,
            model: product_model,
            price: product_price
        })
    })
    .then(repsone => repsone.json())
    .then(result => {
        product_manufacturer_html.innerHTML = result.manufacturer;
        product_model_html.innerHTML = result.model;
        product_price_html.innerHTML = `R ${result.price}`;
        
        modal.classList.remove('show');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('style', 'display: none');

        const modalsBackdrops = document.getElementsByClassName('modal-backdrop');

        for(let i=0; i<modalsBackdrops.length; i++) {
            document.body.removeChild(modalsBackdrops[i]);}
        console.log(result.name)
    })
}