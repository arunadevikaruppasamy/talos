from .performance import Performance
from numpy import nan


# Inspired by predict_classes function from Keras Sequential Model
# Supports Functional Model (Experimental)
def _functional_predict(model, x, batch_size=32, verbose=0):

        proba = model.predict(x, batch_size=batch_size, verbose=verbose)
        if proba.shape[-1] > 1:
            return proba.argmax(axis=-1)
        else:
            return (proba > 0.5).astype('int32')


def get_score(self):

    '''SCORE MODEL CONFIGURATION

    Initiates the model scoring process. Currently works
    only for binary and categorical predictions. The model scoring
    currently is only used in the Talos master log, and is not
    available in the experiment log or reports.

    TODO: the exception handling needs to become metric based.

    '''

    try:
        if self.experimental_functional_support:
            y_pred = _functional_predict(self.keras_model, self.x_val)
        else:
            y_pred = self.keras_model.predict_classes(self.x_val)

        return Performance(y_pred, self.y_val, self.shape, self.y_max).result

    except TypeError:
        return nan
