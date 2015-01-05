from __future__ import unicode_literals

from flask import request

from thornbush import models

from . import Resource, app, requires_auth


@app.route('/comments', methods=['POST'])
@requires_auth
def create_comment():
    payload = request.json
    comment = payload.get('comment')
    parent_id = payload.get('parent_id')
    comment = request.user.comment(text=comment, on=parent_id)
    models.Session.commit()
    response_body = dict(id=comment.guid, comment=comment.text)
    return Resource.render(response_body), 201


@app.route('/comments/<id>', methods=['GET'])
@requires_auth
def get_comment(id):
    return Resource.render(models.Comment.query.get(id).to_dict())
