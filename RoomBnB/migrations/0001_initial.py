# Generated by Django 2.0.2 on 2018-03-22 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='')),
                ('date_signed', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=16)),
                ('cvv', models.CharField(max_length=3)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=100)),
                ('address', models.TextField(max_length=100)),
                ('description', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('contract', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='RoomBnB.Contract')),
                ('credit_card', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='RoomBnB.CreditCard')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smoker', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('neat', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('sporty', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('gamer', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('sociable', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('active', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
                ('degree', models.CharField(choices=[('1', 'Enfermeria'), ('2', 'Ing. Informatica'), ('3', 'Medicina'), ('4', 'Biologia'), ('5', 'Arquitectura')], max_length=1)),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='RoomBnB.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='RentRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('accepted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('date', models.DateField(auto_now_add=True)),
                ('rating', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=500)),
                ('price', models.FloatField()),
                ('belong_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RoomBnB.Flat')),
                ('temporal_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FlatImage',
            fields=[
                ('image_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='RoomBnB.Image')),
            ],
            bases=('RoomBnB.image',),
        ),
        migrations.CreateModel(
            name='FlatReview',
            fields=[
                ('review_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='RoomBnB.Review')),
            ],
            bases=('RoomBnB.review',),
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('image_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='RoomBnB.Image')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RoomBnB.Room')),
            ],
            bases=('RoomBnB.image',),
        ),
        migrations.CreateModel(
            name='RoomReview',
            fields=[
                ('review_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='RoomBnB.Review')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RoomBnB.Room')),
            ],
            bases=('RoomBnB.review',),
        ),
        migrations.CreateModel(
            name='UserReview',
            fields=[
                ('review_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='RoomBnB.Review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('RoomBnB.review',),
        ),
        migrations.AddField(
            model_name='rentrequest',
            name='requested',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RoomBnB.Room'),
        ),
        migrations.AddField(
            model_name='rentrequest',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='flat',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flats', to='RoomBnB.Profile'),
        ),
        migrations.AddField(
            model_name='contract',
            name='landlord',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='landlord', to='RoomBnB.Profile'),
        ),
        migrations.AddField(
            model_name='contract',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='RoomBnB.Room'),
        ),
        migrations.AddField(
            model_name='contract',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tenant', to='RoomBnB.Profile'),
        ),
        migrations.AddField(
            model_name='flatreview',
            name='flat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RoomBnB.Flat'),
        ),
        migrations.AddField(
            model_name='flatimage',
            name='flat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RoomBnB.Flat'),
        ),
    ]
