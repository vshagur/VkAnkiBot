import psycopg2
import os
import csv

TIMEOUT = 10


def init_database():
    """"""
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_name = os.getenv('POSTGRES_DB')
    db_host = os.getenv('POSTGRES_HOST')
    db_filename = os.getenv('DB_INIT_FILENAME')

    conn = psycopg2.connect(
        f"dbname={db_name} user={db_user} password={db_password} host={db_host}"
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM questions;")

    if cur.fetchone():
        print(
            'The script has stopped. The database is not empty. Please check the content '
            'of the database.')
    else:
        with open(db_filename, newline='') as csvfile:
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

            conn.commit()
            print('The database has been initialized successfully. ')

    cur.close()
    conn.close()


if __name__ == '__main__':
    init_database()
