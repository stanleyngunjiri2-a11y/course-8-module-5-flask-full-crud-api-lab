from flask import Flask, jsonify, request

app = Flask(__name__)


# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title
        }


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


# POST /events - Create a new event
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    # Check that JSON data was provided
    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    # Check that title was provided
    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Create a new ID
    new_id = max(event.id for event in events) + 1 if events else 1

    # Create and store the new event
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update an event title
@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    # Find the event
    event = next((event for event in events if event.id == id), None)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Check that title was provided
    if "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    # Update the title
    event.title = data["title"]

    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - Remove an event
@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    # Find the event
    event = next((event for event in events if event.id == id), None)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Remove the event from the list
    events.remove(event)

    return jsonify({
        "message": "Event deleted successfully",
        "event": event.to_dict()
    }), 200


if __name__ == "__main__":
    app.run(debug=True)