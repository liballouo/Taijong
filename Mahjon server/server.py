from flask import Flask, request, jsonify
import response

app = Flask(__name__,static_folder='./', static_url_path='/',template_folder='./')

@app.route("/response/", methods=['GET'])
def response_from_model():

    # can_Chow = request.values['can_Chow']
    # if can_Chow:
    #     Chow_prob = response.Chow(request.values['throw'], request.values['hand_tiles'])

    # can_Pong = request.values['can_Pong']
    # if can_Pong:
    #     Pong_prob = response.Pong(request.values['throw'], request.values['hand_tiles'])
    
    # can_Kong = request.values['can_Kong']
    # if can_Kong:
    #     Kong_prob = response.Kong(request.values['throw'], request.values['hand_tiles'])

    result = response.discard_tile(request.values['hand_tiles'])
    return str(result)

@app.route("/discard_tile/", methods=['POST'])
def disacrd():
    try:
        data = request.json  # This will contain the parsed JSON data
        
        if "hand_tiles" in data:
            hand_tiles = data["hand_tiles"]
            # Process hand_tiles data here
            drop_tile_index = response.discard_tile(hand_tiles).indices
            
            return jsonify({"success": True, "message": "Data received and processed",
                                "action": "drop", "tile_index": drop_tile_index.item()})
        else:
            return jsonify({"success": False, "message": "hand_tiles data missing"})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/", methods=['GET'])
def index():
    return "connected"


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)