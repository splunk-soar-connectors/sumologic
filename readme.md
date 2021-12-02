[comment]: # " File: readme.md"
[comment]: # "  Copyright (c) 2016-2019 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
When completing the asset configuration, there's a field called **environment** . The easiest way to
find the value for this field is to take a look at the URL you use to access the platform, which
should be of the form:  
https://service. **\[environment\]** .sumologic.com/ and extract it from there.

  

## Considerations for Ingestion

When running scheduled polling, the start time is from when the previous one ended. There is also a
limit of 10,000 messages which can be received per each poll.  
With these two factors in mind, it is best to keep your **poll interval** small enough that you
would expect to receive less than the configured **Max Messages** in that interval, or else there
will be messages which won't be ingested.  
If there are still too many messages being received in a smaller time interval, consider creating
multiple assets with more specific queries.  
