from flask import request, jsonify, session, Flask, redirect, session, url_for
from flask_login import login_user, login_required, logout_user, current_user
from api import app
from datetime import timedelta
from api.controllers import userController
from os import environ
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.consumer import oauth_authorized

print("hello")
app.secret_key = environ.get("APP_SECRET")
github_blueprint = make_github_blueprint(
    client_id = environ.get("GITHUB_ID"),
    client_secret = environ.get("GITHUB_SECRET")
)

app.register_blueprint(github_blueprint, url_prefix="/login")

# User
@app.route("/users", methods=['POST'])
def create_user():
    """
    Create user
    ---
    tags:
        - User
    parameters:
        -   in: body
            name: User
            required: true
            description: User object containing data for creation
            schema:
                $ref: "#/definitions/User"
    definitions:
        - schema:
            id: User
            properties:
                id:
                    type: integer
                    description: Id of the user. This property will be assigned a value returned by the database
                name:
                    type: string
                    description: Name of the user
                bio:
                    type: string
                    description: Biography of the user
                languages:
                    type: string
                    description: List of programming languages the user uses
                interests:
                    type: string
                    description: Interests of the user
                location:
                    type: string
                    description: Location of the user
                occupation:
                    type: string
                    description: Formal occupation, eg. student at X or works at Y
                projects:
                    type: array
                    description: List of projects
                    items:
                        $ref: "#/definitions/Project"
                links:
                    type: array
                    description: List of links
                    items:
                        $ref: "#/definitions/UserLink"
                project_feedbacks:
                    type: array
                    description: List of feedbacks given to projects
                    items:
                        $ref: "#/definitions/ProjectFeedback"
                user_feedbacks:
                    type: array
                    description: List of feedbacks given to users
                    items:
                        $ref: "#/definitions/UserFeedback"
                received_feedbacks:
                    type: array
                    description: List of received feedbacks from users
                    items:
                        $ref: "#/definitions/UserFeedback"
    responses:
        201:
            description: User created successfully
        400:
            description: Failed to create user
    """
    user = userController.create_user(**request.get_json())

    if user == None:
        return "Failed to create user.", 400
    else:
        return jsonify(user.as_dict()), 201

@app.route("/users/<id>", methods=['PUT'])
def update_user(id):
    """
    Update user
    Updates user with `id` using the data in request body
    ---
    tags:
        - User
    parameters:
        -   in: path
            name: id
            type: integer
            required: true
            description: Id of user to update
        -   in: body
            name: User
            required: true
            description: User object containing data to update
            schema:
                $ref: "#/definitions/User"
    responses:
        200:
            description: User updated successfully
        400:
            description: Failed to update user
    """
    if 'id' in request.get_json():
        return "Failed to update user. Request body can not specify user's id.", 400

    user = userController.update_user(id, **request.get_json())

    if user == None:
        return "Failed to update user.", 400
    else:
        return jsonify(user.as_dict()), 200

@app.route("/users/<id>", methods=['POST'])
@login_required
def update_user(id):
    if 'id' in request.get_json():
        return "", 501
    user = userController.update_user(id, **request.get_json())

    return jsonify(user.as_dict()), 200

@app.route("/users/<id>", methods=['GET'])
def get_user(id):
    """
    Get user
    Retreives user with `id`
    ---
    tags:
        - User
    parameters:
        -   in: path
            name: id
            type: integer
            required: true
            description: Id of the user to retrieve
    responses:
        200:
            description: User object
        404:
            description: User not found
    """
    user = userController.get_user(id=id)

    if user:
        return jsonify(user.as_dict()), 200
    else:
        return "", 404

@app.route("/users", methods=['GET'])
def get_all_users():
    """
    Get all users
    Retreives all users
    ---
    tags:
        - User
    responses:
        200:
            description: List of users
    """
    all_users = userController.get_all_users()

    users = [ user.as_dict() for user in all_users ]

    return jsonify(users), 200

