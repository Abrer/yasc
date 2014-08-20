#!/usr/bin/python2
__author__ = 'abrer'    # PyCharm adds this to everything....
# Last updated 08 / 20 / 2014
# Yet Another Subnet Calculator --  YASC 

""" Last working on:

        - Moved calc functions to their own file: submath.py
        - Those functions are now imported.

    TODO:
        - Fix input of masks at /8 or lower:
            /8 shows 255.0.0
            Lower shows 0.0.0.0
        - Finish the GetClass() function! It's easy, dunno why I haven't bothered yet.
        - Fix line 92 -- use a for loop to add . for readability... mehbe.
        - Add subnets per host and etc...
        - Colorize output for better visibility -- hopefully with ANSI escape codes for $BASH.
"""
import sys

# import all of the old functions now in the
# newly created submath.py file!
from submath import *

def main():

    # # Fixed values for debugging
    # ip_address = '192.168.15.43'
    # # subnet_mask = '255.255.255.252'

    err_check_input(sys.argv)

    # Detect CIDR (/20, /24, /29) notation.
    if '/' in sys.argv[2]:
        # If CIDR ('/'), convert to decimal
        subnet_mask = cidr_to_decimal(sys.argv[2])
    else:
        # If no '/' found, it's already in decimal
        subnet_mask = sys.argv[2]
    ip_address = sys.argv[1]

    # Some handy vars!
    network_bits = get_network_bits(subnet_mask)
    working_octet = get_working_octet(subnet_mask)
    working_octet_value = get_working_octet_value(subnet_mask)
    
    net_increment = get_net_increment(working_octet_value)
    binary_mask = get_binary_mask(subnet_mask)

    network_address = get_network_address(ip_address,
                                          working_octet, net_increment)
    
    broadcast_address = get_broadcast(network_address,
                                      working_octet, net_increment)

    last_usable_address = get_last_usable_address(broadcast_address)
    first_usable_address = get_first_usable_address(network_address)

    # Print our info to the screen!
    print ''
    print 'IP Address: \t%s /%s'        % (ip_address, network_bits)
    print 'Subnet Mask: \t%s'           % subnet_mask
    print '-' * 40                      # Divider!
    print 'Network Addr: \t%s'          % network_address
    print 'Network Range: \t%s - %s'    % (first_usable_address, last_usable_address)
    print 'Broadcast: \t%s'             % broadcast_address
    print '-' * 40                      # Divider!
    print 'Binary Mask: \t%s'           % binary_mask
    print 'Net Increment: \t%s'         % net_increment
    print ''



    # These values are used for calculating subnet information
    # and aren't generally relevant to the subnetter.
    #
    # Working octet may be useful as it's the relevant octet
    # for which we are subnetting.

    # print 'Working Octet: \t\t%s'     % working_octet
    # print 'Working Octet Val: \t%s'   % working_octet_value


# Boilerplate to start main()
if __name__ == '__main__':
    main()