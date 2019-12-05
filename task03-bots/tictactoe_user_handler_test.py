from typing import List
from pytest_mock import MockFixture
from tictactoe_user_handler import TicTacToeUserHandler


def handle_multiple_messages(handler: TicTacToeUserHandler, messages: List[str]) -> None:
    for message in messages:
        handler.handle_message(message=message)


def test_game_not_started(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handle_multiple_messages(handler, [
        'X 0 0', 'X 0 1',
        'stop', 'start',
        'X 0 0'
    ])
    assert send_message.call_args_list == [
        mocker.call('Game not started'),
        mocker.call('Game not started'),
        mocker.call('Game not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...')
    ]


def test_multiple_start(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handle_multiple_messages(handler, [
        'start', 'X 0 0',
        'start', 'start'
    ])
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n...')
    ]


def test_invalid_turn(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handle_multiple_messages(handler, [
        'start', 'X 0 0',
        'O 0 0', 'O 2 3',
        'O -1 2', 'A 1 1'
    ])
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]


def test_x_wins_result(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handle_multiple_messages(handler, [
        'start',
        'X 0 0', 'O 1 0', 'X 2 0',
        'O 0 1', 'X 1 1', 'O 2 1',
        'X 0 2'
    ])
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
    handle_multiple_messages(handler, [
        'start',
        'X 2 2', 'O 0 0', 'X 2 0',
        'O 0 1', 'X 1 1', 'O 0 2'
    ])
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
    handle_multiple_messages(handler, [
        'start',
        'X 0 0', 'O 1 0', 'X 2 0',
        'O 1 1', 'X 0 1', 'O 2 1',
        'X 1 2', 'O 0 2', 'X 2 2'
    ])
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
