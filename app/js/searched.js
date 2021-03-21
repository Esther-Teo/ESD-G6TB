//console.log(user_input);
//alert(previous_user_input);

if (previous_user_input != null){
    //alert("user came from home");
    //alert(previous_user_input);
    //alert(previous_user_option);
    document.getElementById("search_option_title").innerText = previous_user_option;
    document.getElementById("user_input").value = previous_user_input;
    get_searched_listings();
}
function ChangeDropDownBox (option){
    var selected_search_option = option;
    document.getElementById("search_option_title").innerText = selected_search_option;
}
var allListings1 = document.getElementById('listings1');


 
function get_searched_listings_by_enter(event){
    if (event.keyCode === 13) {
        get_searched_listings();
    }
}

function get_searched_listings(){
    //alert("tried to fetch books");
    var searched = document.getElementById("user_input").value;
    var searched_option =  document.getElementById("search_option_title").innerText;
    //alert(searched_option);
    //alert(searched);
    if (searched_option == "Author")
    {
        if (document.getElementById("listings1").innerHTML != undefined) {
            document.getElementById("listings1").innerHTML = "";
            //alert("element exist");
        }
    const request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (request.readyState == 4 && request.status == 200){
            var data = JSON.parse(request.responseText);
        }
        if (data != undefined){
            for (s=0; s< data.length;s++){
                const request = new XMLHttpRequest();
                request.onreadystatechange = function() {
                    if (request.readyState == 4 && request.status == 200){
                        // console.log(data[s]);
                        // console.log(request.responseText);
                        var listing_data = JSON.parse(request.responseText);
                        var isbn = listing_data.isbn;
                        var author = listing_data.author; 
                        var title = listing_data.title; 
                        var id = listing_data.Lid; 
                        if (listing_data.availability == 1){
                        createListings(isbn, author, title, id)
                        }
                    }
                }
                request.open("GET", `database/getListingByID.php?id=${data[s]}`, true);
                request.send();
            }
        }
}
    request.open("GET", `database/getListingByAuthor.php?author=${searched}`, true);
    request.send();
    }
    else if (searched_option=="Title"){
        //alert("Is title");
        //console.log(document.getElementById("listings1"));
        //console.log(document.getElementById("listings1").innerHTML);
        if (document.getElementById("listings1").innerHTML != undefined) {
            document.getElementById("listings1").innerHTML = "";
            //alert("element exist");
        }
        const request = new XMLHttpRequest();
        request.onreadystatechange = function() {
            if (request.readyState == 4 && request.status == 200){
            var data = JSON.parse(request.responseText);
            }
            if (data != undefined){
                for (s=0; s < data.length;s++){
                    const request = new XMLHttpRequest();
                    request.onreadystatechange = function() {
                        if (request.readyState == 4 && request.status == 200){
                            var listing_data = JSON.parse(request.responseText);
                            //console.log(listing_data);
                            var isbn = listing_data.isbn;
                            var author = listing_data.author; 
                            var title = listing_data.title; 
                            var id = listing_data.Lid; 
                            if (listing_data.availability == 1){
                            createListings(isbn, author, title, id)
                            }
                        }
                    }
                    request.open("GET", `database/getListingByID.php?id=${data[s]}`, true);
                    request.send();
                }
            }
    }
    request.open("GET", `database/getListingByTitle.php?book_title=${searched}`, true);
    request.send();
    }
    else if (searched_option=="Genre"){
        if (document.getElementById("listings1").innerHTML != undefined) {
            document.getElementById("listings1").innerHTML = "";
            //alert("element exist");
        }
        //alert(searched_option);
        //alert(searched);
        const request = new XMLHttpRequest();
        request.onreadystatechange = function() {
            if (request.readyState == 4 && request.status == 200){
            var data = JSON.parse(request.responseText);
            //console.log(data);
            }
            if (data != undefined){
                for (s=0; s < data.length;s++){
                    const request = new XMLHttpRequest();
                    request.onreadystatechange = function() {
                        if (request.readyState == 4 && request.status == 200){
                            var listing_data = JSON.parse(request.responseText);
                            //console.log(listing_data);
                            var isbn = listing_data.isbn;
                            var author = listing_data.author; 
                            var title = listing_data.title; 
                            var id = listing_data.Lid; 
                            if (listing_data.availability == 1){
                            createListings(isbn, author, title, id)
                            }
                        }
                    }
                    request.open("GET", `database/getListingByID.php?id=${data[s]}`, true);
                    request.send();
                }
            }
    }
    request.open("GET", `database/getListingByGenre.php?genre=${searched}`, true);
    request.send();

   }
   else if (searched_option=="User"){
    if (document.getElementById("listings1").innerHTML != undefined) {
        document.getElementById("listings1").innerHTML = "";
        //alert("element exist");
    }
    const request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (request.readyState == 4 && request.status == 200){
        var data = JSON.parse(request.responseText);
        //console.log(data);
        }
        if (data != undefined){
            for (s=0; s < data.length;s++){
                const request = new XMLHttpRequest();
                request.onreadystatechange = function() {
                    if (request.readyState == 4 && request.status == 200){
                        var listing_data = JSON.parse(request.responseText);
                        //console.log(listing_data);
                        //console.log("is owner");

                        var isbn = listing_data.isbn;
                        var author = listing_data.author; 
                        var title = listing_data.title; 
                        var id = listing_data.Lid; 
                        if (listing_data.availability == 1){
                        createListings(isbn, author, title, id)
                        }
                    }
                }
                request.open("GET", `database/getListingByID.php?id=${data[s]}`, true);
                request.send();
            }
        }
}
request.open("GET", `database/getListingByOwner.php?owner_email=${searched}`, true);
request.send();
}

 }

