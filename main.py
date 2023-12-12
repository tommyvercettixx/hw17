from flask import Flask, jsonify, request, render_template, redirect, url_for
from functions import jsonify_response, get_profiles_from_file, set_profiles_to_file
import uuid

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World"

@app.route("/profiles")
def get_profiles():
    profiles = get_profiles_from_file()
    return render_template('get_profiles.html', profiles=profiles)

@app.route("/profiles/<int:id>")
def get_profile_by_id(id):
    profiles = get_profiles_from_file()
    for profile in profiles:
        if profile.get("id") == id:
            return render_template('get_profile_by_id.html', profile=profile)
    return render_template('get_profile_by_id.html', profile=None, message=f"There is no profile with ID: {id}")

def create_profile():
    profiles = get_profiles_from_file()
    if request.method == "POST":
        login = request.form.get("login")
        for profile in profiles:
            if profile.get("login") == login:
                return render_template('create_profile.html', message="Login already exists, creation has failed.")

        account = request.form.get("account")
        nat = request.form.get("nationality")

        created_profile = {
            "id": str(uuid.uuid4()),
            "login": login,
            "account": account,
            "nationality": nat
        }

        profiles.append(created_profile)
        set_profiles_to_file(profiles)

        return redirect(url_for('get_profiles'))

    return render_template('create_profile.html', message=None)

@app.route("/profiles/update/<int:id>", methods=["GET", "POST"])
def update_profile_by_id(id):
    profiles = get_profiles_from_file()
    for profile in profiles:
        if profile.get("id") == id:
            if request.method == "POST":
                for key in request.form:
                    profile[key] = request.form[key]
                set_profiles_to_file(profiles)
                return redirect(url_for('get_profile_by_id', id=id))
            return render_template('update_profile_by_id.html', updated_profile=profile)

@app.route("/profiles/delete/<int:id>", methods=["GET", "POST"])
def delete_profile_by_id(id):
    profiles = get_profiles_from_file()
    for index, profile in enumerate(profiles):
        if profile.get("id") == id:
            if request.method == "POST":
                deleted_profile = profiles.pop(index)
                set_profiles_to_file(profiles)
                return redirect(url_for('get_profiles'))
            return render_template('delete_profile_by_id.html', deleted_profile=profile)
    return render_template('delete_profile_by_id.html', deleted_profile=None, message=f"Can't find profile with ID {id}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)