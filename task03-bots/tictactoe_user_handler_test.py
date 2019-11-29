import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_tictactoe_not_start(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('aafafa')
    bot.handle_message('asasfafaasd')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started')
    ]


def test_tictactoe_start(mocker: pytest_mock.MockFixture, capsys) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '...\n...\n...\n'


def test_tictactoe_invalid_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('X 2 0')
    bot.handle_message('X 2 1')
    assert send_message.call_args_list == [
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]


def test_tictactoe_valid_turn(mocker: pytest_mock.MockFixture, capsys) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '...\n...\n...\n...\n.X.\n...\n'


def test_tictactoe_win(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 2 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 1')
    assert send_message.call_args_list == [
        mocker.call('Game is finished, X wins'),
    ]


def test_tictactoe_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 2 1')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 2')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 2')
    assert send_message.call_args_list == [
        mocker.call('Game is finished, draw'),
    ]
