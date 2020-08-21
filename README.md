![](extention/icons/secsnake.png)                    

## About
**SecSnake** is a Man-in-the-Browser (MitB) attack finder tool that it works with four main modules:
1. Web Extension: This module installed on the browser and gets all documents and request for analyze and shows notification and results to user.
2. Pattern Parser: This module parses **attack_pattern.json** that wrote with user (For get information about how this file can be configured, see **/app/classes/attack_pattern_schema.py**).
3. Interaction Monitoring: This module finds all attack patterns on HTML attribute, CSS properties and JavaScript codes.
4. Request Analyzer: This module Blocks the request that it has a bad property. 

----
## Installation
#### Requirements
> Python3.*

> semgrep

> scrapy


#### Installation
At first you should clone the repository
> $ git clone https://gitlab.com/majidmc2/secsnake

Then load **/extention/manifest.json**  to "about:debugging#/runtime/this-firefox"
After that run this commands:
> $ cp app/interaction_monitoring.json app/pattern_parser.json app/request_analyzer.json ~/.mozilla/native-messaging-hosts
 
> $ chmod 775 ~/.mozilla/native-messaging-hosts/interaction_monitoring.json ~/.mozilla/native-messaging-hosts/pattern_parser.json ~/.mozilla/native-messaging-hosts/request_analyzer.json

> $ chmod 775 app/interaction_monitoring.py app/pattern_parser.py app/request_analyzer.py

> $ sudo apt-get install python3 python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev

> $ pip3 install scrapy

> $ pip3 install semgrep

> $ pip3 install jsonschema

> $ pip3 install cssutils
