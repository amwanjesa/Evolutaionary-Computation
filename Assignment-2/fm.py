import numpy as np
import pandas as pd
from tqdm import tqdm

def convert_to_dataframe(filename):
    data = pd.DataFrame(columns = ['ID', 'coordinates', 'number_connections', 'ID_connections'])
    with open(filename) as f:
        graph = f.read()
    
    graph = graph.split('\n')

    for line in tqdm(graph):
        l = line.split()
        if len(l) > 0:
            data = data.append({'ID': l[0], 'coordinates': l[1], 
                'number_connections': l[2], 'ID_connections': l[3:]}, ignore_index=True)
    return data

def MLS(graph):
    cell_distribution = {}

    #random division in two subsets
    graph_array = np.random.choice(2, graph.shape[0])

    for index, row in tqdm(graph.iterrows()):
        subset_A = 0
        for num in row.ID_connections:
            if graph_array[int(num)-1] == 1:
                subset_A += 1

        if row.ID in cell_distribution:
            cell_distribution[row.ID].append([graph_array[int(row.ID)-1], subset_A, int(row.number_connections)-subset_A])
        else:
            cell_distribution[row.ID] = [graph_array[int(row.ID)-1], subset_A, int(row.number_connections)-subset_A]
    
    return cell_distribution


if __name__ == '__main__':

    np.random.seed(352)

    graph = convert_to_dataframe('Graph500.txt')
    cell_distribution = MLS(graph)

    

