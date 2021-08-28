updater = Updater(token='1736686159:AAFG0jC4qEHE5ahhc_F7kZY-LMH5UR1lxAM', use_context=True)
dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger()

updater.start_polling(drop_pending_updates = True)


