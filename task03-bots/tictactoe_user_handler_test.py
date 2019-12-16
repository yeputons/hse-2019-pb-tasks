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


def test_winner_o(mocker: MockFixture) -> None:
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
        mocker.call('...\nX..\n...'),
        mocker.call('...\nXO.\n...'),
        mocker.call('...\nXOX\n...'),
        mocker.call('...\nXOX\n.O.'),
        mocker.call('...\nXOX\n.OX'),
        mocker.call('.O.\nXOX\n.OX'),
        mocker.call('Game is finished, O wins')]


def test_winner_x(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 0')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('.O.\n.X.\n...'),
        mocker.call('.O.\n.X.\nX..'),
        mocker.call('OO.\n.X.\nX..'),
        mocker.call('OOX\n.X.\nX..'),
        mocker.call('Game is finished, X wins')]


def test_draw(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 2 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 1 2')
    bot.handle_message('X 1 0')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X..\n.O.\n..X'),
        mocker.call('X..\nOO.\n..X'),
        mocker.call('X..\nOOX\n..X'),
        mocker.call('X.O\nOOX\n..X'),
        mocker.call('X.O\nOOX\nX.X'),
        mocker.call('X.O\nOOX\nXOX'),
        mocker.call('XXO\nOOX\nXOX'),
        mocker.call('Game is finished, draw')]


def test_invalid_turns(mocker: MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 2 0')
    bot.handle_message('O 2 0')
    bot.handle_message('X 1 1')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('..X\n...\n...'),
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
