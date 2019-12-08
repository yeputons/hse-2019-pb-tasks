import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('who?')
    handler.handle_message('X 1 1')
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 0 1')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 0')
    handler.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\nOX.\n...'),
        mocker.call('X..\nOX.\n...'),
        mocker.call('XO.\nOX.\n...'),
        mocker.call('XO.\nOX.\n..X'),
        mocker.call('Game is finished, X wins'),
    ]


def test_o_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 2 0')
    handler.handle_message('X 1 2')
    handler.handle_message('O 2 1')
    handler.handle_message('X 0 2')
    handler.handle_message('O 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('..O\n.X.\n...'),
        mocker.call('..O\n.X.\n.X.'),
        mocker.call('..O\n.XO\n.X.'),
        mocker.call('..O\n.XO\nXX.'),
        mocker.call('..O\n.XO\nXXO'),
        mocker.call('Game is finished, O wins'),
    ]


def test_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 1 0')
    handler.handle_message('X 0 0')
    handler.handle_message('O 2 2')
    handler.handle_message('X 2 0')
    handler.handle_message('O 0 2')
    handler.handle_message('X 1 2')
    handler.handle_message('O 0 1')
    handler.handle_message('X 2 1')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('.O.\n.X.\n...'),
        mocker.call('XO.\n.X.\n...'),
        mocker.call('XO.\n.X.\n..O'),
        mocker.call('XOX\n.X.\n..O'),
        mocker.call('XOX\n.X.\nO.O'),
        mocker.call('XOX\n.X.\nOXO'),
        mocker.call('XOX\nOX.\nOXO'),
        mocker.call('XOX\nOXX\nOXO'),
        mocker.call('Game is finished, draw'),
    ]
