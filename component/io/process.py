# It is strongly suggested to us a separate file to define the io of your tile and process. 
# it will help you to have control over it's fonctionality using object oriented programming

# in python variable are not mutable object (their value cannot be changed in a function)
# Thus use a class to define your input and output in order to have mutable variables
class Process:
    def __init__(self):
        
        # set up your inputs
        self.start = None
        self.end = None
        self.l8 = False
        self.l7 = False
        self.l5 = False
        self.l4 = False
        self.t2 = False
        self.s2 = False
        self.sr = False
        self.measure = 'pixel_count'
        self.annual = False
        
        # set up your outputs
        self.asset_id = None
        self.dataset  = None