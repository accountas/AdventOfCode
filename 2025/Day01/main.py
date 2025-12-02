from common.data import *

def main():
    input = get_data(year=2025, day=1, sample=False).splitlines()
    
    zero_stops = 0
    zero_passes = 0
    cur_pos = 50

    for line in input:
        direction, amount = line[0], int(line[1:])
        prev_pos = cur_pos

        if direction == "R":
            cur_pos += amount
            zero_passes += cur_pos // 100
        else:
            cur_pos -= amount
            zero_passes += 0 if cur_pos > 0 else - cur_pos // 100 + (prev_pos != 0)
        
        cur_pos %= 100
        zero_stops += cur_pos == 0

    print("Part 1:", zero_stops)
    print("Part 2:", zero_passes)
    

if __name__ == "__main__":
    main()
    