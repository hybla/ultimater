import random
import os
import json

# import my own modules
import m_file

debug = False

# Create the list of Zones:
# OZ (own zone)
# L1 L2 L3 (left zones)
# C2 C2 C3 (center zones)
# R1 R2 R3 (right zones)
# EZ (end zone)
Zones = ['OZ', 'L1', 'L2', 'L3', 'C2', 'C2', 'C3', 'R1', 'R2', 'R3', 'EZ']

# Create the list of Directions
Directions = ['N', 'NE', 'E', 'SE', 'W', 'SW', 'W', 'NW']

# Create the complete genome for a team
def CreateTeamGenome(team_name):
    ''' Creates a team with random genes. Returns the genome as a dict.'''
# Create the Movement genes
# Influence whether or not a player will move, and in what direction
    MovementMe = dict()
    for zone in Zones:
        for direction in Directions:
            key = zone + '_' + direction
            MovementMe[key] = random.random()

    MovementOpponent = dict()
    for direction in Directions:
        for IsThere in ['Yes', 'No']:
            key = direction + '_' + IsThere 
            MovementOpponent[key] = random.random()

    MovementTeammate = dict()
    for direction in Directions:
        for IsThere in ['Yes', 'No']:
            key = direction + '_' + IsThere 
            MovementTeammate[key] = random.random()

# Create the Throw Genes
# Influence whether or not a player will throw, and in what direction
    ThrowMe = dict()
    for zone in Zones:
        for direction in Directions:
            key = zone + '_' + direction
        ThrowMe[key] = random.random()

    ThrowOpponent = dict()
    for direction in Directions:
        for IsThere in ['Yes', 'No']:
            key = direction + '_' + IsThere 
            ThrowOpponent[key] = random.random()

    ThrowTeammate = dict()
    for direction in Directions:
        for IsThere in ['Yes', 'No']:
            key = direction + '_' + IsThere 
            ThrowTeammate[key] = random.random()

# Create the Threshhold Genes
# The threshold above which a player will move or throw
    Threshhold = dict()
    Threshhold['Move'] = random.random()
    Threshhold['Throw'] = random.random()

# Assemble the complete genome into a dictionary
    Genome = dict()
    Genome['Team'] = team_name
    Genome['MovementMe'] = MovementMe
    Genome['MovementOpponent'] = MovementOpponent
    Genome['MovementTeammate'] = MovementTeammate
    Genome['ThrowMe'] = ThrowMe
    Genome['ThrowOpponent'] = ThrowOpponent
    Genome['ThrowTeammate'] = ThrowTeammate
    Genome['Threshhold'] = Threshhold

    return Genome

# Creates a set of teams and saves them as individual files
def Create_teams(qty, generation, path):
    Teamlist = dict()
    Teamlist['Generation'] = 'GEN-' + generation
    Teamlist['Path'] = path
    Teamlist['Teams'] = []
    os.chdir(path)
    for n in range(qty):
        teamname = 'GEN-' + generation + '_' + str(n).zfill(3)
        genome = CreateTeamGenome(teamname)
        m_file.save(genome, teamname)
        Teamlist['Teams'].append(teamname)
    with open('GEN-' + generation + '_teamlist', 'w') as outfile:
        json.dump(Teamlist, outfile)
    return Teamlist
       
Create_teams(100, 'TEST3','/Users/testuser/Projects/ultimater/data/teams/test')


if debug == True:
    genome = CreateTeamGenome('test')
    print('the whole genome is: \n', genome, '\n')
    print('team name = ', genome['Team'], '\n')
    print('Throw threshhold is: \n', genome['Threshhold']['Throw'], '\n')
    print('ThrowOpponent is: \n', genome['ThrowOpponent'], '\n')

    cwd = os.getcwd()
    print('Current Directory is: ', cwd)
    os.chdir("/Users/testuser/Projects/ultimater/data/teams/test")
    nwd = os.getcwd()
    print('Current Directory is: ', nwd)
    
    Save_genome_to_file(genome, 'test001.txt')
    ImportedGenome = Read_genome_from_file('test001.txt')
    print('Imported genome is:', ImportedGenome)

# done.
