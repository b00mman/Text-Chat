function takeInput(websocket){
    document.onkeydown = e=>{
        if (e.key === "Enter"){
            e.preventDefault()
            sendMessage(websocket, document.getElementById('message').value);
            document.getElementById('form').reset();
        }
    }
}

async function sendMessage(websocket, message){
    const event = {type: "message", user: user, text: message}
    websocket.send(JSON.stringify(event))
}

function init(websocket){
    websocket.addEventListener("message",({ data }) => {
        const event = JSON.parse(data);
        document.querySelector(".messages").innerHTML += event.user + ": " + event.text + "<br>";
    });
}

window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://localhost:8001");
    const params = new URLSearchParams(window.location.search);
    user = params.get("user");
    if (user === ""){
        user = "Anonymous";
    }
    websocket.onopen = () => {
        init(websocket);
        takeInput(websocket);
        const event = {type: "fetch"};
        websocket.send(JSON.stringify(event));
    }
});