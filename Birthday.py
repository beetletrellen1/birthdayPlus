from calendar import day_abbr, month
import numpy as np
from collections import Counter
from datetime import date

class Birthday:

    def __init__(self, seed, num_trials, min_people, max_people, n_share_bday, 
                    possible_days = 365):
        self.seed = int(seed)
        self.num_trials = num_trials
        self.min_people = min_people
        self.max_people = max_people
        self.shared_bday = n_share_bday
        self.num_possible_bdays = possible_days


    def generate_random_birthday(self):
        return np.random.randint(1, self.num_possible_bdays)

    def generate_k_birthdays(self, k):
        return [self.generate_random_birthday() for _ in range(k)]

    def x_people_share_bday(self, birthdays, x=2):
        unique_birthdays = Counter(birthdays)
        return any(same_bday >= x for same_bday in unique_birthdays.values())

    def estimate_p_coincidence(self, people=None):
        np.random.seed(self.seed)
        if people == None:
            people = self.max_people

        num_coincidence = 0
        for _ in range(self.num_trials):
            birthdays = self.generate_k_birthdays(people)
            has_coincidence = self.x_people_share_bday(birthdays, x=self.shared_bday)
            if has_coincidence:
                num_coincidence += 1
        
        return num_coincidence / self.num_trials


class MyBirthday(Birthday):

    def __init__(self, month, day):
        self.month = month
        self.day = day
        self.year = 2023

    def my_birthday(self):
        jan_1 = date(self.year, 1, 1)
        birthday = date(self.year, self.month, self.day)
    
        return (birthday - jan_1).days

    def my_birthday_coincidence(self, birthdays):
        my_birthday = self.my_birthday()
    
        if my_birthday in birthdays:
            return True
        else: 
            return False

    def estimate_p_share_my_birthday(self, threshold = 0.1):
        num_people = 1
        p_share = [0]
        
        while p_share[-1] < threshold:
            num_people += 1
            num_coincidence = 0
            for _ in range(self.num_trials):
                birthdays = self.generate_k_birthdays(num_people)
                has_coincidence = self.my_birthday_coincidence(birthdays)
                if has_coincidence:
                    num_coincidence += 1

            p_coincidence = num_coincidence / self.num_trials
            p_share.append(p_coincidence)
        return p_share