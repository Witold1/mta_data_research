#from collections import defaultdict
import matplotlib.pyplot as plt
#import seaborn as sns
#import july
#import plotly.express as px
# import numpy as np

def _add_custom_text_units_per_stations(df_aux, axis):
    """Adds custom text with station names to top 5 stations number of units.

        * Question DA1. Which station has the most number of units?

    Parameters
    ----------
    df_aux : pd.DataFrame or [container]
        data table or container with values set ticks to
    axis : matplotlib.pyplot.axis
        axis object, where to add annotation
    """
    from collections import defaultdict

    dict_aux = defaultdict(list)
    for item in df_aux.nlargest(5).items():
        dict_aux[item[1]].append(item[0])

    for k, val in dict_aux.items(): # write here 'stations: '
        axis.text(x=15, y=k - 1.05, s="; ".join(val), style='italic')

def plot_bar_chart_units_per_stations(df_to_plot, axis):
    """Plots aggregated number of units per station.

        * Question DA1. Which station has the most number of units?

    Parameters
    ----------
    df_to_plot : pd.DataFrame
        Total number of entries
    axis : matplotlib.pyplot.axis
        axis object, where to plot
    """

    df_to_plot.value_counts(ascending=False).plot.barh(ax=axis, color='#009aa6', zorder=10)

    axis.bar_label(axis.containers[0], padding=10, style='italic')
    _add_custom_text_units_per_stations(df_to_plot, axis)

    # Beautify
    axis.grid(axis='x', alpha=0.20, c='gray', linestyle='--', zorder=0)
    axis.tick_params(axis='both', which='major')
    axis.set(xlabel='Number of Stations', ylabel='Number of Units')
    axis.set_title(f'How many stations have how many units?', loc='left', pad=-0.03) # pad=-0.05, fontsize=18
    axis.spines[['top', 'left', 'right']].set_visible(False)

    return axis

def plot_one_line_entry_exit_chart(entries, exits, y, axis):
    """Plots total (aggregated) number of entries & exits across the subway system.

        ??? Curt. version is for one "row" (line) only, add loop(s) and use container(s)
            to process multiple rows

        * Chart idea credits to Diane Ferrera - Standing Room Only https://dianeferrera.com/data-mta.html
        * Question DA2. What is the total number of entries & exits across the subway system for February 1, 2013?

    Parameters
    ----------
    entries : int
        total number of entries
    exits : int
        total number of exits
    y : int
        y axis values
    axis : matplotlib.pyplot.axis
        axis object, where to plot
    ----------
    """

    # vertical ENTRIES & EXITS parts separator
    axis.vlines(x=0, ymin=0.75, ymax=1.25, linewidth=3, colors=None, linestyles='solid',
                label='', alpha=0.8) #a60c00

    # ENTRIES and EXITS arrows
    axis.arrow(-entries, 1., entries, 0, head_width=0.1, head_length=entries/30,
                linewidth=4, color='g', alpha=0.9, length_includes_head=True) #009aa6
    axis.arrow(0, 1., exits, 0, head_width=0.1, head_length=entries/30,
                linewidth=4, color='g', alpha=0.9, length_includes_head=True) #009aa6
    # ENTRIES and EXITS annotations
    axis.annotate(f"{entries / 1000}K", xy=(-entries, 1.05), style='italic')
    axis.annotate(f"{exits / 1000}K", xy=(exits / 20, 1.05), style='italic')
    axis.annotate('Entries', xy=(-entries, 1.15), fontsize=14)
    axis.annotate('Exits', xy=(exits / 20, 1.15), fontsize=14)

    # Beautify
    axis.margins(0.1)
    axis.grid(axis='x', alpha=0.20, c='gray', linestyle='--', zorder=0)
    axis.set(xticklabels=[], yticks=[])
    axis.set_title('Total number of entries & exits across the subway system for February 1, 2013', loc='left') # pad=+0.05
    axis.spines[['left', 'right', 'bottom']].set_visible(False)

    return axis

