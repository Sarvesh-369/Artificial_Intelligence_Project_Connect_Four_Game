#!/usr/bin/env python3
from FourConnect import * # See the FourConnect.py file
import csv

class GameTreePlayer:
    
    def __init__(self, depth=4): # Adjust the depth parameter based on the search depth you desire
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
            
            if board_value > best_value:
                best_value = board_value
                best_move = action
            alpha = max(alpha, best_value)

        return best_move

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

        score = 0

        # Emphasizing on potential winning moves
        score += 5000 * count_sets_of_length(state, 4, 2)
        
        # Potential moves which could result in a win in the next move
        score += 200 * count_sets_of_length(state, 3, 2)
        
        # Basic alignment which can potentially lead to a win
        score += 50 * count_sets_of_length(state, 2, 2)
        
        # Prioritizing blocking the opponent from winning
        score -= 4000 * count_sets_of_length(state, 4, 1)
        
        # Blocking moves which could let the opponent win in the next move
        score -= 150 * count_sets_of_length(state, 3, 1)
        
        # Opponent alignments which may not be immediate threats but can be in the future
        score -= 40 * count_sets_of_length(state, 2, 1)

        return score

    def get_possible_moves(self, state):
        # Returns a list of valid columns where a coin can be inserted
        moves = []
        for col in range(7):
            if state[0][col] == 0: # Check if the top-most cell of the column is empty
                moves.append(col)
        return moves

    def play_move(self, state, action, player):
        # Play a move in the specified column for the given player and update the state
        for row in range(5, -1, -1):  # Start from the bottom row
            if state[row][action] == 0:
                state[row][action] = player
                break


def LoadTestcaseStateFromCSVfile():
    testcaseState=list()

    with open('testcase.csv', 'r') as read_obj: 
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
    
    """
    You can add your code here to count the number of wins average number of moves etc.
    You can modify the PlayGame() function to play multiple games if required.
    """
    if fourConnect.winner==None:
        print("Game is drawn.")
    else:
        print("Winner : Player {0}\n".format(fourConnect.winner))
    print("Moves : {0}".format(move))

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
    
    print("Roll no : 2020B5A71839G") #Put your roll number here
    
    if fourConnect.winner==2:
        print("Player 2 has won. Testcase passed.")
    else:
        print("Player 2 could not win in 5 moves. Testcase failed.")
    print("Moves : {0}".format(move))
    

def main():
    
    PlayGame()
    """
    You can modify PlayGame function for writing the report
    Modify the FindBestAction in GameTreePlayer class to implement Game tree search.
    You can add functions to GameTreePlayer class as required.
    """

    """
        The above code (PlayGame()) must be COMMENTED while submitting this program.
        The below code (RunTestCase()) must be UNCOMMENTED while submitting this program.
        Output should be your rollnumber and the bestAction.
        See the code for RunTestCase() to understand what is expected.
    """
    
    # RunTestCase()


if __name__=='__main__':
    main()
