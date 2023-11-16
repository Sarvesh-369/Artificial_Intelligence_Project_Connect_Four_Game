#!/usr/bin/env python3
from FourConnect import * # See the FourConnect.py file
import csv
import time
class GameTreePlayer:
    
    def __init__(self, depth=5): # Adjust the depth parameter based on the search depth you desire
        self.depth = depth
        self.game = FourConnect()
    
    # def FindBestAction(self,currentState):
    #     """
    #     Modify this function to search the GameTree instead of getting input from the keyboard.
    #     The currentState of the game is passed to the function.
    #     currentState[0][0] refers to the top-left corner position.
    #     currentState[5][6] refers to the bottom-right corner position.
    #     Action refers to the column in which you decide to put your coin. The actions (and columns) are numbered from left to right.
    #     Action 0 is refers to the left-most column and action 6 refers to the right-most column.
    #     """
        
    #     bestAction = input("Take action (0-6) : ")
    #     bestAction = int(bestAction)
    #     return bestAction
    def FindBestAction(self, state):
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for action in self.get_possible_moves(state):
            simulated_state = copy.deepcopy(state)
            self.play_move(simulated_state, action, 2)
            board_value = self.minimax(simulated_state, self.depth-1, False, alpha, beta)
            # board_value = self.minimax(simulated_state, self.depth-1, False)
            
            if board_value > best_value:
                best_value = board_value
                best_move = action
            alpha = max(alpha, best_value)

        return best_move

###############################################################################################
#   MIN MAX WITHOUT ALPHA BETA PRUNING
###############################################################################################
    # def minimax(self, state, depth, is_maximizing):
    #     if depth == 0:
    #         return self.evaluate(state)

    #     if is_maximizing:
    #         max_eval = float('-inf')
    #         for action in self.get_possible_moves(state):
    #             simulated_state = copy.deepcopy(state)
    #             self.play_move(simulated_state, action, 2)
    #             eval = self.minimax(simulated_state, depth-1, False)
    #             max_eval = max(max_eval, eval)
    #         return max_eval
    #     else:
    #         min_eval = float('inf')
    #         for action in self.get_possible_moves(state):
    #             simulated_state = copy.deepcopy(state)
    #             self.play_move(simulated_state, action, 1)
    #             eval = self.minimax(simulated_state, depth-1, True)
    #             min_eval = min(min_eval, eval)
    #         return min_eval
