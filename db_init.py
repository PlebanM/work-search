import sqlite3


conn = sqlite3.connect('python.db')
c = conn.cursor()


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(id INTEGER PRIMARY KEY, '
          'tittle TEXT, date_add TEXT, cash TEXT, adver TEXT,link TEXT, new TEXT)')
    conn.commit()

def clear_new():
    c.execute("UPDATE stuffToPlot SET new = ? WHERE new = new", (' '))
    conn.commit()


def data_entry(title, date, cash, adver, link):
    create_table()
    c.execute("INSERT INTO stuffToPlot (tittle, date_add, cash, adver, link, new) VALUES (?, ?, ?, ?, ?, ?)",
             (title, date, cash, adver, link, 'new'))
    conn.commit()


def find_record(link):
    c.execute("SELECT * FROM stuffToPlot WHERE link=?",
                (link,))
    showtext = c.fetchone()
    return showtext


def find_new(new='new'):
    c.execute("SELECT * FROM stuffToPlot WHERE new=?", (new,))
    newrecords = c.fetchall()
    return newrecords