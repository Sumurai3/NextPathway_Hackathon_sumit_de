class QueryParserclass:
    def __init__(self,sql):
        self.sql=sql.upper().replace("\n"," ").replace(")  ",") ").replace("  "," ")
        self.alias_dict = {}

    def get_table_name(self,char):
        a = self.sql.split("{}".format(char))[0].split("FROM")[-1].split(" ")
        temp = [i for i in a if i]

        return temp[0]
    def sql_parser(self):

        cols = self.sql.split("FROM")[0].split("SELECT")[-1].split(",")
        fetched_cols = [i.replace("\n", "").replace("\t", "").replace(" ","") for i in cols if i]
        fetched_cols_dict={x.split(".")[1]:x.split(".")[0] for x in fetched_cols}
        alias_names = set([x.split(".")[0] for x in fetched_cols])
        for i in alias_names:
            char=") {}".format(i)
            tablename=self.get_table_name(char)
            self.alias_dict[i]=tablename
        return [fetched_cols_dict,self.alias_dict]
sql="""SELECT
T.SWB_CNTRY_ID,
T.CNTRY_TYPE_CD,
T.DW_EFF_DT,
S.DW_AS_OF_DT
FROM
(SELECT
SWB_CNTRY_ID,
CNTRY_TYPE_CD,
RCV_IN,
DW_EFF_DT,
MAX(DW_EFF_DT) MAX_EFF_DT
FROM IDW_DATA.CNTRY_MULTI_DEF_CD_T
WHERE
CURR_IN=1 GROUP BY 1,2,3,4) T,
(SELECT
SWB_CNTRY_ID,
CNTRY_SCHEME_CD,
DW_AS_OF_DT,
DW_ACTN_IND
FROM IDW_STAGE.CNTRY_MULTI_DEF_CD_S) S
WHERE
S.SWB_CNTRY_ID = T.SWB_CNTRY_ID AND S.CNTRY_SCHEME_CD = T.CNTRY_TYPE_CD
AND (S.DW_SCTN_IND=‘U’ OR (S.DW_ACTN_IND=‘I’ AND T.RCV_IN=0))
AND S.DW_AS_OF_DT > T.MAX_EFF_DT"""#input your query
obj=QueryParserclass(sql)
result=obj.sql_parser()
for i,j in zip(result[0].keys(),result[0].values()):
    print("{} -> {}".format(i,result[1][j]))