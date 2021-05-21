""" this module is used for Challenge asynchronous solutions using await. Performance matters!"""

import asyncio
import time
import json
import sys
import aiohttp
import requests

Q_CHAR = "q"
FAIL_CODE = 599
SUCESS_CODE = 200
FINISH_CHAR =""


def get_params_first(url):
    """
    Execute first request to get response ,then extract data from it
    if response get status code 599 , it raise Error

    Parameters
    ----------
    url : str
        The url of request

    Returns
    -------
    output : str
    request_id : str
    targets : dictionary
        extract output, request_id, targets from response
    """

    response = requests.get(url)

    if response.status_code == FAIL_CODE: # check status code of response
        raise Exception("Error status code {FAIL_CODE} at first request, please run this file again .")

    my_bytes_value = response._content  # convert response to Json
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    data = json.loads(my_json)
    print("expected_execution_time: ", data["expected_execution_time"]) 

    # extract output, request_id, targets from data
    output = data["output"]
    targets = data["targets"]
    request_id = data["request_id"]

    return output, request_id, targets

def sort_string(str_in: str) -> str:
    """
    Execute sort string
    Parameters
    ----------
    str_in : str
        input string need to be sorted
    Returns
    ------- :
    "".join(sorted(str_in)) : str
        output a string which is sorted
    """

    return "".join(sorted(str_in))

def create_url(output: str, request_id: str, targets: dict) ->str:
    """
    excecute to create new url from input data

    Parameters
    ----------
    output : str
        to create value from query param
    request_id : string
        from first response or None
    targets : dict
        dictionary contain the name of function and the query param

    Returns
    -------
    arr_url : tuple
        tuple of new url from input parameters

    """

    global final_output
    arr_url = []
    str_param =""
    for (funcs, params) in (targets.items()):
        for func in funcs:
            for param in params:
                new_url = "https://api.telnyx.com/hiring/func_" \
                f"{func}?{param}={output}&request_id={request_id}"
                arr_url.append(new_url)

    return tuple(arr_url)

def create_list_url(urls : tuple) -> tuple:
    """
    this function create a tuple of url from two seprerate tuple arrays
    that get from responses run in parallel

    Parameters
    ----------
    urls : tuple
        tuple of two seperate tuple urls from two request.
    Returns
    -------
    list_urls : tuple
        contain a tuple of urls to loop
    """

    list_urls = []
    # loop inside two seperate list to make single list of url only
    for list_url in urls:
        for url in list_url:
            list_urls.append(url)

    return tuple(list_urls)

async def fetch(session: aiohttp.ClientSession, url: str) ->'coroutine':
    """
    This function run get request in asynchronous

    Parameters
    ----------
    session : aiohttp.ClientSession()

    url : str
        url of request

    Returns
    -------
    response.text() : 'coroutine'
        contain string value from response
        this will allow other request to run asynchronous
    """

    async with session.get(url) as response:    # get response from url
        return await response.text()    #waiting response and allow other code run asynchronous

async def parallel(arr_url : tuple) ->tuple:
    """
    This function run tuple of requests in async
    then gather result response_result
    then extract data from response
    it return a new tuple request and possible output of call to y
    it detect call to t hit by check the target in response.
    it detect error from response (599) by checking output in response
    Parameters
    ----------
    arr_url : tuple
        contain tuple of url to make requests
    Returns
    -------
    list_url : tuple
        contain new tuple of url from input of
    y_output : str
        if y_output has value, it means that hit call to t.
    """

    tasks = []
    y_output = ""
    global request_id
    list_url = []

    # making HTTP requests
    async with aiohttp.ClientSession() as session:
        for url in arr_url:
            tasks.append(fetch(session, url))

        response_content = tuple(await asyncio.gather(*tasks))

        # extract data from response content
        for iter, content in enumerate( response_content):    
            
            data = json.loads(content)  # convert to json
            output_in_data = "output" in data # check output in data or not.

            if output_in_data:
                output = data["output"] # extract output from data.
            else:   #  output_in_data is False
                print(186, "url error", arr_url[iter], data)
                raise Exception("Error status code {FAIL_CODE}, please run this file again .")
            targets_in_data = "targets" in data # check target exist in data or not.

            if  targets_in_data:     # if targets, extract the targets
                targets = data["targets"]
            else:    # if not targets, create targets and append output for for func y
                targets = {
                    "y":["x1"]
                }
                y_output = y_output + output
            # create new url base on output, request id and targets.
            temp_url = create_url(output, request_id, targets)  
            list_url.append(temp_url)   # create list of url

        return tuple(list_url), y_output

if __name__ == '__main__':
    """
    This is the main program. It run call to q in synchoronous.
    Then it fetch result from get request, extract data to make tuple of urls.
    It show the expected time in terminal.
    It run this tuple url in asynchronous. 
    It create two array of url from 2 request run asynchronous.
    It create single tuple of urls, then run each url of this tuple in async again.
    If hit call to t, it then concatenate the output of them, sort it and then make final call to y.
    It show the result of final request and time process in terminal.
    """

    start_time = time.time()    # start time for calculation process time
    input_char = str(sys.argv[1])  # read the input q from terminal

    if input_char != Q_CHAR:  # raise error if input is not q character
        raise ValueError('q param value is needed.')

    first_url = f"https://api.telnyx.com/hiring/func_{input_char}?x1"
    request_id = ""

    # create tuple of url from call to q request
    output, request_id, targets = get_params_first(first_url)
    arr_url = create_url(output, request_id, targets)

    # second batch requests in asynchronous run parallel
    loop = asyncio.get_event_loop()
    second_url, final_output = loop.run_until_complete(parallel(arr_url))
    

    if final_output == FINISH_CHAR:
    #  the value of final_output is None (not hit call to t), 
    # make another batch of requests.
    # append two seperate tuple url to a tuple of url
    # third batch requests, run asynchronous
       
        list_second_url = create_list_url(second_url)
        third_url, final_output = loop.run_until_complete(parallel(list_second_url)) 
        
    # hit call to t, sort output string of call to y
    final_output = sort_string(final_output)     
    final_url = f"https://api.telnyx.com/hiring/func_y?x1={final_output}&request_id={request_id}"   # url of call to y

    # call to y to get result
    final_response = requests.get(final_url)    
    
    # if error on call to y, run it gain
    if final_response.status_code != SUCESS_CODE:   
        raise Exception("Error status code {FAIL_CODE}, please run this file again .")
    my_bytes_value = final_response._content
    data = json.loads(my_bytes_value)
    print("Output result of final call to y: ", data["output"])   # output result of program
    print( "execution_time : %.2f "%(time.time() - start_time) )   # uncomment this line to get the duration of this program.
