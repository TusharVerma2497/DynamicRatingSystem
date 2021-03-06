# Generated by Django 3.0.4 on 2020-08-08 11:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import unixtimestampfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='rating',
            fields=[
                ('value', models.FloatField(validators=[django.core.validators.MaxValueValidator(10.0), django.core.validators.MinValueValidator(0.1)])),
                ('epoch', unixtimestampfield.fields.UnixTimeStampField(default=django.utils.timezone.now)),
                ('lastUpdated', unixtimestampfield.fields.UnixTimeStampField(default=django.utils.timezone.now)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movies')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'movie')},
            },
        ),
    ]
