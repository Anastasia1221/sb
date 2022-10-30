from dataclasses import dataclass
from typing import List

from models import Board, CellState
from player import Player
from utils import Vec2


@dataclass(frozen=True)
class Renderer:
    show_ships: bool
    show_contours: bool

    def render_board(self, board: Board):
        print('\n'.join(self._lines(board)))

    def _lines(self, board: Board) -> List[str]:
        symbols = {
            CellState.Empty: '🟦',
            CellState.Ship: '⛵',
            CellState.Hit: '🔥',
            CellState.Miss: '❌',
            CellState.Dead: '💀',
        }

        lines = []
        for y in range(board.size.y):
            pieces = []
            for x, cell in enumerate(board.cells[y]):
                symbol = symbols[cell]

                if cell == CellState.Ship and not self.show_ships:
                    symbol = '🟦'

                if self.show_contours and cell == CellState.Empty and board.has_ship_nearby(Vec2(x, y)):
                    symbol = '🟥'

                pieces.append(symbol)

            lines.append(''.join(pieces))

        return lines

    @staticmethod
    def render_boards(boards: List[Board], renderers: List['Renderer'], players: List[Player]):
        all_lines = [r._lines(b) for b, r in zip(boards, renderers)]
        nrows = len(all_lines[0])

        annotation = 'Boards: ' + '\t -> '.join(p.name for p in players)
        rows = [annotation]
        for i in range(nrows):
            row = '\t'.join(all_lines[b][i] for b in range(len(boards)))
            rows.append(row)

        print('\n'.join(rows))

    @staticmethod
    def player() -> 'Renderer':
        return Renderer(show_ships=True, show_contours=False)

    @staticmethod
    def player_setup() -> 'Renderer':
        return Renderer(show_ships=True, show_contours=True)

    @staticmethod
    def enemy() -> 'Renderer':
        return Renderer(show_ships=False, show_contours=False)
