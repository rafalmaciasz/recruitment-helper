import numpy as np
class Fuzzy_Numb:
    def __init__(self, a : float, b : float, c : float) -> None:
        self.a = a
        self.b = b
        self.c = c
        pass

    def d(self,other) -> float:
        """
        return
            distance between two trangular fuzzy numbers 
        """
        return np.sqrt(1/3*[(self.a-other.a)**2+(self.b-other.b)**2+(self.c-other.c)**2])

    def normalised_benefit_criteria(self, c_star):
        """
        return 
            normalized over benefit criteria triangular fuzzy number
        """
        return Fuzzy_Numb(self.a/c_star,self.b/c_star,self.c/c_star)

    def normalised_cost_criteria(self, a_minus):
        """
        return 
            normalized over cost criteria triangular fuzzy number
        """
        return Fuzzy_Numb(a_minus/self.a,a_minus/self.b,a_minus/self.c)
    
    def __mul__(self,other):
        return Fuzzy_Numb(self.a*other.a, self.b*other.b, self.b*other.b)

    def __gt__(self,other):
        if self.c>other.c:
            return True
        elif self.c<other.c:
            return False
        elif self.b>other.b:
            return True
        elif self.b<other.b:
            return False
        elif self.a>other.a:
            return True
        else:
            return False

    def __lt__(self,other):
        if self.a<other.a:
            return True
        elif self.a>other.a:
            return False
        elif self.b<other.b:
            return True
        elif self.b>other.b:
            return False
        elif self.c<other.c:
            return True
        else:
            return False
        
