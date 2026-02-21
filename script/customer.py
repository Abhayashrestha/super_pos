import random
import data.storage
import time


connect=data.storage.get_connection()

bot_names=["piers", "john", "josh", "johny", "arthur",
    "clav", "togi", "steve", "jake", "Finn"]

def bot_purchase(connection):
    try:
        while True:
            with connection.cursor() as cur:
                query = """
                    """

