from enum import Enum



class TypeOfHistory(Enum):
    room = "room"
    group = "group"
    teacher = "teacher"
    
    @classmethod
    def choices(cls):
        return [(i.name, i.value) for i in cls]
    
        
    