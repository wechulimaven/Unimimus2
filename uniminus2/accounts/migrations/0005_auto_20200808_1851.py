# Generated by Django 3.1 on 2020-08-08 15:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200808_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='userregistration',
            name='institution_qualification',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='userregistration',
            name='kcse_mean_grade',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='userregistration',
            name='other_institution_attended',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.CreateModel(
            name='Qualifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.userregistration')),
            ],
        ),
    ]
