# Generated by Django 4.1.7 on 2023-03-15 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0004_remove_goal_metric_goal_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='limit',
        ),
        migrations.AddField(
            model_name='goal',
            name='enddate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='goal',
            name='type',
            field=models.CharField(choices=[('FI', 'Financial Goal'), ('FQ', 'Frequency Goal')], max_length=2),
        ),
        migrations.CreateModel(
            name='GoalProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress', models.FloatField()),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.goal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]