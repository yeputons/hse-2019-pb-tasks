import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_tictactoe_user_handler_invalid_turn(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    user_handler = TicTacToeUserHandler(send_message)

    user_handler.handle_message('hi')
    user_handler.handle_message('X 1 1')
    user_handler.handle_message('start')
    user_handler.handle_message('X 1 1')
    user_handler.handle_message('O 0 1')
    user_handler.handle_message('O 0 0')
    user_handler.handle_message('start')

    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\nOX.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('...\n...\n...')
    ]


def test_tictactoe_user_handler_both_players_win(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    user_handler = TicTacToeUserHandler(send_message)

    user_handler.handle_message('start')
    user_handler.handle_message('X 0 1')
    user_handler.handle_message('O 1 1')
    user_handler.handle_message('X 0 2')
    user_handler.handle_message('O 1 0')
    user_handler.handle_message('X 0 0')
    user_handler.handle_message('start')
    user_handler.handle_message('X 0 0')
    user_handler.handle_message('O 0 1')
    user_handler.handle_message('X 1 0')
    user_handler.handle_message('O 1 1')
    user_handler.handle_message('X 2 2')
    user_handler.handle_message('O 2 1')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\nX..\n...'),
        mocker.call('...\nXO.\n...'),
        mocker.call('...\nXO.\nX..'),
        mocker.call('.O.\nXO.\nX..'),
        mocker.call('XO.\nXO.\nX..'),
        mocker.call('Game is finished, X wins'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\nO..\n...'),
        mocker.call('XX.\nO..\n...'),
        mocker.call('XX.\nOO.\n...'),
        mocker.call('XX.\nOO.\n..X'),
        mocker.call('XX.\nOOO\n..X'),
        mocker.call('Game is finished, O wins')
    ]


def test_tictactoe_user_handler_draw(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    user_handler = TicTacToeUserHandler(send_message)

    user_handler.handle_message('start')
    user_handler.handle_message('X 1 1')
    user_handler.handle_message('O 0 2')
    user_handler.handle_message('X 0 1')
    user_handler.handle_message('O 2 1')
    user_handler.handle_message('X 2 2')
    user_handler.handle_message('O 0 0')
    user_handler.handle_message('X 1 0')
    user_handler.handle_message('O 1 2')
    user_handler.handle_message('X 2 0')

    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('...\n.X.\n...'),
        mocker.call('...\n.X.\nO..'),
        mocker.call('...\nXX.\nO..'),
        mocker.call('...\nXXO\nO..'),
        mocker.call('...\nXXO\nO.X'),
        mocker.call('O..\nXXO\nO.X'),
        mocker.call('OX.\nXXO\nO.X'),
        mocker.call('OX.\nXXO\nOOX'),
        mocker.call('OXX\nXXO\nOOX'),
        mocker.call('Game is finished, draw')
    ]


def test_tictactoe_user_handler_invlid_turn_2(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    user_handler = TicTacToeUserHandler(send_message)

    user_handler.handle_message('hi')
    user_handler.handle_message('X 1 1')
    user_handler.handle_message('start')
    user_handler.handle_message('X 5 6')

    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        ]
