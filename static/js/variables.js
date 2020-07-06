var select_tr = []; // Выбранные элементы в общей таблице
var check_tr = []; // Выбранные элементы в 'корзине' (таблица с выбранными элементами)

var id_checkbox_all = 'id_checkbox_all_select' // checkbox в шапке корзины
var all_table = ['sample', 'trials'] // Список таблиц
var dimmer = $('<div class="ui active inverted dimmer" id="id_dimmer">' +
        '<div class="ui active green inline slow text loader">' +
        'Загрузка</div></div>')

var main_field = {
    'sample': {
        'main_table': 'sample_table',
        'tr': 'tr_',
        'basket_tr': 'tr_select_',
        'segment_select_table': 'id_segment_select_table',
        'basket_table': 'sample_table_select',
        'url_tr': '/sample/detail/tr/',
        'arr_el': select_tr,
    },
    'trials': {
        'main_table': 'trial_table',
        'tr': 'tr_',
        'basket_tr': 'tr_select_',
        'segment_select_table': 'id_segment_select_table',
        'basket_table': 'trial_table_select',
        'url_tr': '/trial/detail/tr/',
        'arr_el': select_tr,
    },
    'sample_table_select': {
        'tr': 'tr_select_',
        'arr_el': check_tr,
        'checkbox': 'select_checkbox_',
        'btn_detail': 'id_btn_detail',
        'btn_graphs': 'id_btn_compare_graphs',
        'url_detail': '/sample/detail/',
        'message': 'id_message_table_select',
        'modal_detail': 'id_sample_modal',
    },
    'trial_table_select': {
        'tr': 'tr_select_',
        'arr_el': check_tr,
        'checkbox': 'select_checkbox_',
        'btn_detail': 'id_btn_detail',
        'btn_graphs': 'id_btn_compare_graphs',
        'message': 'id_message_table_select',
        'url_detail': '/trial/detail/',
        'modal_detail': 'id_trial_modal',
    }
}