def plot_interactive_line_or_bar(df_aux, title, yaxis_label, xaxis_label, lineplot=True):
    """Plots line chart with interactive hover.

        # Chart idea credits ???
        * Question VIZ2. Plot the daily total number of entries & exits across the system for Q1 2013.

    Parameters
    ----------
    df_aux : pd.DataFrame
        data table
    title : str
        main title of chart
    yaxis_label : str
        label of y axis
    xaxis_label : str
        label of x axis
    ----------
    """
    import plotly.express as px

    if lineplot:
        fig = px.line(data_frame=df_aux)
    else:
        fig = px.bar(data_frame=df_aux)

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="7 Days", step="day", stepmode="backward"),
                dict(count=1, label="1 Month", step="month", stepmode="backward"),
                dict(count=1, label="YTD (all)", step="year", stepmode="todate"),
            ])
        )
    )

    fig.update_layout(
        title=title,
        yaxis_title=yaxis_label,
        xaxis_title=xaxis_label,
        legend_title="Legend",
    )

    fig.show()

def plot_gradientplot_intervals(df_aux, fig, axis):
    """Plots point estimation using gradient (intervals) plot.

        # Chart idea credits to Michael Friendly - Visualizing Uncertainty,
            https://friendly.github.io/6135/lectures/Uncertainty-2x2.pdf
        * Question VIZ4, VIZ5. Visualize parameter (point) estimation

    Parameters
    ----------
    df_jitter : pd.DataFrame
        data table
    fig : matplotlib.pyplot.figure
        figure object to abjust legend & custom labels (coord are manually set now)
    axis : matplotlib.pyplot.axis
        axis object, where to plot
    """
    for indx, weekend_flag in enumerate([False, True]):

        df_aux_tmp = df_aux.xs((weekend_flag), level=('IS_WEEKEND'))
        inds = df_aux_tmp.index.get_level_values(0).unique().values - 1
        mean_tmp = df_aux_tmp.groupby(['AUDIT_MONTH']).mean()
        std_tmp = df_aux_tmp.groupby(['AUDIT_MONTH']).std()
        max_tmp = df_aux_tmp.groupby(['AUDIT_MONTH']).max()
        min_tmp = df_aux_tmp.groupby(['AUDIT_MONTH']).min()

        mean_marker = axis.scatter(inds + indx / 8, mean_tmp, marker='o', color='red', s=80,
                                zorder=3, label = 'Mean value')
        one_std = axis.vlines(x=inds + indx / 8, ymin=mean_tmp - std_tmp, ymax=mean_tmp + std_tmp,
                                color='k', linestyle='-', lw=5, alpha=0.5, label = '±1 std')
        two_std = axis.vlines(x=inds + indx / 8, ymin=mean_tmp - 2 * std_tmp, ymax=mean_tmp + 2 * std_tmp,
                                color='k', linestyle='-', lw=7, alpha=0.25, label = '±2 std')

        marker_color = 'blue' if indx % 2 == 0 else 'orange'
        max_marker = axis.scatter(x=inds + indx / 8, y=max_tmp, marker=7, color=marker_color, s=80,
                                zorder=3, label = 'Max value')
        min_marker = axis.scatter(x=inds + indx / 8, y=min_tmp, marker=6, color=marker_color, s=80,
                                zorder=3, label = 'Min value')

        points = axis.scatter(x=df_aux_tmp.index.get_level_values(0) - 1.1,
                   y=df_aux_tmp.values, marker=1, alpha=0.6, # marker  1 if weekend_flag else 0
                   linewidths=3, label='Weekend' if weekend_flag else 'Weekday')

        n_days_text = [axis.text(x, y, f'days={s}') for x, y, s in
                    zip(inds + indx / 8 + 0.05, mean_tmp.values, df_aux_tmp.groupby('AUDIT_MONTH').size().values)]

    # Beautify
    axis.margins(y=0.1)
    axis.grid(axis='y', linestyle='--', alpha=0.2, color='g', zorder=10)
    axis.set_xticklabels([None, 'January', None, 'February', None, 'March'], weight='bold')
    #axis.set_ylabel('Total number of entries & exits'); #axes.set_xlabel('Month')
    axis.set_title('Daily total number of entries & exits for each month in Q1 2013 for station 34 ST-PENN STA.',
                    fontsize=12, loc='left')
    axis.spines[['left', 'right', 'bottom']].set_visible(False)
    axis.spines[['top']].set_visible(True)
    handles, labels = fig.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    legend = fig.legend(by_label.values(), by_label.keys(), ncol=7, loc='upper left',
               bbox_to_anchor=(0.05, 0.91), frameon=False)

    return axis

