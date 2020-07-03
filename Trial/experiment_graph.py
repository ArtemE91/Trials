import plotly.graph_objs as go


def multigraf(coordinates):
    figure = go.Figure()
    config = {'displayModeBar': True}
    for c in coordinates:
        figure.add_trace(go.Scatter(
            y=c[1],
            x=c[0],
            name=c[2],
            mode='lines+markers',
        ))

    figure.update_layout(
        xaxis_title="Изменение времени, мин",
        yaxis_title="Изменение массы, г",
        title='Сравнение испытаний',
    )
    plt_div = figure.to_html(config=config, )
    return plt_div


def figure(x, y):
    fig = go.Figure()
    config = {'displayModeBar': False}
    fig.add_trace(go.Scatter(
        y=y,
        x=x,
        name="Испытание №1",
        mode='lines+markers',
    ))

    # fig.add_trace(go.Scatter(
    #     y=[0.00088, 0.00088, 0.00088, 0.00168, 0.00424, 0.00804, 0.01242, 0.01786, 0.0227,
    #        0.02764, 0.03176, 0.03516, 0.03864, 0.0414],
    #     x=[20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150],
    #     name="Испытание №2",
    #      mode='lines+markers',
    # ))

    fig.update_layout(
        xaxis_title="Изменение времени, мин",
        yaxis_title="Изменение массы, г",
        title='График экспериментов',
    )
    plt_div = fig.to_html(full_html=False, default_height=500,
                          default_width=850, config=config,)
    # plt_div = plot(fig, output_type='div', config=config, auto_open=False)
    return plt_div
