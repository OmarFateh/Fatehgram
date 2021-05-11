$(document).ready(function () {
    // ajax emails validation
    $(document).on("keyup", ".js-validate-email , .js-validate-email2", function () {
        var email1 = document.getElementById('id_email').value;
        var email2 = document.getElementById('id_email2').value;
        
        if (email1 && email2) {
            if (email1 != email2) {
                $('.js-validate-email1-error').text("The two emails don't match.").show()
                $('#submit-btn').attr('disabled', 'disabled');
            }
            else {
                $('.js-validate-email1-error').hide();
                $('#submit-btn').removeAttr('disabled');
            }
        }
        else {
            $('.js-validate-email1-error').hide();
            $('#submit-btn').removeAttr('disabled');
        }
    });
})    