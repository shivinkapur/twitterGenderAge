
//db.follower_ids.ensureIndex( { "user_id": 1 } )

//print("id, name, screen_name, description, tweet")

//db.follower_ids.find().forEach(function(user){
//  print("#{user.user_id},#{user.name},#{user.screen_name},#{user.description},#{user.tweet}");
//})

cursor = db.follower_ids.find({user_id: 131621124});
while(cursor.hasNext()){
    print(cursor.next().user_id+","+cursor.next().name+","+cursor.next().screen_name+","+cursor.next().description+","+cursor.next().tweet);
}

