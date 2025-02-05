# import unittest
# from models.user import User
# from services.user import UserDBaseManagement
# from tests.database_test import FakeSQLAlchemyDBase

# from services.user import UserAuth

# #fake database

# class AuthTest(unittest.TestCase):
#     def test_usr_login():
#         pass

#     def test_admin_login():
#         pass

#     def test_usr_failed():
#         pass

#     def test_admin_failed():
#         pass


# class UserManagementTest(unittest.TestCase):
#     pass

# if __name__ == '__main__':
#     test_database = FakeSQLAlchemyDBase()
#     session = test_database.get_session()

#     usr_manager = UserDBaseManagement(session)
#     usr_manager.add_user('testusr', b'testusr', '21223', False)
#     usr_manager.delete_user('andrew')

#     usr_manager.save_changes()
#     test_database.list_user()
#     print('test executed')
