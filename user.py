class User:
	def __init__(self, email, is_admin):
		self.email = email
		self.is_admin = is_admin

	def get_id(self):
		return self.email

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True

	def is_admin_user(self):
		if self.is_admin:
			return True

		return False