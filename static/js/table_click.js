
const select_tr = []; // Выбранные элементы в общей таблице
const check_tr = []; // Выбранные элементы в 'корзине' (таблица с выбранными элементами)
const id_btn_detail = 'id_btn_detail'
const id_btn_graphs = 'id_btn_compare_graphs'
const id_checkbox_all = 'id_checkbox_all_select' // checkbox в шапке корзины
const all_table = ['sample'] // Список таблиц
const main_field = { // Основные поля для изменения
    'sample': {
        'tr': 'tr_',
        'basket_tr': 'tr_select_',
        'segment_select_table': 'id_segment_select_table',
        'basket_table': 'sample_table_select',
        'url': '/sample/detail/tr/',
        'arr_el': select_tr,
    },
    'sample_table_select': {
        'tr': 'tr_select_',
        'arr_el': check_tr,
        'checkbox': 'select_checkbox_',
        'btn_detail': 'id_btn_detail',
        'btn_graphs': 'id_btn_compare_graphs',
        'message': 'id_message_table_select',
    }
}

const dimmer = $('<div class="ui active inverted dimmer" id="id_dimmer">' +
        '<div class="ui active green inline slow text loader">' +
        'Загрузка</div></div>')

// Проверка выбран ли элемент в таблице
function check_action(id, table){
    let index = 0;
    if( all_table.indexOf(table) !== -1){
        index = select_tr.indexOf(id);
    }
    else {
        index = check_tr.indexOf(id);
    }

    if (index === -1){
        return 'check';
    }

    return 'uncheck';
}

// Подсветка строки
function line_highlight(action, id, table){
    if (action === 'check') {
        $('#' + main_field[table]['tr'] + id).attr('class', 'green');
        if (all_table.indexOf(table) === -1) // Если корзина то подсвечиваем checkbox
            $('#' + main_field[table]['checkbox'] + id).checkbox('set checked');
        main_field[table]['arr_el'].push(id);
    }
    else {
        $('#' + main_field[table]['tr'] + id).removeAttr('class');
        if (all_table.indexOf(table) === -1) // Если корзина убираем checkbox
            $('#' + main_field[table]['checkbox'] + id).checkbox('set unchecked');
        else { // Если основная таблица удалем элемент из массива корзины
            if (check_tr.indexOf(id) !== -1)
                check_tr.splice(check_tr.indexOf(id), 1);
        }

        main_field[table]['arr_el'].splice(main_field[table]['arr_el'].indexOf(id), 1);
    }

    active_btn();
}

// Добавление и удаление строки в корзину
function add_or_remove_line_basket(action, table, id) {
    if (action === 'check') {
        $('#' + main_field[table]['segment_select_table']).append(dimmer); // Вешаем dimmer на таблицу
        ajax_get_detail_tr_all(id, table);
    } else {
        $('#' + main_field[table]['basket_table']).find('#' + main_field[table]['basket_tr'] + id ).remove();
    }
}


// Клик основных таблиц
function click_table(table){
    $(".table tbody tr").on("click", function (data) {
        let id = data.currentTarget.attributes.id.value.slice(main_field[table]['tr'].length);
        let action = check_action(id, table)
        line_highlight(action, id, table); // Подсвечиваем строку
        add_or_remove_line_basket(action, table, id); // Добавляем либо удаляем строку из корзины
        action_checkbox_all(); // Выставляем checkbox в шапке корзины
        show_select_table(main_field[table]['basket_table']); // Отображение корзины
    });
}

// Добавление обработчика нажатия на строки корзины
function add_bind(id, table, line){
    line.bind('click', function () {
        let action = check_action(id, table);
        line_highlight(action, id, table);
        action_checkbox_all();
    })
}

// Функция сравнения массивов, возращает элементы которых нет во 2 массиве
function diff(a1, a2) {
    return a1.filter(i=>!a2.includes(i))
    .concat(a2.filter(i=>!a1.includes(i)))
}

// Проверка на одинаковые элементы массива
function same_array(){
    for (let el of select_tr){
        if (check_tr.indexOf(el) === -1)
            return false
    }
    return true
}

