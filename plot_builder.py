import matplotlib.pyplot as plt


def build_plot(statuses_distribution_sequence, statistic_values, time, statuses_names, medical_statuses_names):
    for i in range(len(statuses_distribution_sequence)):
        f, axarr = plt.subplots(len(statuses_distribution_sequence[i]))
        plt.grid(True)
        for j in range(len(statuses_distribution_sequence[i])):
            axarr[j].plot(time, statuses_distribution_sequence[i][j],
                     label=statuses_names[i] + ' ' + medical_statuses_names[j])
            axarr[j].plot(time, statistic_values[i][j],
                     label=statuses_names[i] + ' ' + medical_statuses_names[j] + ' statistic')
            axarr[j].legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        plt.tight_layout()
        plt.show()
