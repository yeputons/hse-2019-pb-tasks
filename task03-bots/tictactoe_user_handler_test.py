import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_integrate_multistart(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)

    handler.handle_message('start')
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('start')
    handler.handle_message('O 1 1')
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 1 0')
    handler.handle_message('start')

    assert send_message.call_args_list == [
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('...\n'
                    '.X.\n'
                    '...'),
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('...\n'
                    '.X.\n'
                    '...'),
        mocker.call('.O.\n'
                    '.X.\n'
                    '...'),
        mocker.call('...\n'
                    '...\n'
                    '...')
    ]


def test_integrate_win_x(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)

    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 0 1')
    handler.handle_message('X 2 2')
    handler.handle_message('O 0 0')
    handler.handle_message('X 0 2')
    handler.handle_message('O 1 2')
    handler.handle_message('X 2 0')

    assert send_message.call_args_list == [
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('...\n'
                    '.X.\n'
                    '...'),
        mocker.call('...\n'
                    'OX.\n'
                    '...'),
        mocker.call('...\n'
                    'OX.\n'
                    '..X'),
        mocker.call('O..\n'
                    'OX.\n'
                    '..X'),
        mocker.call('O..\n'
                    'OX.\n'
                    'X.X'),
        mocker.call('O..\n'
                    'OX.\n'
                    'XOX'),
        mocker.call('O.X\n'
                    'OX.\n'
                    'XOX'),
        mocker.call('Game is finished, X wins')
    ]


def test_integrate_win_o(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)

    handler.handle_message('start')
    handler.handle_message('X 2 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 0')
    handler.handle_message('X 0 1')
    handler.handle_message('O 1 2')

    assert send_message.call_args_list == [
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('..X\n'
                    '...\n'
                    '...'),
        mocker.call('..X\n'
                    '.O.\n'
                    '...'),
        mocker.call('X.X\n'
                    '.O.\n'
                    '...'),
        mocker.call('XOX\n'
                    '.O.\n'
                    '...'),
        mocker.call('XOX\n'
                    'XO.\n'
                    '...'),
        mocker.call('XOX\n'
                    'XO.\n'
                    '.O.'),
        mocker.call('Game is finished, O wins')
    ]


def test_integrate_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)

    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 0 1')
    handler.handle_message('X 1 0')
    handler.handle_message('O 1 2')
    handler.handle_message('X 2 2')
    handler.handle_message('O 0 0')
    handler.handle_message('X 0 2')
    handler.handle_message('O 2 0')
    handler.handle_message('X 2 1')

    assert send_message.call_args_list == [
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('...\n'
                    '.X.\n'
                    '...'),
        mocker.call('...\n'
                    'OX.\n'
                    '...'),
        mocker.call('.X.\n'
                    'OX.\n'
                    '...'),
        mocker.call('.X.\n'
                    'OX.\n'
                    '.O.'),
        mocker.call('.X.\n'
                    'OX.\n'
                    '.OX'),
        mocker.call('OX.\n'
                    'OX.\n'
                    '.OX'),
        mocker.call('OX.\n'
                    'OX.\n'
                    'XOX'),
        mocker.call('OXO\n'
                    'OX.\n'
                    'XOX'),
        mocker.call('OXO\n'
                    'OXX\n'
                    'XOX'),
        mocker.call('Game is finished, draw')
    ]


def test_integrate_invalid_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)

    handler.handle_message('X 1 1')
    handler.handle_message('start')
    handler.handle_message('O 1 1')
    handler.handle_message('X 1 1 1')
    handler.handle_message('X 1')
    handler.handle_message('X')
    handler.handle_message('')
    handler.handle_message('Y 1 1')
    handler.handle_message('X a b')
    handler.handle_message('X 1 1')
    handler.handle_message('X 1 2')
    handler.handle_message('O 1 1')
    handler.handle_message('O 5 -1')
    handler.handle_message('Never gonna give you up'
                           'Never gonna let you down')

    print(send_message.call_args_list)

    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('...\n'
                    '.X.\n'
                    '...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]


def test_integrate_game_is_not_started(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)

    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 0 1')
    handler.handle_message('X 2 2')
    handler.handle_message('O 0 0')
    handler.handle_message('X 0 2')
    handler.handle_message('O 1 2')
    handler.handle_message('X 2 0')
    handler.handle_message('O 1 0')
    handler.handle_message('pls do smthing')
    handler.handle_message('pls do smthing 2')
    handler.handle_message('pls do smthing 3')
    handler.handle_message('start')

    assert send_message.call_args_list == [
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('...\n'
                    '.X.\n'
                    '...'),
        mocker.call('...\n'
                    'OX.\n'
                    '...'),
        mocker.call('...\n'
                    'OX.\n'
                    '..X'),
        mocker.call('O..\n'
                    'OX.\n'
                    '..X'),
        mocker.call('O..\n'
                    'OX.\n'
                    'X.X'),
        mocker.call('O..\n'
                    'OX.\n'
                    'XOX'),
        mocker.call('O.X\n'
                    'OX.\n'
                    'XOX'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n'
                    '...\n'
                    '...')
    ]


def test_integrate_ok_google(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)

    handler.handle_message('start')
    handler.handle_message('X 2 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 0')
    handler.handle_message('X 0 1')
    handler.handle_message('O 1 2')
    handler.handle_message('- Player.X: OK Google how to win tictactoe')
    handler.handle_message('- Google: Here is an algorithm <pic>')
    handler.handle_message('- Player.X: Thanks!')
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 0 1')
    handler.handle_message('X 2 2')
    handler.handle_message('O 0 0')
    handler.handle_message('X 0 2')
    handler.handle_message('O 1 2')
    handler.handle_message('X 2 0')
    handler.handle_message('- Player.X: EEEEEEEEEEEEEE!')

    assert send_message.call_args_list == [
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('..X\n'
                    '...\n'
                    '...'),
        mocker.call('..X\n'
                    '.O.\n'
                    '...'),
        mocker.call('X.X\n'
                    '.O.\n'
                    '...'),
        mocker.call('XOX\n'
                    '.O.\n'
                    '...'),
        mocker.call('XOX\n'
                    'XO.\n'
                    '...'),
        mocker.call('XOX\n'
                    'XO.\n'
                    '.O.'),
        mocker.call('Game is finished, O wins'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n'
                    '...\n'
                    '...'),
        mocker.call('...\n'
                    '.X.\n'
                    '...'),
        mocker.call('...\n'
                    'OX.\n'
                    '...'),
        mocker.call('...\n'
                    'OX.\n'
                    '..X'),
        mocker.call('O..\n'
                    'OX.\n'
                    '..X'),
        mocker.call('O..\n'
                    'OX.\n'
                    'X.X'),
        mocker.call('O..\n'
                    'OX.\n'
                    'XOX'),
        mocker.call('O.X\n'
                    'OX.\n'
                    'XOX'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started'),
    ]
