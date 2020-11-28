setInterval(function () {    
    document.getElementById("subject").value = document.getElementById("subject_tmp").value;
    document.getElementById("msg").value = document.getElementById("editor").firstChild.innerHTML;    
}, 250);


function print() {
    window.print();
}

function waiting() {
    document.getElementById("centerbox-shadow").style.display = "block";
}

