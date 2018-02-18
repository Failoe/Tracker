import psycopg2
import configparser


def pgsql_connect():
	config = configparser.ConfigParser()
	config.read('db.config')
	conn = psycopg2.connect(
		database=config['db']['database'],
		user=config['db']['user'],
		password=config['db']['password'],
		host=config['db']['host'],
		port=config['db']['port'])
	return conn


def drop(conn, tablename):
	try:
		cur = conn.cursor()
		cur.execute("DROP TABLE " + tablename)
		conn.commit()
	except:
		conn.commit()


def initialize_db(conn):
	init_cur = conn.cursor()

	drop(conn, "chatlog")
	init_cur.execute("""CREATE TABLE chatlog (
		author text,
		author_id bigint,
		content text,
		channel text,
		channel_id bigint,
		id bigint,
		embeds text,
		reactions text,
		channel_mentions text,
		role_mentions text,
		mentions text,
		guild text,
		guild_id bigint,
		created_at timestamp,
		edited_at timestamp
		);""")

	drop(conn, "reactionslog")
	init_cur.execute("""CREATE TABLE reactionslog (
		message_id bigint,
		reaction_emoji text,
		count smallint,
		emoji_id bigint,
		animated boolean
		);""")
	conn.commit()
	init_cur.close()
