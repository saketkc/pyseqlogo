# -*- coding: utf-8 -*-

"""Main module."""
from __future__ import division
from __future__ import absolute_import
import matplotlib.pyplot as plt
from matplotlib.patheffects import RendererBase
from matplotlib import transforms
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import MultipleLocator
from matplotlib.ticker import FormatStrFormatter
from .utils import despine


class Scale(RendererBase):
    """Scale alphabets using affine transformation"""
    def __init__(self, sx, sy=None):
        self._sx = sx
        self._sy = sy

    def draw_path(self, renderer, gc,
                  tpath, affine, rgbFace):
        affine = affine.identity().scale(self._sx, self._sy) + affine
        renderer.draw_path(gc, tpath, affine, rgbFace)


__COLOR_SCHEME__ = {'G': 'orange',
                        'A': 'red',
                        'C': 'blue',
                        'T': 'darkgreen'}

def _setup_plt():
    plt.rcParams['savefig.dpi'] = 120
    plt.rcParams['figure.dpi'] = 120
    plt.rcParams['figure.autolayout'] = False
    plt.rcParams['figure.figsize'] = 12, 8
    plt.rcParams['axes.labelsize'] = 18
    plt.rcParams['axes.titlesize'] = 20
    plt.rcParams['font.size'] = 16
    plt.rcParams['lines.linewidth'] = 2.0
    plt.rcParams['lines.markersize'] = 8
    plt.rcParams['legend.fontsize'] = 14


def _setup_font(fontfamily, fontsize=12):
    """Setup font properties"""

    _setup_plt()
    font = FontProperties()
    font.set_size(fontsize)
    font.set_weight('bold')
    font.set_family(fontfamily)
    return font


def _draw_text(height_matrix, ax, font):
    fig = ax.get_figure()
    trans_offset = transforms.offset_copy(ax.transData,
                                            fig=fig,
                                            x=1,
                                            y=0,
                                            units='dots')
    for xindex, xcol in enumerate(height_matrix):
        yshift = 0
        for basechar, basescore in xcol:
            txt = ax.text(xindex + 1,
                            0,
                            basechar,
                            transform=trans_offset,
                            fontsize=80,
                            color=__COLOR_SCHEME__[basechar],
                            ha='center',
                            fontproperties=font,
                        )
            txt.set_path_effects([Scale(1.0, basescore)])
            fig.canvas.draw()
            window_ext = txt.get_window_extent(txt._renderer)
            yshift = window_ext.height * basescore
            trans_offset = transforms.offset_copy(txt._transform,
                                                  fig=fig,
                                                  y=yshift,
                                                  units='dots')
        trans_offset = transforms.offset_copy(ax.transData,
                                              fig=fig,
                                              x=1,
                                              y=0,
                                              units='dots')


def setup_axis(ax, axis='x', majorticks=10, minorticks=5, xrotation=0, yrotation=0):
    """Setup axes defaults"""

    major_locator = MultipleLocator(majorticks)
    major_formatter = FormatStrFormatter('%d')
    minor_locator = MultipleLocator(minorticks)
    if axis == 'x':
        ax.xaxis.set_major_locator(major_locator)
        ax.xaxis.set_major_formatter(major_formatter)
        ax.xaxis.set_minor_locator(minor_locator)

    elif axis == 'y':
        ax.yaxis.set_major_locator(major_locator)
        ax.yaxis.set_major_formatter(major_formatter)
        ax.yaxis.set_minor_locator(minor_locator)
    elif axis == 'both':
        ax.xaxis.set_major_locator(major_locator)
        ax.xaxis.set_major_formatter(major_formatter)
        ax.yaxis.set_minor_locator(minor_locator)
        ax.yaxis.set_major_locator(major_locator)
        ax.yaxis.set_major_formatter(major_formatter)
        ax.yaxis.set_minor_locator(minor_locator)
    ax.tick_params(which='major', width=2, length=10)
    ax.tick_params(which='minor', width=1, length=6)


def draw_logo(pwm_matrix, fontfamily='Arial', ax=None):
    """Plain motif logo"""

    #TODO take other inputs than just the PWM

    font = _setup_font(fontfamily)
    if ax is None:
        fig, ax = plt.subplots(figsize=(len(pwm_matrix), 2.75))
    else:
        fig = ax.get_figure()

    ax.set_xticks(range(1, len(pwm_matrix) + 1))
    ax.set_yticks(range(0, 3))
    ax.set_xticklabels(range(1, len(pwm_matrix) + 1), rotation=90)
    #ax.set_yticklabels(np.arange(0, 3, 1))
    setup_axis(ax, 'y', majorticks=1, minorticks=0.1)
    _draw_text(pwm_matrix, ax, font)
    despine(ax=ax, trim=True, offset=10)
    return ax
