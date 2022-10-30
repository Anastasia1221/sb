from dataclasses import dataclass
from typing import List, Dict
from models import Board, PlacementException, GenerationException, InvalidShotException
from player import Player, AiPlayer
from rendering import Renderer
from utils import Vec2


GEN_ATTTEMPS = 1000


@dataclass(frozen=True)
class Game:
    board_size: Vec2
    fleet: Dict[int, int]
    players: List[Player]
    renderers: List[Renderer]
    pause: bool = False

    def play(self):
        assert len(self.players) == 2
        assert len(self.renderers) == 2

        boards = self._make_boards()
        print('Game starts!')
        Renderer.render_boards(boards, self.renderers, self.players)
        self._play(boards)

    def _make_boards(self):
        boards = [Board.make(self.board_size) for _ in self.players]
        for player, board in zip(self.players, boards):
            def gen_ship(ship_length: int):
                for _ in range(GEN_ATTTEMPS):
                    player.on_before_placement(board)
                    candidate = player.gen_ship(ship_length)
                    try:
                        board.add_ship(candidate)
                        return
                    except PlacementException as err:
                        player.on_invalid_placement(err)

                raise GenerationException(GEN_ATTTEMPS)

            for length, cnt in self.fleet.items():
                for _ in range(cnt):
                    gen_ship(length)

        return boards

    def _play(self, boards: List[Board]):
        def make_shot(p: Player, eboard: Board):
            while True:
                coord = p.fire()
                try:
                    eboard.shoot(coord)
                    print(f"Player {player.name} shoots at: {coord}")
                    return
                except InvalidShotException as e:
                    player.on_invalid_shot(e)

        while True:
            print('\n' * 2)

            for player, enemy_board in zip(self.players, reversed(boards)):
                make_shot(player, enemy_board)
                if enemy_board.is_finished:
                    Renderer.render_boards(boards, self.renderers, self.players)
                    print(f'{player.name} won!')
                    return

            print('\n' * 2)
            Renderer.render_boards(boards, self.renderers, self.players)
            if self.pause:
                input("Press any key to continue")


def main():
    board_size = Vec2(6, 6)
    fleet = {
        3: 1,
        2: 2
    }
    game = Game(
        board_size,
        fleet,
        [AiPlayer('Bot 1', board_size), AiPlayer('Bot 2', board_size)],
        [Renderer.player(), Renderer.player()],
        pause=True
    )

    # game = Game(
    #     board_size,
    #     fleet,
    #     [HumanPlayer('Human'), AiPlayer('Bot 2', board_size)],
    #     [Renderer.player(), Renderer.enemy()]
    # )

    game.play()


if __name__ == '__main__':
    main()
