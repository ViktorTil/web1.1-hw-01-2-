class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
filename = "data.bin"
file_help = "help.txt"

WELCOME = "Welcome to Virtual Assistant!"
BYE = "Good bye! Have a nice day!"
ENTER_COMMAND = "Enter the command: "
ENTER_NOTE_TITLE = f"Enter the {Colors.HEADER}note title{Colors.ENDC}: "
ENTER_NOTE_TITLE_TAGS = f"Enter the {Colors.HEADER}note title{Colors.ENDC} of the tags: "
ENTER_NAME_CONTACT = f"Enter the name of the contact: "
CHOOSE_OPTIONS = f"{Colors.FAIL}{Colors.UNDERLINE}Error: choose from available options.{Colors.ENDC}"
FOLDER_ORGANIZE = "Enter the path of the folder to organize: "
ENTER_CONTENT = "Enter the content: "
ADD_TAGS = "Add tags: "
ERROR_CHOICE = f"{Colors.FAIL}{Colors.UNDERLINE}Error: Invalid choice.{Colors.ENDC}"
NO_PHONE = f"{Colors.FAIL}{Colors.UNDERLINE}Error: No phone numbers available.{Colors.ENDC}"
AVAILABLE_PHONES = "Available phones: "


format_maps = {
                "phone": "any ukrainian number",
                "email": "any email format",
                "birthday": "any data format in this sequence: dd,mm, yyyy",
                "address": "free",
            }

available_options = {
    "add":
        {
            "contact": True, 
            "phone": True, 
            "email": True, 
            "birthday": True, 
            "address": True, 
            "note": True,
            "tags": True
        },
    "edit":
        {
            "contact": False, 
            "phone": True,  
            "email": True,  
            "birthday": True,  
            "address": True,  
            "note": True, 
            "tags": False
        },
    "delete": 
        {
            "contact": True, 
            "phone": True,  
            "email": True,  
            "birthday": True,  
            "address": True,  
            "note": True, 
            "tags": False
        }
    }

