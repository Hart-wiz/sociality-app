# sociality-app

This is a social media api for social communication

# Social Media App Authentication with Django & JWT

In modern apps, users need to create accounts, login, and logout securely. Social media apps like Facebook use token-based authentication (like JWT) instead of traditional sessions and this is how this app sociality works.

Register – create a new user.

Login – get a token for authentication.

Logout – invalidate the token so it can’t be used.

Auth API – Django REST Framework (JWT)

Base path: (from your snippet) /<app>/
If you mount this under a project prefix like /api/v1/auth/, just prepend that to each route in the docs/tests.

## Endpoints Overview

Endpoint Methods Auth Description
api/v1/register/ POST Public Register a new user and return JWT tokens
api/v1/login/ POST Public Login with username or email + password; returns JWT tokens
api/v1/logout/ POST Bearer JWT (access) Blacklist a refresh token
api/v1/me/ PUT, PATCH Bearer JWT (access) Update the logged-in user (via MeUpdateSerializer)

# API END POINTS

# ....................... AUTH ..................................

1. ## Register — POST api/v1/register/

Request (JSON)

        {
       "username": "james_wisdom",
        "email": "james@example.com"
        "password": "StrongPass!234"
        }

201 Created

        {
        "user": {
            "id": 7,
            "username": "james_wisdom",
            "email": "james@example.com"
        },
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..."
        }

400 Bad Request

        {"detail": "Validation error details..."}

2. ## Login — POST api/v1/login/

Login by username:

        {
        "username": "james_wisdom",
        "password": "StrongPass!234"
        }

or by email:

        {
        "email": "james@example.com",
        "password": "StrongPass!234"
        }

200 OK

        {
        "user": { "id": 7, "username": "james_wisdom", "email": "james@example.com" },
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..."
        }

400 Bad Request

        {"detail": "Invalid credentials"}

3. ## Logout — POST api/v1/logout/ (requires Bearer access token)

Headers: Authorization: Bearer <ACCESS_TOKEN>

Body

        {"refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1..."}

205 Reset Content – refresh token blacklisted

400 Bad Request – missing/invalid refresh, or blacklist app not enabled

Ensure rest_framework_simplejwt.token_blacklist is in INSTALLED_APPS and migrations applied.

4. ## Update Me — PUT|PATCH api/v1/me/ (requires Bearer access token)

Headers: Authorization: Bearer <ACCESS_TOKEN>

        {
        "first_name": "James",
        "last_name": "Wisdom",
        "bio": "Startup builder",
        "avatar_url": "https://example.com/a.jpg"
        }

200 OK

        {
        "id": 7,
        "username": "james_wisdom",
        "email": "james@example.com",
        "first_name": "James",
        "last_name": "Wisdom",
        "bio": "Startup builder",
        "avatar_url": "https://example.com/a.jpg"
        }

401 Unauthorized – missing/invalid token
400 Bad Request – validation errors

# ........................... Posts.....................................

1. ## List / Create — GET | POST /api/v1/posts/

GET (public) — paginated list

POST (auth) — create; author is set automatically (perform_create)

Create Request

    {
      "content": "Hello world my first post created",
      "image_url": null
    }

Create Response — 201

    {
      "id": 124,
      "author": {"id": 7, "username": "james_wisdom"},
      "content": "Hello world",
      "image_url": null,
      "created_at": "2025-08-26T18:31:00Z",
      "updated_at": "2025-08-26T18:31:00Z"
    }

2. ## Retrieve / Update / Delete — GET | PUT | PATCH | DELETE /api/v1/posts/{id}/

GET (public)

PUT|PATCH|DELETE — author only (IsAuthorOrReadOnly)

Update (PATCH) Request

    { "content": "Edited body" }

Update Response — 200

    {
      "id": 124,
      "author": {"id": 7, "username": "james_wisdom"},
      "content": "Edited body",
      "image_url": null,
      "created_at": "2025-08-26T18:31:00Z",
      "updated_at": "2025-08-26T18:40:00Z"
    }

Delete — 204 No Content

# ...................................Users..........................................

1. ## Public Detail — GET /api/v1/users/{username}/

Returns public profile + follower/following counts (via queryset annotations).

200 OK

{
"id": 7,
"username": "james_wisdom",
"email": "james@example.com",
"bio": "Startup builder",
"avatar_url": "https://example.com/a.jpg",
"followers_count": 12,
"following_count": 7
}

404 if username not found.

2. ## Update Current User — PUT | PATCH /api/v1/users/me/ (auth)

Updates the authenticated user using MeUpdateSerializer.

PATCH Request

{ "bio": "Building Africa's biggest startup hub" }

200 OK (returns updated user fields as defined by your serializer)

# **Follow / Unfollow**

1. ## Follow — POST /api/v1/follow/{user_id} (auth)

Follows the target user.

Prevents following self.

Idempotent via get_or_create.

Responses

204 No Content on success

400 if trying to follow yourself: {"detail":"You cannot follow yourself."}

404 if target user missing: {"detail":"User not found."}

2. ## Unfollow — DELETE /api/v1/follow/{user_id} (auth)

Removes follow relationship (if exists).

204 No Content (idempotent even if nothing to delete)

# .......................Feed..........................

## List Feed — GET /api/v1/feed/ (auth)

Returns posts from users you follow + your own posts. Ordered newest first. Paginated.

Query params

page — page number

page_size — override page size (default 10, max 50)

200 OK (PageNumberPagination example)

        {
        "count": 34,
        "next": "http://127.0.0.1:8000/api/v1/feed/?page=2",
        "previous": null,
        "results": [
            {
            "id": 201,
            "author": {"id": 8, "username": "fresh_user"},
            "content": "Morning!",
            "image_url": null,
            "created_at": "2025-08-26T07:00:00Z",
            "updated_at": "2025-08-26T07:00:00Z"
            }
        ]

}
