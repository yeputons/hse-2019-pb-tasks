#!/usr/bin/env python3
import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_simple_error_message(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('rofl')
    assert send_message.call_args_list == [
        mocker.call('Game is not started')
    ]


def test_two_games_in_a_row(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('start')
    bot.handle_message('X 1 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...\n'),
        mocker.call('...\n.X.\n...\n'),
        mocker.call('...\n...\n...\n'),
        mocker.call('...\nX..\n...\n'),
    ]


def test_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 2')
    bot.handle_message('X 0 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 2 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...\n'),
        mocker.call('...\n.X.\n...\n'),
        mocker.call('...\nOX.\n...\n'),
        mocker.call('X..\nOX.\n...\n'),
        mocker.call('X..\nOX.\n..O\n'),
        mocker.call('X.X\nOX.\n..O\n'),
        mocker.call('XOX\nOX.\n..O\n'),
        mocker.call('XOX\nOX.\nX.O\n'),
        mocker.call('Game is finished, X wins'),
    ]


def test_make_turn_y_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 2')
    bot.handle_message('O 1 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...\n'),
        mocker.call('...\n...\n..X\n'),
        mocker.call('O..\n...\n..X\n'),
        mocker.call('O..\n..X\n..X\n'),
        mocker.call('O..\nO.X\n..X\n'),
        mocker.call('O..\nOXX\n..X\n'),
        mocker.call('O..\nOXX\nO.X\n'),
        mocker.call('Game is finished, O wins'),
    ]


def test_draw_draw_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 2 2')
    bot.handle_message('O 1 2')
    bot.handle_message('X 0 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 2 0')
    bot.handle_message('X 2 1')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...\n'),
        mocker.call('...\n...\n..X\n'),
        mocker.call('...\n..O\n..X\n'),
        mocker.call('..X\n..O\n..X\n'),
        mocker.call('.OX\n..O\n..X\n'),
        mocker.call('XOX\n..O\n..X\n'),
        mocker.call('XOX\n.OO\n..X\n'),
        mocker.call('XOX\nXOO\n..X\n'),
        mocker.call('XOX\nXOO\nO.X\n'),
        mocker.call('XOX\nXOO\nOXX\n'),
        mocker.call('Game is finished, draw'),
    ]


def two_in_one_error(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 0')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn')
    ]
