from enum import Enum


class Sections(Enum):
    managers = 'managers'
    education = 'education'
    accounting = 'accounting'
    marketing = 'marketing'
    
    
    @classmethod
    def choices(cls):
        return ((i.name, i.value) for i in cls)


class ProfileRoles(Enum):
    director = 'director'
    teacher  = 'teacher'
    mentor = 'mentor'
    student = 'student'
    parent = 'parent'
    manager = 'manager'
    hr_manager = 'hr_manager'   
    administrator = 'administrator'
    marketer = 'marketer'
    accountant = 'accountant'
    cashier = 'cashier'
    developer = 'developer'

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Regions(Enum):
    tashkent = 'Toshkent'
    samarkand = 'Samarqand'
    andijan = 'Andijon'
    fargona = 'Fargona'
    namangan = 'Namangan'
    qashqadaryo = 'Qashqadaryo'
    surxondaryo = 'Surxondaryo'
    buxoro = 'Buxoro'
    navoiy = 'Navoiy'
    xorazm = 'Xorazm'
    sirdaryo = 'Sirdaryo'
    jizzax = 'Jizzax'
    qoraqalpoq = 'Qoraqalpog\'iston Respublikasi'
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)



class Gender(Enum):
    man = 'man'
    woman = 'woman'
    
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)