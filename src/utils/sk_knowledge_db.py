import sqlite3
import os
from threading import Lock
from enum import IntEnum
from datetime import datetime, timezone


# 定义适配器和转换器
def adapt_datetime(dt):
    return dt.isoformat()


def convert_datetime(s):
    return datetime.fromisoformat(s)


# 注册适配器和转换器
sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("timestamp", convert_datetime)


class FileType(IntEnum):
    PDF = 1
    IMAGE = 2
    VIDEO = 3
    AUDIO = 4
    WORD = 5
    TEXT = 6
    EXCEL = 7
    PPT = 8
    UNKNOWN = 9

def get_file_name(file_path: str) -> str:
    return os.path.basename(file_path)

def check_file_type_by_extension(file_path: str) -> FileType:
    """
    Check the type of a file by its extension.

    Args:
        file_path (str): The path of the file.

    Returns:
        FileType: The type of the file.
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension == '.pdf':
        return FileType.PDF
    elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        return FileType.IMAGE
    elif file_extension in ['.mp4', '.avi', '.mov', '.mkv', 
                            '.flv', '.wmv', '.webm', '.m4v', '.mpg']:
        return FileType.VIDEO
    elif file_extension in ['.mp3', '.wav', '.ogg', '.flac',
                             '.m4a', '.wma', '.aac']:
        return FileType.AUDIO
    elif file_extension in ['.docx', '.doc']:
        return FileType.WORD
    elif file_extension in ['.txt', '.log', '.md']:
        return FileType.TEXT
    elif file_extension in ['.xlsx', '.xls']:
        return FileType.EXCEL
    elif file_extension in ['.pptx', '.ppt']:
        return FileType.PPT
    else:
        return FileType.UNKNOWN


class UploadStatus(IntEnum):
    UNPROCESSED = 1
    NOT_UPDATED = 2
    COMPLETED = 3


class SQLiteFileDB:
    def __init__(self, db_name: str = 'files.db') -> None:
        """
        初始化数据库连接、游标、锁并创建表。

        :param db_name: 数据库文件名，默认为 'files.db'
        """
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.lock = Lock()
        self.create_table()

    def create_table(self) -> None:
        """
        创建文件信息表，如果表不存在的话。
        """
        with self.lock:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT,
                    collection_name TEXT,
                    absolute_path TEXT UNIQUE,
                    file_type INTEGER,
                    file_md5 TEXT,
                    upload_status INTEGER,
                    process_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    update_at TIMESTAMP
                )
            ''')
            self.conn.commit()

    def add_record(
            self,
            filename: str,
            collection_name: str,
            absolute_path: str,
            file_type: FileType,
            file_md5: str,
            upload_status: UploadStatus = UploadStatus.UNPROCESSED,
            process_id: str = '',
            update_at: datetime = datetime.now(timezone.utc)
    ) -> None:
        """
        向文件信息表中添加一条新记录。
        :param filename: 文件名
        :param collection_name: 文件夹名
        :param absolute_path: 文件地址
        :param file_type: 文件类型，类型为 FileType 枚举
        :param file_md5: 文件的 MD5 值
        :param upload_status: 文件上传状态，类型为 UploadStatus 枚举，默认为未处理
        :param process_id: 文件处理 ID，默认为空字符串
        :param update_at: 文件更新时间，默认为当前时间
        :return: 新记录的 ID
        """
        with self.lock:
            self.cursor.execute('''
                INSERT OR REPLACE INTO files (filename, collection_name, absolute_path, file_type, file_md5, upload_status, process_id, update_at)
                VALUES (?,?,?,?,?,?,?,?)
            ''', (filename, collection_name, absolute_path, file_type.value, file_md5, upload_status.value, process_id, update_at))
            self.conn.commit()

    def find_records_by_collection_and_filename(
            self,
            collection_name: str,
            filename: str
    ) -> list[tuple]:
        """
        根据文件夹名和文件名查找文件记录。

        :param collection_name: 文件夹名
        :param filename: 文件名
        :return: 匹配的记录列表，每个记录为一个元组
        """
        with self.lock:
            self.cursor.execute('''
                SELECT * FROM files WHERE collection_name =? AND filename =?
            ''', (collection_name, filename))
            return self.cursor.fetchall()

    def update_status_by_id(
            self,
            file_id: int,
            upload_status: UploadStatus,
            update_at: datetime,
            file_md5: str
    ) -> None:
        """
        根据文件 ID 更新文件的上传状态、更新时间和 MD5 值。

        :param file_id: 文件记录的 ID
        :param upload_status: 文件上传状态，类型为 UploadStatus 枚举
        :param update_at: 文件更新时间
        :param file_md5: 文件的 MD5 值
        """
        with self.lock:
            self.cursor.execute('''
                UPDATE files
                SET upload_status =?, update_at =?, file_md5 =?
                WHERE id =?
            ''', (upload_status.value, update_at, file_md5, file_id))
            self.conn.commit()

    def close(self) -> None:
        """
        关闭数据库连接。
        """
        self.conn.close()


if __name__ == "__main__":
    db = SQLiteFileDB()
    # 新增记录
    # new_id = db.add_record(
    #     "test.txt",
    #     "test_folder",
    #     "/path/to/file",
    #     FileType.TEXT,
    #     "1234567890abcdef"
    # )
    # print(f"新增记录的 ID: {new_id}")

    # 按文件夹名和文件名查找记录
    records = db.find_records_by_collection_and_filename("test_folder", "test.txt")
    print("查找结果:")
    for record in records:
        # 按 id 更新状态
        new_update_at = datetime.now(timezone.utc)
        db.update_status_by_id(
            record[0],
            UploadStatus.COMPLETED,
            new_update_at,
            "abcdef1234567890"
        )
        print("状态已更新")

    # 再次查找以验证更新
    records = db.find_records_by_collection_and_filename("test_folder", "test.txt")
    print("更新后的查找结果:")
    for record in records:
        print(record)

    db.close()
    