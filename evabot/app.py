from telegram.ext import Updater, CommandHandler

from commands import BotCommands

def main():
    # Create the Updater and pass it your bot's token.
    # Replace 'TOKEN' with your Bot's API token.
    updater = Updater("TOKEN")

    # Start the Bot
    updater.start_polling()

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register handlers.
    dispatcher.add_handler(CommandHandler('start', BotCommands.start))

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    print("Initializing EVA ..")
    print("To shutdown, press CTRL + C")
    main()