from flask import Blueprint, render_template, redirect, url_for, flash

from .users import require_login, github
from ..pagination import Paginator

starry = Blueprint("starry", __name__)


@starry.route("/", defaults={"page": 1})
@starry.route("/page/<int:page>")
@require_login
def index(page):
    resp = github.get("/user/starred?page={}".format(page))

    paginator = Paginator(resp, page)

    return render_template("index.html",
                           paginator=paginator,
                           repos=resp.data)


@starry.route("/unstar/<user>/<repo>")
@require_login
def unstar(user, repo):
    try:
        resp = github.request("/user/starred/{}/{}".format(user, repo),
                              data={}, format='json', method='DELETE')
    except ValueError:
        flash("You unstarred {}/{}.".format(user, repo))
        return redirect(url_for(".index"))