"""
Labour work #2. Levenshtein distance.
"""

def generate_edit_matrix(num_rows: int, num_cols: int) -> list:
    edit_matrix = []
    if isinstance(num_rows, int) and isinstance(num_cols, int):
        for _ in range(num_rows):
            edit_matrix.append([0] * num_cols)
    return edit_matrix


def initialize_edit_matrix(edit_matrix: tuple, add_weight: int, remove_weight: int) -> list:
    if not isinstance(edit_matrix, tuple) or not edit_matrix:
        return []
    edit_matrix = list(edit_matrix)
    if not isinstance(add_weight, int) or not isinstance(remove_weight, int):
        return edit_matrix
    if edit_matrix == [[]] * len(edit_matrix):
        return edit_matrix
    for i in range(1, len(edit_matrix)):
        edit_matrix[i][0] = edit_matrix[i - 1][0] + remove_weight
    for j in range(1, len(edit_matrix[0])):
        edit_matrix[0][j] = edit_matrix[0][j - 1] + add_weight
    return edit_matrix


def minimum_value(numbers: tuple) -> int:
    return min(numbers)


def fill_edit_matrix(edit_matrix: tuple,
                     add_weight: int,
                     remove_weight: int,
                     substitute_weight: int,
                     original_word: str,
                     target_word: str) -> list:
    if not isinstance(edit_matrix, tuple):
        return []
    edit_matrix = list(edit_matrix)
    if not isinstance(original_word, str) or not isinstance(target_word, str) or original_word == '' \
            or target_word == '':
        return edit_matrix
    if not isinstance(add_weight, int) or not isinstance(remove_weight, int) or not isinstance(substitute_weight, int):
        return edit_matrix
    original_word = ' ' + original_word
    target_word = ' ' + target_word
    for i in range(1, len(edit_matrix)):
        for j in range(1, len(edit_matrix[0])):
            first_var = edit_matrix[i - 1][j] + remove_weight
            second_var = edit_matrix[i][j - 1] + add_weight
            third_var = edit_matrix[i - 1][j - 1]
            if original_word[i] != target_word[j]:
                third_var += substitute_weight
            edit_matrix[i][j] = minimum_value((first_var, second_var, third_var))
    return edit_matrix


def find_distance(original_word: str,
                  target_word: str,
                  add_weight: int,
                  remove_weight: int,
                  substitute_weight: int) -> int:
    if not isinstance(original_word, str) or not isinstance(target_word, str) or not isinstance(add_weight, int) \
            or not isinstance(remove_weight, int) or not isinstance(substitute_weight, int):
        return -1
    rows = len(original_word) + 1
    cols = len(target_word) + 1
    edit_matrix = generate_edit_matrix(rows, cols)
    initialized_matrix = initialize_edit_matrix(tuple(edit_matrix), add_weight, remove_weight)
    full_matrix = fill_edit_matrix(tuple(initialized_matrix), add_weight, remove_weight, substitute_weight,
                                   original_word, target_word)
    return full_matrix[-1][-1]


def save_to_csv(edit_matrix: list, path_to_file: str) -> None:
    if not isinstance(edit_matrix, list) or not isinstance(path_to_file, str):
        return None
    with open(path_to_file, "w") as file:
        for row in edit_matrix:
            for element in row:
                file.write(str(element))
                if row.index(element) != len(row) - 1:
                    file.write(',')
            if edit_matrix.index(row) != len(edit_matrix) - 1:
                file.write('\n')
    return None


def load_from_csv(path_to_file: str) -> list:
    if not isinstance(path_to_file, str):
        return []
    with open(path_to_file) as file:
        matrix_from_file = file.readlines()
        matrix = []
        for element in matrix_from_file:
            element = element.replace('\n', '')
            numbers = element.split(',')
            to_add = list(map(int, numbers))
            matrix.append(to_add)
    return matrix


def search_for_path(matrix: list, ind_1: int, ind_2: int, number=0) -> int:
    if not(ind_1 >= len(matrix) - 1 or ind_2 >= len(matrix[0]) - 1) and \
            matrix[ind_1][ind_2] == matrix[ind_1 + 1][ind_2 + 1]:
        number = search_for_path(matrix, ind_1 + 1, ind_2 + 1, number + 1)
    return number


def describe_edits(edit_matrix: tuple, original_word: str, target_word: str, add_weight: int, remove_weight: int,
                   substitute_weight: int) -> list:
    edits = []
    edit_matrix = list(edit_matrix)
    distance = find_distance(original_word, target_word, add_weight, remove_weight, substitute_weight)
    row = 0
    col = 0
    for _ in range(distance):
        var_1 = search_for_path(edit_matrix, row, col + 1)
        var_2 = search_for_path(edit_matrix, row + 1, col)
        if var_1 == var_2:
            if (not edits or 'insert' in edits[-1]) and row != len(edit_matrix) - 1:
                edits.append('remove ' + original_word[row])
                row += 1
            elif col != len(edit_matrix[0]) - 1:
                edits.append('insert ' + target_word[col])
                col += 1
        elif var_1 > var_2:
            edits.append('insert ' + target_word[col])
            edits.append([])
            col += var_1 + 1
            row += var_1
        else:
            edits.append('remove ' + original_word[row])
            edits.append([])
            row += var_2 + 1
            col += var_2
    return edits


def create_edits_with_subs(edits: tuple) -> list:
    edits_with_subs = []
    if isinstance(edits, tuple):
        flag = 1
        for ind, edit in enumerate(edits):
            if ind != len(edits) - 1 and 'remove' in edit and 'insert' in edits[ind + 1]:
                edits_with_subs.append('substitute {} with {}'.format(edit[-1], edits[ind + 1][-1]))
                flag = 0
            elif not flag:
                flag = 1
            elif edit:
                edits_with_subs.append(edit)
    return edits_with_subs
