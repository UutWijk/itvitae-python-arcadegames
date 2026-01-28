import json
import os

class HighScore:
    def __init__(self, filename='highscores.json'):
        self.filename = filename
        self.highscore = self._load()

    def _load(self): #private function - #Load highscore from file
        if os.path.exists(self.filename): 
            try:
                with open(self.filename, 'r') as file: # r = read-only
                    data = json.load(file)
                    #loads highscore and returns 0 if it does not exist
                    return data.get('highscore', 0) #
            except:
                return 0 #safety measure for corrupted file
        return 0 
    
    def _save(self): #private function
        with open(self.filename, 'w') as file: # w = write
            json.dump({'highscore': self.highscore}, file)
            # Debug:
            print(f"High score saved to: {os.path.abspath(self.filename)}")
                
    def update(self, score): # True if new score is highscore, False if not
        if score > self.highscore:
            self.highscore = score
            self._save()
            return True
        return False

    def get_highscore(self):
        return self.highscore
    
    # maybe add a hi-score reset later?
    # def reset(self)
    #     self.highscore = 0
    #     self._save()