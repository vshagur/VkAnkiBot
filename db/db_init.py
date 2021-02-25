import csv
import os

import psycopg2

TIMEOUT = 10


def init_database():
    """"""
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_name = os.getenv('POSTGRES_DB')
    db_host = os.getenv('POSTGRES_HOST')

    conn = psycopg2.connect(
        f"dbname={db_name} user={db_user} password={db_password} host={db_host}"
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM questions;")
    row_from_questions = cur.fetchone()
    cur.execute("SELECT * FROM documents;")
    row_from_documents = cur.fetchone()

    # check db is not empty
    if row_from_questions or row_from_documents:
        print(
            'The script has stopped. The database is not empty. Please check the content '
            'of the database.\n')
        cur.close()
        conn.close()
        return

    # add data to db (questions table)
    with open('db/QuestionsEnRuDictionaryTop1000.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question_text = f'Translate the word: {row["question_text"]}.'
            answer1_text = row['answer1_text']
            answer2_text = row['answer2_text']
            answer3_text = row['answer3_text']
            correct_id = row['correct_id']

            cur.execute(
                "INSERT INTO questions (question_text, answer1_text, answer2_text, "
                "answer3_text, correct_id, timeout) VALUES (%s, %s, %s, %s, %s, %s)",
                (question_text,
                 answer1_text,
                 answer2_text,
                 answer3_text,
                 correct_id,
                 TIMEOUT)
            )

        # add data to db (documents table)
        with open('db/man.txt') as file:
            text = file.read()
            cur.execute(
                "INSERT INTO documents (name, text) VALUES (%s, %s)", ('help', text)
            )

    print('The database has been initialized successfully. ')

    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    init_database()
