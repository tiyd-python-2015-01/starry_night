from functools import wraps

from flask import session, Blueprint, url_for, request, redirect, flash, render_template

from ..extensions import oauth


github = oauth.remote_app(
    'github',
    base_url='https://api.github.com',
    request_token_url=None,
    access_token_method='POST',
    authorize_url='https://github.com/login/oauth/authorize',
    access_token_url='https://github.com/login/oauth/access_token',
    app_key='GITHUB',
    request_token_params={'scope': 'user:email,repo,user:follow'}
)


@github.tokengetter
def get_github_token(token=None):
    return session.get('github_token')


def require_login(view):
    @wraps(view)
    def decorated_view(*args, **kwargs):
        if 'github_token' in session:
            return view(*args, **kwargs)
        else:
            return redirect(url_for("users.login"))

    return decorated_view


users = Blueprint("users", __name__)


@users.route("/login")
def login():
    return render_template("login.html")

@users.route("/logout")
def logout():
    session.pop('github_token', None)
    return redirect(url_for("starry.index"))


@users.route("/github/login")
def github_login():
    session.pop('github_token', None)
    return github.authorize(callback=url_for('.github_authorized',
                                             _external=True,
                                             next=request.args.get('next') or url_for("starry.index")))


@users.route('/github/authorized', methods=["GET", "POST"])
def github_authorized():
    next_url = request.args.get('next') or url_for('starry.index')
    resp = github.authorized_response()
    if resp is None:
        flash('You denied the request to sign in.')
        return redirect(next_url)

    session['github_token'] = (resp['access_token'],)
    me = github.get('/user')
    session['github_name'] = me.data['name']

    flash('You were signed in as %s' % repr(me.data['name']))
    return redirect(next_url)