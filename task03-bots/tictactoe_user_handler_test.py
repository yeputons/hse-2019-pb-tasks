import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_no_start(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('hi')
    bot.handle_message('strt')
    bot.handle_message('bye')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started')]


def test_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 2')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\nX..\n...'),
        mocker.call('XOO\nX..\n...'),
        mocker.call('XOO\nX..\nX..'),
        mocker.call('Game is finished, X wins')]


def test_o_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 2')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('.X.\n.O.\n...'),
        mocker.call('XX.\n.O.\n...'),
        mocker.call('XXO\n.O.\n...'),
        mocker.call('XXO\nXO.\n...'),
        mocker.call('XXO\nXO.\nO..'),
        mocker.call('Game is finished, O wins')]


def test_start_in_process(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 0')
    bot.handle_message('start')
    bot.handle_message('X 0 0')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('.X.\n.O.\n...'),
        mocker.call('XX.\n.O.\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...')]


def test_invalid_turns(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 1')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('.X.\n.O.\n...'),
        mocker.call('Invalid turn')]
