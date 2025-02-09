from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyBudhZAc3D8TkBoLTxK2xvkSEVdB5mVtlQ"
import sys
sys.stdout.reconfigure(encoding='utf-8')



# Initialize the model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

# Create a prompt template
prompt_template = PromptTemplate.from_template("""You are an intelligent chatbot that processes user input to identify objects from a predefined list of objects, translate text, and return a structured JSON output. Follow these steps precisely:

Translate {input} in english and determine if it contains any object or its synonym which is mentioned in the following list:
[person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, traffic light, fire hydrant, stop sign, parking meter, bench, bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe, backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard, sports ball, kite, baseball bat, baseball glove, skateboard, surfboard, tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl, banana, apple, sandwich, orange, brocolli, carrot, hot dog, pizza, donut, cake, chair, couch, potted plant, bed, dining table, toilet, tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster, sink, refrigerator, book, clock, vase, scissors, teddy bear, hair drier, toothbrush]
If an object is found, return its English name. Otherwise, return none.
Translate the entire list of 80 objects into the {language} language.
Translate instructions: {instructions} into the {language} language.
Format the response as JSON with the following structure:
{{
  "identified_object": "<object_in_english_or_none>",
  "translated_objects": {{
    "person": "<translated_word>",
    "bicycle": "<translated_word>",
    ...
  }},
  "instructions": "<translated_instructions>"
}}
If no object is found, set "identified_object": "none" and "translated_objects": null, but still translate the instructions.

Ensure accuracy in translations and maintain JSON structure integrity.

Additional note to take care when translating the instructions, look for double curly braces {{}} in the instructions and consider the text between them as a variable so translate it accordingly that it makes sense if i replace the variable with the object in future.""")

# Prepare the prompt with input
input_text = "मैं अपनी बोतल ढूंढना चाहता हूँ"
language = "hi"
instructions = ["turn left", "turn right", "There is a {{variable}} in front of you, turn left"]

prompt = prompt_template.format(input=input_text, language=language, instructions=instructions)

# Invoke the model with the prepared prompt
response = llm.invoke(prompt)

print(response.content)
