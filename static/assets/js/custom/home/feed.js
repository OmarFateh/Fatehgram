$(document).ready(function () {
    // ajax suggested profiles follow button 
    $(document).on('click', '.suggested-follow', function (e) {
        e.preventDefault();
        var followUrl = $(this).attr('data-href');

        $.ajax({
            type: 'GET',
            url: $(this).attr('data-href'),
            dataType: 'json',
            success: function (data) {
                $('.suggested_profiles').html(data.suggested_profiles);
            }
        });
    });
    
    // Load Modal
    var loadForm = function (btn) {
        $.ajax({
            url: btn.attr('data-href'),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-item").modal("show");
            },
            success: function (data) {
                $("#modal-item .modal-content").html(data.html_data);
            }
        });
    };

    // ajax item tags
    $(document).on("click", ".explore-top-tags", function (e) {
        loadForm($(this));
    })	
    
    // ajax item likes modal display
    $(document).on("click", ".modal-one", function (e) {
        loadForm($(this));
    })	

    // Item Like
    var likeItem = function (btn) {
        var icon = $(".feed-like").find('i');
        var itemId = btn.attr('value');
        var likesCount = $('.count-feed-like' + itemId);

        $.ajax({
            url: btn.attr('data-href'),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                if (data.liked) {
                    icon.addClass('fa fa-heart');
                    if (data.likes_count == '1') {
                        likesCount.show();
                        likesCount.text(data.likes_count + ' like')
                    }
                    else if (data.likes_count == '0') {
                        likesCount.hide();
                        likesCount.text('')
                    }
                    else {
                        likesCount.show();
                        likesCount.text(data.likes_count + ' likes')
                    }
                }
                else {
                    icon.removeClass('fa fa-heart');
                    icon.addClass('far fa-heart');
                    if (data.likes_count == '1') {
                        likesCount.show();
                        likesCount.text(data.likes_count + ' like')
                    }
                    else if (data.likes_count == '0') {
                        likesCount.hide();
                        likesCount.text('')
                    }
                    else {
                        likesCount.show();
                        likesCount.text(data.likes_count + ' likes')
                    }
                }
            }
        });
    };

    // ajax feed item double click like
    $(document).on("dblclick", ".feed-item", function (e) {
        likeItem($(this));
    })	

    // ajax feed item like
    $(document).on("click", ".feed-like", function (e) {
        likeItem($(this));
    })	

})    