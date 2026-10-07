# -*- coding: UTF-8 -*-
"""Connect 4 — 四子棋

雙人對戰 / 人機對戰。遊戲邏輯（Connect4Game、Engine）不依賴 tkinter，
可單獨 import 做測試；UI 層（BoardView、Connect4App）負責繪製與互動。
"""

import math
import random
import sys
import tkinter as tk

# ---------------------------------------------------------------- 棋盤常數

COLS, ROWS = 7, 6
EMPTY, P1, P2 = 0, 1, 2
WIN_SCORE = 1_000_000
INF = WIN_SCORE * 10


def _build_windows():
    """列出棋盤上所有「連續四格」的位置組合（共 69 組）。"""
    out = []
    for c in range(COLS):
        for r in range(ROWS):
            if c + 3 < COLS:
                out.append(tuple((c + i, r) for i in range(4)))
            if r + 3 < ROWS:
                out.append(tuple((c, r + i) for i in range(4)))
            if c + 3 < COLS and r + 3 < ROWS:
                out.append(tuple((c + i, r + i) for i in range(4)))
            if c + 3 < COLS and r - 3 >= 0:
                out.append(tuple((c + i, r - i) for i in range(4)))
    return tuple(out)


WINDOWS = _build_windows()

# 每個格子參與到哪些四連組合，用來只檢查剛落子的那一格
WINDOWS_AT = {}
for _w in WINDOWS:
    for _cell in _w:
        WINDOWS_AT.setdefault(_cell, []).append(_w)
WINDOWS_AT = {k: tuple(v) for k, v in WINDOWS_AT.items()}


def landing_row(board, col):
    """回傳該欄最低的空格列號，滿欄則回傳 None。"""
    column = board[col]
    for r in range(ROWS):
        if column[r] == EMPTY:
            return r
    return None


def wins_at(board, col, row):
    """若 (col, row) 這一子構成四連，回傳那四格；否則回傳 None。"""
    player = board[col][row]
    for w in WINDOWS_AT[(col, row)]:
        if all(board[c][r] == player for c, r in w):
            return w
    return None


# ---------------------------------------------------------------- 遊戲邏輯


