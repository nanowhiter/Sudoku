import cv2
import numpy as np
import os

from Sudoku import Sudoku

CLICKED = False
MOUSE_X, MOUSE_Y = -1, -1
BLOCK_SIZE = 100


def mouse_callback(event, x, y, flags, param):
    global CLICKED, MOUSE_X, MOUSE_Y
    if event == cv2.EVENT_LBUTTONUP:
        CLICKED = True
        MOUSE_X = x
        MOUSE_Y = y


def draw_sudoku(sudoku_img, sudoku_map, sudoku_candidate_map, is_clicked=False, x=0, y=0):
    sudoku_img[:, :] = (125, 125, 125)
    for i in range(9):
        if i % 3 == 0:
            cv2.line(sudoku_img, (i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, 9 * BLOCK_SIZE), (0, 0, 0), 10)
            cv2.line(sudoku_img, (0, i * BLOCK_SIZE), (9 * BLOCK_SIZE, i * BLOCK_SIZE), (0, 0, 0), 10)
        else:
            cv2.line(sudoku_img, (i * BLOCK_SIZE, 0), (i * BLOCK_SIZE, 9 * BLOCK_SIZE), (0, 0, 0), 3)
            cv2.line(sudoku_img, (0, i * BLOCK_SIZE), (9 * BLOCK_SIZE, i * BLOCK_SIZE), (0, 0, 0), 3)

    x, y = x - x % BLOCK_SIZE, y - y % BLOCK_SIZE

    if is_clicked:
        cv2.rectangle(sudoku_img, (x, y, BLOCK_SIZE, BLOCK_SIZE), (0, 0, 255), 2)

    # Draw value and candidate value
    for i in range(9):
        for j in range(9):
            if sudoku_map[j * 9 + i] > 0:
                cv2.putText(sudoku_img, f"{sudoku_map[j * 9 + i]}",
                            (int((i + 0.25) * BLOCK_SIZE), int((j + 0.75) * BLOCK_SIZE)),
                            cv2.FONT_HERSHEY_SIMPLEX, 3.0, (0, 125, 255), 3)
            else:
                x = 0
                y = 0
                for idx in range(9):
                    if sudoku_candidate_map[j * 9 + i][idx + 1] >= 0:
                        x = idx % 3
                        y = idx // 3
                        cv2.putText(sudoku_img, f"{idx + 1}",
                                    (int((i + 0.1 + x * 0.33) * BLOCK_SIZE), int((j + 0.25 + y * 0.33) * BLOCK_SIZE)),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 125, 255), 3)

    return sudoku_img


def draw_hint(sudoku_img, x, y, flag):
    # Vertical
    if flag == 0:
        cv2.rectangle(sudoku_img, (x * BLOCK_SIZE, 0, BLOCK_SIZE, BLOCK_SIZE * 9), (255, 125, 255), 2)

    elif flag == 1:
        cv2.rectangle(sudoku_img, (0, y * BLOCK_SIZE, BLOCK_SIZE * 9, BLOCK_SIZE), (255, 125, 255), 2)

    elif flag == 2:
        cv2.rectangle(sudoku_img, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE * 3, BLOCK_SIZE * 3), (255, 125, 255), 2)

    return sudoku_img


def main():
    global CLICKED, MOUSE_X, MOUSE_Y
    sudoku = Sudoku()

    if os.path.exists('last_game.bak'):
        with open('last_game.bak') as fin:
            val_list = [int(val) for val in fin.read().strip().split()]
        sudoku.init(val_list)

    window_name = "Sudoku"

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, mouse_callback)

    is_clicked = False

    sudoku_img = np.ones((9 * BLOCK_SIZE, 9 * BLOCK_SIZE, 3), np.uint8) * 125

    changed = True

    _sudoku_map = sudoku.get_map()
    _sudoku_candidate_map = sudoku.get_candidate_map()

    while True:
        if changed:
            changed = False
            sudoku_img = draw_sudoku(sudoku_img, _sudoku_map, _sudoku_candidate_map, is_clicked, MOUSE_X, MOUSE_Y)

        cv2.imshow(window_name, sudoku_img)
        if CLICKED:
            CLICKED = False
            is_clicked = True
            changed = True

        key = cv2.waitKey(10) & 0xff
        if key == ord('q') or key == 27:
            break

        elif ord('1') <= key <= ord('9'):
            val = int(key - ord('0'))
            if is_clicked:
                is_clicked = False
                changed = True
                if sudoku.set_val(MOUSE_X // BLOCK_SIZE, MOUSE_Y // BLOCK_SIZE, val):
                    _sudoku_map = sudoku.get_map()
                    _sudoku_candidate_map = sudoku.get_candidate_map()
        elif key == 0:
            changed = True
            sudoku.clean_val(MOUSE_X // BLOCK_SIZE, MOUSE_Y // BLOCK_SIZE)

        elif key == ord('r'):
            changed = True
            sudoku.reset()
            _sudoku_map = sudoku.get_map()
            _sudoku_candidate_map = sudoku.get_candidate_map()

        elif key == ord('w') or key == ord('a') or key == ord('s') or key == ord('d'):
            is_clicked = True
            changed = True

            if MOUSE_X == -1:
                MOUSE_X, MOUSE_Y = 0, 0
            else:
                if key == ord('w'):
                    MOUSE_Y -= BLOCK_SIZE
                elif key == ord('a'):
                    MOUSE_X -= BLOCK_SIZE
                elif key == ord('s'):
                    MOUSE_Y += BLOCK_SIZE
                elif key == ord('d'):
                    MOUSE_X += BLOCK_SIZE

                MOUSE_X, MOUSE_Y = max(0, min(8 * BLOCK_SIZE, MOUSE_X)), max(0, min(8 * BLOCK_SIZE, MOUSE_Y))

        elif key == ord('h'):
            flag, x, y = sudoku.get_hint()
            print(flag, x, y)
            sudoku_img = draw_hint(sudoku_img, x, y, flag)

        if changed:
            with open('last_game.bak', 'w') as fout:
                for val in _sudoku_map:
                    fout.write(f"{val} ")


if __name__ == '__main__':
    main()
