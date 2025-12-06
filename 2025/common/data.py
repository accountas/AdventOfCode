from aocd import get_data as aocd_get_data

def get_data(year, day, sample = False):
    if not sample:
        return aocd_get_data(year=year, day=day)
    
    with open(f"Day{str(day).rjust(2, '0')}/sample.txt") as f:
        return f.read()