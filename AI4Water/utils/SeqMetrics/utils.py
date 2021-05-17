import os
from collections import OrderedDict

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def take(st, en, d):
    keys = list(d.keys())[st:en]
    values = list(d.values())[st:en]

    return {k:v for k,v in zip(keys, values)}


def plot_metrics(metrics:dict,
                 ranges:tuple=((0.0, 1.0), (1.0, 10), (10, 1000)),
                 exclude:list = None,
                 plot_type:str='bar',
                 max_metrics_per_fig:int=15,
                 save:bool=True,
                 save_path:str=None,
                 **kwargs):
    """
    Plots the metrics given as dictionary as radial or bar plot between specified ranges.

    Arguments:
        metrics dict:
            dictionary whose keys are names are erros and values are error values.
        ranges tuple:
            tuple of tuples defining range of errors to plot in one plot
        exclude list/None:
            List of metrics to be excluded from plotting.
        max_metrics_per_fig int:
            maximum number of metrics to show in one figure.
        plot_type str:
            either of `radial` or `bar`.
        save bool:
            if True, the figure will be saved.
        save_path string/pathlike:
            if given, the figure will the saved at this location.
        kwargs dict:
            keyword arguments for plotting

    Example
    ---------
    ```python
    >>>import numpy as np
    >>>from AI4Water.utils.SeqMetrics import Metrics
    >>>from AI4Water.utils.SeqMetrics.utils import plot_metrics
    >>>t = np.random.random((20, 1))
    >>>p = np.random.random((20, 1))
    >>>er = Metrics(t, p)
    >>>all_errors = er.calculate_all()
    >>>plot_metrics(all_errors, plot_type='bar', max_metrics_per_fig=50)
    >>># or draw the radial plot
    >>>plot_metrics(all_errors, plot_type='radial', max_metrics_per_fig=50)
    ```
    """
    for idx, rng in enumerate(ranges):
        assert rng[1]>rng[0], f'For range {idx}, second value: {rng[1]} is not greater than first value: {rng[0]}. '
        assert len(rng) == 2, f"Range number {idx} has length {len(rng)}. It must be a tuple of length 2."

    if exclude is None:
        exclude = []

    _metrics = metrics.copy()
    for k,v in metrics.items():
        if k in exclude:
            _metrics.pop(k)

    assert plot_type in ['bar', 'radial'], f'plot_type must be either `bar` or `radial`.'

    for _range in ranges:
        plot_metrics_between(_metrics,
                             *_range,
                             plot_type=plot_type,
                             max_metrics_per_fig=max_metrics_per_fig,
                             save=save, save_path=save_path, **kwargs)
    return


def plot_metrics_between(errors: dict,
                         lower:int,
                         upper:int,
                         plot_type:str='bar',
                         max_metrics_per_fig:int=15,
                         save=True,
                         save_path=None, **kwargs):
    zero_to_one = {}
    for k, v in errors.items():
        if v is not None:
            if lower < v < upper:
                zero_to_one[k] = v
    st = 0
    n = len(zero_to_one)
    for i in np.array(np.linspace(0, n, int(n/max_metrics_per_fig)+1),
                      dtype=np.int32):
        if i == 0:
            pass
        else:
            en = i
            d = take(st,en, zero_to_one)
            if plot_type=='radial':
                plot_radial(d, lower, upper, save=save, save_path=save_path, **kwargs)
            else:
                plot_circular_bar(d, save=save, save_path=save_path, **kwargs)
            st = i
    return


