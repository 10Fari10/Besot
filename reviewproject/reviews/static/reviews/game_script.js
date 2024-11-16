const roomName = JSON.parse(document.getElementById('room-name').textContent);
const layout = JSON.parse(document.getElementById('map_layout').textContent);
const game_socket = new WebSocket('ws://' + window.location.host+ '/ws/game/'+ roomName+ '/');

game_socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log(data)
    console.log(layout)
};

game_socket.onclose = function(e) {
    console.error('Socket closed unexpectedly');
};

//text input is placeholder. Remove when pin selection is implemented.
document.getElementById("submit").onclick = function(e) {
    solution = document.getElementById('test').value
    console.log(solution)
    game_socket.send(JSON.stringify({"solution":solution,"room":roomName}));
};