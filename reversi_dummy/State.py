import numpy as np
player_name={
    1: "WHITE",
    2: "BLACK"}

class State:
    """ Zachycení stavu partie
    gameplan - dvourozměrné numpy pole 8x8
             - 0 - prázdné pole
             - 1 - bílý kámen
             - 2 - černý kámen
    player - hráč, který je v partii na tahu

    current_player - hráč, který je na tahu v daném stavu při prohledávání stavového prostoru
    depth          - hloubka prohledávání stavového prostoru
    """

    generated = 0

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    def __init__(self, gameplan, player, current_player=None, depth=0, max_depth=3):
        self.gameplan = gameplan
        self.player = player
        if current_player is None:
            self.current_player = player
        else:
            self.current_player = current_player
        self.depth = depth
        self.max_depth = max_depth
        
        State.generated += 1
        
    def terminal_test(self):
        """ Otestuje, zda je partie dohraná:
            1. Není volné pole.
            2. Žádný hráč nemá tah.
        """
        
        # Žádné volné pole
        if not np.any(self.gameplan == 0):  
            return True

        # Žádný hráč nemá tah
        if not self.possible_actions() and not State(self.gameplan, self.next_current_player()).possible_actions():
            return True  
                        
        return False    
        
    def score(self):
        """ Metoda vrací počet bílý a černých kamenů 
        """
        white_count = np.sum(self.gameplan == 1)
        black_count = np.sum(self.gameplan == 2)
        return white_count, black_count       
                
    def winner(self):
        """
            Zjištění vítěze partie
            0 - remíza
            1 - bílý
            2 - černý
        """
        white_stones, black_stones = self.score()
        if white_stones == black_stones:
            return 0
        elif white_stones > black_stones:
            return 1
        else:
            return 2

    def next_player(self):
        """ Metoda vrátí protihráče
        """
        return 3 - self.player
        
    def next_current_player(self):
        """ Metoda vrátí protihrače pro procházení stavového prostoru
        """
        return 3 - self.current_player

    def possible_actions(self):
        """ 1. Platný tah začíná na prázdném poli
            2. Na sousedním poli je protihráčův kámen
            3. Pokud ho najdu, pokračuji daným směrem a stále nacházím soupeřovi kameny
            4. Ve chvíli, kdy skončí soupeřovi kameny, musí následovat hráčův kámen
            5. Nesmím opustit hrací pole
        """
        actions = []
        opponent = self.next_current_player()
        
        # Ověření všech hracích polí
        for x in range(8):
            for y in range(8):
                if self.gameplan[x][y] != 0:
                    # Políčko není prázdné
                    continue
        
                # Ověření všech směrů        
                for dx, dy in self.directions:
                    nx, ny = x + dx, y + dy
                    found_opponent = False
                    
                    while 0 <= nx < 8 and 0 <= ny < 8 and self.gameplan[nx][ny] == opponent:
                        found_opponent = True
                        nx += dx
                        ny += dy
                    
                    if found_opponent and 0 <= nx < 8 and 0 <= ny < 8 and self.gameplan[nx][ny] == self.current_player:
                        # Alespoň v jednom směru se našel platný tah
                        actions.append((x, y))
                        break  
        return actions

    def expand(self, action):
        """ Provedení tahu
            1. Vytvořím kopii stavu
            2. Polož kámen na vybrané pole
            3. Prověř všechny směry, kdy si poznamenáš všechny pozice soupeřových kamenů, které se zamění
        """ 
        new_gameplan = np.copy(self.gameplan)
        x, y = action
        new_gameplan[x][y] = self.player
        
        opponent = self.next_player()
        
        # prozkoumání všech směrů
        for dx, dy in self.directions:
            nx, ny = x + dx, y + dy
            
            stones_to_flip = []
            while 0 <= nx < 8 and 0 <= ny < 8 and new_gameplan[nx][ny] == opponent:
                stones_to_flip.append((nx, ny))
                nx += dx
                ny += dy
            
            # kameny se otáčí, pokud jsou uzavřeny hráčovým kamenem
            if stones_to_flip and 0 <= nx < 8 and 0 <= ny < 8 and new_gameplan[nx][ny] == self.player:
                for fx, fy in stones_to_flip:
                    new_gameplan[fx][fy] = self.player
                    
        return State(new_gameplan, 
                     self.current_player,        # zkoumám stále partii z pohledu hráče na tahu, proto ho neměním
                     self.next_current_player(),   # v další vrstvě stromu bude na tahu druhý hráč
                     self.depth + 1, 
                     max_depth=self.max_depth)

    def utility(self):
        """ Metoda vrací ohodnocení aktuálního stavu partie
            0  - remíza
            <0  - vítězí hráč, který je na tahu
            >0 - vítězí protihráč
        """
        white_stones, black_stones = self.score()
        if self.current_player == 1:
            return white_stones - black_stones
        else:
            return black_stones - white_stones
            
    def minmax(self, strategy="max"):
        """"
        Metoda vybere z možných akcí pro daný stav partie tu, která odpovídá strategii

        stategy - jaká strategie se bude používat pro výběr z možných akcí
        """
        
        # kontrola stavu partie, pro ukončenou partii se vrací hodnocení z utility metody
        if self.terminal_test():
            return self.utility(), None
                        
        # kontrola, zda je možný tah    
        actions = self.possible_actions()
        if len(actions) == 0:
            return self.utility(), None            
        
        # inicializace hodnot pro jednotlivé strategie
        if strategy == "max":
            selected_utilization_value = float('-inf')
            next_strategy = "min"
        else:
            selected_utilization_value = float('inf')
            next_strategy = "max"

        # vybraný tah se naplní prvním tahem z možných akcí
        selected_action = actions[0]
        
        # TODO - aplikujte vlastní algoritmus výběru tahu
        for action in actions:
            # expanze stavu
            expanded_state = self.expand(action)
            utilization = expanded_state.utility()
            
            # podle strategie se ohodnocená akce volí jako vybraná akce
            if utilization > selected_utilization_value and strategy == "max":
                selected_utilization_value = utilization
                selected_action = action
            elif utilization < selected_utilization_value and strategy == "min":
                selected_utilization_value = utilization
                selected_action = action

        return selected_utilization_value, selected_action