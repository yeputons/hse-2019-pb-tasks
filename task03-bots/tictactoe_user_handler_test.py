import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_integrate_correct_requests_crosses_wins(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 1 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 2 0')
    handler.handle_message('O 0 0')
    handler.handle_message('X 2 2')
    handler.handle_message('O 0 1')
    handler.handle_message('X 2 1')
    handler.handle_message('hi')
    assert send_message.call_args_list == [
        mocker.call('...\n'
                    '...\n'
                    '...\n'),
        mocker.call('...\n'
                    'X..\n'
                    '...\n'),
        mocker.call('...\n'
                    'XO.\n'
                    '...\n'),
        mocker.call('...\n'
                    'XO.\n'
                    'X..\n'),
        mocker.call('O..\n'
                    'XO.\n'
                    'X..\n'),
        mocker.call('O..\n'
                    'XO.\n'
                    'X.X\n'),
        mocker.call('OO.\n'
                    'XO.\n'
                    'X.X\n'),
        mocker.call('OO.\n'
                    'XO.\n'
                    'XXX\n'),
        mocker.call('Game is finished, X wins\n'),
        mocker.call('Game is not started\n')
    ]
    assert handler.game is None


def test_integrate_correct_requests_noughts_wins(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 1 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 2 0')
    handler.handle_message('O 0 0')
    handler.handle_message('X 2 2')
    handler.handle_message('O 2 1')
    handler.handle_message('X 1 2')
    handler.handle_message('O 0 1')
    handler.handle_message('sart')
    assert send_message.call_args_list == [
        mocker.call('...\n'
                    '...\n'
                    '...\n'),
        mocker.call('...\n'
                    'X..\n'
                    '...\n'),
        mocker.call('...\n'
                    'XO.\n'
                    '...\n'),
        mocker.call('...\n'
                    'XO.\n'
                    'X..\n'),
        mocker.call('O..\n'
                    'XO.\n'
                    'X..\n'),
        mocker.call('O..\n'
                    'XO.\n'
                    'X.X\n'),
        mocker.call('O..\n'
                    'XO.\n'
                    'XOX\n'),
        mocker.call('O..\n'
                    'XOX\n'
                    'XOX\n'),
        mocker.call('OO.\n'
                    'XOX\n'
                    'XOX\n'),
        mocker.call('Game is finished, O wins\n'),
        mocker.call('Game is not started\n')
    ]
    assert handler.game is None


def test_integrate_correct_requests_draw(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 1 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 2 0')
    handler.handle_message('O 0 0')
    handler.handle_message('X 2 2')
    handler.handle_message('O 2 1')
    handler.handle_message('X 1 2')
    handler.handle_message('O 0 2')
    handler.handle_message('X 0 1')
    handler.handle_message('X 0 1')
    assert send_message.call_args_list == [
        mocker.call('...\n'
                    '...\n'
                    '...\n'),
        mocker.call('...\n'
                    'X..\n'
                    '...\n'),
        mocker.call('...\n'
                    'XO.\n'
                    '...\n'),
        mocker.call('...\n'
                    'XO.\n'
                    'X..\n'),
        mocker.call('O..\n'
                    'XO.\n'
                    'X..\n'),
        mocker.call('O..\n'
                    'XO.\n'
                    'X.X\n'),
        mocker.call('O..\n'
                    'XO.\n'
                    'XOX\n'),
        mocker.call('O..\n'
                    'XOX\n'
                    'XOX\n'),
        mocker.call('O.O\n'
                    'XOX\n'
                    'XOX\n'),
        mocker.call('OXO\n'
                    'XOX\n'
                    'XOX\n'),
        mocker.call('Game is finished, draw\n'),
        mocker.call('Game is not started\n')
    ]
    assert handler.game is None


def test_integrate_incorrect_requests(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('Start')
    handler.handle_message('X 0 1')
    handler.handle_message('\n')
    handler.handle_message('S')
    handler.handle_message('123')
    assert send_message.call_args_list == [
        mocker.call('Game is not started\n'),
        mocker.call('Game is not started\n'),
        mocker.call('Game is not started\n'),
        mocker.call('Game is not started\n'),
        mocker.call('Game is not started\n')
    ]
    assert handler.game is None


def test_integrate_invalid_turn(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 1')
    handler.handle_message('X 2 1')
    handler.handle_message('O 0 1')
    handler.handle_message('O 2 1')
    handler.handle_message('O 2 1')
    handler.handle_message('O 1 1')

    assert send_message.call_args_list == [
        mocker.call('...\n'
                    '...\n'
                    '...\n'),
        mocker.call('.X.\n'
                    '...\n'
                    '...\n'),
        mocker.call('Invalid turn\n'),
        mocker.call('Invalid turn\n'),
        mocker.call('.X.\n'
                    '...\n'
                    '.O.\n'),
        mocker.call('Invalid turn\n'),
        mocker.call('Invalid turn\n')
    ]
    assert handler.game is not None


def test_integrate_multiple_start(mocker: pytest_mock.MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('Start')
    handler.handle_message('start')
    handler.handle_message('X 0 1')
    handler.handle_message('\n')
    handler.handle_message('start')
    handler.handle_message('start')
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 0 1')
    handler.handle_message('X 0 2')
    handler.handle_message('O 1 0')
    handler.handle_message('X 1 1')
    handler.handle_message('O 1 2')
    handler.handle_message('X 2 1')
    handler.handle_message('O 2 0')
    handler.handle_message('X 2 2')
    handler.handle_message('X 0 1')
    assert send_message.call_args_list == [
        mocker.call('Game is not started\n'),
        mocker.call('...\n'
                    '...\n'
                    '...\n'),
        mocker.call('.X.\n'
                    '...\n'
                    '...\n'),
        mocker.call('Invalid turn\n'),
        mocker.call('...\n'
                    '...\n'
                    '...\n'),
        mocker.call('...\n'
                    '...\n'
                    '...\n'),
        mocker.call('...\n'
                    '...\n'
                    '...\n'),
        mocker.call('X..\n'
                    '...\n'
                    '...\n'),
        mocker.call('XO.\n'
                    '...\n'
                    '...\n'),
        mocker.call('XOX\n'
                    '...\n'
                    '...\n'),
        mocker.call('XOX\n'
                    'O..\n'
                    '...\n'),
        mocker.call('XOX\n'
                    'OX.\n'
                    '...\n'),
        mocker.call('XOX\n'
                    'OXO\n'
                    '...\n'),
        mocker.call('XOX\n'
                    'OXO\n'
                    '.X.\n'),
        mocker.call('XOX\n'
                    'OXO\n'
                    'OX.\n'),
        mocker.call('XOX\n'
                    'OXO\n'
                    'OXX\n'),
        mocker.call('Game is finished, X wins\n'),
        mocker.call('Game is not started\n')
    ]
    assert handler.game is None
