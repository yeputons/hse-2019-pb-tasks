from pytest_mock import MockFixture
from tictactoe_user_handler import TicTacToeUserHandler


def test_ordinary_case(mocker: MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start\n')
    handler.handle_message('X 1 1\n')
    handler.handle_message('O 0 2\n')
    handler.handle_message('X 2 0\n')
    handler.handle_message('O 2 2\n')
    handler.handle_message('X 0 0\n')
    handler.handle_message('O 1 0\n')
    handler.handle_message('X 0 1\n')
    handler.handle_message('O 2 1\n')
    handler.handle_message('X 1 2\n')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\nO..'),
        mocker.call('..X\n.X.\nO..'),
        mocker.call('..X\n.X.\nO.O'),
        mocker.call('X.X\n.X.\nO.O'),
        mocker.call('XOX\n.X.\nO.O'),
        mocker.call('XOX\nXX.\nO.O'),
        mocker.call('XOX\nXXO\nO.O'),
        mocker.call('XOX\nXXO\nOXO'),
        mocker.call('Game is finished, draw')
    ]
    assert handler.game is None


def test_o_win_case(mocker: MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start\n')
    handler.handle_message('X 1 1\n')
    handler.handle_message('O 0 2\n')
    handler.handle_message('X 2 0\n')
    handler.handle_message('O 2 2\n')
    handler.handle_message('X 0 0\n')
    handler.handle_message('O 1 2\n')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\nO..'),
        mocker.call('..X\n.X.\nO..'),
        mocker.call('..X\n.X.\nO.O'),
        mocker.call('X.X\n.X.\nO.O'),
        mocker.call('X.X\n.X.\nOOO'),
        mocker.call('Game is finished, O wins')
    ]
    assert handler.game is None


def test_x_win_case(mocker: MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start\n')
    handler.handle_message('X 1 1\n')
    handler.handle_message('O 0 2\n')
    handler.handle_message('X 2 0\n')
    handler.handle_message('O 2 2\n')
    handler.handle_message('X 0 0\n')
    handler.handle_message('O 2 1\n')
    handler.handle_message('X 1 0\n')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\nO..'),
        mocker.call('..X\n.X.\nO..'),
        mocker.call('..X\n.X.\nO.O'),
        mocker.call('X.X\n.X.\nO.O'),
        mocker.call('X.X\n.XO\nO.O'),
        mocker.call('XXX\n.XO\nO.O'),
        mocker.call('Game is finished, X wins')
    ]
    assert handler.game is None


def test_for_other_messages(mocker: MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('O 2 2\n')
    handler.handle_message('start\n')
    handler.handle_message('X 1 1\n')
    handler.handle_message('O 0 2\n')
    handler.handle_message('X 2 0\n')
    handler.handle_message('O 2 2\n')
    handler.handle_message('X 0 0\n')
    handler.handle_message('X 1 0\n')
    handler.handle_message('O 2 1\n')
    handler.handle_message('X 1 0\n')
    handler.handle_message('X 1 1\n')

    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\nO..'),
        mocker.call('..X\n.X.\nO..'),
        mocker.call('..X\n.X.\nO.O'),
        mocker.call('X.X\n.X.\nO.O'),
        mocker.call('Invalid turn'),
        mocker.call('X.X\n.XO\nO.O'),
        mocker.call('XXX\n.XO\nO.O'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started')
    ]
    assert handler.game is None
