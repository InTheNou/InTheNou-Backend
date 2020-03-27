from flask import jsonify
from psycopg2 import IntegrityError









class PhoneHandler:

    def unpackPhones(self, json):
        numbers = []
        for num in json:
            if num['number'] not in numbers:
                numbers.append(num['number'])
        return numbers
