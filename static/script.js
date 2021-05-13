var seconds = 0;
var player = "test_user_" + Math.floor(Math.random() * 1000000);

function connect(event) {
    var timer = startTimer()

    ws = new WebSocket("ws://0.0.0.0:8000/queue?user=" + player);
    addMessageToMessages(player + " has entered the queue.")

    ws.onmessage = function (event) {
        clearInterval(timer)
        addMessageToMessages("Found a game after " + seconds + " seconds.")
        var jsonObject = JSON.parse(event.data)
        addMessageToMessages(jsonObject.player_1 + " will be facing " + jsonObject.player_2 + " in room " + jsonObject.room_id + ".")


        setTimeout(simulateMatch, 2500, jsonObject.player_1, jsonObject.player_2)
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
    seconds = 0
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

    if (player === player_1) {
        var data = {
            winner: player_1,
            loser: player_2
        };

        var json = JSON.stringify(data);

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "http://0.0.0.0:8000/game");
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(json);
    }
}