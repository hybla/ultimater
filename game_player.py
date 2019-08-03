import random
import os
import json

# import my own modules
import m_file
from m_angle import angle_to, direction
from m_zones import zones, directions


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

# function that finds which zone a point is in
def zone_finder(point):
    current_zone = 'OFF_FIELD'
    for z in field:
        #assign values to variables
        x1,y1=field[z][0][0],field[z][0][1]
        x2,y2=field[z][1][0],field[z][1][1]
        x,y=point[0],point[1]
        # is our point between the x and y corners of the zone?
        if (x >= x1 and x <= x2 and y >= y1 and y <= y2) :
            current_zone = z
            break
    return current_zone

# a tester for zone_finder()
def zone_finder_TESTER():
    for x in range(142):
        for y in range(47):
            print ('Point ({}, {}) is in Zone: {}'.format(x, y, zone_finder((x,y))))

# flips the field.  Used to get locations from the Away team's point of view
# the field is flipped the long way only, so only the x value is flipped (not y).
def flip_field(point):
    field_length = 140
    flipped = (field_length - point[0], point[1])
    return flipped

# a tester for flip_field()
def flip_field_TESTER():
    for x in range(0, 140, 5):
        for y in range(0, 45, 5):
            a = flip_field((x, y))[0]
            b = flip_field((x, y))[1]
            print ('Point ({}, {}) flipped is ({}, {})'.format(x, y, a, b))

# tells you which genes to use for direction calculations.
# works for MovementOpponent, MovementTeammate, ThrowOpponent,
# and ThrowTeammate
# Pass it the direction towards the other player that your working on.
# (for example, N, NE, S etc.)
def direction_index(player_dir):
    gene_index = []
    for d in directions:
        if player_dir == d:
            gene_index.append(d + '_Yes')
        else:
            gene_index.append(d + '_No')
    return gene_index

# Set up starting (kickoff) player locations
start_spots = dict()
start_spots['home_left']   = (  0, 35)
start_spots['home_center'] = (  0, 22)
start_spots['home_right']  = (  0, 10)
start_spots['away_left']   = (115, 10)
start_spots['away_center'] = (115, 22)
start_spots['away_right']  = (115, 35)

# Define the Team and Player classes
class Player:
    location = (0,0)
    has_disc = False

    steps = 0
    throws = 0
    completed_throws = 0
    intercepted_throws = 0
    turnovers = 0
    thrown_goals = 0
    caught_goals = 0
    
    def __init__(self, name, position, team):
        self.name = name
        self.position = position
        self.team = team
    def description(self):
        msg = (
            'Details for player named {0}:\n'
            '  Location: {1[0]:d}, {1[1]:d}\n  Has disc: {2}\n'
            '  Steps Taken: {3}\n  Throws Made: {4}\n  Throws Completed: {5}\n'
            '  Throws Intercepted: {6}\n  Turnovers: {7}\n  Thrown Goals: {8}\n'
            '  Caught Goals: {9}\n  Team: {10}\n  Home team: {11}\n'.format(self.name, self.location, self.has_disc,
               self.steps, self.throws, self.completed_throws,
               self.intercepted_throws, self.turnovers, self.thrown_goals,
               self.caught_goals, self.team.name, self.team.home_team))
        return msg 

class Team:
    
    def __init__(self, name, generation, genes, home_team):
        self.name = name
        self.generation = generation
        self.genes = genes
        self.home_team = home_team # am I the home team? Boolean.
        self.left = Player('left', 'left', self)
        self.center = Player('center', 'center', self)
        self.right = Player('right', 'right', self)

    def description(self):
        team_msg = (
            'Details for team {} from generation {}:\n'
            'Home team: {}\n'.format(self.name, self.generation, self.home_team))
        left_msg = self.left.description()
        center_msg = self.center.description()
        right_msg = self.right.description()
        return team_msg + left_msg + center_msg + right_msg

# Defining the game class
class Game:
    clock = 0

    def __init__(self, home, away, duration, start_spots):
        self.home = home
        self.away = away
        self.duration = duration
        self.start_spots = start_spots
        self.player_list = [home.left, home.center, home.right,
                            away.left, away.center, away.right]
    def setup(self):
        # Put the players on the field and give the home center the disc
        home.left.location = start_spots['home_left']
        home.center.location = start_spots['home_center']
        home.right.location = start_spots['home_right']
        away.left.location = start_spots['away_left']
        away.center.location = start_spots['away_center']
        away.right.location = start_spots['away_right']
        home.center.has_disc = True

    def describe_all(self):
        msg = ''
        for p in self.player_list:
            msg = msg + p.description()
        return msg

    def disc_holder(self):
        # which player has the disc?
        for t in [home, away]:
            for p in [t.left, t.center, t.right]:
                if p.has_disc == True:
                    dh = p
                    break
        return dh

    # all the players who can move, and want to move, move
    def move(self):
        # create a list of the players who can move (don't have the disc)
        movers = self.player_list.copy()
        movers.remove(self.disc_holder())
        for p in movers:
            # create a place to hold all the gene values that will
            # go into the decision about whether or not to move
            gene_pile = dict()
            for d in directions:
                gene_pile[d] = dict()
                gene_pile[d]['MyPos'] = 0 # a place for the 'MovementMe' value
                gene_pile[d][0] = 0 # for the 'MovementOpponent' and
                gene_pile[d][1] = 0 # 'MovementTeammate' values
                gene_pile[d][2] = 0
                gene_pile[d][3] = 0
                gene_pile[d][4] = 0
            print('the original gene_pile:\n{}\n'.format(gene_pile))
            if p.team == home:
                # find the zone of the mover, and load the MovementMe gene values
                zone = zone_finder(p.location)
                for d in directions:
                    gene_pile[d]['MyPos'] = p.team.genes['MovementMe'][zone + '_' + d]
                print('the gene_pile after adding MyPos:\n{}\n'.format(gene_pile))
                # now load the MovementTeammate and MovementOpponent genes
                others = self.player_list.copy()
                others.remove(p)
                counter = 0
                for other in others:
                    a = angle_to(p.location, other.location)
                    d = direction(a)
                    index = direction_index(d)
                    if p.team == other.team:
                        genetype = 'MovementTeammate'
                    else:
                        genetype = 'MovementOpponent'

                    for d in directions:
                        for i in index:
                            gene_pile[d][counter] = p.team.genes[genetype][i]
                    counter += 1
                    print('the gene_pile in the Others loop:\n{}\n'.format(gene_pile))






            else:
                zone = zone_finder(flip_field(p.location))





# Load the home and away team genomes. In the future this should be
# done creating the team pairngs for a round-robin, but for
# now we are just selecting two teams by hand.
generation = 'TEST2'
Path = '/Users/testuser/Projects/ultimater/data/teams/test'
os.chdir(Path)
Teamlist = m_file.read('GEN-' + generation + '_teamlist')
home_team_name = Teamlist['Teams'][3]
away_team_name = Teamlist['Teams'][22]
home_genes = m_file.read(home_team_name)
away_genes = m_file.read(away_team_name)

# Instantiate the home and away teams
home = Team(home_team_name, generation, home_genes, True)
away = Team(away_team_name, generation, away_genes, False)

# Instantiate the game
game = Game(home, away, 100, start_spots)
game.setup()
game.move()

# done.

