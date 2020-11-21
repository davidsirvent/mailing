import mailing_app

app = mailing_app.create_app()

if __name__ == '__main__':
    app.run(debug=True)
