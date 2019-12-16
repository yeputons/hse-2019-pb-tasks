import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_tictactoe_user_hander_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\nX..\n...'),
        mocker.call('XO.\nXO.\n...'),
        mocker.call('XO.\nXO.\nX..'),
        mocker.call('Game is finished, X wins'),
    ]


def test_tictactoe_user_hander_o_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 2')
    bot.handle_message('O 2 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X..\nXO.\n...'),
        mocker.call('X..\nXO.\nO..'),
        mocker.call('X..\nXO.\nO.X'),
        mocker.call('X.O\nXO.\nO.X'),
        mocker.call('Game is finished, O wins')
    ]


def test_tictactoe_user_hander_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 2')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 1 2')
    bot.handle_message('X 2 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\nX..\n...'),
        mocker.call('...\nXO.\n...'),
        mocker.call('.X.\nXO.\n...'),
        mocker.call('OX.\nXO.\n...'),
        mocker.call('OX.\nXO.\n..X'),
        mocker.call('OXO\nXO.\n..X'),
        mocker.call('OXO\nXO.\nX.X'),
        mocker.call('OXO\nXO.\nXOX'),
        mocker.call('OXO\nXOX\nXOX'),
        mocker.call('Game is finished, draw')
    ]


def test_tictactoe_user_hander_correct_start(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('mew')
    bot.handle_message('mew!')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 2')
    bot.handle_message('O 2 0')
    bot.handle_message('O 2 0')
    bot.handle_message('X 2 2')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X..\nXO.\n...'),
        mocker.call('X..\nXO.\nO..'),
        mocker.call('X..\nXO.\nO.X'),
        mocker.call('X.O\nXO.\nO.X'),
        mocker.call('Game is finished, O wins'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...')
    ]


def test_tictactoe_user_hander_invalid_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\nX..\n...'),
        mocker.call('XO.\nXO.\n...'),
        mocker.call('Invalid turn'),
    ]
