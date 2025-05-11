from db.initialise_database import initialise_database


def build():
    '''
    Initializes the database by dropping existing tables and creating new ones.
    '''
    initialise_database()


if __name__ == "__main__":
    build()
