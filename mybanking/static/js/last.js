
function last(currency, number) {
    function getURL() {
        var url = filterExchangesURL.replace('NUMBER', number);
        url = url.replace('CURRENCY', currency);
        return url;
    }
    $.ajax({
        url: getURL(),
        type: 'GET',
        success: function (response) {
            if (response.success == false) {
                alert(response.error);
                return;
            }
            
            var htmlContent = getTableHTMLContent(response.data);
            $("tbody.filter-exchange").html(htmlContent);
        },
        error: function(xhr, status, error) {
            alert("Error: " + xhr.responseJSON.error);
        }
    });
}

function getTableHTMLContent(exchanges) {
    var content = "";
    $.each(exchanges, function (i, exchange) {
        content += '\
            <tr>\
                <td>' + exchange.currency + '</td>\
                <td>' + exchange.amount + '</td>\
                <td>' + exchange.exchange_rate + '</td>\
                <td>' + exchange.amount_usd + '</td>\
            </tr>';
    });
    return content
}

$(document).ready(function () {
    $('form.filter-exchange').submit(function() {
        var currency = $('form.filter-exchange input#currency').val();
        var number = $('form.filter-exchange input#number').val();

        last(currency, number);
        return false;
    });
});