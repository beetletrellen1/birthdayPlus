from calendar import day_abbr, month
import random
import numpy as np
import pandas as pd
from collections import Counter
from datetime import date
import plotly.express as px

class Birthday:

    def __init__(self, seed, num_trials, min_people, max_people, n_share_bday, 
                    possible_days = 366):
        self.seed = int(seed)
        self.num_trials = num_trials
        self.min_people = min_people
        self.max_people = max_people
        self.shared_bday = n_share_bday
        self.num_possible_bdays = possible_days
        self.trial_list =[]
        self.has_coincidence = []
        self.probability = []
        self.df = None
        self.fig = None

    def generate_random_birthday(self):
        return np.random.randint(1, self.num_possible_bdays)

    def generate_k_birthdays(self, k):
        return [self.generate_random_birthday() for _ in range(k)]

    def x_people_share_bday(self, birthdays, x=2):
        unique_birthdays = Counter(birthdays)
        return any(same_bday >= x for same_bday in unique_birthdays.values())

    def estimate_p_coincidence(self, idx, people=None):
        if people == None:
            people = self.max_people

        birthdays = self.generate_k_birthdays(people)
        has_coincidence = self.x_people_share_bday(birthdays, x=self.shared_bday)
        self.has_coincidence.append(has_coincidence)
        self.calc_p()

    def calc_p(self):
        self.probability.append(sum(self.has_coincidence) / len(self.has_coincidence))


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
        
        while self.probability[-1] < threshold:
            num_people += 1
            for _ in range(self.num_trials):
                birthdays = self.generate_k_birthdays(num_people)
                self.has_coincidence.append(self.my_birthday_coincidence(birthdays))
                self.calc_p()


class WeightedBirthdays(Birthday):

    def create_df(self):
        self.df = pd.read_csv("https://raw.githubusercontent.com/fivethirtyeight/data/master/births/US_births_1994-2003_CDC_NCHS.csv")

    def group_bday_by_day(self):
        self.avg_bday_df = self.df.groupby(['month', 'date_of_month']).agg({'births': np.mean}).reset_index()

    def create_heat_map(self):
        self.month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.heat_df = self.avg_bday_df.pivot(index='month', columns='date_of_month')['births']
        fig = px.imshow(self.heat_df, labels=dict(x="Day of Month", y="Month"),
                                x=[str(i+1) for i in range(31)],
                                y=self.month_labels,
                                color_continuous_scale='RdBu_r', 
                                title="Average Birthdays by Day")
        fig.update_xaxes(side="top")
        return fig
    
    def create_bday_weight(self):
        total_births = np.sum(self.avg_bday_df['births'])
        self.birth_weight = [birth / total_births for birth in self.avg_bday_df['births']]

    def generate_random_birthday(self):
        return random.choices(range(1, 367), weights=self.birth_weight, k=1)[0]

if __name__ == "__main__":
    bday = WeightedBirthdays(seed=1, num_trials=100, min_people=10, max_people=40, n_share_bday=3, 
                    possible_days = 366)
    bday.create_df()
    bday.group_bday_by_day()
    bday.create_bday_weight()
    for idx, _ in enumerate(range(100)):
        bday.estimate_p_coincidence(idx=idx)
        bday.trial_list.append(idx)
        p_coincidence = bday.probability[-1]
    print(p_coincidence)