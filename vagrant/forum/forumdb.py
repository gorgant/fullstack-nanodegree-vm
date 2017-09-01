# "Database code" for the DB Forum.

import datetime, psycopg2

POSTS = []

def get_posts():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect("dbname=forum")
  c = db.cursor()
  query = "SELECT content, time FROM posts ORDER BY time DESC"
  c.execute(query)
  rows = c.fetchall()
  POSTS = rows
  db.close()
  return POSTS

def add_post(content):
  POSTS.append((content, datetime.datetime.now()))
  """Add a post to the 'database' with the current timestamp."""
  sql = """INSERT INTO posts(content) VALUES(%s);"""
  db = psycopg2.connect("dbname=forum")
  c = db.cursor()
  c.execute(sql,(content,))
  db.commit()
  db.close()