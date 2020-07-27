# Generated by Django 3.0.3 on 2020-07-27 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DesignerApp', '0003_auto_20200716_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.CharField(max_length=256)),
                ('child', models.CharField(max_length=256)),
                ('assistant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relationships', to='DesignerApp.Assistant')),
            ],
        ),
    ]
