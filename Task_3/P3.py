def common_elements(set1, set2):
    return set1.intersection(set2)

if __name__ == "__main__":
    a = {1, 2, 3, 4}
    b = {3, 4, 5, 6}

    result = common_elements(a, b)
    print(result)