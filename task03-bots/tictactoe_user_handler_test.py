from typing import List
from pytest_mock import MockFixture
from tictactoe_user_handler import TicTacToeUserHandler


def handle_multiple_messages(handler: TicTacToeUserHandler, messages: List[str]) -> None:
    for message in messages:
        handler.handle_message(message=message)


def test_win_of_o(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handle_multiple_messages(handler, [
        'start', 'X 2 2', 'O 1 0', 'X 0 0', 'O 1 1', 'X 0 2', 'O 1 2'
    ])
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n..X'),
        mocker.call('.O.\n...\n..X'),
        mocker.call('XO.\n...\n..X'),
        mocker.call('XO.\n.O.\n..X'),
        mocker.call('XO.\n.O.\nX.X'),
        mocker.call('XO.\n.O.\nXOX'),
        mocker.call('Game is finished, O wins')
    ]


def test_draw(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handle_multiple_messages(handler, [
        'start', 'X 1 0', 'O 2 2', 'X 0 0', 'O 1 2', 'X 0 2', 'O 2 0',
        'X 2 1', 'O 0 1', 'X 1 1'
    ])
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('.X.\n...\n..O'),
        mocker.call('XX.\n...\n..O'),
        mocker.call('XX.\n...\n.OO'),
        mocker.call('XX.\n...\nXOO'),
        mocker.call('XXO\n...\nXOO'),
        mocker.call('XXO\n..X\nXOO'),
        mocker.call('XXO\nO.X\nXOO'),
        mocker.call('XXO\nOXX\nXOO'),
        mocker.call('Game is finished, draw')
    ]


def test_win_of_x(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handle_multiple_messages(handler, [
        'start', 'X 2 2', 'O 1 0', 'X 1 2', 'O 0 1', 'X 0 2'
    ])
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n..X'),
        mocker.call('.O.\n...\n..X'),
        mocker.call('.O.\n...\n.XX'),
        mocker.call('.O.\nO..\n.XX'),
        mocker.call('.O.\nO..\nXXX'),
        mocker.call('Game is finished, X wins')
    ]


def test_invalid_start(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handle_multiple_messages(handler, [
        'TEST1', 'TEST2'
        ])
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        ]


def test_invalid_turn(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message=send_message)
    handle_multiple_messages(handler, [
        'start', 'X 1 1', 'O 1 1'
        ])
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn')
    ]
