import pymysql

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='team2')
cursor = db.cursor()
sql = ''' 
        CREATE TABLE users(
            id INT(11) AUTO_INCREMENT PRIMARY KEY, 
            firstname VARCHAR(100),
            lastname VARCHAR(100),
            email VARCHAR(100),
            password VARCHAR(100),
            register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
            ENGINE=InnoDB DEFAULT CHARSET=utf8;
    '''

cursor.execute(sql)
db.commit()
db.close() 