def plot_boxplot_jitter_mix(df_jitter, df_boxes, fig, axis):
    """Plots a mix of boxplots and jittered scatterplot to show quantiles.

        Semantically it's a custom `Raincloud plot` without cloud
            See. github.com/pog87/PtitPrince . It's a mix of plots
            that improves opportunities to see point estimations
            and distributions at the same time

    # Chart idea credits to Michael Friendly - Visualizing Uncertainty,
        https://friendly.github.io/6135/lectures/Uncertainty-2x2.pdf;
        https://github.com/RainCloudPlots/RainCloudPlots
    * Question VIZ4, VIZ5. Visualize parameter (point) estimation

    Parameters
    ----------
    df_jitter : pd.DataFrame or [container]
        df with points to plot stripplot/jittered scatter (rain)
    df_boxes : pd.DataFrame or [container]
        df with points to plot boxes
    fig : matplotlib.pyplot.figure
        figure object to abjust custom labels (coord are manually set now)
    axis : matplotlib.pyplot.axis
        axis object, where to plot
    """
    import seaborn as sns

    jitter = sns.swarmplot(x='BUSYNESS', y='AUDIT_MONTH', hue='IS_WEEKEND',
                  data=df_jitter,
                  edgecolor="white",
                  size=4, #jitter=0.1,
                  zorder=0, orient='h',
                  ax=axis)

    weekend_weekday = axis.boxplot(x=df_boxes[:-3],
                 positions=[0.15, 0.20, 1.15, 1.20, 2.15, 2.20],
                 widths=0.05,
                 vert=False, zorder=0)
    month = axis.boxplot(x=df_boxes[-3:], positions=[0.35, 1.35, 2.35],
                 widths=0.05, vert=False, zorder=0)

    # https://stackoverflow.com/questions/44250055/text-caption-not-appearing-matplotlib
    axis.text(x=0.07, y=0.7, s='January', transform=fig.transFigure, rotation=90, weight='bold')
    axis.text(x=0.07, y=0.45, s='February', transform=fig.transFigure, rotation=90, weight='bold')
    axis.text(x=0.07, y=0.15, s='March', transform=fig.transFigure, rotation=90, weight='bold')

    # Beautify
    axis.grid(axis='x', alpha=0.20, c='gray', linestyle='--', zorder=0)
    axis.set(ylabel='', yticklabels=[], yticks=[])
    axis.set_xlabel('Daily total number of entries & exits')
    axis.spines[['left', 'right']].set_visible(False); axis.spines['top'].set_visible(True)
    axis.legend().remove()
    legend = fig.legend(frameon=False, ncol=2, loc='upper left',
               bbox_to_anchor=(0.06, 0.99)) # labels=['Weekday', 'Weekday']
    legend.get_texts()[0].set_text('Weekday'); legend.get_texts()[1].set_text('Weekend')

    return axis

