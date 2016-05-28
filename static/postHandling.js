 var socket = io();

 function scrollChat() {
    // a jQuery result is a list, get the first element
    var chat = $('#messages')[0];
    // figure out the height the *top* of window should scroll to
    var pos = chat.scrollHeight - chat.clientHeight;
    chat.scrollTop = pos;
}


 $('post_messages_js').on('submit', function (event) {

     event.preventDefault();
     var message = $('#message_js').val();
     socket.send(message);
     $('#message_js').val('');
     $('#user_posts').append($('<li>')).addClass('posted').text(message);

 })
socket.on('message', function(message) {
    $('#user_posts').append($('<li>').addClass('received').text(message));
    scrollChat();
});