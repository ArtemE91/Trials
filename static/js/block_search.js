
var search_list = {};

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
                const name_dropdown = $(this).closest('.ui.normal.dropdown').attr('name');
                search_list[name_dropdown + '__in'] = value.split(',');
                if (value === '') {
                    delete search_list[name_dropdown + '__in'];
                }
                ajax_get_table(table);
            },
        });
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