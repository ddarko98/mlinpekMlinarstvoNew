window.addEventListener('scroll', reveal);

function reveal() {
    let reveals = document.querySelectorAll('.reveal');
    for (let i = 0; i < reveals.length; i++) {
        let windowheight = window.innerHeight;
        let revealTop = reveals[i].getBoundingClientRect().top;
        let revealpoint = 150;

        if (revealTop < windowheight - revealpoint) {
            reveals[i].classList.add('aktiviraj');
        } else {
            reveals[i].classList.remove('aktiviraj');
        }
    }
}

let mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
    scrollFunction();
};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
    } else {
        mybutton.style.display = "none";
    }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function updateToCart(event) {
    event.preventDefault();
    event.stopPropagation();

    let productId = event.target.dataset.product;
    let action = event.target.dataset.action;
    console.log(productId, action);

    if (user === 'AnonymousUser') {
        console.log('Not logged in');
        return;
    }

    // Update UI immediately
    const cartTotal = document.getElementById('cartTotal');
    const plusMinus = action === 'add' ? 1 : -1;
    cartTotal.innerText = Math.max(0, +cartTotal.innerText + plusMinus);

    if (location.pathname.includes('cart')) {
        // Update quantities and totals dynamically
        const tr = event.target.closest('tr');
        const korpaCena = parseFloat(tr.querySelector('.korpaCena').innerText.slice(0, -4));
        const quantity = tr.querySelector('.quantity');
        const korpaTotal = tr.querySelector('.korpaTotal');

        const newQuantity = +quantity.innerText + plusMinus;

        if (newQuantity > 0) {
            // Update quantities and totals
            quantity.innerText = newQuantity;

            const newTotal = +korpaTotal.innerText.slice(0, -3) + korpaCena * plusMinus;
            korpaTotal.innerText = newTotal.toFixed(2) + ',00';

            const cartCheckout = document.getElementById('cartCheckout');
            const [ukupnaKorpa, ukupnaCena] = cartCheckout.querySelectorAll('tbody td');
            const [ukupnaKorpaText, ukupnaKorpaNum] = ukupnaKorpa.innerText.split(': ');
            ukupnaKorpa.innerText = ukupnaKorpaText + ': ' + Math.max(0, +ukupnaKorpaNum + plusMinus);

            const [ukupnaCenaText, ukupnaCenaNum] = ukupnaCena.innerText.split(': ');
            ukupnaCena.innerText =
                ukupnaCenaText + ': ' + (+ukupnaCenaNum.slice(0, -4) + korpaCena * plusMinus).toFixed(2) + ',00e';
        } else {
            // Remove row if quantity reaches 0
            tr.remove();

            // Update totals in cart summary
            const cartCheckout = document.getElementById('cartCheckout');
            const [ukupnaKorpa, ukupnaCena] = cartCheckout.querySelectorAll('tbody td');
            const [ukupnaKorpaText, ukupnaKorpaNum] = ukupnaKorpa.innerText.split(': ');
            ukupnaKorpa.innerText = ukupnaKorpaText + ': ' + Math.max(0, +ukupnaKorpaNum + plusMinus);

            const [ukupnaCenaText, ukupnaCenaNum] = ukupnaCena.innerText.split(': ');
            ukupnaCena.innerText =
                ukupnaCenaText + ': ' + (+ukupnaCenaNum.slice(0, -4) + korpaCena * plusMinus).toFixed(2) + ',00e';
        }
    }

    // Send update to the server
    let url = '/update_item/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json',
            'x-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ productId: productId, action: action }),
    })
        .then((response) => response.json())
        .then((data) => {
            console.log('Response from backend:', data);

            if (data.cartItems !== undefined) {
                cartTotal.innerText = data.cartItems;
            }

            if (data.newQuantity === 0 && location.pathname.includes('cart')) {
                const tr = event.target.closest('tr');
                tr.remove();
            }
        })
        .catch((error) => {
            console.error('Error updating cart:', error);

            // Rollback UI changes in case of an error
            cartTotal.innerText = Math.max(0, +cartTotal.innerText - plusMinus);

            if (location.pathname.includes('cart')) {
                const tr = event.target.closest('tr');
                const quantity = tr.querySelector('.quantity');
                const korpaCena = parseFloat(tr.querySelector('.korpaCena').innerText.slice(0, -4));
                const korpaTotal = tr.querySelector('.korpaTotal');

                if (+quantity.innerText - plusMinus >= 0) {
                    quantity.innerText = +quantity.innerText - plusMinus;

                    const newTotal = +korpaTotal.innerText.slice(0, -3) - korpaCena * plusMinus;
                    korpaTotal.innerText = newTotal.toFixed(2) + ',00';
                }
            }
        });
}
