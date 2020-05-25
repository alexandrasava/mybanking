
function grabAndSave(currency, amount) {
    $.ajax({
        url: grabAndSaveURL,
        type: 'POST',
        data: {
            currency: currency,
            amount: amount
        },
        success: function (response) {
            if (response.success == false) {
                alert(response.error);
                return;
            }
            
            location.replace(listExchangesURL)
        },
        error: function(xhr, status, error) {
            alert("Error: " + xhr.responseJSON.error);
        }
    });
}


$(document).ready(function () {
    $('.create-exchange form').submit(function() {
        var currency = $('.create-exchange form input#currency').val();
        var amount = $('.create-exchange form input#amount').val();

        grabAndSave(currency, amount);
        return false;
    });
});