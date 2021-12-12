import requests
import json
import re
import base64


def validate_signature(file_name):
    """
    Given a path to a filename of a electronic document.
    Uses DSS API to check and verify (if exists) all digital signatures in a given file.
    """
    page_url="https://ec.europa.eu/cefdigital/DSS/webapp-demo/validation"
    download_url = "https://ec.europa.eu/cefdigital/DSS/webapp-demo/validation/download-simple-report"

    with requests.Session() as client:
        r = client.get(page_url)

        pattern = r'<meta name="_csrf" content="([\w, -]+)"/>'
        csrf = re.findall(pattern, str(r.content))[0]

        data_header = {
            "_csrf": csrf,
            "_includeCertificateTokens": "on",
            "_includeRevocationTokens": "on",
            "_includeSemantics": "on",
            "_includeTimestampTokens": "on",
            "_includeUserFriendlyIdentifiers": "on",
            "defaultPolicy": True,
            "includeUserFriendlyIdentifiers": True,
            "validationLevel": "ARCHIVAL_DATA"
        }

        with open(file_name, "rb") as f:
            r = client.post(
                page_url,
                data = data_header,
                files={"signedFile": f}
            )
            
        if re.findall(download_url, str(r.content)):
            raport = client.get(download_url)
            raport_bytes = base64.b64encode(raport.content)

            return json.dumps({"signed": True, "image": str(raport_bytes)[2:-1]})

        else:
            return json.dumps({"signed": False})