@app.route("/users/<id>", methods=['DELETE'])
@login_required
def delete_user(id):
    """
    Delete user
    Deletes user with `id`
    ---
    tags:
        - User
    parameters:
        -   in: path
            name: id
            type: integer
            required: true
            description: Id of the user to delete
    responses:
        200:
            description: User deleted successfully
        401:
            description: Not allowed to delete the specified user
        404:
            description: User not found
    """
    if int(current_user.id) == int(id):
        user = userController.delete_user(id)

        if user:
            return "", 200
        else:
            return "", 404
    else:
        return "You cannot delete an other user", 401

# User Link
@app.route("/users/<user_id>/links", methods=['POST'])
def create_user_link(user_id):
    """
    Create user link
    ---
    tags:
        - UserLink
    parameters:
        -   in: body
            name: UserLink
            required: true
            description: User link object containing data to update
            schema:
                $ref: "#/definitions/UserLink"
    definitions:
        - schema:
            id: UserLink
            properties:
                id:
                    type: integer
                    description: Id of the user link. This property will be assigned a value returned by the database
                name:
                    type: string
                    description: Name of the user link
                url:
                    type: string
                    description: Url of the user link
                user_id:
                    type: integer
                    description: Id of the user
    responses:
        201:
            description: User link created successfully
        400:
            description: Failed to create user link
    """
    if 'user_id' in request.get_json():
        return "Failed to create user link. Request body can not specify link's user_id.", 400

    link = userController.create_link(user_id, **request.get_json())

    if link == None:
        return "Failed to create user link.", 400
    else:
        return jsonify(link.as_dict()), 201

@app.route("/users/<user_id>/links/<link_id>", methods=['PUT'])
def update_user_link(user_id, link_id):
    """
    Update user link
    Updates user link with `user_id` and `link_id` using the data in request body
    ---
    tags:
        - UserLink
    parameters:
        -   in: path
            name: user_id
            type: integer
            required: true
            description: Id of the user
        -   in: path
            name: link_id
            type: integer
            required: true
            description: Id of the user link to update
        -   in: body
            name: UserLink
            required: true
            description: User link object containing data to update
            schema:
                $ref: "#/definitions/UserLink"
    responses:
        200:
            description: User link updated successfully
        400:
            description: Failed to update user link
    """
    if 'user_id' in request.get_json():
        return "Failed to update user link. Request body can not specify link's user_id.", 400
    elif 'link_id' in request.get_json():
        return "Failed to update user link. Request body can not specify link's link_id.", 400

    link = userController.update_link(user_id, link_id, **request.get_json())

    if link == None:
        return "Failed to update user link.", 400
    else:
        return jsonify(link.as_dict()), 200

@app.route("/users/<user_id>/links", methods=['GET'])
def get_all_user_links(user_id):
    """
    Get all user links
    Retreives all user links with `user_id`
    ---
    tags:
        - UserLink
    parameters:
        -   in: path
            name: user_id
            type: integer
            required: true
            description: Id of the user
    responses:
        200:
            description: List of user links
    """
    all_links = userController.get_all_links(user_id)

    links = [ link.as_dict() for link in all_links ]

    return jsonify(links), 200

@app.route("/users/<user_id>/links/<link_id>", methods=['DELETE'])
def delete_user_link(user_id, link_id):
    """
    Delete user link
    Deletes user link with `user_id` and `link_id`
    ---
    tags:
        - UserLink
    parameters:
        -   in: path
            name: user_id
            type: integer
            required: true
            description: Id of the user
        -   in: path
            name: link_id
            type: integer
            required: true
            description: Id of the user link to delete
    responses:
        200:
            description: User link deleted successfully
        404:
            description: User link not found
    """
    link = userController.delete_link(user_id, link_id)

    if link == None:
        return "", 404
    else:
        return "", 200

