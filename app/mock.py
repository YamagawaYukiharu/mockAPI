from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
import configparser
from pydantic import BaseModel
from typing import Callable, Dict, Any

app = FastAPI()

mocks_config = configparser.ConfigParser()
mocks_config_file_path = './properties/mock.properties'

response_config = configparser.ConfigParser()
response_config_file_path = './properties/response.properties'

class MockConfig(BaseModel):
    path: str
    method: str
    response_file_path: str = ''

def update_mock():
    global app

    #load mocks from file
    mocks_config.read(mocks_config_file_path)
    mocks: Dict[str, Dict[str, Any]] = {}
    for section in mocks_config.sections():
        mock_name = section
        mock_info = {
            'path' : mocks_config.get(section, 'path'),
            'method' : mocks_config.get(section, 'method'),
            'response_file_path' : mocks_config.get(section, 'response_file_path', fallback='')
            }
        mocks[mock_name] = mock_info

    #add mocks to the app
    for mock_name, mock_info in mocks.items():
        #separate the dedicated route that add new mocks
        if mock_name == 'ADDMOCK':
            endpoint = add_mock()
            app.add_api_route(mock_info['path'], endpoint, methods=[mock_info['method']])
        else:
            endpoint = create_endpoint(mock_name, mock_info['response_file_path'])
            app.add_api_route(mock_info['path'], endpoint, methods=[mock_info['method']])

def create_endpoint(mock_name: str, response_file_path: str) -> Callable:
    async def endpoint(request: Request):
        try:
            with open(response_file_path, 'r') as file:
                full_path = request.url.path
                body = request.json

                content = file.read()
                response_config.read(response_config_file_path)
                response_code = int(response_config.get(mock_name,'response_code'))
                content_type = response_config.get(mock_name, 'content_type')

                return Response(content=content, status_code=response_code, media_type=content_type)
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail='File not found')
    return endpoint

def add_mock() -> Callable:
    async def endpoint(request: Request):
        new_config = await request.json()

        #read existing config
        mock_config.read(mocks_config_file_path)
        response_config.read(response_config_file_path)

        #update mock.properties with new data
        for section, options in new_config.items():
            if not mock_config.has_section(section):
                mock_config.add_section(section)
            for key, value in options.items():
                mock_config.set(section, key, value)

        #write updated config to file
        with open(mocks_config_file_path, 'w') as config_file:
            mock_config.write(config_file)

        for section, options in new_config.items():
            if not response_config.has_section(section):
                response_config.add_section(section)
            # setting default value
            response_config.set(section, "response_code", "200")
            response_config.set(section, "content_type", "application/json")

        #write updated response_config to file
        with open(response_config_file_path, 'w') as response_config_file:
            response_config.write(response_config_file)

        #clear new_config to ensure it`s not reused unintentionally
        new_config.clear()

        update_mock()

        return JSONResponse(content={'message': 'Mocks config updated succesfully'})

    return endpoint

# Root endpoint to check the API
@app.get("/")
def read_root():
    return {"message": "MockPIE is working! Check /info to more information..."}


# Endpoint to check some info
@app.get("/info")
def read_root():
    return {"message": "This is a test version, soon there will be more...."}

update_mock()
