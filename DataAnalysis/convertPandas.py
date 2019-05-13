import pandas as pd


def convert(data):
    """load.convert_format(data)
        Return the converted type of the parameter.
        The argument `data` will be interpreted as either:
        (1) a Pandas.DataFrame object with R rows and C columns,
            satisfying (R >= 1) and (C >= 1);
        (2) a list resembling JSON with matching slice indices;
        (3) other forms, not yet discovered, that work by the magic
            of Python"""

    def toRawStruct(dataframe):
        listOfDicts = []
        for index in range(len(dataframe)):
            try:
                entry = dict(dataframe.T[index])
            except Exception as e:
                raise(e)
            listOfDicts.append(entry)
        return listOfDicts

    def toDataFrame(listOfDicts):
        try:
            pd.DataFrame(listOfDicts)
        except Exception as e:
            raise(e)

    try:
        assert(isinstance(data, pd.DataFrame().__class__))
        return toRawStruct(dataframe=data)

    except AssertionError:
        if all([isinstance(slice, dict().__class__) for slice in data]):
            return toDataFrame(listOfDicts=data)
        else:
            statement = '''The parameter `data` could not be interpreted
            because it was not formatted properly. Its format should resemble
                _data = [
                    {'value':1234,'time':'3:22 P.M.'},
                    {'value':1235.0564,'time':'3:23 P.M.'},
                    {'value':1233, 'time':'3:23 P.M.'}]'''
            print(statement)
            raise ValueError(data)
