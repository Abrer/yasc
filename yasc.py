#!/usr/bin/python2
__author__ = 'abrer'    # PyCharm adds this to everything....
# Yet Another Subnet Calculator --  YASC

import sys

# import all of the old functions now in the
# newly created submath.py file
from submath import *

def main():

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
    network_class = get_class(ip_address)
    network_bits = get_network_bits(subnet_mask)
    working_octet = get_working_octet(subnet_mask)
    working_octet_value = get_working_octet_value(subnet_mask)
    
    net_increment = get_net_increment(working_octet_value)
    binary_mask = get_binary_mask(subnet_mask)

    network_address = get_network_address(ip_address,
                                          working_octet, net_increment, network_bits)
    
    broadcast_address = get_broadcast(network_address,
                                      working_octet, net_increment, network_bits)

    last_usable_address = get_last_usable_address(broadcast_address)
    first_usable_address = get_first_usable_address(network_address)

    available_hosts = num_of_hosts(network_bits)
    available_subnets = num_of_networks(network_class, network_bits)

    # Print our info to the screen
    print ''
    print 'IP Address: \t%s /%s'        % (ip_address, network_bits)
    print 'Subnet Mask: \t%s'           % subnet_mask
    print '-' * 15                      # Divider!
    print 'Class: \t\t%s'               % network_class
    print 'Network Addr: \t%s'          % network_address
    print 'Host Range: \t%s - %s'       % (first_usable_address, last_usable_address)
    print 'Broadcast: \t%s'             % broadcast_address
    print 'Avail Hosts: \t%s'           % available_hosts
    print 'Avail Subnets: \t%s'         % available_subnets
    print '-' * 15                      # Divider!
    print 'Binary Mask: \t%s'           % binary_mask
    print 'Net Increment: \t%s'         % net_increment
    print ''


    # Working octet may be useful as it's the relevant octet
    # for which we are subnetting.
    # print 'Working Octet: \t\t%s'     % working_octet


# Boilerplate to start main()
if __name__ == '__main__':
    main()