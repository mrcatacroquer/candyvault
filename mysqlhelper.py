import pymysql

DBHOST = "localhost"
DATABASE = "candydb"
DBUSER= "candydbuser"
DBPASSWORD= "candudabpassword"

class MYSQLHelper:

	def __init__(self):
		try:
			connection = self.connect()
		finally:
			connection.close()

	def connect(self):
		return pymysql.connect(host=DBHOST,	user=DBUSER, passwd=DBPASSWORD, db=DATABASE)

	def get_user(self, email):
		query = "SELECT * FROM user WHERE mail='{0}';".format(email)
		return self.execute_select_one_query(query)

	def get_user_by_carduid(self, carduid):
		query = "SELECT * FROM user WHERE carduid='{0}';".format(carduid)
		return self.execute_select_one_query(query)

	def add_user(self, email, salt, hashed, is_admin, cardid):
		query = "INSERT INTO user (mail, salt, hashed, isadmin, carduid) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}');".format(email, salt, hashed, is_admin, cardid)
		self.execute_insert_query(query)

	def clear_all_users(self):
		query = "DELETE FROM user;"
		self.execute_insert_query(query)

	def add_reward(self, reward_owner, reward_guid, reward_timestamp):
		query = "INSERT INTO reward (owner, guid, granted) VALUES ('{0}', '{1}', '{2}');".format(reward_owner, reward_guid, reward_timestamp)
		print str(query)
		self.execute_insert_query(query)

	def delete_reward_by_user(self, owner_mail):
		query = "DELETE FROM reward WHERE owner='{0}';".format(owner_mail)
		self.execute_insert_query(query)

	def get_reward_by_carduid(self, reward_guid):
		query = "SELECT * FROM reward WHERE guid='{0}';".format(reward_guid)
		return self.execute_select_one_query(query)

	def get_reward_for_user(self, reward_owner):
		query = "SELECT * FROM reward WHERE owner='{0}';".format(reward_owner)
		return self.execute_select_one_query(query)

	def execute_insert_query(self, query):
		connection = self.connect()
		try:
			with connection.cursor() as cursor:
				cursor.execute(query)
				connection.commit()
		finally:
			connection.close()

	def execute_select_one_query(self, query):
		connection = self.connect()
		try:
			with connection.cursor() as cursor:
				cursor.execute(query)
				return cursor.fetchone()
		finally:
			connection.close()