import datetime
from sqlite3 import Date
from decimal import Decimal
from django.test import TestCase
from rest_framework.test import APIClient
from lumos.models import *
from model_bakery import baker

class ArtistViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_artist_list(self):
        artist = baker.make("lumos.Artist")

        r = self.client.get('/api/artists/')
        data = r.json()
        print(data)

        assert artist.id == data[0]['id']
        assert artist.first_name == data[0]['first_name']
        assert artist.last_name == data[0]['last_name']
        assert artist.phone == data[0]['phone']
        assert artist.balance == Decimal(data[0]['balance'])
        assert len(data) == 1

    def test_create_artist(self):
        r = self.client.post("/api/artists/",{
            "first_name": "Фамилия",
            "last_name": "Имя",
            "phone": "89641111111",
            "balance": 0
        })

        new_artist_id = r.json()['id']

        artistn = Artist.objects.all()
        assert len(artistn) == 1

        new_artist = Artist.objects.filter(id=new_artist_id).first()
        assert new_artist.first_name == 'Фамилия'
        assert new_artist.last_name == 'Имя'
        assert new_artist.phone == '89641111111'
        assert new_artist.balance == 0

    def test_delete_artist(self):
        artists = baker.make("Artist",10)
        r = self.client.get('/api/artists/')
        data = r.json()
        assert len(data) == 10

        artist_id_to_delete = artists[3].id
        r = self.client.delete(f'/api/artists/{artist_id_to_delete}/')
 
        r = self.client.get('/api/artists/')
        data = r.json()
        assert len(data) == 9

        assert artist_id_to_delete not in [i['id'] for i in data]

    def test_update_artist(self):
        artists = baker.make("Artist",10)
        artist: Artist = artists[2]

        r = self.client.get(f'/api/artists/{artist.id}/')
        data = r.json()
        assert data['first_name'] == artist.first_name

        r = self.client.put(f'/api/artists/{artist.id}/',{
            "first_name":"Валерия",
            "last_name": artist.last_name,
            "phone": artist.phone,
            "balance": artist.balance
        })
        assert r.status_code==200

        r = self.client.get(f'/api/artists/{artist.id}/')
        data = r.json()
        assert data['first_name'] == "Валерия"

        artist.refresh_from_db()
        assert data['first_name'] == artist.first_name

class TypeViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_type_list(self):
        type = baker.make("lumos.Type")

        r = self.client.get('/api/types/')
        data = r.json()
        print(data)

        assert type.id == data[0]['id']
        assert type.show_type == data[0]['show_type']
        assert len(data) == 1

    def test_create_type(self):
        r = self.client.post("/api/types/",{
            "show_type": "Бумажное шоу"
        })

        new_type_id = r.json()['id']

        typen = Type.objects.all()
        assert len(typen) == 1

        new_type = Type.objects.filter(id=new_type_id).first()
        assert new_type.show_type == 'Бумажное шоу'

    def test_delete_type(self):
        types = baker.make("Type",10)
        r = self.client.get('/api/types/')
        data = r.json()
        assert len(data) == 10

        type_id_to_delete = types[3].id
        r = self.client.delete(f'/api/types/{type_id_to_delete}/')
 
        r = self.client.get('/api/types/')
        data = r.json()
        assert len(data) == 9

        assert type_id_to_delete not in [i['id'] for i in data]

    def test_update_type(self):
        types = baker.make("Type",10)
        types: Type = types[2]

        r = self.client.get(f'/api/types/{types.id}/')
        data = r.json()
        assert data['show_type'] == types.show_type

        r = self.client.put(f'/api/types/{types.id}/',{
            "show_type":"Бумажное шоу"
        })
        assert r.status_code==200

        r = self.client.get(f'/api/types/{types.id}/')
        data = r.json()
        assert data['show_type'] == "Бумажное шоу"

        types.refresh_from_db()
        assert data['show_type'] == types.show_type

class ShowRateViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_showRate_list(self):
        st = baker.make("lumos.Type")
        showRate = baker.make("ShowRate",show_type = st)

        r = self.client.get('/api/showrates/')
        data = r.json()
        print(data)

        assert showRate.id == data[0]['id']
        assert showRate.show_type.id == data[0]['show_type']['id']
        assert showRate.rate == Decimal(data[0]['rate'])
        assert len(data) == 1

    def test_create_showRate(self):
        st = baker.make("lumos.Type")

        r = self.client.post("/api/showrates/",{
            "rate": 2000,
            "show_type": st.id,
        })  

        new_rate_id = r.json()['id']

        raten = ShowRate.objects.all()
        assert len(raten) == 1

        new_rate = ShowRate.objects.filter(id=new_rate_id).first()
        assert new_rate.rate == 2000
        assert new_rate.show_type == st

    def test_delete_showRate(self):
        showRates = baker.make("ShowRate",10)
        r = self.client.get('/api/showrates/')
        data = r.json()
        assert len(data) == 10

        showRate_id_to_delete = showRates[3].id
        r = self.client.delete(f'/api/showrates/{showRate_id_to_delete}/')
 
        r = self.client.get('/api/showrates/')
        data = r.json()
        assert len(data) == 9

        assert showRate_id_to_delete not in [i['id'] for i in data]

    def test_update_showRate(self):
        showRates = baker.make("ShowRate",10)
        showRate: ShowRate = showRates[2]

        r = self.client.get(f'/api/showrates/{showRate.id}/')
        data = r.json()
        assert Decimal(data['rate']) == Decimal(showRate.rate)

        r = self.client.put(f'/api/showrates/{showRate.id}/',{
            "rate":2000,
            "show_type": showRate.show_type.id
        })
        assert r.status_code==200

        r = self.client.get(f'/api/showrates/{showRate.id}/')
        data = r.json()
        assert Decimal(data['rate']) == 2000

        showRate.refresh_from_db()
        assert Decimal(data['rate']) == Decimal(showRate.rate)

class PerformanceViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_performance_list(self):
        t = baker.make("lumos.Type")
        performance = baker.make("Performance",type = t)

        r = self.client.get('/api/performances/')
        data = r.json()
        print(data)

        assert performance.id == data[0]['id']
        assert performance.type.id == data[0]['type']['id']
        assert performance.title == data[0]['title']
        assert performance.duration == data[0]['duration']
        assert performance.cnt_artists == data[0]['cnt_artists']
        assert performance.cost == Decimal(data[0]['cost'])
        assert len(data) == 1

    def test_create_performance(self):
        t = baker.make("lumos.Type")

        r = self.client.post("/api/performances/",{
            "cost": 2000,
            "type": t.id,
            "title": "Название",
            "duration": 5,
            "cnt_artists": 3,
        })  

        new_performance_id = r.json()['id']

        performancen = Performance.objects.all()
        assert len(performancen) == 1

        new_performance = Performance.objects.filter(id=new_performance_id).first()
        assert new_performance.cost == 2000
        assert new_performance.type == t
        assert new_performance.title == "Название"
        assert new_performance.duration == 5
        assert new_performance.cnt_artists == 3

    def test_delete_performance(self):
        performances = baker.make("Performance",10)
        r = self.client.get('/api/performances/')
        data = r.json()
        assert len(data) == 10

        performance_id_to_delete = performances[3].id
        r = self.client.delete(f'/api/performances/{performance_id_to_delete}/')
 
        r = self.client.get('/api/performances/')
        data = r.json()
        assert len(data) == 9

        assert performance_id_to_delete not in [i['id'] for i in data]

    def test_update_performance(self):
        performances = baker.make("Performance",10)
        performance: Performance = performances[2]

        r = self.client.get(f'/api/performances/{performance.id}/')
        data = r.json()
        assert Decimal(data['cost']) == Decimal(performance.cost)

        r = self.client.put(f'/api/performances/{performance.id}/',{
            "cost":13000,
            "type": performance.type.id,
            "title": performance.title,
            "duration": performance.duration,
            "cnt_artists": performance.cnt_artists
        })
        assert r.status_code==200

        r = self.client.get(f'/api/performances/{performance.id}/')
        data = r.json()
        assert Decimal(data['cost']) == 13000

        performance.refresh_from_db()
        assert Decimal(data['cost']) == Decimal(performance.cost)

class ArtistPerformanceViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_artistperformance_list(self):
        a = baker.make("lumos.Artist")
        p = baker.make("lumos.Performance")
        r = baker.make("lumos.ShowRate")
        artistperformance = baker.make("ArtistPerformance",artist = a, performance = p, rate = r)

        r = self.client.get('/api/artistperformances/')
        data = r.json()
        print(data)

        assert artistperformance.id == data[0]['id']
        assert artistperformance.artist.id == data[0]['artist']['id']
        assert artistperformance.performance.id == data[0]['performance']['id']
        assert artistperformance.rate.id == data[0]['rate']['id']
        assert len(data) == 1

    def test_create_artistperformance(self):
        a = baker.make("lumos.Artist")
        p = baker.make("lumos.Performance")
        rt = baker.make("lumos.ShowRate")

        r = self.client.post("/api/artistperformances/",{
            "artist": a.id,
            "performance": p.id,
            "rate": rt.id
        })  

        new_artistperformance_id = r.json()['id']

        artistperformancen = ArtistPerformance.objects.all()
        assert len(artistperformancen) == 1

        new_artistperformance = ArtistPerformance.objects.filter(id=new_artistperformance_id).first()
        assert new_artistperformance.artist == a
        assert new_artistperformance.performance == p
        assert new_artistperformance.rate == rt

    def test_delete_artistperformance(self):
        artistperformances = baker.make("ArtistPerformance",10)
        r = self.client.get('/api/artistperformances/')
        data = r.json()
        assert len(data) == 10

        artistperformance_id_to_delete = artistperformances[3].id
        r = self.client.delete(f'/api/artistperformances/{artistperformance_id_to_delete}/')
 
        r = self.client.get('/api/artistperformances/')
        data = r.json()
        assert len(data) == 9

        assert artistperformance_id_to_delete not in [i['id'] for i in data]

    def test_update_artistperformance(self):
        artistperformances = baker.make("ArtistPerformance",10)
        artistperformance: ArtistPerformance = artistperformances[2]

        r = self.client.get(f'/api/artistperformances/{artistperformance.id}/')
        data = r.json()
        assert Decimal(data['rate']['rate']) == Decimal(artistperformance.rate.rate)

        r = self.client.put(f'/api/artistperformances/{artistperformance.id}/',{
            "rate":2,
            "artist": artistperformance.artist.id,
            "performance": artistperformance.performance.id
        })
        assert r.status_code==200

        r = self.client.get(f'/api/artistperformances/{artistperformance.id}/')
        data = r.json()
        assert data['rate']['id'] == 2

        artistperformance.refresh_from_db()
        assert Decimal(data['rate']['rate']) == Decimal(artistperformance.rate.rate)

class OrderViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_order_list(self):
        p = baker.make("lumos.Performance")
        order = baker.make("Order",performance = p)

        r = self.client.get('/api/orders/')
        data = r.json()
        print(data)

        assert order.id == data[0]['id']
        assert order.performance.id == data[0]['performance']['id']
        assert str(order.date) == data[0]['date']
        assert order.location == data[0]['location']
        assert order.comment == data[0]['comment']
        assert order.completed == data[0]['completed']
        assert order.amount == Decimal(data[0]['amount'])
        assert len(data) == 1

    def test_create_order(self):
        p = baker.make("lumos.Performance")

        r = self.client.post("/api/orders/",{
            "date": "2025-05-21",
            "performance": p.id,
            "location": "Название",
            "comment": "Комментарий",
            "amount": 30000,
            "completed": False
        })  

        new_order_id = r.json()['id']

        ordern = Order.objects.all()
        assert len(ordern) == 1

        new_order = Order.objects.filter(id=new_order_id).first()
        assert str(new_order.date) == "2025-05-21"
        assert new_order.performance == p
        assert new_order.location == "Название"
        assert new_order.comment == "Комментарий"
        assert new_order.amount == 30000
        assert new_order.completed == False

    def test_delete_order(self):
        orders = baker.make("Order",10)
        r = self.client.get('/api/orders/')
        data = r.json()
        assert len(data) == 10

        order_id_to_delete = orders[3].id
        r = self.client.delete(f'/api/orders/{order_id_to_delete}/')
 
        r = self.client.get('/api/orders/')
        data = r.json()
        assert len(data) == 9

        assert order_id_to_delete not in [i['id'] for i in data]

    def test_update_order(self):
        orders = baker.make("Order",10)
        order: Order = orders[2]

        r = self.client.get(f'/api/orders/{order.id}/')
        data = r.json()
        assert data['location'] == order.location

        r = self.client.put(f'/api/orders/{order.id}/',{
            "date": order.date,
            "performance": order.performance.id,
            "location": "Название",
            "comment": order.comment,
            "amount": order.amount,
            "completed": order.completed
        })
        assert r.status_code==200

        r = self.client.get(f'/api/orders/{order.id}/')
        data = r.json()
        assert data['location'] == "Название"

        order.refresh_from_db()
        assert data['location'] == order.location

class EarningViewsetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_earning_list(self):
        a = baker.make("lumos.Artist")
        o = baker.make("lumos.Order")
        earning = baker.make("Earning",artist = a, order = o)

        r = self.client.get('/api/earnings/')
        data = r.json()
        print(data)

        assert earning.id == data[0]['id']
        assert earning.artist.id == data[0]['artist']['id']
        assert earning.order.id == data[0]['order']['id']
        assert earning.amount == Decimal(data[0]['amount'])
        assert earning.paid == data[0]['paid']
        assert len(data) == 1

    def test_create_earning(self):
        a = baker.make("lumos.Artist")
        o = baker.make("lumos.Order")

        r = self.client.post("/api/earnings/",{
            "artist": a.id,
            "order": o.id,
            "amount": 2000,
            "paid": False,
        })  

        new_earning_id = r.json()['id']

        earningn = Earning.objects.all()
        assert len(earningn) == 1

        new_earning = Earning.objects.filter(id=new_earning_id).first()
        assert new_earning.artist == a
        assert new_earning.order == o
        assert new_earning.amount == 2000
        assert new_earning.paid == False

    def test_delete_earning(self):
        earnings = baker.make("Earning",10)
        r = self.client.get('/api/earnings/')
        data = r.json()
        assert len(data) == 10

        earning_id_to_delete = earnings[3].id
        r = self.client.delete(f'/api/earnings/{earning_id_to_delete}/')
 
        r = self.client.get('/api/earnings/')
        data = r.json()
        assert len(data) == 9

        assert earning_id_to_delete not in [i['id'] for i in data]

    def test_update_earning(self):
        earnings = baker.make("Earning",10)
        earning: Earning = earnings[2]

        r = self.client.get(f'/api/earnings/{earning.id}/')
        data = r.json()
        assert Decimal(data['amount']) == Decimal(earning.amount)

        r = self.client.put(f'/api/earnings/{earning.id}/',{
            "amount": 1500,
            "artist": earning.artist.id,
            "order": earning.order.id,
            "paid": earning.paid
        })
        assert r.status_code==200

        r = self.client.get(f'/api/earnings/{earning.id}/')
        data = r.json()
        assert Decimal(data['amount']) == 1500

        earning.refresh_from_db()
        assert  Decimal(data['amount']) == Decimal(earning.amount)