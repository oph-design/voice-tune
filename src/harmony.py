import asyncio
from integrations import (
    speech_to_text,
    init_generative_model,
    query_model,
    train_model,
    load_data,
    build_model,
    predict,
    # text_to_speech,
    seat_controller,
)


async def main():
    speech = speech_to_text()
    print(f"Speech: {speech}")
    tool, model = build_model()
    prediction = predict(model, tool, speech)
    print(f"Prediction: {prediction}")
    # text_to_speech(prediction[0] if prediction[0] is not None else "I'm sorry, I didn't understand that.")
    if (prediction[1] is not None):
        await seat_controller.seat_control(prediction[1], prediction[2])
    ## TODO: I think we should initialize the model once in the beginning of the program, not everytime we want to use it
    # multimodal_model = init_generative_model("bosch-bcx-hack24ber-2305", "europe-west2")
    # response = query_model(multimodal_model, speech)
    # data = load_data()
    # tool, model = build_model()
    # train_model(data, model, tool)
    # test_data = [
    #     "make a 20 degrees cake and skip the red line",
    #     "blow a candle forwards by 21 degrees",
    #     "extract 20 degrees of cake",
    #     "decrease the temprature of the sun by 50 degrees",
    #     "throw me forward",
    #     "move the seat back by 21 degrees.",
    #     "move the seat forward by 33 degrees.",
    #     "move the seat back by 15 degrees.",
    #     "move the seat front by 22 degrees.",
    #     "move the seat upwards by -23423423 degrees.",
    #     "move the seat sideway by 0 degrees.",
    #     "adjust my seat backwards by 15 %",
    #     "move me to the front",
    #     "take me to the back a bit",
    #     "make a crab dance",
    #     "mars is a planet",
    #     "will humans stay on earth?",
    #     "venus is a planet",
    #     "move my seat in party mode",
    # ]
    # import time
    # for query in test_data:
    #     prediction = predict(model, tool, query)
    #     print(f"Query: {query}, Prediction: {prediction}")
    #     time.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
