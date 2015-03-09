from flask import Blueprint, render_template, redirect, url_for, flash

from .github import github, require_github_login
from ..pagination import Paginator

starry = Blueprint("starry", __name__)


@starry.route("/", defaults={"page": 1})
@starry.route("/page/<int:page>")
@require_github_login
def index(page):
    resp = github.get("/user/starred?page={}".format(page))

    paginator = Paginator(resp, page)

    return render_template("index.html",
                           paginator=paginator,
                           repos=resp.json())


@starry.route("/unstar/<user>/<repo>")
@require_github_login
def unstar(user, repo):
    resp = github.delete("/user/starred/{}/{}".format(user, repo))
    flash("You unstarred {}/{}.".format(user, repo))
    return redirect(url_for(".index"))