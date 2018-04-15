import telepot
from handlers.requestor import Response
from settings import BOT
from telepot.loop import MessageLoop
from handlers.reader import MessageInfoHandler
from controllers.main import EVAController


def main():
    eva = EVAController()
    MessageLoop(BOT, eva.main).run_as_thread()


if __name__ == '__main__':
    print("Initializing EVA ..")
    print("To shutdown, press CTRL + C")
    main()

    while True:
        pass
