from flask import jsonify, request
from . import db
from .models import Card, Collection, Set


def bad_request(message):
    response = jsonify({"error": message})
    response.status_code = 400
    return response


def not_found(message):
    response = jsonify({"error": message})
    response.status_code = 404
    return response


def create_card_from_payload(payload, set_id):
    if not payload or "name" not in payload or "number" not in payload:
        return None
    return Card(name=payload["name"], number=payload["number"], set_id=set_id)


def create_set_from_payload(payload, collection_id):
    if not payload or "name" not in payload:
        return None

    new_set = Set(name=payload["name"], collection_id=collection_id)
    cards_payload = payload.get("cards")
    if isinstance(cards_payload, list):
        for card_payload in cards_payload:
            card = create_card_from_payload(card_payload, None)
            if card is not None:
                new_set.cards.append(card)
    return new_set


def register_routes(app):
    @app.route("/collections", methods=["GET"])
    def list_collections():
        collections = Collection.query.all()
        return jsonify([collection.to_dict() for collection in collections])

    @app.route("/collections", methods=["POST"])
    def create_collection():
        data = request.get_json(force=True, silent=True)
        if not data or "name" not in data:
            return bad_request("Missing required field: name")

        collection = Collection(name=data["name"])
        sets_payload = data.get("sets")
        if isinstance(sets_payload, list):
            for set_payload in sets_payload:
                set_item = create_set_from_payload(set_payload, None)
                if set_item is not None:
                    collection.sets.append(set_item)

        db.session.add(collection)
        db.session.commit()
        return jsonify(collection.to_dict()), 201

    @app.route("/collections/<int:collection_id>", methods=["DELETE"])
    def delete_collection(collection_id):
        collection = Collection.query.get(collection_id)
        if collection is None:
            return not_found("Collection not found")
        db.session.delete(collection)
        db.session.commit()
        return "", 204

    @app.route("/collections/<int:collection_id>", methods=["PATCH"])
    def update_collection(collection_id):
        collection = Collection.query.get(collection_id)
        if collection is None:
            return not_found("Collection not found")

        data = request.get_json(force=True, silent=True)
        if not data:
            return bad_request("Invalid JSON payload")

        if "name" in data:
            collection.name = data["name"]

        if "sets" in data:
            existing_sets = list(collection.sets)
            for existing_set in existing_sets:
                db.session.delete(existing_set)

            sets_payload = data.get("sets")
            if isinstance(sets_payload, list):
                for set_payload in sets_payload:
                    set_item = create_set_from_payload(set_payload, collection.id)
                    if set_item is not None:
                        collection.sets.append(set_item)

        db.session.commit()
        return jsonify(collection.to_dict())

    @app.route("/collections/<int:collection_id>/sets", methods=["GET"])
    def list_sets_by_collection(collection_id):
        collection = Collection.query.get(collection_id)
        if collection is None:
            return not_found("Collection not found")
        return jsonify([set_.to_dict() for set_ in collection.sets])

    @app.route("/sets", methods=["POST"])
    def create_set():
        data = request.get_json(force=True, silent=True)
        if not data or "name" not in data or "collectionId" not in data:
            return bad_request("Missing required fields: name, collectionId")

        collection = Collection.query.get(data["collectionId"])
        if collection is None:
            return not_found("Collection not found")

        set_item = Set(name=data["name"], collection_id=collection.id)
        cards_payload = data.get("cards")
        if isinstance(cards_payload, list):
            for card_payload in cards_payload:
                card = create_card_from_payload(card_payload, None)
                if card is not None:
                    set_item.cards.append(card)

        db.session.add(set_item)
        db.session.commit()
        return jsonify(set_item.to_dict()), 201

    @app.route("/sets/<int:set_id>", methods=["DELETE"])
    def delete_set(set_id):
        set_item = Set.query.get(set_id)
        if set_item is None:
            return not_found("Set not found")
        db.session.delete(set_item)
        db.session.commit()
        return "", 204

    @app.route("/sets/<int:set_id>", methods=["PATCH"])
    def update_set(set_id):
        set_item = Set.query.get(set_id)
        if set_item is None:
            return not_found("Set not found")

        data = request.get_json(force=True, silent=True)
        if not data:
            return bad_request("Invalid JSON payload")

        if "name" in data:
            set_item.name = data["name"]
        if "collectionId" in data:
            collection = Collection.query.get(data["collectionId"])
            if collection is None:
                return not_found("Collection not found")
            set_item.collection_id = collection.id
        if "cards" in data:
            existing_cards = list(set_item.cards)
            for existing_card in existing_cards:
                db.session.delete(existing_card)
            cards_payload = data.get("cards")
            if isinstance(cards_payload, list):
                for card_payload in cards_payload:
                    card = create_card_from_payload(card_payload, set_item.id)
                    if card is not None:
                        set_item.cards.append(card)

        db.session.commit()
        return jsonify(set_item.to_dict())

    @app.route("/cards", methods=["POST"])
    def create_card():
        data = request.get_json(force=True, silent=True)
        if not data or "name" not in data or "setId" not in data or "number" not in data:
            return bad_request("Missing required fields: name, setId, number")

        set_item = Set.query.get(data["setId"])
        if set_item is None:
            return not_found("Set not found")

        card = Card(name=data["name"], number=data["number"], set_id=set_item.id)
        db.session.add(card)
        db.session.commit()
        return jsonify(card.to_dict()), 201

    @app.route("/cards/<int:card_id>", methods=["DELETE"])
    def delete_card(card_id):
        card = Card.query.get(card_id)
        if card is None:
            return not_found("Card not found")
        db.session.delete(card)
        db.session.commit()
        return "", 204

    @app.route("/cards/<int:card_id>", methods=["PATCH"])
    def update_card(card_id):
        card = Card.query.get(card_id)
        if card is None:
            return not_found("Card not found")

        data = request.get_json(force=True, silent=True)
        if not data:
            return bad_request("Invalid JSON payload")

        if "name" in data:
            card.name = data["name"]
        if "number" in data:
            card.number = data["number"]
        if "setId" in data:
            set_item = Set.query.get(data["setId"])
            if set_item is None:
                return not_found("Set not found")
            card.set_id = set_item.id

        db.session.commit()
        return jsonify(card.to_dict())

    @app.route("/sets/<int:set_id>/cards", methods=["GET"])
    def list_cards_by_set(set_id):
        set_item = Set.query.get(set_id)
        if set_item is None:
            return not_found("Set not found")
        return jsonify([card.to_dict() for card in set_item.cards])
