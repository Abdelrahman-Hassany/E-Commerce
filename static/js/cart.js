var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log('Product Id:', productID, 'Action:', action)

        console.log('user:', user)
        if (user == 'AnonymousUser') {
            console.log('You Need To authenticated ')
        } else {
            updateUserOrder(productID,action)
        }
    })
}

function updateUserOrder(productID,action){
    console.log(user ,'is authenticated ')

    var url = '/update_item/'
    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productID':productID,'action':action}),
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
       console.log('data',data);
       if (user == 'AnonymousUser') {
        console.log('You Need To authenticated ')
    } else {
        location.reload()
    }
    });

}