import vertexai
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel
import json
import time

def load_data():
    data = None
    with open("/Users/ramymoussa/projects/bcw24/voice-tune/src/integrations/data.json") as f:
        data = json.loads(f.read())
    return data

def init_generative_model(project_id: str, location: str):
    vertexai.init(project=project_id, location=location)
    multimodal_model = GenerativeModel("gemini-1.0-pro-001")
    return multimodal_model

def build_model():
    model = init_generative_model("bosch-bcx-hack24ber-2305", "europe-west2")
    get_game_time_func = generative_models.FunctionDeclaration(
        name="get_device_settings_from_query",
        description="Determine the direction of the movement of a chair and how much it should be moved. For example, 'move the seat forward by 20 degrees' or 'move the seat backward by a bit' or 'move the seat forward by a little' or 'move the seat forward by a lot'. Other ambiguous sentences that contains planet names or other irrelevant information will be considered invalid.",
        parameters={
            "type": "object",
            "properties": {
                # "position": {
                #     "type": "string",
                #     "description": "The position to set, for example '20 degrees forward' or '20 degrees backward' or a bit"
                # },
                "device": {
                    "type": "string",
                    "enum": ["seat",],
                    "description": "The device to control, for example 'seat' or 'temperature'"
                },
                "degree": {
                    "type": "integer",
                    "description": "The degree to set, for example 20 or 30 or a little, it's a numeric value that starts from one if the prompt has a little or a bit"
                },
                "direction": {
                    "type": "string",
                    "enum": ["forward", "backward", "up", "down", "invalid"],
                    "description": "The direction to set, for example 'forward' or 'backward', 'up', 'down', or 'invalid'"
                },
                "response": {
                    "type": "string",
                    "description": "To be passed back to Text to Speech as a verification for taking an action." +
                     "examples: 'Okay.. Moving the seat forward by 20 degrees', 'I'm moving the seat backwards by a bit' or 'I didn't understand that, can you repeat?'." +
                     " When the direction or the query doesn't make sense or is invalid, the response can be something like this: 'I didn't understand that, can you repeat?'."
                },
            },
            "required": ["query", "device", "response", "direction"]
        },
    )

    gametime_tool = generative_models.Tool(
        function_declarations=[get_game_time_func]
    )
    # Example query
    # q = "move the seat forward by 5 dgrees."
    # model_response = model.generate_content(
    #     q,
    #     generation_config={"temperature": 0},
    #     tools=[gametime_tool],
    # )
    # args = model_response.candidates[0].content.parts[0].function_call.args.pb
    return gametime_tool, model


def check_accuracy(predicted, truth):
    if predicted == None or predicted == 0:
        return 1
    if (isinstance(predicted, str)):
        return 1 if (predicted.lower() == truth.lower()) or predicted.lower() in truth.lower() else 0
    return 1 if (predicted < 5 or predicted == truth) else 0


def train_model(data, model, gametime_tool):
    # Process each query
    correct_directions, correct_degrees, total_queries = 0, 0, len(data)
    for record in data:
        # Call the model for inference
        model_response = model.generate_content(
            record.get('prompt'),
            generation_config={"temperature": 0.15},
            tools=[gametime_tool],
        )
        if (not model_response.candidates[0].content.parts[0].function_call.args):
            predicted_direction = None
            predicted_degree = 0
        else:
            print(f"{record.get('prompt')}")
            args = model_response.candidates[0].content.parts[0].function_call.args.pb
            print(args)
            predicted_direction = args.get("direction").string_value
            predicted_degree = 1
            if (args.get("degree")):
                predicted_degree = float(args.get("degree").number_value)

        # Calculate accuracies
        direction_accuracy = check_accuracy(predicted_direction, record.get('action'))
        degree_accuracy = check_accuracy(predicted_degree, record.get('value'))
        correct_directions += direction_accuracy
        correct_degrees += degree_accuracy

        # Log to wandb table
        # results_table.add_data(query, predicted_sport.lower(), predicted_team.lower(), truth_sport.lower(), truth_team.lower())
        time.sleep(5)

    # Calculate and log overall accuracies
    overall_sport_accuracy = correct_directions / total_queries
    overall_team_accuracy = correct_degrees / total_queries

    print(overall_sport_accuracy)
    print(overall_team_accuracy)


def predict(model, gametime_tool, prompt):
    model_response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.15},
        tools=[gametime_tool],
    )
    try:
        if (not model_response.candidates[0].content.parts[0].function_call.args):
            return None, None, 0
        args = model_response.candidates[0].content.parts[0].function_call.args.pb
        print(args)
        predicted_direction = args.get("direction").string_value
        predicted_response = args.get("response").string_value
        if (not args.get("degree")):
            return predicted_response, predicted_direction, 1
        predicted_degree = float(args.get("degree").number_value)
        return predicted_response, predicted_direction, predicted_degree
    except Exception as e:
        print(e)
        return None, None, 0