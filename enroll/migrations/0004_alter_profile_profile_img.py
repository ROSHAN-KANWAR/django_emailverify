# Generated by Django 3.2.3 on 2021-06-12 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enroll', '0003_alter_profile_profile_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(blank=True, default='team_3.jpg', null=True, upload_to=''),
        ),
    ]
