from imagekitio import ImageKit
import base64
# import os
# import sys

import settings as s

# print(s.get_imagekit_private_key())
# print(s.get_imagekit_public_key())
# print(s.get_imagekit_url_endpoint())
class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

def get_options(destiny_path:str) -> Struct:
    args = {
        'folder' : destiny_path,#"/example-folder/",
        "response_fields" : ["is_private_file", "custom_metadata", "tags"],
        'is_private_file' : False,
        'tags' : ["tag1", "tag2"],
        'webhook_url' : "url",
        'overwrite_file' : False,
        'overwrite_ai_tags': False,
        'overwrite_tags' : False,
        'overwrite_custom_metadata' : True,
        # 'custom_metadata' : {"test": 11}
    }
    options = Struct(**args)
    return options


def upload_file_to_imagekit_io(image:base64, file_name:str, options: Struct) -> dict:
    upload = imagekit.upload_file(
        file=image,
        file_name=file_name,
        options=options
    )
    return upload.response_metadata.raw
    # print("Upload base64", upload)
    # print(upload.response_metadata.raw)    # Raw Response
    # print(upload.file_id) # print that uploaded file's ID
    # print(upload.version_info.id)# print that uploaded file's version ID


imagekit = ImageKit(
    private_key=s.get_imagekit_private_key(), #'private_EAScro9GeDSdJ1MGxeeri3wXvhU=',
    public_key=s.get_imagekit_public_key(),#'public_qWBbQ8R24wygLI12rWcAScJmoKc=',
    url_endpoint=s.get_imagekit_url_endpoint()#'https://ik.imagekit.io/srodrigo23/'
)

images = ["./src/storage/imagekit/me.jpeg", "./src/storage/imagekit/rodrigo.jpg"]


def upload_file(image_file, file_label:str, path_to_upload:str)->dict:
    # imagekit_io_url_list = []
    # for image_file in file_paths:
        # image = "./src/storage/imagekit/me.jpeg"
    with open(image_file, mode="rb") as img:
        imgstr = base64.b64encode(img.read())
    image_uploaded_data = upload_file_to_imagekit_io(
        image=imgstr,
        file_name=file_label,
        options=get_options(destiny_path=path_to_upload)
    )
    # imagekit_io_url_list.append(image_uploaded_data['url'])
    # return imagekit_io_url_list
    return image_uploaded_data
