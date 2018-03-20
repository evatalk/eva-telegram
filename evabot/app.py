import telepot
from request_handler import Response
from settings import TELEGRAM_TOKEN
from telepot.loop import MessageLoop
from utils import MessageInfoHandler

BOT = telepot.Bot(TELEGRAM_TOKEN)


def handle(msg):
    # Chamar o controller
    BOT.sendMessage(MessageInfoHandler.get_chat_id(msg),
                    Response.request_to_response(msg))


def main():
    MessageLoop(BOT, handle).run_as_thread()


if __name__ == '__main__':
    print("Initializing EVA ..")
    print("To shutdown, press CTRL + C")
    main()

    while True:
        pass
