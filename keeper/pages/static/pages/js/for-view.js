$(document).ready(function() {
    const elementsArray = Array.from(document.querySelectorAll('[id^="keeper-"]'));
    console.log(elementsArray);
    var token = $('input[name="csrfmiddlewaretoken"]').attr('value');
    elementsArray.forEach((element) => {
        const fullId = element.id;
        const parts = fullId.split('-');
        const search_object = parts[1];
        console.log(search_object);
        $.ajax({
            type: "GET",
            url: 'get_keeper_object/',
            data: {'search_object': search_object}
        })
        .done(function(response) {
            setTimeout(() => {
                $('#spinner-' + search_object).attr('hidden', true);
                $('#' + fullId).append(response);
                }, 250);
        });
    });
});