from typing import List
import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def handle_all_messages(handler: TicTacToeUserHandler,
                        messages: List[str]) -> None:
    for message in messages:
        handler.handle_message(message=message)


def test_handle_message(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message')
    handler = TicTacToeUserHandler(send_message)
    messages = [
        'asdfasdfas asdf asd fas df',
        'start',
        'start',
        'X 0 0',
        'X 0 0',
        'O 2 2',
        'O 2 1',
        'start',
        'O 2 1'
    ]
    handle_all_messages(handler, messages)
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n...\n..O'),
        mocker.call('Invalid turn'),
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn')
    ]


def test_start_game(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message')
    handler = TicTacToeUserHandler(send_message)
    handler.start_game()
    assert send_message.call_args_list == [mocker.call('...\n...\n...')]


def test_make_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message')
    handler = TicTacToeUserHandler(send_message)
    messages = [
        'start',
        'X 0 0',
        'X 0 0',
        'O 0 0',
        'O 0 1',
        'X 0 1',
        'X 0 2'
    ]
    handle_all_messages(handler, messages)
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('XO.\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('XOX\n...\n...'),
    ]


def test_send_field(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message')
    handler = TicTacToeUserHandler(send_message)
    messages = [
        'start',
        'X 1 1',
        'O 0 0',
        'X 0 2',
        'O 2 0',
        'X 1 0',
        'O 1 2',
        'X 2 1',
        'O 0 1'
    ]
    handle_all_messages(handler, messages)
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O.X\n.X.\n...'),
        mocker.call('O.X\n.X.\nO..'),
        mocker.call('O.X\nXX.\nO..'),
        mocker.call('O.X\nXXO\nO..'),
        mocker.call('O.X\nXXO\nOX.'),
        mocker.call('OOX\nXXO\nOX.')
    ]


def test_win_x(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message')
    handler = TicTacToeUserHandler(send_message)
    messages = [
        'start',
        'X 0 0',
        'O 0 1',
        'X 1 1',
        'O 0 2',
        'X 2 2'
    ]
    handle_all_messages(handler, messages)
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\n.X.\n...'),
        mocker.call('XOO\n.X.\n...'),
        mocker.call('XOO\n.X.\n..X'),
        mocker.call('Game is finished, X wins')
    ]


def test_win_o(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message')
    handler = TicTacToeUserHandler(send_message)
    messages = [
        'start',
        'X 2 0',
        'O 0 0',
        'X 2 1',
        'O 0 1',
        'X 1 1',
        'O 0 2'
    ]
    handle_all_messages(handler, messages)
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\nX..'),
        mocker.call('O..\n...\nX..'),
        mocker.call('O..\n...\nXX.'),
        mocker.call('OO.\n...\nXX.'),
        mocker.call('OO.\n.X.\nXX.'),
        mocker.call('OOO\n.X.\nXX.'),
        mocker.call('Game is finished, O wins')
    ]


def test_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message')
    handler = TicTacToeUserHandler(send_message)
    messages = [
        'start',
        'X 1 1',
        'O 0 0',
        'X 0 2',
        'O 2 0',
        'X 1 0',
        'O 1 2',
        'X 2 1',
        'O 0 1',
        'X 2 2'
    ]
    handle_all_messages(handler, messages)
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O.X\n.X.\n...'),
        mocker.call('O.X\n.X.\nO..'),
        mocker.call('O.X\nXX.\nO..'),
        mocker.call('O.X\nXXO\nO..'),
        mocker.call('O.X\nXXO\nOX.'),
        mocker.call('OOX\nXXO\nOX.'),
        mocker.call('OOX\nXXO\nOXX'),
        mocker.call('Game is finished, draw')
    ]
