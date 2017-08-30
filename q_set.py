from question import quest_tree
from csv_uti import csv_util

# only one instance of this class to manage
class q_set():
    """docstring for q_set."""
    set_questions =[]
    def __init__(self):
        # super(q_set, self).__init__()

        # initialize this class
        csv_util.read_csv(self)

    # functions for csv_util
    def csv_name(cls):
        return "csv/quest_set.csv"
    def csv_readRow(cls,row):
        print(row)#only one row
        # convert the input into int and store in this set
        cls.set_questions = [int(item ) for item in row]

    def csv_content(cls):
        # save the current question into the csv file
        return cls.set_questions
    # not use this fucntion yet
    # def csv_append(self):
    #     return [[1,2,3,4]]




# all the manage functions are achieve in this set. CRUD
class q_set_opt(object):
    """docstring for q_set_opt."""
    def __init__(self, q_set_ins):
        super(q_set_opt, self).__init__()
        # get the question set instance from user
        self._q_set = q_set_ins
    # remap two functions in the q_set to achieve same fucntion
    def get(self):
        # get all the question id in the set
        return self._q_set.csv_content()
    def set(self, q_ids = []):
        # if pass in nothing, it's clearing this set
        self._q_set.csv_readRow(q_ids)
        # should write back to csv
        csv_util.write_csv(self._q_set)


    def delete_q(self,q_ids = []):
        sets  = self.get()
        for i in q_ids:
            # remove all the userwant id from the set
            sets.remove(int(i))
        # write the result to the csv file
        self.set(sets)

if __name__ == '__main__':
    # unit tests
    set_opt = q_set_opt(q_set())
    print(set_opt.get())
    set_opt.set([1,2])
    print(set_opt.get())
    set_opt.delete_q([1])
    print(set_opt.get())
