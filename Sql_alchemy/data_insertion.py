import csv
from datetime import datetime
from db import get_db, Currency, Historical, GitHub, Language, LanguageCurrency, Tag, TagsCurrency

def parse_datetime(datetime_str):
    try:
        return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=None)
    except ValueError:
        print(f"Invalid datetime format: {datetime_str}")
        return None

def insert_currency_data(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        with get_db() as session:
            for row in csv_reader:
                currency = Currency(
                    rank=row['rank'],
                    name=row['name'],
                    symbol=row['symbol'],
                    circulating_supply=row['circulating_supply'],
                    main_link=row['main_link'],
                    historical_link=row['historical_link']
                )
                session.add(currency)

def insert_historical_data(csv_file_path):
    with open(csv_file_path, 'r') as historical_csv_file:
        historical_csv_reader = csv.DictReader(historical_csv_file)
        with get_db() as session:
            for historical_row in historical_csv_reader:
                currency_id = historical_row['id'] 
                currency = session.query(Currency).filter_by(id=currency_id).first()
                if currency is None:
                    print(f"Currency with ID {currency_id} not found.")
                else:
                    historical_record = Historical(
                        currency_id=currency.id,
                        timeOpen=parse_datetime(historical_row['timeOpen']),
                        timeClose=parse_datetime(historical_row['timeClose']),
                        timeHigh=parse_datetime(historical_row['timeHigh']),
                        timeLow=parse_datetime(historical_row['timeLow']),
                        open=historical_row['open'],
                        high=historical_row['high'],
                        low=historical_row['low'],
                        close=historical_row['close'],
                        volume=historical_row['volume'],
                        marketCap=historical_row['marketCap'],
                        timestamp=parse_datetime(historical_row['timestamp'])
                    )
                    session.add(historical_record)

def insert_github_data(csv_file_path):
    with open(csv_file_path, 'r') as github_csv_file:
        github_csv_reader = csv.DictReader(github_csv_file)
        with get_db() as session:
            for github_row in github_csv_reader:
                currency_id = github_row['currency_id'] 
                currency = session.query(Currency).filter_by(id=currency_id).first()
                if currency is None:
                    print(f"Currency with ID {currency_id} not found.")
                else:
                    github_record = GitHub(
                        currency_id=currency.id,
                        commits_count=github_row['commits_count'],
                        contributors_count=int(github_row['contributors_count'] or 0),
                        forks_count=github_row['forks_count'],
                        stars_count=github_row['stars_count'],
                        github_link=github_row['github_link']
                    )
                    session.add(github_record)

def insert_language_data(csv_file_path):
    with open(csv_file_path, 'r') as languages_csv_file:
        languages_csv_reader = csv.DictReader(languages_csv_file)
        with get_db() as session:
            for language_row in languages_csv_reader:
                id = language_row['id']
                language_name = language_row['name']
                language = session.query(Language).filter_by(name=language_name).first()
                if language is None:
                    language = Language(id=id, name=language_name)
                    session.add(language)

def insert_language_currency_data(csv_file_path):
    with open(csv_file_path, 'r') as currency_lang_csv_file:
        currency_lang_csv_reader = csv.DictReader(currency_lang_csv_file)
        with get_db() as session:
            for row in currency_lang_csv_reader:
                currency_id = row['currency_id']
                language_id = row['language_id']
                percentage = row['percentage']
                currency = session.query(Currency).filter_by(id=currency_id).first()
                language = session.query(Language).filter_by(id=language_id).first()
                if currency is None or language is None:
                    print(f"Currency with ID {currency_id} or Language with ID {language_id} not found.")
                else:
                    language_currency = LanguageCurrency(
                        currency_id=currency.id,
                        language_id=language.id,
                        percentage=percentage
                    )
                    session.add(language_currency)

def insert_tags_data(csv_file_path):
    with open(csv_file_path, 'r') as tags_csv_file:
        tags_csv_reader = csv.DictReader(tags_csv_file)
        with get_db() as session:
            for tag_row in tags_csv_reader:
                id = tag_row['id']
                tag_name = tag_row['name']
                tag = session.query(Tag).filter_by(name=tag_name).first()
                if tag is None:
                    tag = Tag(id=id, name=tag_name)
                    session.add(tag)

def insert_tags_currency_data(csv_file_path):
    with open(csv_file_path, 'r') as tag_currency_csv_file:
        tag_currency_csv_reader = csv.DictReader(tag_currency_csv_file)
        with get_db() as session:
            for row in tag_currency_csv_reader:
                currency_id = row['currency_id']
                tag_id = row['tag_id']
                currency = session.query(Currency).filter_by(id=currency_id).first()
                tag = session.query(Tag).filter_by(id=tag_id).first()
                if currency is None or tag is None:
                    print(f"Currency with ID {currency_id} or Tag with ID {tag_id} not found.")
                else:
                    tag_currency = TagsCurrency(
                        currency_id=currency.id,
                        tag_id=tag.id
                    )
                    session.add(tag_currency)

def run_data_insertion():
    currency_csv_file = 'Final_data/currency.csv'
    historical_csv_file = 'Final_data/historical.csv'
    github_csv_file = 'Final_data/github.csv'
    language_csv_file = 'Final_data/languages.csv'
    currency_lang_csv_file = 'Final_data/currency_lang.csv'
    tags_csv_file = 'Final_data/tags.csv'
    tag_currency_csv_file = 'Final_data/currency_tag.csv'

    insert_currency_data(currency_csv_file)
    insert_historical_data(historical_csv_file)
    insert_github_data(github_csv_file)
    insert_language_data(language_csv_file)
    insert_language_currency_data(currency_lang_csv_file)
    insert_tags_data(tags_csv_file)
    insert_tags_currency_data(tag_currency_csv_file)

if __name__ == "__main__":
    run_data_insertion()
