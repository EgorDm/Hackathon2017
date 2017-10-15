from ml.models.BaseModel import BaseModel
from ml.tools.text_processing import clean_text


def classify(text, model_path):
    text_input = clean_text(text)
    model = BaseModel(model_path)
    result = model.predict([text_input])
    return result[0]
