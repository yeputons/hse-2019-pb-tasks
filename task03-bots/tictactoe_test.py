from tictactoe import Player, TicTacToe


def test_game_draw() -> None:
    game = TicTacToe()
    assert not game.is_finished()
    assert game.winner() is None

    assert game.current_player() == Player.X
    assert game.can_make_turn(Player.X, col=0, row=0)
    assert not game.can_make_turn(Player.O, col=0, row=0)
    game.make_turn(Player.X, col=0, row=0)
    assert not game.is_finished()
    assert game.winner() is None

    assert not game.can_make_turn(Player.X, col=0, row=0)
    assert not game.can_make_turn(Player.O, col=0, row=0)
    assert game.current_player() == Player.O
    assert not game.can_make_turn(Player.X, col=1, row=0)
    assert game.can_make_turn(Player.O, col=1, row=0)
    game.make_turn(Player.O, col=1, row=0)
    assert not game.is_finished()
    assert game.winner() is None

    assert not game.can_make_turn(Player.X, col=0, row=0)
    assert not game.can_make_turn(Player.O, col=0, row=0)
    assert not game.can_make_turn(Player.X, col=1, row=0)
    assert not game.can_make_turn(Player.O, col=1, row=0)
    assert game.current_player() == Player.X
    assert game.can_make_turn(Player.X, col=2, row=0)
    assert not game.can_make_turn(Player.O, col=2, row=0)
    game.make_turn(Player.X, col=2, row=0)
    assert not game.is_finished()
    assert game.winner() is None

    # XOX
    # ...
    # ...

    assert game.current_player() == Player.O
    assert game.can_make_turn(Player.O, col=0, row=1)
    game.make_turn(Player.O, col=0, row=1)
    assert not game.is_finished()
    assert game.winner() is None

    # XOX
    # O..
    # ...

    assert game.current_player() == Player.X
    assert game.can_make_turn(Player.X, col=2, row=1)
    game.make_turn(Player.X, col=2, row=1)
    assert not game.is_finished()
    assert game.winner() is None

    # XOX
    # O.X
    # ...

    assert game.current_player() == Player.O
    assert game.can_make_turn(Player.O, col=1, row=1)
    game.make_turn(Player.O, col=1, row=1)
    assert not game.is_finished()
    assert game.winner() is None

    # XOX
    # OOX
    # ...

    assert game.current_player() == Player.X
    assert game.can_make_turn(Player.X, col=1, row=2)
    game.make_turn(Player.X, col=1, row=2)
    assert not game.is_finished()
    assert game.winner() is None

    # XOX
    # OOX
    # .X.

    assert game.current_player() == Player.O
    assert game.can_make_turn(Player.O, col=2, row=2)
    game.make_turn(Player.O, col=2, row=2)
    assert not game.is_finished()
    assert game.winner() is None

    # XOX
    # OOX
    # .XO

    assert game.current_player() == Player.X
    assert game.can_make_turn(Player.X, col=0, row=2)
    game.make_turn(Player.X, col=0, row=2)

    # XOX
    # OOX
    # XXO

    assert game.is_finished()
    assert game.winner() is None
    assert game.current_player() is None


def test_game_x_wins() -> None:
    game = TicTacToe()
    game.make_turn(Player.X, col=1, row=1)
    game.make_turn(Player.O, col=1, row=0)
    game.make_turn(Player.X, col=0, row=2)
    game.make_turn(Player.O, col=2, row=0)
    game.make_turn(Player.X, col=0, row=0)
    game.make_turn(Player.O, col=2, row=1)

    # XOO
    # .XO
    # X..
    assert not game.is_finished()
    assert game.winner() is None

    game.make_turn(Player.X, col=0, row=1)

    assert game.is_finished()
    assert game.winner() is Player.X


def test_game_o_wins() -> None:
    game = TicTacToe()
    game.make_turn(Player.X, col=0, row=0)
    game.make_turn(Player.O, col=1, row=1)
    game.make_turn(Player.X, col=1, row=0)
    game.make_turn(Player.O, col=2, row=0)
    game.make_turn(Player.X, col=0, row=1)

    # XXO
    # XO.
    # ...
    assert not game.is_finished()
    assert game.winner() is None

    game.make_turn(Player.O, col=0, row=2)

    assert game.is_finished()
    assert game.winner() is Player.O
