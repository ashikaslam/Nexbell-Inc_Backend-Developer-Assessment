# Generated by Django 5.1.1 on 2024-10-02 19:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mobilephone', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('phone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mobilephone.phone')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_wish', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-id'],
                'constraints': [models.UniqueConstraint(fields=('user', 'phone'), name='unique_user_phone')],
            },
        ),
    ]
