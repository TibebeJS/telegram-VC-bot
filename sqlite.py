#!/usr/bin/python

import sqlite3

class VoiceChatDatabase:
    def __init__(self, name):
        self.__conn = sqlite3.connect(name)
        print("Opened database successfully")

        self.__conn.execute('''CREATE TABLE IF NOT EXISTS MUTE_LIST (
                    USER_ID     INT PRIMARY KEY   NOT NULL,
                    USER_FULLNAME     TEXT KEY   NOT NULL,
                    MUTED_BY    INT               NOT NULL,
                    MUTED_BY_NAME    TEXT          NOT NULL,
                    REASON      TEXT              NULLABLE,
                    MUTED_AT    TEXT              NOT NULL
            );
        ''')

        self.__conn.execute('''CREATE TABLE IF NOT EXISTS UNMUTE_LIST (
                    USER_ID     INT PRIMARY KEY   NOT NULL,
                    USER_FULLNAME     TEXT   NOT NULL,
                    UNMUTED_BY    INT               NOT NULL,
                    UNMUTED_BY_NAME   TEXT               NOT NULL,
                    REASON      TEXT              NULLABLE,
                    UNMUTED_AT    TEXT              NOT NULL
            );
        ''')

    def is_user_muted(self, user_id):
        cursor = self.__conn.execute("SELECT MUTED_BY, REASON, MUTED_AT FROM MUTE_LIST WHERE USER_ID = ?", (user_id,))
        return cursor.fetchone() is not None

    def mute_user(self, user_id, user_fullname, admin_id, admin_name, reason):
        try:
            self.__conn.execute(f"""DELETE FROM UNMUTE_LIST WHERE USER_ID = {user_id}""")
            self.__conn.execute(f"""INSERT INTO MUTE_LIST (USER_ID, USER_FULLNAME, MUTED_BY, MUTED_BY_NAME, REASON, MUTED_AT)
                                VALUES ({user_id}, "{user_fullname}", {admin_id}, "{admin_name}", "{reason}", datetime('now'));
                        """)
            self.__conn.commit()
        except Exception as e:
            print(e)
        return self.is_user_muted(user_id)

    def unmute_user(self, user_id, user_fullname, admin_id, admin_name, reason):
        try:
            self.__conn.execute(f"""DELETE FROM MUTE_LIST WHERE USER_ID = {user_id}""")
            self.__conn.execute(f"""INSERT INTO UNMUTE_LIST (USER_ID, USER_FULLNAME, UNMUTED_BY, UNMUTED_BY_NAME, REASON, UNMUTED_AT)
                                VALUES ({user_id}, "{user_fullname}", {admin_id}, "{admin_name}", "{reason}", datetime('now'));
                        """)
            self.__conn.commit()
        except Exception as e:
            print(e)
        return self.is_user_unmuted(user_id)

    def is_user_unmuted(self, user_id):
        cursor = self.__conn.execute("SELECT UNMUTED_BY, REASON, UNMUTED_AT FROM UNMUTE_LIST WHERE USER_ID = ?", (user_id,))
        return cursor.fetchone() is not None
    
    def __del__(self):
        self.__conn.close()
