#!/usr/bin/env python3
import pandas as pd


class Report:
    def __init__(self, bom_Dataframe, itemMasterTable, itemLocationTable, shopOrderDetailTable, shopOrderHeaderTable, billOfMaterialProduct):
        self.bom_Dataframe = bom_Dataframe
        self.bom_Dataframe.name = "bom_Dataframe"

        self.itemMasterTable = itemMasterTable
        self.itemMasterTable.name = "itemMasterTable"

        self.itemLocationTable = itemLocationTable
        self.itemLocationTable.name = "itemLocationTable"

        self.shopOrderDetailTable = shopOrderDetailTable
        self.shopOrderDetailTable.name = "shopOrderDetailTable"

        self.billOfMaterialProduct = billOfMaterialProduct
        self.billOfMaterialProduct.name = "billOfMaterialProduct"

        self.excel_Frame = pd.DataFrame()
        self.excel_Frame.name = "excel_Frame"
        
        self.shopOrderHeaderTable = shopOrderHeaderTable 
        self.shopOrderDetailTable.name = "shopOrderHeaderTable"
    
        self.summary = lambda : None
    

    def summarizeFrame(self, dataframe, *tracked_cols):
        """
        Example usage:

            instanceName.summarizeFrame(dataframe = instanceName.shopOrderDetailTable, "qty", "act_lbr_hr", "act_total_cost")

        Access the summarized DataFrame by typing:

            instanceName.summary.itemMasterTable
        
        """
        def getItem(nameSet):
            for name in nameSet:
                yield name
    
        def getRows(df):
            for row in df.itertuples():
                yield row
        
        def updateFrames(summaryFrame, currentFrame, itemName, trackedCols):
            for col in trackedCols:
                try:
                    magicNumber = furtherProcessing.itercolumns(dataframe, col)
                    summaryFrame[itemName][col].append(currentFrame[magicNumber])
                except KeyError:
                    pass
            return summaryFrame

        # Gets unique item numbers from dataframe argument
        item_Names = set(
                name.strip(' ') 
                for name in getattr(self, dataframe.name)['item_no'])

        headers = furtherProcessing.itercolumns(dataframe)
        headers = headers + ['count', 'total_cost', 'total_labor', 'average','minimum', 'first_quartile', 'median', 'third_quartile']
        
        if len(tracked_cols) == 0:
            headers = { (header, typing.Any) for header in headers }
            headers['count'] = 0

        else:
            headers = { (header, typing.Any) for header in headers }
            for colName in list(tracked_cols):
                if (colName in tracked_cols):
                    headers[colName] = []
            headers['count'] = 0


        # summary_Frame maps item_no to values collected from it's SQL table
        summary_Frame = { (name, headers) for name in item_Names } 


        # item_no_col is a magic number corresponding to column name specified
        item_no_col = furtherProcessing.itercolumns(dataframe, 'item_no')
        visited = set()


        for row in getRows(dataframe):
            for itemname in getItem(item_Names):
                
                if (row[item_no_col] == itemname) and (itemname not in visited):
                    summary_Frame[itemname].update(dict(row._asdict()))
                    summary_Frame[itemname]['count'] += 1
                    visited.add(itemname)

                elif(row[item_no_col] == itemname):
                    summary_Frame = updateFrames(
                        summaryFrame=summary_Frame,
                        currentFrame=row,
                        itemName=itemname,
                        trackedCols=tracked_cols,
                        )
                    summary_Frame[itemname]['count'] += 1


        setattr(
                self.summary,
                dataframe.name,
                summary_Frame,
            )
