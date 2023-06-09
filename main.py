from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from MongoDB import MongoDBOperations
from WikipediaScrapper import WikipediaScrapper
from flask import Flask, request, render_template

# initialising the flask app with the name 'app'
app= Flask(__name__)

global_status = True

@app.route('/', methods=['GET', 'POST']) # To render Homepage
def home_page():
    return render_template('index.html')

@app.route('/wiki-scrap',methods=['POST'])
def project():
    if request.method == 'POST':
        # getting data to be search
        search_data = request.form['search_data']
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("headless")
            cl = MongoDBOperations("pradyumn20", "Pradyumn20")
            # getting MongoDB client connection
            mongo_cl = cl.getMongoObject()
            db_name = 'Wikipedia_Scrap'
            # checking if database is present in mongodb
            if cl.IsDatabasePresent(mongo_cl, db_name):
                database1 = cl.getDatabase(db_name)
            else:
                database1 = cl.CreatingDatabase(mongo_cl, db_name)
            # Checking if collection is already present in database or not
            if cl.IsCollectionPresent(db_name, search_data):
                collection = cl.getCollection(database1, search_data)
                record = collection.find({})
                # If collection already is present, we will retrieve the data and will close the app
                for i in record:
                    name = i['Name']
                    summary = ''.join(i['Summary'])
                    links = '\n'.join(i['Links'])
                    images = '\n'.join(i['Images'])
                return render_template('results.html', search_data=name, Summary=summary, Links=links,
                                       Images=images)
                quit()
            else:
                collection = cl.CreatingCollection(db_name, search_data)
            # initializing driver for scrapping
            wiki_object = WikipediaScrapper(executable_path=ChromeDriverManager().install(), chrome_options=options)
            wiki_object.OpenUrl("https://www.wikipedia.org/")
            # getting search button
            x = wiki_object.getSearchButton()
            x.send_keys(search_data)
            # searching the data on url
            wiki_object.searchData()
            time.sleep(5)
            # getting body content of data searched
            data = wiki_object.getPageData()
            # Getting Summarize data
            summary = wiki_object.getSummary(data)
            # Getting links
            count = wiki_object.getLinks()
            # Getting images
            imgs = wiki_object.getImages()
            result = {
                "Name": search_data,
                "Summary": summary,
                "Links": count,
                "Images": imgs
            }
            cl.insertOne(collection, result)
            return render_template('results.html', search_data=search_data, Summary=''.join(summary),
                                   Links='\n'.join(count), Images='\n'.join(imgs))
            # closing driver and database connection
            mongo_cl.close()
            wiki_object.closeDriver()

        except Exception as e:
            raise Exception("Issue while running the app : ", str(e))


if __name__=="__main__":
    app.run(debug=True)
