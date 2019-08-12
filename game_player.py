import random
import os
import json
from statistics import mean

# import my own modules
import m_file
from m_angle import angle_to, direction
from m_zones import zones, directions, field

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

# Translate a move direction (like N, S, SE) to an offset (like (1, 0)).
# Used by move_offset()
def direction_to_offset(d):
    offsets = dict()
    offsets['N']  = ( 0,  1)
    offsets['NE'] = ( 1,  1)
    offsets['E']  = ( 1,  0)
    offsets['SE'] = ( 1, -1)
    offsets['S']  = ( 0, -1)
    offsets['SW'] = (-1, -1)
    offsets['W']  = (-1,  0)
    offsets['NW'] = (-1,  1)
    return offsets[d]

# tells you which direction a player wants to move in. Uses the
# gene_piles that is created in Game.move(). Returns a tuple indicating
# the x and y offset to apply to the player position.  Does the
# field flipping for away players.
def move_offset(p, gene_piles):
    move_urge = 0
    move_dir = ''
    offset = (0, 0)
    # find which direction the player most wants to move in:
    for d in directions:
        mean = gene_piles[p][d]['Mean']
        if mean > move_urge:
            move_urge = mean
            move_dir = d
    # calculate the actual move offset
    if move_urge < p.team.genes['Threshhold']['Move']:
        offset = (0, 0)
        print('>> move urge for {}: {} {:.4}, Threshhold: {:.4}'.format(p.name, move_dir, move_urge, p.team.genes['Threshhold']['Move']))
    else:
        offset = direction_to_offset(move_dir)
    # flip East / West for away players
    if p.team.home_team == False:
        offset = (offset[0] * -1, offset[1])
    return offset

# adds two 'location' tuples.
def add_tups(a, b):
    return (a[0] + b[0], a[1] + b[1])

