from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
from scipy.optimize import minimize
import time


app = Flask(__name__)

# Check that Python API is active by going to http://0.0.0.0:8001/
@app.route('/', methods=['GET'])
def get_method():
    return 'API is active.'

# Excel/VBA accesses optimizer API with this function
@app.route('/optimizer', methods=['POST'])
def post_data():
    df = pd.DataFrame(request.json)
    df['return yards'] = df['punt return yards'] + df['kickoff return yards']
    df['o:return yards'] = df['o:punt return yards'] + df['o:kickoff return yards']
    result = run_opt(df)
    result.to_csv('SolverResults.csv')
    return "Optimization complete! Ready to load results."

# Excel/VBA accesses data return API with this function
@app.route('/results', methods=['POST'])
def return_data():
    _ = request.json
    df = pd.read_csv('SolverResults.csv').set_index('TeamNames')
    print('Returning optimized results!')
    return jsonify(df.to_dict())

def run_opt(df):
    # Index for the Average Score variable = 0
    ASI = 0
    # Indices for Offense / Defense ratings variables
    ncaa = df[['TeamNames']][1:131]
    ncaa['off'] = np.arange(1,131)
    ncaa['def'] = np.arange(131,261)
    # Get rating index, given Team name and offense/defense
    def GRI(team, flag):
        return ncaa.loc[ncaa.TeamNames == team][flag].values[0]

    # Constraints
    cons = ({'type': 'eq', 'fun': lambda x: sum(x[1:131])}, {'type': 'eq', 'fun': lambda x: sum(x[131:261])})

    # Calculate squared error for each row
    def CalcSE(row, x):
        HomeFun = x[GRI(row['team'], 'off')] + x[GRI(row['o:team'], 'def')] + x[ASI]
        AwayFun = x[GRI(row['o:team'], 'off')] + x[GRI(row['team'], 'def')] + x[ASI]
        return (row['score'] - HomeFun)**2 + (row['o:score'] - AwayFun)**2

    # Objective function to minimize
    def ObjFun(x, df):
        df = df.rename(columns={df.columns[2]:'score', df.columns[3]:'o:score'})
        return df.apply(lambda row: CalcSE(row, x), axis=1).sum()
    
    # Load initialization weights (start with previous values)
    init = {}
    init[0] = [df['AvgRush'][0]] + list(df['RushOff'][1:131]) + list(df['RushDef'][1:131])
    init[1] = [df['AvgPass'][0]] + list(df['PassOff'][1:131]) + list(df['PassDef'][1:131])
    init[2] = [df['AvgReturn'][0]] + list(df['ReturnOff'][1:131]) + list(df['ReturnDef'][1:131])
    init[3] = [df['AvgTakeaway'][0]] + list(df['TakeawayOff'][1:131]) + list(df['TakeawayDef'][1:131])
    
    # Setup objective functions
    fun = {}
    fun[0] = lambda x: ObjFun(x, df[['team','o:team','rushing yards','o:rushing yards']][131:])
    fun[1] = lambda x: ObjFun(x, df[['team','o:team','passing yards','o:passing yards']][131:])
    fun[2] = lambda x: ObjFun(x, df[['team','o:team','return yards','o:return yards']][131:])
    fun[3] = lambda x: ObjFun(x, df[['team','o:team','takeaways','o:takeaways']][131:])
    
    # Minimize with SLSQP
    results = {}
    tols = [df['RushTol'][0], df['PassTol'][0], df['ReturnTol'][0], df['TakeawayTol'][0]]
    print('Running optimizer, started', time.ctime())
    for i in range(4):
        print('--------------------')
        print(['Rushing:','Passing:','Special Teams:','Takeaway:'][i])
        print('Tolerance =', tols[i])
        start_tm = time.time()
        res = minimize(fun=fun[i], x0=init[i], method='SLSQP', constraints=cons, tol=tols[i], options={'disp':True})
        results[i] = res['x']
        print('Runtime', round((time.time() - start_tm) / 60, 1), 'minutes')
    print('--------------------')
    print(time.ctime())
    print('Optimization complete! Saving results to SolverResults.csv')
    
    # Assemble optimized variable results into dataframe
    df_result = ncaa[['TeamNames']]
    df_result['AvgRush'] = results[0][0]
    df_result['AvgPass'] = results[1][0]
    df_result['AvgReturn'] = results[2][0]
    df_result['AvgTakeaway'] = results[3][0]
    df_result['RushOff'] = results[0][1:131]
    df_result['RushDef'] = results[0][131:261]
    df_result['PassOff'] = results[1][1:131]
    df_result['PassDef'] = results[1][131:261]
    df_result['ReturnOff'] = results[2][1:131]
    df_result['ReturnDef'] = results[2][131:261]
    df_result['TakeawayOff'] = results[3][1:131]
    df_result['TakeawayDef'] = results[3][131:261]
    
    return df_result.set_index('TeamNames')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
