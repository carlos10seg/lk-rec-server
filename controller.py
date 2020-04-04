from os import path
from datetime import datetime
from lenskit_proxy import LenskitProxy
from data_manager import DataManager
from db_manager import DbManager
from model_manager import ModelManager

class Controller:
    def create_db_structure_with_data(self):
        dataManager = DataManager()
        dbManager = DbManager()
        movies = dataManager.get_movies()
        ratings = dataManager.get_ratings()
        links = dataManager.get_links()
        dbManager.create_db_structure_with_data(movies, ratings, links)

    # Get recommendations from data file or database
    def get_recs(self, user_id, nr_recs, algo, items):
        #dataManager = DataManager()
        #ratings = dataManager.get_ratings()
        dbManager = DbManager()
        ratings = dbManager.get_ratings()
        
        lkProxy = LenskitProxy()
        # recs = []
        # for userId in users:
        #     recs.append({'user': userId, 'recs': lkProxy.get_recs(userId, nr_recs, algo, ratings, items)})        
        # return recs
        return lkProxy.get_recs(user_id, nr_recs, algo, ratings, items)
    
    # Get recommendations using a saved model
    def get_recs_using_model(self, user_id, nr_recs, algo, items):
        modelManager = ModelManager()
        lkProxy = LenskitProxy()
        model = modelManager.load(algo)
        return lkProxy.get_recs_from_model(model, user_id, nr_recs,items)

    def save_models(self, algos):
        lkProxy = LenskitProxy()
        #dataManager = DataManager()
        #ratings = dataManager.get_ratings()
        dbManager = DbManager()
        ratings = dbManager.get_ratings()
        print(len(ratings))
        modelManager = ModelManager()
        for algo in algos.split(','):
            model = lkProxy.create_model(algo, ratings)
            modelManager.store(model, algo)
    
    def get_model_info(self, algo):
        model_file_dir_path = "files/" + algo + '.pickle'
        creation_date = ""
        updated_date = ""
        size = 0
        if path.exists(model_file_dir_path):
            creation_date = datetime.utcfromtimestamp(path.getctime(model_file_dir_path)).strftime('%Y-%m-%d %H:%M:%S') 
            updated_date = datetime.utcfromtimestamp(path.getmtime(model_file_dir_path)).strftime('%Y-%m-%d %H:%M:%S')
            size = path.getsize(model_file_dir_path) / 1000
        return {"creation_date": creation_date + " UTC", "updated_date": updated_date + " UTC", "size": str(size) + " KB"}

    def upload_model(self, algo, data):
        return None

    def preload_models(self):
        return None