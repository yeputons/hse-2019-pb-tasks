import pytest
import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_integrate_start_many_games(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('not start')
    handler.handle_message('not start2')
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('...\n...\n...'),
    ]


def test_integrate_invalid_turn(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 1 1')

    handler.handle_message('X 1 1')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 1')

    with pytest.raises(AssertionError):
        handler.handle_message('O -1 0')
    with pytest.raises(AssertionError):
        handler.handle_message('O 3 0')
    with pytest.raises(AssertionError):
        handler.handle_message('O 0 -1')
    with pytest.raises(AssertionError):
        handler.handle_message('O 0 3')

    handler.handle_message('O 0 0')

    handler.handle_message('O 2 2')
    handler.handle_message('X 1 1')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),

        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),

        mocker.call('O..\n.X.\n...'),

        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
    ]


def test_integrate_player_x_win(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 2 0')
    handler.handle_message('X 0 1')
    handler.handle_message('O 2 1')
    handler.handle_message('X 0 2')
    handler.handle_message('O 2 2')
    assert send_message.call_args_list[-2:] == [
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started'),
    ]


def test_integrate_player_o_win(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 2 0')
    handler.handle_message('X 0 1')
    handler.handle_message('O 2 1')
    handler.handle_message('X 1 1')
    handler.handle_message('O 2 2')
    handler.handle_message('X 1 2')
    assert send_message.call_args_list[-2:] == [
        mocker.call('Game is finished, O wins'),
        mocker.call('Game is not started'),
    ]


def test_integrate_draw(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')

    handler.handle_message('X 0 0')
    handler.handle_message('O 1 0')
    handler.handle_message('X 2 0')
    handler.handle_message('O 0 1')
    handler.handle_message('X 0 2')
    handler.handle_message('O 1 1')
    handler.handle_message('X 1 2')
    handler.handle_message('O 2 2')
    handler.handle_message('X 2 1')
    handler.handle_message('X 2 1')
    assert send_message.call_args_list[-2:] == [
        mocker.call('Game is finished, draw'),
        mocker.call('Game is not started'),
    ]