# User Feedback
@app.route("/users/<user_id>/feedbacks", methods=['POST'])
def create_user_feedback(user_id):
    """
    Create user feedback
    ---
    tags:
        - UserFeedback
    parameters:
        -   in: body
            name: UserFeedback
            required: true
            description: User feedback object containing data to update
            schema:
                $ref: "#/definitions/UserFeedback"
    definitions:
        - schema:
            id: UserFeedback
            properties:
                id:
                    type: integer
                    description: Id of the user feedback. This property will be assigned a value returned by the database
                author_id:
                    type: integer
                    description: Id of the author
                user_id:
                    type: integer
                    description: Id of the user
                rating:
                    type: string
                    description: The rating of the user feedback
                description:
                    type: string
                    description: The body of the user feedback
    responses:
        201:
            description: User feedback created successfully
        400:
            description: Failed to create user feedback
    """
    if 'user_id' in request.get_json():
        return "Failed to create feedback. Request body can not specify feedback's user_id.", 400

    feedback = userController.create_feedback(user_id, **request.get_json())

    if feedback == None:
        return "Failed to create feedback.", 400
    else:
        return jsonify(feedback.as_dict()), 201

@app.route("/users/<user_id>/feedbacks", methods=['GET'])
def get_all_user_feedbacks(user_id):
    """
    Get all user feedbacks
    Retreives all user feedbacks with `user_id`
    ---
    tags:
        - UserFeedback
    parameters:
        -   in: path
            name: user_id
            type: integer
            required: true
            description: Id of the user
    responses:
        200:
            description: List of user feedbacks
    """
    all_feedbacks = userController.get_all_feedbacks(user_id)

    feedbacks = [ feedback.as_dict() for feedback in all_feedbacks ]

    return jsonify(feedbacks), 200

@app.route("/users/<user_id>/feedbacks/<feedback_id>", methods=['DELETE'])
def delete_user_feedback(user_id, feedback_id):
    """
    Delete user feedback
    Deletes user feedback with `user_id` and `feedback_id`
    ---
    tags:
        - UserFeedback
    parameters:
        -   in: path
            name: user_id
            type: integer
            required: true
            description: Id of the user
        -   in: path
            name: feedback_id
            type: integer
            required: true
            description: Id of the user feedback to delete
    responses:
        200:
            description: User feedback deleted successfully
        404:
            description: User feedback not found
    """
    feedback = userController.delete_feedback(user_id, feedback_id)

    if feedback == None:
        return "", 404
    else:
        return "", 200

@app.before_request
def before_sign_in():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=20)

@app.route("/login", methods=["GET"])
def login_route():
    account = request.args.get('account')
    session['action'] = "login"
    session['redirect'] = request.args.get('redirect')

    if account == 'github':
        return redirect(url_for("github.login"))
    else:
        return "", 400

@app.route("/register", methods=["GET"])
def register_route():
    account = request.args.get('account')
    session['action'] = "register"
    session['username'] = request.args.get('username')
    session['redirect'] = request.args.get('redirect')

    if account == 'github':
        return redirect(url_for("github.login"))
    else:
        return "", 400

@oauth_authorized.connect
def oathed(blueprint, token):
    if session['action'] == 'login':
        return login(blueprint)
    elif session['action'] == 'register':
        return register(blueprint)
    else:
        return "", 501

@app.route("/users/sign-out")
@login_required
def sign_out():
    logout_user()
    return "", 200

def login(blueprint):
    if blueprint.name == "github":
        resp = github.get("/user").json()
        id = resp["id"]
        user = userController.get_user(github_id=id)
        if user:
            login_user(user)
        return redirect(session['redirect'])

def register(blueprint):
    if blueprint.name == "github":
        resp = github.get("/user").json()
        id = resp["id"]
        user = userController.get_user(github_id=id)
        if not user:
            user = userController.create_user(github_id=id, name=session["username"])
            login_user(user)
        return redirect(session['redirect'])
