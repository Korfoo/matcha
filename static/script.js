var seconds = 0;

function connect(event) {
    var timer = startTimer()

    var player_a = "test_user_" + Math.floor(Math.random() * 1000000);
    var player_b = "test_user_" + Math.floor(Math.random() * 1000000);

    ws_a = new WebSocket("ws://0.0.0.0:8000/queue?user=" + player_a);
    addMessageToMessages(player_a + " has entered the queue.")

    ws_b = new WebSocket("ws://0.0.0.0:8000/queue?user=" + player_b);
    addMessageToMessages(player_b + " has entered the queue.")

    ws_a.onmessage = function (event) {
        addMessageToMessages(event.data)
        // var message = document.createElement('li')
        // var content = document.createTextNode(event.data)
        // message.appendChild(content)
        // messages.appendChild(message)
    };
    ws_b.onmessage = function (event) {
        addMessageToMessages(event.data)
        // var message = document.createElement('li')
        // var content = document.createTextNode(event.data)
        // message.appendChild(content)
        // messages.appendChild(message)
        clearInterval(timer)
    };
    event.preventDefault()
}

function addMessageToMessages(text) {
    var messages = document.getElementById('messages')
    var message = document.createElement('li')
    var content = document.createTextNode(text)
    message.appendChild(content)
    messages.appendChild(message)
}



function startTimer() {
    var el = document.getElementById("timer");
    el.innerText = "Time in queue: " + seconds + " seconds.";

    return setInterval(incrementSeconds, 1000);
}

function incrementSeconds() {
    var el = document.getElementById("timer");

    seconds += 1;
    el.innerText = "Time in queue: " + seconds + " seconds.";
}
