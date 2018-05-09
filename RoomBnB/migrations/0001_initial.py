# Generated by Django 2.0.4 on 2018-05-09 10:22

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
                ('text', models.TextField()),
                ('date_signed', models.DateField(auto_now_add=True)),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='landlord', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Flat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=100)),
                ('address', models.TextField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('picture', models.ImageField(default='flat/generic/default.jpg', upload_to='flat/')),
            ],
        ),
        migrations.CreateModel(
            name='FlatProperties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elevator', models.BooleanField(default=False, verbose_name='Elevator')),
                ('washdisher', models.BooleanField(default=False, verbose_name='Dishwasher')),
                ('flat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='RoomBnB.Flat')),
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
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='profile/generic/default.png', upload_to='profile/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
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
                ('picture', models.ImageField(default='room/generic/default.jpg', upload_to='room/')),
                ('belong_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='RoomBnB.Flat')),
                ('temporal_owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RoomProperties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balcony', models.BooleanField(default=False, verbose_name='Balcony')),
                ('window', models.BooleanField(default=False, verbose_name='Window')),
                ('air_conditioner', models.BooleanField(default=False, verbose_name='Air conditioner')),
                ('bed', models.CharField(choices=[('1', 'Couple'), ('2', 'Single'), ('3', 'Sofa'), ('4', 'None')], default=2, max_length=1, verbose_name='Bed')),
                ('room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='RoomBnB.Room')),
            ],
        ),
        migrations.CreateModel(
            name='UserProperties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('smoker', models.BooleanField(default=False, verbose_name='Smoker')),
                ('pets', models.BooleanField(default=False, verbose_name='Pets')),
                ('sporty', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1, verbose_name='Sporty')),
                ('gamer', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1, verbose_name='Gamer')),
                ('sociable', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1, verbose_name='Sociable')),
                ('degree', models.CharField(choices=[('1', 'Nursing'), ('2', 'Computer Engineering'), ('3', 'Medicine'), ('4', 'Biology'), ('5', 'Architecture')], max_length=1, verbose_name='Degree')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='RoomBnB.Profile')),
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
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rent_requests', to='RoomBnB.Room'),
        ),
        migrations.AddField(
            model_name='rentrequest',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rent_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='flat',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flats', to='RoomBnB.Profile'),
        ),
        migrations.AddField(
            model_name='contract',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='RoomBnB.Room'),
        ),
        migrations.AddField(
            model_name='contract',
            name='tenant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tenant', to=settings.AUTH_USER_MODEL),
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
