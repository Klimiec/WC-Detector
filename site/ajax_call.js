$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "http://localhost:8181/toilets",
        dataType: 'json',
        success: function (data) { 

            
            if (data.wc1 == 'Free') {
                $('#wc1').attr("class", "success");
                $('#wc1state').text("Free");
            } else {
                $('#wc1').attr("class", "danger");
                $('#wc1state').text("Occupied");
            }

            if (data.urinal == 'Free') {
                $('#urinal').attr("class", "success");
                $('#urinalstate').text("Free");
            } else {
                $('#urinal').attr("class", "danger");
                $('#urinalstate').text("Occupied");
            }

            if (data.wc2 == 'Free') {
                $('#wc2').attr("class", "success");
                $('#wc2state').text("Free");
            } else {
                $('#wc2').attr("class", "danger");
                $('#wc2state').text("Occupied");
            }



            //alert("OK");
        },
        error: function (jqXHR, textStatus, errorThrown ) {
              alert('Error: ' + jqXHR.responseText);  
        }
    });
});