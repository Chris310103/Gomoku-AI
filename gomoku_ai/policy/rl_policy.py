import sys, json, time, math, random
from collections import defaultdict
import torch
import torch.nn as nn
import torch.nn.functional as F
import os

POLICY_SAMPLING_MODE = "softmax" 


POLICY_MODEL = None

class PolicyNet(nn.Module):
    def __init__(self, N):
        super().__init__()
        self.N = N
        self.conv1 = nn.Conv2d(2, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.head  = nn.Conv2d(64, 1, kernel_size=1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = self.head(x)
        return x.squeeze(1)

def load_policy_model(N):
    global POLICY_MODEL
    if POLICY_MODEL is None:
        model = PolicyNet(N)

        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, "gomoku_policy.pt")
       
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at: {model_path}")

        state = torch.load(model_path, map_location="cpu")
        model.load_state_dict(state)
        model.eval()
        POLICY_MODEL = model
    return POLICY_MODEL

EMPTY, BLACK, WHITE = 0, 1, 2

def board_to_tensor(board, who):
    N = len(board)
    me_plane  = [[0.0]*N for _ in range(N)]
    opp_plane = [[0.0]*N for _ in range(N)]
    OPP = BLACK if who == WHITE else WHITE

    for r in range(N):
        for c in range(N):
            v = board[r][c]
            if v == who:
                me_plane[r][c] = 1.0
            elif v == OPP:
                opp_plane[r][c] = 1.0

    x = torch.tensor([[me_plane, opp_plane]], dtype=torch.float32)
    return x

def _zobrist_init(N):
    rnd = random.Random(2025)
    return [[[rnd.getrandbits(64) for _ in range(3)] for _ in range(N)] for _ in range(N)]
ZOBRIST = None

def zobrist_hash(board):
    h = 0
    N = len(board)
    for r in range(N):
        for c in range(N):
            if board[r][c] != 0: h ^= ZOBRIST[r][c][board[r][c]]
    return h

def inb(N,r,c): return 0 <= r < N and 0 <= c < N
DIRS = [(0,1),(1,0),(1,1),(1,-1)]

def five_in_a_row(board, r, c, who):
    N = len(board)
    for dr,dc in DIRS:
        cnt = 1
        rr,cc = r+dr,c+dc
        while inb(N,rr,cc) and board[rr][cc]==who: cnt+=1; rr+=dr; cc+=dc
        rr,cc = r-dr,c-dc
        while inb(N,rr,cc) and board[rr][cc]==who: cnt+=1; rr-=dr; cc-=dc
        if cnt >= 5: return True
    return False

def legal_moves(board, radius=2):
    N = len(board)
    stones = [(r,c) for r in range(N) for c in range(N) if board[r][c]!=0]
    if not stones: return [(N//2, N//2)]
    seen=set()
    for r0,c0 in stones:
        for dr in range(-radius, radius+1):
            for dc in range(-radius, radius+1):
                r,c = r0+dr, c0+dc
                if inb(N,r,c) and board[r][c]==0: seen.add((r,c))
    return list(seen)

def can_win_points(board, who):
    res=[]
    for (r,c) in legal_moves(board):
        board[r][c]=who
        if five_in_a_row(board,r,c,who): res.append((r,c))
        board[r][c]=0
    return res

TTEntry = defaultdict(lambda: None)

def choose_move_with_rl(board, who, mode=None):

    N = len(board)

    stone_count = sum(1 for r in range(N) for c in range(N) if board[r][c] != 0)
    
    if stone_count == 0:
        center = N // 2
        
        candidates = [
            (center + dr, center + dc)
            for dr in [-1, 0, 1]
            for dc in [-1, 0, 1]
        ]
        
        return random.choice(candidates)

    if mode is None:
        mode = POLICY_SAMPLING_MODE

    model = load_policy_model(N)
    x = board_to_tensor(board, who)
    
    with torch.no_grad():
        logits = model(x)[0]

    for r in range(N):
        for c in range(N):
            if board[r][c] != EMPTY:
                logits[r, c] = -1e9

    flat = logits.view(-1)
    
    if torch.all(flat <= -1e8):
        return (0, 0)

    if mode == "softmax":
        probs = torch.softmax(flat, dim=0)
        if torch.isnan(probs).any() or probs.sum().item() <= 0:
            idx = int(torch.argmax(flat).item())
        else:
            idx = int(torch.multinomial(probs, num_samples=1).item())
    else:
        idx = int(torch.argmax(flat).item())

    r = idx // N
    c = idx % N
    return (r, c)

def find_best_move_fallback(board, who):

    moves = legal_moves(board)
    if not moves: return (0,0)
    return random.choice(moves)

def main_loop():
    global ZOBRIST
    for line in sys.stdin:
        s = line.strip()
        if not s: continue
        try:
            req = json.loads(s)
            board = req["board"]
            player = req.get("player", "white")
            N = len(board)
            
            if ZOBRIST is None or len(ZOBRIST) != N:
                globals()["ZOBRIST"] = _zobrist_init(N)
                TTEntry.clear()
                
            who = WHITE if player == "white" else BLACK
            
            try:
                r, c = choose_move_with_rl(board, who)
            except Exception as e:
                sys.stderr.write(f"RL Error: {e}\n")
                r, c = find_best_move_fallback(board, who)
                
            sys.stdout.write(json.dumps({"row": int(r), "col": int(c)}) + "\n")
            sys.stdout.flush()
            
        except Exception as e:
            sys.stdout.write(json.dumps({"row": -1, "col": -1, "error": str(e)}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":

    seed_val = int(time.time() * 1000)
    random.seed(seed_val)
    torch.manual_seed(seed_val)
    
    main_loop()