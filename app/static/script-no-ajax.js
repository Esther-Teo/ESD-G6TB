// var stripe = Stripe('checkout_public_key');
        
// var checkoutButton = document.getElementById('checkout-button');
// console.log(checkoutButton);
// console.log("LANJIAO");
// checkoutButton.addEventListener('click', function() {
// // Create a new Checkout Session using the server-side endpoint you
// // created in step 3.


// // fetch appended to the end of the url
// fetch('/create-checkout-session', {
//     method: 'POST',
//     })
//     .then(function(response) {
//         return response.json();
//     })
//     .then(function(session) {
//         return stripe.redirectToCheckout({ sessionId: checkout_session_id });
//     })
//     .then(function(result) {
//         // If `redirectToCheckout` fails due to a browser or network
//         // error, you should display the localized error message to your
//         // customer using `error.message`.
//         if (result.error) {
//         alert(result.error.message);
//         }
//     })
//     .catch(function(error) {
//         console.error('Error:', error);
//     });
// });