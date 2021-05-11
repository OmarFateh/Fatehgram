// ajax passwords validation
$(document).ready(function () {    
    $(document).on("keyup", ".js-validate-password1 , .js-validate-password2", function () {
        var password1 = document.getElementById('id_password1').value;
        var password2 = document.getElementById('id_password2').value;
        
        if (password1 && password2) {
            if (password1 != password2) {
                $('.js-validate-password1-error').text("The two passwords don't match.").show()
                $('#submit-btn').attr('disabled', 'disabled');
            }
            else {
                $('.js-validate-password1-error').hide();
                $('#submit-btn').removeAttr('disabled');
            }
        }
        else {
            $('.js-validate-password1-error').hide();
            $('#submit-btn').removeAttr('disabled');
        }
    });
})