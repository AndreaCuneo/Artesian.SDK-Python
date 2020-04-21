from Artesian import *

cfg = ArtesianConfig("baseaddr","apikey")

qs = GMEPublicOfferService(cfg)


test1 = qs.createQuery() \
    .forDate("2020-04-01") \
    .forMarket([Market.MGP]) \
    .forStatus(Status.ACC) \
    .forPurpose(Purpose.BID) \
    .forZone([Zone.NORD]) \
    .withPagination(1,10) \
    .execute()


res = test1

