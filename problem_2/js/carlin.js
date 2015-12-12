/**
 * Created by jnaylor on 12/11/15.
 */
$(document).ready(function() {

    $('#cleanit-button-one').click(function() {
        $('div.report').empty();
        var json_input_area = $('#json-input-area').val();
        $.ajax({
            url: '/send',
            data: json_input_area,
            success: function(result) {
                var cleaned_data=result.cleaned_data;
                $('div.cleaned').text(cleaned_data);
                result.cleaning_report.forEach(function(line) {
                    var $div = $("<div/>").addClass("report-line").html(line);
                    $('div.report').append($div);
                });
            },
            failure: function(result) {
                console.info("FAILED");
            },
            contentType: "application/json",
            dataType: "json",
            type: 'POST'});
    });

    $('#cleanit-button-two').click(function() {
        console.info("Clicked");
        $('div.report').empty();
        var json_input_area = $('#json-input-area').val();
        $.ajax({
            url: '/send',
            data: json_input_area,
            success: function(result) {
                $('#content').html(result);
            },
            failure: function(result) {
                console.info("FAILED");
            },
            contentType: "application/json",
            dataType: "html",
            type: 'POST'});
    });

});
