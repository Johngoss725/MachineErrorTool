from website import create_app
# we have this access becuase "website is a package due to the __init__.py file"

app = create_app()
if __name__ == "__main__":
    app.run(debug = True)

