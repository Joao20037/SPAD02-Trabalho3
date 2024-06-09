from view import View

def main():
    dbname = 'northwind'
    user = 'postgres'
    password = 'root'

    app = View(dbname, user, password)
    app.run()

if __name__ == "__main__":
    main()
