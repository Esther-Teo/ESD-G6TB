<?php
    session_start();
    //var_dump($_POST['form1']);
    $previous_user_input = $_GET['user_input'];
    $previous_user_option = $_GET['user_searched_option'];
    //var_dump($previous_user_input);
    //var_dump($previous_user_option);
    
?>

<!DOCTYPE html>

<html>
  
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  
        <link rel="stylesheet" href="css/allListings.css">
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        <script src="https://use.fontawesome.com/a64b47fd82.js"></script>
        <link rel="stylesheet" href="css/homeresponsive.css">
        <link rel="stylesheet" href="css/testHome.css">

        <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css"/>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500&display=swap" rel="stylesheet"> 



    </head>
    <body class="body2" onload="clickSearchIcon()" onload= "ChangeDropDownBox('Title')">
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
                <div class="p-1 bg-light shadow-sm">
                  <div class="input-group">
                    <input type="search" onkeyup="get_searched_listings_by_enter(event)" placeholder="Search based on title, genre, author" class="form-control border-0 bg-light" name="user_input" id="user_input">
                    <div class="input-group-append">
                      <!-- Button -->
                      <div class="btn-group" >
                        <button type="button" class="btn btn-secondary dropdown-toggle smallscreen" data-toggle="dropdown" aria-haspopup="true" id="search_option_title">Title</button>
                        <div class="dropdown-menu" id= "drop_down_input" name="drop_down_input">
                          <option class="dropdown-item" id="book" value="book" onclick="ChangeDropDownBox('Title')" selected>Title</option>
                          <option class="dropdown-item" id="author" value="author" onclick="ChangeDropDownBox('Author')">Author</option>
                          <option class="dropdown-item" id="genre" value="genre" onclick="ChangeDropDownBox('Genre')">Genre</option>
                          <option class="dropdown-item" id="user" value="user" onclick="ChangeDropDownBox('User')">User</option>
                        </div>
                      </div>
                      <div class="input-group-append">
                        <button type="submit" id="searched" class="btn btn-link"  onclick="get_searched_listings()"><a class="searchIcon"></a></button>
                      </div>
                    </div>
                  </div>
                </div>
              <!-- </form> -->
            </div>
          </div>
        </div>
      </section>
        <div class="overlay" >
          <h2 class='mt-3 header text-center display-4'><u>Search Results</u></h2>
          <div class='container-fluid row mx-auto pt-5 pb-5' id='listings1'>    
          </div>



        </div>

        <script src="js/homeui.js"></script>
        <script> var user_input = "<?=false?>"; </script>
        <script> var previous_user_input = "<?=$previous_user_input ?>";</script>
        <script> var previous_user_option = "<?=$previous_user_option ?>";</script>
        <script src="js/searched.js"></script>
        <!-- <script type="text/javascript" src="//code.jquery.com/jquery-1.11.0.min.js"></script> -->
        <script type="text/javascript" src="//code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
        
        

      </body>
</html>