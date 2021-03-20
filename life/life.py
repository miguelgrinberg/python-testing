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
    def __init__(self, survival=None, birth=None):
        self.survival = survival or [2, 3]
        self.birth = birth or [3]
        self.alive = CellList()

    def load(self, filename):
        with open(filename, "rt") as f:
            header = f.readline()
            if header == '#Life 1.05\n':
                x = y = 0
                for line in f.readlines():
                    if line.startswith('#D'):
                        continue
                    elif line.startswith('#N'):
                        self.survival = [2, 3]
                        self.birth = [3]
                    elif line.startswith('#R'):
                        self.survival, self.birth = [
                            [int(n) for n in i]
                            for i in line[2:].strip().split('/', 1)]
                    elif line.startswith('#P'):
                        x, y = [int(i) for i in line[2:].strip().split(' ', 1)]
                    else:
                        i = line.find('*')
                        while i != -1:
                            self.alive.set(x + i, y, True)
                            i = line.find('*', i + 1)
                        y += 1
            elif header == '#Life 1.06\n':
                for line in f.readlines():
                    if not line.startswith('#'):
                        x, y = [int(i) for i in line.strip().split(' ', 1)]
                        self.cells.set(x, y, True)
            else:
                raise RuntimeError('Unknown file format')

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
            return neighbors in self.survival
        else:
            return neighbors in self.birth
