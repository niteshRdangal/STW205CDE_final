var delivery = '{{order.delivery}}'
var total = '{{order.get_cart_total}}'
console.log(total)

if(delivery == 'False'){
    document.getElementById('delivery-info').innerHTML = ''
    }

if (user != 'AnonymousUser'){
   document.getElementById('user-info').innerHTML = ''
}

if (delivery == 'False' && user != 'AnonymousUser'){
    document.getElementById('form-wrapper').classList.add("hidden");
    document.getElementById('payment-info').classList.remove("hidden");
}

var form = document.getElementById('form')
    form.addEventListener('submit',function(e){
        e.preventDefault()
        console.log('Form Submitted')
        document.getElementById('form-button').classList.add("hidden");
        document.getElementById('payment-info').classList.remove("hidden")
    })

    document.getElementById('make-payment').addEventListener('click',function(e){
        submitFormdata()

    })

    function submitFormdata(){
        console.log('payment button Clicked')

        var userFormData = {
            'name':null,
            'email':null,
            'total':total,
        }

        var deliveryInfo = {
            'address':null,
            'city':null,
            'state':null,
            'zipcode':null,

        }

        if(delivery != 'False'){
            deliveryInfo.address = form.address.value
            deliveryInfo.city = form.city.value
            deliveryInfo.state = form.state.value
            deliveryInfo.zipcode = form.zipcode.value
        }

        if(user == 'AnonymousUser'){
            userFormData.name = form.name.value
            userFormData.city = form.email.value
        }

        var url = '/process_order/'
        fetch(url,{
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'X-CSRFToken':csrftoken,
            },
            body:JSON.stringify({'form':userFormData, 'delivery':deliveryInfo})
        })
        .then((response) => response.json())
        .then((data) => {
            console.log('Success:',data);
            alert('transaction completed');

            cart = {}
            document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

            window.location.href = 'http://localhost:8000';


        })

    }

