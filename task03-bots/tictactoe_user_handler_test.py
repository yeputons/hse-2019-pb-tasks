import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_github_example(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('hi')
    handler.handle_message('X 1 1')
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 0 1')
    handler.handle_message('O 0 0')
    handler.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\nOX.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n...\n...'),
    ]


def test_multiple_start_and_start(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('\\start')
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('asd')
    handler.handle_message('start')
    handler.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n...'),
    ]


def test_win_X(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 0 1')
    handler.handle_message('O 2 1')
    handler.handle_message('X 0 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X..\nXO.\n...'),
        mocker.call('X..\nXOO\n...'),
        mocker.call('X..\nXOO\nX..'),
        mocker.call('Game is finished, X wins'),
    ]


def test_win_O(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 0 1')
    handler.handle_message('O 1 2')
    handler.handle_message('X 2 2')
    handler.handle_message('O 1 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X..\nXO.\n...'),
        mocker.call('X..\nXO.\n.O.'),
        mocker.call('X..\nXO.\n.OX'),
        mocker.call('XO.\nXO.\n.OX'),
        mocker.call('Game is finished, O wins'),
    ]


def test_win_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 2 0')
    handler.handle_message('O 1 0')
    handler.handle_message('X 2 1')
    handler.handle_message('O 2 2')
    handler.handle_message('X 0 1')
    handler.handle_message('O 0 2')
    handler.handle_message('X 1 2')

    handler.handle_message('X 2 1')
    handler.handle_message('asd')
    handler.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X.X\n.O.\n...'),
        mocker.call('XOX\n.O.\n...'),
        mocker.call('XOX\n.OX\n...'),
        mocker.call('XOX\n.OX\n..O'),
        mocker.call('XOX\nXOX\n..O'),
        mocker.call('XOX\nXOX\nO.O'),
        mocker.call('XOX\nXOX\nOXO'),
        mocker.call('Game is finished, draw'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
    ]
