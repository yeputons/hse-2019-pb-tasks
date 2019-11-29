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
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('.X.'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('Invalid turn'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('.X.'),
        mocker.call('...'),
        mocker.call('.O.'),
        mocker.call('.X.'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...')
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
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('.X.'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('OX.'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('OX.'),
        mocker.call('..X'),
        mocker.call('O..'),
        mocker.call('OX.'),
        mocker.call('..X'),
        mocker.call('O..'),
        mocker.call('OX.'),
        mocker.call('X.X'),
        mocker.call('O..'),
        mocker.call('OX.'),
        mocker.call('XOX'),
        mocker.call('O.X'),
        mocker.call('OX.'),
        mocker.call('XOX'),
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
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('..X'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('..X'),
        mocker.call('.O.'),
        mocker.call('...'),
        mocker.call('X.X'),
        mocker.call('.O.'),
        mocker.call('...'),
        mocker.call('XOX'),
        mocker.call('.O.'),
        mocker.call('...'),
        mocker.call('XOX'),
        mocker.call('XO.'),
        mocker.call('...'),
        mocker.call('XOX'),
        mocker.call('XO.'),
        mocker.call('.O.'),
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
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('.X.'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('OX.'),
        mocker.call('...'),
        mocker.call('.X.'),
        mocker.call('OX.'),
        mocker.call('...'),
        mocker.call('.X.'),
        mocker.call('OX.'),
        mocker.call('.O.'),
        mocker.call('.X.'),
        mocker.call('OX.'),
        mocker.call('.OX'),
        mocker.call('OX.'),
        mocker.call('OX.'),
        mocker.call('.OX'),
        mocker.call('OX.'),
        mocker.call('OX.'),
        mocker.call('XOX'),
        mocker.call('OXO'),
        mocker.call('OX.'),
        mocker.call('XOX'),
        mocker.call('OXO'),
        mocker.call('OXX'),
        mocker.call('XOX'),
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
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('...'),
        mocker.call('.X.'),
        mocker.call('...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]
