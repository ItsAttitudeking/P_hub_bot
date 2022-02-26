HEROKU = True  #

# 
if HEROKU:
    from os import environ

    Bot_token = environ["Bot_token"]
    ARQ_API_KEY = environ["ARQ_API_KEY"]

# 
if not HEROKU:
    Bot_token = "Insert Bot_Token Here"
    ARQ_API_KEY = "Get this from @ARQRobot"
