import unittest

from estruturas.quickSort import quickSort

class ObjetoTeste:
    def __init__(self, valor):
        self.valor = valor

class TestQuickSort(unittest.TestCase):
    def testOrdenaVetorVazioOuUnitario(self):
        vetor = []
        quickSort(vetor)
        self.assertEqual(vetor, [])

        vetor = [5]
        quickSort(vetor)
        self.assertEqual(vetor, [5])

    def testOrdenaVetorPequeno(self):
        vetor = [3, 1, 2]
        quickSort(vetor)
        self.assertEqual(vetor, [1, 2, 3])
        
        vetor = [4, 3, 2, 1]
        quickSort(vetor)
        self.assertEqual(vetor, [1, 2, 3, 4])

    def testOrdenaVetorComNumeros(self):
        vetor = [10, 7, 8, 9, 1, 5, 2, 4, 3, 6]
        quickSort(vetor)
        self.assertEqual(vetor, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def testOrdenaVetorJaOrdenadoInvertido(self):
        vetor = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        quickSort(vetor)
        self.assertEqual(vetor, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    def testOrdenaVetorComElementosRepetidos(self):
        vetor = [4, 1, 3, 4, 2, 4, 1, 3]
        quickSort(vetor)
        self.assertEqual(vetor, [1, 1, 2, 3, 3, 4, 4, 4])

    def testOrdenaComChaveCustomizada(self):
        vetor = [
            ObjetoTeste(10),
            ObjetoTeste(2),
            ObjetoTeste(8),
            ObjetoTeste(5)
        ]
        quickSort(vetor, chave=lambda x: x.valor)
        self.assertEqual([obj.valor for obj in vetor], [2, 5, 8, 10])

if __name__ == "__main__":
    unittest.main()
