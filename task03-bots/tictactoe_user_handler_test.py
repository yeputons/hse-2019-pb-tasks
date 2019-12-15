import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_tic_tac_toe_some_fails_simple(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('')
    bot.handle_message('hi')
    bot.handle_message('starts')
    bot.handle_message(' start')
    bot.handle_message('start')
    bot.handle_message('O 1 2')
    bot.handle_message('O 3 3')
    bot.handle_message('X 1 1')
    bot.handle_message('X 2 2')
    bot.handle_message('O 3 2')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]


def test_tic_tac_toe_x_wins_simple(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 2')
    bot.handle_message('X 1 2')
    bot.handle_message('O 0 0')
    bot.handle_message('X 1 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\n..O'),
        mocker.call('...\n.X.\n.XO'),
        mocker.call('O..\n.X.\n.XO'),
        mocker.call('OX.\n.X.\n.XO'),
        mocker.call('Game is finished, X wins')
    ]


def test_tic_tac_toe_o_wins_simple(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 2')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 2')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 2 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\nX..'),
        mocker.call('...\n.O.\nX..'),
        mocker.call('...\n.O.\nXX.'),
        mocker.call('O..\n.O.\nXX.'),
        mocker.call('O.X\n.O.\nXX.'),
        mocker.call('O.X\n.O.\nXXO'),
        mocker.call('Game is finished, O wins')
    ]


def test_tic_tac_toe_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 1')
    bot.handle_message('O 2 2')
    bot.handle_message('X 1 2')
    bot.handle_message('hey?')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XOX\n...\n...'),
        mocker.call('XOX\n.O.\n...'),
        mocker.call('XOX\nXO.\n...'),
        mocker.call('XOX\nXO.\nO..'),
        mocker.call('XOX\nXOX\nO..'),
        mocker.call('XOX\nXOX\nO.O'),
        mocker.call('XOX\nXOX\nOXO'),
        mocker.call('Game is finished, draw'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...')
    ]


def test_tic_tac_toe_lots_of_fails_complex(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('hi')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 2')
    bot.handle_message('start')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 3 3')
    bot.handle_message('O 2 2')
    bot.handle_message('X 2 0')
    bot.handle_message('please start')
    bot.handle_message('X 1 1')
    bot.handle_message('start')
    bot.handle_message('')
    bot.handle_message('X 1 1')
    bot.handle_message('start')
    bot.handle_message('stop')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('XX.\n.O.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('XX.\n.O.\n..O'),
        mocker.call('XXX\n.O.\n..O'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn')
    ]


def test_tic_tac_toe_o_wins_complex(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 2')
    bot.handle_message('yehoo')
    bot.handle_message('start')
    bot.handle_message("let's repeat")
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 2 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 2')
    bot.handle_message('good')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XOX\n...\n...'),
        mocker.call('XOX\n.O.\n...'),
        mocker.call('XOX\nXO.\n...'),
        mocker.call('XOX\nXO.\n.O.'),
        mocker.call('Game is finished, O wins'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XOX\n...\n...'),
        mocker.call('XOX\n.O.\n...'),
        mocker.call('XOX\nXO.\n...'),
        mocker.call('XOX\nXO.\n.O.'),
        mocker.call('Game is finished, O wins'),
        mocker.call('Game is not started')
    ]
