import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_invalid_turn(mocker) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')]


def test_game_not_started(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('BUCKWHEAT ONELOVE')
    assert send_message.call_args_list == [
        mocker.call('Game is not started')]


def test_x_win(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 2')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\nX..\n...'),
        mocker.call('XO.\nXO.\n...'),
        mocker.call('XO.\nXO.\nX..'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started')]


def test_o_win(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 0')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 1')
    bot.handle_message('X 2 0')
    bot.handle_message('O 0 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('OX.\n...\n...'),
        mocker.call('OX.\n.X.\n...'),
        mocker.call('OX.\nOX.\n...'),
        mocker.call('OXX\nOX.\n...'),
        mocker.call('OXX\nOX.\nO..'),
        mocker.call('Game is finished, O wins')]


def test_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 2')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 0')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\nX..\n...'),
        mocker.call('XO.\nXO.\n...'),
        mocker.call('XO.\nXO.\n.X.'),
        mocker.call('XO.\nXO.\nOX.'),
        mocker.call('XOX\nXO.\nOX.'),
        mocker.call('XOX\nXOO\nOX.'),
        mocker.call('XOX\nXOO\nOXX'),
        mocker.call('Game is finished, draw')]
