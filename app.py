@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    # Find the event
    event = next((event for event in events if event.id == id), None)

    if event is None:
        return jsonify({"error": "Event not found"}), 404

    # Remove the event from the list
    events.remove(event)

    return "", 204