#!/usr/bin/env python3
import re
import sqlite3
import shutil
from bs4 import BeautifulSoup


def generate_doc():
    """
    Generate AHK Docset
    """
    source_path = 'AutoHotkey_L-Docs/docs/'
    dest_path = 'Autohotkey.docset/Contents/Resources/Documents/'
    db_path = 'Autohotkey.docset/Contents/Resources/docSet.dsidx'

    shutil.rmtree(dest_path)
    shutil.copytree(source_path, dest_path)

    db = sqlite3.connect(db_path)
    cur = db.cursor()

    cur.execute('DROP TABLE IF EXISTS searchIndex;')

    cur.execute(
        r'CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')

    cur.execute(
        r'CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

    doc_path = 'autohotkey.docset/Contents/Resources/Documents'

    re_any = re.compile('.*')

    with open(doc_path + '/AutoHotkey.htm') as f:
        page = f.read()

    soup = BeautifulSoup(page)

    for tag in soup.find_all('a', attrs={'href': re_any}):
        name = tag.text.strip()

        if name:
            path = tag.attrs['href'].strip()

            if not path.startswith("http"):
                cur.execute(
                    'INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (name, 'Category', path))
                print('name: {}, path: {}'.format(name, path))

    print("------------------------------------------------------------------")

    with open(doc_path + '/commands/index.htm') as f:
        page = f.read()

    soup = BeautifulSoup(page)

    for tag in soup.find_all('a', attrs={'href': re_any}):
        name = tag.text.strip()

        if name:
            path = tag.attrs['href'].strip()

            cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)',
                        (name, 'Function', './commands/' + path))
            print('name: {}, path: {}'.format(name, path))

    db.commit()
    db.close()


if __name__ == "__main__":
    generate_doc()
