# Contains some basic data structures defining the field etc.

# Create the list of Zones:
# OZ (own zone)
# L1 L2 L3 (left zones)
# C2 C2 C3 (center zones)
# R1 R2 R3 (right zones)
# EZ (end zone)
zones = ['OZ', 'L1', 'L2', 'L3', 'C2', 'C2', 'C3', 'R1', 'R2', 'R3', 'EZ']

# Set up the field
field = dict()
field['OZ'] = [(  0,  0),(  25, 45)] # Own Zone
field['L1'] = [( 25, 30),(  55, 45)] # Left Zones
field['L2'] = [( 55, 30),(  85, 45)]
field['L3'] = [( 85, 30),( 115, 45)]
field['C1'] = [( 25, 15),(  55, 30)] # Center Zones
field['C2'] = [( 55, 15),(  85, 30)]
field['C3'] = [( 85, 15),( 115, 30)]
field['R1'] = [( 25,  0),(  55, 15)] # Right Zones
field['R2'] = [( 55,  0),(  85, 15)]
field['R3'] = [( 85,  0),( 115, 15)]
field['EZ'] = [(115,  0),( 140, 45)] # End Zone

# Create the list of Directions
directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

# done.
