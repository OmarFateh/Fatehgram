$(document).ready(function () {
    // jquery reply list button
    $(document).on('click', '.reply-btn', function (event) {
        event.preventDefault();
        var replyCount = $(this).find('.btn-reply').attr('value');
        if (replyCount > '0') {
            $(this).parent().parent().next('.comment-reply').fadeToggle();
            $(this).find('.btn-reply').toggleClass('replyHidden');
            if ($(this).find('.btn-reply').hasClass('replyHidden')) {
                $(this).find('.btn-reply').text('View replies ' + '(' + replyCount + ')');
            } else {
                $(this).find('.btn-reply').text('Hide replies');
            }
        }
        else {
            $(this).find('.btn-reply').text('');
        }
    });

    // jquery reply button
    $(document).on('click', '.reply-btn-form', function (event) {
        event.preventDefault();
        $(this).parent().parent().next().next('.comment-reply-form').fadeToggle();
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
    
    // ajax edit item
    $(document).on("click", ".edit-item", function (e) {
        loadForm($(this));
    })
    
    $(document).on("submit", "#updateItem", function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.edit_item_form_is_valid) {
                    $('.add_comment_form').html(data.comment_form);
                    $('.item_caption').html(data.item_caption);
                    $('.item-tags-icon').html(data.item_tags_icon);
                    $(".modal-item").modal("hide");
                }
                else {
                    $(".modal-item .modal-content").html(data.html_data);
                }
            }
        });
        return false;
    });
    
    // ajax delete item
    $(document).on("click", ".delete-item", function (e) {
        loadForm($(this));
    })
    
    // ajax item tags
    $(document).on("click", ".explore-top-tags", function (e) {
        loadForm($(this));
    })	
    
    // ajax item likes modal display	
    $(document).on("click", ".modal-one", function (e) {
        loadForm($(this));
    })
    
    // ajax comment likes modal display	
    $(document).on("click", ".modal-comment-like", function (e) {
        loadForm($(this));
    })
    
    // ajax like button 
    $(document).on('click', '.modal-like', function (e) {
        e.preventDefault();
        var icon = $(this).find('i');
        var likeUrl = $(this).attr('data-href');
        var likesCount = $('.modal-one');

        $.ajax({
            type: 'GET',
            url: likeUrl,
            dataType: 'json',
            success: function (data) {
                if (data.liked) {
                    icon.addClass('fa fa-heart');
                    if (data.likes_count == '1') {
                        likesCount.text(data.likes_count + ' like')
                    }
                    else if (data.likes_count == '0') {
                        likesCount.text('')
                    }
                    else {
                        likesCount.text(data.likes_count + ' likes')
                    }
                } else {
                    icon.removeClass('fa fa-heart');
                    icon.addClass('far fa-heart');
                    if (data.likes_count == '1') {
                        likesCount.text(data.likes_count + ' like')
                    }
                    else if (data.likes_count == '0') {
                        likesCount.text('')
                    }
                    else {
                        likesCount.text(data.likes_count + ' likes')
                    }
                }
            },
        });
    });

    // ajax comment 
    $(document).on('submit', '.comment_form', function (e) {
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            dataType: 'json',
            success: function (data) {
                $('.add_comment_form').html(data.comment_form);
                $('.partial_comment_list').html(data.partial_comment_list);
                $('.comment_count').html(data.comment_count);
                $('textarea').val('');
            },
        });
    });

    // ajax comment like button 
    $(document).on('click', '.comment-like', function (e) {
        e.preventDefault();
        var icon = $(this).find('i');
        var likeUrl = $(this).attr('data-href');
        var commentId = $(this).attr('value');
        var likesCount = $('.modal-comment-like' + commentId);

        $.ajax({
            type: 'GET',
            url: likeUrl,
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
                } else {
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
            },
        });
    });

    // ajax edit comment 
    $(document).on("click", ".edit-comment", function (e) {
        loadForm($(this));
    })	

    $(".modal-item").on("submit", ".updateComment", function (e) {
        e.preventDefault();
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.edit_comment_form_is_valid) {
                    $('.partial_comment_list').html(data.partial_comment_list);
                    $(".modal-item").modal("hide");
                }
                else {
                    $(".modal-item .modal-content").html(data.html_data);
                }
            }
        });
    });
    
    // ajax delete comment 	
    $(document).on("click", ".delete-comment", function (e) {
        loadForm($(this));
    })
    
    $(".modal-item").on("submit", ".DeletComment", function (e) {
        e.preventDefault();
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if (data.delete_comment_form_is_valid) {
                    $(".partial_comment_list").html(data.partial_comment_list);
                    $(".comment_count").html(data.comment_count);
                    $(".modal-delete-comment").modal("hide");
                }
                else {
                    $(".modal-delete-comment .modal-content").html(data.html_data);
                }
            }
        });
    });
})