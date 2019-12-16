import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_start_game_false(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    TicTacToeUserHandler(send_message).handle_message('hi')
    assert send_message.call_args_list == [mocker.call('Game is not started')]


def test_start_game_turn_before(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    TicTacToeUserHandler(send_message).handle_message('X 1 0')
    assert send_message.call_args_list == [mocker.call('Game is not started')]


def test_start_game_true(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    TicTacToeUserHandler(send_message).handle_message('start')
    assert send_message.call_args_list == [mocker.call('...\n...\n...')]


def test_multiple_operations_multiple_starts(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n...')]


def test_multiple_operations(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('X 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn')]


def test_multiple_operations_o_starts(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n...\n.X.')]


def test_multiple_operations_o_multiple_starts(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('O 1 1')
    bot.handle_message('O 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')]


def test_multiple_operations_invalid_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('X 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn')]


def test_multiple_operations_exception(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('I will win!')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...')]


def test_multiple_operations_right_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\n.O.')]


def test_multiple_operations_new_game(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 2')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 2')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\n.O.'),
        mocker.call('...\n.X.\n.OX'),
        mocker.call('...\n.X.\nOOX'),
        mocker.call('...\n...\n...')]


def test_multiple_operations_winner_x_game(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 2')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 2')
    bot.handle_message('X 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\n.O.'),
        mocker.call('...\n.X.\n.OX'),
        mocker.call('...\n.X.\nOOX'),
        mocker.call('X..\n.X.\nOOX'),
        mocker.call('Game is finished, X wins')]


def test_multiple_operations_winner_o_game(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 2')
    bot.handle_message('X 1 0')
    bot.handle_message('O 0 2')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\n.O.'),
        mocker.call('.X.\n.X.\n.O.'),
        mocker.call('.X.\n.X.\nOO.'),
        mocker.call('XX.\n.X.\nOO.'),
        mocker.call('XX.\n.X.\nOOO'),
        mocker.call('Game is finished, O wins')]


def test_multiple_operations_draw_game(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 2')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 2')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 0')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\n.O.'),
        mocker.call('...\n.X.\n.OX'),
        mocker.call('...\n.X.\nOOX'),
        mocker.call('...\nXX.\nOOX'),
        mocker.call('O..\nXX.\nOOX'),
        mocker.call('OX.\nXX.\nOOX'),
        mocker.call('OX.\nXXO\nOOX'),
        mocker.call('OXX\nXXO\nOOX'),
        mocker.call('Game is finished, draw')]
