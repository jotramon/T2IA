# Usando la búsqueda BFS, este programa genera una base de datos de patrones
# En una abstracción del espacio de búsqueda, realiza BFS desde el estado final
# hasta que visita todos los estados del espacio (abstracto) de búsqueda

import sys
from node import Node
from puzzle import Puzzle


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def is_empty(self):
        return (self.items == [])

    def __repr__(self):
        return str(self.items) + ' (el del principio se muestra primero) '

    def __len__(self):
        return len(self.items)

    def insert(self, item):
        self.enqueue(item)

    def extract(self):
        return self.dequeue()


class GenericSearch:
    def __init__(self, initial_state, strategy, file):
        self.expansions = 0
        self.initial_state = initial_state
        self.strategy = strategy
        self.max_depth = 0
        self.file = file

    def _newopen(self):
        if self.strategy == 'bfs':
            return Queue()
        else:
            print(type, 'is not supported')
            sys.exit(1)

    def write_state(self, state, depth):
        self.file.write(' '.join([str(n) for n in state.board]) + ' ' + str(depth) + '\n')

    def search(self):
        self.open = self._newopen()
        self.expansions = 0
        self.open.insert(Node(self.initial_state))
        self.generated = set()  ## generated mantiene la union entre OPEN y CLOSED
        self.generated.add(self.initial_state)
        while not self.open.is_empty():
            n = self.open.extract()   # extrae n de la open
            self.write_state(n.state, n.depth)
            if n.depth > self.max_depth:
                self.max_depth = n.depth
                print('Generando estados a profundidad', n.depth)
            succ = n.state.successors()
            self.expansions += 1
            for child_state, action, _ in succ:
                if child_state in self.generated:  # en DFS este chequeo se puede hacer sobre la rama
                    continue
                child_node = Node(child_state, n, action)
                # Aquí un BFS normal habría preguntado si child_node es un estado
                # objetivo. Esta versión no lo hace pues queremos explorar todo el espacio
                # de búsqueda
                self.generated.add(child_state)
                self.open.insert(child_node)
        return None


def abstract(board, pattern):
    '''
      retorna la versión abstracta de board según pattern
    '''
    abstract_board = []
    for x in board:
        if x in pattern or x == 0:
            abstract_board.append(x)
        else:
            abstract_board.append(-1)
    return abstract_board

# Así es como se ve el puzle original
# 0  1  2  3
# 4  5  6  7
# 8  9 10 11
#12 13 14 15

pattern = [2, 3, 7, 11]  # patron a utilizar: todo lo que no está en esta lista se transforma en -1
# al usar el patrón de la línea anterior, el estado final abstracto se ve así:
# 0 -1  2  3
#-1 -1 -1  7
#-1 -1 -1 11
#-1 -1 -1 -1


abstract_init = abstract(list(range(16)), pattern)  ## generamos estado inicial en donde se abstrae a -1 todo lo que no esta en pattern
init = Puzzle(abstract_init)

f = open('pdb1.txt', 'w')
f.write(' '.join([str(x) for x in pattern])+'\n') ## escribimos el patron en el archivo
s = GenericSearch(init, 'bfs', f)  # iniciamos un BFS desde el estado final abstracto
result = s.search()
print('Total de estados generados :', len(s.generated))
f.close()