# Set up starting (kickoff) player locations
start_spots = dict()
start_spots['home_left']   = ( 25, 35)
start_spots['home_center'] = ( 25, 22)
start_spots['home_right']  = ( 25, 10)
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
            '  Steps Taken: {3}\n  Throws Made: {4}\n'
            '  Throws Completed: {5}\n'
            '  Throws Intercepted: {6}\n  Turnovers: {7}\n'
            '  Thrown Goals: {8}\n  Caught Goals: {9}\n'
            '  Team: {10}\n  Home team: {11}\n'.format(self.name,
               self.location, self.has_disc,
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
        if self.home_team == True:
            self.left = Player('home_left', 'left', self)
            self.center = Player('home_center', 'center', self)
            self.right = Player('home_right', 'right', self)
        else:
            self.left = Player('away_left', 'left', self)
            self.center = Player('away_center', 'center', self)
            self.right = Player('away_right', 'right', self)

    def description(self):
        team_msg = (
            'Details for team {} from generation {}:\n'
            'Home team: {}\n'.format(self.name, self.generation,
                                     self.home_team))
        left_msg = self.left.description()
        center_msg = self.center.description()
        right_msg = self.right.description()
        return team_msg + left_msg + center_msg + right_msg

# Defining the game class
class Game:
    clock = 0
    game_record = dict()

    def __init__(self, home, away, duration, start_spots):
        self.home = home
        self.away = away
        self.duration = duration
        self.start_spots = start_spots
        self.player_list = [home.left, home.center, home.right,
                            away.left, away.center, away.right]
    # create a dict to hold a complete record of the game
    # this is saved to a file after the game is played and
    # used by the viewer to play back the game

    def setup(self):
        # Put the players on the field and give the home center the disc
        home.left.location = start_spots['home_left']
        home.center.location = start_spots['home_center']
        home.right.location = start_spots['home_right']
        away.left.location = start_spots['away_left']
        away.center.location = start_spots['away_center']
        away.right.location = start_spots['away_right']
        home.center.has_disc = True
        self.game_record['Home_Team'] = home.name
        self.game_record['Away_Team'] = away.name
        self.game_record['Duration'] = self.duration
        self.game_record['Start_Spots'] = dict()
        self.game_record['Start_Spots'] \
                        ['home_left'] = home.left.location
        self.game_record['Start_Spots'] \
                        ['home_center'] = home.center.location
        self.game_record['Start_Spots'] \
                        ['home_right'] = home.right.location
        self.game_record['Start_Spots'] \
                        ['away_left'] = away.left.location
        self.game_record['Start_Spots'] \
                        ['away_center'] = away.center.location
        self.game_record['Start_Spots'] \
                        ['away_right'] = away.right.location
        for n in range(self.duration):
            self.game_record[n] = dict()
            self.game_record[n]['Moves'] = ''
            self.game_record[n]['Throw'] = ''

    def print_headline(self):
        print('Today\'s Game: {} (away) vs. {} (home).'.format(self.away.name, self.home.name))

    def describe_all(self):
        msg = ''
        for p in self.player_list:
            msg = msg + p.description()
        return msg

    def print_all_player_locations(self):
        print('home L:{} C:{} R:{}\n'
              'away L:{} C:{} R:{}'.format(self.home.left.location,
                                           self.home.center.location,
                                           self.home.right.location,
                                           self.away.left.location,
                                           self.away.center.location,
                                           self.away.right.location))
                                                                
    def disc_holder(self):
        # which player has the disc?
        for t in [home, away]:
            for p in [t.left, t.center, t.right]:
                if p.has_disc == True:
                    dh = p
                    break
        return dh

    def save_record(self, path):
        os.chdir(path)
        m_file.save(self.game_record, self.away.name +
                                      '_vs_' + game.home.name)

    # all the players who can move, and want to move, move
    def move(self):
        # create a place to store all the moves made.
        # the method will return this list.
        moves = dict()
        # create a list of the players who can move (don't have the disc)
        movers = self.player_list.copy()
        movers.remove(self.disc_holder())
        # create a place to store all the players gene_piles
        gene_piles = dict()
        for p in movers:
            # create a place to hold all the gene values that will
            # go into the decision about whether or not to move
            gene_pile = dict()
            for d in directions:
                gene_pile[d] = dict()
                gene_pile[d]['MyPos'] = 0 # a place for the
                                          # 'MovementMe' value
                gene_pile[d][0] = 0 # for the 'MovementOpponent' and
                gene_pile[d][1] = 0 # 'MovementTeammate' values
                gene_pile[d][2] = 0
                gene_pile[d][3] = 0
                gene_pile[d][4] = 0
                gene_pile[d]['Mean'] = 0 # this will store the mean value
                                       # for this direction, used to decide
                                       # where to move
            # now we do all the operations to load up the gene_pile from the genes
            # find the zone of the mover
            if p.team == home:
                zone = zone_finder((p.location))
            else:
                zone = zone_finder(flip_field(p.location))
            # put MyPos into the gene_pile for each direction
            for d in directions:
                gene_pile[d]['MyPos'] = p.team.genes['MovementMe'][zone + '_' + d]
            # now load the MovementTeammate and MovementOpponent genes
            others = self.player_list.copy()
            others.remove(p)
            counter = 0
            for other in others:
                # find the direction to each other player, flipping field for away team
                if p.team == home:
                    a = angle_to((p.location), (other.location))
                else:
                    a = angle_to(flip_field(p.location), flip_field(other.location))
                d = direction(a)
                index = direction_index(d)
                if p.team == other.team:
                    genetype = 'MovementTeammate'
                else:
                    genetype = 'MovementOpponent'
                # load the right gene for MovementTeammate or MovementOpponent
                for d in directions:
                    for i in index:
                        if d == i.split('_')[0]:
                            gene_pile[d][counter] = p.team.genes[genetype][i]
                counter += 1
            # find the mean gene value for each direction
            for d in directions:
                gene_pile[d]['Mean'] = mean([gene_pile[d]['MyPos'],
                                            gene_pile[d][0],
                                            gene_pile[d][1],
                                            gene_pile[d][2],
                                            gene_pile[d][3],
                                            gene_pile[d][4]])
            # add the completed gene_pile for this player to gene_piles
                gene_piles[p] = gene_pile
        # actually move the players to their new locations
        for p in movers: 
            do_not_move = False
            others = self.player_list.copy()
            others.remove(p)
            offset = move_offset(p, gene_piles)
            new_location = add_tups(p.location, offset)
            # make sure the player is not trying to move off the field
            if zone_finder(new_location) == 'OFF_FIELD':
                do_not_move = True
                print('{} is trying to move off the field'.format(p.name))
            # make sure the player is not crashing into another player
            else:
                for other in others:
                    if new_location == other.location:
                        do_not_move = True
                        print('{} is crashing into'
                              'another player'.format(p.name))
                        print('>> crashing into'
                              '{} at {}'.format(other.name, other.location))
                        break
            if do_not_move == False:
                print('moving {} by offset {} to {}'.format(p.name,
                                                     offset, new_location))
                p.location = new_location
                mv = dict()
                mv['offset'] = offset
                mv['location'] = new_location
                moves[p.name] = mv
        self.game_record[self.clock]['Moves'] = moves
        self.clock += 1
        return moves

# Load the home and away team genomes. In the future this should be
# done creating the team pairngs for a round-robin, but for
# now we are just selecting two teams by hand.
generation = 'TEST3'
Path = '/Users/testuser/Projects/ultimater/data/teams/test'
os.chdir(Path)
Teamlist = m_file.read('GEN-' + generation + '_teamlist')
home_team_name = Teamlist['Teams'][3]
away_team_name = Teamlist['Teams'][4]
home_genes = m_file.read(home_team_name)
away_genes = m_file.read(away_team_name)

# Instantiate the home and away teams
home = Team(home_team_name, generation, home_genes, True)
away = Team(away_team_name, generation, away_genes, False)

# Instantiate the game
game = Game(home, away, 500, start_spots)
print('after instantiating the game:')
game.print_all_player_locations()

game.setup()
print('after game setup:')
game.print_all_player_locations()
game.print_headline()

for n in range(game.duration):
    print('count = {}'.format(n))
    play_moves = game.move()
    print(play_moves)

Path = Path + '/games'
game.save_record(Path)
print(game.game_record)

# done.
