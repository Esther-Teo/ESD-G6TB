
var userID  = 1;

var get_all_URL = "http://localhost:5001/offerByUser";
// var place_order_URL = "http://localhost:5100/place_order";
function getAllOffers() {
    // on Vue instance created, load the book list
    const response =
        fetch(get_all_URL+`/${userID}`)
            .then(response => response.json())
            .then(data => {
                console.log(response);
                console.log("meep");
                console.log(data)
                if (data.code === 400) {
                    // no book in db
                    message = data.message;
                } else {
                    allElse = ""
                    html = ""
                    for (each in data.offers) {
                        console.log(data.offers[each])
                        offer = data.offers[each]
                        if (offer.status == "pending") {
                            id = offer.assignmentId
                            fetch("http://localhost:5001/assignmentById/"+id)
                            .then(response => response.json())
                            .then(data => {
                                console.log(response);
                                console.log("wahsehhhh");
                                console.log(data)
                                for (each of data) {
                                    console.log(each)
                                }
                            })
                        }
                    }
                        // html += `
                        //     <tr>
                        //     <td>${childName1}</td>
                        //     <td>${primary1}</td>
                        //     <td>${lvl}</td>
                        //     <td>${subj}</td>
                        //     <td>${E_price}</td>
                        //     <td>${preferred_D}</td>
                        //     <td><input type="button" value="Accept" onclick="SomeDeleteRowFunction()" style="border-radius:5px; background-color: rgb(76, 237, 78);"></td>
                        //     <td><input type="button" value="Reject" onclick="SomeDeleteRowFunction()" style="border-radius:5px; background-color: rgb(227, 32, 32);"></td>
                        //     </tr>
                        //     ` 
                    }
                    document.getElementById("offerTable").innerHTML = html
                })
            
            .catch(error => {
                // Errors when calling the service; such as network error, 
                // service offline, etc
                console.log( error);

            });

}

function addBook() {
    // reset data
    this.bookAdded = false;
    this.addBookError = "";

    let jsonData = JSON.stringify({
        title: this.newTitle,
        price: this.newPrice,
        availability: this.newAvailability
    });

    fetch(`${get_all_URL}/${this.newISBN13}`,
        {
            method: "POST",
            headers: {
                "Content-type": "application/json"
            },
            body: jsonData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            result = data.data;
            console.log(result);
            // 3 cases
            switch (data.code) {
                case 201:
                    this.bookAdded = true;

                    // refresh book list
                    this.getAllBooks();

                    // an alternate way is to add this one element into this.books
                    break;
                case 400:
                case 500:
                    this.addBookError = data.message;
                    break;
                default:
                    throw `${data.code}: ${data.message}`;
            }
        })
}
