import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from Plot.draw_helper import get_color, get_hatch, get_marker, to_percent, to_scf, label_all
from matplotlib.ticker import FuncFormatter, MultipleLocator
import seaborn as sns

class Draw:
    #fig = None
    #ax = None
    #data = None
    #legend = None
    #xaxis = None
    #title = None
    def __init__(self, data, legend, xaxis, title, large):
        'data, legend, xaxis, title, type, para'
        self.data = data
        self.legends = legend
        self.xaxis = xaxis
        self.title = title
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        sns.set_style("white")
        if large==1:
            self.fig, self.ax = plt.subplots(1, 1, sharex=True, figsize=(18, 3))
        elif large==0:
            self.fig, self.ax = plt.subplots(1, 1, sharex=True, figsize=(8, 4))
        elif large==2:
            self.fig, self.ax = plt.subplots(1, 1, sharex=True, figsize=(6, 8))


    def output(self, path, despine=True):
        if despine:
            sns.despine()
        self.fig.savefig(
            path,
            format='pdf',
            dpi=1000,
            bbox_inches='tighfilename,t')


    def get_pic(self):
        'return the fig and ax, enable further customize.'
        return self.fig, self.ax


    def draw_stack(self, **kwargs):
        benches = len(self.data[0])
        bars = len(self.data)
        ind = np.arange(start=0, stop=benches*3, step=3)
        width = 3.0/(2)
        for i in range(bars):
            self.ax.bar(
                ind + width/2.0,
                self.data[i],
                width,
                color=kwargs.setdefault('color', 'w'),
                bottom=np.sum(self.data[:i], axis=0),
                edgecolor=get_color(i),
                hatch=get_hatch(i),
                label=self.legends[i])
        self.ax.set_ylabel(self.title)
        self.ax.set_xticks(ind+bars/2.0*width)
        self.fig.gca().set_ylim(
            kwargs.setdefault('y_start', 0),
            kwargs.setdefault('y_end', 1.2))
        self.fig.gca().set_xlim(0, benches*3)
        self.ax.set_xticklabels(
            self.xaxis,
            rotation=kwargs.setdefault('rotate', 0),
            fontsize=kwargs.setdefault('xaxis_fs', 9),
            va=kwargs.setdefault('xaxis_va', 'top'),
            ha=kwargs.setdefault('xaxis_ha', 'center'))
        if kwargs.setdefault('use_lgd', True):
            self.ax.legend(
                ncol=kwargs.setdefault('lgd_col', '8'),
                bbox_to_anchor=kwargs.setdefault('lgd_cord', (0., 1, 1., 0)),
                fontsize=kwargs.setdefault('lgd_fs', 9),
                loc='upper center')
        if kwargs.setdefault('use_percent', '0'):
            formatter = FuncFormatter(to_percent)
            self.fig.gca().yaxis.set_major_formatter(formatter)


    def draw_hist(self, **kwargs):
        benches = len(self.data[0])
        bars = len(self.data)
        ind = np.arange(start=0, stop=benches*3, step=3)
        width = 3.0/(bars+1)
        rects = []
        for i in range(bars):
            tmp = self.ax.bar(
                ind+i*width+width/2.0,
                self.data[i],
                width,
                # color=kwargs.setdefault('color', 'w'),
                color=get_color(i),
                edgecolor='w',
                # hatch=get_hatch(i),
                label=self.legends[i])
            rects.append(tmp)
        self.ax.set_ylabel(self.title)
        self.ax.set_xticks(ind+bars/2.0*width)
        self.fig.gca().set_ylim(
            kwargs.setdefault('y_start', 0),
            kwargs.setdefault('y_end', 1.2))
        self.fig.gca().set_xlim(0, benches*3)
        self.ax.set_xticklabels(
            self.xaxis,
            rotation=kwargs.setdefault('rotate', 0),
            fontsize=kwargs.setdefault('xaxis_fs', 9),
            va=kwargs.setdefault('xaxis_va', 'top'),
            ha=kwargs.setdefault('xaxis_ha', 'center'))
        if kwargs.setdefault('use_lgd', True):
            self.ax.legend(
                ncol=kwargs.setdefault('lgd_col', '8'),
                bbox_to_anchor=kwargs.setdefault('lgd_cord', (0., 1, 1., 0)),
                fontsize=kwargs.setdefault('lgd_fs', 9),
                loc='upper center')
        if kwargs.setdefault('use_percent', '0'):
            formatter = FuncFormatter(to_percent)
            # Set the formatter
            self.fig.gca().yaxis.set_major_formatter(formatter)
        if kwargs.setdefault('use_labelall', 0):
            for rect in rects:
                label_all(
                    self.ax,
                    rect,
                    kwargs.setdefault('use_labelall_rotate', 0),
                    kwargs.setdefault('use_labelall_percent', 0),
                    kwargs.setdefault('use_labelall_space', 0.01),
                    kwargs.setdefault('use_labelall_lim', 1.2))


    def draw_hist_err(self, **kwargs):
        benches = len(self.data[0])
        bars = len(self.data)/2
        ind = np.arange(start=0, stop=benches*3, step=3)
        width = 3.0/(bars+1)
        for i in range(bars):
            self.ax.bar(
                ind+i*width+width/2,
                self.data[i],
                width,
                # color=kwargs.setdefault('color', 'w'),
                color=get_color(i),
                edgecolor=get_color(i),
                ecolor = get_color(bars+i),
                # hatch=get_hatch(i),
                yerr=self.data[bars+i],
                label=self.legends[i])
        self.ax.set_ylabel(self.title)
        self.ax.set_xticks(ind+bars/2.0*width+width/2.0)
        self.fig.gca().set_ylim(
            kwargs.setdefault('y_start', 0),
            kwargs.setdefault('y_end', 1.2))
        self.fig.gca().set_xlim(0, benches*3)
        self.ax.set_xticklabels(
            self.xaxis,
            rotation=kwargs.setdefault('rotate', 0),
            fontsize=kwargs.setdefault('xaxis_fs', 9),
            va=kwargs.setdefault('xaxis_va', 'top'),
            ha=kwargs.setdefault('xaxis_ha', 'center'))
        if kwargs.setdefault('use_lgd', True):
            self.ax.legend(
                ncol=kwargs.setdefault('lgd_col', '8'),
                bbox_to_anchor=kwargs.setdefault('lgd_cord', (0., 1, 1., 0)),
                fontsize=kwargs.setdefault('lgd_fs', 9),
                loc='upper center')
        if kwargs.setdefault('use_percent', '0'):
            formatter = FuncFormatter(to_percent)
            self.fig.gca().yaxis.set_major_formatter(formatter)


    def draw_one_cdf(self, id, **kwargs):
        n_bins = 10000
        self.ax.hist(
            self.data,
            n_bins,
            normed=1,
            histtype='step',
            cumulative=True,
            edgecolor=get_color(id),
            linewidth=kwargs.setdefault('lw', 1.5),
            label=self.legends[id])
        self.ax.set_ylabel(self.title)
        self.fig.gca().set_ylim(
            kwargs.setdefault('y_start', 0),
            kwargs.setdefault('y_end', 1.2))
        self.fig.gca().set_xlim(
            kwargs.setdefault('x_start', 0),
            kwargs.setdefault('x_end', np.max(self.data)))
        if kwargs.setdefault('use_lgd', True):
            self.ax.legend(
                ncol=kwargs.setdefault('lgd_col', '8'),
                bbox_to_anchor=kwargs.setdefault('lgd_cord', (0., 1, 1., 0)),
                fontsize=kwargs.setdefault('lgd_fs', 9),
                loc='upper center')
        if kwargs.setdefault('use_percent', '0'):
            formatter = FuncFormatter(to_percent)
            self.fig.gca().yaxis.set_major_formatter(formatter)


    def draw_cdf(self, **kwargs):
        lines = len(self.data)
        n_bins = 10000
        for i in range(lines):
            self.ax.hist(
                self.data[i],
                n_bins,
                normed=1,
                histtype='step',
                cumulative=True,
                edgecolor=get_color(i),
                linewidth=kwargs.setdefault('lw', 1.5),
                label=self.legends[i])
        self.ax.set_ylabel(self.title)
        self.fig.gca().set_ylim(
            kwargs.setdefault('y_start', 0),
            kwargs.setdefault('y_end', 1.2))
        self.fig.gca().set_xlim(
            kwargs.setdefault('x_start', 0),
            kwargs.setdefault('x_end', np.max(self.data)))
        if kwargs.setdefault('use_lgd', True):
            self.ax.legend(
                ncol=kwargs.setdefault('lgd_col', '8'),
                bbox_to_anchor=kwargs.setdefault('lgd_cord', (0., 1, 1., 0)),
                fontsize=kwargs.setdefault('lgd_fs', 9),
                loc='upper center')
        if kwargs.setdefault('use_percent', '0'):
            formatter = FuncFormatter(to_percent)
            self.fig.gca().yaxis.set_major_formatter(formatter)


    def draw_line(self, **kwargs):
        benches = 0
        lines = len(self.data)
        for i in range(len(self.data)):
            if benches < len(self.data[i]):
                benches = len(self.data[i])
        xticks = np.arange(0, (benches+2), 1)
        indi = self.xticks[1:-1] - 0.5
        for i in range(lines):
            self.ax.plot(
                indi[:len(self.data[i])],
                self.data[i],
                color=get_color(i),
                linestyle=kwargs.setdefault('ls', '-'),
                linewidth=kwargs.setdefault('lw', 1.0),
                marker=get_marker(i),
                markersize=kwargs.setdefault('mrk_size', 5),
                markevery=kwargs.setdefault('mrk_inv', 1),
                label=self.legends[i])
        self.ax.set_ylabel(self.title)
        self.fig.gca().set_xlim(0, benches)
        self.fig.gca().set_ylim(
            kwargs.setdefault('y_start', 0),
            kwargs.setdefault('y_end', 1.2))
        self.ax.set_xticks(indi)
        self.ax.set_xticklabels(
            self.xaxis,
            rotation=kwargs.setdefault('rotate', 0),
            fontsize=kwargs.setdefault('xaxis_fs', 9),
            va=kwargs.setdefault('xaxis_va', 'top'),
            ha=kwargs.setdefault('xaxis_ha', 'center'))
        if kwargs.setdefault('use_lgd', True):
            legend = self.ax.legend(
                ncol=4,
                bbox_to_anchor=kwargs.setdefault('lgd_cord', (0., 1, 1., 0)),
                fontsize=9,
                loc=kwargs.setdefault('lgd_loc', 'upper center'))
            legend.get_frame().set_zorder(20)
        if kwargs.setdefault('use_percent', '0'):
            formatter = FuncFormatter(to_percent)
            # Set the formatter
            plt.gca().yaxis.set_major_formatter(formatter)


    def draw_one_line(self, id, **kwargs):
        benches = 0
        if benches < len(self.data):
            benches = len(self.data)
        xticks = np.arange(0, (benches+2), 1)
        indi = xticks[1:-1] - 0.5
        self.ax.plot(
            indi[:len(self.data)],
            self.data,
            color=get_color(id),
            linestyle=kwargs.setdefault('ls', '-'),
            linewidth=kwargs.setdefault('lw', 1.0),
            marker=get_marker(id),
            markersize=kwargs.setdefault('mrk_size', 5),
            markevery=kwargs.setdefault('mrk_inv', 1),
            label=self.legends)
        self.ax.set_ylabel(self.title)
        self.fig.gca().set_xlim(0, benches)
        self.fig.gca().set_ylim(
            kwargs.setdefault('y_start', np.min(self.data)-1),
            kwargs.setdefault('y_end', np.max(self.data)+1))
        self.ax.set_xticks(indi[::kwargs.setdefault('xaxis_inv', 1)])
        # xaxis = [int(i) for i in xaxis]
        # xaxis[0] = 1
        self.ax.set_xticklabels(
            self.xaxis[::kwargs.setdefault('xaxis_inv', 1)],
            rotation=kwargs.setdefault('xaxis_rotate', 0),
            fontsize=kwargs.setdefault('xaxis_fs', 9),
            va=kwargs.setdefault('xaxis_va', 'top'),
            ha=kwargs.setdefault('xaxis_ha', 'center'))
        if kwargs.setdefault('use_lgd', True):
            legend = self.ax.legend(
                ncol=4,
                bbox_to_anchor=kwargs.setdefault('lgd_cord', (0., 1, 1., 0)),
                fontsize=9,
                loc=kwargs.setdefault('lgd_loc', 'upper center'))
            legend.get_frame().set_zorder(20)
        if kwargs.setdefault('use_percent', '0'):
            formatter = FuncFormatter(to_percent)
            # Set the formatter
            plt.gca().yaxis.set_major_formatter(formatter)
