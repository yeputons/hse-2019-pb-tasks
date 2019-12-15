from pytest_mock import MockFixture
from tictactoe_user_handler import TicTacToeUserHandler


def test_game_not_started(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('X 0 0')
    handler.handle_message('X 0 1')
    handler.handle_message('stop')
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...')
    ]


def test_multiple_start(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('start')
    handler.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n...')
    ]


def test_invalid_turn_this_tile_is_occupied(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn')
    ]


def test_invalid_turn_another_player_turn(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('O 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn')
    ]


def test_x_wins_result(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 0')
    handler.handle_message('X 2 0')
    handler.handle_message('O 0 1')
    handler.handle_message('X 1 1')
    handler.handle_message('O 2 1')
    handler.handle_message('X 0 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XOX\n...\n...'),
        mocker.call('XOX\nO..\n...'),
        mocker.call('XOX\nOX.\n...'),
        mocker.call('XOX\nOXO\n...'),
        mocker.call('XOX\nOXO\nX..'),
        mocker.call('Game is finished, X wins')
    ]


def test_o_wins_result(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 2 2')
    handler.handle_message('O 0 0')
    handler.handle_message('X 2 0')
    handler.handle_message('O 0 1')
    handler.handle_message('X 1 1')
    handler.handle_message('O 0 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n..X'),
        mocker.call('O..\n...\n..X'),
        mocker.call('O.X\n...\n..X'),
        mocker.call('O.X\nO..\n..X'),
        mocker.call('O.X\nOX.\n..X'),
        mocker.call('O.X\nOX.\nO.X'),
        mocker.call('Game is finished, O wins')
    ]


def test_draw_result(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 0')
    handler.handle_message('X 2 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 0 1')
    handler.handle_message('O 2 1')
    handler.handle_message('X 1 2')
    handler.handle_message('O 0 2')
    handler.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XOX\n...\n...'),
        mocker.call('XOX\n.O.\n...'),
        mocker.call('XOX\nXO.\n...'),
        mocker.call('XOX\nXOO\n...'),
        mocker.call('XOX\nXOO\n.X.'),
        mocker.call('XOX\nXOO\nOX.'),
        mocker.call('XOX\nXOO\nOXX'),
        mocker.call('Game is finished, draw')
    ]


def test_game_restart_after_finish(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 0')
    handler.handle_message('X 2 0')
    handler.handle_message('O 1 1')
    handler.handle_message('X 0 1')
    handler.handle_message('O 2 1')
    handler.handle_message('X 1 2')
    handler.handle_message('O 0 2')
    handler.handle_message('X 2 2')
    handler.handle_message('start')
    handler.handle_message('X 0 0')
    handler.handle_message('O 1 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XOX\n...\n...'),
        mocker.call('XOX\n.O.\n...'),
        mocker.call('XOX\nXO.\n...'),
        mocker.call('XOX\nXOO\n...'),
        mocker.call('XOX\nXOO\n.X.'),
        mocker.call('XOX\nXOO\nOX.'),
        mocker.call('XOX\nXOO\nOXX'),
        mocker.call('Game is finished, draw'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...')
    ]
