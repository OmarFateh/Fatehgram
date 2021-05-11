$(document).ready(function () {    
    // item upload & preview 
    $(function () {

        var picture;
        // Viewing Uploaded Picture On Setup Admin Profile
        function livePreviewPicture(picture) {
            if (picture.files && picture.files[0]) {
                var picture_reader = new FileReader();
                picture_reader.onload = function (event) {
                    $('#uploaded').attr('src', event.target.result);
                };
                picture_reader.readAsDataURL(picture.files[0]);
            }
        }

        $('.setup-picture form .picture input').on('change', function () {
            $('#uploaded').fadeIn();
            livePreviewPicture(this);
        });

        // Disable upload button if there's no image.
        $('#upload-item').attr('disabled', true);
        $(document.body).on('keyup change', '#id_image', function () {
            var image = $('#id_image').val();
            if (image != '') {
                $('#upload-item').attr('disabled', false);
            } else {
                $('#upload-item').attr('disabled', true);
            }
        });
    });
})    