__author__ = 'beast'

import argparse

from controller import Manager



class Admin(object):

    def __init__(self):
        pass

    def add_collection(label, collection_name, config):
        pass

    def setup_parser(self):

        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(help='sub-command help')

        parser_add = subparsers.add_parser('--add', help='configures metre by adding collections, search data or users')

        parser_add.add_argument("collection", help="add collection to metre - label, collection_name", nargs=2)
        parser_add.add_argument("search", help="load searches into metre")

        parser_add.add_argument("users", help="load searches into metre")


        return parser

    def get_args(self):

        parser = self.setup_parser()


        parser.parse_args()


    def run(self):
        args = self.get_args()





if __name__ == "__main__":
    Admin().run()