function sendMessage(){

    let message = document.getElementById("message").value;

    let chatBox = document.getElementById("chat-box");

    chatBox.innerHTML += "<p>" + message + "</p>";

    document.getElementById("message").value = "";
}