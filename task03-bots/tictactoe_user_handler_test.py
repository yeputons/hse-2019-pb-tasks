import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_tictactoe_user_handler_start(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    user_handler = TicTacToeUserHandler(send_message)

    user_handler.handle_message('Надо что-то делать, надо что-то делать!')
    user_handler.handle_message('Надо что-то делать... Надо выпить.')
    user_handler.handle_message('X 0 1')
    user_handler.handle_message('start')
    user_handler.handle_message('X 1 0')
    user_handler.handle_message('start')
    user_handler.handle_message('X 1 1')

    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
    ]


def test_tictactoe_user_handler_game_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    user_handler = TicTacToeUserHandler(send_message)

    user_handler.handle_message('start')
    user_handler.handle_message('X 1 1')
    user_handler.handle_message('O 0 1')
    user_handler.handle_message('X 2 2')
    user_handler.handle_message('O 0 0')
    user_handler.handle_message('X 0 2')
    user_handler.handle_message('O 1 2')
    user_handler.handle_message('X 2 0')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\nOX.\n...'),
        mocker.call('...\nOX.\n..X'),
        mocker.call('O..\nOX.\n..X'),
        mocker.call('O..\nOX.\nX.X'),
        mocker.call('O..\nOX.\nXOX'),
        mocker.call('O.X\nOX.\nXOX'),
        mocker.call('Game is finished, X wins')
    ]


def test_tictactoe_user_handler_game_o_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    user_handler = TicTacToeUserHandler(send_message)

    user_handler.handle_message('start')
    user_handler.handle_message('X 2 1')
    user_handler.handle_message('O 1 1')
    user_handler.handle_message('X 0 1')
    user_handler.handle_message('O 2 2')
    user_handler.handle_message('X 0 0')
    user_handler.handle_message('O 0 2')
    user_handler.handle_message('X 1 2')
    user_handler.handle_message('O 2 0')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n..X\n...'),
        mocker.call('...\n.OX\n...'),
        mocker.call('...\nXOX\n...'),
        mocker.call('...\nXOX\n..O'),
        mocker.call('X..\nXOX\n..O'),
        mocker.call('X..\nXOX\nO.O'),
        mocker.call('X..\nXOX\nOXO'),
        mocker.call('X.O\nXOX\nOXO'),
        mocker.call('Game is finished, O wins')
    ]


def test_tictactoe_user_handler_invalid_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    user_handler = TicTacToeUserHandler(send_message)

    user_handler.handle_message('start')
    user_handler.handle_message('x 0 0')
    user_handler.handle_message('X 0 0')
    user_handler.handle_message('X 0 1')
    user_handler.handle_message('O 0 0')
    user_handler.handle_message('O 0 1')
    user_handler.handle_message('X 1 0')
    user_handler.handle_message('O 1 2 3')
    user_handler.handle_message('O 1 3')
    user_handler.handle_message('O -5 1')
    user_handler.handle_message('O 2 2')
    user_handler.handle_message('X 2 0')
    user_handler.handle_message('S 1 2')
    user_handler.handle_message('start')
    user_handler.handle_message('S 1 2')
    user_handler.handle_message('S 1 2 3')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('X..\nO..\n...'),
        mocker.call('XX.\nO..\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('XX.\nO..\n..O'),
        mocker.call('XXX\nO..\n..O'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]


def test_tictactoe_user_handler_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    user_handler = TicTacToeUserHandler(send_message)
    user_handler.handle_message('start')
    user_handler.handle_message('X 1 1')
    user_handler.handle_message('O 0 0')

    user_handler.handle_message('X 0 1')
    user_handler.handle_message('O 2 1')
    user_handler.handle_message('X 1 0')
    user_handler.handle_message('O 1 2')
    user_handler.handle_message('X 0 2')
    user_handler.handle_message('O 2 0')
    user_handler.handle_message('X 2 2')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\nXX.\n...'),
        mocker.call('O..\nXXO\n...'),
        mocker.call('OX.\nXXO\n...'),
        mocker.call('OX.\nXXO\n.O.'),
        mocker.call('OX.\nXXO\nXO.'),
        mocker.call('OXO\nXXO\nXO.'),
        mocker.call('OXO\nXXO\nXOX'),
        mocker.call('Game is finished, draw')
    ]
