EMPTY=0
BLACK=1
WHITE=2

DIRECTIONS =[
    (0,1),
    (1,0),
    (1,1,),
    (1,-1),
]

def opponent(player:int)->int:
    if player==BLACK:
        return WHITE
    if player==WHITE:
        return BLACK
    
def in_bounds(board_size:int, row:int, col:int)->bool:
    return 0 <= row < board_size and 0 <= col < board_size

def five_in_a_row(board, row:int, col: int, player: int) -> bool:
    board_size=len(board)

    for dr, dc in DIRECTIONS:
        count=1

        r,c=row+dr, col+dc
        while in_bounds(board_size, r, c) and board[r][c]==player:
            count+=1
            r+=dr
            c+=dc

        r,c=row-dr, col-dc
        while in_bounds(board_size, r, c) and board[r][c]==player:
            count+=1
            r-=dr
            c-=dc

        if count>=5:
            return True

    return 

def legal_moves(board, radius: int = 2):
    board_size = len(board)

    stones = []
    for row in range(board_size):
        for col in range(board_size):
            if board[row][col] != EMPTY:
                stones.append((row, col))

    if not stones:
        mid = board_size // 2
        return [(mid, mid)]

    moves = set()

    for row, col in stones:
        for dr in range(-radius, radius + 1):
            for dc in range(-radius, radius + 1):
                nr = row + dr
                nc = col + dc

                if in_bounds(board_size, nr, nc) and board[nr][nc] == EMPTY:
                    moves.add((nr, nc))

    return list(moves)

def can_win_points(board, player: int):
    winning_moves = []

    for row, col in legal_moves(board):
        board[row][col] = player

        if five_in_a_row(board, row, col, player):
            winning_moves.append((row, col))

        board[row][col] = EMPTY

    return winning_moves

def all_lines_with_coords(board):
    board_size = len(board)

    # 1. rows
    for row in range(board_size):
        values = board[row][:]
        coords = [(row, col) for col in range(board_size)]
        yield values, coords

    # 2. columns
    for col in range(board_size):
        values = [board[row][col] for row in range(board_size)]
        coords = [(row, col) for row in range(board_size)]
        yield values, coords

    # 3. main diagonals: top-left to bottom-right
    for start_col in range(board_size):
        values = []
        coords = []

        row, col = 0, start_col
        while row < board_size and col < board_size:
            values.append(board[row][col])
            coords.append((row, col))
            row += 1
            col += 1

        if len(values) >= 5:
            yield values, coords

    for start_row in range(1, board_size):
        values = []
        coords = []

        row, col = start_row, 0
        while row < board_size and col < board_size:
            values.append(board[row][col])
            coords.append((row, col))
            row += 1
            col += 1

        if len(values) >= 5:
            yield values, coords

    for start_col in range(board_size):
        values = []
        coords = []

        row, col = 0, start_col
        while row < board_size and col >= 0:
            values.append(board[row][col])
            coords.append((row, col))
            row += 1
            col -= 1

        if len(values) >= 5:
            yield values, coords

    for start_row in range(1, board_size):
        values = []
        coords = []

        row, col = start_row, board_size - 1
        while row < board_size and col >= 0:
            values.append(board[row][col])
            coords.append((row, col))
            row += 1
            col -= 1

        if len(values) >= 5:
            yield values, coords
