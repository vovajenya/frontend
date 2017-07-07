import sqlite3

class DB_Handler():
    def create_db(self, name):
        # create a connection. if file doesn't exist, sqlite will create it
        conn = sqlite3.connect(name)

        # cursor
        c = conn.cursor()
        self.conn = conn
        self.c = c

        self.create_table()

    def read_all(self):
        c = self.c
        c.execute('SELECT * FROM stuffToPlot')
        data = c.fetchall()
        return data

    def read_all_as_dict(self):
        data = self.read_all()
        column_names = ['stock','link','origin','title']
        out_data = []

        for d in range(len(data)):
            an_item = dict(id=d+1, stock=data[d][0], link=data[d][1], origin=data[d][2], title=data[d][3])
            out_data.append(an_item)

        return out_data

    def get_links(self,symbol):
        c = self.c
        c.execute('SELECT * FROM stuffToPlot WHERE stock = ?', (symbol,))
        data = c.fetchall()
        return data


    def add_data(self, data):

        for d in data:
            for row in d:
                self.c.execute("INSERT INTO stuffToPlot (stock, link, origin, title) VALUES (?, ?, ?, ?)",
                               (row[0], row[1], row[2], row[3]))
            self.conn.commit()

    def create_table(self):
        # using caps for pure SQL language
        self.c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(stock TEXT, link TEXT, origin TEXT, title TEXT)')

    def clear_db(self):
        c = self.c
        c.execute('DROP TABLE IF EXISTS stuffToPlot')

    def build_new_db(self,name,data):
        self.create_db(name)
        self.clear_db()
        self.create_db(name)
        self.add_data(data)

