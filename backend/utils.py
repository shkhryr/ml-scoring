import pandas as pd
import tensorflow as tf

from backend.settings import CONTINUOUS_FEATURES


def get_normalization_layer(name, dataset):
    normalizer = tf.keras.layers.Normalization(axis=None)
    feature_ds = dataset.map(lambda x, y: x[name])
    normalizer.adapt(feature_ds)
    return normalizer


def dataframe_to_dataset(dataframe, shuffle=True, batch_size=32):
    df = dataframe.copy()
    labels = df.pop('open_account_flg')
    df = {key: value[:, tf.newaxis] for key, value in dataframe.items()}
    ds = tf.data.Dataset.from_tensor_slices((dict(df), labels))
    if shuffle:
        ds = ds.shuffle(buffer_size=len(dataframe))
    ds = ds.batch(batch_size)
    ds = ds.prefetch(batch_size)
    return ds


def get_category_encoding_layer(name, dataset, dtype, max_tokens=None):
    if dtype == 'string':
        index = tf.keras.layers.StringLookup(max_tokens=max_tokens)
    else:
        index = tf.keras.layers.IntegerLookup(max_tokens=max_tokens)

    feature_ds = dataset.map(lambda x, y: x[name])
    index.adapt(feature_ds)
    encoder = tf.keras.layers.CategoryEncoding(num_tokens=index.vocabulary_size())
    return lambda feature: encoder(index(feature))


def scoring_function(account):
    account = account.dict()
    client_id = account.pop('client_id');CONTINUOUS_FEATURES.remove('open_account_flg')
    for column in account:
        account[column] = [account[column]]

    account = pd.DataFrame.from_dict(account)

    account[CONTINUOUS_FEATURES] = account[CONTINUOUS_FEATURES].apply(pd.to_numeric)
    loaded_model = tf.keras.models.load_model('model/scoring_model')
    input_dict = {name: tf.convert_to_tensor([value]) for name, value in account.items()}
    predictions = loaded_model.predict(input_dict, verbose=0)
    prob = tf.nn.sigmoid(predictions[0])
    percentage = tf.keras.backend.get_value(prob)[0].item()

    if percentage/0.35 > 0.5:
        response = 'Открыл'
    else:
        response = 'Не открыл'

    response_dict = {'client_id': client_id, 'response': response, 'percentage': round(percentage / 0.35, 2) * 100}

    return response_dict
