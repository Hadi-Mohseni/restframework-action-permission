from django.apps import apps


def create_permission(sender, **kwargs):
    try:
        Permission = apps.get_model("auth", "Permission")
        ContentType = apps.get_model("contenttypes", "ContentType")
    except LookupError:
        return

    for content_type in ContentType.objects.all():
        model_name = content_type.model_class()._meta.model_name
        codename = "list_{}".format(model_name)
        if not Permission.objects.filter(
            content_type_id=content_type.id,
            codename=codename,
        ).exists():
            name = "Can list {}".format(model_name)
            Permission.objects.create(
                name=name, codename=codename, content_type_id=content_type.id
            )