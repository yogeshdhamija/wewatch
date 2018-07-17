function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

function parseTornadoSignedCookie(signed_cookie){
    var pieces = signed_cookie.split("|");
    var b64_piece = pieces[pieces.length - 2].split(":")[1];
    return atob(b64_piece);
}
