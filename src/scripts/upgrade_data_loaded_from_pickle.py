# Useful script to run when a new field has been added/removed from an entity and saved data needs to be refresh
import pickle

from src.entities.user_entity import UserEntity

PICKLE_FILE_LOCATION = "../../data/users.p"

users_by_id = pickle.load(open(PICKLE_FILE_LOCATION, "rb"))
new_users_by_id = {}

for user in users_by_id.values():
    new_users_by_id[user.id] = UserEntity(user.id, user.money, user.boosters_quantity, user.settings)

pickle.dump(new_users_by_id, open(PICKLE_FILE_LOCATION, "wb"))

print("Pickle upgrade done")