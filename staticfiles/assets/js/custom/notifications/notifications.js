$(document).ready(function () {
    // Save Form
    var saveForm = function (form) {
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                $('.partial_notifications').html(data.partial_notifications);
            }
        });
        return false;
    };

    // accept invitation
    $(document).on("submit", "#acceptInvitation", function (e) {
        e.preventDefault();
        saveForm($(this));
    })
    
    // delete invitation
    $(document).on("submit", "#deleteInvitation", function (e) {
        e.preventDefault();
        saveForm($(this));
    })

})