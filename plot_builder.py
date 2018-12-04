import matplotlib.pyplot as plt


def build_plot(statuses_distribution_sequence, statistic_values, time, statuses_names):
    for i in range(len(statuses_distribution_sequence)):
        plt.grid(True)
        plt.plot(time, statuses_distribution_sequence[i], label=statuses_names[i])
        plt.plot(time, statistic_values[i], label=statuses_names[i] + ', статистика')
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        plt.tight_layout()
        plt.xlabel('Час, місяць')
        plt.ylabel('Люди')
        plt.show()
