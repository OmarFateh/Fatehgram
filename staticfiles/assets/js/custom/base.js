$(document).ready(function () {
    // slimScroll
    $('#Slim,#Slim2').slimScroll({
        height: "auto",
        position: 'right',
        railVisible: true,
        alwaysVisible: true,
        size: "8px",
    });

    // messages timeout for 5 sec
    setTimeout(function () {
        $('.message').fadeOut('slow');
    }, 5000); // <-- time in milliseconds, 1000 =  1 sec

    // Search profiles by username
    $(document).on("keyup", ".search", function () {
        var search = $(this).val();
        $.ajax({
            url: $('#search-form').attr('data-href'),
            type: 'GET',
            data: { 'search': search },
        })
            .done(function (response) {
                var json_data = JSON.parse(response);
                var div_data = "";
                if (search){
                    if (json_data.length != 0){
                        for (key in json_data) {
                            div_data += "<a href='" + json_data[key]['profile_url'] + "' >";
                            div_data += "<img src='" + json_data[key]['photo'] + "'  alt=''>";
                            div_data += "<span>" + json_data[key]['username'] + "</span>";
                            div_data +="</a>";
                        }
                        $(".custom-search-dropdown").show();
                        $(".custom-search-dropdown").html(div_data);
                    }else {
                        div_data = 'No results found.';
                        $(".custom-search-dropdown").show()
                        $(".custom-search-dropdown").html(div_data);
                    }
                }else {
                        div_data = '';
                        $(".custom-search-dropdown").hide()
                        $(".custom-search-dropdown").html(div_data);
                    }
            })
    }); 	
});