$(document).ready(function () {
    // ajax save button 
    $(document).on('click', '.modal-bookmark', function (e) {
        e.preventDefault();
        var icon = $(this).find('i');

        $.ajax({
            type: 'GET',
            url: $(this).attr('data-href'),
            dataType: 'json',
            success: function (data) {
                if (data.saved) {
                    icon.removeClass('far fa-bookmark');
                    icon.addClass('fas fa-bookmark');
                } else {
                    icon.removeClass('fas fa-bookmark');
                    icon.addClass('far fa-bookmark');
                }
            },
        });
    });
})    