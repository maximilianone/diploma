import matplotlib.pyplot as plt


def build_plot(statuses_distribution_sequence, statistic_values, time, statuses_names, medical_statuses_names):
    for i in range(len(statuses_distribution_sequence)):
        fig = plt.figure()
        plt.grid(True)
        for j in range(len(statuses_distribution_sequence[i])):
            plt.plot(time, statuses_distribution_sequence[i][j],
                     label=statuses_names[i] + ' ' + medical_statuses_names[j])
            plt.plot(time, statistic_values[i][j],
                     label=statuses_names[i] + ' ' + medical_statuses_names[j] + ' statistic')
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=4, ncol=3, mode="expand", borderaxespad=1.)
        plt.show()
