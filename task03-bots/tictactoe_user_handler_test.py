from typing import List, Optional
from tictactoe_user_handler import TicTacToeUserHandler, Player
import pytest_mock


# def test_chat_broadcast(mocker: pytest_mock.MockFixture) -> None:
#     send_message = mocker.stub(name='send_message_stub')
#     bot = ChatBot(send_message)
#     bot.handle_message(10, 'hello')
#     bot.handle_message(11, 'world')
#     assert send_message.call_args_list == [
#         mocker.call(10, '#10: hello'),
#         mocker.call(10, '#11: world'),
#         mocker.call(11, '#11: world'),
#     ]


# def send_message(message: str) -> None:
#     print(message)


def test_handler_invalid_input_number(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('12')
    assert send_message.call_args_list == [
        mocker.call('Invalid turn'),
    ]


def test_handler_invalid_input_not_enough_args(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('X 0')
    assert send_message.call_args_list == [
        mocker.call('Invalid turn'),
    ]


def test_handler_not_started_game(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('X 0 1')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
    ]


def test_handler_invalid_choice(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.start_game()
    bot.handle_message('Z 0 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('Incorrect choice (X|O)'),
    ]


def test_handler_invalid_values(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.start_game()
    bot.handle_message('X 3 3')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
    ]


def test_handler_impossible_turn_same_spot(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.start_game()
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
    ]


def test_handler_impossible_turn_another_player(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.start_game()
    bot.handle_message('X 0 0')
    bot.handle_message('X 1 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
    ]


def test_handler_start_game(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.start_game()
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
    ]


def test_send_field_mid_game(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.start_game()
    field: List[List[Optional[Player]]] = [
        [Player.X, Player.O, Player.X],
        [None, None, None],
        [None, None, None]
    ]
    bot.game.field = field
    bot.send_field()
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('XOX\n...\n...'),
    ]


def test_start_game(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.start_game()
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
    ]
    assert bot.game


def test_make_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.start_game()
    bot.make_turn(Player.X, row=1, col=0)
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\nX..\n...'),
    ]
    assert bot.game.field[1][0] == Player.X


def test_make_turn_game_finished(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.start_game()
    bot.game.field = [
        [Player.X, Player.X, None],
        [Player.O, Player.O, None],
        [None, None, None]
    ]
    bot.make_turn(Player.X, row=0, col=2)
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('XXX\nOO.\n...'),
        mocker.call('Game is finished, X wins')
    ]


def test_make_turn_game_finished_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.start_game()
    bot.game.field = [
        [Player.X, Player.X, Player.O],
        [Player.O, Player.O, Player.X],
        [Player.X, Player.O, None],
    ]
    bot.make_turn(Player.X, row=2, col=2)
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('XXO\nOOX\nXOX'),
        mocker.call('Game is finished, draw'),
    ]
