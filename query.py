import csv



class query:
    """
    docstring for query.
    base class manipulate the csv reading and writing.
    """
    def __init__(self, fileName,directory="",prefix=""):
        super(query, self).__init__()
        self.__fileName = directory+prefix+fileName
        # all the data would save in this key = id(string(primary key)), value is array
        self.__dataDict = {}
        # for all the value that have been select
        self.__holdId = []
        # value for where the whole class something update.
        self.__update = False
        # initial this class by reading the fileName
        self.__readFile()

    def get_fileName(self):
        # return the file name store in this instance
        return self.__fileName

    def all(self):
        # list of all the value should return
        if len(self.__holdId) == 0:
            # user doesn't select the data
            # return all the value in dictory
            return [data for data in self.__dataDict.values()]
        else:
            # search for all the id that holds
            return [self.__dataDict[key] for key in self.__holdId]

    def __readFile(self):
        with open(self.get_fileName(),'r') as csv_in:
            reader = csv.reader(csv_in)
            for row in reader:
                # for all the row in the file store in this instance
                self.__dataDict[row[0]]= row

    def save(self):
        # write all the changes in the file
        if self.__update:
            # flush all the information to the csv file
            write_list = [data for data in self.__dataDict.values()]
            with open(self.get_fileName(),'w+') as csv_out:
                writer = csv.writer(csv_out)
                for row in write_list:
                    writer.writerow(row)
        # the file doesn't need to be update, do nothing
        return self
    def update(self,newData):
        slef.__update = True
        return self
    def append(self,data):
        return self
    def findId(self,ids):
        if type(ids) == list:
            # the input type is list
            # clear this list
            self.__holdId= []
            for thisId in ids:
                str(thisId)
                # try to find this id
                self.__dataDict[str(thisId)]
                # append this in the list
                self.__holdId.append(str(thisId))

        elif type(ids) == str or type(ids) == int:
            # the input is a str or int
            # clear the list
            self.__holdId = []
            # try to find this id
            self.__dataDict[str(ids)]
            # append this in the list
            self.__holdId.append(str(ids))
        else:
            # input an un manageable type
            raise TypeError

        return self
    def where(self,key):
        return self


if __name__ == '__main__':
    course = query("courses.csv", directory="", prefix="")
    # print(course.get_fileName())
    print(course.all())

    course.findId("COMP1511 17s1")
    print(course.all())
    course.findId(["COMP1511 17s1"])
    print(course.all())
