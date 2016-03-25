# Constants
MAX_FRAMES = 10
ADDR_SIZE = 2 ** 32
PAGE_SIZE = 4 * (2 ** 10)
MAX_PAGES = ADDR_SIZE // PAGE_SIZE

# Initialize stuff
trace_file = 'bzip.trace'
page_table = [None] * MAX_PAGES
frame_table = [None] * MAX_FRAMES
'''
pte = {
    'page': '',
    'dirty': '',
    'ref': '',
    'valid' ''
}
'''


def parse_trace(line):
    addr, mode = line.rstrip('\n').split(' ')
    addr = int(addr, 16)
    return addr, mode


def split_virtual_address(addr):
    page_num = addr // PAGE_SIZE
    offset = addr % PAGE_SIZE
    return page_num, offset


def map_address(addr, mode):
    page_num, offset = split_virtual_address(addr)
    # check page table for page's PTE
    pte = page_table[page_num]

    # if it's not loaded into a frame
    if pte is None:
        page_table[page_num] = {
            'frame': get_frame(),
            'dirty': True if 'w' in mode else False,
            'ref': True,
            'valid': True
        }


def get_frame():
    pass


def evict():
    pass


with open('traces/' + trace_file) as f:
    for line in (f):
        # get address
        addr, mode = parse_trace(line)

        # get page of address/ try to map it
        map_address(addr, mode)

'''
- get address
- find page address belongs to
- try to map it
- if it is, hit! - do nothing
- if it's not:
    - map it!
        - enter into free space if available
        - evict old one if necessary (using different algorithms)
            - evict dirty (w)
            - evict clean (r)



'''
