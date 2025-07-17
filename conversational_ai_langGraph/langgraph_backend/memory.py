from collections import defaultdict

_user_memories = defaultdict(dict)
 
def get_user_memory(user_id):
    return _user_memories[user_id] 