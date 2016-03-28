import os

methods = ['nru', 'clock', 'aging', 'opt']
frame_counts = ['8', '16', '32', '64']
refresh_rate = '1000'

for method in methods:
    for frame_count in frame_counts:
        call = 'py E:/Projects/vm_simulator/vmsim.py -n {} -a {} -r {} ./traces/bzip.trace'.format(frame_count, method, refresh_rate)
        os.system(call)