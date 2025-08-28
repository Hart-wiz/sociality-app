# sociality-app

This is a social media app for social communication like facebook

# Social Media App Authentication with Django & JWT

In modern apps, users need to create accounts, login, and logout securely. Social media apps like Facebook use token-based authentication (like JWT) instead of traditional sessions. adn this is how this app sociality works.

Register – create a new user.

Login – get a token for authentication.

Logout – invalidate the token so it can’t be used.

Auth API – Django REST Framework (JWT)

Base path: (from your snippet) /<app>/
If you mount this under a project prefix like /api/v1/auth/, just prepend that to each route in the docs/tests.

Endpoints Overview
Endpoint Methods Auth Description
api/v1/register/ POST Public Register a new user and return JWT tokens
api/v1/login/ POST Public Login with username or email + password; returns JWT tokens
api/v1/logout/ POST Bearer JWT (access) Blacklist a refresh token
api/v1/me/ PUT, PATCH Bearer JWT (access) Update the logged-in user (via MeUpdateSerializer)

Note: Your current MeUpdateView is an UpdateAPIView (PUT/PATCH). If you also want GET /me/, I include a tiny view at the end you can add in seconds.

# Request/Response Examples

1. ## Register — POST api/v1/register/

Request (JSON)

        {
        "username": "james_wisdom",
        "email": "james@example.com",
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

Quick cURL Cheatsheet

# Register

curl -X POST http://127.0.0.1:8000/api/v1/register/ \
 -H "Content-Type: application/json" \
 -d '{"username":"james_wisdom","email":"james@example.com","password":"StrongPass!234"}'

# Login

curl -X POST http://127.0.0.1:8000/api/v1/login/ \
 -H "Content-Type: application/json" \
 -d '{"email":"james@example.com","password":"StrongPass!234"}'

# Logout (needs access)

curl -X POST http://127.0.0.1:8000/api/v1/logout/ \
 -H "Authorization: Bearer ACCESS_TOKEN" \
 -H "Content-Type: application/json" \
 -d '{"refresh":"REFRESH_TOKEN"}'

# Update Me (PATCH)

curl -X PATCH http://127.0.0.1:8000/api/v1/me/ \
 -H "Authorization: Bearer ACCESS_TOKEN" \
 -H "Content-Type: application/json" \
 -d '{"bio":"Startup builder"}'

<!-- .........................social app................ -->

_Posts (CRUD via PostViewSet)_

_User detail by username (UserDetail)_

_Update current user (MeUpdate)_

_Follow/Unfollow (FollowToggle)_

_Feed (paginated, followed users + self)_

Social API — Docs (DRF + SimpleJWT)

**Base URL (dev): http://127.0.0.1:8000/api/v1/**
**Auth: Bearer JWT for protected endpoints**

Endpoints Overview
Endpoint Methods Auth Description
/posts/ GET, POST GET = Public, POST = Auth List posts / Create post
/posts/{id}/ GET, PUT, PATCH, DELETE GET = Public; write = Author only Retrieve/Update/Delete a post
/users/{username}/ GET Public Public user profile + follower/following counts
/users/me/ PUT, PATCH Auth Update current user (partial/full)
/users/{user_id}/follow/ POST, DELETE Auth Follow (POST) / Unfollow (DELETE) a user
/feed/ GET Auth Posts from followed users + own posts (paginated)

Permissions reflected from code:

Posts: IsAuthenticatedOrReadOnly + custom IsAuthorOrReadOnly

Follow/Unfollow, Feed, MeUpdate: IsAuthenticated

UserDetail: public

PostSerializer (example)
{
"id": 123,
"author": {
"id": 7,
"username": "james_wisdom"
},
"content": "Hello world",
"image_url": null,
"created_at": "2025-08-26T18:30:00Z",
"updated_at": "2025-08-26T18:30:00Z"
}

UserPublicSerializer (example)
{
"id": 7,
"username": "james_wisdom",
"email": "james@example.com",
"bio": "Startup builder",
"avatar_url": "https://example.com/a.jpg",
"followers_count": 12,
"following_count": 7,
"date_joined": "2025-08-20T10:05:00Z"
}

MeUpdateSerializer — request (example)
{
"first_name": "James",
"last_name": "Wisdom",
"bio": "Startup builder",
"avatar_url": "https://example.com/new.png"
}

# Posts

List / Create — GET | POST /api/v1/posts/

GET (public) — paginated list

POST (auth) — create; author is set automatically (perform_create)

Create Request

    {
      "content": "Hello world",
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

Retrieve / Update / Delete — GET | PUT | PATCH | DELETE /api/v1/posts/{id}/

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

# Users

## Public Detail — GET /api/v1/users/{username}/

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

## Update Current User — PUT | PATCH /api/v1/users/me/ (auth)

Updates the authenticated user using MeUpdateSerializer.

PATCH Request

{ "bio": "Building Africa's biggest startup hub" }

200 OK (returns updated user fields as defined by your serializer)

# **Follow / Unfollow**

## Follow — POST /api/v1/follow/{user_id} (auth)

Follows the target user.

Prevents following self.

Idempotent via get_or_create.

Responses

204 No Content on success

400 if trying to follow yourself: {"detail":"You cannot follow yourself."}

404 if target user missing: {"detail":"User not found."}

## Unfollow — DELETE /api/v1/follow/{user_id} (auth)

Removes follow relationship (if exists).

204 No Content (idempotent even if nothing to delete)

# .............Feed...............

List Feed — GET /api/v1/feed/ (auth)

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

cURL Quick Tests

# List posts (public)

curl :8000/api/v1/posts/

# Create post (auth)

curl -X POST :8000/api/v1/posts/ \
 -H "Authorization: Bearer ACCESS_TOKEN" \
 -H "Content-Type: application/json" \
 -d '{"content":"Hello world"}'

# Retrieve user by username (public)

curl :8000/api/v1/users/james_wisdom/

# Update me (PATCH)

curl -X PATCH :8000/api/v1/users/me/ \
 -H "Authorization: Bearer ACCESS_TOKEN" \
 -H "Content-Type: application/json" \
 -d '{"bio":"Startup builder"}'

# Follow user_id=9

curl -X POST :8000/api/v1/users/9/follow/ \
 -H "Authorization: Bearer ACCESS_TOKEN"

# Unfollow user_id=9

curl -X DELETE :8000/api/v1/users/9/follow/ \
 -H "Authorization: Bearer ACCESS_TOKEN"

# Feed (auth)

curl :8000/api/v1/feed/ \
 -H "Authorization: Bearer ACCESS_TOKEN"

If your usernames can contain spaces or special chars, expose a slug field or change lookup_field accordingly.