###############################################################################################
#   MIN MAX WITH ALPHA BETA PRUNING
###############################################################################################
    def minimax(self, state, depth, is_maximizing, alpha, beta):
        if depth == 0:
            return self.evaluate(state)

        if is_maximizing:
            max_eval = float('-inf')
            for action in self.get_possible_moves(state):
                simulated_state = copy.deepcopy(state)
                self.play_move(simulated_state, action, 2)
                eval = self.minimax(simulated_state, depth-1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for action in self.get_possible_moves(state):
                simulated_state = copy.deepcopy(state)
                self.play_move(simulated_state, action, 1)
                eval = self.minimax(simulated_state, depth-1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
        
    def evaluate(self, state):
        def count_sets_of_length(board, length, player):
            count = 0
            for row in range(6):
                for col in range(7):
                    # Check horizontally
                    if col + length <= 7 and all([board[row][c] == player for c in range(col, col+length)]):
                        count += 1
                    # Check vertically
                    if row + length <= 6 and all([board[r][col] == player for r in range(row, row+length)]):
                        count += 1
                    # Check positively sloped diagonals
                    if col + length <= 7 and row + length <= 6 and all([board[row+r][col+c] == player for r, c in zip(range(length), range(length))]):
                        count += 1
                    # Check negatively sloped diagonals
                    if col - length >= -1 and row + length <= 6 and all([board[row+r][col-c] == player for r, c in zip(range(length), range(length))]):
                        count += 1
            return count

        def calculate_center_control(board, player):
            center_column = [board[row][3] for row in range(6)]
            center_count = center_column.count(player)
            return center_count * 3  # Assign a small score for each piece in the center

        score = 0
###############################################################################################
#   EVALUATION FUNCTION 1
###############################################################################################

        # #Player 2's winning lines
        # score += 1000 * count_sets_of_length(state, 4, 2)  

        # #Player 1's winning lines
        # score -= 500 * count_sets_of_length(state, 4, 1)   

##################################################################################################
#   EVALUATION FUNCTION 2
##################################################################################################

        # # Emphasizing on potential winning moves for player 2
        # score += 5000 * count_sets_of_length(state, 4, 2)
        
        # #Potential moves which could result in a win for player 2 in the next move
        # score += 200 * count_sets_of_length(state, 3, 2)
        
        # #Basic alignment which can potentially lead to a win for player 2
        # score += 50 * count_sets_of_length(state, 2, 2)

        # #Prioritizing blocking the opponent from winning
        # score -= 4000 * count_sets_of_length(state, 4, 1)
        
        # #Blocking moves which could let the opponent win in the next move
        # score -= 150 * count_sets_of_length(state, 3, 1)
        
        # #Opponent alignments which may not be immediate threats but can be in the future
        # score -= 40 * count_sets_of_length(state, 2, 1)

##################################################################################################
#   EVALUATION FUNCTION 3
##################################################################################################

        # # Emphasizing on potential winning moves for player 2
        # score += 5000 * count_sets_of_length(state, 4, 2)
        
        # # Potential moves which could result in a win for player 2 in the next move
        # score += 200 * count_sets_of_length(state, 3, 2)
        
        # # Basic alignment which can potentially lead to a win for player 2
        # score += 50 * count_sets_of_length(state, 2, 2)
        
        # # Blocking the opponent when they are about to win
        # if count_sets_of_length(state, 4, 1) > 0:
        #     score -= 10000
        
        # # Blocking moves which could let the opponent win in the next move
        # if count_sets_of_length(state, 3, 1) > 0:
        #     score -= 1000
        
        # # Opponent alignments which may not be immediate threats but can be in the future
        # score -= 40 * count_sets_of_length(state, 2, 1)

##################################################################################################
#   EVALUATION FUNCTION 4
##################################################################################################
        # Central control
        score += calculate_center_control(state, 2)
        score -= calculate_center_control(state, 1)

        # Immediate win
        score += 10000 * count_sets_of_length(state, 4, 2)
        score -= 10000 * count_sets_of_length(state, 4, 1)

        # Potential win in the next move
        score += 4000 * count_sets_of_length(state, 3, 2)
        score -= 4000 * count_sets_of_length(state, 3, 1)

        # Two in a row (flexibility)
        score += 50 * count_sets_of_length(state, 2, 2)
        score -= 50 * count_sets_of_length(state, 2, 1)

        # Empty spaces below potential connect-3 situations for player 2
        for col in range(7):
            for row in range(6):
                if state[row][col] == 0:
                    if row + 1 < 6 and state[row + 1][col] == 2:
                        if count_sets_of_length(state, 3, 2) > 0:
                            score += 100  # Encourage stacking to create connect-4
##################################################################################################        
        return score
##################################################################################################

    def get_possible_moves(self, state):
        # Returns a list of valid columns where a coin can be inserted
        # moves = []
        # for col in range(7):
        #     if state[0][col] == 0: # Check if the top-most cell of the column is empty
        #         moves.append(col)
        # return moves
##################################################################################################
#   MOVE ORDERING 1
##################################################################################################
        # preferred_order_2 = [6 ,5, 4, 3, 2, 1, 0]
        # moves = [col for col in preferred_order_2 if state[0][col] == 0]
        # return moves          
##################################################################################################
#   MOVE ORDERING 2
##################################################################################################
        #heuristic: prefer center columns
        preferred_order_3 = [3, 2, 4, 1, 5, 0, 6]
        moves = [col for col in preferred_order_3 if state[0][col] == 0]
        return moves
##################################################################################################
#   MOVE ORDERING 3
##################################################################################################
        # preferred_order_1 = [0 ,1, 2, 3, 4, 5, 6]
        # moves = [col for col in preferred_order_1 if state[0][col] == 0]
        # return moves   

    def play_move(self, state, action, player):
        # Play a move in the specified column for the given player and update the state
        for row in range(5, -1, -1):  # Start from the bottom row
            if state[row][action] == 0:
                state[row][action] = player
                break


def LoadTestcaseStateFromCSVfile():
    testcaseState=list()

    with open('testcase_new.csv', 'r') as read_obj: 
       	csvReader = csv.reader(read_obj)
        for csvRow in csvReader:
            row = [int(r) for r in csvRow]
            testcaseState.append(row)
        return testcaseState


def PlayGame():
    fourConnect = FourConnect()
    fourConnect.PrintGameState()
    gameTree = GameTreePlayer()
    
    move=0
    while move<42: #At most 42 moves are possible
        if move%2 == 0: #Myopic player always moves first
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break

    if fourConnect.winner==None:
        print("Game is drawn.")
    else:
        print("Winner : Player {0}\n".format(fourConnect.winner))
    print("Moves : {0}".format(move))
    return fourConnect.winner,move
def RunTestCase():
    """
    This procedure reads the state in testcase.csv file and start the game.
    Player 2 moves first. Player 2 must win in 5 moves to pass the testcase; Otherwise, the program fails to pass the testcase.
    """
    
    fourConnect = FourConnect()
    gameTree = GameTreePlayer()
    testcaseState = LoadTestcaseStateFromCSVfile()
    fourConnect.SetCurrentState(testcaseState)
    fourConnect.PrintGameState()

    move=0
    while move<5: #Player 2 must win in 5 moves
        if move%2 == 1: 
            fourConnect.MyopicPlayerAction()
        else:
            currentState = fourConnect.GetCurrentState()
            gameTreeAction = gameTree.FindBestAction(currentState)
            fourConnect.GameTreePlayerAction(gameTreeAction)
        fourConnect.PrintGameState()
        move += 1
        if fourConnect.winner!=None:
            break
    
    if fourConnect.winner==2:
        print("Player 2 has won. Testcase passed.")
    else:
        print("Player 2 could not win in 5 moves. Testcase failed.")
    print("Moves : {0}".format(move))
    

def main():
    start_time = time.time()
    count = 0
    count1 = 0
    for i in range(50):
        winner,moves = PlayGame()
        if winner == 2:
            count = count + moves
            count1=count1+1
    win_percentage = (count1 / 50) * 100
    average_moves = count / count1 if count1 else 0  # Check to avoid division by zero
    print("On running 50 Games the results are")
    print(f"Average number of times player 2 win = {win_percentage:.2f} %")
    print(f"Average number of moves moves player 2 win = {average_moves:.2f}")
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total execution time: {total_time:.2f} seconds")
    
    # RunTestCase()


if __name__=='__main__':
    main()
