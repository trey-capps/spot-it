import requests

class ExtractReddit:

    def __init__(self, kwargs):
        self.CLIENT_ID = kwargs["redditClientID"]
        self.SECRET_KEY = kwargs["redditSecretKey"]
        self.USERNAME = kwargs["redditUsername"]
        self.PASS = kwargs["redditPass"]
        self.USER_AGENT = kwargs["redditUserAgent"]
        
        # Documentation : https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example
        self.client_auth = requests.auth.HTTPBasicAuth(f"{self.CLIENT_ID}", f"{self.SECRET_KEY}")
        self.post_data = {"grant_type": "password", "username": f"{self.USERNAME}", "password": f"{self.PASS}"}
        self.headers = {"User-Agent": f"{self.USER_AGENT}"}

    def get_access_token(self):
        """Get access token from Reddit API"""
        try:
            response = requests.post("https://www.reddit.com/api/v1/access_token", auth=self.client_auth, data=self.post_data, headers=self.headers)
            #Save Token 
            token_type = response.json()['token_type']
            access_token = response.json()['access_token']
            return {"Authorization": f"{token_type} {access_token}", **self.headers} #Now send GET requests to "https://oauth.reddit.com"
        except:
            print(f"Error generating token, status code: {response.status_code}")
            return None

    def get_subreddit_data(self, subreddit):
        """
        Generate post request with access tokens to gather post data
        subreddit (str): Subreddit name
        """
        #Add testing as to whether that is an actual subreddit
        try:
            headers = self.get_access_token()
            limit = 30
            get_posts = requests.get(f"https://oauth.reddit.com/r/{subreddit}/new?limit={limit}", headers=headers)
            print(f"Collected {limit} posts from r/{subreddit}")
            return get_posts
        except:
            print(f"Error getting posts, status code: {get_posts.status_code}")
            return None