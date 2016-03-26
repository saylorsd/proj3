# Constants
MAX_FRAMES = 10
ADDR_SIZE = 2 ** 32
PAGE_SIZE = 4 * (2 ** 10)
MAX_PAGES = ADDR_SIZE // PAGE_SIZE
hits = 0
faults = 0

# Initialize stuff
trace_file = 'bzip.trace'
page_table = [None] * MAX_PAGES
frame_table = [None] * MAX_FRAMES

def parse_trace(line):
    addr, mode = line.rstrip('\n').split(' ')
    addr = int(addr, 16)
    return addr, mode


def split_virtual_address(addr):
    page_num = addr // PAGE_SIZE
    offset = addr % PAGE_SIZE
    return page_num, offset


def map_address(addr, mode):
    '''
    Adds address

    returns:
        hit, frame  (if it's a hit, and frame number)
    '''
    page_num, offset = split_virtual_address(addr)
    # check page table for page's PTE

    # if it's not loaded into a frame
    if page_table[page_num] is None:
        # make new PTE for it
        page_table[page_num] = {
            'frame': get_frame(),
            'dirty': True if 'w' in mode else False,
            'ref': True,
            'valid': True,
            'page' : page_num,
            'offset': offset,
            'addr': addr
        }
        hit = False
    # else, it's already loaded into the frame
    else:
        hit = True
        hits += 1

    # copy pte to frame list
    frame_table[page_table[page_num]['frame']] = page_table[page_num]

    return hit, page_table[page_num]['frame']


def get_frame():
    # cycle through frames
    reffed = []
    unreffed = []
    for i in range(len(frame_table)):
        if frame_table[i] is None:
            return i
        elif frame_table[i]['ref']:
            reffed.append(i)
        else:
            unreffed.append(i)
    if len(unreffed)>0:
        return unreffed[0]
    else :
        return reffed[0]


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
