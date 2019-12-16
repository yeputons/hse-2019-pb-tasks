from pytest_mock import MockFixture
from tictactoe_user_handler import TicTacToeUserHandler


def test_game_start(mocker: MockFixture) -> None:
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


def test_multiple_starts(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('hi')
    handler.handle_message('bye((')
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('start')
    handler.handle_message('X 2 2')
    handler.handle_message('start')
    handler.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n..X'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n...')

    ]


def test_invalid_turn_o(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 1 2')
    handler.handle_message('O 1 2')
    handler.handle_message('O 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n.X.'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]


def test_invalid_turn_x(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 1 2')
    handler.handle_message('O 1 1')
    handler.handle_message('X 1 1')
    handler.handle_message('X 1 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n.X.'),
        mocker.call('...\n.O.\n.X.'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]


def test_invalid_turn_not_your_turn_x(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 1 2')
    handler.handle_message('X 1 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n.X.'),
        mocker.call('Invalid turn')
    ]


def test_invalid_turn_not_your_turn_o(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('O 1 1')
    handler.handle_message('X 1 1')
    handler.handle_message('O 0 0')
    handler.handle_message('O 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('Invalid turn')
    ]


def test_x_wins(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 0 0')
    handler.handle_message('X 2 1')
    handler.handle_message('O 1 0')
    handler.handle_message('X 0 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.XX\n...'),
        mocker.call('OO.\n.XX\n...'),
        mocker.call('OO.\nXXX\n...'),
        mocker.call('Game is finished, X wins')
    ]


def test_o_wins(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 1 0')
    handler.handle_message('O 2 0')
    handler.handle_message('X 0 1')
    handler.handle_message('O 0 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('XX.\n.O.\n...'),
        mocker.call('XXO\n.O.\n...'),
        mocker.call('XXO\nXO.\n...'),
        mocker.call('XXO\nXO.\nO..'),
        mocker.call('Game is finished, O wins')
    ]


def test_draw(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 2 2')
    handler.handle_message('O 0 2')
    handler.handle_message('X 2 0')
    handler.handle_message('O 1 0')
    handler.handle_message('X 1 2')
    handler.handle_message('O 2 1')
    handler.handle_message('X 0 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X..\n.O.\n..X'),
        mocker.call('X..\n.O.\nO.X'),
        mocker.call('X.X\n.O.\nO.X'),
        mocker.call('XOX\n.O.\nO.X'),
        mocker.call('XOX\n.O.\nOXX'),
        mocker.call('XOX\n.OO\nOXX'),
        mocker.call('XOX\nXOO\nOXX'),
        mocker.call('Game is finished, draw')
    ]


def test_game_restart(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 1 1')
    handler.handle_message('O 0 0')
    handler.handle_message('X 2 1')
    handler.handle_message('O 1 0')
    handler.handle_message('X 0 1')
    handler.handle_message('O 2 2')
    handler.handle_message('((((')
    handler.handle_message('aaaaaaaa')
    handler.handle_message('X 1 1')
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 1')
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 1 0')
    handler.handle_message('O 2 0')
    handler.handle_message('X 0 1')
    handler.handle_message('O 0 2')
    handler.handle_message('X 1 1')
    handler.handle_message('ok')
    handler.handle_message('start')
    handler.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.XX\n...'),
        mocker.call('OO.\n.XX\n...'),
        mocker.call('OO.\nXXX\n...'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('XX.\n.O.\n...'),
        mocker.call('XXO\n.O.\n...'),
        mocker.call('XXO\nXO.\n...'),
        mocker.call('XXO\nXO.\nO..'),
        mocker.call('Game is finished, O wins'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n...')
    ]
