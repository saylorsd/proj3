import sys
from PageTable import PageTable, PageTableEntry

def parse_trace(line):
    addr, mode = line.rstrip('\n').split(' ')
    addr = int(addr, 16)
    return addr, mode

args = sys.argv

# Constants
ADDR_SIZE = 2 ** 32
PAGE_SIZE = 4 * (2 ** 10)
MAX_PAGES = ADDR_SIZE // PAGE_SIZE
frames = 0
traces = 0
replacement = ''

for i in range(len(args)):
    if '-n' in args[i]:
        frames = int(args[i+1])
    if '-a' in args[i]:
        replacement = args[i+1]
    if '-r' in args[i]:
        refresh_rate = int(args[i+1])

trace_file = args[-1]




opt_pages = [[] for _ in range(MAX_PAGES)]
# preprocess trace for opt
if 'opt' in replacement:

    print 'Preprocessing file for OPT...'
    i = 1
    with open(trace_file) as f:
        for line in f:
            addr, mode = parse_trace(line)
            opt_pages[addr//PAGE_SIZE].append(i)
            i += 1
    print 'Done!\n'
opt_size =0
for item in opt_pages:
    if len(item) > 0:
        opt_size+=1

print opt_size
pt = PageTable(MAX_PAGES, frames, replacement, opt_pages)

with open(trace_file) as f:
    for line in (f):
        traces += 1
        if traces % refresh_rate == 0:
            # print '--{} Traces Complete --'.format(traces)
            if replacement == 'nru':
                pt.refresh()
            if replacement == 'aging':
                pt.update_ages()
                pt.refresh()

        addr, mode = parse_trace(line)
        page = addr // PAGE_SIZE
        pt.load_page(page, mode)


    print '\nSTATS\n===='
    print  replacement.upper()
    print 'Frames:\t {}'.format(frames)
    print 'Traces:\t {:>7}'.format(traces)
    print 'Hits:\t {:>7}'.format(pt.hits)
    print 'Faults:\t {:>7}'.format(pt.faults)
    print 'Writes:\t {:>7}'.format(pt.disk_writes)


    print pt.first_access