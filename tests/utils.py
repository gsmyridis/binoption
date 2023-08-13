def lists_are_almost_equal(list1, list2, places):
    """
    Checks if lists are almost equal
    :param list1: first list
    :param list2: second list
    :param places: list entries to be equal to this number of places
    :return: True if they are almost equal, False otherwise
    """
    if len(list1) != len(list2):
        return False

    for sublist1, sublist2 in zip(list1, list2):
        if len(sublist1) != len(sublist2):
            return False

        for elem1, elem2 in zip(sublist1, sublist2):
            if isinstance(elem1, (int, float)) and isinstance(elem2, (int, float)):
                if round(elem1, places) != round(elem2, places):
                    return False
            elif elem1 != elem2:
                return False
    return True
