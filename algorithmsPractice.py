def recursiveSelectionSort(array, current, pos):
    if pos == len(array) - 1:
        return array
    elif array[pos] > array[pos + 1]:
        first = array[current]
        second = array[pos]

        array[current] = second
        array[pos] = first

        recursiveSelectionSort(array, current, pos + 1)
    else:
        recursiveSelectionSort(array, current,  pos + 1)


def selectionSort(array):
    for i in range(0, len(array)):
        if i == len(array):
            return array

        smallest = i
        for j in range(i, len(array)):
            #print j
            if array[j] < array[smallest]:
                first = array[smallest]
                second = array[j]

                array[smallest] = second
                array[j] = first
                return array




unsortedArray = [ 1, 3, 6, 7, 9, 4, 3, 5]

print selectionSort(unsortedArray)
#recursiveSelectionSort(unsortedArray, 0)
