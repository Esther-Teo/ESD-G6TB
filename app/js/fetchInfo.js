// fetches the book information by making api calls


const vm = new Vue({
    el: '#search',
    data: {
        isbn : '',
        title: '',
        author: '',
        description: '',
        genre: '',
        showImage: false,
        url: '',
        isbnError: false,
        isbnInvalid: false,
        titleError: false,
        authorError: false,
        descriptionError: false,
        genreError: false,
        errors: [],
        

    },
    methods: {
        getInfo: function(){
            event.preventDefault();
            if (this.isbn === ''){
                this.isbnError = true;
                this.title = '';
                this.description = '';
                this.genre = '';
                this.author = '';
                this.url = '';
                this.showImage = false
                
            }else{
                var ISBN = this.isbn;
                var fill = this.fillInfo;
                var invalid = this.invalidISBN;
                var request = new XMLHttpRequest();
                request.onreadystatechange = function(){
                    if (this.readyState == 4 && this.status == 200){
                        // console.log(JSON.parse(this.responseText).totalItems)
                        var output = JSON.parse(this.responseText).totalItems;
                        if (output === 0){
                            invalid();
                        }else{
                            var data = JSON.parse(this.responseText).items[0].volumeInfo;
                            // console.log(data)
                            var title = data.title;
                            var authors = data.authors;
                            var description = data.description;
                            var genre = data.categories;
                            if (data.hasOwnProperty('imageLinks')){
                                var image = data.imageLinks.thumbnail;
                            }else{
                                var image = 'no image';
                            }
                            fill(title, authors, description, genre, image);
                            
                        }
                    }
                }
                request.open("GET", `https://www.googleapis.com/books/v1/volumes?q=isbn:${ISBN}`, true);
                request.send();
            }
        },
        fillInfo: function(title, authors, description, genre, image){
            this.title = title;
            this.description = description;
            this.genre = genre;
            this.author = authors;
            this.url = image;
            if (image == 'no image'){
                this.showImage = false;
            }else{
                this.showImage = true;
            }

            this.authorError = false;
            this.isbnError = false;
            this.titleError = false;
            this.genreError = false;
            this.descriptionError = false;
            this.isbnInvalid = false;

        },
        showPopUp: function(){
            $('#modalConfirm').modal('show');
            event.preventDefault();
        },
        validateForm: function(){
            showPopUp = this.showPopUp;
              if (!this.author) {
                this.authorError = true;
                event.preventDefault();
              }else{
                  this.authorError = false;
              }
              if (!this.isbn) {
                this.isbnError = true;
                event.preventDefault();
              }else{
                  this.isbnError = false;
              }
              if (!this.title) {
                this.titleError = true;
                event.preventDefault();
              }else{
                  this.titleError = false;
              }
              if (!this.genre) {
                this.genreError = true;
                event.preventDefault();
              }else{
                  this.genreError = false;
              }
              if (!this.description) {
                this.descriptionError = true;
                event.preventDefault();
              }else{
                  this.descriptionError = false;
              }
              if (this.titleError == false && this.authorError == false && this.isbnError == false && this.genreError == false && this.descriptionError == false){
                event.preventDefault();
                showPopUp();  
              }



            //   
        }, 
        invalidISBN: function(){
            this.isbnInvalid = true;
            this.isbnError = false;
            this.title = '';
            this.description = '';
            this.genre = '';
            this.author = '';
            this.url = '';
            this.showImage = false
        }
    }
})