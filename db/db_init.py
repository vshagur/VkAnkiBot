from db.db_utils import (add_data_to_documents, add_data_to_questions,
                         check_data, create_connection)


def init_database():
    cur, conn = create_connection()

    if check_data(cur, 'documents') or check_data(cur, 'questions'):
        print(
            'The script has stopped. The database is not empty. Please check the content '
            'of the database.\n'
        )
        cur.close()
        conn.close()
        return

    add_data_to_questions(cur, 'db/QuestionsEnRuDictionaryTop1000.csv')
    add_data_to_documents(cur, 'db/man.txt', 'help')
    print('The database has been initialized successfully. ')

    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    init_database()
