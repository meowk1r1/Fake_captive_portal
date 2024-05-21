class bstring:
    ERROR = '[\033[91merror\033[0m]'
    INFO = '[\033[92minfo\033[0m]'
    ACTION = '[\033[93maction\033[0m]'
    CREDS = '[\033[1;95;5mcreds\033[0m]'
    INPUT = '[\033[94minput\033[0m]'
    VIOLET = '\033[95m' 
    BLUE = '\033[96m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():

    print(bstring.VIOLET + """\
███╗   ███╗███████╗ ██████╗ ██╗    ██╗
████╗ ████║██╔════╝██╔═══██╗██║    ██║
██╔████╔██║█████╗  ██║   ██║██║ █╗ ██║
██║╚██╔╝██║██╔══╝  ██║   ██║██║███╗██║
██║ ╚═╝ ██║███████╗╚██████╔╝╚███╔███╔╝
          
FAKE CAPTIVE PORTAL""" + bstring.RESET +
bstring.BOLD + """
[ Fake CP v1 ] [ Created by github.com/meowk1r1 ]
""" + bstring.RESET)