def plot_radial(errors:dict, low:int, up:int, save=True, save_path=None, **kwargs):
    """Plots all the errors in errors dictionary. low and up are used to draw the limits of radial plot."""

    fill = kwargs.get('fill', None)
    fillcolor = kwargs.get('fillcolor', None)
    line = kwargs.get('line', None)
    marker = kwargs.get('marker', None)

    OrderedDict(sorted(errors.items(), key=lambda kv: kv[1]))

    lower = round(np.min(list(errors.values())), 4)
    upper = round(np.max(list(errors.values())), 4)

    fig = go.Figure()
    categories = list(errors.keys())

    fig.add_trace(go.Scatterpolar(
        r=list(errors.values()),
        theta=categories,  # angular coordinates
        fill=fill,
        fillcolor=fillcolor,
        line=line,
        marker=marker,
        name='errors'
    ))

    fig.update_layout(
        title_text=f"Errors from {lower} to {upper}",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[low, up]
            )),
        showlegend=False
    )

    fig.show()
    if save:
        fname = f"radial_errors_from_{lower}_to_{upper}.png"
        if save_path is not None:
            fname = os.path.join(save_path, fname)
        fig.write_image(fname)
    return


def plot_circular_bar(metrics:dict, save:bool, save_path:str, **kwargs):
    """
    modified after https://www.python-graph-gallery.com/circular-barplot-basic
    :param metrics:
    :param save:
    :param save_path:
    :param kwargs:
        figsize:
        linewidth:
        edgecolor:
        color:
    :return:
    """

    # initialize the figure
    plt.close('all')
    plt.figure(figsize=kwargs.get('figsize', (8, 12)))
    ax = plt.subplot(111, polar=True)
    plt.axis('off')

    # Set the coordinates limits
    upperLimit = 100
    lowerLimit = 30
    Value = np.array(list(metrics.values()))

    lower = round(np.min(list(metrics.values())), 4)
    upper = round(np.max(list(metrics.values())), 4)

    # Compute max and min in the dataset
    _max = max(Value) # df['Value'].max()

    # Let's compute heights: they are a conversion of each item value in those new coordinates
    # In our example, 0 in the dataset will be converted to the lowerLimit (10)
    # The maximum will be converted to the upperLimit (100)
    slope = (_max - lowerLimit) / _max
    heights = slope * Value + lowerLimit

    # Compute the width of each bar. In total we have 2*Pi = 360°
    width = 2 * np.pi / len(metrics)

    # Compute the angle each bar is centered on:
    indexes = list(range(1, len(metrics) + 1))
    angles = [element * width for element in indexes]

    # Draw bars
    bars = ax.bar(
        x=angles,
        height=heights,
        width=width,
        bottom=lowerLimit,
        linewidth=kwargs.get('linewidth', 2),
        edgecolor=kwargs.get('edgecolor', "white"),
        color=kwargs.get('color', "#61a4b2"),
    )

    # little space between the bar and the label
    labelPadding = 4

    # Add labels
    for bar, angle, height, label1, label2 in zip(bars, angles, heights, metrics.keys(), metrics.values()):

        label = f'{label1} {round(label2, 4)}'

        # Labels are rotated. Rotation must be specified in degrees :(
        rotation = np.rad2deg(angle)

        # Flip some labels upside down
        alignment = ""
        if angle >= np.pi / 2 and angle < 3 * np.pi / 2:
            alignment = "right"
            rotation = rotation + 180
        else:
            alignment = "left"

        # Finally add the labels
        ax.text(
            x=angle,
            y=lowerLimit + bar.get_height() + labelPadding,
            s=label,
            ha=alignment,
            va='center',
            rotation=rotation,
            rotation_mode="anchor")

    if save:
        fname = f"bar_errors_from_{lower}_to_{upper}.png"
        if save_path is not None:
            fname = os.path.join(save_path, fname)
        plt.savefig(fname, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    return


def plot1d(true, predicted, save=True, name="plot", show=False):
    fig, axis = plt.subplots()

    axis.plot(np.arange(len(true)), true, label="True")
    axis.plot(np.arange(len(predicted)), predicted, label="Predicted")
    axis.legend(loc="best")

    if save:
        plt.savefig(name, dpi=300, bbox_inches='tight')
    if show:
        plt.show()

    plt.close('all')
    return