from flask import Flask, render_template, redirect, url_for, request, flash
from models import db, Friend
from forms import FriendForm


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "change-this-secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///friends.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        friends = Friend.query.order_by(Friend.created_at.desc()).all()
        return render_template("index.html", friends=friends)

    @app.route("/add", methods=["GET", "POST"])
    def add_friend():
        form = FriendForm()
        if form.validate_on_submit():
            friend = Friend(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
            )
            db.session.add(friend)
            db.session.commit()
            flash("친구가 추가되었습니다.", "success")
            return redirect(url_for("index"))
        return render_template("edit_friend.html", form=form, title="친구 추가")

    @app.route("/edit/<int:friend_id>", methods=["GET", "POST"])
    def edit_friend(friend_id):
        friend = Friend.query.get_or_404(friend_id)
        form = FriendForm(obj=friend)
        if form.validate_on_submit():
            friend.name = form.name.data
            friend.email = form.email.data
            friend.phone = form.phone.data
            db.session.commit()
            flash("친구 정보가 수정되었습니다.", "success")
            return redirect(url_for("index"))
        return render_template("edit_friend.html", form=form, title="친구 수정")

    @app.route("/delete/<int:friend_id>", methods=["POST"])
    def delete_friend(friend_id):
        friend = Friend.query.get_or_404(friend_id)
        db.session.delete(friend)
        db.session.commit()
        flash("친구가 삭제되었습니다.", "info")
        return redirect(url_for("index"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)