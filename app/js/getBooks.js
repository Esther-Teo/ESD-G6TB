
// console.log(user);
const allListings = document.getElementById('listings');

if (user === 'no'){
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            var books = JSON.parse(this.responseText).listing;
            console.log(books);
            for (const book of books){
                var id = book.Lid;
                var author = book.author;
                var availability = book.availability;
                var description = book.description;
                var isbn = book.isbn;
                var title = book.title;
    
                if (availability === String(1) ){
                    createListings(isbn, author, title, id);
                };
    
            }
            
        }
    }
    request.open("GET", 'database/getAllListings.php', true);
    request.send();
}else{
    var request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if (this.readyState == 4 && this.status == 200){
            var books = JSON.parse(this.responseText).listing;
            console.log(books);
            for (const book of books){
                var id = book.Lid;
                var author = book.author;
                var availability = book.availability;
                var description = book.description;
                var isbn = book.isbn;
                var title = book.title;

                if (availability === String(1) ){
                    createListings(isbn, author, title, id);
                };

            }
            
        }
    }
    request.open("GET", `database/getListingByNonOwner.php?owner_email=${user}`, true);
    request.send();
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
            allListings.appendChild(individualListing);

            
        }
    }
    request.open("GET", `https://www.googleapis.com/books/v1/volumes?q=isbn:${isbn}`, true);
    request.send();
}