# Generated by Django 2.1.5 on 2019-04-15 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooking', '0005_recipe_food_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='food_category',
            new_name='foodcategory',
        ),
    ]