def plot_panel_bars_station_change(df_aggregated, df_stations_change, fig, axes,
                                   plot_MA=True, plot_pct_change=True):
    """Plots a panel with mix of bar charts and line charts.

    * Question DA4. What stations have seen the most usage growth/decline in 2013?

    Parameters
    ----------
    df_aggregated : pd.DataFrame or [container]
        df with grouped (aggregated) numbers by station and date
    df_stations_change : pd.DataFrame or [container]
        df with usage changes and respective station names, better be sorted
    fig : matplotlib.pyplot.figure
        figure object
    axis : matplotlib.pyplot.axis
        axis object, where to plot
    plot_MA : bool
        if add moving average {windows = 1, 2, 3} lines to chart
    plot_pct_change : bool
        if add percent change lines to chart
    """

    for indx, (station_name, value) in enumerate(df_stations_change.iteritems()):

        color = 'red' if value < 0 else 'green'
        alpha = 1. if abs(value) >= 1 else abs(value)

        df_to_plot = df_aggregated.xs(station_name)
        bars = df_to_plot.plot.bar(color='#009aa6', ax=axes[indx], label='Weekly totals')

        if plot_MA:
            for i in range(1, 3):
                df_to_plot.rolling(i).mean().plot.line(ax=axes[indx], style='-', color=color, alpha=0.3,
                                                        label='Moving Averages')
        elif plot_pct_change:
            # we may plot many options, and many rollings too
            df_to_plot.pct_change(1).plot.line(ax=axes[indx], color=color, alpha=0.3,
                                                label='Change rate', secondary_y=True)

        axes[indx].set(#title=station_name + f', {round(value, 3)}', xticks=[],
                        ymargin=0.1, xmargin=0.1)
        axes[indx].xaxis.set_tick_params(which='minor', bottom=False)

        axes[indx].grid(axis='y', linestyle='--', alpha=0.2, color='g', zorder=10)
        axes[indx].set_title(station_name, loc='left')
        axes[indx].set_title(f'{round(value, 2)}', loc='right', c='black', x=0.98,
                             bbox=dict(facecolor=color, edgecolor='white', alpha=alpha * 0.5))
        axes[indx].spines[['left', 'right', 'bottom']].set_visible(False)

    return axes

def plot_heatmap_calendar(df_aux, title, title_style_dict):
    """Plots heatmap calendar chart.

    !!! `july` Chart package sets globals params which
            brokes relative coordinates for other charts if run again
            https://github.com/e-hulten/july/issues/26

    # Chart idea credits to Aaron Schumacher etc. - NYC Subway Usage bl.ocks.org/ajschumacher/5127001,
        slideshare.net/ajschumacher/turnstile-presentation
    * Question VIZ5. Plot the daily number of closed stations and number of stations
        that were not operating at full capacity in Q1 2013

    Parameters
    ----------
    df_aux : pd.DataFrame
        data table
    title : str
        main title of a chart
    title_style_dict : dict
        dictionary with main (figure) title params
    """
    import july

    fig, axes = plt.subplots(1, 3, figsize=(15, 5), dpi=350)

    for indx in range(0, 3):
        july.month_plot(data=df_aux.values, dates=df_aux.index, month=indx + 1,
                weeknum_label=True, value_label=True, ax=axes[indx]) # , cmap="gray_r"
        #plt.setp(axes[indx].texts, color='white')

    fig.suptitle(t=title, x=0.016, y=0.98, **title_style_dict)
    fig.tight_layout(rect=[0.0, 0.0, 1.0, 1.0])

    return axes

def plot_barplot_metric_hourly(axes):
    """Plots hourly `busyness metric` (of subway usage) in ordinal barplot.

    * Question DA5. Bonus: What hour is the busiest for station CANAL ST in Q1 2013?

    Parameters
    ----------
    axis : matplotlib.pyplot.axis
        axis object, where to plot
    param : type
        placeholder
    """

    pass

def plot_clock_metric_hourly(radii, color, title, axis):
    """Plots hourly `busyness metric` (of subway usage) in fancy , 'polar-coordinates'
        (circular) barplot.

    # Chart idea and code credits to Chih-Ling Hsu - Analyze the NYC Taxi Data,
        chih-ling-hsu.github.io/2018/05/14/NYC
    * Question DA5. Bonus: What hour is the busiest for station CANAL ST in Q1 2013?

    Parameters
    ----------
    radii : type
        placeholder
    title :
        main title of a chart
    color :
        color of bars
    axis : matplotlib.pyplot.axis
        axis object, where to plot
    ----------
    """
    import numpy as np

    N = 24
    bottom = 2

    # create theta for 24 hours
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)

    # width of each bin on the plot
    width = (2 * np.pi) / N

    bars = axis.bar(theta, radii, width=width, bottom=bottom, color=color, align='edge') #edgecolor="#999999"

    # set the lable go clockwise and start from the top
    axis.set_theta_zero_location("N")
    # clockwise
    axis.set_theta_direction(-1)

    # set the label
    axis.set_xticks(theta)
    ticks = ["{}:00".format(x) for x in range(24)]
    axis.set_xticklabels(ticks)
    axis.set_title(title, loc='center')

    return axis
