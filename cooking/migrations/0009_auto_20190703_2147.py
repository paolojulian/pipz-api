# Generated by Django 2.1.5 on 2019-07-03 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooking', '0008_auto_20190424_0127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='duration_from',
            new_name='cooking_time_from',
        ),
        migrations.RenameField(
            model_name='recipe',
            old_name='duration_to',
            new_name='cooking_time_to',
        ),
        migrations.RenameField(
            model_name='recipeingredient',
            old_name='description',
            new_name='details',
        ),
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='image_path',
            field=models.CharField(default=None, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='prep_time_from',
            field=models.PositiveIntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='recipe',
            name='prep_time_to',
            field=models.PositiveIntegerField(blank=True, default=5),
        ),
    ]