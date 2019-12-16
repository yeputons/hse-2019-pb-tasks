import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_tictactoe_user_hander_x_wins(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 2 0')
    bot.handle_message('start')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\nO..\n...'),
        mocker.call('XX.\nO..\n...'),
        mocker.call('XX.\nOO.\n...'),
        mocker.call('XXX\nOO.\n...'),
        mocker.call('Game is finished, X wins'),
        mocker.call('...\n...\n...')
    ]


def test_ticktactoe_user_hadler_o_wins(mocker: pytest_mock.MockFixture
                                       ) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 2 0')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('X.X\n.O.\n...'),
        mocker.call('XOX\n.O.\n...'),
        mocker.call('XOX\nXO.\n...'),
        mocker.call('XOX\nXO.\n.O.'),
        mocker.call('Game is finished, O wins')
    ]


def test_ticktactoe_user_hadler_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 2 0')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 2')
    bot.handle_message('X 2 1')
    bot.handle_message('O 1 2')
    bot.handle_message('X 0 2')
    bot.handle_message('O 0 1')
    bot.handle_message('X 1 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('..O\n.X.\n...'),
        mocker.call('X.O\n.X.\n...'),
        mocker.call('X.O\n.X.\n..O'),
        mocker.call('X.O\n.XX\n..O'),
        mocker.call('X.O\n.XX\n.OO'),
        mocker.call('X.O\n.XX\nXOO'),
        mocker.call('X.O\nOXX\nXOO'),
        mocker.call('XXO\nOXX\nXOO'),
        mocker.call('Game is finished, draw')
    ]


def test_tictactoe_user_hander_multiple_games(mocker: pytest_mock.MockFixture
                                              ) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 1')
    bot.handle_message('X q 1')
    bot.handle_message('X 1 1')
    bot.handle_message('X 1 0')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 0')
    bot.handle_message('O 2 2')
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('start')
    bot.handle_message('X 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 0 1')
    bot.handle_message('O 1 0')
    bot.handle_message('X 0 2')
    bot.handle_message('O 2 0')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('XX.\n.O.\n...'),
        mocker.call('XX.\n.O.\nO..'),
        mocker.call('XXX\n.O.\nO..'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('O..\n.X.\n...'),
        mocker.call('O..\nXX.\n...'),
        mocker.call('OO.\nXX.\n...'),
        mocker.call('OO.\nXX.\nX..'),
        mocker.call('OOO\nXX.\nX..'),
        mocker.call('Game is finished, O wins')
    ]


def test_ticktactoe_user_hadler_invalid_turns_while_making_turn(
        mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('aavbb')
    bot.handle_message('X 0 1')
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 2')
    bot.handle_message('O 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 2')
    bot.handle_message('X 0 0')
    bot.handle_message('X 1 1')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n...\n..O'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n.X.\n..O'),
    ]


def test_ticktactoe_user_hadler_invalid_turns_while_parsing(
        mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('a b c')
    bot.handle_message('X q w')
    bot.handle_message('X 1 1')
    bot.handle_message('O 1 w')
    bot.handle_message('X q 2')
    bot.handle_message('q 1 2')
    bot.handle_message('o q')
    bot.handle_message('O 1')
    bot.handle_message('X O')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('...\n.X.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn'),
        mocker.call('Invalid turn')
    ]
