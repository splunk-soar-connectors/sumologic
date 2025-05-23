# File: sumologic_parser.py
#
# Copyright (c) 2016-2025 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
import datetime

from phantom.utils import is_email, is_hash, is_ip, is_md5, is_sha1, is_sha256, is_url


def _format_to_cef_key(key):
    """
    Converts snake_case to camelCase

    :param key: The name of the field from Sumologic
    :type key: string
    :return: The key converted to camelCase
    :rtype: string
    """

    parts = key.split("_")
    if key.startswith("_"):
        parts = parts[1:]
    if len(parts) >= 2:
        for i, p in enumerate(parts[1:], 1):
            parts[i] = p.title()
    return "".join(parts)


def _update_cef_types(cef, cef_types):
    """
    Updates an artifact's cef_types dictionary with appropriate values

    :param cef: CEF dictionary
    :type cef: dict
    :param cef_types: CEF types dictionary
    :type cef_types: dict
    """

    for k, v in cef.items():
        if is_ip(v):
            cef_types[k] = ["ip"]
        elif is_url(v):
            cef_types[k] = ["url"]
        elif is_email(v):
            cef_types[k] = ["email"]
        elif is_hash(v):
            if is_md5(v):
                cef_types[k] = ["hash", "md5"]
            elif is_sha1(v):
                cef_types[k] = ["hash", "sha1"]
            elif is_sha256(v):
                cef_types[k] = ["hash", "sha256"]
            else:
                cef_types[k] = ["hash"]

    if "hostname" in list(cef.keys()):
        cef_types["hostname"] = ["host name"]


def message_parser(response, query):
    """
    Parse the response from Sumologic into containers and artifacts
    This should return a list of dictionaries. Each dictionary should have
    a key 'container' and 'artifacts'

    The response is the same as the response from Sumologic's Search Job API
    Roughly, the response will look something like this.

    {
        'fields': [
            {
                'name': '_fieldname',
                'fieldType': 'long',
                'keyField': False
            },
            ...
        ],
        'messages': [
            {
                'map': {
                    '_fieldname': 'This value of this field',
                    ...
                }
            },
            ...
        ]
    }

    In the case of searching for records instead of messages, the 'messages' key
    will be 'records' instead, but the response will otherwise look the same. The only
    key in the object in either of these lists is just going to be 'map'.

    :param response: The response to the query from Sumologic
    :type response: dict
    :param query: The query which was ran
    :type query: string
    :return: A list of dictionaries describing the container and artifacts
    :rtype: list
    """

    ret_list = []

    if "messages" in response:
        items = response["messages"]
    elif "records" in response:
        items = response["records"]
    else:
        return []

    if len(items) == 0:
        return []

    for it in items:
        # We want to create a container for each message / record
        ret = {}
        artifact_json = {}
        container_json = {}
        artifact_list = [artifact_json]

        ret["artifacts"] = artifact_list
        ret["container"] = container_json
        cef = {}
        cef_types = {}

        container_json["name"] = "Container created on {}".format(datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
        container_json["description"] = "Sumologic Ingestion"

        info = it["map"]

        artifact_json["run_automation"] = False
        artifact_json["cef"] = cef
        artifact_json["cef_types"] = cef_types

        for k, v in info.items():
            cef[_format_to_cef_key(k)] = v

        _update_cef_types(cef, cef_types)

        ret_list.append(ret)

    return ret_list
