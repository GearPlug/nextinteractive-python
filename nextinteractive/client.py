from urllib.parse import urlencode
from xml.etree import cElementTree as ET
from collections import OrderedDict

import requests
import xmltodict
import json

BASE_URL = "http://api.inexusdialer.com"
API_URL = "/iNexusSoap/Service.asmx"


class Client(object):

    def __init__(self, user, passwd):
        self._user = user
        self._passwd = passwd

    def add_disposition(self, campaign_id, name, is_sale, is_contact, is_redialable_agent):
        """
        Adds a new disposition
        :param campaign_id: The campaign ID
        :param name: The disposition name
        :param is_sale: A boolean value that identifies if this disposition is concider a sale
        :param is_contact: A boolean value that identifies if this disposition is concider a contact
        :param is_redialable_agent: A boolean value that identifies if this disposition is concider a
        redialable agent disposition
        :return:
        NOTE: This function does not check for dupplicate entries.
        """
        data = {
            "campaignID": campaign_id, "dispo_Name": name, "dispo_Is_FlagAsSale": is_sale,
            "dispo_Is_FlagAsContact": is_contact, "dispo_Is_FlagAsAgtRecall": is_redialable_agent}
        endpoint = "/AddDisposition"
        return self._post(endpoint, **data)

    def assign_lead(self, lead_name, campaign_id):
        """
        Assigns a lead to a campaign
        :param lead_name: The name of the lead to be assigned
        :param campaign_id: The campaign ID of where the lead will be assigned to.
        :return:
        """
        data = {"campaignID": campaign_id, "LeadName": lead_name}
        endpoint = "/AssignedLead"
        return self._post(endpoint, **data)

    def copy_dispositions(self, from_campaign_id, to_campaign_id):
        """
        Copies the dispositions between 2 campaigns
        :param from_campaign_id: The campaign ID to copy from.
        :param to_campaign_id: The campaign ID to copy to.
        :return:
        """
        data = {"fromCampaignID": from_campaign_id, "toCampaignID": to_campaign_id}
        endpoint = "/CopyDispositions"
        return self._post(endpoint, **data)

    def create_campaign(self, campaign_name, _type, new_lead_name, template_name, template_id, custom_fields=None):
        """
        Creates a campaign and returns an xml structure e.g. <Data LeadID="22095" TemplateID="923" CampID="1983" />
        :param campaign_name: is the name of the campaign to be created
        :param _type: The type of campaign either "I" for inbound or "O" for outbound
        :param template_name: The name of the template the campaign is bound to (a template is a record structure
        that a campaign is based on). This parameter is only used when passing custom fields
        :param template_id: An existing template id or -1 for the default. This parameter is only used when
        not passing custom fields to specify an existing template
        :param custom_fields: An xml list of addional columns that define a template. There are 15 default column names
        so any additional custom columns will be specified in this list int the following format
            <customFields><field name="AccountNo"/><field name="Comments"/></customFields>
        To empty this paramter pass an empty string or <customFields />. This field is only used when creating a new
        template
        :param new_lead_name: The name of the lead that will be assigned to the new campaign
        :return: <Data LeadID="22095" TemplateID="923" CampID="1983" />
        """
        data = {"CampaignName": campaign_name, "Type": _type, "NewLeadName": new_lead_name,
                "TemplateName": template_name, "TemplateID": template_id}
        if custom_fields is not None:
            data["CustFlds"] = custom_fields
        endpoint = "/CreateCampaign"
        return self._post(endpoint, **data)

    def create_lead(self, lead_name, template_id):
        """
        Creates an empty lead
        :param lead_name: The name of the lead to be created
        :param template_id: An existing template id or -1 for the default
        :return:
        """
        data = {"LeadName": lead_name, "TemplateID": template_id}
        endpoint = "/CreateLead"
        return self._post(endpoint, **data)

    def create_template(self, template_name, custom_fields):
        """
        Creates a new template and returns an xml structure
        :param template_name: The name of the template the campaign is bound to (a template is a record structure
        that a campaign is based on).
        :param custom_fields:  An xml list of addional columns that define a template. There are 15 default column
        names so any additional custom columns will be specified in this list int the following format
            <customFields><field name="AccountNo"/><field name="Comments"/></customFields>
        :return: <Data TemplateID="923" />
        """
        data = {"TemplateName": template_name, "CustFlds": custom_fields}
        endpoint = "/CreateTemplate"
        return self._post(endpoint, **data)

    def delete_campaign(self, campaign_name):
        """
        Deletes a campaign
        :param campaign_name: The campaign name.
        :return:
        """
        data = {"campaignName": campaign_name}
        endpoint = "/DeleteCampaign"
        return self._post(endpoint, **data)

    def get_all_campaigns(self):
        """

        :return:
        """
        endpoint = "/GetAllCampaigns?"
        return self._get(endpoint)

    def get_campaign_assigned_leads(self, campaign_id):
        """
        Gets an xml list of the leads currently assigned to a campaign
        :param campaign_id: The campaign ID
        :return:
        """
        params = {'CampID': campaign_id}
        endpoint = "/GetAssignedLeads?" + urlencode(params)
        return self._get(endpoint)

    def get_available_templates(self):
        """
        A template is a record structure and its used by a campaign.
        This functions returns an xml string of all templates currently available
        :return:
        """
        endpoint = "/GetAvailableTemplates?"
        return self._get(endpoint)

    def get_campaign_results(self, from_datetime):
        """
        Gets up to a thousand call history records
        :param from_datetime:  The starting date/time (e.g. 2018-10-01T12:00:00-0500)
        :return:
        """
        params = {'fromDateTime': from_datetime}
        endpoint = "/GetCampaignResults?" + urlencode(params)
        return self._get(endpoint)

    def get_campaign_results_by_id(self, from_id):
        """
        Gets up to a thousand call hitory records
        :param from_id:  The starting ID number
        :return:
        """
        params = {'fromID': from_id}
        endpoint = "/GetCampaignResultsById?" + urlencode(params)
        return self._get(endpoint)

    def import_lead_batch(self, xml_data):
        """
        Imports records into a specific lead
        :param xml_data:an xml list of the records to be imported e.g.
        <Records LeadName="Lead_02_18_2012">
         <Record>
          <Column Name="First Name" Value="Al"/>
          <Column Name="Last Name" Value="Giron"/>
          <Column Name="Phone" Value="2132223456"/>
         </Record>
        </Records>
        :return:
        """
        data = {"xmlData": xml_data}
        endpoint = "/ImportLeadBatch"
        return self._post(endpoint, **data)

    def purge_by_distinct_columns(self, campaign_id, *columns):
        """
        Purge Accounts based on disticnt columns
        :param campaign_id: The ID of the campaign
        :param columns: A comma delimeted list of the columns=values that define the purge
        :return:
        """
        data = {"campaignID": campaign_id, "columns": str(*columns)}
        endpoint = "/PurgeByDistinctColumns"
        return self._post(endpoint, **data)

    def reset_custom_recalls(self, leads):
        """
        Resets custom recall records
        :param leads:  A list of leads in XML format
            <leads>
              <lead name="Lead_02_18_2012" uniqueIdColumnName="RecID" uniqueIdValue="A1B76T"/>
              <lead name="Lead_02_18_2013" uniqueIdColumnName="RecID" uniqueIdValue="B1B76T"/>
            </leads>
        :return:
        """
        data = {"leads": leads}
        endpoint = "/ResetCustomRecalls"
        return self._post(endpoint, **data)

    def set_campaign_ratios(self, camps):
        """
        Set campaign dial ratios
        :param camps: A list of campaigns in XML format
            <camps>
              <camp name="RD1" ratio="1.5"/>
              <camp name="RD2" ratio="3.0"/>
            </camps>
        :return:
        """
        data = {"camps": camps}
        endpoint = "/SetCampaignRatios"
        return self._post(endpoint, **data)

    def set_campaign_state(self, camps):
        """
        Set campaign on/off states
        :param camps: A list of campaigns in XML format
            <camps>
              <camp name="RD1" enabled="true"/>
              <camp name="RD2" enabled="false"/>
            </camps>
        :return:
        """
        data = {"camps": camps}
        endpoint = "/SetCampaignState"
        return self._post(endpoint, **data)

    def suppress_lead(self, lead_name, campaign_name, phone, record_id_col, record_id_value):
        """
        Suppresses a lead record
        :param lead_name: The name of the lead to search in
        :param campaign_name: The name of the campaign the lead was assigned to
        :param phone:  The phone number in the lead to search for
        :param record_id_col: The name of the column in the lead that contains a record identifier
        :param record_id_value: The value of the record identifier
        :return:
        """
        data = {"leadName": lead_name, "campaignName": campaign_name, "phone": phone, "recIdCol": record_id_col,
                "recIdValue": record_id_value}
        endpoint = "/SuppressLead"
        return self._post(endpoint, **data)

    def suppress_multiple_leads(self, leads):
        """
        Suppresses lead records
        :param leads: A list of leads in XML format
        <leads>
          <lead name="RD1" campaignName="Callbacks" searchColName="RecId">
            <rec searchVal="73465" phone="2137628974"/>
            <rec searchVal="72906" phone="3107254817"/>
          </lead>
          <lead name="RD2" campaignName="Dish" searchColName="CustRecId">
            <rec searchVal="93617" phone="8054825483"/>
          </lead>
        </leads>
        :return:
        """
        data = {"leads": leads}
        endpoint = "/SuppressLeads"
        return self._post(endpoint, **data)

    def unassigned_lead(self, lead_name, campaign_id):
        """
        Unassigns a lead from a campaign
        :param lead_name: The name of the lead to be unassigned.
        :param campaign_id: The campaign ID of where the lead is assigned to.
        :return:
        """
        data = {"LeadName": lead_name, "CampaignID": campaign_id}
        endpoint = "/UnassignedLead"
        return self._post(endpoint, **data)

    def unsuppress_lead(self, lead_name, campaign_name, phone, record_id_col, record_id_value):
        """
        Unsuppresses a lead record
        :param lead_name: The name of the lead to search in
        :param campaign_name: The name of the campaign the lead was assigned to
        :param phone: The phone number in the lead to search for
        :param record_id_col: The name of the column in the lead that contains a record identifier
        :param record_id_value:  The value of the record identifier
        :return:
        """
        data = {"leadName": lead_name, "campaignName": campaign_name, "phone": phone, "recIdCol": record_id_col,
                "recIdValue": record_id_value}
        endpoint = "/UnsuppressLead"
        return self._post(endpoint, **data)

    def unsuppress_multiple_leads(self, leads):
        """
        Unsuppresses lead records
        :param leads: A list of leads in XML format
        <leads>
          <lead name="RD1" campaignName="Callbacks" searchColName="RecId">
            <rec searchVal="73465" phone="2137628974"/>
            <rec searchVal="72906" phone="3107254817"/>
          </lead>
          <lead name="RD2" campaignName="Dish" searchColName="CustRecId">
            <rec searchVal="93617" phone="8054825483"/>
          </lead>
        </leads>
        :return:
        """
        data = {"leads": leads}
        endpoint = "//UnsuppressLeads"
        return self._post(endpoint, **data)

    # Communications
    def _get(self, endpoint, ):
        return self._request('GET', endpoint)

    def _post(self, endpoint, **kwargs):
        return self._request('POST', endpoint, **kwargs)

    def _put(self, endpoint, **kwargs):
        return self._request('PUT', endpoint, **kwargs)

    def _patch(self, endpoint, **kwargs):
        return self._request('PATCH', endpoint, **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self._request('DELETE', endpoint, **kwargs)

    def _request(self, method, endpoint, **kwargs):
        headers = {'content-type': "application/x-www-form-urlencoded"}
        url = BASE_URL + API_URL + endpoint
        if method == 'GET':
            return self._parse(
                requests.request(method, url, auth=(self._user, self._passwd), headers=headers, data=kwargs))
        else:
            response = requests.request(method, url, auth=(self._user, self._passwd), headers=headers, data=kwargs)
            clean_response = self._parse(response)
            return clean_response

    def _parse(self, response):
        if "System." in response.text:
            return response.text
        if response.status_code == 200:
            root = ET.fromstring(response.text)
        if len(root) == 0 and 'Failed' in root.text:
            return root.text
        elif len(root) == 0 and 'Success' in root.text:
            return root.text
        else:
            first_pass = xmltodict.parse(response.text)
            try:
                return xmltodict.parse(first_pass['string']['#text'])
            except Exception as e:
                return root.text
