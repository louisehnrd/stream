let socket = io();

let form = document.getElementById('form');
let input = document.getElementById('input');

let imageInput = document.getElementById('image');

/*
form.addEventListener('submit',(event)=>{
    event.preventDefault();

    let message = input.value;
    socket.emit('message',message);

    input.value="";
})
*/

form.addEventListener('submit',(event)=>{
    event.preventDefault();
    let period = input.value;
    console.log(period);
    socket.emit('stream',period);
    input.value="";
})


/*
imageInput.addEventListener('change',(e)=>{
    let file = imageInput.files[0];
    let reader = new FileReader();
    reader.addEventListener('load',()=>{
        socket.emit('image',reader.result);
    })
    reader.readAsDataURL(file);
})
*/

socket.on('streaming_started',function(data){
    console.log(data.video_data);
    //let videoData = new Uint8Array(data.video_data);
    let videoBlob = new Blob([data.video_data],{type:'video/mp4'});
    let videoUrl = URL.createObjectURL(videoBlob);
    //let output = data.output;
    // Manipuler la vidéo ou les images du streaming côté client
    // Par exemple, afficher la vidéo dans un élément <video> HTML
    let videoElement = document.getElementById('video');
    //videoElement.src = URL.createObjectURL(output);
    videoElement.src=videoUrl;
    videoElement.play();
    console.log("chuis la");
    socket.emit('stream',5);
})

socket.on('message',(message)=>{
    let li = document.createElement('li');
    li.textContent=message;
    console.log(li.textContent);
    document.getElementById('messages').prepend(li);
})

socket.on('image',(src,period)=>{
    let li = document.createElement('li');
    let img = document.createElement('img');
    console.log(src);
    img.src = src;
    img.width = 640;
    img.height = 480;
    li.appendChild(img);
    document.getElementById('pic').prepend(li);
    socket.emit('image2',period);
})

socket.on('img',(src,period)=>{
    let li = document.createElement('li');
    let img = document.createElement('img');
    console.log(src);
    img.src = src;
    img.width = 640;
    img.height = 480;
    li.appendChild(img);
    document.getElementById('pic').prepend(li);
    socket.emit('image1',period);
})
















//send a message to the server
/*
socket.on('connect', function() {
socket.emit('message', {data: 'I\'m connected!',reponse : 'Message received!'});
});
//and print the message's server in log and in html
socket.on('message_back', function(msg) {
console.log(msg['data']);
document.getElementById('message-container').innerHTML = msg['data'];
});

socket.on('connect',function(){
    socket.emit('picture',{name:'Untitled.jpeg'});
})
            
socket.on('image',function(data){
    var image_data = data['data'];
    var blob = new Blob([image_data], { type: 'image/jpeg' }); // Remplacez 'image/jpeg' par le type MIME approprié pour votre image
    var imageUrl = URL.createObjectURL(blob);
                
    var imgElement = document.createElement('img');
    imgElement.src = imageUrl;
                
    document.getElementById('image-container').appendChild(imgElement);
    //document.getElementById('image-container').innerHTML = '<img src="' + data_img['data'] + '">';
})

*/
