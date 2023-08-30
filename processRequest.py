from processor import execute

def processRequest(request):
    #print('in process analysis')
    if request.method == "GET":
        params = request.args.to_dict(flat=False)
        msrs = {}
        for i in params:
            msrs[i] = params[i][0]
        try:
            out,status=execute(msrs)
            if(status):
                result = out.to_dict(orient="records")
                resp = {'success': True, 'message': '-', 'res':result}
            else:
                resp = {'success': True, 'message': out, 'res':''}
            
        except Exception as e:
            print(e)
            resp = {'success': False, 'message':'Something went wrong', 'res': str(e)}  
        
        return resp
    
    elif request.method == "POST":
        
        
        params = request.form.to_dict(flat=False)
        msrs = {}
        if not bool(params):
            params = request.get_json(force=True)
            for i in params:
                msrs[i] = params[i]
        else:
            for i in params:
                msrs[i] = params[i][0]
                
                        
        try:
            out,status=execute(msrs)
            if(status):
                result = out.to_dict(orient="records")
                resp = {'success': True, 'message': '-', 'res':result}
            else:
                resp = {'success': True, 'message': out, 'res':''}
            
        except Exception as e:
            print(e)
            resp = {'success': False, 'message':'Something went wrong', 'res': str(e)}  
        
        return resp
