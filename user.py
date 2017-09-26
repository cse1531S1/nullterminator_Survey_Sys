from sql_uti import sql_util


class User(sql_util):
    """docstring for user."""
    def __init__(self):
        super().__init__("users")

    def findById(self, id):
        if type(id)!=int:
            raise TypeError("id for a user muset be a interger")
        # simple case of mapping a function to dynamic execute SQL
        return self.find("user_id",id).one()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        if type(name)!= str:
            raise TypeError("User's name must be a string")
        self.__name = name

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self,password):
        if type(password)!= str:
            raise TypeError("User's password must be a string")
        self.__password = password

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self,id):
        if type(id)!= int:
            raise TypeError("User's id must be a string")
        self.__id = id

    def saveUser(self):
        if not (self.name and self.id and self.password):
            raise TypeError("the user_name, user_id, password must be all setted")
        # store the information in the class
        self.insert(["user_id","user_name","password"],[self.id,self.name,self.password]).save()
        # return self to have the property of one online execution
        return self
    def deleteById(self, id):
        if type(id)!= int:
            raise TypeError("input id must be int")
        self.find("user_id",id).delete()



if __name__ == '__main__':
    user = User()
    # use.print_table()
    print(user.findById(50))

    user.name = "toby"
    user.password = "secret"
    user.id = 1
    user.saveUser()

    print(user.findById(1))

    # cleanup the added user
    user.deleteById(1)
    print(user.findById(1))
