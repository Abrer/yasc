__author__ = 'abrer'    # PyCharm adds this to everything....

# All the maths for yasc.

import sys

def cidr_to_decimal(network_bits):
    # Take CIDR /notation (/30) and return the decimal equivalent

    network_bits = network_bits[1:]  # Remove the / at the beginning

    full_octets = int(network_bits) / 8
    octets_left = 4 - int(full_octets)
    remaining_bits = int(network_bits) % 8
    remaining_bits = str(remaining_bits)

    bit_decimal_vals = {
        '0':   '0.',
        '1': '128.',
        '2': '192.',
        '3': '224.',
        '4': '240.',
        '5': '248.',
        '6': '252.',
        '7': '254.',
        '8': '255.'
    }

    decimal_mask = ''

    for i in range(0, full_octets):
        decimal_mask += '255.'
        if i == full_octets - 1:
            octets_left -= 1
            if int(remaining_bits) > 0:
                decimal_mask += bit_decimal_vals[remaining_bits]

    # Add 0's to remaining octets
    for i in range(0, octets_left):
        if octets_left == 0:
            break
        else:
            decimal_mask += '0.'

    return decimal_mask[:-1]

def num_of_hosts(net_bits):
    # Return number of hosts per network
    MAX_BITS = 32
    hosts_per_network = 2 ** (MAX_BITS - net_bits) - 2

    return str(hosts_per_network)

def num_of_networks(net_class, net_bits):
    # Return number of networks the subnetting yields.

    class_bits = 0

    if net_class == 'A':
        class_bits = 8
    if net_class == 'B':
        class_bits = 16
    if net_class == 'C':
        class_bits = 24

    networks = 2 ** (net_bits - class_bits)

    return str(networks)

def get_first_usable_address(network_address):
    #Get first usable address
    network_address = network_address.split('.')

    # String to hold final address
    first_usable = ''

    # Turns out the first usable address is just the last octet + 1
    for i in range(0, len(network_address)):
        if i == 3:
            network_address[i] = str(int(network_address[i]) + 1)
        # Just adding decimal points so our address looks proper.
        first_usable += network_address[i] + '.'

    return first_usable[:-1]

def get_last_usable_address(broadcast_address):
    # Just -1 from the last octet apparently?
    # let's try it...
    broadcast_address = broadcast_address.split('.')

    # Last octet - 1
    for i in range(0, len(broadcast_address)):
        if i == 3:
            broadcast_address[i] = str(int(broadcast_address[i]) - 1)

    # String to hold our final address
    last_usable = ''

    # Just adding decimal points so our address looks proper.
    for i in range(0, len(broadcast_address)):
        last_usable += broadcast_address[i] + '.'

    #Shaves off the last . from the string so it looks nice. Slices are awesome!
    return last_usable[:-1]

def get_broadcast(ip_net_address, working_octet, net_increment):
    # Currently returns Broadcast
    net_address = ip_net_address.split('.')
    working_octet -= 1

    for i in range(0, len(net_address)):
        if i == working_octet:
            net_address[i] = str(int(net_address[i]) + net_increment -1)
        if i > working_octet:
            net_address[i] = '255'

    broadcast_address = ''

    for i in range(0, len(net_address)):
        broadcast_address += net_address[i] + '.'

    return broadcast_address[:-1]

def get_network_address(ip_address, working_octet, net_increment):
    # Get Network Address
    working_octet -= 1  # Subtract 1 since list index start at 0.

    ip_address = ip_address.split('.')

    # For every octet past initial work octet, set to 0
    for i in range(0, len(ip_address)):
        if i > working_octet:
            ip_address[i] = '0'

    # Math for network address
    ip_address[working_octet] = str((int(ip_address[working_octet]) / int(net_increment)) * net_increment)

    network_address = ip_address[0] + '.' + ip_address[1] + '.' + ip_address[2]\
                      + '.' + ip_address[3]  # Find a better way to do this

    return network_address

