import graphene
from graphene import relay

from payments import get_payment_model
from decimal import Decimal

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hi!")


class  MakingPaymentMutation(relay.ClientIDMutation):
    status = graphene.String()


    class Input:
        variant= graphene.String()
        description= graphene.String()
        total=graphene.Float()
        tax=graphene.Float()
        currency=graphene.String()
        delivery=graphene.Float()
        billing_first_name=graphene.String()
        billing_last_name=graphene.String()
        billing_address_1=graphene.String()
        billing_address_2=graphene.String()
        billing_city=graphene.String()
        billing_postcode=graphene.String()
        billing_country_code=graphene.String()
        billing_country_area=graphene.String()
        customer_ip_address=graphene.String()
        


    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
      unpacked_dict = {key: value for key, value in input.items() if value is not None}
      Payment = get_payment_model()
      payment = Payment(**unpacked_dict)
      payment.save()
      return cls(status="Done")
    
          
class  RefundingPaymentMutation(relay.ClientIDMutation):
    status = graphene.String()


    class Input:
        id = graphene.Int(required=True)
        amount = graphene.Float()
        


    @classmethod
    def mutate_and_get_payload(cls, root, info, id, amount):
        Payment = get_payment_model()
        payment = Payment.objects.get(id=id)
        if amount:
            payment.refund(amount=Decimal(amount))
        else:
            payment.refund()
        return cls(status="Done") 


class  CapturingPaymentMutation(relay.ClientIDMutation):
    status = graphene.String()


    class Input:
        id = graphene.Int(required=True)
        amount = graphene.Float()
        


    @classmethod
    def mutate_and_get_payload(cls, root, info, id, amount):
        Payment = get_payment_model()
        payment = Payment.objects.get(id=id)
        if amount:
            payment.capture(amount=Decimal(amount))
        else:
            payment.capture()
        return cls(status="Done") 

class  ReleasingPaymentMutation(relay.ClientIDMutation):
    status = graphene.String()


    class Input:
        id = graphene.Int(required=True)
        


    @classmethod
    def mutate_and_get_payload(cls, root, info, id, amount):
        Payment = get_payment_model()
        payment = Payment.objects.get(id=id)
        payment.release()
        return cls(status="Done") 
    

class Mutation(graphene.ObjectType):
    making_payment    = MakingPaymentMutation.Field()
    refunding_payment = RefundingPaymentMutation.Field()
    capturing_payment = CapturingPaymentMutation.Field()
    releasing_payment  = ReleasingPaymentMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)