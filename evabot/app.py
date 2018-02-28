import telepot
from telepot.loop import MessageLoop

def handle(msg):
    print(msg['text'])

def main():
    bot = telepot.Bot(TOKEN)
    MessageLoop(bot, handle).run_as_thread()


if __name__ == '__main__':
    print("Initializing EVA ..")
    print("To shutdown, press CTRL + C")
    main()