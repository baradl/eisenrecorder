import request as re

def get_session_from_user(sessions):
    if len(sessions) > 1:
        print("Found more than one session for that date:")
        for session in sessions:
            re.printer.print_session(session)
        which_session = int(input("Type index of session [>0]: "))
        session = sessions[which_session]
    else:
        session = sessions[0]

    return session
