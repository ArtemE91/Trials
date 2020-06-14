
// get url_create - получаем форму создания объекта
// post url_create - отправляем форму на создание объекта
// get url_list - получаем форму списка объектов
//  model - модель объекта (например, type или material)
function ajax_get_modal(url_create, url_list, model){
    $.ajax({
        url: url_create,
        type: 'get',
        success: function(data)
        { // Получили форму модального окна
            $(data)
                .modal({
                    onApprove : function () { // Ставим обработчик на кнопку сохранить
                    ajax_post_modal(url_create, url_list, model);
                },
            })
            .modal('show');
        }
    });
}

function ajax_post_modal(url_create, url_list, model){
    let form = $('#id_' + model + '_form').serialize(); // Введенные данные в модальное окно
    $.ajax({
        url: url_create,
        type: 'post',
        data: form,
        success: function(data)
        {
            let pk_object = data['pk']; // Primary key созданного объекта
            if (pk_object){
                // Делаем видимым message что объект создан
                $('#id_message_' + model + '_success').attr('class', 'ui success message visible');
                ajax_get_list_object(url_list, model);
            }
        }
    });
}

function ajax_get_list_object(url_list, model){ // Получаемый новый список объектов
    $.ajax({
        url: url_list,
        type: 'get',
        success: function(data)
        {
            $('#id_' + model + '_field').remove(); // Удаляем старый список объектов
            $(data).appendTo($('#id_block_' + model)); // Вставляем новый список объектов
            $('#id_' + model + '_modal').remove(); // удаляем модальное окно из кеша semantic
        }
    });
}
