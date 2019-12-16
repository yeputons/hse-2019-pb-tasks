from pytest_mock import MockFixture
from tictactoe_user_handler import TicTacToeUserHandler


def test_start_game(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    handler.handle_message('maslo')
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 0 1')
    handler.handle_message('X 0 1')
    handler.handle_message('O 2 2')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\nO..\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
    ]


def test_invalid_turns(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 1 1')
    handler.handle_message('X 2 2')
    handler.handle_message('O 1 1')
    handler.handle_message('X 2 1')
    handler.handle_message('O 2 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n.O.\n..X'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n.OO\n..X'),
    ]


def test_x_wins(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 0 1')
    handler.handle_message('X 1 1')
    handler.handle_message('O 0 2')
    handler.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\nO..\n...'),
        mocker.call('X..\nOX.\n...'),
        mocker.call('X..\nOX.\nO..'),
        mocker.call('X..\nOX.\nO.X'),
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
    handler.handle_message('O 1 0')
    handler.handle_message('X 2 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 1 2')
    handler.handle_message('O 0 1')
    handler.handle_message('X 2 1')
    handler.handle_message('O 2 2')
    handler.handle_message('X 0 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XOX\n...\n...'),
        mocker.call('XOX\n.O.\n...'),
        mocker.call('XOX\n.O.\n.X.'),
        mocker.call('XOX\nOO.\n.X.'),
        mocker.call('XOX\nOOX\n.X.'),
        mocker.call('XOX\nOOX\n.XO'),
        mocker.call('XOX\nOOX\nXXO'),
        mocker.call('Game is finished, draw')
    ]
