var selections;
$("#system").mousedown(function(e) {
    selections = $(this).val();

}).click(function() {

    if (selections == null) {
        var selected = -1;
        selections = [];
    } else
        var selected = selections.indexOf($.isArray($(this).val()) ? $(this).val()[$(this).val().length - 1] : $(this).val());

    if (selected >= 0)
        selections.splice(selected, 1);
    else
        selections.push($(this).val()[0]);

    $('#system option').each(function() {
        $(this).prop('selected', selections.indexOf($(this).val()) >= 0);
    });
});