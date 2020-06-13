import plotly.graph_objs as go


def figure():
    fig = go.Figure()
    config = {'displayModeBar': False}
    fig.add_trace(go.Scatter(
        y=[0.00058, 0.00138, 0.00216, 0.00462, 0.00692, 0.01092, 0.01446, 0.01878, 0.02232,
           0.02692, 0.03076, 0.03384, 0.03644, 0.03928],
        x=[20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150],
        name="Испытание №1"
    ))

    # fig.add_trace(go.Scatter(
    #     y=[0.00088, 0.00088, 0.00088, 0.00168, 0.00424, 0.00804, 0.01242, 0.01786, 0.0227,
    #        0.02764, 0.03176, 0.03516, 0.03864, 0.0414],
    #     x=[20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150],
    #     name="Испытание №2"
    # ))

    fig.update_layout(
        xaxis_title="Время",
        yaxis_title="Изменение массы", )
    plt_div = fig.to_html(full_html=False, default_height=500, default_width=700, config=config)
    # plt_div = plot(fig, output_type='div', config=config, auto_open=False)
    return plt_div
