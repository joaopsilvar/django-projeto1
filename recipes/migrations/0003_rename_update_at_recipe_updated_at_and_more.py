# Generated by Django 5.0 on 2024-03-19 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_category_alter_recipe_cover_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='update_at',
            new_name='updated_at',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cover',
            field=models.ImageField(blank=True, default='', upload_to='recipes/covers/%Y/%m/%d/'),
        ),
    ]
