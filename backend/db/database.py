from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib.parse  # Thêm thư viện này để mã hóa ký tự đặc biệt

# 1. NHẬP MẬT KHẨU CỦA BẠN VÀO ĐÂY (Kể cả có dấu #, @, ! cũng không sao)
my_password = "abc123!@#"

# 2. Hệ thống sẽ tự động mã hóa an toàn (VD: '#' thành '%23')
encoded_password = urllib.parse.quote_plus(my_password)

# Nếu không có mật khẩu (chuỗi rỗng ""), chuỗi kết nối sẽ tự động bỏ password đi
if encoded_password:
    SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://root:{encoded_password}@127.0.0.1:3306/fastvid_db"
else:
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@127.0.0.1:3306/fastvid_db"


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()