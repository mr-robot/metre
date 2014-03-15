__author__ = 'beast'


class ConfigStruct:
    def __init__(self, entries):
        self.__dict__.update(entries)
        self.config_dict = entries


debug_config = {
    "app_name": "datafall",

    "store_key": "default_manager",
    "DEBUG": True,
    "SECRET_KEY": 'debug key',

    'MONGODB_SETTINGS': {'DB': 'debug',

    },
    'Collections': [
        ("Customer","customer"),
                        ],
    "Commands":[ ("Group","group$")


    ]


}

test_config = {

    "app_name": "datafall",
    "store_key": "default_manager",
    "DEBUG": True,
    "SECRET_KEY": 'development key',
    "db_config_prefix": "test",
    "test_DBNAME": "test_db",

    'MONGODB_SETTINGS': {'DB': 'testing'},
    'Collections': [
        ("Customer","customer"),
                        ],
    "Commands":[ ("Group","group$")


    ]

}

prod_config = {

    "app_name": "datafall",
    "store_key": "default_manager",
    "DEBUG": False,
    "SERVER_NAME": "metre.pw",

    "SECRET_KEY": 'safiokm35y98uq23ujert54o9w3iohujnesdkmlweaklmfgtijtrije!@E$($@%(*!@UHQFWikasf',
    'Collections': [
        ("Customer","customer"),
                        ],
    "Commands":[ ("Group","group$")


    ]
}


def config(test_only=False, prod_only=False):
    if prod_only:
        return ConfigStruct(prod_config)
    if test_only:
        return ConfigStruct(test_config)

    return ConfigStruct(debug_config)



