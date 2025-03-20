# File: sumologic_consts.py
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
SUMOLOGIC_JSON_QUERY = "query"
SUMOLOGIC_JSON_ENVIRONMENT = "environment"
SUMOLOGIC_JSON_ACCESS_ID = "access_id"
SUMOLOGIC_JSON_ACCESS_KEY = "access_key"
SUMOLOGIC_JSON_FROM_TIME = "from_time"
SUMOLOGIC_JSON_TO_TIME = "to_time"
SUMOLOGIC_JSON_TIMEZONE = "timezone"
SUMOLOGIC_JSON_LIMIT = "limit"
SUMOLOGIC_JSON_TYPE = "type"
SUMOLOGIC_JSON_JOB_ID = "search_id"
SUMOLOGIC_JSON_COLLECTOR_ID = "collector_id"
SUMOLOGIC_JSON_NAME = "name"
SUMOLOGIC_JSON_DESCRIPTION = "description"
SUMOLOGIC_JSON_CATEGORY = "category"
SUMOLOGIC_US1_API_ENDPOINT = "https://api.sumologic.com/api/v1"
SUMOLOGIC_COLLECTOR_ENDPOINT = "https://collectors.sumologic.com"
SUMOLOGIC_OTHER_API_ENDPOINT = "https://api.{environment}.sumologic.com/api/v1"

SUMOLOGIC_ERR_CONNECTION_FAILED = "Connection to the SumoLogic API has failed."

SUMOLOGIC_PROG_CREATING_SEARCH_JOB = "Creating search job..."
SUMOLOGIC_PROG_POLLING_JOB = "Polling job for success..."
SUMOLOGIC_POLLING_TIME_LIMIT = 60
SUMOLOGIC_JSON_DEFAULT_RESPONSE_LIMIT = 100
SUMOLOGIC_JSON_DEFAULT_RESPONSE_TYPE = "messages"
SUMOLOGIC_JSON_DEFAULT_COLLECTOR_LIMIT = 1000
MILLISECONDS = 100
SUMOLOGIC_FIVE_DAYS_IN_SECONDS = 432000
