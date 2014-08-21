"""
                    Yet Another Subnet Calculator

    Last updated:   08 / 21 / 2014



    Last working on:

            Available Hosts per Network
            Available Subnets

    TODO:
        - Fix input of masks at /8 or lower:
            /8 shows 255.0.0
            Lower shows 0.0.0.0
            Binary Mask displays incorrectly

        - Fix Avail Subnets:
            191.168.5.4 /14 returns 0.25 because the class is wrong.

        - Add wildcard masks
        - Colorize output for better visibility -- hopefully with ANSI escape codes for $BASH.
                Maybe it works with Windows too?
"""