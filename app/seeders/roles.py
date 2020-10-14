from ..models import Roles
from ..settings import Database

def role_seeder():
    database = Database()
    database.start_connection()

    roles = [
        {
            'name': 'admin',
            'code': '000',
            'scopes': [
                '00_role_table',
                '00_role_get_all',
                '00_role_get',
                '00_role_save',
                '00_role_update',
                '00_role_delete',
                '01_currency_table',
                '01_currency_get_all',
                '01_currency_get',
                '01_currency_save',
                '01_currency_update',
                '01_currency_delete',
                '01_language_table',
                '01_language_get_all',
                '01_language_get',
                '01_language_save',
                '01_language_update',
                '01_language_delete',
                '03_country_table',
                '03_country_get_all',
                '03_country_get',
                '03_country_save',
                '03_country_update',
                '03_country_delete',
                '03_state_table',
                '03_state_get_all',
                '03_state_get',
                '03_state_save',
                '03_state_update',
                '03_state_delete',
                '03_city_table',
                '03_city_get_all',
                '03_city_get',
                '03_city_save',
                '03_city_update',
                '03_city_delete',
                '04_american_banks_table',
                '04_american_banks_get_all',
                '04_american_banks_get',
                '04_american_banks_save',
                '04_american_banks_update',
                '04_american_banks_delete',
                '04_european_banks_table',
                '04_european_banks_get_all',
                '04_european_banks_get',
                '04_european_banks_save',
                '04_european_banks_update',
                '04_european_banks_delete',
                '04_latinamerican_banks_table',
                '04_latinamerican_banks_get_all',
                '04_latinamerican_banks_get',
                '04_latinamerican_banks_save',
                '04_latinamerican_banks_update',
                '04_latinamerican_banks_delete',
                '04_credit_cards_table',
                '04_credit_cards_get_all',
                '04_credit_cards_get',
                '04_credit_cards_save',
                '04_credit_cards_update',
                '04_credit_cards_delete'
            ]
        },
        {
            'name': 'basic_user',
            'code': '001',
            'scopes': []
        }
    ]

    for role in roles:
        exist_role = Roles.objects(code=role['code'])
        if not exist_role: Roles(**role).save()

    database.close_connection()
