
const left = document.getElementById('left');
const carousel = document.getElementById('swiper')
const right = document.getElementById('right');



var request = new XMLHttpRequest();
request.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200){
        var listing = JSON.parse(this.responseText);

        var id = listing.Lid;
        var email = listing.email;
        var author = listing.author;
        var availability = listing.availability;
        var description = listing.description;
        var isbn = listing.isbn;
        var title = listing.title;
        var additionalImages = listing.additional_images;
        createListing(isbn, author, description, title, email, additionalImages, id);
        document.title = title;

        
    }
}
request.open("GET", `database/getListingByID.php?id=${id}`, true);
request.send();


function createListing(isbn, author, description, title, email, additional_images, id){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            var data = JSON.parse(this.responseText).items[0].volumeInfo;

            var image = data.imageLinks.thumbnail;
            addImages(image, additional_images, id);
            var details = document.createElement('div');
            details.className = 'container-fluid mt-3';
            details.innerHTML = `
                                <h1 class='display-5'>${title} <h1>
                                <h3>by ${author}</h3>
                                `;        
            left.appendChild(details);


            if (description.length < 300){
                right.innerHTML = `<h2 class='text-center mb-1'><u>Synopsis</u></h2>
                <h4 class='mt-1'>${description}</h4>
                `;
            }else{
                right.innerHTML = `<h2 class='text-center mb-1'><u>Synopsis</u></h2>
                <h4 class='mt-1'>${description.slice(0,250)}<span id='dots'>...</span><span id="more" class='d-none'>${description.slice(250,description.length)}</span></h4>
                <button type="button" class="btn btn-secondary mt-1" onclick="getMore()" id='moreButton'>Read More</button>`;    
            }
            fetchUserInfo(email);
        }
    }
    request.open("GET", `https://www.googleapis.com/books/v1/volumes?q=isbn:${isbn}`, true);
    request.send();
}

function getMore(){
    event.preventDefault();
    var more = document.getElementById('more');
    var dots = document.getElementById('dots');
    var button = document.getElementById('moreButton')
    if (more.className == 'd-none'){
        more.className = 'd-inline';
        dots.className = 'd-none';
        button.innerText = 'Read Less'
    }else{
        more.className = 'd-none';
        dots.className = 'd-inline';
        button.innerText = 'Read More'

    }
}

function fetchUserInfo(email){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
    if (this.readyState == 4 && this.status == 200){
        var listing = JSON.parse(this.responseText);

        var lastName = listing.lastName;
        var firstName = listing.firstName;
        var telegram = listing.telegram;
        var email = listing.email;

        var profile = document.createElement('div');
        profile.className = 'container-fluid';
        if (loggedIn){
            profile.innerHTML = `<h5 class='mt-5'>
                                    <strong><u>Owner Details:</u></strong><br>
                                    ${lastName} ${firstName}<br>
                                    Email: ${email}<br>
                                    Telegram Handle: ${telegram}
                                </h5>
                                <a href="./listingsForTrade.html?id=${id}" role="button"><button type="button" class="btn btn-primary mt-5">Request Trade</button></a>
                                `;

        }else{
            profile.innerHTML = `<h5 class='mt-5'>
                                    <strong><u>Owner Details:</u></strong><br>
                                    Please Log In to see Owner Details!<br>
                                </h5>
                                <a href="./loginPage.html" role="button"><button type="button" class="btn btn-primary mt-2">Log In</button></a>
                                `;            
        }
        
        // console.log(listing)

        right.appendChild(profile);


        
    }
}
request.open("GET", `database/getUserByEmail.php?email=${email}`, true);
request.send()
};


function addImages(image, additional_images, id){
    if (additional_images == 1){
        carousel.innerHTML = `
                            <div class="swiper-slide"><img src="userAdded/${id}-0.jpg" style="width: 70%; height: 80%"></div>
                            <div class="swiper-slide"><img src="${image}" class="w-50 mx-auto"></div>`;
                

    }else if(additional_images == 2){
        carousel.innerHTML = `
        <div class="swiper-slide"><img src="userAdded/${id}-0.jpg" style="width: 70%; height: 80%"></div>
        <div class="swiper-slide"><img src="userAdded/${id}-1.jpg" style="width: 70%; height: 80%"></div>
        <div class="swiper-slide"><img src="${image}" class="w-50 mx-auto"></div>
        `;                

    }else{
        left.innerHTML = `<img src='${image}' class='pl-2 w-50 mx-auto'> `;

    }
    var swiper = new Swiper('.swiper-container', {
        observer: true,
        autoHeight: true, //enable auto height
        spaceBetween: 20,
        loop: true,
        slidesPerView: 1,
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },

        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
    });


}