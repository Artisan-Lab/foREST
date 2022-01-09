""" THIS IS AN AUTOMATICALLY GENERATED FILE!"""
from __future__ import print_function
import json
from engine import primitives
from engine.core import requests
from engine.errors import ResponseParsingException
from engine import dependencies

_groups_post_id = dependencies.DynamicVariable("_groups_post_id")

_groups__id__hooks_post_confidential_issues_events = dependencies.DynamicVariable("_groups__id__hooks_post_confidential_issues_events")

_groups__id__hooks_post_confidential_note_events = dependencies.DynamicVariable("_groups__id__hooks_post_confidential_note_events")

_groups__id__hooks_post_deployment_events = dependencies.DynamicVariable("_groups__id__hooks_post_deployment_events")

_groups__id__hooks_post_enable_ssl_verification = dependencies.DynamicVariable("_groups__id__hooks_post_enable_ssl_verification")

_groups__id__hooks_post_id = dependencies.DynamicVariable("_groups__id__hooks_post_id")

_groups__id__hooks_post_issues_events = dependencies.DynamicVariable("_groups__id__hooks_post_issues_events")

_groups__id__hooks_post_job_events = dependencies.DynamicVariable("_groups__id__hooks_post_job_events")

_groups__id__hooks_post_merge_requests_events = dependencies.DynamicVariable("_groups__id__hooks_post_merge_requests_events")

_groups__id__hooks_post_note_events = dependencies.DynamicVariable("_groups__id__hooks_post_note_events")

_groups__id__hooks_post_pipeline_events = dependencies.DynamicVariable("_groups__id__hooks_post_pipeline_events")

_groups__id__hooks_post_push_events = dependencies.DynamicVariable("_groups__id__hooks_post_push_events")

_groups__id__hooks_post_releases_events = dependencies.DynamicVariable("_groups__id__hooks_post_releases_events")

_groups__id__hooks_post_tag_push_events = dependencies.DynamicVariable("_groups__id__hooks_post_tag_push_events")

_groups__id__ldap_group_links_post_cn = dependencies.DynamicVariable("_groups__id__ldap_group_links_post_cn")

_groups__id__ldap_group_links_post_provider = dependencies.DynamicVariable("_groups__id__ldap_group_links_post_provider")

def parse_groupspost(data, **kwargs):
    """ Automatically generated response parser """
    # Declare response variables
    temp_7262 = None

    if 'headers' in kwargs:
        headers = kwargs['headers']


    # Parse body if needed
    if data:

        try:
            data = json.loads(data)
        except Exception as error:
            raise ResponseParsingException("Exception parsing response, data was not valid json: {}".format(error))
        pass

    # Try to extract each dynamic object

        try:
            temp_7262 = str(data["id"])
            
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass



    # If no dynamic objects were extracted, throw.
    if not (temp_7262):
        raise ResponseParsingException("Error: all of the expected dynamic objects were not present in the response.")

    # Set dynamic variables
    if temp_7262:
        dependencies.set_variable("_groups_post_id", temp_7262)


