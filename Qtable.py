import csv
class Qtable:
    def __init__(self, q_table_path):
        self.q_table = self.__load_q_table(q_table_path)


    @staticmethod
    def __load_q_table(path):
        q_table = []
        with open(path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                q_value = float(row['Q_Value'])
                state = row['State'].split(', ')
                action = row['Action']
                q_table.append({'q_value': q_value, 'state': state, 'action': action})
        return q_table

    def getQTable(self):
        return self.q_table

    def getAction(self, states):
        current_state = [str(states[x]) for x in states]
        max_q_value = float('-inf')  # Initialize with negative infinity
        best_action = ''
        for item in self.q_table:
            # Check if the state matches the current state
            if item['state'] == current_state:
                if item['q_value'] > max_q_value:
                    max_q_value = item['q_value']
                    best_action = item['action']
        print(best_action)
        return best_action
