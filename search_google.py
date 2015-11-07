import datetime as dt
import json, sys
from apiclient.discovery import build


if __name__ == '__main__':
    # Create an output file name in the format "srch_res_yyyyMMdd_hhmmss.json"
    now_sfx = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = './output/'
    output_fname = output_dir + 'srch_res_' + now_sfx + '.json'
    search_term = sys.argv[1]
    num_requests = int(sys.argv[2])

    # Key codes we created earlier for the Google CustomSearch API
    search_engine_id = '008146087719383437777:opsxgaqjaes'
    api_key = 'AIzaSyAAUHfgxKLebepLMiDCOdWoqb6633j70mQ'
    
    # The build function creates a service object. It takes an API name and API 
    # version as arguments. 
    service = build('customsearch', 'v1', developerKey=api_key)
    # A collection is a set of resources. We know this one is called "cse"
    # because the CustomSearch API page tells us cse "Returns the cse Resource".
    collection = service.cse()

    output_f = open(output_fname, 'ab')

    for i in range(0, num_requests):
        # This is the offset from the beginning to start getting the results from
        start_val = 1 + (i * 5)
        # Make an HTTP request object
        request = collection.list(q=search_term,
            num=5, #this is the maximum & default anyway
            start=start_val,
            cx=search_engine_id
        )
        response = request.execute()
        output = json.dumps(response, sort_keys=True, indent=2)
        output_f.write(output)
        print('Wrote 5 search results...')

    output_f.close()
    print('Output file "{}" written.'.format(output_fname)) 