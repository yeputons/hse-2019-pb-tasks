from typing import List
from pytest_mock import MockFixture
from tictactoe_user_handler import TicTacToeUserHandler


def handle_multiple_messages(handler: TicTacToeUserHandler, messages: List[str]) -> None:
    for message in messages:
        handler.handle_message(message=message)


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
