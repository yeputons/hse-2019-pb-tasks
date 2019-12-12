import pytest_mock
from tictactoe_user_handler import TicTacToeUserHandler


def test_tictactoe_user_handler_part1(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    message_sequence = [
        'not start',
        'start',
        'X 0 0',
        'O 1 1',
        'X 1 0',
        'X 2 0',
        'O 2 2',
        'X 2 0',
        'O 0 2',
        'X wins',
        'start',
        'X 1 2',
        'O 2 0',
        'O 1 0',
        'start',
        'O 0 0',
        'X 0 0',
        'O 0 0'
    ]
    for msg in message_sequence:
        handler.handle_message(msg)
    assert send_message.call_args_list == [
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('X..\n.O.\n...'),
        mocker.call('XX.\n.O.\n...'),
        mocker.call('Invalid turn'),
        mocker.call('XX.\n.O.\n..O'),
        mocker.call('XXX\n.O.\n..O'),
        mocker.call('Game is finished, X wins'),
        mocker.call('Game is not started'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('...\n...\n.X.'),
        mocker.call('..O\n...\n.X.'),
        mocker.call('Invalid turn'),
        mocker.call('...\n...\n...'),
        mocker.call('Invalid turn'),
        mocker.call('X..\n...\n...'),
        mocker.call('Invalid turn')
    ]


def test_tictactoe_user_handler_part2(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    handler = TicTacToeUserHandler(send_message)
    message_sequence = [
        'start',
        'X 1 0',
        'O 0 0',
        'X 0 2',
        'O 2 2',
        'X 0 1',
        'O 1 1',
        'O wins',
        'start',
        'X 0 0',
        'O 1 0',
        'X 1 1',
        'O 2 0',
        'X 2 1',
        'O 0 1',
        'X 0 2',
        'O 2 2',
        'X 1 2',
        'this is draw'
    ]
    for msg in message_sequence:
        handler.handle_message(msg)
    assert send_message.call_args_list == [
        mocker.call('...\n...\n...'),
        mocker.call('.X.\n...\n...'),
        mocker.call('OX.\n...\n...'),
        mocker.call('OX.\n...\nX..'),
        mocker.call('OX.\n...\nX.O'),
        mocker.call('OX.\nX..\nX.O'),
        mocker.call('OX.\nXO.\nX.O'),
        mocker.call('Game is finished, O wins'),
        mocker.call('Game is not started'),
        mocker.call('...\n...\n...'),
        mocker.call('X..\n...\n...'),
        mocker.call('XO.\n...\n...'),
        mocker.call('XO.\n.X.\n...'),
        mocker.call('XOO\n.X.\n...'),
        mocker.call('XOO\n.XX\n...'),
        mocker.call('XOO\nOXX\n...'),
        mocker.call('XOO\nOXX\nX..'),
        mocker.call('XOO\nOXX\nX.O'),
        mocker.call('XOO\nOXX\nXXO'),
        mocker.call('Game is finished, draw'),
        mocker.call('Game is not started')
    ]
