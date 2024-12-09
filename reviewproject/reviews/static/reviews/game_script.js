const roomName = JSON.parse(document.getElementById('room-name').textContent);
const layout = JSON.parse(document.getElementById('map_layout').textContent);
const game_socket = new WebSocket('ws://' + window.location.host+ '/ws/game/'+ roomName+ '/');
// const game_socket = new WebSocket('wss://' + window.location.host+ '/ws/game/'+ roomName+ '/');



game_socket.onopen = function() {
    setInterval(() => {
        game_socket.send(JSON.stringify({
            "room":roomName,
        }));
    }, 1000);
    
    // startTimer();
};
game_socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data){
        console.log(data.min);
        console.log(data.sc);
        document.getElementById("minutes").innerHTML = data.min.toString().padStart(2,"0");
        document.getElementById("seconds").innerHTML = data.sc.toString().padStart(2,"0");
        const leaderboard_div = document.getElementById("user_leaders");
        leaderboard_div.innerHTML ="";
        for (let i = 0 ; i < data.leader_user.length; i++ ) {
            const user = document.createElement("div");
            let place = i + 1;
            user.textContent = `    ${place}. ${data.leader_user[i]} : ${data.leader_time[i]}`
            leaderboard_div.appendChild(user)
        }
    }
    if (data.correct && data.redirect) {
    window.location.href = "/completed_screen"; 
    }else if (data.correct === false) {
        alert("Incorrect solution. The puzzle will reset.");
        //resetGame();
    }
    console.log(data)
    console.log(layout)
}
  //for reset functionality. must be fixed 
//function resetGame(){
    //document.getElementById("pin-bar").innerText = "Your Path: (Select pins to build your sequence)"; 
    //pinSequence = [];
    //selectPin();
//}


game_socket.onclose = function(e) {
    console.error('Socket closed unexpectedly');
};


document.getElementById("submit").onclick = function(e) {
    const solution = pinSequence.join(",");  
    console.log("Submitting solution: ", solution);
         
    game_socket.send(JSON.stringify({
        "solution": solution,
        "room": roomName,
    }));
};

let pinSequence = [];
function selectPin(pinID) {
    if (!pinSequence.includes(pinID)) {
        pinSequence.push(pinID);
        updatePinBar(pinSequence);
    }
}

function updatePinBar(sequence) {
    const pinBar = document.getElementById("pin-bar");
    pinBar.textContent = `Your Path: ${sequence.join(" → ")}`;
}
const resetButton = document.getElementById("reset-button");
resetButton.addEventListener("click", function () {
        pinSequence = [];
        updatePinBar(pinSequence);
    });
