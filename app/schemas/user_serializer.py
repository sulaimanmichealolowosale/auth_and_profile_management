def user_serializer(user) -> dict:
    return {
        "id":str(user['_id']),
        "username":user['username'],
        "email":user['email'],
        "created_at":user['created_at'],
    }