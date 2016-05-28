/**
 * Created by Justin on 4/18/2016.
 */
$(window).on('load', function() {
    console.log('the page is loaded');
});


$('.user_follow_button').on('click', function() {
    console.log('follow/un-follow was clicked');
    var state = $(this).attr('data-state');

    if (state == "False")
        $.ajax('/api/follow', {
            method: 'POST',
            data: {
                follower: $('.js_follow').attr('data-g'),
                user: $('.js_follow').attr('data-user'),
                _csrf_token: csrfToken
            },
            success: function(data) {
                /* called when post succeeds */
                $(".user_follow_button").attr('data-state',"True");
                $( "button.user_follow_button" ).text("Click to Un-Follow");
                console.log('post succeeded with result %s', data.result);
                // Jquery text editor!!!!

            },
            error: function() {
                /* called when post fails */
                console.error('post failed');
            }
        });
    else if (state == "True")
        $.ajax('/api/unfollow', {
            method: 'POST',
            data: {
                follower: $('.js_follow').attr('data-g'),
                user: $('.js_follow').attr('data-user'),
                _csrf_token: csrfToken
            },
            success: function(data) {
                $(".user_follow_button").attr('data-state',"False");
                $( "button.user_follow_button" ).text("Click to Follow");
                console.log('post succeeded with result %s', data.result);
            },
            error: function() {
                console.error('post failed');
            }
        });
    else
        console.log('SOME KIND OF HORRIBLE ERROR WHERE LOGIC FAILS')
});
