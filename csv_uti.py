import csv


class csv_util():
    """docstring for csv_util."""
    def __init__(self):
        super(csv_util, self).__init__()
        # self.arg = arg
    def read_csv(obj):
        with open(obj.csv_name(),'r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                obj.csv_readRow(row)
    def write_csv(obj):
        # input content must be an array
        with open(obj.csv_name(),'w') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow(obj.csv_content())
    def append_csv(obj):
        # input content must be an array
        with open(obj.csv_name(),'a') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow(obj.csv_append())



if __name__ == '__main__':
    class validClass():
        """docstring for validClass."""
        def __init__(self):
            super(validClass, self).__init__()
        def csv_name(cls):
            return "question.csv"
        def csv_readRow(cls,row):
            print(row)
        def csv_content(self):
            return [1,2,3]
        def csv_append(self):
            return [1,2,3,4]



    aobj = validClass()
    csv_util.read_csv(aobj)
    csv_util.write_csv(aobj)
    csv_util.append_csv(aobj)
