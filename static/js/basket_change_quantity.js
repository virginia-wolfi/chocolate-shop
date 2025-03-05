document.addEventListener("DOMContentLoaded", function () {
    let decreaseButtons = document.querySelectorAll(".minus-btn");
    let increaseButtons = document.querySelectorAll(".plus-btn");
    let quantityInputs = document.querySelectorAll(".quantity-input");

    function updateCart(productId, changeInQuantity) {
        fetch(addToCartUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": getCSRFToken(),
            },
            body: `product_pk=${productId}&quantity=${changeInQuantity}`
        }).then(response => {
            if (response.ok) {
                location.reload();  // Перезагружаем страницу
            } else {
                console.error("Ошибка обновления корзины");
            }
        }).catch(error => console.error("Ошибка:", error));
    }

    decreaseButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            let productId = this.dataset.productId;
            let quantityInput = document.querySelector(`input[data-product-id='${productId}']`);
            let currentQuantity = parseInt(quantityInput.value);

            if (currentQuantity > 1) {
                updateCart(productId, -1);  // Отправляем -1 для уменьшения
                quantityInput.value = currentQuantity - 1;
            }
        });
    });

    increaseButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            let productId = this.dataset.productId;
            let quantityInput = document.querySelector(`input[data-product-id='${productId}']`);
            let currentQuantity = parseInt(quantityInput.value);

            updateCart(productId, 1);  // Отправляем +1 для увеличения
            quantityInput.value = currentQuantity + 1;
        });
    });

    quantityInputs.forEach(function (input) {
        input.addEventListener("change", function () {
            let productId = this.dataset.productId;
            let newQuantity = Math.max(1, parseInt(this.value));
            this.value = newQuantity;
            updateCart(productId, newQuantity - parseInt(this.defaultValue));  // Отправляем изменение количества
        });
    });

    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});