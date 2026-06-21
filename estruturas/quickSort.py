def quickSort(array, chave=lambda x: x):
    """
    Ordena um array in-place utilizando o algoritmo Quicksort adaptado do C.
    Utiliza mediana de 3 e particionamento de Sedgewick/Hoare.
    """
    _quickSortRecursivo(array, 0, len(array) - 1, chave)


def _cmpexch(array, i, j, chave):
    if chave(array[j]) < chave(array[i]):
        array[i], array[j] = array[j], array[i]


def _particionar(array, l, r, chave):
    i = l - 1
    j = r
    pivot_val = chave(array[r])

    while True:
        i += 1
        while chave(array[i]) < pivot_val:
            i += 1
            
        j -= 1
        while pivot_val < chave(array[j]) and j > l:
            j -= 1
            
        if i >= j:
            break
            
        array[i], array[j] = array[j], array[i]
        
    array[i], array[r] = array[r], array[i]
    return i


def _quickSortRecursivo(array, l, r, chave):
    if r <= l:
        return

    meio = (l + r) // 2
    
    _cmpexch(array, l, meio, chave)
    _cmpexch(array, l, r, chave)
    _cmpexch(array, r, meio, chave)

    p = _particionar(array, l, r, chave)
    _quickSortRecursivo(array, l, p - 1, chave)
    _quickSortRecursivo(array, p + 1, r, chave)
