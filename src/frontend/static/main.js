function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

function parseSignedCookie(signed_cookie){
    var pieces = signed_cookie.split("|");;
    return pieces[pieces.length - 1].split("\"")[0]
}
