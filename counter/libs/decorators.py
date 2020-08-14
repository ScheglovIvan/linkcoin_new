from django.contrib.gis.geoip2 import GeoIP2

from . import client
from register.models import User
from counter.models import Visit
import datetime
from user_profile.models import Ref_Link
geo_loc = GeoIP2()

# def count_user(view):
#     def wrapper(request):
#         user_ip = client.get_client_ip(request)
#         try:
#             if request.user.is_authenticated:
#                 #Вызов исключения
#                 x = 1 / 0

#             startdate = datetime.datetime.now().strftime("%Y-%m-%d")
#             enddate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

#         #     visit = Visit.objects.get(ip=user_ip, date__range=[startdate, enddate])
#         # except Visit.DoesNotExist:
#             user_agent = request.user_agent

#             try:
#                 geo_data = geo_loc.city(user_ip)

#                 country = geo_data.get('country_name', '')
#                 region = geo_data.get('region', '')
#                 city = geo_data.get('city', '')

#                 if type(country) == type(None):
#                     country = ''

#                 if type(region) == type(None):
#                     region = ''

#                 if type(city) == type(None):
#                     city = ''

#             except Exception:
#                 country = region = city = ''

#             if user_agent.is_mobile:
#                 device_type = 'mobile'
#             elif user_agent.is_tablet:
#                 device_type = 'tablet'
#             else:
#                 device_type = 'pc'

#             cookies = request.COOKIES

#             inviter_id = cookies.get('inviter')

#             visit = Visit()

#             if inviter_id:
#                 if "ref" in request.GET:
#                     ref_link = Ref_Link.objects.filter(ref_link=request.GET["ref"], active=True)
#                     if ref_link:
#                         ref_link = ref_link[0]

#                         visit.ref_link = ref_link
#                         visit.user = ref_link.user

#             visit.ip = user_ip    
#             visit.device_type = device_type
#             visit.country = country
#             visit.region = region
#             visit.city = city
#             visit.save()
#         except:
#             pass

#         return view(request)

#     return wrapper


def newVisit(request, ref_link):
    user_ip = client.get_client_ip(request)
    try:
        if request.user.is_authenticated:
            #Вызов исключения
            x = 1 / 0

        startdate = datetime.datetime.now().strftime("%Y-%m-%d")
        enddate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        user_agent = request.user_agent

        try:
            geo_data = geo_loc.city(user_ip)

            country = geo_data.get('country_name', '')
            region = geo_data.get('region', '')
            city = geo_data.get('city', '')

            if type(country) == type(None):
                    country = ''

            if type(region) == type(None):
                    region = ''

            if type(city) == type(None):
                city = ''
                
        except Exception:
            country = region = city = ''

        if user_agent.is_mobile:
            device_type = 'mobile'
        elif user_agent.is_tablet:
            device_type = 'tablet'
        else:
            device_type = 'pc'


        visit = Visit()
                    
        visit.ref_link = ref_link
        visit.user = ref_link.user
        visit.ip = user_ip    
        visit.device_type = device_type
        visit.country = country
        visit.region = region
        visit.city = city
        visit.save()
    except:
        pass

