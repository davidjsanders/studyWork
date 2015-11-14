from marshmallow_jsonapi import Schema, fields

class PostSchema(Schema):
    id = fields.Str(dump_only=True)
    title = fields.Str()

    author = fields.Relationship(
        related_url='/authors/{author_id}',
        related_url_kwargs={'author_id': '<author.id>'},
    )

    comments = fields.Relationship(
        related_url='/posts/{post_id}/comments',
        related_url_kwargs={'post_id': '<id>'},
        # Include resource linkage
        many=True, include_data=True,
        type_='comments'
    )

    class Meta:
        type_ = 'posts'
        strict = True

post_schema = PostSchema()
post_schema.dump(post).data
