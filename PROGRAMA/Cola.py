# cola.py

class Cola:
    def __init__(self):
        self.items = []

    def enqueue(self, mission):
        """ Añadir misión al final de la cola """
        self.items.append(mission)

    def dequeue(self):
        """ Eliminar y retornar la primera misión """
        if not self.is_empty():
            return self.items.pop(0)
        raise IndexError("La cola está vacía")

    def first(self):
        """ Ver la primera misión sin removerla """
        if not self.is_empty():
            return self.items[0]
        raise IndexError("La cola está vacía")

    def is_empty(self):
        """ Verificar si la cola está vacía """
        return len(self.items) == 0

    def size(self):
        """ Obtener cantidad de misiones """
        return len(self.items)