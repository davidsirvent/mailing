setInterval(function () {    
    document.getElementById("subject").value = document.getElementById("subject_tmp").value;
    document.getElementById("msg").value = document.getElementById("editor").firstChild.innerHTML;
}, 250);