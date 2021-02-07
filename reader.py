import json
import pprint


class DISCORD_READER:
	def __init__(self, messages_directory=""):
		self.messages_directory = messages_directory
		try:
			self.index = json.loads(open(str(self.messages_directory)+"index.json", "r").read())
		except Exception as e:
			print(e)
			input()
		self.discord_ids = list(self.index.keys())

	def get_username_from_id(self, discord_id):
		try:
			return self.index[str(discord_id)]
		except:
			return "Uknown discord_id"

	def get_id_from_username(self, username):
		for discord_id in self.discord_ids:
			if self.index[discord_id] == username:
				return discord_id
		return False

	def display_messages_from(self, username=False, discord_id=False):
		messages = self.get_messages_from(username=username, discord_id=discord_id)

		for m in messages:
			message = m[2]
			if message == "":
				message = m[3]
			print("{}: {}".format(self.get_username_from_id(m[0]), message))

	def get_messages_from(self, username=False, discord_id=False):
		if not discord_id:
			if username:
				discord_id = self.get_id_from_username(username)
			else:
				return False

		messages = open("{}{}/{}".format(self.messages_directory, discord_id, "messages.csv"), "r").read()
		lines = messages.split("\n")
		data = []
		for l in lines:
			info = l.split(",")
			if len(info) >= 4:
				if len(info) > 4:
					content = ""
					n_messages = len(info)-3
					for i in range(n_messages):
						content += info[i+2]
				else:
					content = info[2]

				sender_id = info[0]
				timestamp = info[1]
				atachment = info[len(info)-1]

				data.append([sender_id, timestamp, content, atachment])
			else:
				data[len(data)-1][2] += "\n -----------------" + info[0]
		return data

	def channel_menu(self, discord_id):
		channel_info = json.loads(open("{}{}/{}".format(self.messages_directory, discord_id, "channel.json"), "r").read())

		try:
			rec = channel_info["recipients"]
		except:
			print("Chat with {}".format(self.get_username_from_id(discord_id)))
		else:
			print("Recipients:")
			for u in rec:
				print(" -{}".format(self.get_username_from_id(u)))
		self.display_messages_from(discord_id=discord_id)

	def users_menu(self, max_ids=10):
		i = 0
		selection = "m"
		while True:
			if "a" in selection.lower():
				i = 0
				selection = "m"
			if "m" in selection.lower():
				for e in range(max_ids):
					user = self.discord_ids[i]
					print(" {}.{}".format(i, self.get_username_from_id(user)).replace("Direct Message with ", ""))
					i += 1
			selection = input()
			if not "m" in selection.lower():
				try:
					id_selected = int(selection)
				except:
					pass
					#print("Try with a number dumbass")
				else:
					discord_id = self.discord_ids[id_selected]
					self.channel_menu(discord_id)




d = DISCORD_READER()

d.users_menu()

input()