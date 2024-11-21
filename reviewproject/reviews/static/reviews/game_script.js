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

window.onload = function(){

    let minutes = 0;
    let seconds = 0;
    let  tens = 0;
    let appendMinutes = document.getElementById("minutes");
     let appendSeconds = document.getElementById("seconds");
     let appendTens = document.getElementById("tens");
     let interval;

     const startTimer = () => {
         tens ++;
         if (tens <= 9){
             appendTens.innerHTML = '0'+ tens.toString();
         }
         if (tens>9){
             appendTens.innerHTML = tens.toString();
         }
         if (tens > 99){
              seconds ++;
              appendSeconds.innerHTML = '0' + seconds.toString();
              tens = 0 ;
             appendTens.innerHTML = '00';
         }
         if (seconds > 9){
             appendSeconds.innerHTML = seconds.toString();
         }
         if (seconds > 59){
             minutes ++;
             appendMinutes.innerHTML ='0'+ minutes.toString();
             seconds = 0
             appendSeconds.innerHTML = '00';
         }

     }
}