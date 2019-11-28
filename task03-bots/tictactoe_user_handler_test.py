from pytest_mock import MockFixture
from tictactoe_user_handler import TicTacToeUserHandler


def test_draw(mocker: MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 2 0')
    handler.handle_message('X 1 0')
    handler.handle_message('O 0 1')
    handler.handle_message('X 2 1')
    handler.handle_message('O 1 1')
    handler.handle_message('X 0 2')
    handler.handle_message('O 2 2')
    handler.handle_message('X 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X.O\n...\n...'),
        mocker.call('XXO\n...\n...'),
        mocker.call('XXO\nO..\n...'),
        mocker.call('XXO\nO.X\n...'),
        mocker.call('XXO\nOOX\n...'),
        mocker.call('XXO\nOOX\nX..'),
        mocker.call('XXO\nOOX\nX.O'),
        mocker.call('XXO\nOOX\nXXO'),
        mocker.call('Game is finished, draw')
    ]
    assert handler.game is None


def test_x_wins(mocker: MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 0 1')
    handler.handle_message('X 1 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 2 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\nO..\n...'),
        mocker.call('XX.\nO..\n...'),
        mocker.call('XX.\nOO.\n...'),
        mocker.call('XXX\nOO.\n...'),
        mocker.call('Game is finished, X wins')
    ]
    assert handler.game is None


def test_o_wins(mocker: MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 0 1')
    handler.handle_message('X 1 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 2 2')
    handler.handle_message('O 2 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\nO..\n...'),
        mocker.call('XX.\nO..\n...'),
        mocker.call('XX.\nOO.\n...'),
        mocker.call('XX.\nOO.\n..X'),
        mocker.call('XX.\nOOO\n..X'),
        mocker.call('Game is finished, O wins')
    ]
    assert handler.game is None


def test_invalid_commands(mocker):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('X 0 0')
    handler.handle_message('start')
    handler.handle_message('O 0 0')
    handler.handle_message('X 0 0')
    handler.handle_message('X 0 1')
    handler.handle_message('O 0 0')
    handler.handle_message('O 0 1')
    handler.handle_message('O 0 2')
    handler.handle_message('X 1 0')
    handler.handle_message('O 1 2')
    handler.handle_message('X 2 0')
    handler.handle_message('O 0 2')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('X..\nO..\n...'),
        mocker.call('Invalid turn'),
        mocker.call('XX.\nO..\n...'),
        mocker.call('XX.\nO..\n.O.'),
        mocker.call('XXX\nO..\n.O.'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started')
    ]
