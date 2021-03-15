window.onscroll = function() {myFunction()};
var _nav = document.getElementById("nav-bar");

var sticky = _nav.offsetTop;
function myFunction() {
    if(window.pageYOffset >= 0) {
        _nav.classList.add('sticky');
    }else{
        _nav.classList.remove('sticky');
    }
}