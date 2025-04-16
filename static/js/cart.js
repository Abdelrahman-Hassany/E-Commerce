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
        if (data.newQuantity === 0 || data.deleted == 'True' ) {
            const itemRow = document.getElementById(`item-row-${productID}`);
            if (itemRow) {
                itemRow.remove();
            }
        }

        // update quanityt in cart
        const cartTotal = document.getElementById('cart-total');
        if (cartTotal && data.cartItemsCount !== undefined) {
            cartTotal.innerText = data.cartItemsCount;
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

        if(data.message == 'u must log in'){
            console.log('log in plz!')

            if (action == 'add' ) {
                if(cart[productID] == undefined){
                    cart[productID] = {'quantity':1}
                }else{
                    cart[productID]['quantity'] += 1 
                }
            }
            
            if (action == 'remove'){
                cart[productID]['quantity'] -= 1
        
                if (cart[productID]['quantity'] <= 0){
                    console.log('cart is deleted')
                    delete cart[productID]
                }
            }

            console.log('cart:',cart)
            document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
        }
        

    })
    .catch(error => {
        console.error('Error:', error);
        alert('You need to log in to update the cart.');
    });
}
