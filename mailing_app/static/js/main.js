setInterval(function () {    
    document.getElementById("subject").value = document.getElementById("subject_tmp").value;
    document.getElementById("subject_file").value = document.getElementById("subject_tmp").value;
    document.getElementById("msg").value = document.getElementById("editor").firstChild.innerHTML;       
}, 250);

function uploadForm() {
    document.getElementById("upload-form").style.display = "block"; 
}

function hideUploadForm() {
    document.getElementById("upload-inner-form").setAttribute('novalidate', true);
    // Also valid if <form ... name="upload-inner-form" ... >
    // document.forms["upload-inner-form"].setAttribute('novalidate', true);
    document.getElementById("upload-form").style.display = "hidden";
}

function test() {
    document.getElementById("msg-preview").value="<html><head><style>* {color: red;}</style></head><body><h1>Test mail</h1></body></html>";
}