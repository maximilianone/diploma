import matplotlib.pyplot as plt


def build_plot(statuses_distribution_sequence, time, statuses_names):
    fig = plt.figure()
    plt.grid(True)
    for i in range(len(statuses_distribution_sequence)):
        plt.plot(time, statuses_distribution_sequence[i], label=statuses_names[i])
    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=4, mode="expand", borderaxespad=1.)
    plt.show()
