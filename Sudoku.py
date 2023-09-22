class Sudoku:
    def __init__(self):
        self._map = [0] * 9 * 3 * 3
        self._candidate_map = [{idx: 0 for idx in range(1, 10)} for _ in range(9 * 3 * 3)]

    def init(self, val_list):
        for idx, val in enumerate(val_list):
            if val > 0:
                self.set_val(idx % 9, idx // 9, val)

    def set_val(self, x, y, val):
        self._resume_candidate_map(x, y, self._map[y * 9 + x])

        if self._is_val_available(x, y, val):
            self._map[y * 9 + x] = val
            self._update_candidate_map(x, y, val)

        else:
            return False

        return True

    def clean_val(self, x, y):
        self._resume_candidate_map(x, y, self._map[y * 9 + x])
        self._map[y * 9 + x] = 0

    def _is_val_available(self, x, y, val):
        return self._candidate_map[y * 9 + x][val] >= 0

    def _update_candidate_map(self, x, y, val):
        if val < 1:
            return

        block_x = (x // 3) * 3
        block_y = (y // 3) * 3
        for i in range(9):
            self._candidate_map[i * 9 + x][val] -= 1
            self._candidate_map[y * 9 + i][val] -= 1

        for i in range(3):
            for j in range(3):
                self._candidate_map[(block_y + j) * 9 + block_x + i][val] -= 1

    def _resume_candidate_map(self, x, y, val):
        if val < 1:
            return

        block_x = (x // 3) * 3
        block_y = (y // 3) * 3
        for i in range(9):
            self._candidate_map[i * 9 + x][val] += 1
            self._candidate_map[y * 9 + i][val] += 1

        for i in range(3):
            for j in range(3):
                self._candidate_map[(block_y + j) * 9 + block_x + i][val] += 1

        self._map[y * 9 + x] = 0

    def get_map(self):
        return self._map

    def get_candidate_map(self):
        return self._candidate_map

    def reset(self):
        self._map[:] = [0] * 9 * 3 * 3
        for candidate_dict in self._candidate_map:
            for idx in range(1, 10):
                candidate_dict[idx] = 0
        # print(self._candidate_map)


def main():
    sudoku = Sudoku()
    sudoku.set_val(0, 0, 1)
    sudoku.set_val(0, 0, 2)


if __name__ == '__main__':
    main()
