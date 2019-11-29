#!/usr/bin/env python3
import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_integrative_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('gsdjkghskfd')
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 2')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 0 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 0 1')
    bot.handle_message('O 2 1')
    bot.handle_message('X 2 2')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.XX\n...'),
        mocker.call('O..\nOXX\n...'),
        mocker.call('O..\nOXX\nX..'),
        mocker.call('O.O\nOXX\nX..'),
        mocker.call('Invalid turn'),
        mocker.call('OXO\nOXX\nX..'),
        mocker.call('OXO\nOXX\nXO.'),
        mocker.call('OXO\nOXX\nXOX'),
        mocker.call('Game is finished, draw'),
    ]


def test_integrative_x(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('sdfads')
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 2')
    bot.handle_message('O 2 2')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 2')
    bot.handle_message('O 2 1')
    bot.handle_message('X 1 0')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\n.XX\n...'),
        mocker.call('O..\n.XX\n..O'),
        mocker.call('OX.\n.XX\n..O'),
        mocker.call('Invalid turn'),
        mocker.call('OX.\n.XX\n.OO'),
        mocker.call('OX.\nXXX\n.OO'),
        mocker.call('Game is finished, X wins'),
    ]


def test_integrative_o(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('sdvsdfsfdvs')
    bot.handle_message('start')
    bot.handle_message('X 2 2')
    bot.handle_message('O 1 1')
    bot.handle_message('X 2 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 2')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n..X'),
        mocker.call('...\n.O.\n..X'),
        mocker.call('...\n.O.\n.XX'),
        mocker.call('...\n.O.\nOXX'),
        mocker.call('.X.\n.O.\nOXX'),
        mocker.call('.XO\n.O.\nOXX'),
        mocker.call('Game is finished, O wins'),
    ]
