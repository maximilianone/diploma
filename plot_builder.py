import matplotlib.pyplot as plt


def build_plot(statuses_distribution_sequence, statistic_values, time, statuses_names):
    fig = plt.figure()
    plt.grid(True)
    for i in range(len(statuses_distribution_sequence)):
        plt.plot(time, statuses_distribution_sequence[i], label=statuses_names[i])
    for i in range(len(statistic_values)):
        plt.plot(time, statistic_values[i], label=statuses_names[i] + ' statistic')
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=3, mode="expand", borderaxespad=1.)
    plt.show()
