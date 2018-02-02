# --
# File: sumologic_parser.py
#
# Copyright (c) Phantom Cyber Corporation, 2017-2018
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber.
#
# --

import datetime
import re

IP_REGEX = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'


# This only assumes that the default fields exists
# If your query is something like "_SourceCategory=apache | parse "GET * " as url",
# then you can just reference the 'url' field
# I'd imagine in writing a custom parser method that regexes should be completely unnecessary
def message_parser(response, query):
    ret_json = {}
    container_json = {}
    artifact_list = []

    ip_regexc = re.compile(IP_REGEX)

    ret_json['artifacts'] = artifact_list
    ret_json['container'] = container_json

    container_json['name'] = '{0} on {1}'.format(
                query,
                datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            )
    container_json['description'] = "Sumo Logic Message Artifacts"
    container_json['run_automation'] = False

    messages = response['messages']
    # Don't create a new container if there are no results from the query
    if len(messages) == 0:
        return []
    for message in messages:
        artifact_json = {}
        artifact_list.append(artifact_json)

        info = message['map']

        artifact_json['run_automation'] = False
        artifact_json['source_data_identifier'] = info['_messagecount']
        artifact_json['name'] = 'Message {0} from {1}'.format(
                    info['_messagecount'],
                    info['_sourcehost']
                )
        cef = {}

        artifact_json['cef'] = cef
        cef['log_source'] = info['_sourcename']
        cef['message'] = info['_raw']
        cef['fsize'] = info['_size']
        ips = ip_regexc.findall(info['_raw'])
        size = len(ips)
        if size >= 1:
            cef.update({'sourceIp': ips[0]})
        if size >= 2:
            cef.update({'destinationIp': ips[1]})

    return [ret_json]
