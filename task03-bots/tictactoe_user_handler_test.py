import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_tictactoe_friendship_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.handle_message('fdg')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 2')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 2')
    bot.handle_message('X 1 2')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 0')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X..\nO..\n...'),
        mocker.call('XX.\nO..\n...'),
        mocker.call('XXO\nO..\n...'),
        mocker.call('XXO\nOX.\n...'),
        mocker.call('XXO\nOX.\n..O'),
        mocker.call('XXO\nOXX\n..O'),
        mocker.call('XXO\nOXX\n.OO'),
        mocker.call('XXO\nOXX\nXOO'),
        mocker.call('Game is finished, draw'),
    ]


def test_tictactoe_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\nO..\n...'),
        mocker.call('X..\nOX.\n...'),
        mocker.call('X..\nOX.\n.O.'),
        mocker.call('X..\nOX.\n.OX'),
        mocker.call('Game is finished, X wins'),
    ]


def test_tictactoe_o_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message=send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 2')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 2 1')
    bot.handle_message('O 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('..X\n...\n...'),
        mocker.call('O.X\n...\n...'),
        mocker.call('O.X\nX..\n...'),
        mocker.call('O.X\nXO.\n...'),
        mocker.call('O.X\nXO.\n.X.'),
        mocker.call('O.X\nXO.\n.XO'),
        mocker.call('Game is finished, O wins'),
    ]
