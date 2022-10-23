# shelly_mock
Several mocks of Shelly devices' interfaces, based on their great products' [API documentation](https://shelly-api-docs.shelly.cloud/gen1/#shelly-family-overview)

This tool was developed using [fastapi](https://fastapi.tiangolo.com/) and is run using [uvicorn](https://www.uvicorn.org/) - (I instantly felt in love with those projects)

run the server with: <pre>uvicorn shelly_plug:shelly_plug_s --reload</pre>
(the "--reload" option will make the server watching for source code changes)
