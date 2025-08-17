# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
def can_attend_all_meetings():
    """
    Args:
     intervals(list_list_int32)
    Returns:
     int32
    """
    # Write your code here.
    intervals = [[1, 5],[4, 8]]

    start = []
    end = []

    for i in intervals:
        print(i)
        start.append(i[0])
        end.append(i[1])

        if start[i] < start[i+1]:
            return True

    return False



print(can_attend_all_meetings())