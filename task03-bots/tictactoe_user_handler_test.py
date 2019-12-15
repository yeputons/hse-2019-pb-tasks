import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_tictactoe_user_handle_start(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)

    handler.handle_message('Some dumb text for testing errors')
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 1 1')
    handler.handle_message('start')
    handler.handle_message('X 2 2')

    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n..X')
    ]


def test_tictactoe_user_handle_win_x(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)

    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 0 0')
    handler.handle_message('X 2 0')
    handler.handle_message('O 0 1')
    handler.handle_message('X 0 2')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O.X\n.X.\n...'),
        mocker.call('O.X\nOX.\n...'),
        mocker.call('O.X\nOX.\nX..'),
        mocker.call('Game is finished, X wins')
    ]


def test_tictactoe_user_handle_win_o(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)

    handler.handle_message('MORE TESTS')
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('OO 2 2')
    handler.handle_message('O 3 3')
    handler.handle_message('O 0 0')
    handler.handle_message('X 2 1')
    handler.handle_message('O DROP DATABASE')
    handler.handle_message('O 0 1')
    handler.handle_message('X 2 0')
    handler.handle_message('O 0 2')
    handler.handle_message('X 1 1')
    handler.handle_message('start')

    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.XX\n...'),
        mocker.call('Invalid turn'),
        mocker.call('O..\nOXX\n...'),
        mocker.call('O.X\nOXX\n...'),
        mocker.call('O.X\nOXX\nO..'),
        mocker.call('Game is finished, O wins'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...')
    ]


def test_tictactoe_user_handle_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)

    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 0 0')
    handler.handle_message('X 2 0')
    handler.handle_message('O 0 2')
    handler.handle_message('X 0 1')
    handler.handle_message('O 2 1')
    handler.handle_message('X 1 0')
    handler.handle_message('O 1 2')
    handler.handle_message('X 2 2')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O.X\n.X.\n...'),
        mocker.call('O.X\n.X.\nO..'),
        mocker.call('O.X\nXX.\nO..'),
        mocker.call('O.X\nXXO\nO..'),
        mocker.call('OXX\nXXO\nO..'),
        mocker.call('OXX\nXXO\nOO.'),
        mocker.call('OXX\nXXO\nOOX'),
        mocker.call('Game is finished, draw')
    ]
