import configparser
import io
import json
import re

ENCODING_FORMAT = "utf-8"


class SnipsI18n(object):
    __dic = {}

    __path = None
    __locale = None

    def __init__(self, path, locale = 'en_US'):
        self.__path = path
        self.__locale = locale
        self.__load_dictionary()

    def __load_dictionary(self):
        dir = '{}/{}.json'.format(self.__path, self.__locale)
        try:
            with open(dir, 'r', encoding=ENCODING_FORMAT) as f:
                self.__dic = json.loads(f.read())
        except IOError as e:
            print (e)

    def get(self, raw_key, parameters = {}):
        keys = raw_key.split('.')
        temp = self.__dic

        for key in keys:
            temp = temp.get(key, 'null')

        if not parameters or temp == 'null':
            return temp
        else:
            for key in parameters:
                pattern = '(\{){2}(\s)*(' + key +'){1}(\s)*(\}){2}'
                temp = re.sub(pattern, str(parameters[key]), temp)
            return temp