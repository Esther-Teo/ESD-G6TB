<?php
    session_start();
    if (isset($_SESSION["user"])){
        $user = $_SESSION['user'];
        $logged_In = true;
    }else{
        $logged_In = false;
        $user = null;
    }
    
    //require_once("protect.php"); //redirect to log in page since this is for logged in users to list
?> 

<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">


        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://use.fontawesome.com/a64b47fd82.js"></script>
        <link rel="stylesheet" href="css/homeresponsive.css">
        <link rel="stylesheet" href="css/individualListing.css">
        <link rel="stylesheet" href="css/testHome.css">

        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500&display=swap" rel="stylesheet"> 
        <link rel="stylesheet" href="https://unpkg.com/swiper/swiper-bundle.css">

        <style>
            .swiper-slide {
                height: auto;
                }
            .btn-secondary{
                border-color: #6c757d;
                border-radius: .25rem;
                padding: .375rem .75rem;
                border-left: 0;
            }
        </style>



    </head>
    <body class="body1" onload="clickSearchIcon()">

    <nav class="navbar navbar-expand-lg navbar-dark bg-light" id="test1">
          <a class="navbar-brand" href="index.html">Re-Zero</a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon" style="color: white;"></span>
          </button>
          <div class="collapse navbar-collapse " id="navbarNav">
            <ul class="navbar-nav ml-auto">
              <li class="nav-item active">
                <button type="button" class="btn btn-linkNav" style="margin-top: 15px; padding-top:12px;" onclick="toggleSearch()"></button>
              </li>
              <li class="nav-item active">
                <a class="nav-link" href="index.html">Home</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="allListings.html">Browse</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="about.html">About</a>
              </li>
          <?php 
            //Displays different buttons depending on user session status (whether user is logged in or not)
            if ( !isset($_SESSION["user"]) ) {
              echo "
              <li class='nav-item'>
                <a class='nav-link' href='loginPage.html' id='login'>Log In</a>
              </li>
              <li class='nav-item'>
                <a class='nav-link' href='registerPage.html' id='signup'>Sign Up</a>
              </li>
              ";
            }
            else{
              echo "
              <li class='nav-item'>
              <a class='nav-link' href='myCurrentListings.html'>Profile</a>
              </li>  
              <li class='nav-item'>
                <a class='nav-link' href='logout.php' id='login'>Log Out</a>
              </li>
              ";
            }
          ?>
    
              
            </ul>
          </div>
        </nav>
        
        <!-- SearchBar -->
        <section id="searchBar" class="search-bar">
          <div class="container mt-0">
            <div class="row">
              <div class="col-lg-10 mx-auto">
                  <form action="searched.php" method="POST" name='form6'>
                  <div class="p-1 bg-light shadow-sm">
                    <div class="input-group">
                      <input id='user_input' type="search" name="user_input" placeholder="Search based on title, genre, author" class="form-control border-0 bg-light">
                      <div class="input-group-append" name='form5'>
                        <!-- Button -->
                        <div class="btn-group">
                          <button id='laopuo' type="button" name="form" class="btn btn-secondary dropdown-toggle smallscreen" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Title</button>
                          <div class="dropdown-menu">
                            <option class="dropdown-item" id="book" name="Title" value="book" onclick="ChangeDropDownBox('Title')" selected>Title</option>
                            <option class="dropdown-item" id="author" name="Author" value="author" onclick="ChangeDropDownBox('Author')">Author</option>
                            <option class="dropdown-item" id="genre" name="Genre" value="genre" onclick="ChangeDropDownBox('Genre')">Genre</option>
                            <option class="dropdown-item" id="user" name="User" value="user" onclick="ChangeDropDownBox('User')">User</option> 
                          </div>
                        </div>
                        <div class="input-group-append">
                          <button id="submit"  class="btn btn-link"><a  class="searchIcon"></a></button>
                        </div>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </section>
        
        <div class="overlay-listing d-flex justify-content-center  pb-5" >
            <div class='container-fluid row pt-5 pb-5' >
                <div class="col-lg-5 text-center container-fluid " id='left'>
                    <div class="swiper-container" style="cursor: pointer">
                        <div class="swiper-wrapper" id='swiper'>
                        </div>
                        <!-- Add Pagination -->
                        <div class="swiper-pagination"></div>
                        <!-- Add Pagination -->
                        <div class="swiper-button-next"></div>
                        <div class="swiper-button-prev"></div>
                    </div>
                    <!-- <div id='title'></div>  -->
                </div>
                <div class="col-lg-7 text-center mt-3 " id='right'>
                </div>
            </div>
        </div>

        <?php
            $listing = $_GET['listingID'];
        ?>
        <script src="js/homeui.js"></script>

        <script> var id = "<?=$listing ?>"; </script>
        <script> var loggedIn = "<?=$logged_In ?>"; </script>
        <script> var $user = "<?=$user ?>"; </script>

        <script>
          document.getElementById('submit').addEventListener('click',function(event) {
            event.preventDefault();
            let dropdownform = document.getElementById('laopuo').innerText
            let text = document.getElementById('user_input').value
            window.location = `searched.php?user_input=${text}&user_searched_option=${dropdownform}`
          })
        </script>

        <script src="https://unpkg.com/swiper/swiper-bundle.js"></script>
        <script src='js/fetchListing.js'></script>
        <script type="text/javascript" src="//code.jquery.com/jquery-1.11.0.min.js"></script>
        <script type="text/javascript" src="//code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <!-- <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>     -->
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>

    </body>
</html>