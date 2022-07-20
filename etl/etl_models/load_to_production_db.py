def export_data(subreddit, database, num_post = 100):
    '''
    This function will populate MongoDB with respective subreddit posts
    subreddit (str): subreddit to scrape and add to DB 
    '''
    #Connect to MongoDB
    client = pymongo.MongoClient(config.mongo_cred)
    #Define database
    db = client[database]
    #Define collection within 'RedditCollect'
    collection = db[subreddit]

    subreddit_all = {
        'indieheads': get_indieheads_data,
        'Alternativerock': get_Alternativerock_data
        }
    
    subreddit_data = subreddit_all[subreddit](num_post = num_post)

    duplicate = []
    for post in subreddit_data:
        try:
            collection.insert_one(post)
        except pymongo.errors.DuplicateKeyError:
            duplicate.append(1)
    
    print('{0} records were not added becasue they are duplicates'.format(len(duplicate)))
