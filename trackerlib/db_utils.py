import psycopg2
import configparser


def pgsql_connect(config_path):
	config = configparser.ConfigParser()
	config.read(config_path)
	conn = psycopg2.connect(
		database=config['PostgreSQL']['database'],
		user=config['PostgreSQL']['user'],
		password=config['PostgreSQL']['password'],
		host=config['PostgreSQL']['host'],
		port=config['PostgreSQL']['port'])
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

	init_cur.execute("""CREATE TABLE reactionslog (
		message_id bigint,
		reaction_emoji text,
		count smallint,
		emoji_id bigint,
		animated boolean
		);""")
	conn.commit()
	init_cur.close()


def build_roles_table(conn):
	init_cur = conn.cursor()
	init_cur.execute("""CREATE TABLE roles (
		guild_id bigint,
		role text,
		role_id bigint,
		UNIQUE (guild_id, role_id)
		);""")
	conn.commit()
	init_cur.close()


def build_user_role_table(conn):
	init_cur = conn.cursor()
	# drop(conn, 'user_roles')
	init_cur.execute("""CREATE TABLE IF NOT EXISTS user_roles (
		guild_id bigint,
		user_id bigint,
		role_id bigint,
		UNIQUE (guild_id, user_id, role_id)
		);""")
	conn.commit()
	init_cur.close()


def build_user_name_table(conn):
	init_cur = conn.cursor()
	# drop(conn, 'user_names')
	init_cur.execute("""CREATE TABLE IF NOT EXISTS user_names (
		guild_id bigint,
		user_id bigint,
		member_name text,
		display_name text,
		UNIQUE (guild_id, user_id)
		);""")
	conn.commit()
	init_cur.close()
