class CellList:
    def __init__(self):
        self.cells = {}

    def has(self, x, y):
        return x in self.cells.get(y, [])

    def set(self, x, y, value=None):
        if value is None:
            value = not self.has(x, y)
        if value:
            row = self.cells.setdefault(y, set())
            if x not in row:
                row.add(x)
        else:
            try:
                self.cells[y].remove(x)
            except KeyError:
                pass
            else:
                if not self.cells[y]:
                    del self.cells[y]

    def __iter__(self):
        for y in self.cells:
            for x in self.cells[y]:
                yield (x, y)


class Life:
    def __init__(self):
        self.alive = CellList()

    def load(self, filename, x, y):
        with open(filename, "rt") as f:
            for line in f.readlines():
                i = line.find('*')
                while i != -1:
                    self.alive.set(x + i, y, True)
                    i = line.find('*', i + 1)
                y += 1

    def bounding_box(self):
        min_x = min_y = max_x = max_y = None
        for cell in self.alive:
            x = cell[0]
            y = cell[1]
            if min_x is None or x < min_x:
                min_x = x
            if min_y is None or y < min_y:
                min_y = y
            if max_x is None or x > max_x:
                max_x = x
            if max_y is None or y > max_y:
                max_y = y
        return (min_x or 0, min_y or 0, max_x or 0, max_y or 0)

    def advance(self):
        new_alive = CellList()
        for cell in self.alive:
            x = cell[0]
            y = cell[1]
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if self.advance_cell(x + i, y + j):
                        new_alive.set(x + i, y + j, True)
        self.alive = new_alive

    def advance_cell(self, x, y):
        neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    neighbors += 1 if self.alive.has(x + i, y + j) else 0

        if self.alive.has(x, y):
            if neighbors < 2:
                return False
            elif neighbors > 3:
                return False
            else:
                return True
        elif neighbors == 3:
            return True
        else:
            return False
