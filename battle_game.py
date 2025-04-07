import numpy as np
import pygame
import tkinter as tk
from tkinter import scrolledtext

class BattleGame:
    def __init__(self):
        print("Initializing game...")
        self.board_size = 9
        self.cell_size = 60
        self.log_area_height = 150
        self.window_width = self.board_size * self.cell_size
        self.window_height = self.board_size * self.cell_size + self.log_area_height
        self.board = np.zeros((self.board_size, self.board_size), dtype=int)
        self.players = [
            {'soldiers': (1, 1), 'king': (0, 0), 'symbol': 1, 'king_symbol': 3, 'mask': np.ones((3, 3), dtype=int)},
            {'soldiers': (5, 5), 'king': (8, 8), 'symbol': 2, 'king_symbol': 4, 'mask': np.ones((3, 3), dtype=int)* 2}
        ]
        print("Player 1 initial mask:")
        print(self.players[0]['mask'])
        print("Player 2 initial mask:")
        print(self.players[1]['mask'])
        self.hidden_king = {1: self.players[0]['king'], 2: self.players[1]['king']}
        self.place_pieces()
        print("Game initialized successfully.")
        pygame.init()
        self.font = pygame.font.SysFont(None, 24)
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        self.selected_piece = None
        self.current_player = 1
        self.selected_is_king = False
        # ログ用の変数と Tkinter のログウィンドウを作成
        self.log_messages = []

    #ログ表示用の関数
    def log(self, message):
        print(message)
        self.log_messages.append(message)
        if len(self.log_messages) > 10:
            self.log_messages.pop(0)
    def place_pieces(self):
        print("Placing pieces on the board...")
        for player in self.players:
            sx, sy = player['soldiers']
            self.board[sx:sx+3, sy:sy+3] = player['mask']
            kx, ky = player['king']
            self.board[kx, ky] = player['king_symbol']
        print("Pieces placed successfully.")

    def draw_board(self):
        self.screen.fill((255, 255, 255))
        for x in range(self.board_size):
            for y in range(self.board_size):
                rect = pygame.Rect(y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (200, 200, 200), rect, 1)
                if self.board[x, y] == 1:
                    pygame.draw.circle(self.screen, (0, 0, 255), rect.center, self.cell_size // 3)
                elif self.board[x, y] == 2:
                    pygame.draw.circle(self.screen, (255, 0, 0), rect.center, self.cell_size // 3)
                elif self.board[x, y] in [3, 4]:
                    pygame.draw.rect(self.screen, (0, 255, 0), rect)
        if self.selected_piece is not None:
            if self.selected_is_king:
                rect = pygame.Rect(self.selected_piece[1] * self.cell_size,
                                self.selected_piece[0] * self.cell_size,
                                self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, (255, 255, 0), rect, 3)
            else:
                # 兵士グループの場合：soldier_pos は兵士ブロックの左上座標
                soldier_pos = self.players[self.current_player - 1]['soldiers']
                mask = self.players[self.current_player - 1]['mask']
                # 盤面上の左上のピクセル座標を計算
                top = soldier_pos[0] * self.cell_size
                left = soldier_pos[1] * self.cell_size
                # mask の各セルについて、隣接セルが無効な部分に境界線を描画
                for i in range(3):
                    for j in range(3):
                        if mask[i, j] != 0:
                            cell_left = left + j * self.cell_size
                            cell_top = top + i * self.cell_size
                            # 左辺
                            if j == 0 or mask[i, j-1] == 0:
                                pygame.draw.line(self.screen, (255, 255, 0),
                                                (cell_left, cell_top),
                                                (cell_left, cell_top + self.cell_size), 3)
                            # 右辺
                            if j == 2 or mask[i, j+1] == 0:
                                pygame.draw.line(self.screen, (255, 255, 0),
                                                (cell_left + self.cell_size, cell_top),
                                                (cell_left + self.cell_size, cell_top + self.cell_size), 3)
                            # 上辺
                            if i == 0 or mask[i-1, j] == 0:
                                pygame.draw.line(self.screen, (255, 255, 0),
                                                (cell_left, cell_top),
                                                (cell_left + self.cell_size, cell_top), 3)
                            # 下辺
                            if i == 2 or mask[i+1, j] == 0:
                                pygame.draw.line(self.screen, (255, 255, 0),
                                                (cell_left, cell_top + self.cell_size),
                                                (cell_left + self.cell_size, cell_top + self.cell_size), 3)
        # ログを画面下部に描画
        self.draw_logs()
        pygame.display.flip()

    def draw_logs(self):
        # ログを右下に表示する例
        y_offset = self.window_size - 20 * len(self.log_messages)
        for msg in self.log_messages:
            text_surf = self.font.render(msg, True, (0, 0, 0))
            self.screen.blit(text_surf, (5, y_offset))
            y_offset += 20
    # 駒をクリックしたときのログ更新
    def handle_click(self, pos):
        x, y = pos[1] // self.cell_size, pos[0] // self.cell_size
        if self.board[x, y] in [1, 3] and self.current_player == 1:
            if self.board[x, y] == 1:
                self.selected_piece = self.players[0]['soldiers']
                self.selected_is_king = False
                self.log(f"Selected soldier group for player 1 at {self.selected_piece}.")
            else:
                self.selected_piece = (x, y)
                self.selected_is_king = True
                self.log(f"Selected king for player 1 at ({x}, {y}).")
        elif self.board[x, y] in [2, 4] and self.current_player == 2:
            if self.board[x, y] == 2:
                self.selected_piece = self.players[1]['soldiers']
                self.selected_is_king = False
                self.log(f"Selected soldier group for player 2 at {self.selected_piece}.")
            else:
                self.selected_piece = (x, y)
                self.selected_is_king = True
                self.log(f"Selected king for player 2 at ({x}, {y}).")
        else:
            self.log(f"Invalid selection at cell ({x}, {y}). Not your movable piece.")

    def update_soldier_mask(self, mask, dest_area, enemy, player_symbol):
        new_mask = mask.copy()
        for i in range(mask.shape[0]):
            for j in range(mask.shape[1]):
                if mask[i, j] == player_symbol and dest_area[i, j] in enemy:
                    new_mask[i, j] = 0
        return new_mask

    def move_selected_piece(self, direction):
        if not self.selected_piece:
            return
        dx, dy = direction
        if self.selected_is_king:
            x, y = self.selected_piece
            new_x, new_y = x + dx, y + dy
            if not (0 <= new_x < self.board_size and 0 <= new_y < self.board_size):
                self.log("Invalid move: Out of bounds.")
                return
            if self.board[new_x, new_y] in [0, 2, 4]:
                if self.board[new_x, new_y] == 4:
                    self.log(f"Player {self.current_player} wins! Game over.")
                    pygame.quit()
                    exit()
                self.board[new_x, new_y] = self.board[x, y]
                self.board[x, y] = 0
                self.hidden_king[self.current_player] = (new_x, new_y)
            else:
                self.log("Invalid move: Space occupied by friendly unit.")
                return
        else:
            orig = self.players[self.current_player - 1]['soldiers']
            print(f"Player {self.current_player} original soldier position: {orig}")  # デバッグ出力
            mask = self.players[self.current_player - 1]['mask']
            print(f"Player {self.current_player} mask: {mask}")
            new_x, new_y = orig[0] + dx, orig[1] + dy
            if not (0 <= new_x <= self.board_size - 3 and 0 <= new_y <= self.board_size - 3):
                self.log("Invalid move: Out of bounds.")
                return
            # コピーした移動先の領域
            dest_area = self.board[new_x:new_x+3, new_y:new_y+3].copy()
            print(f"Player {self.current_player} dest area:")
            print(dest_area)
            enemy = [2, 4] if self.current_player == 1 else [1, 3]

            # 現在のプレイヤーに応じた敵番号と敵のデータを取得
            if self.current_player == 1:
                enemy_symbol = 2
                enemy_king_symbol = 4
                enemy_index = 1
            else:
                enemy_symbol = 1
                enemy_king_symbol = 3
                enemy_index = 0
            # 敵兵士ブロックの情報
            enemy_orig = self.players[enemy_index]['soldiers']
            print(f"Player {self.current_player} enemy soldier position: {enemy_orig}")
            enemy_mask = self.players[enemy_index]['mask'].copy()
            print(f"Player {self.current_player} enemy soldier mask: {enemy_mask}")
            # 移動先ブロック内で、もし敵兵士ブロックと重なる領域があれば、敵マスクを更新（重なった箇所を0にする）
            # まず、重なり領域の範囲を計算
            overlap_top = max(new_x, enemy_orig[0])
            overlap_left = max(new_y, enemy_orig[1])
            overlap_bottom = min(new_x+3, enemy_orig[0]+3)
            overlap_right = min(new_y+3, enemy_orig[1]+3)
            
            captured_positions = []  # 捕獲したマスのリスト
            if overlap_bottom > overlap_top and overlap_right > overlap_left:
                for i in range(overlap_top, overlap_bottom):
                    for j in range(overlap_left, overlap_right):
                        # 重なりセルの相対座標（敵側）
                        rel_i = i - enemy_orig[0]
                        rel_j = j - enemy_orig[1]
                        # もし移動する兵士側のマスクが有効なら、敵のそのセルを捕獲（0にする）
                        if mask[i-new_x, j-new_y] != 0 and enemy_mask[rel_i, rel_j] != 0:
                            print(f"Captured enemy soldier at enemy_mask[{rel_i}][{rel_j}] (Board Position: {i}, {j})")
                            enemy_mask[rel_i, rel_j] = 0
                            captured_positions.append((rel_i, rel_j, i, j))
                # 捕獲したマスを表示
                if captured_positions:
                    print("Captured Positions:")
                    for rel_i, rel_j, i, j in captured_positions:
                        print(f"  enemy_mask[{rel_i}][{rel_j}] -> 0 (Board Position: {i}, {j})")
                   # 更新後の敵マスクを表示
                print("Updated Enemy Mask:")
                for row in enemy_mask:
                    print("  " + " ".join(map(str, row)))
            # 更新した敵マスクを保存
            self.players[enemy_index]['mask'] = enemy_mask
            # new_area を、dest_area の中から敵の番号だけを保持し、その他は 0 にする
            new_area = np.where(np.isin(dest_area, enemy), dest_area, 0)
            for i in range(3):
                for j in range(3):
                    if mask[i, j] != 0:
                        new_area[i, j] = self.current_player
                        
            print(f"Player {self.current_player} new area: {new_area}")
            # 元の移動元ブロックのうち、mask が有効なセルのみ 0 にする
            for i in range(3):
                for j in range(3):
                    if mask[i, j] != 0:
                        self.board[orig[0] + i, orig[1] + j] = 0

            # 移動先ブロックを更新
            self.board[new_x:new_x+3, new_y:new_y+3] = new_area
            # 更新後、移動側の兵士データはマスクそのまま、移動先座標のみ更新
            self.players[self.current_player - 1]['soldiers'] = (new_x, new_y)
        self.selected_piece = None
        self.log(f"Player {self.current_player} moved soldiers to ({new_x}, {new_y})")
        self.current_player = 2 if self.current_player == 1 else 1
        self.log(f"Next turn: Player {self.current_player}")

    def game_loop(self):
        running = True
        while running:
            self.draw_board()
            self.log_window.update()  # Tkinterウィンドウの更新
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.move_selected_piece((-1, 0))
                    elif event.key == pygame.K_s:
                        self.move_selected_piece((1, 0))
                    elif event.key == pygame.K_a:
                        self.move_selected_piece((0, -1))
                    elif event.key == pygame.K_d:
                        self.move_selected_piece((0, 1))
        pygame.quit()
        self.log_window.destroy()
if __name__ == "__main__":
    game = BattleGame()
    game.game_loop()
