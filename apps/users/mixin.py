from exam import fixture
from faker import Faker

class UserMixin(object):

    def create_user_data(self):
        fake = Faker()
        base_password = fake.password()
        user_data = {
            'username': fake.user_name(),
            'first_name': fake.name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'password1': base_password,
            'password2': base_password,
        }
        return user_data

    @fixture
    def user(self):
        return self.create_user_data()