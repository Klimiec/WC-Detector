$(document).ready(function() {
    setInterval("ajaxd()",1000);
});


function ajaxd() { 
  $.ajax({
    type: "GET",
    url: "http://localhost:8181/toilets",
    dataType: 'json',
   success: function(data){
            if (data.wc1 == 'Free') {
                $('#wc1').attr("class", "success");
                $('#wc1state').text("Free");
                //alert('IF1 - free');  
            } else {
                $('#wc1').attr("class", "danger");
                $('#wc1state').text("Occupied");
                //alert('ELSE - occupied');  
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
   },
    error: function (jqXHR, textStatus, errorThrown ) {
              alert('Error!');  
    }
 });
}


/*
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
        },
        error: function (jqXHR, textStatus, errorThrown ) {
              alert('Error: ' + jqXHR.responseText);  
        }
    });
}
);

*/