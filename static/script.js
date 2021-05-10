var seconds = 0;

function connect(event) {
    var timer = startTimer()

    var player_a = "test_user_" + Math.floor(Math.random() * 1000000);
    var player_b = "test_user_" + Math.floor(Math.random() * 1000000);

    ws_a = new WebSocket("ws://0.0.0.0:8000/queue?user=" + player_a);
    addMessageToMessages(player_a + " has entered the queue.")

    ws_b = new WebSocket("ws://0.0.0.0:8000/queue?user=" + player_b);
    addMessageToMessages(player_b + " has entered the queue.")

    ws_b.onmessage = function (event) {
        clearInterval(timer)

        var jsonObject = JSON.parse(event.data)
        addMessageToMessages(jsonObject.player_1 + " will be facing " + jsonObject.player_2 + " in room " + jsonObject.room_id + ".")
        simulateMatch(jsonObject.player_1, jsonObject.player_2)
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

function simulateMatch(player_1, player_2) {
    addMessageToMessages(player_1 + " has won.")

    var data = {
        winner: player_1,
        loser: player_2
    };

    var json = JSON.stringify(data);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://0.0.0.0:8000/game");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(json);
    addMessageToMessages(xhr.response)
    
}