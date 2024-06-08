from view import View

def main():
    dbname = 'postgres'
    user = 'postgres'
    password = '2018'

    app = View(dbname, user, password)
    app.run()

if __name__ == "__main__":
    main()
