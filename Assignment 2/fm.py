import numpy as np
import pandas as pd
from tqdm import tqdm


def convert_to_dataframe(filename):
    
    data = pd.DataFrame(columns = ['ID', 'coordinates', 'number connections', 'ID connections'])

    with open(filename) as f:
        graph = f.read()
    
    graph = graph.split('\n')

    for line in tqdm(graph):
        l = line.split()
        if len(l) > 0:
            data = data.append({'ID': l[0], 'coordinates': l[1], 
                'number connections': l[2], 'ID connections': l[3:]}, ignore_index=True)

    return data

if __name__ == '__main__':

    np.random.seed(352)

    graph = convert_to_dataframe('Graph500.txt')
    print(graph)
