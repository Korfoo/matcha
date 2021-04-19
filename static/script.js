var ws = null;
function connect(event) {
    var user = document.getElementById("id")
    ws = new WebSocket("ws://0.0.0.0:8000/queue?user=" + user.value);
    ws.onmessage = function (event) {
        var messages = document.getElementById('messages')
        var message = document.createElement('li')
        var content = document.createTextNode(event.data)
        message.appendChild(content)
        messages.appendChild(message)
    };
    event.preventDefault()
}