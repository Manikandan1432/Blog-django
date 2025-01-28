from django.contrib.auth.models import Group, Permission
def create_groups_and_permissions(sender, **kwargs):
    try:
        readers_group,created = Group.objects.get_or_create(name='Readers')
        authors_group,created = Group.objects.get_or_create(name='Authors')
        editors_group,created = Group.objects.get_or_create(name='Editors')

        readers_permissions = [
            Permission.objects.get(codename='view_datas')
        ]

        authors_permissions = [
            Permission.objects.get(codename='view_datas'),
            Permission.objects.get(codename='change_datas'),
            Permission.objects.get(codename='add_datas'),
            Permission.objects.get(codename='delete_datas')
        ]

        permissions, created = Permission.objects.get_or_create(codename='can_publish', content_type_id=8, name="can_publish_datas")
        editors_permissions = [
            permissions,
            Permission.objects.get(codename='view_datas'),
            Permission.objects.get(codename='change_datas'),
            Permission.objects.get(codename='add_datas'),
            Permission.objects.get(codename='delete_datas')
        ]


        readers_group.permissions.set(readers_permissions)
        authors_group.permissions.set(authors_permissions)
        editors_group.permissions.set(editors_permissions)

        print('groups and permissions created successfully')

    except Exception as e:
        print(f'the error occured {e}')
