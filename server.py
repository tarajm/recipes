from flask_app import app
from flask_app.controllers import users_controllers
from flask_app.controllers import recipes_controllers
from flask_app.models.users_models import User
from flask_app.models.recipes_models import Recipe

if __name__=="__main__":
    app.run(debug=True)