from canonicalwebteam.flask_base.app import FlaskBase

from webapp.webteam.views import webteam


app = FlaskBase(
    __name__,
    "random.webteam.space",
    template_folder="../templates",
    static_folder="../static",
    template_404="404.html",
    template_500="500.html",
)

app.register_blueprint(webteam)
