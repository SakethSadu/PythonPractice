from Website import create_app

app = create_app() #calling the function created early from the website package.

#only if we run this main.py file - we execute the next line i.e., to run the flask application
# If not, just importing the file would run the application and create a webserver
if __name__ == '__main__':

    app.run(debug= True) #running the flask application


