$(document).ready(function () {    
    // ajax follow button 
    $(document).on('click', '.follow', function (event) {
        event.preventDefault();
        var followText = $(this).find('.follow-text');

        $.ajax({
            type: 'GET',
            url: $(this).attr('data-href'),
            dataType: 'json',
            success: function (data) {
                if (data.followed_by) {
                    followText.text('Unfollow')
                    $('.profile-navbar').html(data.profile_navbar);
                }
                else if (data.sent_follow_request) {
                    followText.text('Requested')
                }
                else {
                    followText.text('Follow')
                    $('.profile-navbar').html(data.profile_navbar);
                }
            },
        });
    });

    // ajax modal follow button 
    $(document).on('click', '.modal-follow', function (event) {
        event.preventDefault();
        var followText = $(this).find('.follow-text');

        $.ajax({
            type: 'GET',
            url: $(this).attr('data-href'),
            dataType: 'json',
            success: function (data) {
                if (data.followed_by) {
                    followText.text('Unfollow')
                }
                else if (data.sent_follow_request) {
                    followText.text('Requested')
                }
                else {
                    followText.text('Follow')
                }
            },
        });
    });
})