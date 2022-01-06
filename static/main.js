var socket = io({"forceNew": true});

function takeInput(){
    document.onkeydown = e=>{
        if (e.key === "Enter"){
            e.preventDefault();
            sendMessage(document.getElementById('message').value);
            document.getElementById('form').reset();
        }
    }
}

socket.on("connect", function(){
    socket.emit("fetch");
})

function sendMessage(message){
    const event = {user: user, text: message}
    socket.emit("message", JSON.stringify(event))
}

socket.on("message", function (data){
    const event = JSON.parse(data);
    document.querySelector(".messages").innerHTML += event.user + ": " + event.text + "<br>";
})

window.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    user = params.get("user");
    if (user === ""){
        user = "Anonymous";
    }
});