import discord
import asyncio
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
	conn.commit()
	init_cur.close()


class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged in as')
		print(self.user.name)
		print(self.user.id)
		# print(self.guilds)

		conn = pgsql_connect()
		# initialize_db(conn)
		cur = conn.cursor()

		for guild in self.guilds:
			if guild.name != "Reeeeeeeeeee":
				for channel in guild.channels:
					if isinstance(channel, discord.channel.TextChannel):
						print("{}: {}".format(guild.name, channel))

						cur3 = conn.cursor()
						while True:
							cur3.execute("""SELECT id FROM chatlog WHERE channel_id='{}' AND guild_id='{}' ORDER BY created_at ASC LIMIT 1""".format(
								channel.id, guild.id))
							try:
								firstmessage = discord.Object(cur3.fetchone()[0])
							except TypeError:
								firstmessage = None
								print("No first message found.")

							try:
								message_list = []
								first = True
								async for message in channel.history(limit=1000, before=firstmessage):
									first = False
									message_list.append((
										guild.id,
										message.author.name,
										message.author.id,
										message.content,
										message.channel.name,
										channel.id,
										message.id,
										message.embeds.__str__(),
										message.reactions.__str__(),
										message.channel_mentions.__str__(),
										message.role_mentions.__str__(),
										message.mentions.__str__(),
										message.guild.name,
										message.created_at,
										message.edited_at))
								if first is True:
									break
								args_str = b','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in message_list)
								cur.execute(b"INSERT INTO chatlog (guild_id, author, author_id, content, channel, channel_id, id, embeds, reactions, channel_mentions, role_mentions, mentions, guild, created_at, edited_at) VALUES " + args_str)
								conn.commit()
								print("Added rows.")

							except discord.errors.Forbidden as e:
								print(e)
								break
						cur3.close()

						cur2 = conn.cursor()
						cur2.execute("""SELECT id FROM chatlog WHERE channel_id='{}' AND guild_id='{}' ORDER BY created_at DESC LIMIT 1""".format(
							channel.id, guild.id))
						try:
							lastmessage = discord.Object(cur2.fetchone()[0])
						except TypeError:
							lastmessage = None
							print("No previous records found.")
						cur2.close()

						try:
							message_list = []
							first = True
							async for message in channel.history(limit=None, after=lastmessage):
								first = False
								# print(message.created_at, message.author.name, message.content)
								message_list.append((
									guild.id,
									message.author.name,
									message.author.id,
									message.content,
									message.channel.name,
									channel.id,
									message.id,
									message.embeds.__str__(),
									message.reactions.__str__(),
									message.channel_mentions.__str__(),
									message.role_mentions.__str__(),
									message.mentions.__str__(),
									message.guild.name,
									message.created_at,
									message.edited_at))
							if first is True:
								continue
							args_str = b','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in message_list)
							cur.execute(b"INSERT INTO chatlog (guild_id, author, author_id, content, channel, channel_id, id, embeds, reactions, channel_mentions, role_mentions, mentions, guild, created_at, edited_at) VALUES " + args_str)
							conn.commit()
							print("Completed.")
						except discord.errors.Forbidden as e:
							print(e)
		conn.close()
		print("Connection closed.")
		print('------')
		client.logout()
		client.close()


client = MyClient()
client.run(open('token.txt').read(), bot=False)
