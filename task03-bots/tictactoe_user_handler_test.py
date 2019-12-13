import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_tictactoe_user_hander_correct_work(mocker: pytest_mock.MockFixture
                                            ) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('start')
    for i in range(2):
        bot.handle_message('X ' + str(i) + ' 0')
        bot.handle_message('O ' + str(i) + ' 1')

    bot.handle_message('X 2 0')
    bot.handle_message(TicTacToeUserHandler.START_COMMAND)
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


def test_ticktactoe_user_hadler_incorrect_work(mocker: pytest_mock.MockFixture
                                               ) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message('aavbb')
    bot.handle_message('X 0 1')
    bot.handle_message(TicTacToeUserHandler.START_COMMAND)
    bot.handle_message('X 0 0')
    bot.handle_message('O 2 2')
    bot.handle_message('O 1 1')
    bot.handle_message('O 0 0')
    bot.handle_message('X 2 2')
    bot.handle_message('X 0 0')
    bot.handle_message('X 1 1')
    assert send_message.call_args_list == [
        mocker.call(TicTacToeUserHandler.GAME_IS_NOT_STARTED),
        mocker.call(TicTacToeUserHandler.GAME_IS_NOT_STARTED),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n...\n..O'),
        mocker.call(TicTacToeUserHandler.INVALID_TURN),
        mocker.call(TicTacToeUserHandler.INVALID_TURN),
        mocker.call(TicTacToeUserHandler.INVALID_TURN),
        mocker.call(TicTacToeUserHandler.INVALID_TURN),
        mocker.call('X..\n.X.\n..O'),
    ]


def test_ticktactoe_user_hadler_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message(TicTacToeUserHandler.START_COMMAND)
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
        mocker.call(TicTacToeUserHandler.GAME_FINISHED + ' draw')
    ]


def test_ticktactoe_user_hadler_O_wins(mocker: pytest_mock.MockFixture
                                       ) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = TicTacToeUserHandler(send_message)
    bot.handle_message(TicTacToeUserHandler.START_COMMAND)
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
        mocker.call(TicTacToeUserHandler.GAME_FINISHED + ' O wins')
    ]
