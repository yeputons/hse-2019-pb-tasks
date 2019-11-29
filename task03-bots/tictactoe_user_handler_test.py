from pytest_mock import MockFixture
from tictactoe_user_handler import TicTacToeUserHandler


def test_draw(mocker: MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start\n')
    handler.handle_message('X 1 0\n')
    handler.handle_message('O 1 1\n')
    handler.handle_message('X 1 2\n')
    handler.handle_message('O 2 0\n')
    handler.handle_message('X 2 1\n')
    handler.handle_message('O 2 2\n')
    handler.handle_message('X 0 0\n')
    handler.handle_message('O 0 1\n')
    handler.handle_message('X 0 2\n')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('.X.\n.O.\n...'),
        mocker.call('.X.\n.O.\n.X.'),
        mocker.call('.XO\n.O.\n.X.'),
        mocker.call('.XO\n.OX\n.X.'),
        mocker.call('.XO\n.OX\n.XO'),
        mocker.call('XXO\n.OX\n.XO'),
        mocker.call('XXO\nOOX\n.XO'),
        mocker.call('XXO\nOOX\nXXO'),
        mocker.call('Game is finished, draw')
    ]
    assert handler.game is None


def test_o_win(mocker: MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start\n')
    handler.handle_message('X 0 0\n')
    handler.handle_message('O 2 2\n')
    handler.handle_message('X 1 0\n')
    handler.handle_message('O 1 2\n')
    handler.handle_message('X 2 1\n')
    handler.handle_message('O 0 2\n')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n...\n..O'),
        mocker.call('XX.\n...\n..O'),
        mocker.call('XX.\n...\n.OO'),
        mocker.call('XX.\n..X\n.OO'),
        mocker.call('XX.\n..X\nOOO'),
        mocker.call('Game is finished, O wins')
    ]
    assert handler.game is None


def test_x_win(mocker: MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start\n')
    handler.handle_message('X 0 0\n')
    handler.handle_message('O 0 2\n')
    handler.handle_message('X 1 0\n')
    handler.handle_message('O 2 2\n')
    handler.handle_message('X 2 0\n')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n...\nO..'),
        mocker.call('XX.\n...\nO..'),
        mocker.call('XX.\n...\nO.O'),
        mocker.call('XXX\n...\nO.O'),
        mocker.call('Game is finished, X wins')
    ]
    assert handler.game is None


def test_other_commands(mocker: MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('X 0 0\n')
    handler.handle_message('start\n')
    handler.handle_message('X 1 0\n')
    handler.handle_message('X 1 0\n')
    handler.handle_message('O 1 1\n')
    handler.handle_message('O 1 1\n')
    handler.handle_message('X 1 2\n')
    handler.handle_message('O 2 0\n')
    handler.handle_message('X 2 1\n')
    handler.handle_message('O 2 2\n')
    handler.handle_message('X 0 0\n')
    handler.handle_message('O 0 1\n')
    handler.handle_message('X 0 2\n')
    handler.handle_message('X 0 2\n')

    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('.X.\n.O.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('.X.\n.O.\n.X.'),
        mocker.call('.XO\n.O.\n.X.'),
        mocker.call('.XO\n.OX\n.X.'),
        mocker.call('.XO\n.OX\n.XO'),
        mocker.call('XXO\n.OX\n.XO'),
        mocker.call('XXO\nOOX\n.XO'),
        mocker.call('XXO\nOOX\nXXO'),
        mocker.call('Game is finished, draw'),
        mocker.call('Game is not started')
    ]
    assert handler.game is None