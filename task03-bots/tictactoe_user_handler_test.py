from pytest_mock import MockFixture
from tictactoe_user_handler import TicTacToeUserHandler


def test_no_start(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('GGWP')
    bot.handle_message('Start')
    bot.handle_message('O 13 37')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        ]


def test_start(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        ]


def test_good_day_for_o_player(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 2 1')
    bot.handle_message('O 1 2')
    bot.handle_message('X 2 2')
    bot.handle_message('O 1 0')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('.X.\n.O.\n...'),
        mocker.call('.X.\n.O.\n.X.'),
        mocker.call('.X.\n.OO\n.X.'),
        mocker.call('.X.\n.OO\n.XX'),
        mocker.call('.X.\nOOO\n.XX'),
        mocker.call('Game is finished, O wins')]


def test_invalid_players(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 2 0')
    bot.handle_message('O 2 0')
    bot.handle_message('X 1 1')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\nX..'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')]


def test_sudden_start_over(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('start')
    bot.handle_message('X 1 1')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...')]
