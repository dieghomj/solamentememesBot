import tweepy


def twitter_api():

    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def upload_photo(caption='t.me/solamentememes'):
    api = twitter_api()

    try:
        api.update_status_with_media(caption, 'photo.jpg')
        return True
    except Exception as e:
        print(
            "encountered error in photo upload! error deets: %s" % str(e)
        )
        return False


def upload_video():
    api = twitter_api()

    try:
        api.media_upload('video.mp4')
        return True
    except Exception as e:
        print(
            "encountered error in video upload! error deets: %s" % str(e)
        )
        return False
