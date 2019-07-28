import random
import os

# Are we in debug mode?
debug = True

# Set up the field
Field = dict()
Field['OZ'] = [  0,  0,  25, 45] # Own Zone
Field['L1'] = [ 25, 30,  55, 45] # Left Zones
Field['L2'] = [ 55, 30,  85, 45]
Field['L3'] = [ 85, 30, 115, 45]
Field['C1'] = [ 25, 15,  55, 30] # Center Zones
Field['C2'] = [ 55, 15,  85, 30]
Field['C3'] = [ 85, 15, 115, 30]
Field['R1'] = [ 25,  0,  55, 15] # Right Zones
Field['R2'] = [ 55,  0,  85, 15]
Field['R3'] = [ 85,  0, 115, 15]
Field['EZ'] = [115,  0, 140, 45] # End Zone

# Set up Player Positions
Player_positions = ['Left', 'Center', 'Right']

# Set up Teams
Teams = ['Home', 'Away']

# Set up Rosters
Roster = dict()
for team in Teams:
    Roster[team] = Player_positions

# Set up game stats. These will be tracked for teams and maybe for individual players as well.
Stats = ['Goals', 'Completions', 'Interceptions', 'Incomplete_passes']

# Set up Scoreboard
Scoreboard = dict()
for team in Teams:
    for stat in Stats:
        key = team + '_' + stat
        Scoreboard[key] = 0

# Set up overall game status.
Status = dict()
Status['Time'] = 0 # Game time, meaning a count of plays
Status['Posession'] = 'Home' # the Home team starts with the disc. They kick off to the away team.


# Debug actions
if debug:
    print('----- Field Debug -----\n')
    print('the field is:\n', Field)
    print('here is the whole field:\n')
    for zone in Field:
        print(zone, ': ', Field[zone])

    print('\n----- Scoreboard Debug -----')
    print('the Scoreboard is:\n', Scoreboard)
    print('\nhere is the whole Scoreboard:')
    for key in Scoreboard:
        print(key, ': ', Scoreboard[key])

    print('\n----- Roster Debug -----')
    print('the Roster is:\n', Roster)
    print('\nhere is the whole Roster:')
    for key in Roster:
        print(key, ': ', Roster[key])
    
    print('\n----- Status Debug -----')
    print('the Status is:\n', Status)
    print('\nhere is the whole Status:')
    for key in Status:
        print(key, ': ', Status[key])

# done.

