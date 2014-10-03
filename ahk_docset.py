#!/usr/bin/env python3
import re
import sqlite3
import shutil
from bs4 import BeautifulSoup


shutil.rmtree('autohotkey.docset/Contents/Resources/Documents/')
shutil.copytree('AutoHotkey_L-Docs/docs/', 'autohotkey.docset/Contents/Resources/Documents/')

db = sqlite3.connect('autohotkey.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

cur.execute('DROP TABLE IF EXISTS searchIndex;')

cur.execute(r'CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')

cur.execute(r'CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

doc_path = 'autohotkey.docset/Contents/Resources/Documents'

any = re.compile('.*')

with open(doc_path + '/index.html') as f:
    page = f.read()

soup = BeautifulSoup(page)

for tag in soup.find_all('a', {'href': any}):
    name = tag.text.strip()

    if len(name) > 0:
        path = tag.attrs['href'].strip()

        cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Category', path))
        print('name: {}, path: {}'.format(name, path))


with open(doc_path + '/commands/index.htm') as f:
    page = f.read()

soup = BeautifulSoup(page)

for tag in soup.find_all('a', {'href': any}):
    name = tag.text.strip()

    if len(name) > 0:
        path = tag.attrs['href'].strip()

        cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Function', './commands/' + path))
        print('name: {}, path: {}'.format(name, path))

db.commit()
db.close()
