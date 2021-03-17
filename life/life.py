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

    def living_cells(self):
        return self.alive.__iter__()

    def bounding_box(self):
        minx = miny = maxx = maxy = None
        for cell in self.living_cells():
            x = cell[0]
            y = cell[1]
            if minx is None or x < minx:
                minx = x
            if miny is None or y < miny:
                miny = y
            if maxx is None or x > maxx:
                maxx = x
            if maxy is None or y > maxy:
                maxy = y
        return (minx or 0, miny or 0, maxx or 0, maxy or 0)

    def advance(self):
        processed = CellList()
        new_alive = CellList()
        for cell in self.living_cells():
            x = cell[0]
            y = cell[1]
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (x + i, y + j) in processed:
                        continue
                    processed.set(x + i, y + j, True)
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
