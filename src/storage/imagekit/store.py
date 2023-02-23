from imagekitio import ImageKit
import base64
import os
import sys

imagekit = ImageKit(
    private_key='private_EAScro9GeDSdJ1MGxeeri3wXvhU=',
    public_key='public_qWBbQ8R24wygLI12rWcAScJmoKc=',
    url_endpoint = 'https://ik.imagekit.io/srodrigo23/'
)

with open("./src/storage/imagekit/me.jpeg", mode="rb") as img:
    imgstr = base64.b64encode(img.read())

class UploadFileRequestOptions:

    def __init__(self,folder) -> None:
        self.folder = folder
        pass
    
    
upload = imagekit.upload_file(
    file=imgstr,
    file_name="yo mismo.jpeg",
    options=UploadFileRequestOptions(
            folder ="/example-folder/",
            # response_fields = ["is_private_file", "custom_metadata", "tags"],
            # is_private_file = False,
            # tags = ["tag1", "tag2"],
            # webhook_url = "url",
            # overwrite_file = False,
            # overwrite_ai_tags = False,
            # overwrite_tags = False,
            # overwrite_custom_metadata = True,
            # custom_metadata = {"test": 11}
        )
    )
    # {
        # "folder" : "/example-folder/",
        # 'response_fields' :["is_private_file", "custom_metadata", "tags"],
        # 'is_private_file' : False,
        # 'tags' : ["tag1", "tag2"],
        # 'webhook_url' : "url",
        # 'overwrite_file' : False,
        # 'overwrite_ai_tags' : False,
        # 'overwrite_tags' : False,
        # 'overwrite_custom_metadata' : True,
        # 'custom_metadata' : {"test": 11}
    # }




print("Upload base64", upload)
# Raw Response
print(upload.response_metadata.raw)
# print that uploaded file's ID
print(upload.file_id)
# print that uploaded file's version ID
print(upload.version_info.id)
