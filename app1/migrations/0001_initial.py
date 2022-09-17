# Generated by Django 3.2.5 on 2021-09-19 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app2', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_score', models.PositiveIntegerField(default=0)),
                ('taken_apt_test', models.BooleanField(default=False)),
                ('taken_personality_test', models.BooleanField(default=False)),
                ('personality', models.ManyToManyField(blank=True, to='app2.PersonalityType')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
