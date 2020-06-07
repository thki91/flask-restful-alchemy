from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel


# every resource is a class
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help='Every item needs a store id.'
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"message": "Item not found"}, 404

    def post(self, name):
        # fail fast
        if ItemModel.find_by_name(name):
            return {"message": "an item with name '{}' already exists.".format(name)}, 400
        # pass force=True to get_json ignores content type (content type can be invalid theoretically)
        data = Item.parser.parse_args()
        #data = request.get_json(silent=True) # surpresses error and returns None if content type is not application/json
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500

        return item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
