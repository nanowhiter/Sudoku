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

    def get_hint(self):
        # Vertical
        for i in range(9):
            candidate_counter = {idx: 0 for idx in range(1, 10)}
            for j in range(9):
                if self._map[j * 9 + i] == 0:
                    print(i, j, self._candidate_map[j * 9 + i])
                    for val in range(1, 10):
                        if self._is_val_available(i, j, val):
                            candidate_counter[val] += 1
            for key, val in candidate_counter.items():
                print(key)
                if val == 1:
                    return 0, i, 0

        # Horizontal
        for j in range(9):
            candidate_counter = {idx: 0 for idx in range(1, 10)}
            for i in range(9):
                if self._map[j * 9 + i] == 0:
                    for val in range(1, 10):
                        if self._is_val_available(i, j, val):
                            candidate_counter[val] += 1
            for key, val in candidate_counter.items():
                if val == 1:
                    return 1, 0, j

        # Block
        for block_i in range(3):
            for block_j in range(3):
                candidate_counter = {idx: 0 for idx in range(1, 10)}
                for i in range(3):
                    for j in range(3):
                        idx_i = block_i * 3 + i
                        idx_j = block_j * 3 + j
                        if self._map[idx_j * 9 + idx_i] == 0:
                            for val in range(1, 10):
                                if self._is_val_available(idx_i, idx_j, val):
                                    candidate_counter[val] += 1
                            # candidate_counter[self._candidate_map[idx_j * 9 + idx_i]] += 1

                for key, val in candidate_counter.items():
                    if val == 1:
                        return 2, block_i, block_j
        return -1, -1, -1

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
