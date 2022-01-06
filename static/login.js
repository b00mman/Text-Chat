document.onkeydown = e=>{
    if (e.key === "Enter"){
        e.preventDefault();
        window.location.href = 'chaos.html?user=' + document.getElementById('username').value.replace(" ", "");
    }
}