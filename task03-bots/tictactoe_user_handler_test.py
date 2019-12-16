import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_integrate_draw(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)

    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 0')
    handler.handle_message('X 0 1')
    handler.handle_message('O 1 1')
    handler.handle_message('X 1 2')
    handler.handle_message('O 0 2')
    handler.handle_message('X 2 0')
    handler.handle_message('O 2 1')
    handler.handle_message('X 2 2')

    assert send_message.call_args_list[-2:] == [
        mocker.call('XXO\nOOX\nXOX'),
        mocker.call('Game is finished, draw')
    ]


def test_integrate_invalid_start(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)

    handler.handle_message('Start, please')
    handler.handle_message('Password?')
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('X 0 1')
    handler.handle_message('X 0 1')
    handler.handle_message('start')
    handler.handle_message('X 0 1')
    handler.handle_message('O 0 1')

    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('Invalid turn')
    ]


def test_integrate_o_wins(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)

    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 2 1')
    handler.handle_message('X 0 1')
    handler.handle_message('O 2 2')
    handler.handle_message('X 0 0')
    handler.handle_message('O 2 0')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\n.O.'),
        mocker.call('.X.\n.X.\n.O.'),
        mocker.call('.X.\n.X.\n.OO'),
        mocker.call('XX.\n.X.\n.OO'),
        mocker.call('XX.\n.X.\nOOO'),
        mocker.call('Game is finished, O wins')
    ]
