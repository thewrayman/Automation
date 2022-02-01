from wsgiref.simple_server import make_server
from movr import check_status
from deployment_utils import install_falcon_packages


try:
    import json
    import falcon

except:
    install_falcon_packages()


class StakeResponse:

    def on_get(self, req, resp, address):
        print(req)
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_JSON
        resp.text = json.dumps(check_status(address))


api = falcon.App()
stakeS = StakeResponse()

api.add_route('/staking/{address}', stakeS)

if __name__ == '__main__':
    with make_server('', 8000, api) as httpd:
        print('Serving on port 8000...')
        httpd.serve_forever()
