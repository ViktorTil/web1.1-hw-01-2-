import sys
   
from functions import *
from base_cls import *

def input_command_items():
    messenger.send_message(WELCOME)
    load_books(filename)

    while True:
        messenger.send_message(command_offer(command_maps))
        command = nick_str(command_item = messenger.input_message(ENTER_COMMAND), command_items = command_maps.keys())
        if command:
            try:
                messenger.send_message(command_maps[command](messenger))
            except TypeError:
                try:
                    items = command_items(command, messenger)
                    items = nick_str(command = command, command_items = items)
                    for item in items:
                        if item == "note":
                            name = messenger.input_message(ENTER_NOTE_TITLE)
                            messenger.send_message(
                                command_maps[command]([item], name, messenger))
                            items.remove(item)
                                
                        if len(items) < 1:
                            continue
                    
                        if item == "tags" and item in list(filter(lambda x: available_options[command][x] == True, available_options[command])):
                            name = messenger.input_message(
                                ENTER_NOTE_TITLE_TAGS)
                            messenger.send_message(
                                command_maps[command](items, name, messenger))
                        
                        elif item in list(filter(lambda x: available_options[command][x] == True, available_options[command])):
                            name = messenger.input_message(ENTER_NAME_CONTACT)
                            messenger.send_message(
                                command_maps[command](items, name, messenger))

                        else:
                            messenger.send_message(CHOOSE_OPTIONS)

                except KeyError:
                    folder = messenger.input_folder(FOLDER_ORGANIZE)
                    messenger.send_message(command_maps[command](folder, messenger))
                    continue
                  
            
if __name__ == "__main__":
    
    messenger = Console_Messenger()
    try:
        if sys.argv[1].lower() == 'telegram':
            messenger = Telegram_Messenger()
            print(sys.argv[1].lower())
            exit()
    except IndexError:
        pass
    input_command_items()
