function ajax_experement_create(url_create_experiment){
    $.ajax({
        url: url_create_experiment,
        type: 'get',
        success: function(data)
        { // Получили форму модального окна
            $(data)
                .modal({
                    onApprove : function () { // Ставим обработчик на кнопку сохранить
                    // ajax_post_modal(url_create, url_list, model);
                }
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