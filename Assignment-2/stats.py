import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import wilcoxon, ttest_ind

def get_plot(data, mode = 'MLS'): 
    if mode == 'ILS':
        plt.plot(data[0], label = 'Mutation 0.01')
        plt.plot(data[1], label = 'Mutation 0.05')
        plt.plot(data[2], label = 'Mutation 0.1')
        plt.plot(data[3], label = 'Mutation 0.2')
        plt.plot(data[4], label = 'Mutation 0.3')
        plt.show()
        
        plt.boxplot(data)
        plt.xticks([1,2,3,4,5], ['ILS 0.01','ILS 0.05','ILS 0.1','ILS 0.2','ILS 0.3'])
        plt.show()
    if mode == 'MLS' or mode == 'GLS':
        plt.plot(data)
        plt.show()

        plt.boxplot(data)
        plt.xticks([1], [mode])
        plt.show()

    if mode == 'ALL':
        plt.boxplot(data)
        plt.xticks([1,2,3,4,5,6,7], ['MLS','ILS 0.01','ILS 0.05','ILS 0.1','ILS 0.2','ILS 0.3','GLS'])
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
    ils_data_03 = pd.read_csv('data/ils/ils_with_fm_0.3.csv')
    ils_performance_03 = pd.read_csv('data/ils/ils_with_fm_0.3_performance.csv')
    gls_data = pd.read_csv('data/gls/gls_with_fm.csv')
    gls_performance = pd.read_csv('data/gls/gls_with_fm_performance.csv')


    #### CUTSTATE ####
    data_001 = list(ils_data_03['cutstate'][:25])
    data_005 = list(ils_data_03['cutstate'][25:50])
    data_01 = list(ils_data_03['cutstate'][50:75])
    data_02 = list(ils_data_03['cutstate'][75:100])
    data_03 = list(ils_data_03['cutstate'][100:])

    gls_data_cutstate = get_gls_data(gls_data['Cutstate'])

    average_mls_data = np.mean(mls_data['cutstate'])
    average_ils_001 = np.mean(data_001)
    average_ils_005 = np.mean(data_005)
    average_ils_01 = np.mean(data_01)
    average_ils_02 = np.mean(data_02)
    average_ils_03 = np.mean(data_03)
    average_gls_data = np.mean(gls_data_cutstate)

    get_plot(mls_data['cutstate'], mode = 'MLS')
    get_plot([data_001, data_005, data_01, data_02, data_03], mode = 'ILS')
    get_plot(gls_data_cutstate, mode = 'GLS')
    get_plot([mls_data['cutstate'], data_001, data_005, data_01, data_02, data_03, gls_data_cutstate], mode = 'ALL')

    # Wilcoxon test
    wilcoxon_mls_gls = wilcoxon(mls_data['cutstate'], gls_data_cutstate)
    wilcoxon_mls_ils001 = wilcoxon(mls_data['cutstate'], data_001)
    wilcoxon_mls_ils005 = wilcoxon(mls_data['cutstate'], data_005)
    wilcoxon_mls_ils01 = wilcoxon(mls_data['cutstate'], data_01)
    wilcoxon_mls_ils02 = wilcoxon(mls_data['cutstate'], data_02)
    wilcoxon_mls_ils03 = wilcoxon(mls_data['cutstate'], data_03)
    wilcoxon_gls_ils001 = wilcoxon(gls_data_cutstate, data_001)
    wilcoxon_gls_ils005 = wilcoxon(gls_data_cutstate, data_005)
    wilcoxon_gls_ils01 = wilcoxon(gls_data_cutstate, data_01)
    wilcoxon_gls_ils02 = wilcoxon(gls_data_cutstate, data_02)
    wilcoxon_gls_ils03 = wilcoxon(gls_data_cutstate, data_03)

    #### CPU PERFORMANCE ####
    mls_performance_minutes = mls_performance['Execution Time'] / 60
    performance_001 = list(ils_performance_03['Execution Time'][:25] / 60)
    performance_005 = list(ils_performance_03['Execution Time'][25:50] / 60)
    performance_01 = list(ils_performance_03['Execution Time'][50:75] / 60)
    performance_02 = list(ils_performance_03['Execution Time'][75:100] / 60)
    performance_03 = list(ils_performance_03['Execution Time'][100:] / 60)
    gls_performance_minutes = gls_performance['Execution Time'] / 60

    average_mls_performance = np.mean(mls_performance_minutes)
    average_ils_performance001 = np.mean(performance_001)
    average_ils_performance005 = np.mean(performance_005)
    average_ils_performance01 = np.mean(performance_01)
    average_ils_performance02 = np.mean(performance_02)
    average_ils_performance03 = np.mean(performance_03)
    average_gls_performance = np.mean(gls_performance_minutes)

    #get_plot(mls_performance_minutes, mode = 'MLS')
    #get_plot([performance_001, performance_005, performance_01, performance_02, performance_03], mode = 'ILS')
    #get_plot(gls_performance_minutes, mode = 'GLS')
    #get_plot([mls_performance_minutes, performance_001, performance_005, performance_01, performance_02, performance_03, gls_performance_minutes], mode = 'ALL')

    # Wilcoxon test
    wilcoxon_performance_mls_gls = wilcoxon(mls_performance_minutes, gls_performance_minutes)
    wilcoxon_performance_mls_ils001 = wilcoxon(mls_performance_minutes, performance_001)
    wilcoxon_performance_mls_ils005 = wilcoxon(mls_performance_minutes, performance_005)
    wilcoxon_performance_mls_ils01 = wilcoxon(mls_performance_minutes, performance_01)
    wilcoxon_performance_mls_ils02 = wilcoxon(mls_performance_minutes, performance_02)
    wilcoxon_performance_mls_ils03 = wilcoxon(mls_performance_minutes, performance_03)
    wilcoxon_performance_gls_ils001 = wilcoxon(gls_performance_minutes, performance_001)
    wilcoxon_performance_gls_ils005 = wilcoxon(gls_performance_minutes, performance_005)
    wilcoxon_performance_gls_ils01 = wilcoxon(gls_performance_minutes, performance_01)
    wilcoxon_performance_gls_ils02 = wilcoxon(gls_performance_minutes, performance_02)
    wilcoxon_performance_gls_ils03 = wilcoxon(gls_performance_minutes, performance_03)
