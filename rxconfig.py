import reflex as rx

class FutureAppConfig(rx.Config):
    pass

config = FutureAppConfig(
    app_name="futureapp",
    db_url="sqlite:///reflex.db",
    api_url="https://api.futureflixmedia.com",
    frontend_port="3001",
    backend_port="3002",
    #api_url="https://api.contextdemo.citrusberry.biz",
    #env=rx.Env.DEV,
)
