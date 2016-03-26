from PageTable import PageTable, PageTableEntry

# Constants
MAX_FRAMES = 8
ADDR_SIZE = 2 ** 32
PAGE_SIZE = 4 * (2 ** 10)
MAX_PAGES = ADDR_SIZE // PAGE_SIZE

# Initialize stuff
trace_file = 'gcc.trace'
refresh_rate = 1000

frame_table = [None] * MAX_FRAMES



def parse_trace(line):
    addr, mode = line.rstrip('\n').split(' ')
    addr = int(addr, 16)
    return addr, mode



replacement = 'clock'
pt = PageTable(MAX_PAGES, MAX_FRAMES, replacement)
traces = 0

with open('traces/' + trace_file) as f:
    for line in (f):
        traces += 1

        if  traces % refresh_rate == 0:
            print '--{} Traces Complete --'.format(traces)
            if replacement == 'NRU':
                pt.refresh()

        addr, mode = parse_trace(line)
        page = addr // PAGE_SIZE
        pt.load_page(page, mode)

    print '\nSTATS\n===='
    print  replacement.capitalize()
    print 'Number of Frames:\t {}'.format(MAX_FRAMES)
    print 'Traces:\t {}'.format(traces)
    print 'Hits:\t {}'.format(pt.hits)
    print 'Faults:\t {}'.format(pt.faults)
    print 'Writes:\t {}'.format(pt.disk_writes)