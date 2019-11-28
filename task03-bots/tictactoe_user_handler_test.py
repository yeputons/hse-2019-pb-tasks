import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_chat_broadcast(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    # Game is not started
    bot.handle_message('X 1 1')
    # Invalid turn: two moves in a row
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('X 1 0')
    # Invalid turn: on one place
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 1')
    # Invalid turn: the first move must be X
    bot.handle_message('start')
    bot.handle_message('O 1 1')
    # The right game: X win
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 2')
    # The right game: draw
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
    # still move after the end of the game
    bot.handle_message('X 2 2')

    assert send_message.call_args_list == [
        # Game is not started
        mocker.call('Game is not started'),
        # Invalid turn: two moves in a row
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        # Invalid turn: on one place
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        # Invalid turn: the first move must be X
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        # The right game: X win
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O.X\n.X.\n...'),
        mocker.call('OOX\n.X.\n...'),
        mocker.call('OOX\n.X.\nX..'),
        mocker.call('Game is finished, X wins'),
        # The right game: draw
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
        mocker.call('Game is finished, draw'),
        # still move after the end of the game
        mocker.call('Game is not started')
    ]
