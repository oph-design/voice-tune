from integrations import speech_to_text, init_generative_model, query_model

def main():
    speech = speech_to_text()
    print(f"Speech: {speech}")
    ## TODO: I think we should initialize the model once in the beginning of the program, not everytime we want to use it
    multimodal_model = init_generative_model("bosch-bcx-hack24ber-2305", "europe-west2")
    response = query_model(multimodal_model, speech)
    print(f"Response: {response}")

if __name__ == "__main__":
    main()