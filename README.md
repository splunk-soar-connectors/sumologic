# Sumo Logic

Publisher: Splunk Community \
Connector Version: 3.0.0 \
Product Vendor: Sumo Logic \
Product Name: Sumo Logic \
Minimum Product Version: 5.4.0

This app integrates with the Sumo Logic cloud platform to implement investigative actions

### Configuration variables

This table lists the configuration variables required to operate Sumo Logic. These variables are specified when configuring a Sumo Logic asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**environment** | required | string | Environment Pod |
**access_id** | required | string | Access ID |
**access_key** | required | password | Access Key |
**timezone** | required | timezone | Sumo Logic Timezone |
**delete_job_when_finished** | optional | boolean | Delete search job when finished |
**max_messages** | optional | numeric | Max messages to poll for |
**on_poll_query** | optional | string | Query to use during polling |
**type** | optional | string | Poll for messages or records |
**message_parser** | optional | file | Python file containing a message parsing method |
**first_run_previous_days** | optional | numeric | Start polling from this many days back (minimum 1 day) |
**search_by_receipt_time** | optional | boolean | Set byReceiptTime flag when creating search job |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity \
[on poll](#action-on-poll) - Run a query on Sumo Logic and ingest the results \
[get results](#action-get-results) - Retrieves the result of a search job \
[run query](#action-run-query) - Runs a search query on the Sumo Logic platform \
[delete job](#action-delete-job) - Delete a search job

## action: 'test connectivity'

Validate the asset configuration for connectivity

Type: **test** \
Read only: **True**

This action uses the unique access ID and access key to send a request to the Sumo Logic API to retrieve a single collector.

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'on poll'

Run a query on Sumo Logic and ingest the results

Type: **ingest** \
Read only: **True**

This will run a search for logs that have occurred since the end of the scheduled poll. Since there is a limit of 10,000 messages, if there would be more than 10,000 results in the specified job search, the oldest ones will be discarded.<br>When running <b>POLL NOW</b>, it will run from the time of the last scheduled poll, but will not change which messages the next scheduled poll will receive.</br></br>In order to use this action, a parser method should be provided as a Python file, since almost every log will be different. Provided below is a file which will be used as a fallback and can also serve as a starting point. In order to properly work, the provided file needs a few things.<ul><li>There must be a function named <b>message_parser</b></li><li>It must accept two parameters<ul><li>A response, which will be returned by the endpoints to either get messages or records from a search job (more info <a href="https://help.sumologic.com/APIs/About-the-Search-Job-API">here</a>)</li><li>The query string, which will be the same one from the asset config</li></ul></li><li>It must return a list of dictionaries. Each dictionary will have a container and a list of artifacts to add to that container. These should match the JSON objects that a POST to <b>/rest/container</b> and <b>/rest/artifact</b> expect</li></ul><br><a href="/app_resource/sumologic_8e235e70-57eb-4292-9b7c-6cc44847d837/sumologic_parser.py">Here is the (default) aforementioned parser file</a>.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**start_time** | optional | Parameter Ignored in this app | numeric | |
**end_time** | optional | Parameter Ignored in this app | numeric | |
**container_id** | optional | Parameter Ignored in this app | string | |
**container_count** | optional | Parameter ignored in this app | numeric | |
**artifact_count** | optional | Maximum number of messages to check | numeric | |

#### Action Output

No Output

## action: 'get results'

Retrieves the result of a search job

Type: **investigate** \
Read only: **True**

<p>This action takes a Search Job ID as its primary parameter.</p><p>This is useful if the search job times out in the run query.  It is not, however, guaranteed to return if the Search Job had already finished - once a Search Job has been completed, the Sumo Logic platform deletes the Search Job after an unknown amount of time, resulting in the action failing even though the search job ID may be correct.</p>

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**search_id** | required | Search id | string | `search id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.search_id | string | `search id` | 177C7C195542A613 |
action_result.data.\*.fields.\*.fieldType | string | | long |
action_result.data.\*.fields.\*.keyField | boolean | | True False |
action_result.data.\*.fields.\*.name | string | | \_collectorid |
action_result.data.\*.messages.\*.map.\_blockid | string | | |
action_result.data.\*.messages.\*.map.\_collector | string | | |
action_result.data.\*.messages.\*.map.\_collectorid | string | | |
action_result.data.\*.messages.\*.map.\_format | string | | |
action_result.data.\*.messages.\*.map.\_messagecount | string | | |
action_result.data.\*.messages.\*.map.\_messageid | string | | |
action_result.data.\*.messages.\*.map.\_messagetime | string | | |
action_result.data.\*.messages.\*.map.\_raw | string | | |
action_result.data.\*.messages.\*.map.\_receipttime | string | | |
action_result.data.\*.messages.\*.map.\_size | string | | |
action_result.data.\*.messages.\*.map.\_source | string | | |
action_result.data.\*.messages.\*.map.\_sourcecategory | string | | |
action_result.data.\*.messages.\*.map.\_sourcehost | string | `ip` | 1.1.1.1 |
action_result.data.\*.messages.\*.map.\_sourceid | string | | |
action_result.data.\*.messages.\*.map.\_sourcename | string | | |
action_result.summary.search_id | string | `search id` | 177C7C195542A613 |
action_result.summary.total_objects | numeric | | 1 |
action_result.message | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'run query'

Runs a search query on the Sumo Logic platform

Type: **investigate** \
Read only: **True**

<p>Run Query takes advantage of the Search Job API.</p><p><b>PLEASE NOTE:</b>  If you do not have an Enterprise license with Sumo Logic, the Search Job API is not available to you.  This action will only work if the accessId and the accessKey are associated with an Enterprise-level account.</p><p><b>Run Query</b> takes five different parameters.  Some notes:</p><ul><li><b>query</b> - The text does not have to be escaped.</li><li><b>from_time</b> - Must be UNIX timestamp. The default value is five days ago.</li><li><b>to_time</b> - Must be UNIX timestamp. The default value is the current time.</li><li><b>limit</b> - Limiting the messages can be ideal if the query returns a large amount.  The default limit is 100.</li><li><b>type</b> - Either <i>messages</i> or an aggregate <i>record</i>. The record will be significantly smaller.  If none is specified, it will default to <i>messages</i>.</li></ul><p>The Search Job API is asynchronous and requires polling.  The <b>run query</b> action will poll for up to 60 seconds.</p><ul><li>If the query finishes before the time limit, the action will succeed and the data will be added to the action result.</li><li>If the query does not finish before the time limit, the action will still succeed - but the search job ID (action_result.summary.search_id) will be added to the summary.  This Search Job ID can then be used in <b>getting results</b>.</li></ul>

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**query** | required | Query to run | string | `sumo logic query` |
**from_time** | optional | UNIX start time for search | numeric | |
**to_time** | optional | UNIX end time for search | numeric | |
**limit** | optional | Upper limit of message response results | numeric | |
**type** | optional | Type of response to receive | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.from_time | numeric | | 1545301292 |
action_result.parameter.limit | numeric | | 100 |
action_result.parameter.query | string | `sumo logic query` | \_sourceCategory="uploads/linux/system" |
action_result.parameter.to_time | numeric | | 1545819692 |
action_result.parameter.type | string | | messages |
action_result.data.\*.fields.\*.fieldType | string | | long |
action_result.data.\*.fields.\*.keyField | boolean | | False True |
action_result.data.\*.fields.\*.name | string | | \_blockid |
action_result.data.\*.messages.\*.map.\_blockid | string | | |
action_result.data.\*.messages.\*.map.\_collector | string | | |
action_result.data.\*.messages.\*.map.\_collectorid | string | | |
action_result.data.\*.messages.\*.map.\_format | string | | |
action_result.data.\*.messages.\*.map.\_messagecount | string | | |
action_result.data.\*.messages.\*.map.\_messageid | string | | |
action_result.data.\*.messages.\*.map.\_messagetime | string | | |
action_result.data.\*.messages.\*.map.\_raw | string | | |
action_result.data.\*.messages.\*.map.\_receipttime | string | | |
action_result.data.\*.messages.\*.map.\_size | string | | |
action_result.data.\*.messages.\*.map.\_source | string | | |
action_result.data.\*.messages.\*.map.\_sourcecategory | string | | |
action_result.data.\*.messages.\*.map.\_sourcehost | string | `ip` | 1.1.1.1 |
action_result.data.\*.messages.\*.map.\_sourceid | string | | |
action_result.data.\*.messages.\*.map.\_sourcename | string | | |
action_result.summary.search_id | string | `search id` | 177C7C195542A613 |
action_result.summary.total_objects | numeric | | 0 |
action_result.message | string | | Total objects: 0, Search id: 177C7C195542A613 |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

## action: 'delete job'

Delete a search job

Type: **generic** \
Read only: **False**

<p>This action takes a Search Job ID as its primary parameter.</p><p>This action deletes any existing Search Job. The Sumo Logic platform deletes the Search Job after an unknown amount of time, resulting in the action failing even though the search job ID may be correct.</p>

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**search_id** | required | Search id | string | `search id` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.search_id | string | `search id` | 177C7C195542A613 |
action_result.data.\*.search_id | string | `search id` | 177C7C195542A613 |
action_result.summary.search_id | string | `search id` | 177C7C195542A613 |
action_result.summary.total_objects | numeric | | 1 |
action_result.message | string | | |
summary.total_objects | numeric | | 1 |
summary.total_objects_successful | numeric | | 1 |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2025 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