def parse_groupsidhookspost(data, **kwargs):
    """ Automatically generated response parser """
    # Declare response variables
    temp_8173 = None
    temp_7680 = None
    temp_5581 = None
    temp_2060 = None
    temp_5588 = None
    temp_9060 = None
    temp_4421 = None
    temp_9775 = None
    temp_2737 = None
    temp_2919 = None
    temp_4673 = None
    temp_6326 = None
    temp_4695 = None

    if 'headers' in kwargs:
        headers = kwargs['headers']


    # Parse body if needed
    if data:

        try:
            data = json.loads(data)
        except Exception as error:
            raise ResponseParsingException("Exception parsing response, data was not valid json: {}".format(error))
        pass

    # Try to extract each dynamic object

        try:
            temp_8173 = str(data["confidential_issues_events"])
            temp_8173 = temp_8173.lower()
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass


        try:
            temp_7680 = str(data["confidential_note_events"])
            temp_7680 = temp_7680.lower()
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass


        try:
            temp_5581 = str(data["deployment_events"])
            temp_5581 = temp_5581.lower()
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass


        try:
            temp_2060 = str(data["enable_ssl_verification"])
            temp_2060 = temp_2060.lower()
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass


        try:
            temp_5588 = str(data["id"])
            
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass


        try:
            temp_9060 = str(data["issues_events"])
            temp_9060 = temp_9060.lower()
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass


        try:
            temp_4421 = str(data["job_events"])
            temp_4421 = temp_4421.lower()
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass


        try:
            temp_9775 = str(data["merge_requests_events"])
            temp_9775 = temp_9775.lower()
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass


        try:
            temp_2737 = str(data["note_events"])
            temp_2737 = temp_2737.lower()
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass


        try:
            temp_2919 = str(data["pipeline_events"])
            temp_2919 = temp_2919.lower()
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass


        try:
            temp_4673 = str(data["push_events"])
            temp_4673 = temp_4673.lower()
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass


        try:
            temp_6326 = str(data["releases_events"])
            temp_6326 = temp_6326.lower()
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass


        try:
            temp_4695 = str(data["tag_push_events"])
            temp_4695 = temp_4695.lower()
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass



    # If no dynamic objects were extracted, throw.
    if not (temp_8173 or temp_7680 or temp_5581 or temp_2060 or temp_5588 or temp_9060 or temp_4421 or temp_9775 or temp_2737 or temp_2919 or temp_4673 or temp_6326 or temp_4695):
        raise ResponseParsingException("Error: all of the expected dynamic objects were not present in the response.")

    # Set dynamic variables
    if temp_8173:
        dependencies.set_variable("_groups__id__hooks_post_confidential_issues_events", temp_8173)
    if temp_7680:
        dependencies.set_variable("_groups__id__hooks_post_confidential_note_events", temp_7680)
    if temp_5581:
        dependencies.set_variable("_groups__id__hooks_post_deployment_events", temp_5581)
    if temp_2060:
        dependencies.set_variable("_groups__id__hooks_post_enable_ssl_verification", temp_2060)
    if temp_5588:
        dependencies.set_variable("_groups__id__hooks_post_id", temp_5588)
    if temp_9060:
        dependencies.set_variable("_groups__id__hooks_post_issues_events", temp_9060)
    if temp_4421:
        dependencies.set_variable("_groups__id__hooks_post_job_events", temp_4421)
    if temp_9775:
        dependencies.set_variable("_groups__id__hooks_post_merge_requests_events", temp_9775)
    if temp_2737:
        dependencies.set_variable("_groups__id__hooks_post_note_events", temp_2737)
    if temp_2919:
        dependencies.set_variable("_groups__id__hooks_post_pipeline_events", temp_2919)
    if temp_4673:
        dependencies.set_variable("_groups__id__hooks_post_push_events", temp_4673)
    if temp_6326:
        dependencies.set_variable("_groups__id__hooks_post_releases_events", temp_6326)
    if temp_4695:
        dependencies.set_variable("_groups__id__hooks_post_tag_push_events", temp_4695)


def parse_groupsidldap_group_linkspost(data, **kwargs):
    """ Automatically generated response parser """
    # Declare response variables
    temp_9821 = None
    temp_303 = None

    if 'headers' in kwargs:
        headers = kwargs['headers']


    # Parse body if needed
    if data:

        try:
            data = json.loads(data)
        except Exception as error:
            raise ResponseParsingException("Exception parsing response, data was not valid json: {}".format(error))
        pass

    # Try to extract each dynamic object

        try:
            temp_9821 = str(data["cn"])
            
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass


        try:
            temp_303 = str(data["provider"])
            
        except Exception as error:
            # This is not an error, since some properties are not always returned
            pass



    # If no dynamic objects were extracted, throw.
    if not (temp_9821 or temp_303):
        raise ResponseParsingException("Error: all of the expected dynamic objects were not present in the response.")

    # Set dynamic variables
    if temp_9821:
        dependencies.set_variable("_groups__id__ldap_group_links_post_cn", temp_9821)
    if temp_303:
        dependencies.set_variable("_groups__id__ldap_group_links_post_provider", temp_303)

