class Nodo:
    def __init__(self, data):
        self.data = data
        self.left: Optional['Nodo'] = None
        self.right: Optional['Nodo'] = None