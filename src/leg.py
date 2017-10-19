class Leg:
    '''
    Leg represents positions in a lexical database to search
    start: int - start from
    stop:  int - stop at
    count: int - how many words to generate
    '''
    def __init__(self, start, stop, count, group):
        self.start = start
        self.stop  = stop
        self.count = count
        self.group = group 
