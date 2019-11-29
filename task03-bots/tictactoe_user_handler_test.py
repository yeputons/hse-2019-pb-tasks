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
        mocker.call('\n...\n...\n...\n'),
        mocker.call('\nX..\n...\n...\n'),
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
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 2 0')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('\n...\n...\n...\n'),
        mocker.call('\nX..\n...\n...\n'),
        mocker.call('\nXO.\n...\n...\n'),
        mocker.call('\nXO.\nX..\n...\n'),
        mocker.call('\nXO.\nXO.\n...\n'),
        mocker.call('\nXO.\nXO.\nX..\n'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started')]


def test_o_win(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 2 0')
    assert send_message.call_args_list == [
        mocker.call('\n...\n...\n...\n'),
        mocker.call('\n.X.\n...\n...\n'),
        mocker.call('\nOX.\n...\n...\n'),
        mocker.call('\nOX.\n.X.\n...\n'),
        mocker.call('\nOX.\nOX.\n...\n'),
        mocker.call('\nOXX\nOX.\n...\n'),
        mocker.call('\nOXX\nOX.\nO..\n'),
        mocker.call('Game is finished, O wins')]


def test_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 2 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 1 2')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('\n...\n...\n...\n'),
        mocker.call('\nX..\n...\n...\n'),
        mocker.call('\nXO.\n...\n...\n'),
        mocker.call('\nXO.\nX..\n...\n'),
        mocker.call('\nXO.\nXO.\n...\n'),
        mocker.call('\nXO.\nXO.\n.X.\n'),
        mocker.call('\nXO.\nXO.\nOX.\n'),
        mocker.call('\nXOX\nXO.\nOX.\n'),
        mocker.call('\nXOX\nXOO\nOX.\n'),
        mocker.call('\nXOX\nXOO\nOXX\n'),
        mocker.call('Game is finished, draw')]
