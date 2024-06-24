import os
import json
import csv

import time

class SUTIngestor:
    def __init__(self, csv_path: str):
        self.data = self.read_csv(csv_path)
        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of moderate-intensity aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical activity and engage in muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of moderate-intensity aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening activities on 2 or more days a week',
        ]
    
    def read_csv(self, csv_path):
        with open(csv_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
            return data
        
    # Functie auxiliara ce ne ajuta sa selectam doar randurile ce ne raspund la intrebarea noastra.
    def get_question_rows(self, question):
        question_rows = []
        for row in self.data:
            if row['Question'] == question:
                question_rows.append(row)
        return question_rows
    
    # Primește o întrebare (din setul de întrebări de mai sus) și 
    # calculează media valorilor înregistrate (Data_Value) din intervalul total de timp 
    # (2011 - 2022) pentru fiecare stat, și sortează crescător după medie.
    # Returneaza dictionar de forma {Stat1 : medie1, Stat2: medie2...}
    def calculate_states_mean(self, question):
        state_values = {}
        state_means = {}
        for row in self.get_question_rows(question):
                state = row['LocationDesc']
                value = float(row['Data_Value'])
                # Daca nu exista cheia, initializam lista
                if state not in state_values:
                    state_values[state] = []
                state_values[state].append(value)
        for state, values in state_values.items():
            state_means[state] = sum(values) / len(values)
        return state_means
    
    # Functie auxiliara care calculeaza media unui stat
    # si o returneaza ca numar pt a fi folosit in calculul
    # celorlalte request-uri
    def get_state_mean(self, state, question):
        state_values = []
        for row in self.get_question_rows(question):
            if row['LocationDesc'] == state:
                value = float(row['Data_Value'])
                state_values.append(value)
        if not state_values:
            return 0
        return sum(state_values) / len(state_values)
    
    # Primește o întrebare (din setul de întrebări de mai sus) și un stat, 
    # și calculează media valorilor înregistrate (Data_Value) din intervalul 
    # total de timp (2011 - 2022). 
    # Returneaza dictionar de forma {Stat: medie}.
    def calculate_state_mean(self, state, question):
        return {state: self.get_state_mean(state, question)}
    
    # Primește o întrebare (din setul de întrebări de mai sus) și calculează
    # media valorilor înregistrate (Data_Value) din intervalul total de timp 
    # (2011 - 2022) și întoarce primele 5 state.
    # Returneaza dictionar de forma {Stat1: medie1, Stat2: medie2, ... , Stat5: medie5}.
    def calculate_best5_states(self, question):
        state_means = self.calculate_states_mean(question)
        if question in self.questions_best_is_min:
            sorted_states = sorted(state_means, key=state_means.get)
        else:
            sorted_states = sorted(state_means, key=state_means.get, reverse=True)
        best5_states = {state: state_means[state] for state in sorted_states[:5]}
        return best5_states
    
    # Primește o întrebare (din setul de întrebări de mai sus) și calculează
    # media valorilor înregistrate (Data_Value) din intervalul total de timp
    # (2011 - 2022) și întoarce ultimele 5 state.
    # Returneaza dictionar de forma {Stat1: medie1, Stat2: medie2, ... , Stat5: medie5}.
    def calculate_worst5_states(self, question):
        state_means = self.calculate_states_mean(question)
        if question in self.questions_best_is_min:
            sorted_states = sorted(state_means, key=state_means.get, reverse=True)
        else:
            sorted_states = sorted(state_means, key=state_means.get)
        worst5_states = {state: state_means[state] for state in sorted_states[:5]}
        return worst5_states
    
    # Functie auxiliara care calculeaza media pe intreg setul de date,
    # nu doar pe un stat. Returneaza valoarea ca nr pentru a putea fi folosit
    # in celelalte requesturi.
    def get_global_mean(self, question):
        question_values = []
        for row in self.get_question_rows(question):
                value = float(row['Data_Value'])
                question_values.append(value)
        return sum(question_values) / len(question_values)

    # Primește o întrebare (din setul de întrebări de mai sus) și calculează media
    # valorilor înregistrate (Data_Value) din intervalul total de timp (2011 - 2022)
    # din întregul set de date.
    # Returneaza dictionar de forma {global_mean: medie}.
    def calculate_global_mean(self, question):
        return {"global_mean": self.get_global_mean(question)}
    
    # Primește o întrebare (din setul de întrebări de mai sus) și calculează diferența 
    # dintre global_mean și state_mean pentru toate statele.
    # Returneaza dictionar de forma {Stat1: valoare1, Stat2: valoare2...}
    def calculate_diff_from_mean(self, question):
        global_mean = self.get_global_mean(question)
        mean_dict = {}
        states = []
        for row in self.get_question_rows(question):
            state = row['LocationDesc']
            # Statele trebuie sa fie stocate intr-un set pentru a 
            # fi procesate o singura data, chiar daca apar duplicate.
            if state not in states:
                states.append(state)
        for state in states:
            state_mean = self.get_state_mean(state, question)
            diff = global_mean - state_mean
            mean_dict[state] = diff
        return mean_dict
    
    # Primește o întrebare (din setul de întrebări de mai sus) și un stat, și
    # calculează diferența dintre global_mean și state_mean pentru statul respectiv.
    # Returneaza dictionar de forma {Stat: valoare}.
    def calculate_state_diff_from_mean(self, state, question):
        global_mean = self.get_global_mean(question)
        state_mean = self.get_state_mean(state, question)
        diff = global_mean - state_mean
        return {state: diff}

    # Primește o întrebare (din setul de întrebări de mai sus) și calculează valoarea 
    # medie pentru fiecare segment (Stratification1) din categoriile (StratificationCategory1) 
    # fiecărui stat. 
    # Returneaza dictionar de forma {"('Stat1', 'Categorie1', 'Segment1')": valoare1,
    # "('Stat2', 'Categorie2', 'Segment2')": valoare2, ...}
    def calculate_mean_by_category(self, question):
        category_means = {}
        for row in self.get_question_rows(question):
                state = row['LocationDesc']
                category = row['StratificationCategory1'] 
                segment = row['Stratification1']
                # Am pus aceasta conditie pentru a asigura acele valori care nu au o valoare
                # (NaN) (in acest .csv este doar 'New Jersey').
                if segment == '':
                     continue
                value = float(row['Data_Value'])
                key = (state, category, segment)
                # Daca nu exista cheia, initializam lista.
                if key not in category_means:
                    category_means[key] = []
                category_means[key].append(value)
        for key in category_means:
            values = category_means[key]
            category_means[key] = sum(values) / len(values)
        # Setam cheia sa fie de tip string.
        formatted_category_means = {str(key): value for key, value in category_means.items()}
        return formatted_category_means

    # Primește o întrebare (din setul de întrebări de mai sus) și un stat, și calculează 
    # valoarea medie pentru fiecare segment (Stratification1) din categoriile 
    # (StratificationCategory1).
    # Returneaza dictionar de forma {'Stat': {'('Categorie1', 'Segment1'): valoare1, 
    # ....}
    def calculate_state_mean_by_category(self, state, question):
        state_category_means = {}
        for row in self.get_question_rows(question):
            if row['LocationDesc'] == state:
                category = row['StratificationCategory1'] 
                segment = row['Stratification1']
                value = float(row['Data_Value'])
                if segment == '':
                    continue
                key = (category, segment)
                # Daca nu exista cheia, initializam lista.
                if key not in state_category_means:
                    state_category_means[key] = []
                state_category_means[key].append(value)
        for key in state_category_means:
            values = state_category_means[key]
            state_category_means[key] = sum(values) / len(values)
        # Setam cheia sa fie de tip string.
        formatted_state_category_means = {
            state: {str(key): value for key, value in state_category_means.items()}
        }
        return formatted_state_category_means