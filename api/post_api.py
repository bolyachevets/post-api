# Copyright © 2023 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, request
from google.cloud import storage
from google.oauth2 import service_account
import json
import os

app = Flask(__name__)

@app.route('/api/v1/post', methods=['POST'])
def post_api():
    """return post body"""

    data = request.json
    bucket_name = data['bucket']
    project_id = data['project']
    creds_str = os.environ['SA_DOC_AI_KEY']
    cred_dict = json.loads(creds_str)
    credentials = service_account.Credentials.from_service_account_info(cred_dict)
    storage_client = storage.Client(project=project_id, credentials=credentials)

    bucket = storage_client.bucket(bucket_name)

    res = []
    blobs=list(bucket.list_blobs())
    for blob in blobs:
        if not blob.name.endswith("/"):
            ret = blob.download_as_text()
            json_object = json.loads(ret)
            res.append(json_object)
    res_json = json.dumps(res)
    return res_json
