document.addEventListener("DOMContentLoaded", function () {
    document.getElementById('increase').addEventListener('click', function () {
        let qty = document.getElementById('quantity');
        qty.value = parseInt(qty.value) + 1;
    });
    document.getElementById('decrease').addEventListener('click', function () {
        let qty = document.getElementById('quantity');
        if (parseInt(qty.value) > 1) {
            qty.value = parseInt(qty.value) - 1;
        }
    });
});
document.getElementById('quantity').addEventListener('input', function (e) {
    this.value = this.value.replace(/[^0-9]/g, '');
    if (this.value === '') {
        this.value = '1';
    }
});