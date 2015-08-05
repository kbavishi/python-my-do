#!/usr/bin/python

"""Creates .env file based on user input"""

import getpass

if __name__ == '__main__':
    # Take input from user
    ifttt_key = getpass.getpass( "Enter the key to be used to authenticate "
                                 "the IFTTT recipe: " )
    any_do_username = raw_input( "Enter your Any.do username: " )
    any_do_password = getpass.getpass( "Enter your Any.do password: " )

    # Create the file
    with open( ".env", "w" ) as f:
        f.write( "%s=%s\n" % ( "IFTTT_KEY", ifttt_key ) )
        f.write( "%s=%s\n" % ( "ANY_DO_USERNAME", any_do_username ) )
        f.write( "%s=%s\n" % ( "ANY_DO_PASSWORD", any_do_password ) )