class Connect4Game:
    """棋盤狀態。board[col][row]，row 0 為最底層。"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[EMPTY] * ROWS for _ in range(COLS)]
        self.moves = 0
        self.turn = P1
        self.winner = EMPTY
        self.win_cells = ()

    @property
    def over(self):
        return self.winner != EMPTY or self.moves == COLS * ROWS

    @property
    def draw(self):
        return self.winner == EMPTY and self.moves == COLS * ROWS

    def landing_row(self, col):
        return landing_row(self.board, col)

    def valid_moves(self):
        return [c for c in range(COLS) if self.board[c][ROWS - 1] == EMPTY]

    def drop(self, col):
        """落子，回傳落點列號；不合法則回傳 None。"""
        if self.over:
            return None
        row = self.landing_row(col)
        if row is None:
            return None
        player = self.turn
        self.board[col][row] = player
        self.moves += 1
        cells = wins_at(self.board, col, row)
        if cells:
            self.winner = player
            self.win_cells = cells
        else:
            self.turn = P2 if player == P1 else P1
        return row


# ---------------------------------------------------------------- AI


class Engine:
    """negamax + alpha-beta 剪枝，評估函式為四連組合的加權計分。"""

    # 雙方必須共用同一組權重：negamax 的前提是 eval(局面, A) == -eval(局面, B)，
    # 攻守給不同權重會破壞反對稱性，讓不同視角的葉節點分數無法比較。
    # 4 顆代表已經連成四；搜尋中 wins_at 會先攔下，列在這裡是為了讓
    # _evaluate 對任何盤面都有定義。
    WEIGHT = {0: 0, 1: 2, 2: 16, 3: 80, 4: 100_000}
    # 依「空格還要等幾顆子才填得到」打折，索引即該組合所有空格的距離總和。
    # 單位放大 100 倍以免整數除法失真。
    #
    # 衰減必須和緩。實測陡峭的曲線（如 100/62/34/18…）會讓引擎只看得到眼前的
    # 威脅、放棄佈局，深度 5 對無折扣版本是 0 勝 37 敗；下面這條和緩的曲線則是
    # 90 局 76 勝 14 敗。
    REACH = (100, 94, 88, 83, 78, 73, 69, 65, 61)
    ORDER = (3, 2, 4, 1, 5, 0, 6)  # 中央優先，剪枝效果最好

    def __init__(self, depth=4):
        self.depth = depth

    def choose(self, board, me):
        """回傳 me 這一方的最佳落子欄位；無處可下回傳 None。"""
        moves = [c for c in self.ORDER if landing_row(board, c) is not None]
        if not moves:
            return None
        best_score = -INF
        best = []
        for c in moves:
            row = landing_row(board, c)
            board[c][row] = me
            if wins_at(board, c, row):
                score = WIN_SCORE
            else:
                # 根節點必須用完整窗：收窄的窗會讓剪枝後的回傳值變成邊界而非
                # 精確分數，使必敗的一步看起來與最佳步同分。
                score = -self._negamax(board, self.depth - 1, 3 - me, -INF, INF)
            board[c][row] = EMPTY
            if score > best_score:
                best_score, best = score, [c]
            elif score == best_score:
                best.append(c)
        # 同分時隨機挑一個，避免每局都走同樣的棋
        return random.choice(best)

    def _negamax(self, board, depth, player, alpha, beta):
        moves = [c for c in self.ORDER if landing_row(board, c) is not None]
        if not moves:
            return 0  # 平手
        if depth == 0:
            return self._quiesce(board, player, self.depth)
        best = -INF
        for c in moves:
            row = landing_row(board, c)
            board[c][row] = player
            if wins_at(board, c, row):
                score = WIN_SCORE - (self.depth - depth)  # 愈早取勝愈好
            else:
                score = -self._negamax(board, depth - 1, 3 - player, -beta, -alpha)
            board[c][row] = EMPTY
            if score > best:
                best = score
            if best > alpha:
                alpha = best
            if alpha >= beta:
                break
        return best

    def _quiesce(self, board, player, ply):
        """把視界處的立即勝負算乾淨後才靜態評估。

        不這樣做的話，搜尋會固定停在某一方剛走完的局面：偶數深度總是停在對手
        走完之後，於是每個葉節點看起來都像對手剛佔了便宜，引擎因此系統性低估
        自己、下得過度保守。只要強制把「能立刻連四」與「必須擋的四連」展開到
        沒有立即戰術為止，葉節點就與深度的奇偶無關了。
        """
        opp = 3 - player
        moves = [c for c in self.ORDER if landing_row(board, c) is not None]
        if not moves:
            return 0

        for c in moves:  # 自己能立刻連四
            row = landing_row(board, c)
            board[c][row] = player
            won = wins_at(board, c, row)
            board[c][row] = EMPTY
            if won:
                return WIN_SCORE - ply

        threats = []  # 對手下一手能連四的位置
        for c in moves:
            row = landing_row(board, c)
            board[c][row] = opp
            if wins_at(board, c, row):
                threats.append(c)
            board[c][row] = EMPTY

        if len(threats) > 1:
            return -(WIN_SCORE - ply - 1)  # 兩處以上擋不完
        if threats:
            c = threats[0]
            row = landing_row(board, c)
            board[c][row] = player
            score = -self._quiesce(board, opp, ply + 1)
            board[c][row] = EMPTY
            return score

        return self._evaluate(board, player)

    def _evaluate(self, board, player):
        opp = 3 - player
        # 每欄目前的落點高度，用來算空格還要等幾顆子才填得到
        heights = [landing_row(board, c) for c in range(COLS)]
        score = 0
        for w in WINDOWS:
            mine = theirs = 0
            gap = 0
            for c, r in w:
                v = board[c][r]
                if v == player:
                    mine += 1
                elif v == opp:
                    theirs += 1
                else:
                    gap += r - heights[c]  # 0 代表下一手就能下在這裡
            if mine and theirs:
                continue  # 雙方都有子，這組已無法連成四
            if not mine and not theirs:
                continue
            # 愈難填滿的組合愈不值錢：懸在半空的三連隨時可能被對手搶先，
            # 和落地、下一手就能完成的三連價值差很多。
            value = self.WEIGHT[mine or theirs] * self.REACH[min(gap, len(self.REACH) - 1)]
            score += value if mine else -value
        for r in range(ROWS):  # 中央欄位的子較有價值
            v = board[3][r]
            if v == player:
                score += 400
            elif v == opp:
                score -= 400
        return score


# ---------------------------------------------------------------- 外觀

BG = "#0e1117"
PANEL = "#171c26"
PANEL_HI = "#2b3448"
SEG_IDLE = "#1e2533"
BOARD_FILL = "#24356b"
BOARD_HOLE = "#141c38"
COL_HOVER = "#30478c"
TEXT = "#e8eaf0"
MUTED = "#8b93a7"
ACCENT = "#5b8def"
CHIP_BASE = {P1: "#dc4a56", P2: "#e0a92e"}

DEFAULT_CELL = 64   # 格子邊長，視窗太高時會自動縮小（見 main()）
MIN_CELL = 40

if sys.platform == "darwin":
    UI_FONT = "PingFang TC"
elif sys.platform.startswith("win"):
    UI_FONT = "Microsoft JhengHei"
else:
    UI_FONT = "Helvetica"

FONT_TITLE = (UI_FONT, 25, "bold")
FONT_STATUS = (UI_FONT, 17, "bold")
FONT_UI = (UI_FONT, 13)
FONT_SMALL = (UI_FONT, 11)


def _hex_to_rgb(color):
    return tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))


def _rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v)))) for v in rgb)


def _blend(c1, c2, t):
    """c1 與 c2 依比例 t（0→c1，1→c2）混色。"""
    a, b = _hex_to_rgb(c1), _hex_to_rgb(c2)
    return _rgb_to_hex(a[i] + (b[i] - a[i]) * t for i in range(3))


def _shade(color, factor):
    """factor > 0 提亮（混白），< 0 加深（混黑）。"""
    return _blend(color, "#ffffff" if factor >= 0 else "#000000", abs(factor))


def _round_rect_points(x0, y0, x1, y1, r):
    return [
        x0 + r, y0, x1 - r, y0, x1, y0, x1, y0 + r,
        x1, y1 - r, x1, y1, x1 - r, y1,
        x0 + r, y1, x0, y1, x0, y1 - r,
        x0, y0 + r, x0, y0,
    ]


# ---------------------------------------------------------------- 棋盤繪製


class BoardView(tk.Canvas):
    """負責棋盤的繪製、滑鼠預覽、落子動畫與勝利高亮。"""

    def __init__(self, master, on_column, cell=DEFAULT_CELL):
        super().__init__(master, bg=BG, highlightthickness=0, bd=0)
        self._on_column = on_column
        self._board = [[EMPTY] * ROWS for _ in range(COLS)]
        self._hover_col = None
        self._preview_player = P1
        self._interactive = True
        self._win_cells = ()
        self._pulse = 0.0
        self._gen = 0
        self._after_ids = []
        self.bind("<Motion>", self._on_motion)
        self.bind("<Leave>", lambda e: self._set_hover(None))
        self.bind("<Button-1>", self._on_click)
        self.set_cell(cell)

    # ---- 幾何（依格子大小換算，讓棋盤能配合螢幕縮放）

    def set_cell(self, cell):
        self.cell = cell
        self.pad = max(7, round(cell * 0.18))
        self.drop_h = cell
        self.r_chip = round(cell * 0.405)
        self.width_px = COLS * cell + 2 * self.pad
        self.height_px = self.drop_h + ROWS * cell + 2 * self.pad
        self.configure(width=self.width_px, height=self.height_px)
        self.render()

    def _cx(self, col):
        return self.pad + col * self.cell + self.cell // 2

    def _cy(self, row):
        return self.drop_h + self.pad + (ROWS - 1 - row) * self.cell + self.cell // 2

    def _col_at(self, x):
        col = int((x - self.pad) // self.cell)
        return col if 0 <= col < COLS else None

    # ---- 狀態更新

    def set_state(self, board, preview_player, interactive):
        self._board = board
        self._preview_player = preview_player
        self._interactive = interactive
        self.render()

    def reset(self):
        """取消所有進行中的動畫，供重新開始時呼叫。"""
        self._gen += 1
        for aid in self._after_ids:
            try:
                self.after_cancel(aid)
            except Exception:
                pass
        self._after_ids = []
        self._win_cells = ()
        self._hover_col = None

    def _later(self, ms, fn):
        gen = self._gen

        def guarded():
            if gen == self._gen:
                fn()

        aid = self.after(ms, guarded)
        self._after_ids.append(aid)
        return aid

    # ---- 滑鼠

    def _on_motion(self, event):
        self._set_hover(self._col_at(event.x) if self._interactive else None)

    def _set_hover(self, col):
        if col is not None and landing_row(self._board, col) is None:
            col = None
        if col != self._hover_col:
            self._hover_col = col
            self.render()

    def _on_click(self, event):
        col = self._col_at(event.x)
        if col is not None:
            self._on_column(col)

    # ---- 繪製

    def render(self):
        self.delete("all")

        # 棋盤面板要先畫，欄位高亮才蓋得上去（反過來會被面板遮住）
        self.create_polygon(
            _round_rect_points(0, self.drop_h, self.width_px, self.height_px, 22),
            smooth=True, fill=BOARD_FILL, outline=_shade(BOARD_FILL, -0.3), width=2)

        if self._interactive and self._hover_col is not None:
            x0 = self.pad + self._hover_col * self.cell
            self.create_polygon(
                _round_rect_points(x0 + 2, 4, x0 + self.cell - 2, self.height_px - 4, 14),
                smooth=True, fill=COL_HOVER, outline="")

        for col in range(COLS):
            for row in range(ROWS):
                cx, cy = self._cx(col), self._cy(row)
                player = self._board[col][row]
                if player == EMPTY:
                    self._hole(cx, cy)
                else:
                    self._chip(cx, cy, player)

        if self._interactive and self._hover_col is not None:
            base = CHIP_BASE[self._preview_player]
            r = self.r_chip
            cx, cy = self._cx(self._hover_col), self.drop_h // 2
            self.create_oval(cx - r, cy - r, cx + r, cy + r,
                             fill=_shade(base, -0.5), outline=base, width=2)

        self._draw_win_rings()

    def _hole(self, cx, cy):
        r = self.r_chip
        self.create_oval(cx - r, cy - r, cx + r, cy + r,
                         fill=BOARD_HOLE, outline=_shade(BOARD_FILL, -0.5), width=1)

    def _chip(self, cx, cy, player, tags=()):
        base = CHIP_BASE[player]
        r = self.r_chip
        self.create_oval(cx - r, cy - r, cx + r, cy + r,
                         fill=base, outline=_shade(base, -0.35), width=2, tags=tags)
        ri = r * 0.68
        self.create_oval(cx - ri, cy - ri, cx + ri, cy + ri,
                         fill=_shade(base, 0.12), outline="", tags=tags)
        # 左上角的反光
        self.create_oval(cx - r * 0.52, cy - r * 0.6, cx - r * 0.08, cy - r * 0.16,
                         fill=_shade(base, 0.42), outline="", tags=tags)

    def _draw_win_rings(self):
        self.delete("winring")
        if not self._win_cells:
            return
        k = (math.sin(self._pulse * 2 * math.pi) + 1) / 2
        r = self.r_chip + 3 + 4 * k
        color = _blend(ACCENT, "#ffffff", k)
        for col, row in self._win_cells:
            cx, cy = self._cx(col), self._cy(row)
            self.create_oval(cx - r, cy - r, cx + r, cy + r,
                             outline=color, width=3, tags="winring")

    # ---- 動畫

    def animate_drop(self, col, row, player, done):
        """棋子從頂端落下，播完後呼叫 done()。"""
        self._hover_col = None
        self.render()
        cx = self._cx(col)
        start = self.drop_h // 2
        target = self._cy(row)

        frames = []
        y, v = float(start), 0.0
        while y < target:
            v += 3.4
            y = min(float(target), y + v)
            frames.append(y)
        if not frames:
            frames = [float(target)]

        self._chip(cx, start, player, tags="falling")
        state = {"i": 0, "y": float(start)}

        def step():
            i = state["i"]
            if i >= len(frames):
                self.delete("falling")
                self._board[col][row] = player
                self.render()
                done()
                return
            self.move("falling", 0, frames[i] - state["y"])
            state["y"] = frames[i]
            state["i"] = i + 1
            self._later(16, step)

        step()

    def celebrate(self, cells):
        self._win_cells = tuple(cells)
        self._pulse = 0.0
        self._interactive = False
        self._hover_col = None
        self.render()
        self._pulse_step()

    def _pulse_step(self):
        self._pulse = (self._pulse + 0.05) % 1.0
        self._draw_win_rings()
        self._later(45, self._pulse_step)


# ---------------------------------------------------------------- 分段選擇器


class Segmented(tk.Frame):
    """幾個選項橫向排列的切換器。tk.Button 在 macOS 上不吃顏色，故以 Label 實作。"""

    def __init__(self, master, options, value, command):
        super().__init__(master, bg=PANEL)
        self._command = command
        self._value = value
        self._enabled = True
        self._hovered = None
        self._labels = {}
        for text, val in options:
            lb = tk.Label(self, text=text, font=FONT_UI, padx=13, pady=5,
                          bd=0, cursor="hand2")
            lb.pack(side="left", padx=2)
            lb.bind("<Button-1>", lambda e, v=val: self._select(v))
            lb.bind("<Enter>", lambda e, v=val: self._set_hover(v))
            lb.bind("<Leave>", lambda e: self._set_hover(None))
            self._labels[val] = lb
        self._restyle()

    @property
    def value(self):
        return self._value

    def set_value(self, value):
        self._value = value
        self._restyle()

    def set_enabled(self, enabled):
        self._enabled = enabled
        if not enabled:
            self._hovered = None
        self._restyle()

    def _select(self, value):
        if not self._enabled or value == self._value:
            return
        self._value = value
        self._restyle()
        self._command(value)

    def _set_hover(self, value):
        if self._enabled:
            self._hovered = value
            self._restyle()

    def _restyle(self):
        for val, lb in self._labels.items():
            if not self._enabled:
                lb.configure(bg=_blend(SEG_IDLE, BG, 0.5),
                             fg=_blend(MUTED, BG, 0.6), cursor="")
            elif val == self._value:
                lb.configure(bg=ACCENT, fg="#ffffff", cursor="hand2")
            elif val == self._hovered:
                lb.configure(bg=PANEL_HI, fg=TEXT, cursor="hand2")
            else:
                lb.configure(bg=SEG_IDLE, fg=MUTED, cursor="hand2")


class TextButton(tk.Label):
    """同樣理由自行實作的按鈕。"""

    def __init__(self, master, text, command, accent=ACCENT):
        super().__init__(master, text=text, font=FONT_UI, padx=16, pady=6,
                         bd=0, cursor="hand2", bg=accent, fg="#ffffff")
        self._accent = accent
        self.bind("<Button-1>", lambda e: command())
        self.bind("<Enter>", lambda e: self.configure(bg=_shade(accent, 0.16)))
        self.bind("<Leave>", lambda e: self.configure(bg=accent))


# ---------------------------------------------------------------- 主視窗


# 實測的層級間距（各 40 局，先後手各半）：3 勝 1 為 40:0，5 勝 3 為 25:15。
# 最差耗時分別約 0.00s / 0.01s / 0.31s。
DIFFICULTY_DEPTH = {"easy": 1, "normal": 3, "hard": 5}


class Connect4App(tk.Frame):
    def __init__(self, master, cell=DEFAULT_CELL):
        super().__init__(master, bg=BG)
        self.game = Connect4Game()
        self.engine = Engine(DIFFICULTY_DEPTH["normal"])
        self.mode = "pvp"
        self.human = P1
        self.busy = False
        self._gen = 0
        self._after_ids = []

        self._build(cell)
        self._new_game()

    def fit_to_height(self, available):
        """棋盤太高放不進螢幕時，縮小格子。回傳是否有調整。"""
        window = self.winfo_toplevel()
        window.update_idletasks()
        board = self.board_view
        chrome = window.winfo_reqheight() - board.height_px
        if chrome + board.height_px <= available:
            return False
        cell = (available - chrome - 2 * board.pad) // (ROWS + 1)
        board.set_cell(max(MIN_CELL, min(board.cell, cell)))
        window.update_idletasks()
        return True

    # ---- 版面

    def _build(self, cell):
        tk.Label(self, text="CONNECT 4", font=FONT_TITLE, bg=BG, fg=TEXT).pack(pady=(18, 0))
        tk.Label(self, text="把四顆棋子連成一線就獲勝", font=FONT_SMALL,
                 bg=BG, fg=MUTED).pack(pady=(2, 14))

        controls = tk.Frame(self, bg=PANEL)
        controls.pack(fill="x", padx=24)

        row1 = tk.Frame(controls, bg=PANEL)
        row1.pack(fill="x", padx=12, pady=(10, 4))
        tk.Label(row1, text="模式", font=FONT_SMALL, bg=PANEL, fg=MUTED,
                 width=5, anchor="w").pack(side="left")
        self.mode_seg = Segmented(row1, [("雙人對戰", "pvp"), ("人機對戰", "pve")],
                                  "pvp", self._on_mode)
        self.mode_seg.pack(side="left")

        self.row2 = tk.Frame(controls, bg=PANEL)
        self.row2.pack(fill="x", padx=12, pady=(4, 10))
        tk.Label(self.row2, text="難度", font=FONT_SMALL, bg=PANEL, fg=MUTED,
                 width=5, anchor="w").pack(side="left")
        self.diff_seg = Segmented(self.row2, [("簡單", "easy"), ("普通", "normal"), ("困難", "hard")],
                                  "normal", self._on_difficulty)
        self.diff_seg.pack(side="left")
        tk.Label(self.row2, text="先手", font=FONT_SMALL, bg=PANEL, fg=MUTED,
                 anchor="w").pack(side="left", padx=(18, 6))
        self.first_seg = Segmented(self.row2, [("我", "human"), ("電腦", "ai")],
                                   "human", self._on_first)
        self.first_seg.pack(side="left")

        status = tk.Frame(self, bg=BG)
        status.pack(fill="x", padx=24, pady=(14, 8))
        self.turn_dot = tk.Canvas(status, width=18, height=18, bg=BG,
                                  highlightthickness=0, bd=0)
        self.turn_dot.pack(side="left", padx=(0, 8))
        self.status_label = tk.Label(status, text="", font=FONT_STATUS,
                                     bg=BG, fg=TEXT, anchor="w")
        self.status_label.pack(side="left")
        TextButton(status, "重新開始", self._new_game).pack(side="right")
        self.steps_label = tk.Label(status, text="", font=FONT_SMALL,
                                    bg=BG, fg=MUTED)
        self.steps_label.pack(side="right", padx=12)

        self.board_view = BoardView(self, self._on_column, cell)
        self.board_view.pack(padx=24)

        self.hint_label = tk.Label(self, text="", font=FONT_SMALL, bg=BG, fg=MUTED)
        self.hint_label.pack(pady=(8, 16))

        master = self.winfo_toplevel()
        for i in range(COLS):
            master.bind(str(i + 1), lambda e, c=i: self._on_column(c))
        master.bind("r", lambda e: self._new_game())
        master.bind("R", lambda e: self._new_game())

    # ---- 排程（重新開始時一併作廢）

    def _later(self, ms, fn):
        gen = self._gen

        def guarded():
            if gen == self._gen:
                fn()

        self._after_ids.append(self.after(ms, guarded))

    # ---- 控制項

    def _on_mode(self, value):
        self.mode = value
        self._new_game()

    def _on_difficulty(self, value):
        self.engine = Engine(DIFFICULTY_DEPTH[value])
        self._new_game()

    def _on_first(self, value):
        self.human = P1 if value == "human" else P2
        self._new_game()

    # ---- 局流程

    def _new_game(self):
        self._gen += 1
        for aid in self._after_ids:
            try:
                self.after_cancel(aid)
            except Exception:
                pass
        self._after_ids = []

        self.game.reset()
        self.busy = False
        self.board_view.reset()

        # row2 一律顯示（只是停用），版面高度才不會隨模式變動而擠壓棋盤
        pve = self.mode == "pve"
        self.diff_seg.set_enabled(pve)
        self.first_seg.set_enabled(pve)

        self._refresh()
        if pve and self.game.turn != self.human:
            self._schedule_ai()

    def _on_column(self, col):
        if self.busy or self.game.over:
            return
        if self.mode == "pve" and self.game.turn != self.human:
            return
        if self.game.landing_row(col) is None:
            self.hint_label.configure(text=f"第 {col + 1} 欄已經滿了")
            return
        self._play(col)

    def _play(self, col):
        row = self.game.landing_row(col)
        if row is None:
            return
        player = self.game.turn
        self.game.drop(col)
        self.busy = True
        self.hint_label.configure(text="")
        self._refresh()
        self.board_view.animate_drop(col, row, player, self._after_move)

    def _after_move(self):
        self.busy = False
        self._refresh()
        if self.game.over:
            if self.game.win_cells:
                self.board_view.celebrate(self.game.win_cells)
            return
        if self.mode == "pve" and self.game.turn != self.human:
            self._schedule_ai()

    def _schedule_ai(self):
        self.busy = True
        self._refresh()
        self._later(200, self._ai_move)

    def _ai_move(self):
        col = self.engine.choose(self.game.board, self.game.turn)
        self.busy = False
        if col is None:
            return
        self._play(col)

    # ---- 顯示

    def _player_name(self, player):
        if self.mode == "pvp":
            return "紅方" if player == P1 else "黃方"
        return "你" if player == self.human else "電腦"

    def _refresh(self):
        game = self.game
        human_turn = self.mode == "pvp" or game.turn == self.human
        interactive = not game.over and not self.busy and human_turn
        self.board_view.set_state(game.board, game.turn, interactive)

        self.steps_label.configure(text=f"步數 {game.moves}")

        if game.winner:
            dot_color = CHIP_BASE[game.winner]
            if self.mode == "pvp":
                text = f"{self._player_name(game.winner)}獲勝！"
            elif game.winner == self.human:
                text = "你贏了！"
            else:
                text = "電腦獲勝"
            self.hint_label.configure(text="按 R 或「重新開始」再來一局")
        elif game.draw:
            dot_color = MUTED
            text = "平手！"
            self.hint_label.configure(text="按 R 或「重新開始」再來一局")
        else:
            dot_color = CHIP_BASE[game.turn]
            if self.mode == "pve" and game.turn != self.human:
                text = "電腦思考中…"
            else:
                text = f"{self._player_name(game.turn)}的回合"
                if not self.hint_label.cget("text"):
                    self.hint_label.configure(text="點擊棋盤或按 1–7 落子")

        self.status_label.configure(text=text)
        self.turn_dot.delete("all")
        self.turn_dot.create_oval(2, 2, 16, 16, fill=dot_color,
                                  outline=_shade(dot_color, -0.35), width=1)


def main():
    window = tk.Tk()
    window.title("Connect 4")
    window.configure(bg=BG)
    app = Connect4App(window)
    app.pack(fill="both", expand=True)

    # 視窗若超出螢幕，macOS 會直接把它壓扁、裁掉棋盤底部，所以先量再縮。
    # 扣掉的是選單列、標題列與上下留白。
    app.fit_to_height(window.winfo_screenheight() - 130)

    window.update_idletasks()
    window.geometry(f"{window.winfo_reqwidth()}x{window.winfo_reqheight()}")
    window.update_idletasks()
    window.resizable(False, False)
    window.mainloop()


if __name__ == "__main__":
    main()
