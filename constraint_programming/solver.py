#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymzn

'''
Older versions of pymzn and Minizinc could be configured like this:

pymzn.config.set('mzn2fzn', 'C:\\Program Files\\MiniZinc IDE (bundled)\\mzn2fzn')
pymzn.config.set('solns2out', 'C:\\Program Files\\MiniZinc IDE (bundled)\\solns2out')
pymzn.config.set('solver', pymzn.Gecode(mzn_path='C:\\Program Files\\MiniZinc IDE (bundled)\\mzn-gecode.bat',
                                        fzn_path='C:\\Program Files\\MiniZinc IDE (bundled)\\fzn-gecode'))
'''

# Change this variable if you did not install Minizinc in the default path
pymzn.config['minizinc'] = 'C:\\Program Files\\MiniZinc\\minizinc.exe'


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')
    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    parents = []
    children = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        parents.append(int(parts[0]))
        children.append(int(parts[1]))

    # build a trivial solution
    # every node has its own color
    solution = pymzn.minizinc('grafos.mzn', data=dict(Nodes=node_count, Edges=edge_count, n_p=parents, n_h=children),
                              output_mode='dict', parallel=4)[0]

    # prepare the solution in the specified output format

    output_data = str(solution['mc']+1) + ' ' + str(0) + '\n'
    for i in solution['colors']:
        output_data += str(solution['colors'][i]) + ' '

    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py '
              './data/gc_4_1)')
