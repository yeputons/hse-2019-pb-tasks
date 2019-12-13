from typing import List
import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def send_messages(bot: TicTacToeUserHandler, messages: List[str]) -> None:
    for message in messages:
        bot.handle_message(message)


def create_list_of_calls(mocker: pytest_mock.MockFixture, calls: List[str]) -> List:
    return list(map(mocker.call, calls))


def test_game_not_started(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    send_messages(bot, ['sta', 'HELLO!!!!', 'X 1 1'])
    assert send_message.call_args_list == [mocker.call('Game is not started')] * 3


def test_many_starts(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    send_messages(bot, ['start'] * 4)
    assert send_message.call_args_list == [mocker.call('...\n...\n...')] * 4


def test_many_invalid_turns(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    send_messages(bot, [
        'start', 'O 0 0', 'X 1 1', 'X 1 1', 'O 1 1',
        'O 0 1', 'X 0 0', 'X 2 2', 'O 0 0'
    ])
    assert send_message.call_args_list == create_list_of_calls(mocker, [
        '...\n...\n...', 'Invalid turn', '...\n.X.\n...',
        'Invalid turn', 'Invalid turn', '...\nOX.\n...',
        'X..\nOX.\n...', 'Invalid turn', 'Invalid turn'
    ])


def test_x_wins_result(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    send_messages(bot, [
        'start', 'X 0 0', 'O 0 1',
        'X 1 0', 'O 1 1', 'X 2 0'
    ])
    assert send_message.call_args_list == create_list_of_calls(mocker, [
        '...\n...\n...', 'X..\n...\n...', 'X..\nO..\n...',
        'XX.\nO..\n...', 'XX.\nOO.\n...', 'XXX\nOO.\n...',
        'Game is finished, X wins'
    ])


def test_o_wins_result(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    send_messages(bot, [
        'start', 'X 0 0', 'O 0 1',
        'X 2 2', 'O 1 1', 'X 2 0',
        'O 2 1'
    ])
    assert send_message.call_args_list == create_list_of_calls(mocker, [
        '...\n...\n...', 'X..\n...\n...', 'X..\nO..\n...',
        'X..\nO..\n..X', 'X..\nOO.\n..X', 'X.X\nOO.\n..X',
        'X.X\nOOO\n..X', 'Game is finished, O wins'
    ])


def test_draw_result(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    send_messages(bot, [
        'start', 'X 0 0', 'O 1 0',
        'X 2 0', 'O 1 1', 'X 0 1',
        'O 0 2', 'X 2 1', 'O 2 2',
        'X 1 2'
    ])
    assert send_message.call_args_list == create_list_of_calls(mocker, [
        '...\n...\n...', 'X..\n...\n...', 'XO.\n...\n...',
        'XOX\n...\n...', 'XOX\n.O.\n...', 'XOX\nXO.\n...',
        'XOX\nXO.\nO..', 'XOX\nXOX\nO..', 'XOX\nXOX\nO.O',
        'XOX\nXOX\nOXO', 'Game is finished, draw'
    ])


def test_check_starts_in_the_middle(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    send_messages(bot, [
        'start', 'X 0 0', 'start',
        'X 0 0', 'O 1 1', 'X 1 0',
        'start', 'start', 'O 2 2',
    ])
    assert send_message.call_args_list == create_list_of_calls(mocker, [
        '...\n...\n...', 'X..\n...\n...', '...\n...\n...',
        'X..\n...\n...', 'X..\n.O.\n...', 'XX.\n.O.\n...',
        '...\n...\n...', '...\n...\n...', 'Invalid turn',
    ])


def test_wrong_symbols(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    send_messages(bot, [
        'start', 'X 1 1', 'Z 0 0',
        'O 0 0', 'Q 2 1'
    ])
    assert send_message.call_args_list == create_list_of_calls(mocker, [
        '...\n...\n...', '...\n.X.\n...', 'Invalid turn',
        'O..\n.X.\n...', 'Invalid turn'
    ])
