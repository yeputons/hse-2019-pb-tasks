import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_x_wins(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 2')
    handler.handle_message('O 1 1')
    handler.handle_message('X 0 1')
    handler.handle_message('O 1 0')
    handler.handle_message('X 2 2')
    handler.handle_message('O 0 0')
    handler.handle_message('X 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('...\n'
                    '...\n'
                    'X..'),
        mocker.call('...\n'
                    '.O.\n'
                    'X..'),
        mocker.call('...\n'
                    'XO.\n'
                    'X..'),
        mocker.call('.O.\n'
                    'XO.\n'
                    'X..'),
        mocker.call('.O.\n'
                    'XO.\n'
                    'X.X'),
        mocker.call('OO.\n'
                    'XO.\n'
                    'X.X'),
        mocker.call('OO.\n'
                    'XO.\n'
                    'XXX'),
        mocker.call('Game is finished, X wins'),
    ]
    assert handler.game is None


def test_o_wins(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 2 2')
    handler.handle_message('O 0 0')
    handler.handle_message('X 0 2')
    handler.handle_message('O 1 0')
    handler.handle_message('X 0 1')
    handler.handle_message('O 1 1')
    handler.handle_message('X 2 1')
    handler.handle_message('O 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('...\n'
                    '...\n'
                    '..X'),
        mocker.call('O..\n'
                    '...\n'
                    '..X'),
        mocker.call('O..\n'
                    '...\n'
                    'X.X'),
        mocker.call('OO.\n'
                    '...\n'
                    'X.X'),
        mocker.call('OO.\n'
                    'X..\n'
                    'X.X'),
        mocker.call('OO.\n'
                    'XO.\n'
                    'X.X'),
        mocker.call('OO.\n'
                    'XOX\n'
                    'X.X'),
        mocker.call('OO.\n'
                    'XOX\n'
                    'XOX'),
        mocker.call('Game is finished, O wins'),
    ]
    assert handler.game is None


def test_draw(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 1')
    handler.handle_message('O 1 1')
    handler.handle_message('X 0 2')
    handler.handle_message('O 0 0')
    handler.handle_message('X 2 2')
    handler.handle_message('O 1 2')
    handler.handle_message('X 2 1')
    handler.handle_message('O 2 0')
    handler.handle_message('X 1 0')
    assert send_message.call_args_list == [
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('...\n'
                    'X..\n'
                    '...'),
        mocker.call('...\n'
                    'XO.\n'
                    '...'),
        mocker.call('...\n'
                    'XO.\n'
                    'X..'),
        mocker.call('O..\n'
                    'XO.\n'
                    'X..'),
        mocker.call('O..\n'
                    'XO.\n'
                    'X.X'),
        mocker.call('O..\n'
                    'XO.\n'
                    'XOX'),
        mocker.call('O..\n'
                    'XOX\n'
                    'XOX'),
        mocker.call('O.O\n'
                    'XOX\n'
                    'XOX'),
        mocker.call('OXO\n'
                    'XOX\n'
                    'XOX'),
        mocker.call('Game is finished, draw'),
    ]
    assert handler.game is None


def test_incorrect_commands(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('Start')
    handler.handle_message('Krab')
    handler.handle_message('369')
    handler.handle_message('X 0 0')
    handler.handle_message('\n')
    handler.handle_message('X')
    handler.handle_message('Y')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started')
    ]
    assert handler.game is None


def test_invalid_turn(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 1 0')
    handler.handle_message('X 1 2')
    handler.handle_message('O 1 0')
    handler.handle_message('O 1 2')
    handler.handle_message('O 1 2')
    handler.handle_message('O 1 1')

    assert send_message.call_args_list == [
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('.X.\n'
                    '...\n'
                    '...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('.X.\n'
                    '...\n'
                    '.O.'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]
    assert handler.game is not None


def test_all_commands(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('Start')
    handler.handle_message('start')
    handler.handle_message('X 1 0')
    handler.handle_message('\n')
    handler.handle_message('start')
    handler.handle_message('start')
    handler.handle_message('X 0 1')
    handler.handle_message('O 1 1')
    handler.handle_message('X 0 2')
    handler.handle_message('O 0 0')
    handler.handle_message('X 2 2')
    handler.handle_message('O 1 2')
    handler.handle_message('X 2 1')
    handler.handle_message('O 2 0')
    handler.handle_message('X 1 0')
    handler.handle_message('X 0 0')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('.X.\n'
                    '...\n'
                    '...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('...\n'
                    'X..\n'
                    '...'),
        mocker.call('...\n'
                    'XO.\n'
                    '...'),
        mocker.call('...\n'
                    'XO.\n'
                    'X..'),
        mocker.call('O..\n'
                    'XO.\n'
                    'X..'),
        mocker.call('O..\n'
                    'XO.\n'
                    'X.X'),
        mocker.call('O..\n'
                    'XO.\n'
                    'XOX'),
        mocker.call('O..\n'
                    'XOX\n'
                    'XOX'),
        mocker.call('O.O\n'
                    'XOX\n'
                    'XOX'),
        mocker.call('OXO\n'
                    'XOX\n'
                    'XOX'),
        mocker.call('Game is finished, draw'),
        mocker.call('Game is not started')
    ]
    assert handler.game is None
