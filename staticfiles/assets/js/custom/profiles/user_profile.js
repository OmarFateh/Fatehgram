$(document).ready(function () {
    // Profile Tabs 
    $('.tabgroup > div').hide();
    $('.tabgroup > div:first-of-type').show();
    $('.tabs a').click(function (e) {
        e.preventDefault();
        var $this = $(this),
            tabgroup = '#' + $this.parents('.tabs').data('tabgroup'),
            others = $this.closest('li').siblings().children('a'),
            target = $this.attr('href');
        others.removeClass('active');
        $this.addClass('active');
        $(tabgroup).children('div').hide();
        $(target).show();
    })

    // Load Modal
    var loadForm = function (btn) {
        $.ajax({
            url: btn.attr('data-href'),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#modal-profile").modal("show");
            },
            success: function (data) {
                $("#modal-profile .modal-content").html(data.html_data);
            }
        });
    };

    // ajax edit profile 
    $(document).on("click", ".edit-profile", function (e) {
        loadForm($(this));
    })

    $(document).on("submit", "#updateProfile", function (e) {
        e.preventDefault();
        var form = $(this);
        var fd = new FormData(this);
        $.ajax({
            url: form.attr("action"),
            data: fd,
            type: form.attr("method"),
            dataType: 'json',
            processData: false,
            contentType: false,
            success: function (data) {
                if (data.form_is_valid) {
                    $('.profile-detail').html(data.partial_profile_update);
                    $("#modal-profile").modal("hide");
                }
                else {
                    $("#modal-profile .modal-content").html(data.html_data);
                }
            }
        });
        return false;
    });

    // ajax profile followers 
    $(document).on("click", ".profile-followers", function (e) {
        loadForm($(this));
    })

    // ajax profile following
    $(document).on("click", ".profile-following", function (e) {
        loadForm($(this));
    })

})    