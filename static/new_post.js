/**
 * Created by Andy on 4/20/2016.

var socket = io();

$('#usr_post_m').on('submit', function(event) {

    event.preventDefault();
    var button = $('user_submit_post');

    var state = button.attr('data-state');
    if (state == 'waiting') {
        console.log('request in progress, dropping second click');
        return;
    }
    button.text('Waiting...');
    button.attr('data-state', 'waiting');
    $.ajax('/keet/send', {
        method: 'POST',
        data: {
            initiator: authUser,
            _csrf_token: csrfToken
        },
        success: function(result) {
            console.log('Submitted post.');
            button.text('Post!');
            button.attr('data-state', state);
            addPost(result);
        },
        error: function() {
            console.log('Post failed.');
            button.text('Post!');
            button.attr('data-state', state);
        }
    });
});

// Global mustache template for posts.
var postTmpl = '<div class="user_recent_msgs_content"><div class="user_recent_msgs_photo">{% if photo %} <img class="photo" src="{{ url_for("post_user_photo", login=message.sender) }}" height="64" width="64">{% endif %}{% if not photo %} <a class="photo" href="/"><img src="/static/stock.png" height="64" width="64"></a>{% endif %} </div> <div class="user_recent_msgs_details"> <h3><a href="/u/{{ message.sender}}">{{ message.sender}}</a></h3> <h6>{{ message.time_stamp }}</h6> </div> <p>{{ message.message }}</p>{% if message.photo %} <img class="user_post_image" src="{{ url_for("post_photo", message_id=message.id) }}" height="200"width=200 align="center">{% endif %}</div>'
// Adds new post to top of timeline.
function addPost(post) {
    var msg = Mustache.render(postTmpl, post);
    console.log('generated HTML: %s', msg);
    $('#index_list_posts').prepend(msg);
}




function sendMessage(recip, button) {
    // make sure we don't send on a disabled button
    if (button.attr('disabled')) return;

    // we send a new Hai
    $.ajax('/keet/send', {
        data: {
            initiator: authUser,
            recipient: recip,
            _csrf_token: csrfToken
        },
        method: 'POST',
        success: function(response) {
            button.removeClass('pending');
            addpost(response, postTmpl);
        },
        error: function(err) {
            button.removeClass('pending');
            button.addClass('failed');
        }
    });
    button.addClass('pending');
}

var postTmpl = '<div class="user_recent_msgs_content"><div class="user_recent_msgs_photo">{% if photo %} <img class="photo" src="{{ url_for("post_user_photo", login=message.sender) }}" height="64" width="64">{% endif %}{% if not photo %} <a class="photo" href="/"><img src="/static/stock.png" height="64" width="64"></a>{% endif %} </div> <div class="user_recent_msgs_details"> <h3><a href="/u/{{ message.sender}}">{{ message.sender}}</a></h3> <h6>{{ message.time_stamp }}</h6> </div> <p>{{ message.message }}</p>{% if message.photo %} <img class="user_post_image" src="{{ url_for("post_photo", message_id=message.id) }}" height="200"width=200 align="center">{% endif %}</div>'

function addpost(keet, tmpl) {
    // combine template with hai data to make HTML
    var msg = Mustache.render(tmpl, keet);
    console.log('generated HTML: %s', msg);
    // add HTML to timeline
    $('#index_list_posts').prepend(msg);
    // register handler on new click button
    // only register it on the new thing we built!
    $('#msg-' + keet.message_id + ' .user_submit_post').on('click', onReply)
}


function onReply() {
    // find the user ID we're replying to from the surrounding element
    var recipient = $(this).parent().attr('data-sender');
    // and send them a message
    sendMessage(recipient, $(this));
}

$('.user_post .user_submit_post').on('click', onReply);

$(window).load(function() {
    // when everything is loaded, let's grab the socket
    var socket = io();
    console.log('connected to socket');
    socket.on('hai', function(msg) {
        // we received a message!
        console.log('received new hai from %s', msg.sender.name);
        addHai(msg, recvTmpl);
    });
});*/


$(document).ready(function() {
    $('#user_post_msg').submit(function(event) {
        event.preventDefault(); // Prevents form from automatically sending POST request
        console.log('Clicked post button.');
        var button = $('#post-button');
        var state = button.attr('data-state');
        if (state == 'waiting') {
            console.log('request in progress, dropping second click');
            return;
        }
        button.text('Waiting...');
        button.attr('data-state', 'waiting');
        $.ajax('/api/post', {
            method: 'POST',
            data: {
                recipient: recip,
                _csrf_token: csrfToken
            },
            success: function(result) {
                console.log('Submitted post.');
                button.text('Post!');
                button.attr('data-state', state);
                addPost(result);
            },
            error: function() {
                console.log('Post failed.');
                button.text('Post!');
                button.attr('data-state', state);
            }
         });
    });

    // Global mustache template for posts.
    var postTmpl = '<div class="user_recent_msgs_content"><div class="user_recent_msgs_photo">{% if photo %} <img class="photo" src="{{ url_for("post_user_photo", login=message.sender) }}" height="64" width="64">{% endif %}{% if not photo %} <a class="photo" href="/"><img src="/static/stock.png" height="64" width="64"></a>{% endif %} </div> <div class="user_recent_msgs_details"> <h3><a href="/u/{{ message.sender}}">{{ message.sender}}</a></h3> <h6>{{ message.time_stamp }}</h6> </div> <p>{{ message.message }}</p>{% if message.photo %} <img class="user_post_image" src="{{ url_for("post_photo", message_id=message.id) }}" height="200"width=200 align="center">{% endif %}</div>'

    // Adds new post to top of timeline.
    function addPost(post) {
        var postElt = Mustache.render(postTmpl, post);
        console.log('generated HTML: %s', postElt);
        $('#index_list_posts').prepend(postElt);
    }
});