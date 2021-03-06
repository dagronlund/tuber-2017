from robot import Robot
from constants import Actions, TileType
import random
from math import *
import time

##########################################################################
# One of your team members, Chris Hung, has made a starter bot for you.  #
# Unfortunately, he is busy on vacation so he is unable to aid you with  #
# the development of this bot.                                           #
#                                                                        #
# Make sure to read the README for the documentation he left you         #
#                                                                        #
# @authors: christoh, [TEAM_MEMBER_1], [TEAM_MEMBER_2], [TEAM_MEMBER_3]  #
# @version: 2/4/17                                                       #
#                                                                        #
# README - Introduction                                                  #
#                                                                        #
# Search the README with these titles to see the descriptions.           #
##########################################################################

# !!!!! Make your changes within here !!!!!
class player_robot(Robot):

    def __init__(self, args):
        super(self.__class__, self).__init__(args)
        ##############################################
        # A couple of variables - read what they do! # 
        #                                            #
        # README - My_Robot                          #
        ##############################################
        self.toHome = []
        self.numturns = 0            
        self.goinghome = False;      
        self.targetPath = None
        self.targetDest = (0,0)
        self.preferred_dir = None
        self.x = 0
        self.y = 0
        self.turn = 0

        self.history = [((0, 0), 0)] * 10

        self.home_path = []
        # print(self.history)

        # for i in range(0, SetupConstants.BOARD_DIM)

        # self.angle = random.random() * pi / 2.0
        # self.x_prob = ((pi / 2.0) - angle) / (pi / 2.0)
        # self.y_prob = angle / (pi / 2.0)


        # self.preferred_dir = random.choice([Actions.MOVE_E,Actions.MOVE_N,
        #                   Actions.MOVE_S,Actions.MOVE_W,
        #                   Actions.MOVE_NW,Actions.MOVE_NE,
        #                   Actions.MOVE_SW,Actions.MOVE_SE])

        # def weighted_choice(choices):
        # total = sum(w for c, w in choices)
        # r = random.uniform(0, total)
        # upto = 0
        # for c, w in choices:
        #   if upto + w >= r:
        #      return c
        #   upto += w
        # assert False, "Shouldn't get here"


    # A couple of helper functions (Implemented at the bottom)
    def OppositeDir(self, direction):
        return # See below

    def ViewScan(self, view):
        return # See below

    def FindRandomPath(self, view):
        return # See below

    def UpdateTargetPath(self):
        return # See below

    ###########################################################################################
    # This function is called every iteration. This method receives the current robot's view  #
    # and returns a tuple of (move_action, marker_action).                                    #
    #                                                                                         #
    # README - Get_Move                                                                       #
    ###########################################################################################
    def get_move(self, view):
        self.turn += 1

        if self.preferred_dir is None:
            self.preferred_dir = random.choice([Actions.MOVE_E,Actions.MOVE_N,
                          Actions.MOVE_S,Actions.MOVE_W,
                          Actions.MOVE_NW,Actions.MOVE_NE,
                          Actions.MOVE_SW,Actions.MOVE_SE])
            # print('Preferred dir', self.preferred_dir)
        
        recalculate = False
        dist = abs(self.x - self.history[0][0][0]) + abs(self.y - self.history[0][0][1])
        if dist < 5:
            recalculate = True

        for chapter in self.history:
            if chapter[1] == 1:
                recalculate = False

        if recalculate:
            #print "Recalculate"
            self.preferred_dir = random.choice([Actions.MOVE_E,Actions.MOVE_N,
                          Actions.MOVE_S,Actions.MOVE_W,
                          Actions.MOVE_NW,Actions.MOVE_NE,
                          Actions.MOVE_SW,Actions.MOVE_SE])

        # print(self.held_value())
        # Returns home if you have one resource
        # if (self.held_value() > 0):
        #     self.goinghome = True

        if (995 - self.turn <= len(self.toHome)) or (self.storage_remaining() == 0):
            self.goinghome = True
            # print(self.toHome)

            # print("Going Home", self.storage_remaining(), self.held_value())

        # How to navigate back home
        if(self.goinghome):
            # You are t home
            if(self.toHome == []):
                self.goinghome = False
                # print("Home", self.x, self.y)
                return (Actions.DROPOFF, Actions.DROP_NONE)
            # Trace your steps back home
            prevAction = self.toHome.pop()
            revAction = self.OppositeDir(prevAction)
            assert(isinstance(revAction, int))
            dx, dy = self.xy_from_dir(revAction)
            self.x += dx
            self.y += dy
            return (revAction, Actions.DROP_NONE)

        viewLen = len(view)
        score = 0
        # Run BFS to find closest resource

        # Search for resources
        # Updates self.targetPath, sefl.targetDest
        self.ViewScan(view)
        # self.view_resources_seen(view)


        
        # If you can't find any resources...go in a random direction!
        actionToTake = None
        if(self.targetPath == None):
            actionToTake = self.FindRandomPath(view)

        # Congrats! You have found a resource
        elif(self.targetPath == []):
            self.targetPath = None
            self.history.append(((self.x, self.y), 1))
            del self.history[0]
            return (Actions.MINE, Actions.DROP_NONE)
        else:
            # Use the first coordinate on the path as the destination , and action to move
            actionToTake = self.UpdateTargetPath()
  

        
        # clean home path
        next_loc = (0, 0) + self.xy_from_dir(actionToTake)
        if len(self.home_path) > 0:
            next_loc = self.home_path[-1] + self.xy_from_dir(actionToTake)

        self.toHome.append(actionToTake)
        self.home_path.append(next_loc)

        for i in range(0, len(self.home_path)):
            if self.home_path[i] == next_loc:
                del self.home_path[i+1:-1]
                del self.toHome[i+1:-1]
                break

        # markerDrop = random.choice([Actions.DROP_RED,Actions.DROP_YELLOW,Actions.DROP_GREEN,Actions.DROP_BLUE,Actions.DROP_ORANGE])
        markerDrop = Actions.DROP_NONE
        # if not self.view_resources_seen(view):
        #     markerDrop = Actions.DROP_RED
        assert(isinstance(actionToTake, int))
        dx, dy = self.xy_from_dir(actionToTake)
        self.x += dx
        self.y += dy
        self.history.append(((self.x, self.y), 0))
        del self.history[0]
        return (actionToTake, markerDrop)

    # Returns opposite direction
    def OppositeDir(self, prevAction):
        if(prevAction == Actions.MOVE_N):
            return Actions.MOVE_S
        elif(prevAction == Actions.MOVE_NE):
            return Actions.MOVE_SW
        elif(prevAction == Actions.MOVE_E):
            return Actions.MOVE_W
        elif(prevAction == Actions.MOVE_SE):
            return Actions.MOVE_NW
        elif(prevAction == Actions.MOVE_S):
            return Actions.MOVE_N
        elif(prevAction == Actions.MOVE_SW):
            return Actions.MOVE_NE
        elif(prevAction == Actions.MOVE_W):
            return Actions.MOVE_E
        elif(prevAction == Actions.MOVE_NW):
            return Actions.MOVE_SE
        else:
            return Actions.MOVE_S

    # Scans the entire view for resource searching
    # REQUIRES: view (see call location)
    def ViewScan(self, view):
        viewLen = len(view)
        queue = [[(0,0)]]
        deltas = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
        visited = set()
        visited.add((0,0))

        targetDepleted = (view[self.targetDest[0]][self.targetDest[1]][0].GetType() == TileType.Resource and
                         view[self.targetDest[0]][self.targetDest[1]][0].AmountRemaining() <= 0)

        # BFS TO find the next resource within your view
        if(self.targetPath == None or targetDepleted):
            while(len(queue)>0):
                path = queue[0]
                loc = path[0]
                queue = queue[1:]
                viewIndex = (loc[0] + viewLen//2,loc[1]+viewLen//2)
                if (view[viewIndex[0]][viewIndex[1]][0].GetType() == TileType.Resource and
                    view[viewIndex[0]][viewIndex[1]][0].AmountRemaining() > 0):
                    # print(path)
                    self.targetPath = path[1:]
                    self.targetDest = path[0]
                    return
                elif(view[viewIndex[0]][viewIndex[1]][0].CanMove()):
                    for i in range(8):
                        x = loc[0] + deltas[i][0]
                        y = loc[1] + deltas[i][1]
                        if(abs(x) <= viewLen//2 and abs(y) <= viewLen//2):
                            if((x,y) not in visited):
                                queue.append([(x,y)] + path[1:] + [deltas[i]])
                                visited.add((x,y))

        return

    def view_resources_seen(self, view):
        # First index is the resource
        # 
        # if view[len(view)//2][len(view)//2][0].GetType() == TileType.Resource:
        #     print(view[len(view)//2][len(view)//2][0].AmountRemaining())
        #     print(self.get_max_capacity(), self.get_pickup_amount(), self.storage_remaining())

        found = False
        for i in range(0, len(view)):
            for j in range(0, len(view)):
                if view[i][j][0].GetType() == TileType.Marker:
                    print(view[i][j][1].GetTurns())
        return found

    # Picks a random move based on the view - don't crash into mountains!
    # REQUIRES: view (see call location)
    def FindRandomPath(self, view):
        viewLen = len(view)

        # actionToTake = self.preferred_dir
        actions = [Actions.MOVE_E,Actions.MOVE_N,
                  Actions.MOVE_S,Actions.MOVE_W,
                  Actions.MOVE_NW,Actions.MOVE_NE,
                  Actions.MOVE_SW,Actions.MOVE_SE]
        random.shuffle(actions)

        if random.random() < 0.25:
            actions.insert(0, random.choice(actions))
        else:
            actions.insert(0, self.preferred_dir)

        for actionToTake in actions:
            
            if ((actionToTake == Actions.MOVE_N and view[viewLen//2-1][viewLen//2][0].CanMove()) or
               (actionToTake == Actions.MOVE_S and view[viewLen//2+1][viewLen//2][0].CanMove()) or
               (actionToTake == Actions.MOVE_E and view[viewLen//2][viewLen//2+1][0].CanMove()) or
               (actionToTake == Actions.MOVE_W and view[viewLen//2][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_NW and view[viewLen//2-1][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_NE and view[viewLen//2-1][viewLen//2+1][0].CanMove()) or
               (actionToTake == Actions.MOVE_SW and view[viewLen//2+1][viewLen//2-1][0].CanMove()) or
               (actionToTake == Actions.MOVE_SE and view[viewLen//2+1][viewLen//2+1][0].CanMove()) ):
               return actionToTake

            # actionToTake = random.choice([Actions.MOVE_E,Actions.MOVE_N,
            #                               Actions.MOVE_S,Actions.MOVE_W,
            #                               Actions.MOVE_NW,Actions.MOVE_NE,
            #                               Actions.MOVE_SW,Actions.MOVE_SE])

        return None

    # Returns actionToTake
    # REQUIRES: self.targetPath != []
    def UpdateTargetPath(self):
        actionToTake = None
        (x, y) = self.targetPath[0]

        if(self.targetPath[0] == (1,0)):
            actionToTake = Actions.MOVE_S
        elif(self.targetPath[0] == (1,1)):
            actionToTake = Actions.MOVE_SE
        elif(self.targetPath[0] == (0,1)):
            actionToTake = Actions.MOVE_E
        elif(self.targetPath[0] == (-1,1)):
            actionToTake = Actions.MOVE_NE
        elif(self.targetPath[0] == (-1,0)):
            actionToTake = Actions.MOVE_N
        elif(self.targetPath[0] == (-1,-1)):
            actionToTake = Actions.MOVE_NW
        elif(self.targetPath[0] == (0,-1)):
            actionToTake = Actions.MOVE_W
        elif(self.targetPath[0] == (1,-1)):
            actionToTake = Actions.MOVE_SW

        # Update destination using path
        self.targetDest = (self.targetDest[0]-x, self.targetDest[1]-y)
        # We will continue along our path    
        self.targetPath = self.targetPath[1:]

        return actionToTake

    def xy_from_dir(self, actionToTake):
        if(actionToTake == Actions.MOVE_S):
            return (1, 0)
        elif(actionToTake == Actions.MOVE_SE):
            return (1, 1)
        elif(actionToTake == Actions.MOVE_E):
            return (0, 1)
        elif(actionToTake == Actions.MOVE_NE):
            return (-1, 1)
        elif(actionToTake == Actions.MOVE_N):
            return (-1, 0)
        elif(actionToTake == Actions.MOVE_NW):
            return (-1,-1)
        elif(actionToTake == Actions.MOVE_W):
            return (0, -1) 
        elif(actionToTake == Actions.MOVE_SW):
            return (1, -1)       
        else:
            return (0, 0)
