document.addEventListener('DOMContentLoaded', () => {
    var select_val = document.querySelector("#product").value;
    var manufacturer_filter = document.querySelector("#product");
    manufacturer_filter.addEventListener('change', () => product_filter(manufacturer_filter.value));
    if(select_val === manufacturer_filter.value) {
        console.log(`${select_val} selected`)
    }
});

function product_filter(id) {
    console.log(`${id} selected`)
}