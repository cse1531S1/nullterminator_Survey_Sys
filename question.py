import csv

class question():
    """docstring for question."""
    # allocate the location of the csv file
    _csv_fileName = "ques.csv"
    # a dict to store all the instance of this object
    _questDisct = {}

    def get_csvName():
        return _csv_fileName;

    def __init__(self, row= None):
        super(question, self).__init__()

    def csv_readRow(self,row):
        # try to read each row in this function
        # after reading a row add an instance of this class into the _questDisct
        # data_struct is: id, question, [answers]..
        pass



class myCSV():
    """docstring for myCSV."""
    def __init__(self):
        super(myCSV, self).__init__()

    def write(obj):
        with open(obj.get_csvName(),'a') as csv_out:
            writer = csv.writer(csv_out)
            writer.writerow([name, zID, desc])

    def read(obj):
        with open(obj.get_csvName(),'r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                # calling back the passed in obj to deal with the csv
                obj.csv_readRow(row)




if __name__ == '__main__':
    # unittests
    myCSV.write(question);
