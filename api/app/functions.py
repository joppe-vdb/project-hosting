import database

def create_username(name:str):
    # get intials form the name
    first_letters = [word[0] for word in name.split()]
    intials = "".join(first_letters)
    intials = intials.lower()

    # add number for safety
    return intials + str(database.get_number_of_user())
