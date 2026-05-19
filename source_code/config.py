# --- SYSTEM DIMENSIONS ---
WIDTH, HEIGHT = 1100, 720  
BOARD_SIZE = 15             
CELL_SIZE = 40
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE 

# --- CLASSIC GRAPHIC PALETTE (RETRO WOOD & PAPER) ---
COLOR_BG = (240, 230, 210)       # Warm paper background
COLOR_PANEL = (215, 195, 165)    # Elegant wooden panel
COLOR_GRID = (90, 70, 50)        # Dark walnut grid lines
COLOR_PLAYER_X = (25, 75, 165)   # Deep classic blue for X
COLOR_AI_O = (195, 40, 40)       # Crimson red for O
COLOR_TEXT_DARK = (45, 35, 25)   # Readable charcoal brown
WHITE = (255, 255, 255)
GRAY = (130, 130, 130)

TXT = {
    "PLAY": "PLAY",
    "QUIT_GAME": "QUIT GAME",
    "SELECT_DIFFICULTY": "LEVEL",
    "EASY": "EASY",
    "NORMAL": "NORMAL",
    "HARD": "HARD",
    "BACK": "GO BACK",
    "QUIT_MATCH": "REMATCH",
    "LOADING": "PLEASE WAIT......",
    "AI_TITLE": "AI",
    "STATUS": "MATCH STATUS",
    "GAME_OVER": "MATCH FINISHED",
    "USER_TURN": "YOUR TURN (X) - MAKE A MOVE",
    "AI_TURN": "AI TURN (O) - COMPUTING...",
    "AI_WIN": "AI CORE VICTORIOUS",
    "PLAYER_WIN": "YOU ARE VICTORIOUS",
    "DRAW": "MATCH ENDED IN A DRAW",
    "RESTART_MSG": "Click anywhere on the board to restart",
    "SURRENDER": "GIVE UP",
}