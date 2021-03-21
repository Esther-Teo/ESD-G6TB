<?php
// clear session data when user clicks on logout button, then redirects to homepage

    //$_SESSION = []; This only clears the session in this page for some reason
    // $_SESSION["user"] = null;
    // $_SESSION = array();
    // session_destroy();

    session_unset();
    session_destroy();
    session_write_close();
    setcookie(session_name(),'',0,'/'); //clears cookies so the user email isn't retrieved again even after logout
    session_regenerate_id(true);

    header("Location:index.html");

    exit();

?>