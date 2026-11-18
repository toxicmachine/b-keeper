$(document).ready(function() {
    $('#folder_search').submit(function(event) {
        event.preventDefault();
        $('#spinner-one').attr('hidden', false);
        document.getElementById('add_keeper_object').innerHTML = "";
        search_folder = document.querySelector("#search_input").value;
        $.ajax({
            type: "GET",
            url: 'check_is_folder_exist/',
            data: {'search_folder': search_folder}
        })
        .done(function(response) {
            setTimeout(() => {
                $('#spinner-one').attr('hidden', true);
                $('#add_keeper_object').append(response);
                $('#add_keeper_object').attr('hidden', false);
                }, 250);
        });
    });
    let based_type;
    let initialRadio = document.querySelector('.btn-group input[type="radio"][checked]');
    if (initialRadio) {
        based_type = initialRadio.id.split('-')[1];
    }
    $('#add_keeper_object').on('change', '.btn-group input[type="radio"]', function(event) {
        if (this.checked) {
            based_type = this.id.split('-')[1];
            if (based_type === '3') {
                $('#changeable_but').prop('checked', false); // снимаем выделение
                $('#changeable_but').prop('disabled', true); // запрещаем изменять
            } else {
                $('#changeable_but').prop('checked', true); // снимаем выделение
                $('#changeable_but').prop('disabled', false); // разрешаем изменять
            }
        }
    });
    $('#add_keeper_object').on('click', '#add_object', function(event) {
        $('#spinner-add').attr('hidden', false);
        $('#add_object').attr('disabled', true);
        var token = $('input[name="csrfmiddlewaretoken"]').attr('value');
        var full_path = document.getElementById('full_path').innerText;
        var name_object = document.getElementById('name_object').value;
        var changeable_but = document.getElementById("changeable_but").checked;
        if (based_type === '3') {
            changeable_but = false;
        };
        $.ajax({
            type: 'POST',
            url: 'add_object_in_keeper/',
            headers: {'X-CSRFToken': token},
            data: JSON.stringify({
                'full_path': full_path,
                'name_object': name_object,
                'based_type': based_type,
                'changeable': changeable_but,
            }),
            cache: false,
            contentType: 'application/json',
            processData: false,
            success: function(response) {
                if (response.success) {
                    setTimeout(() => {
                         console.log('ok');
                         $('#spinner-add').attr('hidden', true);
                         $('#add_object').attr('disabled', false);
                         $('#add_table').attr('hidden', true);
                         $('#success-message').attr('hidden', true);
                         $('#success-message-end').attr('hidden', false);
                    }, 250);
                } else {
                }
            },
            error: function(response) {
               // Do something on error
            }
        });
//        $.ajax({
//            type: 'POST',
//            url: 'add_object_in_keeper/',
//            data: {'full_path': full_path,
//                   'name_object': name_object,
//                   'based_type': based_type,
//                   'changeable': changeable_but,
//                   'csrfmiddlewaretoken': token,
//                                 },
//            dataType: 'json',
//            success: function(response) {
//                if (response.success) {
//                    setTimeout(() => {
//                         console.log('ok');
//                         $('#spinner-add').attr('hidden', true);
//                         $('#add_object').attr('disabled', false);
//                         $('#add_table').attr('hidden', true);
//                         $('#success-message').attr('hidden', true);
//                         $('#success-message-end').attr('hidden', false);
//                    }, 250);
//                } else {
//                }
//            },
//            error: function(response) {
//               // Do something on error
//            }
//        });
    });
});