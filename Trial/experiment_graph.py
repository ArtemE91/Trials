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
    
    fig.update_layout(
        xaxis_title="Изменение времени, мин",
        yaxis_title="Изменение массы, г",
        title='График экспериментов',
    )
    plt_div = fig.to_html(full_html=False, default_height=500,
                          default_width=850, config=config,)
    # plt_div = plot(fig, output_type='div', config=config, auto_open=False)
    return plt_div