req_collection = requests.RequestCollection([])
# Endpoint: /groups, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("skip_groups="),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("all_available="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("search="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("order_by="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("sort="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("statistics="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("with_custom_attributes="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("owned="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("min_access_level="),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("top_level_only="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups"
)
req_collection.add_request(request)

# Endpoint: /groups, method: Post
request = requests.Request([
    primitives.restler_static_string("POST "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("path="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("name="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_static_string("Content-Type: "),
    primitives.restler_static_string("application/json"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_static_string("{"),
    primitives.restler_static_string("""
    "name":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string(""",
    "description":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string(""",
    "membership_lock":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "visibility":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string(""",
    "share_with_group_lock":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "require_two_factor_authentication":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "two_factor_grace_period":"""),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(""",
    "project_creation_level":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string(""",
    "auto_devops_enabled":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "subgroup_creation_level":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string(""",
    "emails_disabled":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "avatar":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string(""",
    "mentions_disabled":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "lfs_enabled":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "request_access_enabled":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "parent_id":"""),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(""",
    "default_branch_protection":"""),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(""",
    "shared_runners_minutes_limit":"""),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(""",
    "extra_shared_runners_minutes_limit":"""),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(""",
    "shared_runners_setting":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string("}"),
    primitives.restler_static_string("\r\n"),
    
    {

        'post_send':
        {
            'parser': parse_groupspost,
            'dependencies':
            [
                _groups_post_id.writer()
            ]
        }

    },

],
requestId="/groups"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/subgroups, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("subgroups"),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("skip_groups="),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("all_available="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("search="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("order_by="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("sort="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("statistics="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("with_custom_attributes="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("owned="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("min_access_level="),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/subgroups"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/descendant_groups, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("descendant_groups"),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("skip_groups="),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("all_available="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("search="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("order_by="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("sort="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("statistics="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("with_custom_attributes="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("owned="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("min_access_level="),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/descendant_groups"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/projects, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("projects"),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("archived="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("visibility="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("order_by="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("sort="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("search="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("simple="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("owned="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("starred="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("with_issues_enabled="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("with_merge_requests_enabled="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("with_shared="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("include_subgroups="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("min_access_level="),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("with_custom_attributes="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("with_security_reports="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/projects"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/projects/shared, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("projects"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("shared"),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("archived="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("visibility="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("order_by="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("sort="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("search="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("simple="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("starred="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("with_issues_enabled="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("with_merge_requests_enabled="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("min_access_level="),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("with_custom_attributes="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/projects/shared"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("with_custom_attributes="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("with_projects="),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}, method: Put
request = requests.Request([
    primitives.restler_static_string("PUT "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_static_string("Content-Type: "),
    primitives.restler_static_string("application/json"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_static_string("{"),
    primitives.restler_static_string("""
    "name":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string(""",
    "path":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string(""",
    "description":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string(""",
    "membership_lock":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "share_with_group_lock":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "visibility":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string(""",
    "require_two_factor_authentication":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "two_factor_grace_period":"""),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(""",
    "project_creation_level":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string(""",
    "auto_devops_enabled":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "subgroup_creation_level":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string(""",
    "emails_disabled":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "avatar":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string(""",
    "mentions_disabled":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "lfs_enabled (optional)":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "request_access_enabled":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "default_branch_protection":"""),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(""",
    "file_template_project_id":"""),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(""",
    "shared_runners_minutes_limit":"""),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(""",
    "extra_shared_runners_minutes_limit":"""),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(""",
    "prevent_forking_outside_group":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string("}"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}, method: Delete
request = requests.Request([
    primitives.restler_static_string("DELETE "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/projects/{project_id}, method: Post
request = requests.Request([
    primitives.restler_static_string("POST "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("projects"),
    primitives.restler_static_string("/"),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/projects/{project_id}"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/restore, method: Post
request = requests.Request([
    primitives.restler_static_string("POST "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("restore"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/restore"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/hooks, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("hooks"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/hooks"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/hooks, method: Post
request = requests.Request([
    primitives.restler_static_string("POST "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("hooks"),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("url="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_static_string("Content-Type: "),
    primitives.restler_static_string("application/json"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_static_string("{"),
    primitives.restler_static_string("""
    "url":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string(""",
    "push_events":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "issues_events":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "confidential_issues_events":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "merge_requests_events":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "tag_push_events":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "note_events":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "confidential_note_events":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "job_events":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "pipeline_events":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "wiki_page_events":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "deployment_events":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "releases_events":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "enable_ssl_verification":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "token":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string("}"),
    primitives.restler_static_string("\r\n"),
    
    {

        'post_send':
        {
            'parser': parse_groupsidhookspost,
            'dependencies':
            [
                _groups__id__hooks_post_confidential_issues_events.writer(),
                _groups__id__hooks_post_confidential_note_events.writer(),
                _groups__id__hooks_post_deployment_events.writer(),
                _groups__id__hooks_post_enable_ssl_verification.writer(),
                _groups__id__hooks_post_id.writer(),
                _groups__id__hooks_post_issues_events.writer(),
                _groups__id__hooks_post_job_events.writer(),
                _groups__id__hooks_post_merge_requests_events.writer(),
                _groups__id__hooks_post_note_events.writer(),
                _groups__id__hooks_post_pipeline_events.writer(),
                _groups__id__hooks_post_push_events.writer(),
                _groups__id__hooks_post_releases_events.writer(),
                _groups__id__hooks_post_tag_push_events.writer()
            ]
        }

    },

],
requestId="/groups/{id}/hooks"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/hooks/{hook_id}, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("hooks"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups__id__hooks_post_id.reader(), quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/hooks/{hook_id}"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/hooks/{hook_id}, method: Put
request = requests.Request([
    primitives.restler_static_string("PUT "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("hooks"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups__id__hooks_post_id.reader(), quoted=False),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("url="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_static_string("Content-Type: "),
    primitives.restler_static_string("application/json"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_static_string("{"),
    primitives.restler_static_string("""
    "push_events":"""),
    primitives.restler_static_string(_groups__id__hooks_post_push_events.reader(), quoted=False),
    primitives.restler_static_string(""",
    "issues_events":"""),
    primitives.restler_static_string(_groups__id__hooks_post_issues_events.reader(), quoted=False),
    primitives.restler_static_string(""",
    "confidential_issues_events":"""),
    primitives.restler_static_string(_groups__id__hooks_post_confidential_issues_events.reader(), quoted=False),
    primitives.restler_static_string(""",
    "merge_requests_events":"""),
    primitives.restler_static_string(_groups__id__hooks_post_merge_requests_events.reader(), quoted=False),
    primitives.restler_static_string(""",
    "tag_push_events":"""),
    primitives.restler_static_string(_groups__id__hooks_post_tag_push_events.reader(), quoted=False),
    primitives.restler_static_string(""",
    "note_events":"""),
    primitives.restler_static_string(_groups__id__hooks_post_note_events.reader(), quoted=False),
    primitives.restler_static_string(""",
    "confidential_note_events":"""),
    primitives.restler_static_string(_groups__id__hooks_post_confidential_note_events.reader(), quoted=False),
    primitives.restler_static_string(""",
    "job_events":"""),
    primitives.restler_static_string(_groups__id__hooks_post_job_events.reader(), quoted=False),
    primitives.restler_static_string(""",
    "pipeline_events":"""),
    primitives.restler_static_string(_groups__id__hooks_post_pipeline_events.reader(), quoted=False),
    primitives.restler_static_string(""",
    "wiki_events":"""),
    primitives.restler_fuzzable_bool("true"),
    primitives.restler_static_string(""",
    "deployment_events":"""),
    primitives.restler_static_string(_groups__id__hooks_post_deployment_events.reader(), quoted=False),
    primitives.restler_static_string(""",
    "releases_events":"""),
    primitives.restler_static_string(_groups__id__hooks_post_releases_events.reader(), quoted=False),
    primitives.restler_static_string(""",
    "enable_ssl_verification":"""),
    primitives.restler_static_string(_groups__id__hooks_post_enable_ssl_verification.reader(), quoted=False),
    primitives.restler_static_string(""",
    "token":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string("}"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/hooks/{hook_id}"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/hooks/{hook_id}, method: Delete
request = requests.Request([
    primitives.restler_static_string("DELETE "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("hooks"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups__id__hooks_post_id.reader(), quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/hooks/{hook_id}"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/ldap_group_links, method: Get
request = requests.Request([
    primitives.restler_static_string("GET "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ldap_group_links"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/ldap_group_links"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/ldap_group_links, method: Post
request = requests.Request([
    primitives.restler_static_string("POST "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ldap_group_links"),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("cn="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("group_access="),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("provider="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    
    {

        'post_send':
        {
            'parser': parse_groupsidldap_group_linkspost,
            'dependencies':
            [
                _groups__id__ldap_group_links_post_cn.writer(),
                _groups__id__ldap_group_links_post_provider.writer()
            ]
        }

    },

],
requestId="/groups/{id}/ldap_group_links"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/ldap_group_links, method: Delete
request = requests.Request([
    primitives.restler_static_string("DELETE "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ldap_group_links"),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("cn="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("filter="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("provider="),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/ldap_group_links"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/ldap_group_links/{cn}, method: Delete
request = requests.Request([
    primitives.restler_static_string("DELETE "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ldap_group_links"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups__id__ldap_group_links_post_cn.reader(), quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/ldap_group_links/{cn}"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/ldap_group_links/{provider}/{cn}, method: Delete
request = requests.Request([
    primitives.restler_static_string("DELETE "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("ldap_group_links"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups__id__ldap_group_links_post_provider.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_fuzzable_string("fuzzstring", quoted=False),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/ldap_group_links/{provider}/{cn}"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/share, method: Post
request = requests.Request([
    primitives.restler_static_string("POST "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("share"),
    primitives.restler_static_string("?"),
    primitives.restler_static_string("group_id="),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string("&"),
    primitives.restler_static_string("group_access="),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_static_string("Content-Type: "),
    primitives.restler_static_string("application/json"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),
    primitives.restler_static_string("{"),
    primitives.restler_static_string("""
    "expires_at":"""),
    primitives.restler_fuzzable_string("fuzzstring", quoted=True),
    primitives.restler_static_string("}"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/share"
)
req_collection.add_request(request)

# Endpoint: /groups/{id}/share/{group_id}, method: Delete
request = requests.Request([
    primitives.restler_static_string("DELETE "),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("api"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("v4"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("groups"),
    primitives.restler_static_string("/"),
    primitives.restler_static_string(_groups_post_id.reader(), quoted=False),
    primitives.restler_static_string("/"),
    primitives.restler_static_string("share"),
    primitives.restler_static_string("/"),
    primitives.restler_fuzzable_int("1"),
    primitives.restler_static_string(" HTTP/1.1\r\n"),
    primitives.restler_static_string("Accept: application/json\r\n"),
    primitives.restler_static_string("Host: 192.168.112.181\r\n"),
    primitives.restler_refreshable_authentication_token("authentication_token_tag"),
    primitives.restler_static_string("\r\n"),

],
requestId="/groups/{id}/share/{group_id}"
)
req_collection.add_request(request)
