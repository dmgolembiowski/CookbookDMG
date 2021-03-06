    import numpy as np
    import pandas as pd
    """ 
    `itercolumns(pandas.DataFrame)` is a meaningful way to
    evaluate frames of pandas.DataFrame.itertuples() objects if
    the pandas.DataFrame gains or loses columns such that
    when iterating over pandas.DataFrame.itertuples()
    the pandas.core.frame in the iteration loses a previously
    accurate tuple position in the frame.
    In English:
        This method makes it possible to prepare data analysis 
        scripts that are resilient to fluctuating SQL databases 
        that keep the same column names, however their column
        slice can change as a result of adding or dropping a table.
        
    Input:
        Pandas(Index=0, component_item='E000404-C01',ID=10217.0)
    
    Output:
        {'Index': 0, 'component_item': 1, 'ID': 2}
    
    This method makes it possible to prepare data analysis scripts that are resilient to 
    fluctuating SQL databases that keep longstanding table column names, however their tuple slice location
    is uncertain.
    
        In [0]: import numpy as np
        In [1]: import pandas as pd
        In [2]: df = pd.DataFrame({'foo1' : np.random.randn(5),'foo2' : np.random.randn(5)})
        In [3]: df
        Out[3]:
                        foo1      foo2
                0  1.613616 -2.290613
                1  0.464000 -1.134623
                2  0.227371 -1.561819
                3 -0.496922 -0.260838
                4  0.306389  0.281957
        In [4]: df['foo0'] = (0, 0, 0, 0, 0); df.reindex(columns=['foo0','foo1','foo2'])
        Out[4]: 
                   foo0     foo1      foo2
                0     0 -0.527083  0.267042
                1     0 -0.499462  2.094746
                2     0  0.492421  1.942537
                3     0  1.481899 -0.815123
                4     0 -0.194633 -1.099265
    """
    def itercolumns(dataframe, *colName):
        if len(list(colName)) > 1:
            raise ValueError('*colName cannot accept more than one column name')
        dataframe_columns = {}
        if len(colName) == 0:
            for frame in dataframe.itertuples():
                columnsList = list(frame._asdict())
                break
            i = 0
            while i < len(columnsList):
                dataframe_columns[columnsList[i]] = i
                i += 1
            return dataframe_columns
        else:
            for frame in dataframe.itertuples():
                columnsList = list(frame._asdict())
                break
            i = 0
            while i < len(columnsList):
                dataframe_columns[columnsList[i]] = i
                i += 1
            return dataframe_columns[colName[0]]
