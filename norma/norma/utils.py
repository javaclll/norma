def get_or_none(alist, index):
    try:
        return alist[index]
    except:
        return None


def get_or_zero(alist, index):
    try:
        return alist[index]
    except:
        return 0


def two_in_one_merge(items):
    merged_list = []
    for i in range(int(len(items) / 2) + 1):
        item1 = get_or_none(items, 2 * i)
        item2 = get_or_none(items, 2 * i + 1)

        if not (item1 == None and item2 == None):
            merged_list.append((item1 or 0) + (item2 or 0))

    return merged_list
