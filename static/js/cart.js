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
window.onscroll = function() { scrollFunction() };

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
    event.preventDefault()
    event.stopPropagation()
    let productId = event.target.dataset.product
    let action = event.target.dataset.action
    console.log(productId, action)

    console.log('USER:', user)
    if (user === 'AnonymousUser') {
        console.log('not logged in')
        return
    }
    console.log('user is logged')
    let url = '/update_item/'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'x-CSRFToken': csrftoken
            },
            body: JSON.stringify({ 'productId': productId, 'action': action })
        })
        .then((response) => {
            // location.reload()
            // response.json()
            const cartTotal = document.getElementById('cartTotal')
            const plusMinus = action === 'add' ? 1 : -1;
            cartTotal.innerText = +cartTotal.innerText + plusMinus

            if (location.pathname.includes('cart')) {
                const tr = event.target.closest('tr')
                const korpaCena = tr.querySelector('.korpaCena').innerText.slice(0, -4)
                const quantity = tr.querySelector('.quantity')
                const korpaTotal = tr.querySelector('.korpaTotal')

                quantity.innerText = +quantity.innerText + plusMinus
                const newTotal = +korpaTotal.innerText.slice(0, -3) + korpaCena * plusMinus
                korpaTotal.innerText = newTotal + ',00'

                const cartCheckout = document.getElementById('cartCheckout')
                const [ukupnaKorpa, ukupnaCena] = cartCheckout.querySelectorAll('tbody td')
                const [ukupnaKorpaText, ukupnaKorpaNum] = ukupnaKorpa.innerText.split(': ')
                ukupnaKorpa.innerText = ukupnaKorpaText + ': ' + (+ukupnaKorpaNum + plusMinus)

                const [ukupnaCenaText, ukupnaCenaNum] = ukupnaCena.innerText.split(': ')
                ukupnaCena.innerText = ukupnaCenaText + ': ' + (+ukupnaCenaNum.slice(0, -4) + korpaCena * plusMinus) + ',00e'
            }

        })
}