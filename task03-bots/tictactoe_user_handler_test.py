import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 0')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.XO\n...'),
        mocker.call('X..\n.XO\n...'),
        mocker.call('X.O\n.XO\n...'),
        mocker.call('X.O\n.XO\n..X'),
        mocker.call('Game is finished, X wins')
    ]


def test_o_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\nX..\n...'),
        mocker.call('..O\nX..\n...'),
        mocker.call('..O\nXX.\n...'),
        mocker.call('..O\nXXO\n...'),
        mocker.call('X.O\nXXO\n...'),
        mocker.call('X.O\nXXO\n..O'),
        mocker.call('Game is finished, O wins')
    ]


def test_draw_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 2')
    bot.handle_message('X 0 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('..O\n.X.\n...'),
        mocker.call('..O\nXX.\n...'),
        mocker.call('..O\nXXO\n...'),
        mocker.call('..O\nXXO\n..X'),
        mocker.call('O.O\nXXO\n..X'),
        mocker.call('OXO\nXXO\n..X'),
        mocker.call('OXO\nXXO\n.OX'),
        mocker.call('OXO\nXXO\nXOX'),
        mocker.call('Game is finished, draw')
    ]


def test_after_win_words(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 1 0')
    bot.handle_message('O 2 1')
    bot.handle_message('X 1 2')
    bot.handle_message('O 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('..O\n.X.\n...'),
        mocker.call('.XO\n.X.\n...'),
        mocker.call('.XO\n.XO\n...'),
        mocker.call('.XO\n.XO\n.X.'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started')
    ]


def test_inter_game_words(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 2 2')
    bot.handle_message('O 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('..O\n.X.\n...'),
        mocker.call('..O\n.X.\nX..'),
        mocker.call('..O\n.X.\nX.O'),
        mocker.call('Invalid turn')
    ]


def pre_game_words_test(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('X 0 0')
    assert send_message.call_args_list == [
        mocker.call('Invalid turn')
    ]


def test_inter_game_restart(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 2 2')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\n...\nX..'),
        mocker.call('XO.\n...\nX.O'),
        mocker.call('...\n...\n...')
    ]


def test_exception(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('I want to try exception:D')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('Invalid turn')
    ]
