"""
inversion_count method is used to calculate the total number of inversions
in a given list consisting of different numbers

It is inspired by merge sort algorithm. Because I haven't mastered the mege sort algorithm and
recusive functions. So the following code was mainly from

https://www.geeksforgeeks.org/inversion-count-in-array-using-merge-sort/
"""



def merge(arr, left, mid, right):
    """
    This function merges left half of an array and the right half
    both left half and right half are sorted
    Parameters: mid = len(arr) //2
    left: leftest index for elements in the left half of arr
    right: rightest index in the right half of arr
    """
    i = left # starting index for elements in left half of arr
    j = mid # starting index for elements in right half of arr
    k = 0 # starting index for elements of to be sorted array
    counter = 0
    temp = [0 for x in range(right - left + 1)]
    while i < mid and j <= right:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            k += 1
            i += 1
        else:
            temp[k] = arr[j]
            counter += mid - i
            # when arr[i] > arr[j], all elements at left half after arr[i]
            # are greater than arr[j]. # of inversions will be mid - i
            k += 1
            j += 1
        
    while i < mid:
        temp[k] = arr[i]
        k += 1
        i += 1

    while j <= right:
        temp[k] = arr[j]
        k += 1
        j += 1
            
    k = 0
    # assign the sorted array back to original array
    for i in range(left, right+1):
        arr[i] = temp[k]
        k += 1

    return counter

        
def inversion_count(arr, left, right):
    # similar to merge sort algorithm,
    # we use divide and conquer method to count the # of inversions
    # when two sublists are merged

    counter = 0

    if right > left:
        mid = (right + left)//2

        counter += inversion_count(arr, left, mid)
        counter += inversion_count(arr, mid+1, right)
        counter += merge(arr, left, mid+1, right)

    return counter

def main():
    arr = [1, 20, 6, 4, 5]
####    n = len(arr)
####    print(inversion_count(arr, 0, n-1))

main()

