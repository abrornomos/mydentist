# Generated by Django 3.2 on 2021-09-29 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dentist', '0003_alter_appointment_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='FISh')),
                ('duration', models.TimeField(verbose_name='Xizmat davomiyligi')),
                ('price', models.IntegerField(verbose_name='Xizmat narxi')),
                ('dentist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dentist.dentist', verbose_name='Tish shifokori')),
            ],
            options={
                'verbose_name': 'Xizmat',
                'verbose_name_plural': 'Xizmatlar',
            },
        ),
    ]
