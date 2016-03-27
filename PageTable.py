from copy import deepcopy
from itertools import cycle


class PageTableEntry(object):
    def __init__(self, page, mode):
        self.page = page
        self.frame = None

        self.valid = True
        self.ref = True
        self.dirty = True if 'W' in mode else False

        self.aging = 0

    def refresh(self):
        self.ref = False

    def reset(self):
        ''' Reset to default values after eviction
        '''
        self.frame = None
        self.valid = False
        self.ref = False
        self.dirty = False
        self.aging = 0

    def refer(self, mode):
        self.ref = True
        if 'W' in mode:
            self.dirty = True

class PageTable(object):
    def __init__(self, pages, frames, pr_method, opt_list=None):
        self.size = pages
        self.frames = frames
        self.trace_count = 0
        self.page_table = [None] * pages
        self.frame_table = [None] * frames
        self.empty_frames = frames

        # Performance measures
        self.hits = 0
        self.faults = 0
        self.disk_writes = 0

        self.pr_method = pr_method  # method of page-replacemnt to use during evictions

        # Replacement-specific data structures
        self.fifo = [None for x in range(frames)]
        self.clock_ptr = 0
        self.opt_list=opt_list

    def load_page(self, page, mode):
        ''' Takes page # from virtual address and loads it into physical memory
        '''
        # check if it's already loaded
        if self.search_frame_table(page):
            self.page_table[page].refer(mode)
            self.hits += 1
            return

        # if no space in RAM, we need to use a page replacement algorithm to pick what to evict
        elif self.empty_frames == 0:
            evicted = self.evict()  # page to be evicted
            cleared_frame = evicted.frame
            evicted.reset()
        else:
            cleared_frame = self.get_empty_frame()
            self.empty_frames -= 1

        self.faults += 1

        # Create PTE for current attemp at loading address
        temp_page = PageTableEntry(page, mode)
        temp_page.frame = cleared_frame
        temp_page.valid = True
        temp_page.ref = True

        # add page to page and frame tables
        self.page_table[page] = deepcopy(temp_page)
        self.frame_table[cleared_frame] = self.page_table[page]

        # if using clock, add this new page to where hand is pointing
        # if there wasn't a free frame, evict() will have moved ptr to frame to evict
        if 'clock' in self.pr_method:
            self.fifo[self.clock_ptr] = self.page_table[page]
            self.clock_ptr = (self.clock_ptr + 1) % self.frames  # move clock ptr ahead

        self.trace_count += 1



    def evict(self):
        ''' Choose which frame needs to be evicted when a page fault occurs
        '''
        evicted_frame = getattr(self, self.pr_method)()
        if evicted_frame.dirty:
            self.disk_writes += 1
        return evicted_frame

    def get_empty_frame(self):
        ''' Cycles through frame table and finds the next free frame
        '''
        for frame in range(len(self.frame_table)):
            if self.frame_table[frame] is None:
                return frame

        return -1

    def search_frame_table(self, page):
        pte = self.page_table[page]
        if pte is None:
            return False
        else:
            return pte.frame is not None

    def refresh(self):
        ''' Refreshes all loaded pages
        '''
        for frame in self.frame_table:
            try:
                frame.refresh()
            except:
                continue


    '''
    PAGE REPLACEMENT ALGORITHMS
    '''

    def nru(self):
        nru_classes = [[] for _ in range(4)]
        # categorize loaded frames
        for frame in self.frame_table:
            ref = 2 if frame.ref else 0
            dirty = 1 if frame.dirty else 0
            i = ref + dirty
            nru_classes[i].append(frame)

        # cycle through classes from first choice to last choice until a frame is found
        for nru_class in nru_classes:
            if len(nru_class):
                return nru_class[0]

    def clock(self):
        i = self.clock_ptr
        while(1):
            if not self.fifo[i].ref:
                self.clock_ptr = i
                return self.fifo[i]
            else:
                self.fifo[i].ref = False
                i = (i+1) % self.frames

    def aging(self):
        lowest = 256
        oldest = None
        for page in self.frame_table:
            if page.aging < lowest:
                oldest = page
                lowest = page.aging
            # TODO: tie-breaker
        return oldest

    def update_ages(self):
        # go through each frame and update their aging counters
        for frame in self.frame_table:
            frame.aging = (frame.aging >> 1)
            if frame.ref:
               frame.aging  = frame.aging | 0b10000000

    def opt(self):
        longest = 0
        evicted_page = None
        count = self.trace_count
        for page in self.frame_table:
            score = self.get_opt_score(page.page)
            if score > longest:
                longest = score
                evicted_page = page

        return evicted_page


    def get_opt_score(self, page_num):
        while(len(self.opt_list[page_num])):
            timing = self.opt_list[page_num].pop(0)
            score = timing - self.trace_count
            if score > 0:
                return score

        return len(self.opt_list) + 1
