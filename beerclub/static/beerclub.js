
$(function() {

  $('#account_stats').hide();
  $('#account_unique').hide();
  $("#showhide").hide();

  $('#id_name').focus();
  $('#id_barcode').focus();
  $("#id_name").autocomplete({
    source: function( request, response) {
        $.ajax({
            dataType: "json",
            url: "/bc/api/account_search/" + request.term + "/",
            success: function(data) {
                response($.map(data, function(item) {
                    console.log(data);
                    console.log(item);
                    return {
                        label: item.full_name,
                        value: item.id
                    };
                }));
            },
        });
    }, //end source
    minLength: 2,
    select: function (event, ui) {
        console.log(ui.item.value);
        this.value = ui.item.label;
        $('#id_name_pk').val(ui.item.value);
        $.ajax({
            url: "/bc/api/account/" + ui.item.value + "/",
        }).done(function(account) {
            console.log("Render account details");
            console.log(account);
            render_account_stats(account);
        });
        $.ajax({
            url: "/bc/api/account_unique_available/" + ui.item.value + "/",
        }).done(function(uniques) {
            console.log("Render unique details");
            render_account_unique(uniques);
        });
        return false;
    }
  });
  $("#id_payee_name").autocomplete({
    source: function( request, response) {
        $.ajax({
            dataType: "json",
            url: "/bc/api/account_search/" + request.term + "/",
            success: function(data) {
                response($.map(data, function(item) {
                    console.log(data);
                    console.log(item);
                    return {
                        label: item.full_name,
                        value: item.id
                    };
                }));
            },
        });
    }, //end source
    minLength: 2,
    select: function (event, ui) {
        console.log(ui.item.value);
        this.value = ui.item.label;
        $('#id_payee_name_pk').val(ui.item.value);
        return false;
    }
  });
  $("#id_beer").autocomplete({
    source: function( request, response) {
        $.ajax({
            dataType: "json",
            //url: "/bc/api/beer_search_instock/" + request.term + "/",
            url: "/bc/api/beer_search/" + request.term + "/",
            success: function(data) {
                response($.map(data, function(item) {
                    console.log(item);
                    return {
                        label: item.name + " (" + item.container + ", " + item.brewery + ")",
                        special: item.special,
                        value: item.id
                    };
                }));
            },
        });
    },
    minLength: 2,
    select: function (event, ui) {
        this.value = ui.item.label;
        $('#id_beer_pk').val(ui.item.value);
        $('#id_special').prop("checked", ui.item.special);
        $.ajax({
                url: "/bc/api/account_drunk/" + $("#id_name_pk").val() + "/" + ui.item.value + "/",
                //data: { "name": $("#id_name_pk").val(), "beer": $("#id_beer_pk").val() },
            }).done(function(consumed) {
                render_consumed(consumed['result']);
            });
        return false;
        }
    });
    function runEffect() {
        $("#showhide").show( "blind", {}, 100);
    };
    $("#extras").click(function() {
        runEffect();
    });
});

function render_account_stats(account){
    $('#account_had').text(account.had);
    $('#account_unique_had').text(account.unique);
    $('#account_special_had').text(account.special_had);
    $('#account_special_due').text(account.special_due);
    if (account.special_due > 0) {
        $('#account_special_due').css("background-color", "yellow");
    } else {
        $('#account_special_due').css("background-color", "white");
    }
    $('#account_balance').text(account.balance);
    if (account.balance < 0) {
        $('#account_balance').css("background-color", "pink");
    } else {
        $('#account_balance').css("background-color", "white");
    }
    $('#account_stats').show();
}

function render_account_unique(uniques) {
    $("tr").remove("#autogentable");
    //for (key in uniques) {
    //    var beer = uniques[key];
    for (id in uniques) {
        var beer=uniques[id];
        var update = "";
        console.log(beer);
        update += "<tr id=\"autogentable\">";
        if (beer['special']) {
            update += "<td style='background-color: yellow'>" + beer['name'] + "</td>";
        } else {
            update += "<td style='background-color: white'>" + beer['name'] + "</td>";
        }
        update += "<td>" + beer['abvp'] + "</td>";
        update += "<td>" + beer['volume'] + "ml " + beer['container'] + "</td>";
        update += "<td>" + beer['brewery'] + "</td>";
        update += "</tr>";
        $("#account_unique_table tr:last").after(update);
    }
    $('#account_unique').show();
}

function render_consumed(consumed) {
    console.log(consumed);
    if (consumed == true) {
        $("#id_beer").attr("style", "background-color:pink;");
    } else if (consumed == false) {
        $("#id_beer").attr("style", "background-color:lightgreen;");
    } else {
        $("#id_beer").attr("style", "background-color:white;");
    }
}
