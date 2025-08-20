Table users_user {
  id bigserial [pk]
  username varchar(150) [not null, unique]
  email varchar(254) [unique]
  password varchar(128) [not null]
  bio varchar(160) [default: '']
  avatar_url text
  date_joined timestamp [not null, default: `now()`]
  last_login timestamp
}

Table social_post {
  id bigserial [pk]
  author_id bigint [not null, ref: > users_user.id]
  content text [not null]
  Media_url text [not null]
  created_at timestamp [not null, default: `now()`]
  updated_at timestamp [not null, default: `now()`]
  -- Note: 'Body length must be between 1 and 1000 characters'
}

Table social_follow {
  id bigserial [pk]
  follower_id bigint [not null, ref: > users_user.id]
  following_id bigint [not null, ref: > users_user.id]
  created_at timestamp [not null, default: `now()`]
  Indexes {
    (follower_id, following_id) [unique]
    follower_id
    following_id
  }
  -- Note: 'Follower cannot be the same as Following (no self-follow)'
}

Table social_comment {
  id bigserial [pk]
  post_id bigint [not null, ref: > social_post.id]
  author_id bigint [not null, ref: > users_user.id]
  body text [not null]
  created_at timestamp [not null, default: `now()`]
  Indexes {
    (post_id, created_at)
    (author_id, created_at)
  }
  -- Note: 'Body length must be between 1 and 1000 characters'
}

Table social_message {
  id bigserial [pk]
  sender_id bigint [not null, ref: > users_user.id]
  recipient_id bigint [not null, ref: > users_user.id]
  body text [not null]
  created_at timestamp [not null, default: `now()`]
  read_at timestamp
  Indexes {
    (sender_id, recipient_id, created_at)
    (recipient_id, read_at)
  }
  -- Note: 'Direct messages between users; optionally enforce sender follows recipient at app layer'
}