// Показывать корзину если есть выбранные элементы
function show_select_table(table) {
    if (select_tr.length > 0){
        $('#' + main_field[table]['btn_detail']).removeAttr('style');
        $('#' + main_field[table]['btn_graphs']).removeAttr('style');
        $('#' + table).removeAttr('hidden');
        $('#' + main_field[table]['message']).attr('style', 'display: none');

    }
    else {
        $('#' + main_field[table]['btn_detail']).attr('style', 'display: none');
        $('#' + main_field[table]['btn_graphs']).attr('style', 'display: none');
        $('#' + table).attr('hidden', 'display: none');
        $('#' + main_field[table]['message']).removeAttr('style');
    }
}

// Активация checkbox в шапке корзины
function action_checkbox_all(){
    if (check_tr.length === select_tr.length && same_array()) // Если выбраны все строки делаем активным
        $('#' + id_checkbox_all).checkbox('set checked');
    else
        $('#' + id_checkbox_all).checkbox('set unchecked');
}

// обработка кнопок корзины
function click_btn(table, url=null) {
    $('.ui .button')
        .on('click', function (){
            let name_btn = $(this).attr('id');
            if (id_btn_detail === name_btn)
                btn_detail(table);
            if (id_btn_graphs === name_btn)
                btn_graphs(url);
        })
}

// кнопка детально
function btn_detail(table) {
    $('#id_segment_select_table').append(dimmer);
        let id_tr = main_field[table]['tr'] + check_tr[0];
        let trial_id = ''
        if (table === 'sample_table_select')
            trial_id = $('#' + id_tr).attr('name').slice('id_trials_'.length);
        if (trial_id){
            ajax_get_graph(trial_id, check_tr[0]);
        }else {
            let message = $('<div class="ui message info visible">\n' +
                '        <div class="ui text">У данного образца нет испытаний!</div>\n' +
                '    </div>')
            ajax_get_detail_sample(check_tr[0], message);
        }
}

// кнопка перехода на сравнение графиков
function btn_graphs(url){
    let query_params = jQuery.param({'samples': check_tr});
        document.location=url + query_params;
}

// Активация кнопок
function active_btn() {
    if(check_tr.length > 0){
        $('#id_btn_detail').attr('class', 'ui button')
    } else {
        $('#id_btn_detail').attr('class', 'ui button disabled')
    }
    if(check_tr.length > 1) {
        $('#id_btn_compare_graphs').attr('class', 'ui button')
    } else {
        $('#id_btn_compare_graphs').attr('class', 'ui button disabled')
    }
}

// обработка all checkbox
function click_all_checkbox(table){
    $('.ui.checkbox.all')
    .checkbox({
        onChecked: function(){
            // Если выбранных элементов в корзине нет нет то делаем их все активными
            if (check_tr.length === 0) {
                for (let id of select_tr) {
                    line_highlight('check', id, table);
                }
            }
            else { // Делаем активными только те которые еще не были выбраны
                let uncheck_sample = diff(select_tr, check_tr);
                for (let id of uncheck_sample) {
                    line_highlight('check', id, table);
                }
            }
        },
        // Будет активным только если все элементы в корзине выбраны
        onUnchecked: function(){
            // Убираем подсветку всем выбранным элементам
            if (check_tr.length === select_tr.length) {
                for (let id of select_tr) {
                    line_highlight('uncheck', id, table);
                }
            }
        }
    })
}

function ajax_get_detail_tr_all(id, table){
        $.ajax({
            url: main_field[table]['url'] + id,
            type: 'get',
            success: function (response) {
                // Получаем detail в виде строки таблицы
                let line_table = $(response).clone();
                add_bind(id, main_field[table]['basket_table'], line_table);
                 // Вставляем в корзину новую строку
                $('#' + main_field[table]['basket_table'] + '> tbody:last-child').append(line_table);
                // Записываем в массив id выбранного элемента
                $('#id_dimmer').remove();
            }
        });
    }

