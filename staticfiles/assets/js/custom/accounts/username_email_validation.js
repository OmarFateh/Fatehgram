$(document).ready(function () {
    // ajax username validation
    $(document).on("keyup", ".js-validate-username", function () {
        var form = $(this).closest("form");
        $.ajax({
            url: form.attr("data-validate-username-url"),
            data: {username: $(this).val()},
            dataType: 'json',
            success: function (data) {
                if (data.is_username_taken) {
                    $('.js-validate-username-error').text(data.error_message).show()
                    $('#submit-btn').attr('disabled', 'disabled');
                }
                else {
                    $('.js-validate-username-error').hide();
                    $('#submit-btn').removeAttr('disabled');
                }
            }
        });
    });

    // ajax email validation
    $(document).on("keyup", ".js-validate-email", function () {
        var form = $(this).closest("form");
        $.ajax({
            url: form.attr("data-validate-email-url"),
            data: {email: $(this).val()},
            dataType: 'json',
            success: function (data) {
                if (data.is_email_taken) {
                    $('.js-validate-email-error').text(data.error_message).show()
                    $('#submit-btn').attr('disabled', 'disabled');
                }
                else {
                    $('.js-validate-email-error').hide();
                    $('#submit-btn').removeAttr('disabled');
                }
            }
        });
    });
})    