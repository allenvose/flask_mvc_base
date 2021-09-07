
from twilio.rest import Client
from twilio.rest.verify.v2.service import verification

    
class MobileVerification():
    
    def __init__(self, phone_number):    
        self._account_sid = 'AC246cd0573516203969002ce2c74cbda2'
        self._auth_token = '71847c192734f724f09c106b9c226c85'
        self._client = Client(self._account_sid, self._auth_token)
        self.phone = phone_number

    def sms_verification_create(self):
        verification_request = self._client.verify \
            .services('VA58eb41ac7cb456186ed2847e83914a35') \
            .verifications \
            .create(to=self.phone, channel='sms')
        print(verification_request.status)
        return verification_request

    def sms_verification_check(self, code):
        """
        Args:
            code (string): verification code sent to mobile
        Returns:
            dict : record with verification status
            values  include status, to, date_created, status, channel
        """
        verification_status = self._client.verify \
            .services('VA58eb41ac7cb456186ed2847e83914a35') \
            .verification_checks \
            .create(to=self.phone, code=code)
        print(verification_status.status)
        return verification_status
        
    def line_type(self):
        """
        Args:
            phone_number (string): phone number in e.164 format
        Returns:
            string: line type associated with the phone number
            possible values are mobile, landline, or voip
        """
        try:
            phone_number_type = self._client \
                .lookups \
                .phone_numbers(self.phone) \
                .fetch(type='carrier') \
                .carrier
            return phone_number_type['type']
        except:
            return None

        

    def twilio_create_verify_service(service_name):
        account_sid = 'AC763f94a1112c63aafd37cca681badc26'
        auth_token = '5d4c2e2459019e4e922ed2c816253b45'
        client = Client(account_sid, auth_token)
        service = client.verify.services.create(
                friendly_name=service_name)
        return service.sid