def get_working_octet_value(subnet_mask):
    # Return the DECIMAL VALUE of working octet
    # CLONE OF GETWORKINGOCTET() til I figure out if I want to combine them.
    subnet_mask = subnet_mask.split('.')
    working_octet_value = ''

    for i in range(0, len(subnet_mask)):
        if subnet_mask[i] != '255':
            working_octet_value = subnet_mask[i]
            break
        elif i == 3:  # DEBUGGING PURPOSES -- in the event that mask is /32
            working_octet_value = subnet_mask[i]

    return working_octet_value

def get_binary_mask(subnet_mask):
    # Return Mask in Binary
    subnet_mask = subnet_mask.split('.')
    binary_mask= []
    binary_mask_string = ''

    for i in range(0, len(subnet_mask)):
        # Convert each octet to binary
        binary_mask.append(format(int(subnet_mask[i]), '08b'))

        # And save to MaskString
        binary_mask_string = binary_mask_string + binary_mask[i] + '.'

    return binary_mask_string[:-1]  # Remove the '.' at the end of the string.

def get_network_bits(subnet_mask):
    # Based on Subnet Mask
    bits = 0

    # Decimal:          128 192 224 240 248 252 254 255
    # Bits in Mask:     1   2    3   4  5   6   7   8

    # Dictionary of subnet vals
    # and their # of bits in an octet
    mask_bit_values = {
        '0':   0,
        '128': 1,
        '192': 2,
        '224': 3,
        '240': 4,
        '248': 5,
        '252': 6,
        '254': 7,
        '255': 8
    }

    subnet_mask = subnet_mask.split('.')

    for octet in subnet_mask:
        if octet == '255':
            bits += 8
        if octet != '255':
            # Do math to get bits from value and add to bits var
            if octet in mask_bit_values:
                bits += mask_bit_values[octet]
    return bits

def get_working_octet(subnet_mask):
    # Return the octet in which we can work
    subnet_mask = subnet_mask.split('.')
    working_octet = ''

    for i in range(0, len(subnet_mask)):
        if subnet_mask[i] != '255':
            working_octet = i+1
            break
        else:
            working_octet = 4  # This is in the case that the mask is a /32 for now. DEBUGGING PURPOSES.

    return working_octet

def get_net_increment(working_octet_value):
    # Return the Network Increment based on
    # the working octet value of our Subnet Mask.
    if working_octet_value == '0':
        return 1
    else:
        return 256 - int(working_octet_value)

def get_class(ip_address):
    # Get our class!
    ip_address = ip_address.split('.')

    first_octet = int(ip_address[0])
    net_class = ''

    if first_octet > 0:
        net_class = 'A'
    if first_octet >= 128:
        net_class = 'B'
    if first_octet >= 192:
        net_class = 'C'
    if first_octet >= 224:  # 224 and above is multicast
        net_class = 'MULTICAST'
    if first_octet >= 240:  # 240 and above is expirmental / reserved
        net_class = 'E / EXPERIMENTAL'
    if first_octet == 127:  # 127.x.x.x is loopback
        net_class = 'LOOPBACK'

    return net_class

def err_check_input(arguments):

    #[0] should be script location
    #[1] should be IP Address
    #[2] Should be Subnet in DECIMAL or CIDR notation

    if len(arguments) < 3:
        print '\nOh dear! You need 2 arguments! '
        print 'Something like: $ yasc.py 192.168.2.25 255.255.255.0'
        print 'OR: $ yasc.py 192.168.2.25 /24\n'
        sys.exit(0)

    elif len(arguments) > 3:
        print '\nNow that\'s just too damn many son. You only need TWO arguments.'
        print 'Something like: $ yasc.py 192.168.2.25 255.255.255.0'
        print 'OR: $ yasc.py 192.168.2.25 /24\n'
        sys.exit(0)

    if '/' in arguments[2]:
        bits = arguments[2]
        bits = int(bits[1:])
        if bits > 30:
            print '\nDem bits is too damn high! Don\'t exceed /30!'
            print 'Should I have a use for that in the future I\'ll add it in.\n'
            sys.exit(0)