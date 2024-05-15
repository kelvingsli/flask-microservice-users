class UserUpdatePasswordDto:

    def __init__(self, id=None, firstname=None, lastname=None, email=None, issuccess=False):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email =  email
        self.issuccess = issuccess
