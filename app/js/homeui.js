$(function(){
    $(".dropdown-item").click(function(){
        var icon_text=$(this).html();
        $(".dropdown-toggle").html(icon_text);
    })
})


function toggleSearch(){
    var x = document.getElementById("searchBar");
    console.log(x);
    if(x.style.display == "none")
    {
        console.log("True");
        
        x.style.display = "initial";
    }
    else
    {
        x.style.display = "none";
    }
}

function clickSearchIcon(){
    x = document.getElementsByClassName("btn-linkNav");
    x[0].click();
}





// function verifyLogin(){
//     if(<%Session["email"] )

//     document.getElementById("signup").style.display = "none";
//     document.getElementById("login").style.display = "none";
// }