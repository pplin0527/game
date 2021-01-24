import numpy as np 

class Game_2A2B:
    def __init__(self):
        self.answer_store = [1, 2, 3, 4, 5, 6] # All possible answers
        self.n = 4
        self.replace = False

    def _generate_answer(self) -> np.array:    
        # Random pick N answers from answer store 
        answer = np.random.choice(self.answer_store, self.n, self.replace)
        return answer
    
    
    def _user_guess(self) -> list:
        try:
            guess = input("Please enter a {} digit number: ".format(self.n))
            # Turn into list of integer
            guess = list(map(int, guess)) 
        except:
            print("please enter a number")
            
        return guess 

    def _check_answer(self, guess: list, answer: np.array) -> dict:
        # Result dict 
        result = {"a": 0, "b": 0}
        
        # Check A 
        for i, j in zip(guess, answer):
            if i == j:
                result['a'] += 1

        # Check B
        for i in guess:
            if i in answer:
                result['b'] += 1

        # B = # of B - # of A (minus right index)
        result['b'] = result['b'] - result['a']

        # Check if it's 4A 4b
        if result == {"a": 4, "b": 0}:
            game_end = True
        else:
            game_end = False
        
        
        result = "{a}A{b}B".format(guess = str(guess), a=result["a"], b=result["b"])
       
        return result, game_end

if __name__ == '__main__':
    # Start a game and generate random result
    game = Game_2A2B()
    answer = game._generate_answer()

    print("Guess {n} numbers from this list\n{answer_store}\n".format(n = game.n, answer_store=game.answer_store) )
    
    # Start game     
    game_flag = False
    
    while game_flag == False:
        # Guess - user input 
        guess = game._user_guess()
        # Check result 
        result, game_flag = game._check_answer(guess, answer)
        print(result)
        

        if game_flag == True:
            print("4A0B. Congrats!!")
            break         