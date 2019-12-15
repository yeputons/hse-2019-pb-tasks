from typing import List
from pytest_mock import MockFixture
from tictactoe_user_handler import TicTacToeUserHandler


def handle_multiple_messages(handler: TicTacToeUserHandler, messages: List[str]) -> None:
    for message in messages:
        handler.handle_message(message=message)


def test_start(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handle_multiple_messages(handler, [
        'abc', 'Start', 'X 42 17', 'START', 'X 2 2', 'start', 'X 1 1', 'start', 'start'
    ])
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n...')
    ]


def test_invalid_turn(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handle_multiple_messages(handler, [
        'X 0 0', 'start', 'X 1 1', 'O 1 1', 'O 2 2', 'S 0 0', 'O 2 2'
    ])
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n.X.\n..O'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]


def test_play_x(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handle_multiple_messages(handler, [
        'start', 'X 0 0', 'O 1 0', 'X 2 2', 'O 0 1', 'X 1 1',
    ])
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\n...\n..X'),
        mocker.call('XO.\nO..\n..X'),
        mocker.call('XO.\nOX.\n..X'),
        mocker.call('Game is finished, X wins')
    ]


def test_play_o(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handle_multiple_messages(handler, [
        'start', 'X 2 0', 'O 0 1', 'X 2 2', 'O 0 0', 'X 1 1', 'O 0 2'
    ])
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('..X\n...\n...'),
        mocker.call('..X\nO..\n...'),
        mocker.call('..X\nO..\n..X'),
        mocker.call('O.X\nO..\n..X'),
        mocker.call('O.X\nOX.\n..X'),
        mocker.call('O.X\nOX.\nO.X'),
        mocker.call('Game is finished, O wins')
    ]


def test_play_draw(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handle_multiple_messages(handler, [
        'start', 'X 1 1', 'O 0 0', 'X 2 2', 'O 1 2', 'X 0 1', 'O 2 1', 'X 1 0', 'O 2 0', 'X 0 2'
    ])
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.X.\n..X'),
        mocker.call('O..\n.X.\n.OX'),
        mocker.call('O..\nXX.\n.OX'),
        mocker.call('O..\nXXO\n.OX'),
        mocker.call('OX.\nXXO\n.OX'),
        mocker.call('OXO\nXXO\n.OX'),
        mocker.call('OXO\nXXO\nXOX'),
        mocker.call('Game is finished, draw')
    ]
