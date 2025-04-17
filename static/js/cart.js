var updateBtns = document.getElementsByClassName('update-cart');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productID = this.dataset.product;
        var action = this.dataset.action;

        console.log('Product Id:', productID, 'Action:', action);
        updateUserOrder(productID, action);
    });
}

function updateUserOrder(productID, action) {
    fetch('/update_item/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productID, 'action': action }),
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Unauthorized or server error');
            }
            return response.json();
        })
        .then(data => {
            console.log('Response Body:', data);

            // update quantity 
            const quantityEl = document.getElementById(`item-quantity-${productID}`);
            if (quantityEl && data.newQuantity !== undefined) {
                quantityEl.innerText = data.newQuantity;
            }

            // delete cart and refresh page
            if (data.newQuantity === 0 || data.deleted == 'True') {
                const itemRow = document.getElementById(`item-row-${productID}`);
                if (itemRow) {
                    itemRow.remove();
                }
            }

            // update cart total
            const cartTotal = document.getElementById('cart-total');
            if (cartTotal && data.cartTotal !== undefined) {
                cartTotal.innerText = data.cartTotal;
            }

            
            const totalProductPrice = document.getElementById(`total_product_price_${productID}`);
            if (totalProductPrice && data.ProductTotal !== undefined) {
                totalProductPrice.innerText = data.ProductTotal;
            }

            const cartCount = document.getElementById('cart-count');
            if (cartCount && data.cartItemsCount !== undefined) {
                cartCount.innerText = data.cartItemsCount;
            }

            if (data.cartItemsCount === 0) {
                const table = document.querySelector('table');
                if (table) table.remove();

                const totalSection = document.querySelector('.text-end');
                if (totalSection) totalSection.remove();

                const container = document.querySelector('.container');
                const alert = document.createElement('div');
                alert.className = 'alert alert-info';
                alert.innerText = 'Your cart is empty.';
                container.appendChild(alert);
            }

        })
        .catch(error => {
            console.error('Error:', error);
            alert('You need to log in to update the cart.');
        });
}



