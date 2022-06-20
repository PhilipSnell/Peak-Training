import myfitnesspal as mfp
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model

from api.models import MyFitnessPal, MyFitnessPalFields, TrackingTextField, TrackingTextValue

User = get_user_model()

def sync_mfp():
    clients = User.objects.all()

    for client in clients:
        try:
            mfp_details = MyFitnessPal.objects.get(user=client)
            mfpclient = mfp.Client(mfp_details.username, mfp_details.password)

            mfp_fields = MyFitnessPalFields.objects.get(id=1).fields.all().order_by('id')
            date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            days = [date]
            fields = MyFitnessPalFields.objects.get(id=1).fields.all()
            for i in range(1, 7):
                days.append(date-timedelta(days=i))
            for day in days:
                data=mfpclient.get_date(day.year,day.month,day.day)
                print(data)
                try:
                    try:
                        calories = TrackingTextValue.objects.get(client=client, date=day, field_id=mfp_fields[0].id)
                        calories.value = data.totals['calories']
                        calories.save()
                    except TrackingTextValue.DoesNotExist:
                        calories = TrackingTextValue(
                            value=data.totals['calories'],
                            client=client,
                            field_id=mfp_fields[0].id,
                            date=day
                        )
                        calories.save()
                        fields[0].values.add(calories)
                        fields[0].save()
                except KeyError:
                    print(KeyError)
                    pass
                try:
                    try:
                        protein = TrackingTextValue.objects.get(client=client, date=day, field_id=mfp_fields[1].id)
                        protein.value = data.totals['protein']
                        protein.save()
                    except TrackingTextValue.DoesNotExist:
                        protein = TrackingTextValue(
                            value=data.totals['protein'],
                            client=client,
                            field_id=mfp_fields[1].id,
                            date=day
                        )
                        protein.save()
                        fields[1].values.add(protein)
                        fields[1].save()
                except KeyError:
                    print(KeyError)
                    pass
                try:
                    try:
                        carbs = TrackingTextValue.objects.get(client=client, date=day, field_id=mfp_fields[2].id)
                        carbs.value = data.totals['carbs']
                        carbs.save()
                    except TrackingTextValue.DoesNotExist:
                        carbs = TrackingTextValue(
                            value=data.totals['carbohydrates'],
                            client=client,
                            field_id=mfp_fields[2].id,
                            date=day
                        )
                        carbs.save()
                        fields[2].values.add(carbs)
                        fields[2].save()
                except KeyError:
                    print(KeyError)
                    pass
                try:
                    try:
                        fat = TrackingTextValue.objects.get(client=client, date=day, field_id=mfp_fields[3].id)
                        fat.value = data.totals['fat']
                        fat.save()
                    except TrackingTextValue.DoesNotExist:
                        fat = TrackingTextValue(
                            value=data.totals['fat'],
                            client=client,
                            field_id=mfp_fields[3].id,
                            date=day
                        )
                        fat.save()
                        fields[3].values.add(fat)
                        fields[3].save()
                except KeyError:
                    print(KeyError)
                    pass
                try:
                    try:
                        sodium = TrackingTextValue.objects.get(client=client, date=day, field_id=mfp_fields[4].id)
                        sodium.value = data.totals['sodium']
                        sodium.save()
                    except TrackingTextValue.DoesNotExist:
                        sodium = TrackingTextValue(
                            value=data.totals['sodium'],
                            client=client,
                            field_id=mfp_fields[4].id,
                            date=day
                        )
                        sodium.save()
                        fields[4].values.add(sodium)
                        fields[4].save()
                except KeyError:
                    print(KeyError)
                    pass
                try:
                    try:
                        sodium = TrackingTextValue.objects.get(client=client, date=day, field_id=mfp_fields[5].id)
                        sodium.value = data.totals['sodium']
                        sodium.save()
                    except TrackingTextValue.DoesNotExist:
                        sugar = TrackingTextValue(
                            value=data.totals['sugar'],
                            client=client,
                            field_id=mfp_fields[5].id,
                            date=day
                        )
                        sugar.save()
                        fields[5].values.add(sugar)
                        fields[5].save()
                except KeyError:
                    print(KeyError)
                    pass
        except:
            print("Passed")