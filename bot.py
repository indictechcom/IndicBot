# -*- coding: utf-8 -*-
from botscripts.login import login
from scripts.template_subs import run_template_subs
import sys
from requests import Session

# Login with wiki and get the login session
SESSION: Session | None = login()

# Check the session
if SESSION is None:
    sys.exit("There is some problem with login :(")

else:

    # Check whether the scriptname exist in the argument or not
    if len(sys.argv) < 2:
        print('Script Name is missing: Try \'python3 bot.py scriptname\'')

    else:
        if sys.argv[1] == 'template_subs':
            # Run the script
            run_template_subs(SESSION)
            print("\nDone :)")            
        else:
            print("Wrong script name!")
# Clear the session
SESSION.cookies.clear()