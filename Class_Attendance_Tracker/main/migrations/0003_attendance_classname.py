# Generated by Django 4.1 on 2022-10-25 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_student_netattendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='classname',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.classname'),
            preserve_default=False,
        ),
    ]
