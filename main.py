from email import message
from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

app = Flask(__name__)
api = Api(app=app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


db = SQLAlchemy(app=app)

## Database model
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    
    @classmethod
    def __repr__(cls) -> str:
        return f"Video(name = {cls.name}, views = {cls.views}, likes = {cls.likes})"

## NOTE: ONLY RUN ONCE, otherwise current database.db will be overwritten and data will be lost
# db.create_all() # Create database 

video_post_args = reqparse.RequestParser() # Create request parser object for parsing incoming requests
video_post_args.add_argument("name", type=str, help="Name of video required", required=True)
video_post_args.add_argument("views", type=int, help="View of video required", required=True)
video_post_args.add_argument("likes", type=int, help="Likes on video required", required=True)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of video required", required=False)
video_put_args.add_argument("views", type=int, help="View of video required", required=False)
video_put_args.add_argument("likes", type=int, help="Likes on video required", required=False)

# Create resource fields dict
resource_fields = {
    'id': fields.String,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):

    # marshal_with allows us to create an object that can be JSONified for response
    @marshal_with(resource_fields)
    def get(self, video_id):

        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with id {}".format(video_id))
        return result

    @marshal_with(resource_fields)
    def post(self, video_id):
        args = video_post_args.parse_args()
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        
        
        db.session.add(video)
        try:
            db.session.commit()
            return video, 201
        except exc.SQLAlchemyError:
            abort(409, message="Video id already exists")
    
    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        video_to_update = VideoModel.query.filter_by(id=video_id).first()
        
        if not video_to_update:
            abort(404, message="Could not find video with id {} to update".format(video_id))
        
        # Sloppy way to check if items exist in args, not scalable at all, 
        # TODO: Update this to be scalable, possbly using a set, or adding a helper function to video class
        if args['name']:
            video_to_update.name = args['name']
        if args['views']:
            video_to_update.views = args['views']
        if args['likes']:
            video_to_update.likes = args['likes']
        
        db.session.commit()
        
        return video_to_update, 200
        

    def delete(self, video_id):

        video_to_delete = VideoModel.query.filter_by(id=video_id).first()
        
        if not video_to_delete:
            abort(404, message="Could not find video with id {}".format(video_id))
        
        db.session.delete(video_to_delete)
        db.session.commit()
        
        return '', 204


api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