function createListings(isbn, author, title, id){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            var data = JSON.parse(this.responseText).items[0].volumeInfo;

            console.log(data)
            var image = data.imageLinks.thumbnail;
            // var zoomImage = image.replace('zoom=1', 'zoom=3')
            console.log(id)
            console.log(image)

            if (title.length > 25){
                var individualListing = document.createElement('div');
                individualListing.className = 'col-lg-3 col-sm-6 col-md-4 d-flex justify-content-center mb-5';
                individualListing.innerHTML = `<div class="card border-0" style="width: 70%; height: 100% ; background-color: transparent">
                                                    <img src="${image}" class="card-img-top" style="height: 70%"  >
                                                    <div class="card-body mt-2 pt-0 pl-0 pr-0 text-center listing">
                                                        <h5 class="card-title text-primary text-center" >${title.slice(0,24)}...</h5>
                                                        <h6 class="card-subtitle mb-2 text-muted text-center" >${author}</h6>                                                
                                                    </div>
                                                    <div class="hover">
                                                        <a href="listing.php?listingID=${id}">
                                                        <span><i class="fa fa-long-arrow-right" aria-hidden="true"></i></span>
                                                        </a>
                                                    </div>                    
    
                                                </div>`;
            }else{

            var individualListing = document.createElement('div');
            individualListing.className = 'col-lg-3 col-sm-6 col-md-4 d-flex justify-content-center mb-5';
            individualListing.innerHTML = `<div class="card border-0 listing" style="width: 70%; height: 100% ; background-color: transparent">
                                                <img src="${image}" class="card-img-top" style="height: 70%"  >
                                                <div class="card-body mt-2 pt-0 pl-0 pr-0 text-center listing">
                                                    <h5 class="card-title text-primary text-center" >${title}</h5>
                                                    <h6 class="card-subtitle mb-2 text-muted text-center" >${author}</h6>                                                
                                                </div>
                                                <div class="hover">
                                                    <a href="listing.php?listingID=${id}">
                                                    <span><i class="fa fa-long-arrow-right" aria-hidden="true"></i></span>
                                                    </a>
                                                </div>                    

                                            </div>`;

            }
            allListings1.appendChild(individualListing);

            
        }
    }
    request.open("GET", `https://www.googleapis.com/books/v1/volumes?q=isbn:${isbn}`, true);
    request.send();
}