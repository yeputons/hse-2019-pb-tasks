from typing import List, Optional
from tictactoe_user_handler import TicTacToeUserHandler, Player


def send_message(message: str) -> None:
    print(message)


def test_handler_invalid_input_number(capsys):
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.handle_message('12')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Invalid input - ValueError\n'


def test_handler_invalid_input_not_enough_args(capsys):
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.handle_message('X 0')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Invalid input - ValueError\n'


def test_handler_not_started_game(capsys):
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.handle_message('X 0 1')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Game is not started\n'


def test_handler_invalid_choice(capsys):
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.start_game()
    bot.handle_message('Z 0 1')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '. . . \n. . . \n. . . \nGame is started\nIncorrect choice (X|O)\n'


def test_handler_invalid_values(capsys):
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.start_game()
    bot.handle_message('X 3 3')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '. . . \n. . . \n. . . \nGame is started\nInvalid values of col or row\n'


def test_handler_impossible_turn_same_spot(capsys):
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.start_game()
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 0')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '. . . \n. . . \n. . . \nGame is started\nX . . \n. . . \n. . . \nIncorrect Turn\n'


def test_handler_impossible_turn_another_player(capsys):
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.start_game()
    bot.handle_message('X 0 0')
    bot.handle_message('X 1 0')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '. . . \n. . . \n. . . \nGame is started\nX . . \n. . . \n. . . \nIncorrect Turn\n'


def test_handler_start_game(capsys):
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.start_game()
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '. . . \n. . . \n. . . \nGame is started\n'


def test_send_field_mid_game(capsys):
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.start_game()
    field: List[List[Optional[Player]]] = [
        [Player.X, Player.O, Player.X],
        [None, None, None],
        [None, None, None]
    ]
    bot.game.field = field
    bot.send_field()
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '. . . \n. . . \n. . . \nGame is started\nX O X \n. . . \n. . . \n'


def test_start_game(capsys):
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.start_game()
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '. . . \n. . . \n. . . \nGame is started\n'
    assert bot.game


def test_make_turn(capsys):
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.start_game()
    bot.make_turn(Player.X, row=1, col=0)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '. . . \n. . . \n. . . \nGame is started\n. . . \nX . . \n. . . \n'
    assert bot.game.field[1][0] == Player.X


def test_make_turn_game_finished(capsys):
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.start_game()
    bot.game.field = [
        [Player.X, Player.X, None],
        [Player.O, Player.O, None],
        [None, None, None]
    ]
    bot.make_turn(Player.X, row=0, col=2)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '. . . \n. . . \n. . . \nGame is started\nX X X \nO O . \n. . . \nGame is finished\n'
    assert bot.game.field[0][1] == Player.X
