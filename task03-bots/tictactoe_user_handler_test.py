import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_no_start(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('Misha gay')
    bot.handle_message('MISHA GAY')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started')]


def test_x_win(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 0')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('OX.\n...\n...'),
        mocker.call('OX.\n.X.\n...'),
        mocker.call('OX.\nOX.\n...'),
        mocker.call('OX.\nOX.\n.X.'),
        mocker.call('Game is finished, X wins')]


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
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 2 1')
    bot.handle_message('O 1 2')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('.X.\n.O.\n...'),
        mocker.call('XX.\n.O.\n...'),
        mocker.call('XXO\n.O.\n...'),
        mocker.call('XXO\n.O.\nX..'),
        mocker.call('XXO\nOO.\nX..'),
        mocker.call('XXO\nOOX\nX..'),
        mocker.call('XXO\nOOX\nXO.'),
        mocker.call('XXO\nOOX\nXOX'),
        mocker.call('Game is finished, draw')]
