import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_chat_broadcast(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    # Start game
    bot.handle_message('O 2 1')
    bot.handle_message('Hello')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('O 2 2')
    # X wins
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 2')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 2')
    bot.handle_message('X 0 2')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 1')
    # O wins
    bot.handle_message('start')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 2')
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 2')
    bot.handle_message('X 1 2')
    bot.handle_message('O 2 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 1')
    # Draw
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 2 1')
    bot.handle_message('O 1 2')
    bot.handle_message('X 2 2')

    assert send_message.call_args_list == [
        # Start game
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...\n'),
        mocker.call('X..\n...\n...\n'),
        mocker.call('X..\n.O.\n...\n'),
        mocker.call('Invalid turn'),
        # X wins
        mocker.call('...\n...\n...\n'),
        mocker.call('...\n.X.\n...\n'),
        mocker.call('...\n.X.\n.O.\n'),
        mocker.call('X..\n.X.\n.O.\n'),
        mocker.call('X..\n.X.\n.OO\n'),
        mocker.call('X..\n.X.\nXOO\n'),
        mocker.call('X.O\n.X.\nXOO\n'),
        mocker.call('X.O\nXX.\nXOO\n'),
        mocker.call('Game is finished, X wins'),
        # O wins
        mocker.call('...\n...\n...\n'),
        mocker.call('...\nX..\n...\n'),
        mocker.call('...\nX..\n..O\n'),
        mocker.call('X..\nX..\n..O\n'),
        mocker.call('X..\nX..\nO.O\n'),
        mocker.call('X..\nX..\nOXO\n'),
        mocker.call('X.O\nX..\nOXO\n'),
        mocker.call('X.O\nXX.\nOXO\n'),
        mocker.call('X.O\nXXO\nOXO\n'),
        mocker.call('Game is finished, O wins'),
        # Draw
        mocker.call('...\n...\n...\n'),
        mocker.call('X..\n...\n...\n'),
        mocker.call('X..\n.O.\n...\n'),
        mocker.call('XX.\n.O.\n...\n'),
        mocker.call('XXO\n.O.\n...\n'),
        mocker.call('XXO\n.O.\nX..\n'),
        mocker.call('XXO\nOO.\nX..\n'),
        mocker.call('XXO\nOOX\nX..\n'),
        mocker.call('XXO\nOOX\nXO.\n'),
        mocker.call('XXO\nOOX\nXOX\n'),
        mocker.call('Game is finished, draw')
    ]
