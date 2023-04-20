# Generated by Django 4.1.7 on 2023-04-12 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_postdislike_commentdislike'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentdislike',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_dislikes', to='blog.comment'),
        ),
        migrations.AlterField(
            model_name='commentlike',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_likes', to='blog.comment'),
        ),
    ]
