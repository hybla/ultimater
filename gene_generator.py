import random
import os
import json

# Are we in debug mode?
debug = True

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

# Saves a genome to a file
def Save_genome_to_file(genome, filename):
    with open(filename, 'w') as outfile:
        json.dump(genome, outfile)
    
# Reads a genome from a file
def Read_genome_from_file(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data


if debug == True:
    genome = CreateTeamGenome('test')
    print('the whole genome is: \n', genome, '\n')
    print('team name = ', genome['Team'], '\n')
    print('Throw threshhold is: \n', genome['Threshhold']['Throw'], '\n')
    print('ThrowOpponent is: \n', genome['ThrowOpponent'], '\n')

    cwd = os.getcwd()
    print('Current Directory is: ', cwd)
    os.chdir("/Users/testuser/Projects/ultimater/data/teams")
    nwd = os.getcwd()
    print('Current Directory is: ', nwd)
    
    # with open('TestTeam.txt', 'w') as f:
    #    print(CreateTeamGenome('test'), file=f)

    Save_genome_to_file(genome, 'testy123.txt')
    ImportedGenome = Read_genome_from_file('testy123.txt')
    print('Imported genome is:', ImportedGenome)

# done.
