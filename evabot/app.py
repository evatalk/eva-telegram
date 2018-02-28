import telepot
from telepot.loop import MessageLoop
from request_handler import Response

def handle(msg):
    print(Response.request_to_response(msg))

def main():
    bot = telepot.Bot("515344383:AAGJjjzTMvP4TuHzRpQyx1Vx6r5s-QVlx_E")
    MessageLoop(bot, handle).run_as_thread()


if __name__ == '__main__':
    print("Initializing EVA ..")
    print("To shutdown, press CTRL + C")
    main()
    
    while True:
        pass