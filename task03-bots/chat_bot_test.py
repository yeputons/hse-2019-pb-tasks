import pytest_mock
from chat_bot import ChatBot


def test_chat_broadcast(mocker: pytest_mock.MockFixture) -> None:
    send_message = mocker.stub(name='send_message_stub')
    bot = ChatBot(send_message)
    bot.handle_message(10, 'hello')
    bot.handle_message(11, 'world')
    assert send_message.call_args_list == [
        mocker.call(10, '#10: hello'),
        mocker.call(10, '#11: world'),
        mocker.call(11, '#11: world'),
    ]
