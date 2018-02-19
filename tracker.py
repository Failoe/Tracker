import discord
import asyncio
import psycopg2
import configparser
from trackerlib.db_utils import *


def blacklist_check(guild, channel, blacklist):
	try:
		if channel.name.lower() in blacklist[guild.name].split('\n')[1:]:
			return False
		else:
			return True
	except KeyError:
		return True


class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged in as: {0} (ID: {1})'.format(self.user.name, self.user.id))
		# print(self.guilds)
		config = configparser.ConfigParser()
		config.read('tracker.config')
		whitelist = config['Whitelist']
		blacklist = config['Blacklist']

		conn = pgsql_connect()
		# initialize_db(conn) # Do not turn on unless you're planning on wiping the database.
		cur = conn.cursor()

		for guild in self.guilds:
			if guild.name.lower() in [x for x in whitelist]:
				for channel in guild.channels:
					if (isinstance(channel, discord.channel.TextChannel) and channel.permissions_for(guild.me).read_messages) and ((channel.name.lower() in whitelist[guild.name].split('\n')[1:] or not whitelist[guild.name]) and blacklist_check(guild, channel, blacklist)):
						print("{}: #{}".format(guild.name, channel), end='')
						cur3 = conn.cursor()
						# Backlog logger
						firstmessage = None
						while True:
							if firstmessage is None:
								cur3.execute("""SELECT id FROM chatlog WHERE channel_id='{}' AND guild_id='{}' ORDER BY created_at ASC LIMIT 1""".format(
									channel.id, guild.id))
								try:
									firstmessage = discord.Object(cur3.fetchone()[0])
								except TypeError:
									firstmessage = None
									print("\nNo first message found. Starting at most recent message.")
							try:
								message_list = []
								count = 0
								async for message in channel.history(limit=1, before=firstmessage):
									count += 1
									message_list.append((
										guild.id,
										message.author.name,
										message.author.id,
										message.content,
										message.channel.name,
										channel.id,
										message.id,
										True if message.embeds else False,
										message.reactions.__str__() if message.reactions else None,
										message.channel_mentions.__str__() if message.channel_mentions else None,
										message.role_mentions.__str__() if message.role_mentions else None,
										message.mentions.__str__() if message.mentions else None,
										message.guild.name,
										message.created_at,
										message.edited_at))
									firstmessage = message
								if count == 0:
									break
								args_str = b','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in message_list)
								cur.execute(b"INSERT INTO chatlog (guild_id, author, author_id, content, channel, channel_id, id, embeds, reactions, channel_mentions, role_mentions, mentions, guild, created_at, edited_at) VALUES " + args_str)
								conn.commit()
								print(".", end="")
							except discord.errors.Forbidden as e:
								print(e)
								break
						cur3.close()


						# New message logger
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
							count = 0
							async for message in channel.history(limit=None, after=lastmessage):
								count += 1
								# print(message.created_at, message.author.name, message.content)
								message_list.append((
									guild.id,
									message.author.name,
									message.author.id,
									message.content,
									message.channel.name,
									channel.id,
									message.id,
									True if message.embeds else False,
									message.reactions.__str__() if message.reactions else None,
									message.channel_mentions.__str__() if message.channel_mentions else None,
									message.role_mentions.__str__() if message.role_mentions else None,
									message.mentions.__str__() if message.mentions else None,
									message.guild.name,
									message.created_at,
									message.edited_at))
							if count == 0:
								print(" <No new messages>")
								continue
							args_str = b','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in message_list)
							cur.execute(b"INSERT INTO chatlog (guild_id, author, author_id, content, channel, channel_id, id, embeds, reactions, channel_mentions, role_mentions, mentions, guild, created_at, edited_at) VALUES " + args_str)
							conn.commit()
							print(" [Added {} messages]".format(count))
						except discord.errors.Forbidden as e:
							print(e)
		conn.close()
		print("Data connection closed.")
		print('Data collection completed. It is safe to end the script.')
	# await client.wait_until_ready()
	# print("Test lol!")
	# # Use this to log messages as they come in
	# async def on_message():
	# 	print("New message posted.")


client = MyClient()
client.run(open('token.txt').read(), bot=False)
