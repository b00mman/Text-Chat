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
    const event = {type: "message", text: message}
    websocket.send(JSON.stringify(event))
}

function init(websocket){
    websocket.addEventListener("message",({ data }) => {
        const event = JSON.parse(data);
        document.querySelector(".messages").innerHTML += event.text;
    });
}

window.addEventListener("DOMContentLoaded", () => {
    const websocket = new WebSocket("ws://192.168.86.157:8001");
    websocket.onopen = () => {
        init(websocket);
        takeInput(websocket);
        const event = {type: "fetch"};
        websocket.send(JSON.stringify(event));
    }
});