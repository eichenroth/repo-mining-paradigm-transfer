import matplotlib.pyplot as plt

from src.utils.settings import Settings


class Plotter:
    def __init__(self, figsize=(800, 600)):
        settings = Settings()
        self.figsize = figsize
        self.plot_dir = settings.get_path('plots')

    def __call__(self, aggregations, labels, title, save=True, show=False):
        median_color = '#b1063a'
        dpi = 100
        figsize = (self.figsize[0] / dpi, self.figsize[1] / dpi)

        plt.figure(figsize=figsize)
        plt.grid(True, axis='y')
        plt.title(title)

        plt.boxplot(aggregations,
                    labels=labels,
                    medianprops={'color': median_color, 'linewidth': 2},
                    boxprops={'linewidth': 2},
                    whiskerprops={'linewidth': 2},
                    capprops={'linewidth': 2})

        if save:
            file_title = title.lower().replace(' ', '_')
            file = '{}/{}.png'.format(self.plot_dir, file_title)
            plt.savefig(file)

        if show:
            plt.show()
