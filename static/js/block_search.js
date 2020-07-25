
var search_list = {};
var name_type_dropdown = 'sample__sample_type__name'

var table_value = {
    'sample': {
        'url': '/sample/table',
        'change_segment': 'segment_table'

    },
    'trials': {
        'url': '/trial/table',
        'change_segment': 'segment_trials_table'
    }
}

// обработка дополнительных дропдаунов
function change_add_dropdown(table) {
    $('.ui.pointing.dropdown')
        .dropdown({
                onChange: function (value, text, $selectedItem) {
                    search_list['date'] = value;
                    ajax_get_table(table);
                }
            }
        )
}

// Обработка обычных дропдаунов
function change_dropdown(table) {
    $('.ui.normal.dropdown')
        .dropdown({
            onChange: function (value, text, $selectedItem) {
                $('#' + table_value[table]['change_segment']).append(dimmer);
                var name_dropdown = $(this).closest('.ui.normal.dropdown').attr('name');
                var list_name_value = value.split(',')
                if (name_dropdown === name_type_dropdown) {
                    hide_or_show_add_dropdown(list_name_value)
                }
                search_list[name_dropdown + '__in'] = list_name_value;
                if (value === '') {
                    delete search_list[name_dropdown + '__in'];
                }
                ajax_get_table(table);
            },
        });
}

// Показывает либо скрывает дополнительные блоки дропдаунов для типа образца
function hide_or_show_add_dropdown(list_name_type){
    console.log(list_name_type);
    if(list_name_type.indexOf('грибок') !== -1 ){
        $('#' + 'add_filter_fungus').attr('style', '');
    } else {
        $('#' + 'add_filter_fungus').attr('style', 'display: none');
    }
    if(list_name_type.indexOf('диск') !== -1 || list_name_type.indexOf('пластина') !== -1){
        $('#' + 'add_filter_disk').attr('style', '');
    } else {
        $('#' + 'add_filter_disk').attr('style', 'display: none');
    }
}

function ajax_get_table(table){
        $.ajax({
                  type: "GET",
                  url: table_value[table]['url'],
                  data: {
                      'search': JSON.stringify(search_list),
                  },
                  success: function(msg){
                      $("#" + table_value[table]['change_segment']).replaceWith(msg);
                      // Подсвечиваю строки уже выбранных элементов
                      check_action_line();
                  }
        });
    }

function check_action_line(){
    if (select_tr) {
        for (let id_tr of select_tr) {
            let line = $('#tr_' + id_tr)
            line.attr('class', 'green');
        }
    }
}