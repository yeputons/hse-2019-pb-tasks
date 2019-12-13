import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_chat_broadcast(mocker: pytest_mock.MockFixture) -> None:
    # Game is not started
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('X 1 1')
    assert mocker.call('Game is not started')


def test_chat_broadcast_1(mocker: pytest_mock.MockFixture) -> None:
    # Invalid turn: two moves in a row
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('X 1 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn')
    ]


def test_chat_broadcast_2(mocker: pytest_mock.MockFixture) -> None:
    # Invalid turn: two moves in a row
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn')
    ]


def test_chat_broadcast_3(mocker: pytest_mock.MockFixture) -> None:
    # Invalid turn: the first move must be X
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('O 1 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn')
    ]


def test_chat_broadcast_4(mocker: pytest_mock.MockFixture) -> None:
    # The right game: X win
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O.X\n.X.\n...'),
        mocker.call('OOX\n.X.\n...'),
        mocker.call('OOX\n.X.\nX..'),
        mocker.call('Game is finished, X wins')
    ]


def test_chat_broadcast_5(mocker: pytest_mock.MockFixture) -> None:
    # The right game: draw
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 0 2')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 2')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O.X\n.X.\n...'),
        mocker.call('O.X\n.X.\nO..'),
        mocker.call('O.X\nXX.\nO..'),
        mocker.call('O.X\nXXO\nO..'),
        mocker.call('OXX\nXXO\nO..'),
        mocker.call('OXX\nXXO\nOO.'),
        mocker.call('OXX\nXXO\nOOX'),
        mocker.call('Game is finished, draw')
    ]


def test_chat_broadcast_6(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 0')
    bot.handle_message('start')

    assert send_message.call_args_list == [
        # The beginning of the game when the game is unfinished
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O.X\n.X.\n...'),
        mocker.call('...\n...\n...')
    ]
