from pytest_mock import MockFixture
from tictactoe_user_handler import TicTacToeUserHandler


def integration_test_x_wins(mocker: MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    bot.handle_message('X 0 0')
    bot.handle_message('Look')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 1')
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 2')
    bot.handle_message('X 0 2')
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('XX.\n.O.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('XX.\n.O.\n..O'),
        mocker.call('Game is finished, X wins')
    ]


def test_draw(mocker: MockFixture):
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('Cat')
    bot.handle_message('X 1 1')
    bot.handle_message('start')
    bot.handle_message('X 1 0')
    bot.handle_message('O 1 1')
    bot.handle_message('X 0 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 2')
    bot.handle_message('O 0 2')
    bot.handle_message('X 2 0')
    bot.handle_message('O 2 1')
    bot.handle_message('X 1 2')
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\nX..\n...'),
        mocker.call('...\nXO.\n...'),
        mocker.call('.X.\nXO.\n...'),
        mocker.call('OX.\nXO.\n...'),
        mocker.call('OX.\nXO.\n..X'),
        mocker.call('OXO\nXO.\n..X'),
        mocker.call('OXO\nXO.\nX.X'),
        mocker.call('OXO\nXO.\nXOX'),
        mocker.call('Game is finished, draw')
    ]
