import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon, ttest_ind

def get_plot(data, mode = 'MLS'): 
    if mode == 'ILS':
        plt.plot(data[0], label = 'Mutation 0.01')
        plt.plot(data[1], label = 'Mutation 0.03')
        plt.plot(data[2], label = 'Mutation 0.05')
        plt.show()
        
        plt.boxplot(data)
        plt.xticks([1,2,3], ['ILS 0.01','ILS 0.03','ILS 0.05'])
        plt.show()

    if mode == 'MLS':
        plt.plot(data)
        plt.show()

        plt.boxplot(data)
        plt.xticks([1], [mode])
        plt.show()    

    if mode == 'GLS':
        plt.plot(data[0], label = 'Population 20')
        plt.plot(data[1], label = 'Population 50')
        plt.show()

        plt.boxplot(data)
        plt.xticks([1, 2], ['GLS20', 'GLS50'])
        plt.show()

    if mode == 'ALL':
        plt.boxplot(data)
        plt.xticks([1,2,3,4,5,6], ['MLS','ILS 0.01','ILS 0.03','ILS 0.05','GLS20','GLS50'])
        plt.show()

def get_gls_data(data):
    gls_data_cutstate = []
    # Convert the list of strings to numeric values
    for cut_value in data:
        cut_value = cut_value.replace(']', '[').split('[')
        if len(cut_value) > 0:
            gls_data_cutstate.append(int(cut_value[1]))
    return gls_data_cutstate

if __name__ == '__main__':
    # Read data
    mls_data = pd.read_csv('data/mls/mls_with_fm.csv')
    mls_performance = pd.read_csv('data/mls/mls_with_fm_performance.csv')
    ils_data_005 = pd.read_csv('data/ils/ils_with_fm_0.05.csv')
    ils_performance_005 = pd.read_csv('data/ils/ils_with_fm_0.05_performance.csv')
    gls_data = pd.read_csv('data/gls/gls_with_fm.csv')
    gls_performance = pd.read_csv('data/gls/gls_with_fm_performance.csv')
    gls_data_20 = pd.read_csv('data/gls/gls_with_fm_20.csv')
    gls_performance_20 = pd.read_csv('data/gls/gls_with_fm_performance_20.csv')


    #### CUTSTATE ####
    data_001 = list(ils_data_005['cutstate'][:25])
    data_003 = list(ils_data_005['cutstate'][25:50])
    data_005 = list(ils_data_005['cutstate'][50:])

    gls_data_cutstate = get_gls_data(gls_data['Cutstate'])
    gls_data_cutstate_20 = get_gls_data(gls_data_20['Cutstate'])

    average_mls_data = np.mean(mls_data['cutstate'])
    average_ils_001 = np.mean(data_001)
    average_ils_003 = np.mean(data_003)
    average_ils_005 = np.mean(data_005)
    average_gls_data = np.mean(gls_data_cutstate)
    average_gls_data = np.mean(gls_data_cutstate_20)

    get_plot(mls_data['cutstate'], mode = 'MLS')
    get_plot([data_001, data_003, data_005], mode = 'ILS')
    get_plot([gls_data_cutstate_20, gls_data_cutstate], mode = 'GLS')
    get_plot([mls_data['cutstate'], data_001, data_003, data_005, gls_data_cutstate_20, gls_data_cutstate], mode = 'ALL')

    # Wilcoxon test
    wilcoxon_mls_gls = wilcoxon(mls_data['cutstate'], gls_data_cutstate)
    wilcoxon_mls_ils001 = wilcoxon(mls_data['cutstate'], data_001)
    wilcoxon_mls_ils003 = wilcoxon(mls_data['cutstate'], data_003)
    wilcoxon_mls_ils005 = wilcoxon(mls_data['cutstate'], data_005)
    wilcoxon_gls_ils001 = wilcoxon(gls_data_cutstate, data_001)
    wilcoxon_gls_ils003 = wilcoxon(gls_data_cutstate, data_003)
    wilcoxon_gls_ils005 = wilcoxon(gls_data_cutstate, data_005)
    print(wilcoxon_mls_gls)

    #### CPU PERFORMANCE ####
    mls_performance_minutes = mls_performance['Execution Time'] / 60
    performance_001 = list(ils_performance_005['Execution Time'][:25] / 60)
    performance_003 = list(ils_performance_005['Execution Time'][25:50] / 60)
    performance_005 = list(ils_performance_005['Execution Time'][50:75] / 60)
    gls_performance_minutes = gls_performance['Execution Time'] / 60
    gls_performance_minutes_20 = gls_performance_20['Execution Time'] / 60

    average_mls_performance = np.mean(mls_performance_minutes)
    average_ils_performance001 = np.mean(performance_001)
    average_ils_performance003 = np.mean(performance_003)
    average_ils_performance005 = np.mean(performance_005)
    average_gls_performance = np.mean(gls_performance_minutes)
    average_gls_performance_20 = np.mean(gls_performance_minutes_20)

    get_plot(mls_performance_minutes, mode = 'MLS')
    get_plot([performance_001, performance_003, performance_005], mode = 'ILS')
    get_plot([gls_performance_minutes_20, gls_performance_minutes], mode = 'GLS')
    get_plot([mls_performance_minutes, performance_001, performance_003, performance_005, gls_performance_minutes_20, gls_performance_minutes], mode = 'ALL')

    # Wilcoxon test
    wilcoxon_performance_mls_gls = wilcoxon(mls_performance_minutes, gls_performance_minutes)
    wilcoxon_performance_mls_ils001 = wilcoxon(mls_performance_minutes, performance_001)
    wilcoxon_performance_mls_ils003 = wilcoxon(mls_performance_minutes, performance_003)
    wilcoxon_performance_mls_ils005 = wilcoxon(mls_performance_minutes, performance_005)
    wilcoxon_performance_gls_ils001 = wilcoxon(gls_performance_minutes, performance_001)
    wilcoxon_performance_gls_ils003 = wilcoxon(gls_performance_minutes, performance_003)
    wilcoxon_performance_gls_ils005 = wilcoxon(gls_performance_minutes, performance_005)
