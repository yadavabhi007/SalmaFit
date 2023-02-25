from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Products, Notifications
from pyfcm import FCMNotification


@receiver(post_save, sender=Products)
def product_status_notification(sender, instance, created, **kwargs):
    if created:
        barcode = instance.barcode_number
        status = instance.status
        product_image = instance.product_image
        user = instance.user
        device_token = user.device_token
        Notifications.objects.create(title = barcode+' Added', عنوان =barcode+' اضافه کرده', barcode = barcode, product_image = product_image,
                                    message='Hello! Your product has been added to the system, please wait for review.',
                                    پیام='سلام! محصول شما به سیستم اضافه شده است، لطفا منتظر بررسی باشید.').recipient.add(user)
        if device_token:
            # push_service = FCMNotification(api_key="AAAAoMs1f38:APA91bHqV88hO4VWjZ3Vkj1xNaFN4H6AM2PvyWdOCmsRDDei_-IEMNjQ6MeqSyC7ukM4sqAoE_IvYPeGzj8ajnn9sCQleiQzX4UQGioZ1sl0ldlz6PjpaoR1W-2W7utcsqvUFM6PZ6EI")
            push_service = FCMNotification(api_key="AAAAj38eBRc:APA91bGYlxdKEKkdMSnoqZ-gR9fu8zvDX87rtbYaa1K7HLiOcFqzmDqZtrjMrW0mo5AP1HjFhJUaeHN2pSt-rRlQhD7pWYcW1Piiga6G6YySYt0wufqeMEh7n7mUYFAsYwNE83tPmRMD")
            # OR initialize with proxies
            # proxy_dict = {
            #           "http"  : "http://127.0.0.1",
            #           "https" : "http://127.0.0.1",
            #         }
            # push_service = FCMNotification(api_key="<api-key>", proxy_dict=proxy_dict)
            registration_id = device_token
            message_title = barcode+" Added"
            message_body = "Hello! Your product has been added to the system, please wait for review."
            result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
            # Send to multiple devices by passing a list of ids.
            # registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
            # message_title = barcode+' Added'
            # message_body = "Hello! Your product has an update, please check the details."
            # result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
            print (result)
    else:
        status = instance.status
        user = instance.user
        barcode = instance.barcode_number
        product_image = instance.product_image
        device_token = user.device_token
        if status == 'Not Clear Photos':
            Notifications.objects.create(title = barcode+' Photos Not Clear',  عنوان =barcode+' عکس ها واضح نیستند', barcode = barcode, product_image = product_image,
                                        message='Hello! Your product has an update, photos are not clear, please reupload.',
                                        پیام='سلام! محصول شما دارای به روز رسانی است، عکس ها واضح نیستند، لطفا دوباره آپلود کنید').recipient.add(user)
            if device_token:
                # push_service = FCMNotification(api_key="AAAAoMs1f38:APA91bHqV88hO4VWjZ3Vkj1xNaFN4H6AM2PvyWdOCmsRDDei_-IEMNjQ6MeqSyC7ukM4sqAoE_IvYPeGzj8ajnn9sCQleiQzX4UQGioZ1sl0ldlz6PjpaoR1W-2W7utcsqvUFM6PZ6EI")
                push_service = FCMNotification(api_key="AAAAj38eBRc:APA91bGYlxdKEKkdMSnoqZ-gR9fu8zvDX87rtbYaa1K7HLiOcFqzmDqZtrjMrW0mo5AP1HjFhJUaeHN2pSt-rRlQhD7pWYcW1Piiga6G6YySYt0wufqeMEh7n7mUYFAsYwNE83tPmRMD")
                registration_id = device_token
                message_title = barcode+" Photos Not Clear"
                message_body = "Hello! Your product has an update, photos are not clear, please reupload."
                result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
                print (result)
        else:
            Notifications.objects.create(title = barcode+' Reviewed',  عنوان =barcode+' بررسی شده', barcode = barcode, product_image = product_image,
                                        message='Hello! Your product has an update, please check the details.',
                                        پیام='سلام! محصول شما به‌روزرسانی دارد، لطفاً جزئیات را بررسی کنید.').recipient.add(user)
            if device_token:
                # push_service = FCMNotification(api_key="AAAAoMs1f38:APA91bHqV88hO4VWjZ3Vkj1xNaFN4H6AM2PvyWdOCmsRDDei_-IEMNjQ6MeqSyC7ukM4sqAoE_IvYPeGzj8ajnn9sCQleiQzX4UQGioZ1sl0ldlz6PjpaoR1W-2W7utcsqvUFM6PZ6EI")
                push_service = FCMNotification(api_key="AAAAj38eBRc:APA91bGYlxdKEKkdMSnoqZ-gR9fu8zvDX87rtbYaa1K7HLiOcFqzmDqZtrjMrW0mo5AP1HjFhJUaeHN2pSt-rRlQhD7pWYcW1Piiga6G6YySYt0wufqeMEh7n7mUYFAsYwNE83tPmRMD")
                registration_id = device_token
                message_title = barcode+" Reviewed"
                message_body = "Hello! Your product has an update, please check the details."
                result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,  message_body=message_body)
                print (result)


@receiver(pre_delete, sender=Products)
def product_status_notification(sender, instance, **kwargs):
    barcode = instance.barcode_number
    status = instance.status
    product_image = instance.product_image
    user = instance.user
    device_token = user.device_token
    Notifications.objects.create(title = barcode+' Removed', عنوان =barcode+' حذف شده', barcode = barcode, product_image = product_image,
                                message='Hello! Your product has been removed from the system.',
                                پیام='سلام! محصول شما از سیستم حذف شده است.').recipient.add(user)
    if device_token:
        # push_service = FCMNotification(api_key="AAAAoMs1f38:APA91bHqV88hO4VWjZ3Vkj1xNaFN4H6AM2PvyWdOCmsRDDei_-IEMNjQ6MeqSyC7ukM4sqAoE_IvYPeGzj8ajnn9sCQleiQzX4UQGioZ1sl0ldlz6PjpaoR1W-2W7utcsqvUFM6PZ6EI")
        push_service = FCMNotification(api_key="AAAAj38eBRc:APA91bGYlxdKEKkdMSnoqZ-gR9fu8zvDX87rtbYaa1K7HLiOcFqzmDqZtrjMrW0mo5AP1HjFhJUaeHN2pSt-rRlQhD7pWYcW1Piiga6G6YySYt0wufqeMEh7n7mUYFAsYwNE83tPmRMD")
        # OR initialize with proxies
        # proxy_dict = {
        #           "http"  : "http://127.0.0.1",
        #           "https" : "http://127.0.0.1",
        #         }
        # push_service = FCMNotification(api_key="<api-key>", proxy_dict=proxy_dict)
        registration_id = device_token
        message_title = barcode+" Removed"
        message_body = "Hello! Your product has been removed from the system."
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
        # Send to multiple devices by passing a list of ids.
        # registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
        # message_title = barcode+' Added'
        # message_body = "Hello! Your product has an update, please check the details."
        # result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)
        print (result)