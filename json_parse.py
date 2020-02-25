import urllib.request
import urllib.parse
import urllib.error
import twurl
import json
import ssl


TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


def get_json():
    """
    () -> dict
    Return dictinary with information about user.
    """
    acct = input('Enter Twitter Account: ')
    while len(acct) < 1:
        acct = input('Wrong input. Enter Twitter Account: ')
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '50'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data)

    return js


def json_parse(dic):
    """
    (dict) -> str/int/bool/float
    This function is to help to work json file.
    Return the information chosen by user.
    """
    while isinstance(dic, list) or isinstance(dic, dict):
        if isinstance(dic, dict):
            keys = dic.keys()
            keyss = ', '.join(keys)
            print("Choose one of given keys ({}): ".format(keyss), end='')
            user_input = input()
            while user_input not in keys:
                print("Wrong input. Choose one of given keys ({}): ".format(
                    keyss), end='')
                user_input = input()
            dic = dic[user_input]
        else:
            if len(dic) == 0:
                dic = []
            else:
                print("Choose number of element from 0 to {}: ".format(
                    len(dic) - 1), end='')
                user_input = int(input())
                while int(user_input) not in range(len(dic)):
                    print("Wrong input. Choose number of element from 0 to {}: ".format(
                        len(dic) - 1), end='')
                    user_input = int(input())
                for ind, di in enumerate(dic):
                    if ind == user_input:
                        dic = di
    return dic


if __name__ == "__main__":
    print(json_parse(get_json()))
