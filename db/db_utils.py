import csv
import os

import psycopg2

TIMEOUT = 10


def check_data(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchone()

    return bool(rows)


def create_connection():
    db_user = os.getenv('POSTGRES_USER')
    db_password = os.getenv('POSTGRES_PASSWORD')
    db_name = os.getenv('POSTGRES_DB')
    db_host = os.getenv('POSTGRES_HOST')

    conn = psycopg2.connect(
        f"dbname={db_name} user={db_user} password={db_password} host={db_host}"
    )

    cur = conn.cursor()
    return cur, conn


def add_data_to_documents(cursor, pathtofile, doc_name):
    with open(pathtofile) as file:
        cursor.execute(
            "INSERT INTO documents (name, text) VALUES (%s, %s)", (doc_name, file.read())
        )

        return


def add_data_to_questions(cursor, pathtofile):
    # add data to db (questions table)
    with open(pathtofile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            question_text = f'Translate the word: {row["question_text"]}.'
            answer1_text = row['answer1_text']
            answer2_text = row['answer2_text']
            answer3_text = row['answer3_text']
            correct_id = row['correct_id']

            cursor.execute(
                "INSERT INTO questions (question_text, answer1_text, answer2_text, "
                "answer3_text, correct_id, timeout) VALUES (%s, %s, %s, %s, %s, %s)",
                (question_text,
                 answer1_text,
                 answer2_text,
                 answer3_text,
                 correct_id,
                 TIMEOUT)
            )

        return


def clear_table(cursor, table_name):
    cursor.execute(f"DELETE FROM {table_name};")

    return
