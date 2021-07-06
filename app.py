from flask import Flask, request, jsonify  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import

import cek_inf

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
api = Api(app)  # Flask 객체에 Api 객체 등록


@api.route('/clova')  # 데코레이터 이용, '/clova' 경로에 클래스 등록
class ClovaInterface(Resource):
    def post(self):  # POST 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환

        req_json=request.get_json()
        cekResponse = cek_inf.CEKResponse()
        cekRequest = cek_inf.CEKRequest(req_json)
        cekRequest.do(cekResponse)

        resp_json = {
            "response": cekResponse.response,
            "version": cekResponse.version,
            "sessionAttributes": cekResponse.sessionAttributes
        }

        #print(json.dumps(resp_json))

        return resp_json

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=80)