import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_x_game_winner(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 2')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 2')
    bot.handle_message('X 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\n.O.'),
        mocker.call('...\nXX.\n.O.'),
        mocker.call('...\nXXO\n.O.'),
        mocker.call('..X\nXXO\n.O.'),
        mocker.call('.OX\nXXO\n.O.'),
        mocker.call('.OX\nXXO\n.OX'),
        mocker.call('.OX\nXXO\nOOX'),
        mocker.call('XOX\nXXO\nOOX'),
        mocker.call('Game is finished, X wins')
    ]


def test_o_game_winner(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 2')
    bot.handle_message('X 2 1')
    bot.handle_message('O 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XOX\n...\n...'),
        mocker.call('XOX\n.O.\n...'),
        mocker.call('XOX\nXO.\n...'),
        mocker.call('XOX\nXO.\n..O'),
        mocker.call('XOX\nXOX\n..O'),
        mocker.call('XOX\nXOX\n.OO'),
        mocker.call('Game is finished, O wins')
    ]


def test_draw_game(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 2 2')
    bot.handle_message('X 2 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 2')
    bot.handle_message('X 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XOX\n...\n...'),
        mocker.call('XOX\n...\n..O'),
        mocker.call('XOX\n..X\n..O'),
        mocker.call('XOX\n.OX\n..O'),
        mocker.call('XOX\nXOX\n..O'),
        mocker.call('XOX\nXOX\nO.O'),
        mocker.call('XOX\nXOX\nOXO'),
        mocker.call('Game is finished, draw')
    ]


def test_start_game(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start!')
    bot.handle_message('nachali!')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...')
    ]


def test_turns(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 1')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]


def test_few_starts(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...')
    ]
