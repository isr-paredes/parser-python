def flatten(lst):
    return [item for sublist in lst for item in sublist]
print(flatten([[1,2], [3,4]]))