# Generated by Django 4.1.7 on 2023-03-12 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_projects_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projects',
            options={'verbose_name': '项目表', 'verbose_name_plural': '项目表'},
        ),
        migrations.AlterField(
            model_name='projects',
            name='id',
            field=models.AutoField(help_text='ID主键', primary_key=True, serialize=False, verbose_name='ID主键'),
        ),
    ]