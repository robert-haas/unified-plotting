def try_all_legend_parameters(plotting_function, data):
    arguments = [
        ('legend_title', 'Legend'),
        ('legend_color', 'red'),
        ('legend_color', (0, 1, 0)),
        ('legend_color', 'rgba(0, 0, 1, 0.5)'),
        ('legend_color', '#01090f'),
        ('legend_size', 20),
        ('legend_font', 'serif'),
        ('legend_background_color', 'red'),
        ('legend_background_color', (0, 1, 0)),
        ('legend_background_color', 'rgba(0, 0, 1, 0.5)'),
        ('legend_background_color', '#01090f'),
        ('legend_position_horizontal', 'center'),
        ('legend_position_vertical', 'center'),
        ('legend_border_color', 'red'),
        ('legend_border_color', (0, 1, 0)),
        ('legend_border_color', 'rgba(0, 0, 1, 0.5)'),
        ('legend_border_color', '#01090f'),
        ('legend_border_size', 3.2),
    ]
    png_data_urls = []
    for key, val in arguments:
        kwargs = {key: val}
        fig = plotting_function(show_legend=True, **data, **kwargs)
        png_data_urls.append(fig.png_data_url)
    assert len(png_data_urls) == len(set(png_data_urls))  # check that all plots are different

    # Combinations
    png_data_urls = []
    for pos_h in ['left', 'center', 'right']:
        for pos_v in ['top', 'center', 'bottom']:
            fig = plotting_function(
                **data, show_legend=True,
                legend_position_horizontal=pos_h,
                legend_position_vertical=pos_v)
            png_data_urls.append(fig.png_data_url)
    assert len(png_data_urls) == len(set(png_data_urls))  # check that all plots are different


def try_unknown_argument(caplog, plotting_function, data):
    caplog.clear()
    plotting_function(**data, nonsense_argument='whatever')
    expected_message = 'Following arguments are unknown and ignored: "nonsense_argument"'
    assert [expected_message] == [rec.message for rec in caplog.records]
