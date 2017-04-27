# --
# File: sumologic_connector.py
#
# Copyright (c) Phantom Cyber Corporation, 2016-2017
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber.
#
# --

# Phantom imports
import time

import phantom.app as phantom
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

from sumologic import SumoLogic
from sumologic_consts import *


class SumoLogicConnector(BaseConnector):
    # List of all the actions that this app supports
    ACTION_ID_RUN_QUERY = 'run_query'
    ACTION_ID_TEST_ASSET_CONNECTIVITY = 'test_asset_connectivity'
    ACTION_ID_GET_RESULTS = 'get_results'

    def __init__(self):

        # Call the super class
        super(SumoLogicConnector, self).__init__()

        # Initialize the sumo obj as None for checking later
        self._sumo = None

    def _connect(self):

        # Check if this app is already connected
        if (self._sumo is not None):
            return phantom.APP_SUCCESS

        # Get the confirguration for the environment
        config = self.get_config()

        # Retrieve the needed parameters for the SumoLogic object
        environment = config[SUMOLOGIC_JSON_ENVIRONMENT]
        access_id = config[SUMOLOGIC_JSON_ACCESS_ID]
        access_key = config[SUMOLOGIC_JSON_ACCESS_KEY]
        # collector_endpoint = SUMOLOGIC_COLLECTOR_ENDPOINT

        # Configure the endpoints to use based upon the environment set
        if environment == 'us1':
            api_endpoint = SUMOLOGIC_US1_API_ENDPOINT
        else:
            api_endpoint = SUMOLOGIC_OTHER_API_ENDPOINT.format(environment=environment)

        # Try to make the sumologic object
        try:
            self._sumo = SumoLogic(access_id, access_key, endpoint=api_endpoint)
        except Exception as e:
            return self.set_status(phantom.APP_ERROR, SUMOLOGIC_ERR_CONNECTION_FAILED, e)

        # Return success so that the other actions can be continued after they call connect
        return phantom.APP_SUCCESS

    def _get_results(self, param):

        if (phantom.is_fail(self._connect())):
            return self.get_status()

        action_result = self.add_action_result(ActionResult(dict(param)))

        search_job = {"id": param[SUMOLOGIC_JSON_JOB_ID]}
        try:

            status = self._sumo.search_job_status(search_job)

        except Exception as e:

            return action_result.set_status(phantom.APP_ERROR,
                                            "Could not find the specified job.  It may have been deleted by Sumo Logic.",
                                            e)

        self.save_progress(SUMOLOGIC_PROG_POLLING_JOB)

        status = self._poll_job(status, search_job, action_result)

        if status['state'] == 'DONE GATHERING RESULTS':

            try:
                response = self._sumo.search_job_messages(search_job)
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, "The specified job could not be retreived.", e)

            action_result.add_data(response)
            action_result.add_data({"search_id": search_job['id']})
            action_result.set_summary({"total_objects": len(response["messages"])})
            return action_result.set_status(phantom.APP_SUCCESS)
        else:
            return action_result.set_status(phantom.APP_ERROR, 'Error while getting results')

    def _test_connectivity(self):

        self.save_progress("Attempting to connect to API endpoint...")

        if phantom.is_fail(self._connect()):
            return self.set_status(phantom.APP_ERROR)

        self.save_progress("Requesting a single collector...")

        try:
            self._sumo.collectors(limit=1)

        except:

            return self.set_status(phantom.APP_ERROR)

        self.save_progress("Connection to Sumo Logic with the specified environment has succeeded.")

        return self.set_status(phantom.APP_SUCCESS)

    def _poll_job(self, status, search_job, action_result):

        delay = 2

        # Poll the Search Job until it is done
        while status['state'] != 'DONE GATHERING RESULTS':

            # App error when the state changes to cancelled
            if status['state'] == 'CANCELLED':

                return action_result.set_status(phantom.APP_ERROR, "Search Job was cancelled before finishing")

            # Don't want to be polling forever, so just succeed and give the actionable ID as a result
            elif delay >= SUMOLOGIC_POLLING_TIME_LIMIT:

                action_result.set_summary({'search_id': search_job['id']})

                return action_result.set_status(phantom.APP_SUCCESS)

            # Add a delay so that the server doesn't get overloaded
            time.sleep(delay)
            delay *= 2
            status = self._sumo.search_job_status(search_job)

        return status

    def _run_query(self, param):

        if (phantom.is_fail(self._connect())):
            return self.get_status()

        action_result = self.add_action_result(ActionResult(dict(param)))
        search_string = param[SUMOLOGIC_JSON_QUERY]
        from_time = param.get(SUMOLOGIC_JSON_FROM_TIME, self._five_days_ago())
        to_time = param.get(SUMOLOGIC_JSON_TO_TIME, self._now())

        # Convert to milliseconds if not already
        if from_time == "0" or to_time == "0":
            return action_result.set_status(phantom.APP_ERROR, "Time range cannot start or end with zero")

        from_time = self._to_milliseconds(int(from_time))
        to_time = self._to_milliseconds(int(to_time))

        limit = param.get(SUMOLOGIC_JSON_LIMIT, SUMOLOGIC_JSON_DEFAULT_RESPONSE_LIMIT)
        resp_type = param.get(SUMOLOGIC_JSON_TYPE, SUMOLOGIC_JSON_DEFAULT_RESPONSE_TYPE)
        self.save_progress(SUMOLOGIC_PROG_CREATING_SEARCH_JOB)

        try:
            search_job = self._sumo.search_job(search_string, str(from_time), str(to_time))
        except Exception as e:
            return action_result.set_status(phantom.APP_ERROR,
                                            "Could not create the job with {} {} {}".format(search_string, from_time,
                                                                                            to_time), e)

        status = self._sumo.search_job_status(search_job)

        self.save_progress(SUMOLOGIC_PROG_POLLING_JOB)

        status = self._poll_job(status, search_job, action_result)

        if status['state'] == 'DONE GATHERING RESULTS':

            try:

                if resp_type == "messages":

                    response = self._sumo.search_job_messages(search_job, limit=limit)

                    action_result.set_summary(
                        {"total_objects": len(response["messages"]), "search_id": search_job['id']})

                elif resp_type == "records":

                    response = self._sumo.search_job_records(search_job, limit=limit)

                    action_result.set_summary(
                        {"total_objects": len(response["records"]), "search_id": search_job['id']})
            except Exception as e:
                return action_result.set_status(phantom.APP_ERROR, "The specified job could not be retrieved.  "
                                                                   "If the response type was 'records', make sure that the query supplied is an aggregation query.")

            action_result.add_data(response)

            return action_result.set_status(phantom.APP_SUCCESS)

        else:

            return action_result.set_status(phantom.APP_ERROR, 'Error while getting results')

    def _five_days_ago(self):
        return int(time.mktime(time.localtime())) - SUMOLOGIC_FIVE_DAYS_IN_SECONDS

    def _now(self):
        return int(time.mktime(time.localtime()))

    def _to_milliseconds(self, time):
        now = self._now()
        if time <= now:
            return int(time) * 1000
        return int(time)

    def handle_action(self, param):

        action = self.get_action_identifier()

        if (action == self.ACTION_ID_RUN_QUERY):
            result = self._run_query(param)
        elif (action == self.ACTION_ID_TEST_ASSET_CONNECTIVITY):
            result = self._test_connectivity()
        elif (action == self.ACTION_ID_GET_RESULTS):
            result = self._get_results(param)

        return result


if __name__ == '__main__':
    """ This section is executed when run in standalone debug mode """

    import sys
    import pudb
    import json

    pudb.set_trace()

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)

        connector = SumoLogicConnector()

        connector.print_progress_message = True

        ret_val = connector._handle_action(json.dumps(in_json), None)

        print ret_val

    exit(0)
