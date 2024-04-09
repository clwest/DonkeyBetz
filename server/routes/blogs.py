import os
from dotenv import load_dotenv
import re
import logging
from datetime import datetime

# Flask configuration
from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request, jsonify
from flask_jwt_extended import jwt_required

# Helpers and other functions
from factory.limiter_factory import limiter
from helpers.constants import *
from helpers.helper_permissions import *
from models.blogs import Post
from schemas.blogs import *
import helpers.custom_exceptions as ce
import helpers.helper_functions as hf
from factory.app_factory import jwt

load_dotenv()

# index_name = os.getenv("PINECONE_INDEX")
jwt_secret = os.getenv("JWT_SECRET_KEY")
# logging.info(f"Pinecone index name Blog.py: {index_name}")

blog_blp = Blueprint("blog", "blog", url_prefix="/api/blog")
post_schema = PostSchema()


# Get all blog posts

@blog_blp.route("/posts", methods=["GET"])
class GetAllPostsAPI(MethodView):
    # @jwt_required()
    def get(self):
        posts = Post.query.all()
        for post in posts:
            print(f"Printing post data: {post}")
            print(f"Printing from blog routes {post.user}")
        post_schema = PostSchema(many=True)
        return jsonify(post_schema.dump(posts)), 200


# Create a new blog post
@blog_blp.route("/posts", methods=["POST"])
class CreatePostAPI(MethodView):
    @jwt_required()
    def post(self):
        user_identity = get_jwt_identity()
        user_id = user_identity["id"]

        data = request.json
        data["user_id"] = user_id
        logging.info(f"Data from blog post: {data}")
        validated_data, errors = hf.validate_data(post_schema, data)
        if errors:
            raise ce.BadRequestError("Invalid request", errors)

        title = validated_data.get("title")
        logging.info(f"Title from Blog post: {title}")

        new_post = Post(**validated_data)
        new_post.generate_slug()
        hf.add_to_db(new_post)
        return jsonify(post_schema.dump(new_post)), 201


# Get a blog post by ID
@blog_blp.route("/posts/<string:slug>", methods=["GET"])
class GetPostAPI(MethodView):
    # @jwt_required()
    def get(self, slug):
        post = Post.query.filter_by(slug=slug).first()
        if not post:
            raise ce.ResourceNotFoundError("Post not found", 404)
        return jsonify(post_schema.dump(post)), 200


# Update a blog post
@blog_blp.route("/posts/<string:slug>", methods=["PUT"])
class UpdatePostAPI(MethodView):
    def put(self, slug):
        post = Post.query.filter_by(slug=slug).first()
        if not post:
            raise ce.ResourceNotFoundError("Post not found", 404)
        data = request.json
        validated_data, errors = hf.validate_data(post_schema, data)
        if errors:
            return jsonify(errors), 400
        for key, value in validated_data.items():
            setattr(post, key, value)
        hf.update_db()
        return jsonify(post_schema.dump(post)), 200


# Delete a blog post
@blog_blp.route("/posts/<string:slug>", methods=["DELETE"])
class DeletePostAPI(MethodView):
    def delete(self, slug):
        post = Post.query.filter_by(slug=slug).first()
        if not post:
            raise ce.ResourceNotFoundError("Post not found", 404)
        hf.delete_from_db(post)
        return jsonify({"message": "Post deleted successfully"}), 200
