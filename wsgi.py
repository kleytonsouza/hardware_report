from base import app

#https://flask.palletsprojects.com/en/2.3.x/security/
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

response.set_cookie('username', 'flask', secure=True, httponly=True, samesite='Lax')

if __name__ == "__main__":
    app.run()
